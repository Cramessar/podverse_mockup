#pure parser logic using feedparser - low level logic for parsing rss using feedparser
# Raw XML parsing functions
# (e.g., parse_rss(xml_string) → dict)

import feedparser


def parse_rss_feed(url):
    """
    Parses an RSS feed URL and extracts metadata and items into dictionaries.

    :param url: The URL of the RSS feed to parse.
    :return: A tuple containing a dictionary of feed metadata and a list of item dictionaries.
    """
    # Parse the feed
    feed = feedparser.parse(url)

    # Extract feed metadata
    feed_info = {
        'title': feed.feed.get('title', ''),
        'link': feed.feed.get('link', ''),
        'description': feed.feed.get('description', ''),
        'language': feed.feed.get('language', ''),
        'published': feed.feed.get('published', '')
    }

    # Extract items
    items = []
    for entry in feed.entries:
        item = {
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'description': entry.get('description', ''),
            'published': entry.get('published', ''),
            'author': entry.get('author', '')
        }
        items.append(item)

    return feed_info, items



# TODO: Where to use Feedparser
# In a service function like parse_feed(url)
# Only called during:
# Manual reparse trigger
# New feed creation (optional)
# This function extracts metadata, saves it to DB, logs status/errors


# --------- LAter when the models ready ---------
# import feedparser
# from app.models.feed import Feed
# from app.models.item import Item
# from app.extensions import db


# def parse_rss_feed(url):
#     """
#     Parses an RSS feed URL and creates Feed and Item model instances.

#     :param url: The URL of the RSS feed to parse.
#     :return: A tuple containing a Feed instance and a list of Item instances.
#     """
#     # Parse the feed
#     feed = feedparser.parse(url)

#     # Create a Feed instance
#     feed_instance = Feed(
#         url=url,
#         feed_flag_status_id=1,  # Example value
#         is_parsing=None,
#         parsing_priority=0,
#         last_parsed_file_hash=None,
#         container_id=None
#     )

#     # Extract items and create Item instances
#     item_instances = []
#     for entry in feed.entries:
#         item_instance = Item(
#             title=entry.get('title', ''),
#             slug=entry.get('link', ''),  # fexample value
#             guid=entry.get('id', ''),
#             guid_enclosure_url=entry.get('link', ''),
#             published_at=entry.get('published', None)
#         )
#         item_instances.append(item_instance)

#     # Add to the session and commit
#     db.session.add(feed_instance)
#     db.session.add_all(item_instances)
#     db.session.commit()

    return feed_instance, item_instances