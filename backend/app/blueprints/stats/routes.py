from datetime import datetime
from flask import request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc
from app.blueprints.stats import stats_bp
from app.extensions import db
from app.utils.request_logger import get_logger, log_request
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.blueprints.stats.controller import list_channel_stats, get_channel_stat_details_by_id, list_item_stats, get_item_stat_details_by_id

logger = get_logger(__name__)

@stats_bp.route('/channels', methods=['GET'])
def list_channel_stats():
    try:
        log_request(logger, 'GET', '/stats/channels')

        # Pass the request into the controller
        data = list_channel_stats()

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
        
        data = get_channel_stat_details_by_id(channel_id)

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

        data = list_item_stats()

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
        logger.warning(f"Validation error in list_item_stats: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list_item_stats: {str(e)}")
        raise DatabaseError("Failed to retrieve item statistics")


@stats_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item_stats_detail(item_id):
    try:
        log_request(logger, 'GET', f'/stats/items/{item_id}')

        data = get_item_stat_details_by_id(item_id)

        return jsonify({
            "data": data
        }), 200

    except ValidationError as e:
        logger.warning(f"Validation error in get_item_stats_detail: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_item_stats_detail: {str(e)}")
        raise DatabaseError("Failed to retrieve item statistics")
