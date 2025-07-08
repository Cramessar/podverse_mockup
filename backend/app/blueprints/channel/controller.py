# app/blueprints/channel/controller.py

from flask import request, jsonify
from app.blueprints.channel.services import get_channels_list, get_channel_detail, get_channels_for_export
from app.blueprints.channel.schemas import channels_schema, channel_exports_schema, channel_detail_schema
from app.utils.query_params import get_pagination_params, get_sorting_params, get_search_query
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.utils.logger import get_logger, log_database_operation
from app.utils.export_response import generate_export_response
from datetime import datetime
from app.utils.export_logging import create_export_log_simple, finalize_export_log

logger = get_logger(__name__)

def list_channels():
    try:
        page, limit = get_pagination_params(request)
        sort_by, sort_order = get_sorting_params(request, ['id', 'title'], default_field='id')
        search = get_search_query(request)

        logger.info(f"Listing channels - page: {page}, limit: {limit}, sort: {sort_by} {sort_order}, search: {search or 'none'}")
        log_database_operation(logger, "READ", "channels", f"list_p{page}_l{limit}")

        channels, meta = get_channels_list(search, sort_by, sort_order, page, limit)

        result = {
            "data": channels_schema.dump(channels),
            "meta": {
                "total": meta['total_items'],
                "limit": limit,
                "offset": (page - 1) * limit
            }
        }
        
        logger.info(f"Successfully listed {len(channels)} channels")
        return jsonify(result)
        
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
        # Get admin email from request args
        admin_email = request.args.get("admin_email")
        if not admin_email:
            raise ValidationError("admin_email is required")

        # Create export log
        log = create_export_log_simple(
            export_type="channels",
            format=request.args.get("format", "csv"),
            filters=request.args.to_dict(),
            admin_email=admin_email
        )

        # Get query parameters (reuse same logic as list view)
        sort_by, sort_order = get_sorting_params(request, ['id', 'title'], default_field='id')
        search = get_search_query(request)
        
        # Get max_rows parameter (optional, defaults to 10000)
        max_rows = request.args.get('max_rows', 10000, type=int)
        if max_rows <= 0 or max_rows > 50000:  
            max_rows = 10000

        logger.info(f"Exporting channels - sort: {sort_by} {sort_order}, search: {search or 'none'}, max_rows: {max_rows}")
        log_database_operation(logger, "READ", "channels", f"export_max_{max_rows}")

        # Get channels for export
        channels = get_channels_for_export(search, sort_by, sort_order, max_rows)
        
        # Serialize channels
        export_data = channel_exports_schema.dump(channels)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"channels_export_{timestamp}.csv"
        
        # Create response
        response = generate_export_response(export_data, filename, "channel")
        
        # finalize export log
        finalize_export_log(log, status="success" , file_path=f"/exports/{filename}", counts={"channels": len(export_data)}) # file name is set in generate_export_response
        
        logger.info(f"Generated export file: {filename} with {len(export_data)} records")
        return response

    except ValidationError as e:
        logger.warning(f"Validation error in export_channels: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in export_channels: {str(e)}")
        raise DatabaseError("Failed to export channels")

def get_channel_by_id(channel_id):
    try:   
        logger.info(f"Retrieving channel details for ID: {channel_id}")
        log_database_operation(logger, "READ", "channels", channel_id)
        
        channel = get_channel_detail(channel_id)
        
        result = channel_detail_schema.dump(channel)
        logger.info(f"Successfully retrieved channel: {channel_id} - {channel.title}")
        
        return jsonify(result)
        
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_channel_by_id for ID {channel_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_channel_by_id for ID {channel_id}: {str(e)}")
        raise DatabaseError("Failed to retrieve channel")
