# app/blueprints/feed/services.py

#NOT: Refactor into classes only if logic grows more complex for now stand alonw functions are already modular since it's in the same file

from app.models.feed import Feed, FeedFlagStatus
from app.models.channel import Channel
from app.blueprints.feed.reparse_helpers import reparse_feed_url, handle_bozo_parse_error, create_or_update_channel, insert_items, create_successful_feed_log, get_flag_status_id
from app.extensions import db
from app.utils.logger import get_logger, log_database_operation, log_network_event, log_error
from app.utils.query_helpers import paginate_query, apply_sorting
from app.utils.error_exceptions import NotFoundError, ValidationError, DatabaseError
from datetime import datetime
import xml.etree.ElementTree as ET
from flask import current_app
from sqlalchemy import or_

logger = get_logger(__name__)

def create_single_feed(url: str, parsing_priority: int = 0):
    """
    Create a single feed with the provided URL
    
    Args:
        url (str): The feed URL to add
        parsing_priority (int): Priority for parsing (0-10, default: 0)
        
    Returns:
        Feed: The created feed object
        
    Raises:
        ValidationError: If feed already exists or validation fails
        DatabaseError: If database operation fails
    """
    logger.info(f"Creating single feed with URL: {url}")
    log_database_operation(logger, "CREATE", "feeds", f"single_feed_{url}")
    
    try:
        # Check if feed already exists
        existing_feed = db.session.query(Feed).filter_by(url=url).first()
        if existing_feed:
            logger.warning(f"Feed already exists: {url}")
            raise ValidationError(f"Feed with URL '{url}' already exists")
        
        # Get active flag status ID
        active_flag_id = get_flag_status_id("active")
        
        # Create new feed
        feed = Feed(
            url=url,
            feed_flag_status_id=active_flag_id,
            parsing_priority=parsing_priority,
            is_parsing=False
        )
        
        db.session.add(feed)
        db.session.commit()
        
        logger.info(f"Successfully created feed: ID {feed.id}, URL: {url}")
        log_database_operation(logger, "CREATE", "feeds", f"success_{feed.id}")
        
        return feed
        
    except ValidationError:
        raise
    except Exception as e:
        db.session.rollback()
        log_error("create_single_feed", e)
        raise DatabaseError(f"Failed to create feed: {str(e)}")


def _parse_and_update_feed_object(feed: Feed):
    """Helper function that takes a Feed object directly (avoids redundant DB lookups)"""
    # Race condition guard: check if already parsing
    if feed.is_parsing:
        logger.warning(f"Feed ID {feed.id} is already being parsed")
        raise ValidationError("Feed is already being parsed")
    
    logger.info(f"Starting reparse for Feed ID: {feed.id}, URL: {feed.url}")
    log_database_operation(logger, "UPDATE", "feeds", feed.id)
    
    # mark and commit early feed is being parsed so flag is saved even if crash happens
    feed.is_parsing = True # so i dont touch anything if feed is broken no partial db save 
    db.session.commit()
    
    try:
        parsed_data = reparse_feed_url(feed.url)
        
        # if bozo true then mark the feed as error and log
        if parsed_data["feed"]["bozo"]:
            return handle_bozo_parse_error(feed, parsed_data)

        # If bozo is False, mark as active
        log_network_event(logger, "RSS_PARSE_SUCCESS", f"URL: {feed.url}, Items found: {len(parsed_data['items'])}")
        feed.feed_flag_status_id = get_flag_status_id("active")
        
        # protect db against abuse
        item_limit = current_app.config.get('FEED_ITEM_LIMIT', 500)
        if len(parsed_data["items"]) > item_limit:
            logger.warning(f"Too many items in feed ID {feed.id}: {len(parsed_data['items'])}, limit: {item_limit}")
            raise ValidationError(f"Feed contains too many items. Limit is {item_limit}.")
        
        channel = create_or_update_channel(parsed_data, feed)
        
        insert_items(parsed_data["items"], channel)
        
        create_successful_feed_log(feed.id, parsed_data["feed"]["http_status"])
        
        feed.is_parsing = False
        feed.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Succesxsfully reparsed Feed ID: {feed.id}, Channel ID: {channel.id}, Items: {len(parsed_data['items'])}")
        return {
            "status": "success",
            "feed_id": feed.id,
            "channel_id": channel.id,
            "item_count": len(parsed_data["items"])
        }
    except ValidationError:
        raise
    except Exception as e:
        db.session.rollback()
        # Log network issues separately from general errors
        if "timeout" in str(e).lower() or "connection" in str(e).lower():
            log_network_event(logger, "RSS_FETCH_ERROR", f"URL: {feed.url}, Error: {str(e)}")
        log_error("parse_and_update_feed", e)
        raise DatabaseError(f"Failed to reparse feed: {str(e)}")
    finally:
        feed.is_parsing = False
        try:
            db.session.commit()
        except:
            db.session.rollback()


def parse_and_update_feed(feed_id: int):
    """Public function for single feed reparse (does DB lookup)"""
    feed = db.session.get(Feed, feed_id)
    if not feed:
        raise NotFoundError("Feed not found")
    
    return _parse_and_update_feed_object(feed)
        

def get_all_feeds(page=1, limit=10, parsing_priority=None, is_parsing=None, status=None, sort_by="id", sort_order="desc", search=None):
    """
    Get all feeds with pagination and return structured response
    """
    try:
        # Create base query with left join to Channel for title search
        query = db.session.query(Feed).join(FeedFlagStatus).outerjoin(Channel).order_by(Feed.id.desc())
        log_database_operation(logger, "READ", "feeds", f"page_{page}_limit_{limit}")
             
        if status:
            query = query.filter(FeedFlagStatus.status == status)
            logger.info(f"Filtering feeds by status: {status}")

        if parsing_priority is not None:
            query = query.filter(Feed.parsing_priority == int(parsing_priority))
            logger.info(f"Filtering feeds by parsing_priority: {parsing_priority}")

        if is_parsing is not None:
            if isinstance(is_parsing, str):
                is_parsing = is_parsing.lower() == "true"
            query = query.filter(Feed.is_parsing == is_parsing)
            logger.info(f"Filtering feeds by is_parsing: {is_parsing}")
            
        if search:
            # Enhanced search: ID (exact), URL (partial), or Channel title (partial)
            search_conditions = []
            
            try:
                search_id = int(search)
                search_conditions.append(Feed.id == search_id)
            except ValueError:
                pass  # Not a valid integer, skip ID search
            
            # Always add URL and channel title searches
            search_conditions.append(Feed.url.ilike(f"%{search}%"))
            search_conditions.append(Channel.title.ilike(f"%{search}%"))
            
            # Combine with OR
            query = query.filter(or_(*search_conditions))
            logger.info(f"Filtering feeds by search term (ID/URL/title): {search}")
            
        # Safe dynamic sorting
        query = apply_sorting(query, Feed, sort_by, sort_order)
        # Use existing pagination helper
        feeds, pagination_meta = paginate_query(query, page, limit)
        
        logger.info(f"Retrieved {len(feeds)} feeds for page {page}")
        return {
            "data": feeds,
            "meta": pagination_meta
        }
        
    except Exception as e:
        log_error("get_all_feeds", e)
        raise DatabaseError(f"Failed to retrieve feeds: {str(e)}")

def get_feed_by_id(feed_id: int):
    feed = db.session.get(Feed, feed_id)
    log_database_operation(logger, "READ", "feeds", record_id=feed_id)
    if not feed:
        logger.warning(f"Feed not found: ID {feed_id}")
        raise NotFoundError("Feed not found")
    return feed

#MARK: bulk endpoints
# add json file upload function later if needed 
def import_feeds_from_opml(opml_content: str):
    """
    Parse OPML content and import feed URLs
    
    Args:
        opml_content (str): OPML XML content as string
        
    Returns:
        dict: Import results with counts
    """
    imported_count = 0
    skipped_count = 0
    failed_count = 0
    
    try:
        # Parse the opml xml file
        root = ET.fromstring(opml_content)
        
        # Collect all feed urls from opml file
        feed_urls = []
        for outline in root.findall(".//outline"):
            xml_url = outline.get("xmlUrl")
            if xml_url:
                feed_urls.append(xml_url.strip())
        
        feed_urls = list(set(feed_urls)) 
        
        if not feed_urls:
            logger.warning("No feed URLs found in OPML file")
            return {
                "imported": 0,
                "skipped": 0,
                "failed": 0,
                "message": "No feed URLs found in OPML file"
            }
        
        logger.info(f"Found {len(feed_urls)} feed URLs in OPML file")
        log_database_operation(logger, "CREATE", "feeds", f"bulk_import_{len(feed_urls)}")
        
        active_flag_id = get_flag_status_id("active")
        
        # Get existing URLs in one query to avoid big db hits 
        existing_urls = {row[0] for row in db.session.query(Feed.url).filter(Feed.url.in_(feed_urls)).all()}
        
        # Process each feed URL
        new_feeds = []
        for url in feed_urls:
            if url in existing_urls:
                skipped_count += 1
                logger.info(f"Skipped duplicate feed: {url}")
                continue
            try:
                # Create new feed
                feed = Feed(
                    url=url,
                    feed_flag_status_id=active_flag_id,
                    parsing_priority=0,
                    is_parsing=False
                )
                new_feeds.append(feed)
                
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to import feed {url}: {str(e)}")
                continue
        
       # Add all valid new feeds at once
        try:
            db.session.add_all(new_feeds)
            db.session.commit()
            imported_count = len(new_feeds)
        except Exception as e:
            db.session.rollback()
            log_error("import_feeds_from_opml commit", e)
            raise DatabaseError(f"Bulk commit failed: {str(e)}")
        
        logger.info(f"OPML import completed: {imported_count} imported, {skipped_count} skipped, {failed_count} failed")
        return {
            "imported": imported_count,
            "skipped": skipped_count,
            "failed": failed_count,
            "total_found": len(feed_urls)
        }
        
    except ET.ParseError as e:
        logger.error(f"Failed to parse OPML file: {str(e)}")
        raise ValidationError(f"Invalid OPML file format: {str(e)}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error importing feeds from OPML: {str(e)}")
        raise DatabaseError(f"Failed to import feeds from OPML: {str(e)}")
    

def get_feeds_for_export(search=None, sort_by='id', sort_order='asc', max_rows=10000):
    """
    Retrieve feeds for export with optional search and sorting.
    No pagination, but limited to max_rows for performance.
    
    Args:
        search: Optional search term to filter by ID (exact), URL (partial), or channel title (partial)
        sort_by: Field to sort by (default: 'id')
        sort_order: Sort order (default: 'asc')
        max_rows: Maximum number of rows to export (default: 10000)
        
    Returns:
        List of Feed objects
    """
    try:
        # Add left join to Channel for title search
        query = db.session.query(Feed).join(FeedFlagStatus).outerjoin(Channel)
        log_database_operation(logger, "READ", "feeds", f"export_max_{max_rows}")
        
        if search:
            # Enhanced search: ID (exact), URL (partial), or Channel title (partial)
            search_conditions = []
            
            # Try to parse as integer for ID search
            try:
                search_id = int(search)
                search_conditions.append(Feed.id == search_id)
            except ValueError:
                pass  # Not a valid integer, skip ID search
            
            # Always add URL and channel title searches
            search_conditions.append(Feed.url.ilike(f"%{search}%"))
            search_conditions.append(Channel.title.ilike(f"%{search}%"))
            
            # Combine with OR
            query = query.filter(or_(*search_conditions))
            logger.info(f"Applying enhanced search filter for export (ID/URL/title): {search}")
        
        query = apply_sorting(query, Feed, sort_by, sort_order)
        logger.info(f"Export query with sort: {sort_by} {sort_order}")
        
        # Limit to max_rows for performance
        query = query.limit(max_rows)
        
        feeds = query.all()
        
        logger.info(f"Retrieved {len(feeds)} feeds for export with search: {search or 'none'}")
        if len(feeds) == max_rows:
            logger.warning(f"Export hit max_rows limit of {max_rows} - results may be truncated")
        
        return feeds
        
    except Exception as e:
        logger.error(f"Error retrieving feeds for export: {str(e)}")
        raise DatabaseError(f"Failed to retrieve feeds for export: {str(e)}")


def bulk_update_feeds(feed_ids: list, updates: dict):
    """
    Update multiple feeds with the provided changes
    
    Args:
        feed_ids: List of feed IDs to update
        updates: Dictionary of fields to update
        
    Returns:
        dict: Update results with counts
    """
    updated_count = 0
    not_found_count = 0
    
    try:
        logger.info(f"Starting bulk update for {len(feed_ids)} feeds")
        log_database_operation(logger, "UPDATE", "feeds", f"bulk_update_{len(feed_ids)}")
        
        # Validate updates
        valid_fields = {'feed_flag_status_id', 'parsing_priority', 'is_parsing'}
        if not set(updates.keys()).issubset(valid_fields):
            invalid_fields = set(updates.keys()) - valid_fields
            raise ValidationError(f"Invalid update fields: {invalid_fields}")
        
        # Validate feed_flag_status_id if provided
        if 'feed_flag_status_id' in updates:
            flag_status = db.session.get(FeedFlagStatus, updates['feed_flag_status_id'])
            if not flag_status:
                raise ValidationError(f"Invalid feed_flag_status_id: {updates['feed_flag_status_id']}")
        
        # Update feeds
        for feed_id in feed_ids:
            feed = db.session.get(Feed, feed_id)
            if not feed:
                not_found_count += 1
                logger.warning(f"Feed not found: ID {feed_id}")
                continue
            
            # Apply updates
            for field, value in updates.items():
                if hasattr(feed, field):
                    setattr(feed, field, value)
            
            feed.updated_at = datetime.utcnow()
            updated_count += 1
        
        db.session.commit()
        
        logger.info(f"Bulk update completed: {updated_count} updated, {not_found_count} not found")
        return {
            "updated": updated_count,
            "not_found": not_found_count,
            "total_requested": len(feed_ids)
        }
        
    except ValidationError:
        raise
    except Exception as e:
        db.session.rollback()
        log_error("bulk_update_feeds", e)
        raise DatabaseError(f"Failed to bulk update feeds: {str(e)}")


def bulk_reparse_feeds(feed_ids: list):
    """
    Trigger reparse for multiple feeds
    
    Args:
        feed_ids: List of feed IDs to reparse
        
    Returns:
        dict: Reparse results with counts
    """
    success_count = 0
    failed_count = 0
    not_found_count = 0
    already_parsing_count = 0
    results = []
    
    try:
        logger.info(f"Starting bulk reparse for {len(feed_ids)} feeds")
        log_database_operation(logger, "UPDATE", "feeds", f"bulk_reparse_{len(feed_ids)}")
        
        for feed_id in feed_ids:
            feed = db.session.get(Feed, feed_id)
            if not feed:
                not_found_count += 1
                logger.warning(f"Feed not found: ID {feed_id}")
                results.append({
                    "feed_id": feed_id,
                    "status": "not_found",
                    "error": "Feed not found"
                })
                continue
            
            if feed.is_parsing:
                already_parsing_count += 1
                logger.warning(f"Feed already parsing: ID {feed_id}")
                results.append({
                    "feed_id": feed_id,
                    "status": "already_parsing",
                    "error": "Feed is already being parsed"
                })
                continue
            
            try:
                result = _parse_and_update_feed_object(feed)  # Use helper to avoid redundant lookup
                if result and result.get('status') == 'success':
                    success_count += 1
                    results.append({
                        "feed_id": feed_id,
                        "status": "success",
                        "channel_id": result.get('channel_id'),
                        "item_count": result.get('item_count')
                    })
                else:
                    failed_count += 1
                    results.append({
                        "feed_id": feed_id,
                        "status": "failed",
                        "error": result.get('error', 'Unknown error')
                    })
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to reparse feed {feed_id}: {str(e)}")
                results.append({
                    "feed_id": feed_id,
                    "status": "failed",
                    "error": str(e)
                })
        
        logger.info(f"Bulk reparse completed: {success_count} success, {failed_count} failed, {not_found_count} not found, {already_parsing_count} already parsing")
        return {
            "success": success_count,
            "failed": failed_count,
            "not_found": not_found_count,
            "already_parsing": already_parsing_count,
            "total_requested": len(feed_ids),
            "results": results
        }
        
    except Exception as e:
        log_error("bulk_reparse_feeds", e)
        raise DatabaseError(f"Failed to bulk reparse feeds: {str(e)}")
    
