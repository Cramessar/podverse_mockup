from typing import List, Optional, Dict, Any
from sqlalchemy import asc, desc
from datetime import datetime

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
        pass
    
    @staticmethod
    def get_channel_stats_detail(channel_id: int, start: Optional[datetime] = None, 
                               end: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Retrieve detailed statistics for a specific channel
        Primary tables: channel, stats_aggregated_channel
        """
        # TODO: Implement database query
        # Include basic channel info, aggregated stats, and raw event count
        pass
    
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