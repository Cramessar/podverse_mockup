from flask import jsonify
from . import item_bp
from app.blueprints.item.controller import list_items, get_item_by_id
from app.utils.auth import requires_auth
from backend.app.utils.request_logger import get_logger, log_request, log_request_start, log_request_end
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.extensions import limiter

logger = get_logger(__name__)

@item_bp.before_request
def before_request():
    log_request_start(logger)

@item_bp.after_request
def after_request(response):
    return log_request_end(logger, response)

@item_bp.route('', methods=['GET'])
@limiter.limit("30 per minute")
#@requires_auth
def get_all_items():
    try:
        log_request(logger, 'GET', '/items')
        return list_items()

    except ValidationError as e:
        logger.warning(f"Validation error in get_all_items: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_all_items: {str(e)}")
        raise DatabaseError("Failed to retrieve items")

@item_bp.route('/<int:item_id>', methods=['GET'])
@limiter.limit("60 per minute")
#@requires_auth
def get_single_item(item_id):
    try:
        log_request(logger, 'GET', f'/items/{item_id}')
        return get_item_by_id(item_id)

    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_single_item: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_single_item: {str(e)}")
        raise DatabaseError("Failed to retrieve item")