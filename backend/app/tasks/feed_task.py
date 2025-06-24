# celery async task for parsing/updating feeds

from celery import shared_task
from app.services.feed_parser import parse_rss_feed

@shared_task
def fetch_feed(feed_id):
    # TODO: get feed from db using the id 
    # TODO: call parse_rss_feed(feed.url) 
    # TODO: update feed and items in database
    pass