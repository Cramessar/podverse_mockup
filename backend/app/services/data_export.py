# backend/app/services/data_export.py

import csv
import os
from datetime import datetime
from app.extensions import db
from app.models.channel import Channel
from app.models.item import Item
from backend.app.utils.request_logger import get_logger
from app.blueprints.channel.services import get_channels_for_export
from app.blueprints.feed.services import get_feeds_for_export
from app.blueprints.channel.schemas import channel_exports_schema
from app.blueprints.feed.schemas import feeds_export_schema
from app.utils.file_system_helpers import safe_write_file, FSError
from typing import Optional, Dict, Any

logger = get_logger(__name__)

def ensure_export_directory() -> str:
    """Ensures the exports directory exists"""
    # Use a path relative to the backend directory
    export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'exports')
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        # Ensure directory has correct permissions
        os.chmod(export_dir, 0o755)
    return export_dir

def export_data_to_csv(export_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Export channels and feeds data to CSV files using existing export functionality
    
    Args:
        export_dir: Optional override for export directory
        
    Returns:
        dict with export filenames and counts
        
    Raises:
        FSError: If there are filesystem-related errors
    """
    try:
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        # Export channels using existing functionality
        channels = get_channels_for_export(sort_by='id', sort_order='asc')
        channels_data = channel_exports_schema.dump(channels)
        channels_file = f"channels_export_{timestamp}.csv"
        channels_path = os.path.join(export_dir, channels_file)
        
        def write_channels(f):
            if channels_data:
                writer = csv.DictWriter(f, fieldnames=channels_data[0].keys())
                writer.writeheader()
                writer.writerows(channels_data)
        
        success, error = safe_write_file(channels_path, write_channels)
        if not success:
            raise FSError(f"Failed to write channels file: {error}")
        
        # Export feeds using existing functionality
        feeds = get_feeds_for_export(sort_by='id', sort_order='asc')
        feeds_data = feeds_export_schema.dump(feeds)
        feeds_file = f"feeds_export_{timestamp}.csv"
        feeds_path = os.path.join(export_dir, feeds_file)
        
        def write_feeds(f):
            if feeds_data:
                writer = csv.DictWriter(f, fieldnames=feeds_data[0].keys())
                writer.writeheader()
                writer.writerows(feeds_data)
        
        success, error = safe_write_file(feeds_path, write_feeds)
        if not success:
            raise FSError(f"Failed to write feeds file: {error}")
        
        logger.info(f"Export completed: {len(channels_data)} channels, {len(feeds_data)} feeds")
        
        return {
            "channels_file": channels_file,
            "channels_count": len(channels_data),
            "feeds_file": feeds_file,
            "feeds_count": len(feeds_data),
            "timestamp": timestamp,
            "export_directory": export_dir
        }
        
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        raise FSError(f"Export failed: {str(e)}")

def export_channels(filename: str) -> int:
    """Export channels to CSV"""
    channels = db.session.query(Channel).all()
    count = 0
    
    def write_channels(f):
        nonlocal count
        writer = csv.writer(f)
        writer.writerow([
            'id', 'title', 'description', 'link', 'language',
            'author', 'copyright', 'created_at', 'updated_at'
        ])
        
        for channel in channels:
            writer.writerow([
                channel.id,
                channel.title,
                channel.description,
                channel.link,
                channel.language,
                channel.author,
                channel.copyright,
                channel.created_at,
                channel.updated_at
            ])
            count += 1
    
    success, error = safe_write_file(filename, write_channels)
    if not success:
        raise FSError(f"Failed to write channels file: {error}")
    
    return count

def export_items(filename: str) -> int:
    """Export items to CSV"""
    items = db.session.query(Item).all()
    count = 0
    
    def write_items(f):
        nonlocal count
        writer = csv.writer(f)
        writer.writerow([
            'id', 'guid', 'title', 'description', 'pub_date',
            'link', 'author', 'channel_id', 'created_at', 'updated_at'
        ])
        
        for item in items:
            writer.writerow([
                item.id,
                item.guid,
                item.title,
                item.description,
                item.pub_date,
                item.link,
                item.author,
                item.channel_id,
                item.created_at,
                item.updated_at
            ])
            count += 1
    
    success, error = safe_write_file(filename, write_items)
    if not success:
        raise FSError(f"Failed to write items file: {error}")
    
    return count
