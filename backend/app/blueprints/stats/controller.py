from flask import request
from datetime import datetime
from app.blueprints.stats.services import get_channel_stats, get_channel_stats_detail, get_item_stats, get_item_stats_detail
from app.blueprints.stats.schemas import channel_stats_filter_schema, item_stats_filter_schema
from backend.app.utils.request_logger import get_logger

logger = get_logger(__name__)

def list_channel_stats():
    try:
        # Convert the request MultiDict into a single Dict for the schema load
        filters = request.args.to_dict(flat=False)

        filters = channel_stats_filter_schema.load(request.args)
        return get_channel_stats(filters)
    except Exception as e:
        logger.error(f"Failed to retrieve channel stats: {str(e)}")
        raise

def get_channel_stat_details_by_id(channel_id):
    try:
        start = request.args.get('start')
        end = request.args.get('end')

        start_dt = datetime.fromisoformat(start) if start else None
        end_dt = datetime.fromisoformat(end) if end else None

        return get_channel_stats_detail(channel_id, start_dt, end_dt)
    except Exception as e:
        logger.error(f"Failed to retrieve channel stats detail: {str(e)}")
        raise

def list_item_stats():
    try:
        filters = item_stats_filter_schema.load(request.args)
        return get_item_stats(filters)
    except Exception as e:
        logger.error(f"Failed to retrieve item stats: {str(e)}")
        raise

def get_item_stat_details_by_id(item_id):
    try:
        start = request.args.get("start")
        end = request.args.get("end")

        start_dt = datetime.fromisoformat(start) if start else None
        end_dt = datetime.fromisoformat(end) if end else None
        
        return get_item_stats_detail(item_id, start_dt, end_dt)
    except Exception as e:
        logger.error(f"Failed to retrieve item stat details: {str(e)}")
        raise