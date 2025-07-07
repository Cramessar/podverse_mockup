#app/blueprints/feed/routes.py

from flask import jsonify, request
from . import feed_bp
from app.utils.logger import get_logger, log_request_start, log_request_end
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.extensions import limiter
from app.utils.auth import requires_auth
from .controllers import (
    reparse_feed_controller, 
    get_all_feeds_controller, 
    import_feeds_controller, 
    get_feed_by_id_controller, 
    create_feed_controller, 
    bulk_export_feeds_controller, 
    export_single_feed_controller, 
    bulk_update_feeds_controller, 
    bulk_reparse_feeds_controller,
    get_feed_logs_controller
)

logger = get_logger(__name__)

@feed_bp.before_request
def before_request():
    """Log the start of every request to feed endpoints"""
    log_request_start(logger)

@feed_bp.after_request
def after_request(response):
    """Log the end of every request to feed endpoints"""
    return log_request_end(logger, response)


@feed_bp.route('', methods=['POST'])
@limiter.limit("10 per minute")  # Prevent spam feed creation
#@requires_auth
def create_feed():
    """Create a single feed"""
    try:
        result = create_feed_controller()
        return jsonify(result), 201
    except ValidationError as e:
        logger.warning(f"Validation error in create_feed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_feed: {str(e)}")
        raise DatabaseError("Failed to create feed")


@feed_bp.route('/<int:feed_id>/reparse', methods=['POST'])
def reparse_feed(feed_id: int):
    """
    Reparse a specific feed by ID
    Can be run synchronously or asynchronously based on query parameter
    """
    # Check for async mode in query params or request body
    async_mode = request.args.get('async', '').lower() == 'true'
    if request.is_json:
        async_mode = async_mode or request.json.get('async', False)
    
    return reparse_feed_controller(feed_id, async_mode=async_mode)


@feed_bp.route('', methods=['GET'])
@limiter.limit("80 per minute")  
#@requires_auth
def get_feeds():
    """Get all feeds with pagination"""
    try:
        result = get_all_feeds_controller()
        return jsonify(result), 200
    except ValidationError as e:
        logger.warning(f"Validation error in get_feeds: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_feeds: {str(e)}")
        raise DatabaseError("Failed to retrieve feeds")
   
    
@feed_bp.route('/<int:feed_id>', methods=['GET'])
@limiter.limit("80 per minute")  
#@requires_auth
def get_feed_by_id(feed_id):
    """Get a single feed by ID"""
    try:
        result = get_feed_by_id_controller(feed_id)
        return jsonify(result), 200
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_feed_by_id: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_feed_by_id: {str(e)}")
        raise DatabaseError("Failed to retrieve feed")
    
@feed_bp.route('/<int:feed_id>/export', methods=['GET'])
@limiter.limit("5 per minute")  # Protect against large download spam
#@requires_auth
def export_single_feed(feed_id):
    """Export a single feed as CSV/JSON/OPML"""
    try:
        return export_single_feed_controller(feed_id)
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in export_single_feed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in export_single_feed: {str(e)}")
        raise DatabaseError("Failed to export feed")

#MARK: bulk endpoints   
@feed_bp.route('/import', methods=['POST'])
@limiter.limit("3 per minute") 
#@requires_auth
def import_feeds():
    """Import feeds from OPML file upload """
    try:
        result = import_feeds_controller()
        return jsonify(result), 200    
    except ValidationError as e:
        logger.warning(f"Validation error in import_feeds: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in import_feeds: {str(e)}")
        raise DatabaseError("Failed to import feeds")


@feed_bp.route('/export', methods=['GET'])
@limiter.limit("5 per minute")  
#@requires_auth
def bulk_export_feeds():
    """Export feeds in bulk as CSV/JSON/OPML"""
    try:
        return bulk_export_feeds_controller()
    except ValidationError as e:
        logger.warning(f"Validation error in bulk_export_feeds: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in bulk_export_feeds: {str(e)}")
        raise DatabaseError("Failed to export feeds")



@feed_bp.route('/bulk-update-status', methods=['POST'])
@limiter.limit("4 per minute")  
#@requires_auth
def bulk_update_feeds():
    """Update status/properties of multiple feeds"""
    try:
        result = bulk_update_feeds_controller()
        return jsonify(result), 200
    except ValidationError as e:
        logger.warning(f"Validation error in bulk_update_feeds: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in bulk_update_feeds: {str(e)}")
        raise DatabaseError("Failed to bulk update feeds")


@feed_bp.route('/bulk-reparse', methods=['POST'])
@limiter.limit("4 per minute")  
#@requires_auth
def bulk_reparse_feeds():
    """Trigger reparse for multiple feeds"""
    try:
        result = bulk_reparse_feeds_controller()
        return jsonify(result), 200
    except ValidationError as e:
        logger.warning(f"Validation error in bulk_reparse_feeds: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in bulk_reparse_feeds: {str(e)}")
        raise DatabaseError("Failed to bulk reparse feeds")


@feed_bp.route('/auto-reparse-status', methods=['GET'])
@limiter.limit("10 per minute")  
#@requires_auth
def auto_reparse_status():
    """Check if auto_reparse_all task is currently running"""
    try:
        from app.utils.helpers import is_auto_reparse_running
        
        is_running = is_auto_reparse_running()
        
        return jsonify({
            "auto_reparse_running": is_running,
            "status": "running" if is_running else "idle"
        }), 200
    except Exception as e:
        logger.error(f"Error checking auto_reparse_status: {str(e)}")
        raise DatabaseError("Failed to check auto reparse status")


@feed_bp.route('/<int:feed_id>/logs', methods=['GET'])
@limiter.limit("80 per minute")
#@requires_auth
def get_feed_logs(feed_id):
    """Get logs for a specific feed"""
    try:
        result = get_feed_logs_controller(feed_id)
        return jsonify(result), 200
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_feed_logs: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_feed_logs: {str(e)}")
        raise DatabaseError("Failed to retrieve feed logs")


