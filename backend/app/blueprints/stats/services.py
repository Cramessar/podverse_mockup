# backend/app/blueprints/stats/services.py
from typing import List, Optional, Dict, Any
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import joinedload
from datetime import datetime
from app.models.stats import StatsAggregatedChannel, StatsAggregatedItem, StatsTrackEventChannel, StatsTrackEventItem
from app.models.channel import Channel
from app.models.item import Item
from app.blueprints.stats.schemas import (
    channel_details_schema, 
    channel_daily_stats_only_schema, 
    channel_weekly_stats_only_schema, 
    stats_channel_schema_many, 
    item_daily_stats_only_schema,
    item_details_schema,
    item_weekly_stats_only_schema,
    stats_item_schema_many
)
from app.extensions import db
from app.utils.error_exceptions import NotFoundError, DatabaseError, ValidationError
from app.utils.request_logger import get_logger, log_database_operation

logger = get_logger(__name__)

# class BaseFilterBuilder:
#     def __init__(self, query, model_class):
#         self.query = query
#         self.model_class = model_class
    
#     def apply_sorting(self, sort_by, sort_order='desc'):
#         """
#         Generic sorting that works with any model
        
#         Args:
#             sort_by: Field name to sort by
#             sort_order: 'asc' or 'desc'
#             allowed_fields: List of allowed field names for security
#         """
        
#         # Check if the field exists on the model
#         if hasattr(self.model_class, sort_by):
#             column = getattr(self.model_class, sort_by)
            
#             if sort_order.lower() == 'desc':
#                 self.query = self.query.order_by(desc(column))
#             else:
#                 self.query = self.query.order_by(asc(column))
#         else:
#             raise ValueError(f"Field '{sort_by}' does not exist on {self.model_class.__name__}")
        
#         return self
    
#     def paginate(self, page, per_page):
#         """Generic pagination"""
#         return self.query.paginate(
#             page=page,
#             per_page=per_page,
#             error_out=False
#         )
    
#     def get_query(self):
#         return self.query

def get_channel_stats(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve aggregated channel statistics
    Primary tables: channel, stats_aggregated_channel
    """
    # TODO:
    # Sort by highest monthly count (month_current_count DESC)
    # Support filtering by time window and search
    
    try:
        query = db.session.query(StatsAggregatedChannel)

        #Apply filters
        if filters.get("channel_id"):
            query = query.filter(StatsAggregatedChannel.channel_id == filters["channel_id"])

        if filters.get("channel_ids"):
            query = query.filter(StatsAggregatedChannel.channel_id.in_(filters["channel_ids"]))

        if filters.get("search"):
            query = query.join(Channel).filter(Channel.title.ilike(f"%{filters['search']}%"))

        # Sorting the data
        sort_field = getattr(StatsAggregatedChannel, filters.get("sort_by", "channel_id"))
        sort_column = desc(sort_field) if filters.get("sort_order") == "desc" else sort_field
        query = query.order_by(sort_column)

        # Pagination for returned data
        page = filters.get("page", 1)
        per_page = filters.get("per_page", 20)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)


        # Setup View type for time based statistics
        view = filters.get("view", "monthly")
        if view == "daily":
            schema = channel_daily_stats_only_schema
        elif view == "weekly":
            schema = channel_weekly_stats_only_schema
        elif view in ["monthly", "all_time"]:
            schema = stats_channel_schema_many
        else:
            raise ValidationError(f"Unsupported view: {view}")
            

        log_database_operation(logger, "READ", "channels and stats_aggregated_channel", f"{filters}")

        data = schema.dump(pagination.items, many=True)

        return {
            "results": data,
            "page" : page,
            "per_page": per_page,
            "total": pagination.total,
            "view": view,
        }

    except Exception as e:
        logger.error(f"Error retrieving channel statistics: {str(e)}")
        raise DatabaseError(f"Failed to retrieve channel statistics: {str(e)}")

def get_channel_stats_detail(channel_id: int, start: Optional[datetime] = None, 
                            end: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Retrieve detailed statistics for a specific channel
    Primary tables: channel, stats_aggregated_channel
    """
    try:
        # Fetch Channel info and stats
        channel = (
            db.session.query(Channel)
            .options(joinedload(Channel.stats))
            .filter(Channel.id == channel_id)
            .first()
        )

        if not channel:
            raise NotFoundError(f"Channel with id {channel_id} not found")

        # Count the raw events in the given range
        event_query = db.session.query(func.count(StatsTrackEventChannel.id)).filter(
            StatsTrackEventChannel.channel_id == channel_id
        )

        if start:
            event_query = event_query.filter(StatsTrackEventChannel.created_at >= start)
        if end:
            event_query = event_query.filter(StatsTrackEventChannel.created_at <= end)

        event_count = event_query.scalar()
        setattr(channel, 'raw_event_count', event_count)

        log_database_operation(
            logger,
            "READ",
            "channel + stats_aggregated_channel + stats_tracks_event_channel",
            f"channel_id={channel_id} start={start or 'none'} end={end or 'none'}"
        )

        return channel_details_schema.dump(channel)

    except Exception as e:
        logger.error(f"Error retrieving detailed stats for channel {channel_id}: {str(e)}")
        raise DatabaseError(f"Failed to retrieve channel details: {str(e)}")


def get_item_stats(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve aggregated item statistics
    Primary tables: item, stats_aggregated_item
    """
    # TODO: Implement database query
    # Sort by highest monthly count (month_current_count DESC)
    # Support filtering by time window and search
    try:
        query = db.session.query(StatsAggregatedItem)

        if filters.get("item_id"):
                query = query.filter(StatsAggregatedItem.item_id == filters["item_id"])

        if filters.get("item_ids"):
            query = query.filter(StatsAggregatedItem.item_id.in_(filters["item_ids"]))

        if filters.get("search"):
            query = query.join(Item).filter(Item.title.ilike(f"%{filters['search']}%"))

        sort_field = getattr(StatsAggregatedItem, filters.get("sort_by", "item_id"))
        sort_column = desc(sort_field) if filters.get("sort_order") == "desc" else asc(sort_field)
        query = query.order_by(sort_column)

        page = filters.get("page", 1)
        per_page = filters.get("per_page", 10)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        view = filters.get("view", "monthly")
        if view == "daily":
            schema = item_daily_stats_only_schema
        elif view == "weekly":
            schema = item_weekly_stats_only_schema
        elif view in ["monthly", "all_time"]:
            schema = stats_item_schema_many
        else:
            raise ValueError(f"Unsupported view: {view}")

        data = schema.dump(pagination.items, many=True)

        return {
            "results": data,
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "view": view,
        }

    except Exception as e:
        logger.error(f"Error retrieving item stats: {str(e)}")
        raise DatabaseError("Failed to retrieve item statistics")



def get_item_stats_detail(item_id: int, start: Optional[datetime] = None, 
                        end: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Retrieve detailed statistics for a specific item
    Primary tables: item, stats_aggregated_item, stats_track_event_item
    """
    # TODO: Implement database query
    # Include basic item info, aggregated stats, and raw event count
    try:
        item = (
            db.session.query(Item)
            .filter(Item.id == item_id)
            .first()
        )
        
        if not item:
            raise NotFoundError(f"Item {item_id} not found")
        
        event_query = db.session.query(func.count()).select_from(StatsTrackEventItem).filter(StatsTrackEventItem.item_id == item_id)

        if start:
            event_query = event_query.filter(StatsTrackEventItem.created_at >= start)
        if end:
            event_query = event_query.filter(StatsTrackEventItem.created_at <= end)
        
        event_count = event_query.scalar()
        setattr(item, 'raw_event_count', event_count)

        log_database_operation(
            logger,
            "READ",
            "item + stats_aggregated_item + stats_aggregated_event_item",
            f"item_id={item_id}, start={start}, end={end}"
        )

        return item_details_schema.dump(item)
    
    except Exception as e:
        logger.error(f"Error retrieving detailed stats for item {item_id}: {str(e)}")
        raise DatabaseError("Failed to retrieve item detail statistics")