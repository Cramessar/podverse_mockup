# celery async task for parsing/updating feeds

from celery import shared_task
from app.services.feed_parser import parse_rss_feed

@shared_task
def fetch_feed(feed_id):
    # TODO: get feed from db using the id 
    # TODO: call parse_rss_feed(feed.url) 
    # TODO: update feed and items in database
    pass


# Where to use Celery
# In a task module, e.g. tasks.py
# For /feeds/{id}/reparse, call trigger_reparse.delay(feed_id)
# Task sets is_parsing = True, calls feedparser, logs result, resets is_parsing

