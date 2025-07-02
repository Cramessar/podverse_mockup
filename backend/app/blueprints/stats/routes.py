from datetime import datetime
from flask import request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc
from app.blueprints.stats import stats_bp
from app.extensions import db
from app.models.channel import Channel
from app.models.item import Item
from app.models.stats import StatsAggregatedChannel, StatsAggregatedItem
from app.utils.logger import get_logger, log_request
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.blueprints.stats.services import StatsService
from app.blueprints.stats.schemas import (
    stats_channel_schema,
    stats_item_schema,
    channel_details_schema,
    channel_daily_stats_only_schema,
    channel_weekly_stats_only_schema,
    channel_stats_filter_schema
)

logger = get_logger(__name__)

@stats_bp.route('/channels', methods=['GET'])
def list_channel_stats():
    try:
        log_request(logger, 'GET', '/stats/channels')
        
        # Validate and load the query parameters into a filters dict
        filters = channel_stats_filter_schema.load(request.args)

        # Pass the filters directly into the channel_stats service
        data = StatsService.get_channel_stats(filters)

        return jsonify({
            "data": data["results"],
            "meta": {
                "page": data["page"],
                "per_page": data["per_page"],
                "total": data["total"],
                "view": data["view"]
            }
        }), 200

    except ValidationError as e:
        logger.warning(f"Validation error in list_channel_stats: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list_channel_stats: {str(e)}")
        raise DatabaseError("Failed to retrieve channel statistics")


@stats_bp.route('/channels/<int:channel_id>', methods=['GET'])
def get_channel_stats_detail(channel_id):
    try:
        log_request(logger, 'GET', f'/stats/channels/{channel_id}')
        
        # Optional Date Filters
        start = request.args.get('start')
        end = request.args.get('end')

        start_date = datetime.fromisoformat(start) if start else None
        end_date = datetime.fromisoformat(end) if end else None

        data = StatsService.get_channel_stats_detail(channel_id, start_date, end_date)
        channel = db.session.query(Channel).options(joinedload(Channel.stats)).filter(Channel.id == channel_id).first()
        
        return jsonify({
            "data": data
        }), 200
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_channel_stats_detail: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_channel_stats_detail: {str(e)}")
        raise DatabaseError("Failed to retrieve channel statistics")


@stats_bp.route('/items', methods=['GET'])
def list_item_stats():
    try:
        log_request(logger, 'GET', '/stats/items')
        items = db.session.query(StatsAggregatedItem).all()
        data = stats_item_schema.dump(items, many=True)

        return jsonify({
            "data": data,
            "meta": {"count": len(data)}
        }), 200

    except ValidationError as e:
        logger.warning(f"Validation error in list_item_stats: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list_item_stats: {str(e)}")
        raise DatabaseError("Failed to retrieve item statistics")


@stats_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item_stats_detail(item_id):
    try:
        log_request(logger, 'GET', f'/stats/items/{item_id}')
        item = db.session.query(StatsAggregatedItem).filter_by(item_id=item_id).first()
        if not item:
            raise NotFoundError("Item not found")

        data = stats_item_schema.dump(item)

        return jsonify({
            "data": data
        }), 200

    except ValidationError as e:
        logger.warning(f"Validation error in get_item_stats_detail: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_item_stats_detail: {str(e)}")
        raise DatabaseError("Failed to retrieve item statistics")
