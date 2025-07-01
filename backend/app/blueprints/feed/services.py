# app/blueprints/feed/services.py

#NOT: Refactor into classes only if logic grows more complex for now stand alonw functions are already modular since it's in the same file

from app.models.feed import Feed, FeedLog, FeedFlagStatus
from app.models.channel import Channel
from app.models.item import Item, ItemFlagStatus
from app.extensions import db
from app.utils.logger import get_logger, log_database_operation
from app.utils.utils import get_flag_status_id
from app.utils.query_helpers import paginate_query, apply_sorting
from app.utils.error_exceptions import NotFoundError, ValidationError, DatabaseError
from app.services.feed_parser import parse_feed
from datetime import datetime
from faker import Faker
import random
import xml.etree.ElementTree as ET

fake = Faker()
logger = get_logger(__name__)


def parse_and_update_feed(feed_id: int):
    feed = db.session.get(Feed, feed_id)
    if not feed:
        raise NotFoundError("Feed not found")
    
    logger.info(f"Starting reparse for Feed ID: {feed.id}, URL: {feed.url}")
    log_database_operation(logger, "UPDATE", "feeds", feed_id)
    
    # mark and commit early feed is being parsed so flag is saved even if crash happens
    feed.is_parsing = True # so i dont touch anything if feed is broken no partial db save 
    db.session.commit()
    
    try:
        # 1 - reparse the feed
        parsed_data = parse_feed(feed.url) 
        # 2- if bozo true then mark the feed as error and log
        if parsed_data["feed"]["bozo"]:
            feed.feed_flag_status_id = get_flag_status_id("parse_error") # status trakcing
            
            feed_log = FeedLog(
                feed_id=feed.id,
                parse_errors=1,
                last_finished_parse_time=datetime.utcnow()
            )
            db.session.add(feed_log)
            log_database_operation(logger, "CREATE", "feed_logs", None)

            feed.is_parsing = False
            db.session.commit()

            logger.warning(f"Parse failed for Feed ID: {feed.id} — Error: {parsed_data['feed']['bozo_exception']}")
            return {"status": "parse_failed", "error": str(parsed_data["feed"]["bozo_exception"])}

        # If bozo is False, mark as active
        feed.feed_flag_status_id = get_flag_status_id("active")
        
        # protect db against abuse
        if len(parsed_data["items"]) > 500:
            logger.warning(f"Too many items in feed ID {feed.id}: {len(parsed_data['items'])}")
            raise ValidationError("Feed contains too many items. Limit is 500.")

        #  Handle channel creation/update
        channel = db.session.query(Channel).filter_by(feed_id=feed.id).first()
        
        # todo: add these if/else blocks back in in prod stage (kanal yarattigin alttaki kismi sil)
        # if not channel:
        #     channel = Channel(feed_id=feed.id)
        #     log_database_operation(logger, "CREATE", "channels", None)
        # else:
        #     log_database_operation(logger, "UPDATE", "channels", channel.id)
        
        channel = db.session.query(Channel).filter_by(feed_id=feed.id).first()

        if not channel:
            channel = Channel(
                feed_id=feed.id,
                id_text=fake.unique.user_name()[:15],
                podcast_index_id=random.randint(1000000, 9999999),
                title=parsed_data["channel"]["title"] or "Untitled Feed",
                has_podcast_index_value=False,
                has_value_time_splits=False
            )
            log_database_operation(logger, "CREATE", "channels", None)
        else:
            log_database_operation(logger, "UPDATE", "channels", channel.id)
            channel.title = parsed_data["channel"]["title"] or channel.title

        db.session.add(channel)
        db.session.flush()  # makes sure channel.id is available
        
        # Wipe and re-insert items
        deleted_count = db.session.query(Item).filter_by(channel_id=channel.id).count()
        db.session.query(Item).filter_by(channel_id=channel.id).delete()
        if deleted_count > 0:
            log_database_operation(logger, "DELEE", "items", f"batch_{deleted_count}")
        
        if not parsed_data["items"]:
            logger.warning(f"No items found for Feed ID: {feed.id}")
            # Create/insert new items
        for item_data in parsed_data["items"]:
            # todo: add the item creation back in in prod stage 
            # item = Item(
            #     channel_id=channel.id,
            #     guid=item_data["guid"],
            #     title=item_data["title"],
            #     pub_date=item_data["pub_date"],
            #     guid_enclosure_url=item_data["guid_enclosure_url"]
            # )
            # db.session.add(item) 
            item_flag_status_id = 1  # fallback default (assuming 1 = active)
            active_status = db.session.query(ItemFlagStatus).filter_by(status="active").first()
            if active_status:
                item_flag_status_id = active_status.id

            item = Item(
                id_text=fake.unique.user_name()[:15],  # fallback for required field
                channel_id=channel.id,
                guid=item_data["guid"],
                title=item_data["title"],
                pub_date=item_data["pub_date"],
                guid_enclosure_url=item_data["guid_enclosure_url"],
                item_flag_status_id=item_flag_status_id
            )
            db.session.add(item)

        if parsed_data["items"]:
            log_database_operation(logger, "CREATE", "items", f"batch_{len(parsed_data['items'])}")
        
        # add new success log
        feed_log = FeedLog(
            feed_id=feed.id,
            last_http_status=200,
            last_good_http_status_time=datetime.utcnow(),
            last_finished_parse_time=datetime.utcnow()
        )
        db.session.add(feed_log)
        log_database_operation(logger, "CREATE", "feed_logs", None) 
        
        feed.is_parsing = False
        feed.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Succesxsfully reparsed Feed ID: {feed.id}, Channel ID: {channel.id}, Items: {len(parsed_data['items'])}")
        return {
            "status": "success",
            "feed_id": feed.id,
            "channel_id": channel.id,
            "item_count": len(parsed_data["items"])
        }
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during feed reparse: {str(e)}")
        raise DatabaseError(f"Failed to reparse feed: {str(e)}")
    finally:
        feed.is_parsing = False
        try:
            db.session.commit()
        except:
            db.session.rollback()
        

def get_all_feeds(page=1, limit=10, parsing_priority=None, is_parsing=None, status=None, sort_by="id", sort_order="desc", search=None):
    """
    Get all feeds with pagination and return structured response
    
    Args:
        page (int): Page number (1-based)
        limit (int): Number of items per page
    
    Returns:
        dict: Response with data and meta information
    """
    try:
        # Create base query
        query = db.session.query(Feed).join(FeedFlagStatus).order_by(Feed.id.desc())
        log_database_operation(logger, "READ", "feeds", f"page_{page}")
             
        if status:
            query = query.filter(FeedFlagStatus.status == status)

        if parsing_priority is not None:
            query = query.filter(Feed.parsing_priority == int(parsing_priority))

        if is_parsing is not None:
            if isinstance(is_parsing, str):
                is_parsing = is_parsing.lower() == "true"
            query = query.filter(Feed.is_parsing == is_parsing)
            
        if search:
            query = query.filter(Feed.url.ilike(f"%{search}%"))
            
        # Safe dynamic sorting
        query = apply_sorting(query, Feed, sort_by, sort_order)
        # Use existing pagination helper
        feeds, pagination_meta = paginate_query(query, page, limit)
        
        
        logger.info(f"Retrieved {len(feeds)} feeds for page {page}")
        return {
            "data": feeds,
            "meta": pagination_meta
        }
    except Exception as e:
        logger.error(f"Error retrieving feeds: {str(e)}")
        raise DatabaseError(f"Failed to retrieve feeds: {str(e)}")



def import_feeds_from_opml(opml_content: str):
    """
    Parse OPML content and import feed URLs
    
    Args:
        opml_content (str): OPML XML content as string
        
    Returns:
        dict: Import results with counts
    """
    imported_count = 0
    skipped_count = 0
    failed_count = 0
    
    try:
        # Parse the OPML XML
        root = ET.fromstring(opml_content)
        
        # Find all outline elements with RSS feed URLs
        feed_urls = []
        for outline in root.findall(".//outline"):
            xml_url = outline.get("xmlUrl")
            if xml_url:
                feed_urls.append(xml_url.strip())
        
        if not feed_urls:
            logger.warning("No feed URLs found in OPML file")
            return {
                "imported": 0,
                "skipped": 0,
                "failed": 0,
                "message": "No feed URLs found in OPML file"
            }
        
        logger.info(f"Found {len(feed_urls)} feed URLs in OPML file")
        log_database_operation(logger, "CREATE", "feeds", f"bulk_import_{len(feed_urls)}")
        
        # Get active flag status ID
        active_flag_id = get_flag_status_id("active")
        
        # Process each feed URL
        for url in feed_urls:
            try:
                # Check if feed already exists
                existing_feed = db.session.query(Feed).filter_by(url=url).first()
                if existing_feed:
                    skipped_count += 1
                    logger.debug(f"Skipped duplicate feed: {url}")
                    continue
                
                # Create new feed
                feed = Feed(
                    url=url,
                    feed_flag_status_id=active_flag_id,
                    parsing_priority=0,
                    is_parsing=False
                )
                
                db.session.add(feed)
                imported_count += 1 # since not usingt the bulk_create
                logger.info(f"Imported feed: {url}") 
                
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to import feed {url}: {str(e)}")
                continue
        
        # Commit all changes
        db.session.commit()
        
        logger.info(f"OPML import completed: {imported_count} imported, {skipped_count} skipped, {failed_count} failed")
        return {
            "imported": imported_count,
            "skipped": skipped_count,
            "failed": failed_count
        }
        
    except ET.ParseError as e:
        logger.error(f"Failed to parse OPML file: {str(e)}")
        raise ValidationError(f"Invalid OPML file format: {str(e)}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error importing feeds from OPML: {str(e)}")
        raise DatabaseError(f"Failed to import feeds from OPML: {str(e)}")
    
