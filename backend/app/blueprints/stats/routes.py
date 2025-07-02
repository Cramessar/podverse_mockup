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
        filters = channel_stats_filter_schema.load(request.args)

        query = db.session.query(StatsAggregatedChannel)

        # Filtering logic
        if filters.get("channel_id"):
            query = query.filter(StatsAggregatedChannel.channel_id == filters["channel_id"])

        if filters.get("channel_ids"):
            query = query.filter(StatsAggregatedChannel.channel_id.in_(filters["channel_ids"]))

        # Sorting
        sort_by = getattr(StatsAggregatedChannel, filters["sort_by"], StatsAggregatedChannel.channel_id)
        sort_order = desc(sort_by) if filters["sort_order"] == "desc" else sort_by
        query = query.order_by(sort_order)

        # Pagination
        page = filters["page"]
        per_page = filters["per_page"]
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        view = filters["view"]
        if view == "details":
            data = channel_details_schema.dump(pagination.items, many=True)
        elif view == "daily":
            data = channel_daily_stats_only_schema.dump(pagination.items, many=True)
        elif view == "weekly":
            data = channel_weekly_stats_only_schema.dump(pagination.items, many=True)
        else:
            data = stats_channel_schema.dump(pagination.items, many=True)

        return jsonify({
            "data": data,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total
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
        channel = db.session.query(Channel).options(joinedload(Channel.stats)).filter(Channel.id == channel_id).first()
        if not channel:
            raise NotFoundError("Channel not found")

        data = channel_details_schema.dump(channel)

        return jsonify({
            "data": data
        }), 200

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
