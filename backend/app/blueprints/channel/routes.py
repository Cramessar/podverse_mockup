# app/blueprints/channel/routes.py

from flask import jsonify, g
from . import channel_bp
from app.blueprints.channel.controller import list_channels, get_channel_by_id, export_channels
from app.utils.auth import requires_auth
from app.utils.request_logger import get_logger, log_request, log_request_start, log_request_end
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.extensions import limiter

logger = get_logger(__name__)

@channel_bp.before_request
def before_request():
    """Log the start of every request to channel endpoints"""
    log_request_start(logger)

@channel_bp.after_request
def after_request(response):
    """Log the end of every request to channel endpoints"""
    return log_request_end(logger, response)

@channel_bp.route('', methods=['GET'])
@limiter.limit("30 per minute")
#@requires_auth
def get_all_channels():
    """Get all channels with pagination and filtering"""
    try:
        log_request(logger, 'GET', '/channels')
        return list_channels()
        
    except ValidationError as e:
        logger.warning(f"Validation error in get_all_channels: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_all_channels: {str(e)}")
        raise DatabaseError("Failed to retrieve channels")


@channel_bp.route('/export', methods=['GET'])
@limiter.limit("10 per minute")  # Lower rate limit for exports
#@requires_auth
def export_channels_route():
    """Export channels as CSV/JSON/OPML"""
    try:
        log_request(logger, 'GET', '/channels/export')
        return export_channels()
        
    except ValidationError as e:
        logger.warning(f"Validation error in export_channels_route: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in export_channels_route: {str(e)}")
        raise DatabaseError("Failed to export channels")


@channel_bp.route('/<int:channel_id>', methods=['GET'])
@limiter.limit("60 per minute")
#@requires_auth
def get_single_channel(channel_id):
    """Get a single channel by ID"""
    try:
        log_request(logger, 'GET', f'/channels/{channel_id}')
        return get_channel_by_id(channel_id)
        
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_single_channel: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_single_channel: {str(e)}")
        raise DatabaseError("Failed to retrieve channel")
