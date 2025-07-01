# backend/app/blueprints/stats/services.py
from typing import List, Optional, Dict, Any
from sqlalchemy import asc, desc, func
from datetime import datetime
from app.models.stats import StatsAggregatedChannel, StatsAggregatedItem, StatsTrackEventChannel, StatsTrackEventItem
from app.models.channel import Channel
from app.extensions import db
from app.utils.error_exceptions import NotFoundError, DatabaseError
from app.utils.logger import get_logger, log_database_operation

logger = get_logger(__name__)

class BaseFilterBuilder:
    def __init__(self, query, model_class):
        self.query = query
        self.model_class = model_class
    
    def apply_sorting(self, sort_by, sort_order='desc'):
        """
        Generic sorting that works with any model
        
        Args:
            sort_by: Field name to sort by
            sort_order: 'asc' or 'desc'
            allowed_fields: List of allowed field names for security
        """
        
        # Check if the field exists on the model
        if hasattr(self.model_class, sort_by):
            column = getattr(self.model_class, sort_by)
            
            if sort_order.lower() == 'desc':
                self.query = self.query.order_by(desc(column))
            else:
                self.query = self.query.order_by(asc(column))
        else:
            raise ValueError(f"Field '{sort_by}' does not exist on {self.model_class.__name__}")
        
        return self
    
    def paginate(self, page, per_page):
        """Generic pagination"""
        return self.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    
    def get_query(self):
        return self.query

class StatsService:
    """Service layer for statistics operations"""
    
    @staticmethod
    def get_channel_stats(time_filter: str = 'monthly', limit: int = 20, 
                         offset: int = 0, search: str = '') -> Dict[str, Any]:
        """
        Retrieve aggregated channel statistics
        Primary tables: channel, stats_aggregated_channel
        """
        # TODO: Implement database query
        # Sort by highest monthly count (month_current_count DESC)
        # Support filtering by time window and search
        
        time_column_map = {
            'monthly': StatsAggregatedChannel.month_current_count,
            'weekly': StatsAggregatedChannel.week_current_count,
            'daily': StatsAggregatedChannel.day_current_count,
            'all': StatsAggregatedChannel.all_time_count,
        }

        sort_column = time_column_map(time_filter, StatsAggregatedChannel.month_current_count)
    
        try:
            query = (
                db.session.query(
                    Channel.id.label("channel_id"),
                    Channel.title,
                    StatsAggregatedChannel.month_current_count,
                    StatsAggregatedChannel.week_current_count,
                    StatsAggregatedChannel.day_current_count,
                    StatsAggregatedChannel.all_time_count,
                )
                .join(StatsAggregatedChannel, Channel.id == StatsAggregatedChannel.channel_id)
                .filter(Channel.title.ilike(f"%{search}%"))
                .order_by(desc(sort_column))
                .limit(limit)
                .offset(offset)
            )

            log_database_operation(logger, "READ", "channels and stats_aggregated_channel", f"{search}")

            results = query.all()

            return {
                "results": [dict(row._asdict()) for row in results],
                "limit": limit,
                "offset": offset,
                "time_filter": time_filter,
                "search": search,
            }

        except Exception as e:
            logger.error(f"Error retrieving channel statistics: {str(e)}")
            raise DatabaseError(f"Failed to retrieve channel statistics: {str(e)}")

    @staticmethod
    def get_channel_stats_detail(channel_id: int, start: Optional[datetime] = None, 
                               end: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Retrieve detailed statistics for a specific channel
        Primary tables: channel, stats_aggregated_channel
        """
        # TODO: Implement database query
        # Include basic channel info, aggregated stats, and raw event count
        
        try:
            # Fetch Channel info and stats
            result = (
                db.session.query(
                    Channel.id.label("channel_id"),
                    Channel.title,
                    StatsAggregatedChannel.month_current_count,
                    StatsAggregatedChannel.week_current_count,
                    StatsAggregatedChannel.day_current_count,
                    StatsAggregatedChannel.all_time_count,
                )
                .join(StatsAggregatedChannel, Channel.id == StatsAggregatedChannel.channel_id)
                .filter(Channel.id == channel_id)
                .first()
            )

            if not result:
                raise DatabaseError(f"Channel with id {channel_id} not found")

            # Count the raw events in the given range
            event_query = db.session.query(func.count(StatsTrackEventChannel.id)).filter(
                StatsTrackEventChannel.channel_id == channel_id
            )

            if start:
                event_query = event_query.filter(StatsTrackEventChannel.created_at >= start)
            if end:
                event_query = event_query.filter(StatsTrackEventChannel.created_at <= end)

            event_count = event_query.scalar()

            log_database_operation(
                logger,
                "READ",
                "channels and stats_aggregated_channel",
                f"channel_id={channel_id} start={start or 'none'} end={end or 'none'}"
            )

            return {
                "channel_id": result.channel_id,
                "title": result.title,
                "slug": result.slug,
                "month_current_count": result.month_current_count,
                "week_current_count": result.week_current_count,
                "day_current_count": result.day_current_count,
                "all_time_count": result.all_time_count,
                "event_count_in_range": event_count,
                "start": start,
                "end": end,
            }

        except Exception as e:
            logger.error(f"Error retrieving detailed stats for channel {channel_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve channel details: {str(e)}")
    
    @staticmethod
    def get_item_stats(time_filter: str = 'monthly', limit: int = 20, 
                      offset: int = 0, search: str = '') -> Dict[str, Any]:
        """
        Retrieve aggregated item statistics
        Primary tables: item, stats_aggregated_item
        """
        # TODO: Implement database query
        # Sort by highest monthly count (month_current_count DESC)
        # Support filtering by time window and search
        pass
    
    @staticmethod
    def get_item_stats_detail(item_id: int, start: Optional[datetime] = None, 
                            end: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Retrieve detailed statistics for a specific item
        Primary tables: item, stats_aggregated_item, stats_track_event_item
        """
        # TODO: Implement database query
        # Include basic item info, aggregated stats, and raw event count
        pass 