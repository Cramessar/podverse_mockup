# app/blueprints/channel/services.py

from app.models import Channel
from app.models.channel import ChannelCategory
from app.extensions import db
from sqlalchemy.orm import joinedload
from app.utils.query_helpers import apply_sorting, paginate_query
from app.utils.error_exceptions import NotFoundError

def get_channels_list(search, sort_by, sort_order, page, limit):
    """
    Retrieve a paginated list of channels with optional search and sorting.
    Eager loads related feed, medium, categories, and stats.
    
    """
    # Use eager loading to fetch related medium and feed data in a single query (prevents N+1 query problem by joining related tables immediately)
    query = db.session.query(Channel).options(joinedload(Channel.medium), joinedload(Channel.feed), joinedload(Channel.stats), joinedload(Channel.categories).joinedload(ChannelCategory.category))
    
    if search:
        query = query.filter(Channel.title.ilike(f"%{search}%"))
    query = apply_sorting(query, Channel, sort_by, sort_order)
    
    channels, meta = paginate_query(query, page, limit)
    
    return channels, meta

def get_channels_for_export(search=None, sort_by='id', sort_order='asc', max_rows=10000):
    """
    Retrieve channels for export with optional search and sorting.
    No pagination, but limited to max_rows for performance.
    Eager loads related feed, medium, categories, and stats.
    
    Args:
        search: Optional search term to filter by title
        sort_by: Field to sort by (default: 'id')
        sort_order: Sort order (default: 'asc')
        max_rows: Maximum number of rows to export (default: 10000)
        
    Returns:
        List of Channel objects
    """
    
    query = db.session.query(Channel).options(
        joinedload(Channel.medium), 
        joinedload(Channel.feed), 
        joinedload(Channel.stats),
        joinedload(Channel.categories).joinedload(ChannelCategory.category)
    )
    
    if search:
        query = query.filter(Channel.title.ilike(f"%{search}%"))
    query = apply_sorting(query, Channel, sort_by, sort_order)
    
    # Limit to max_rows for performance
    query = query.limit(max_rows)
    
    channels = query.all()
    
    return channels

def get_channel_detail(channel_id):
    # using stats_aggregated_channel lets the admin see how popular the channel is without needing to sum up raw events every time.
    
    channel = db.session.query(Channel).options(
        joinedload(Channel.medium),
        joinedload(Channel.feed),
        joinedload(Channel.stats),
        joinedload(Channel.categories).joinedload(ChannelCategory.category)
    ).filter_by(id=channel_id).first()

    if not channel:
        raise NotFoundError(f"Channel with ID {channel_id} not found")

    return channel
    
