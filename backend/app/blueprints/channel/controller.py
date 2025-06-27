# app/blueprints/channel/controller.py

from flask import request, jsonify
from app.blueprints.channel.services import get_channels_list, get_channel_detail, get_channels_for_export
from app.blueprints.channel.schemas import channel_schema, channels_schema, channel_exports_schema, channel_detail_schema
from app.utils.query_params import get_pagination_params, get_sorting_params, get_search_query
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.utils.logger import get_logger
from app.utils.cvs_response import generate_csv_response
from datetime import datetime

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

def export_channels():
    """
    Export channels as CSV with optional filtering and sorting.
    Reuses the same filtering logic as list_channels but without pagination.
    """
    try:
        # Get query parameters (reuse same logic as list view)
        sort_by, sort_order = get_sorting_params(request, ['id', 'title'], default_field='id')
        search = get_search_query(request)
        
        # Get max_rows parameter (optional, defaults to 10000)
        max_rows = request.args.get('max_rows', 10000, type=int)
        if max_rows <= 0 or max_rows > 50000:  # Set reasonable bounds
            max_rows = 10000

        # Get channels for export
        channels = get_channels_for_export(search, sort_by, sort_order, max_rows)

        # Serialize channels
        export_data = channel_exports_schema.dump(channels)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"channels_export_{timestamp}.csv"

        return generate_csv_response(export_data, filename)

    except ValidationError as e:
        logger.warning(f"Validation error in export_channels: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in export_channels: {str(e)}")
        raise DatabaseError("Failed to export channels")

def get_channel_by_id(channel_id):
    try:
        if not isinstance(channel_id, int) or channel_id < 1:
            raise ValidationError("Invalid channel ID")
            
        channel = get_channel_detail(channel_id)
        return jsonify(channel_detail_schema.dump(channel))
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_channel_by_id: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_channel_by_id: {str(e)}")
        raise DatabaseError("Failed to retrieve channel")
