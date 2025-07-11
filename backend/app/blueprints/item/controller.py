from flask import request, jsonify
from app.blueprints.item.services import get_items_list, get_item_detail
from app.blueprints.item.schemas import items_schema, item_schema
from app.utils.query_params import get_pagination_params, get_sorting_params, get_search_query
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.utils.request_logger import get_logger, log_database_operation

logger = get_logger(__name__)

def list_items():
    try:
        page, limit = get_pagination_params(request)
        sort_by, sort_order = get_sorting_params(request, ['id', 'title'], default_field='id')
        search = get_search_query(request)

        logger.info(f"Listing Items - page: {page}, limit: {limit}, sort: {sort_by} {sort_order}, search: {search or 'none'}")
        log_database_operation(logger, "READ", "items", f"list_p{page}_1{limit}")

        items, meta = get_items_list(search, sort_by, sort_order, page, limit)

        result = {
            "data": items_schema.dump(items),
            "meta": {
                "total": meta['total_items'],
                "limit": limit,
                "offset": (page - 1) * limit
            }
        }

        logger.info(f"Successfully listed {len(items)} items")
        return jsonify(result)
    
    except ValidationError as e:
        logger.warning(f"Validation error in list_items: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in list_items: {str(e)}")
        raise DatabaseError("Failed to retrieve items")
    

def get_item_by_id(item_id):
    try:
        logger.info(f"Retrieving item details for ID: {item_id}")
        log_database_operation(logger, "READ", "items", item_id)

        item = get_item_detail(item_id)

        result = item_schema.dump(item)
        logger.info(f"Successfully retrieved item: {item_id}")
        return jsonify(result)

    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in get_item_by_id for ID {item_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_item_by_id for ID {item_id}: {str(e)}")
        raise DatabaseError("Failed to retrieve item")