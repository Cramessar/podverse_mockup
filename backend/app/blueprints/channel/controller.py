# app/blueprints/channel/controller.py

from flask import request, jsonify
from app.blueprints.channel.services import get_channels_list, get_channel_detail
from app.blueprints.channel.schemas import channel_schema, channels_schema
from app.utils.query_params import get_pagination_params, get_sorting_params, get_search_query
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.utils.logger import get_logger

logger = get_logger(__name__)

def list_channels():
    try:
        page, limit = get_pagination_params(request)
        sort_by, sort_order = get_sorting_params(request, ['id', 'title'], default_field='id')
        search = get_search_query(request)

        channels, meta = get_channels_list(search, sort_by, sort_order, page, limit)

        return jsonify({
            "data": channels_schema.dump(channels),
            "meta": {
                "total": meta['total_items'],
                "limit": limit,
                "offset": (page - 1) * limit
            }
        })
    except ValidationError as e:
        logger.warning(f"Validation error in list_channels: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list_channels: {str(e)}")
        raise DatabaseError("Failed to retrieve channels")

def get_channel_by_id(channel_id):
    try:
        if not isinstance(channel_id, int) or channel_id < 1:
            raise ValidationError("Invalid channel ID")
            
        channel = get_channel_detail(channel_id)
        return jsonify(channel_schema.dump(channel))
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_channel_by_id: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_channel_by_id: {str(e)}")
        raise DatabaseError("Failed to retrieve channel")
