#app/blueprints/feed/controllers.py

from flask import request
from werkzeug.datastructures import FileStorage
from app.blueprints.feed.services import (
    parse_and_update_feed,
    get_all_feeds,
    import_feeds_from_opml,
    get_feed_by_id,
    create_single_feed,
    get_feeds_for_export,
    bulk_update_feeds,
    bulk_reparse_feeds,
    get_feed_logs
)
from app.blueprints.feed.schemas import feeds_schema, feed_schema, feeds_export_schema, feed_export_schema, feed_logs_schema
from app.utils.query_params import get_pagination_params, get_sorting_params, get_search_query
from app.utils.error_exceptions import ValidationError, NotFoundError, DatabaseError
from app.utils.request_logger import get_logger, log_database_operation
from app.utils.export_response import generate_export_response
from datetime import datetime
from app.tasks.feed_task import reparse_feed_task
from app.utils.export_logging import create_export_log_simple, finalize_export_log   

logger = get_logger(__name__)

def create_feed_controller():
    """
    Controller to handle single feed creation
    Validates request data and coordinates feed creation
    """
    logger.info("Starting single feed creation")
    log_database_operation(logger, "CREATE", "feeds", "single_feed_attempt")
    
    # Validate request has JSON data
    if not request.is_json:
        logger.warning("Feed creation attempt without JSON data")
        raise ValidationError("Request must contain JSON data")
    
    data = request.get_json()
    
    # Basic validation
    if not data or 'url' not in data:
        logger.warning("Feed creation attempt without URL")
        raise ValidationError("URL is required")
    
    url = data['url'].strip()
    if not url:
        raise ValidationError("URL cannot be empty")
    
    parsing_priority = data.get('parsing_priority', 0)
    if not isinstance(parsing_priority, int) or parsing_priority < 0 or parsing_priority > 10:
        raise ValidationError("parsing_priority must be an integer between 0 and 10")
    
    # Create the feed
    feed = create_single_feed(url=url, parsing_priority=parsing_priority)
    
    # Check for async flag (query param ?async=true or JSON field "async": true)
    async_flag = request.args.get("async", "").lower() == "true" or data.get("async", False)
    if async_flag:
        # Queue background Celery task and return immediately
        reparse_feed_task.delay(feed.id)
        serialized_feed = feed_schema.dump(feed)
        serialized_feed["queued"] = True
        return serialized_feed, 202

    # Immediately parse the feed after creation (synchronous path)
    parse_result = parse_and_update_feed(feed.id)
    
    # Serialize and return the created feed
    serialized_feed = feed_schema.dump(feed)
    serialized_feed["channel_id"] = parse_result.get("channel_id")
    serialized_feed["item_count"] = parse_result.get("item_count")
    
    logger.info(f"Successfully created and serialized feed: ID {feed.id}")
    
    return serialized_feed


def reparse_feed_controller(feed_id: int, async_mode: bool = False):
    """
    Controller to handle feed reparsing
    Coordinion and returns result
    """
    logger.info(f"Starting reparse for feed ID: {feed_id}")
    log_database_operation(logger, "UPDATE", "feeds", feed_id)
    
    # First check if feed exists
    feed = get_feed_by_id(feed_id)
    if not feed:
        logger.warning(f"Feed not found: ID {feed_id}")
        raise NotFoundError("Feed not found")
        
    if feed.is_parsing:
        logger.warning(f"Feed {feed_id} is already being parsed")
        return {"status": "error", "message": "Feed is already being parsed"}, 409
    
    try:
        if async_mode:
            # Queue the task
            task = reparse_feed_task.delay(feed_id)
            logger.info(f"Queued reparse task for feed {feed_id}, task id: {task.id}")
            return {
                "status": "queued",
                "feed_id": feed_id,
                "task_id": task.id,
                "message": "Feed reparse queued successfully"
            }, 202
        else:
            # Synchronous reparse
            result = parse_and_update_feed(feed_id)
            if result.get('status') == 'success':
                logger.info(
                    f"Successfully completed reparse for feed ID: {feed_id}, "
                    f"Channel: {result.get('channel_id')}, Items: {result.get('item_count')}"
                )
            else:
                logger.warning(
                    f"Reparse failed for feed ID: {feed_id}, "
                    f"Status: {result.get('status')}, Error: {result.get('error')}"
                )
            return result, 200
            
    except Exception as e:
        logger.error(f"Error reparsing feed {feed_id}: {str(e)}")
        return {"status": "error", "message": "Failed to reparse feed", "error": str(e)}, 500


def get_all_feeds_controller():
    """
    Controller to handle getting all feeds with pagination
    Coordinates between request parsing, service calls, and response formatting
    """
    logger.info("Starting feed retrieval")
    log_database_operation(logger, "READ", "feeds", "all_feeds_query")
    
    page, limit = get_pagination_params(request)
    sort_by, sort_order = get_sorting_params(request, allowed_fields=['id', 'url', 'updated_at'], default_field='id')
    search = get_search_query(request)
    
    # filtering params
    parsing_priority = request.args.get("parsing_priority")
    is_parsing = request.args.get("is_parsing")
    status = request.args.get("status")
    
    logger.info(f"Fetching feeds - page: {page}, limit: {limit}, - filters: priority={parsing_priority}, parsing={is_parsing}, status={status}")
    log_database_operation(logger, "READ", "feeds", f"paginated_query_p{page}_l{limit}")
    
    # Get feeds with pagination from service
    result = get_all_feeds(
        page=page,
        limit=limit,
        parsing_priority=parsing_priority,
        is_parsing=is_parsing,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search
    )
    
    serialized_data = feeds_schema.dump(result["data"])
    
    logger.info(f"Successfully retrieved and serialized {len(serialized_data)} feeds")
    
    return {
        "data": serialized_data,
        "meta": result["meta"]
    }
  
    
def get_feed_by_id_controller(feed_id: int):
    logger.info(f"Fetching feed by ID: {feed_id}")
    log_database_operation(logger, "READ", "feeds", record_id=feed_id)
    
    feed = get_feed_by_id(feed_id)
    if not feed:
        logger.warning(f"Feed not found: ID {feed_id}")
        raise NotFoundError("Feed not found.")
    
    serialized_feed = feed_schema.dump(feed)
    logger.info(f"Feed found and serialized: ID {feed_id}")
    return serialized_feed


def import_feeds_controller():
    """
    Controller to handle OPML file upload and feed import
    Coordinates file handling, validation, and import process
    """
    logger.info("Starting OPML feed import")
    log_database_operation(logger, "CREATE", "feeds", "bulk_import_attempt")
    
    # Validate file upload
    if 'file' not in request.files:
        logger.warning("Import attempt without file upload")
        raise ValidationError("No file provided. Please upload an OPML file.")
    
    file: FileStorage = request.files['file'] 
    
    if file.filename == '':
        logger.warning("Import attempt with empty filename")
        raise ValidationError("No file selected. Please choose an OPML file to upload.")
    
    # validate file extension 
    if not file.filename.lower().endswith(('.opml', '.xml')):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        raise ValidationError("Invalid file type. Please upload an OPML or XML file.")
    
    # Read file content and log it
    try:
        file_content = file.read().decode('utf-8') # binary to string
        logger.info(f"Successfully read OPML file: {file.filename} ({len(file_content)} characters)")
    except UnicodeDecodeError:
        logger.error(f"Failed to decode OPML file: {file.filename}")
        raise ValidationError("Unable to read file. Please ensure it's a valid UTF-8 encoded OPML file.")
    
    if not file_content.strip(): 
        logger.warning(f"Empty OPML file uploaded: {file.filename}")
        raise ValidationError("File is empty. Please upload a valid OPML file with feed data.")
    
    # Process the import 
    result = import_feeds_from_opml(file_content)
    
    # Log detailed import results
    total_processed = result['imported'] + result['skipped'] + result['failed']
    logger.info(f"OPML import completed - Total processed: {total_processed}, Imported: {result['imported']}, Skipped: {result['skipped']}, Failed: {result['failed']}")
    
    if result['imported'] > 0:
        log_database_operation(logger, "CREATE", "feeds", f"bulk_import_success_{result['imported']}")
    
    return result


def bulk_export_feeds_controller():
    """
    Controller to handle bulk export of feeds
    """
    try:
        # Get query parameters
        sort_by, sort_order = get_sorting_params(request, ['id', 'url', 'updated_at'], default_field='id')
        search = get_search_query(request)
        format = request.args.get("format", "csv")
        admin_email = request.args.get("admin_email")

        if not admin_email:
            raise ValidationError("admin_email is required")

        # create export log
        export_log = create_export_log_simple(
            export_type="feeds",
            filters={"format": format, "admin_email": admin_email},
            status="pending",
            file_path=None,
            admin_email=admin_email
        )

        # Get feeds for export
        feeds = get_feeds_for_export(search=search, sort_by=sort_by, sort_order=sort_order)
        
        # Generate filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"feeds_export_{timestamp}"
        
        # Generate response
        response = generate_export_response(feeds, filename, export_type="feed")
        
        # Update export log with success
        finalize_export_log(
            export_log.id,
            status="success",
            file_path=f"/exports/{filename}.{format}",
            format=format,
            feeds_count=len(feeds)
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in bulk_export_feeds: {str(e)}")
        if export_log:
            finalize_export_log(
                export_log.id,
                status="error",
                error_message=str(e)
            )
        raise DatabaseError("Failed to export feeds")


def export_single_feed_controller(feed_id: int):
    """
    Controller to handle export of a single feed
    """
    try:
        logger.info(f"Exporting single feed: ID {feed_id}")
        log_database_operation(logger, "READ", "feeds", f"export_single_{feed_id}")

        feed = get_feed_by_id(feed_id)
        if not feed:
            logger.warning(f"Feed not found for export: ID {feed_id}")
            raise NotFoundError("Feed not found")

        export_data = [feed_export_schema.dump(feed)]

        # Generate filename
        filename = f"feed_{feed_id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"Generated single feed export file: {filename}")
        return generate_export_response(export_data, filename, "feed")

    except NotFoundError:
        raise
    except ValidationError as e:
        logger.warning(f"Validation error in export_single_feed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in export_single_feed: {str(e)}")
        raise DatabaseError("Failed to export single feed")


def bulk_update_feeds_controller():
    """
    Controller to handle bulk update of feeds
    """
    try:
        logger.info("Starting bulk feed update")
        log_database_operation(logger, "UPDATE", "feeds", "bulk_update_attempt")
        
        # Validate request has JSON data
        if not request.is_json:
            logger.warning("Bulk update attempt without JSON data")
            raise ValidationError("Request must contain JSON data")
        
        data = request.get_json()
        
        # Basic validation
        if not data:
            raise ValidationError("Request body is required")
        
        if 'feed_ids' not in data:
            raise ValidationError("feed_ids is required")
        
        if 'updates' not in data:
            raise ValidationError("updates is required")
        
        feed_ids = data['feed_ids']
        updates = data['updates']
        
        if not isinstance(feed_ids, list) or not feed_ids:
            raise ValidationError("feed_ids must be a non-empty list")
        
        if not isinstance(updates, dict) or not updates:
            raise ValidationError("updates must be a non-empty object")
        
        logger.info(f"Bulk updating {len(feed_ids)} feeds with updates: {list(updates.keys())}")
        
        # Process the bulk update
        result = bulk_update_feeds(feed_ids, updates)
        
        logger.info(f"Bulk update completed - Updated: {result['updated']}, Not found: {result['not_found']}")
        
        return result

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in bulk_update_feeds: {str(e)}")
        raise DatabaseError("Failed to bulk update feeds")


def bulk_reparse_feeds_controller():
    """
    Controller to handle bulk reparse of feeds
    """
    try:
        logger.info("Starting bulk feed reparse")
        log_database_operation(logger, "UPDATE", "feeds", "bulk_reparse_attempt")
        
        # Validate request has JSON data
        if not request.is_json:
            logger.warning("Bulk reparse attempt without JSON data")
            raise ValidationError("Request must contain JSON data")
        
        data = request.get_json()
        
        # Basic validation
        if not data:
            raise ValidationError("Request body is required")
        
        if 'feed_ids' not in data:
            raise ValidationError("feed_ids is required")
        
        feed_ids = data['feed_ids']
        
        if not isinstance(feed_ids, list) or not feed_ids:
            raise ValidationError("feed_ids must be a non-empty list")
        
        # Optional async flag
        async_flag = request.args.get("async", "").lower() == "true" or data.get("async", False)
        if async_flag:
            for fid in feed_ids:
                reparse_feed_task.delay(fid)
            logger.info(f"Queued {len(feed_ids)} feeds for async reparse")
            return {"queued": len(feed_ids), "feed_ids": feed_ids}, 202
        
        logger.info(f"Bulk reparsing {len(feed_ids)} feeds")
        
        # Process the bulk reparse synchronously
        result = bulk_reparse_feeds(feed_ids)
        
        logger.info(f"Bulk reparse completed - Success: {result['success']}, Failed: {result['failed']}, Not found: {result['not_found']}, Already parsing: {result['already_parsing']}")
        
        return result

    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in bulk_reparse_feeds: {str(e)}")
        raise DatabaseError("Failed to bulk reparse feeds")


def get_feed_logs_controller(feed_id: int):
    """
    Controller to handle retrieving logs for a specific feed
    """
    try:
        logger.info(f"Fetching logs for feed ID: {feed_id}")
        log_database_operation(logger, "READ", "feed_logs", f"feed_{feed_id}")

        logs = get_feed_logs(feed_id)
        serialized_logs = feed_logs_schema.dump(logs)
        logger.info(f"Retrieved and serialized {len(serialized_logs)} logs for feed ID {feed_id}")

        return {"logs": serialized_logs}

    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_feed_logs: {str(e)}")
        raise DatabaseError("Failed to retrieve feed logs")
