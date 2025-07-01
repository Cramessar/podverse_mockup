#app/blueprints/feed/routes.py

from flask import jsonify
from . import feed_bp
from app.utils.logger import get_logger, log_request, log_request_start, log_request_end
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from .controllers import reparse_feed_controller, get_feeds_controller, import_feeds_controller

logger = get_logger(__name__)

@feed_bp.route('/<int:feed_id>/reparse', methods=['POST'])
def reparse_feed(feed_id):
    """Trigger reparse for a specific feed"""
    try:
        log_request(logger, 'POST', f'/feeds/{feed_id}/reparse')
        
        result = reparse_feed_controller(feed_id)
        return jsonify(result), 200
        
    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in reparse_feed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in reparse_feed: {str(e)}")
        raise DatabaseError("Failed to reparse feed")


@feed_bp.route('', methods=['GET'])
def get_feeds():
    """Get all feeds with pagination"""
    try:
        log_request(logger, 'GET', '/feeds')
        
        result = get_feeds_controller()
        return jsonify(result), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error in get_feeds: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_feeds: {str(e)}")
        raise DatabaseError("Failed to retrieve feeds")


@feed_bp.route('/import', methods=['POST'])
def import_feeds():
    """Import feeds from OPML file upload"""
    try:
        log_request(logger, 'POST', '/feeds/import', include_payload=False)
        
        result = import_feeds_controller()
        return jsonify(result), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error in import_feeds: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in import_feeds: {str(e)}")
        raise DatabaseError("Failed to import feeds")
    
