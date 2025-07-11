#app/blueprints/feed/reparse_helpers.py

from app.services.feed_parser import parse_feed
from app.utils.request_logger import get_logger, log_database_operation
from app.utils.security_logger import log_network_event, log_error
from app.models.feed import Feed
from app.models.feed import FeedLog
from datetime import datetime
from app.models.item import Item, ItemFlagStatus
from app.extensions import db
from app.models.channel import Channel
from faker import Faker
import random
from app.utils.helpers import get_flag_status_id

logger = get_logger(__name__)
fake = Faker()

def reparse_feed_url(feed_url: str) -> dict:
    # 1 - reparse the feed
    logger.info(f"Attempting to fetch RSS feed from URL: {feed_url}")
    log_network_event(logger, "RSS_FETCH_START", f"URL: {feed_url}")
    return parse_feed(feed_url)


def handle_bozo_parse_error(feed: Feed, parsed_data: dict) -> dict:
    # 2 if bozo true then mark the feed as error and log
    error_msg = (
        str(parsed_data.get("feed", {}).get("bozo_exception"))
        if isinstance(parsed_data, dict) and "feed" in parsed_data
        else "Unknown parse error"
    )
    
    log_network_event(logger, "RSS_PARSE_ERROR", f"URL: {feed.url}, Error: {error_msg}")
    feed.feed_flag_status_id = get_flag_status_id("parse_error") # status tracking

    feed_log = FeedLog(
        feed_id=feed.id,
        parse_errors=1,
        last_finished_parse_time=datetime.utcnow()
    )
    db.session.add(feed_log)
    log_database_operation(logger, "CREATE", "feed_logs", None)

    feed.is_parsing = False
    db.session.commit()

    logger.warning(f"Parse failed for Feed ID: {feed.id} — Error: {error_msg}")
    return {
        "status": "failed",
        "error": error_msg,
        "feed_id": feed.id
    }


def create_or_update_channel(parsed_data: dict, feed: Feed) -> Channel:
    """
    Create or update channel based on parsed feed data
    """
    channel = db.session.query(Channel).filter_by(feed_id=feed.id).first()
    channel_data = parsed_data.get("channel", {})
    title = channel_data.get("title") or "Untitled Feed"

    if not channel:
        channel = Channel(
            feed_id=feed.id,
            id_text=fake.unique.user_name()[:15],
            podcast_index_id=random.randint(1000000, 9999999),
            title=title,
            has_podcast_index_value=False,
            has_value_time_splits=False
        )
        log_database_operation(logger, "CREATE", "channels", None)
    else:
        log_database_operation(logger, "UPDATE", "channels", channel.id)
        channel.title = title

    db.session.add(channel)
    db.session.flush()  # makes sure channel.id is available
    return channel


def insert_items(items_data: list, channel: Channel):
    """
    Insert only new items based on GUID (no wipe)
    """
    if not items_data:
        logger.warning(f"No items provided for Channel ID: {channel.id}")
        return

    existing_guids = {
        i[0] for i in db.session.query(Item.guid).filter_by(channel_id=channel.id).all()
    }
    new_items = [item for item in items_data if item["guid"] not in existing_guids]

    if not new_items:
        logger.info(f"No new items to insert for Channel ID: {channel.id}")
        return

    active_status = db.session.query(ItemFlagStatus).filter_by(status="active").first()
    item_flag_status_id = active_status.id if active_status else 1  # fallback default

    for item_data in items_data:
        item = Item(
            id_text=fake.unique.user_name()[:15],
            channel_id=channel.id,
            guid=item_data["guid"],
            title=item_data["title"],
            pub_date=item_data["pub_date"],
            guid_enclosure_url=item_data["guid_enclosure_url"],
            item_flag_status_id=item_flag_status_id
        )
        db.session.add(item)

    log_database_operation(logger, "CREATE", "items", f"batch_{len(new_items)}")


def create_successful_feed_log(feed_id: int, http_status: int = 200):
    #add new success log
    feed_log = FeedLog(
        feed_id=feed_id,
        last_http_status=http_status or 200,  # fallback to 200 if None
        last_good_http_status_time=datetime.utcnow(),
        last_finished_parse_time=datetime.utcnow()
    )
    db.session.add(feed_log)
    log_database_operation(logger, "CREATE", "feed_logs", None)

