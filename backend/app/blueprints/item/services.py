# app/blueprints/item/services.py

from app.models import Item
from app.models.item import ItemFlagStatus
from app.extensions import db
from sqlalchemy.orm import joinedload
from app.utils.query_helpers import apply_sorting, paginate_query
from app.utils.error_exceptions import NotFoundError, DatabaseError
from app.utils.logger import get_logger, log_database_operation

logger = get_logger(__name__)

def item_eagerload_options():
    return (
        joinedload(Item.channel),
        joinedload(Item.stats),
        joinedload(Item.flag_status),
    )

def get_items_list(search, sort_by, sort_order, page, limit):
    try:
        query = db.session.query(Item).options(*item_eagerload_options())
        log_database_operation(logger, "READ", "items", f"page_{page}_limit_{limit}")

        if search:
            query = query.filter(Item.title.ilike(f"%{search}%"))
            logger.info(f"Applying search filter for items: {search}")

        query = apply_sorting(query, Item, sort_by, sort_order)
        logger.info(f"Applying sort: {sort_by} {sort_order}")

        items, meta = paginate_query(query, page, limit)

        logger.info(f"Retrieved {len(items)} items for page {page} with search: {search or 'none'}")
        return items, meta

    except Exception as e:
        logger.error(f"Error retrieving items list: {str(e)}")
        raise DatabaseError(f"Failed to retrieve items: {str(e)}")

def get_item_detail(item_id):
    try:
        log_database_operation(logger, "READ", "items", item_id)

        item = db.session.query(Item).options(*item_eagerload_options()).filter_by(id=item_id).first()

        if not item:
            logger.warning(f"Item with ID {item_id} not found")
            raise NotFoundError(f"Item with ID {item_id} not found")

        logger.info(f"Retrieved item details for ID: {item_id}")
        return item

    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error retrieving item detail for ID {item_id}: {str(e)}")
        raise DatabaseError(f"Failed to retrieve item detail: {str(e)}")