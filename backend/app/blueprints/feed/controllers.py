#app/blueprints/feed/controllers.py

from flask import request
from werkzeug.datastructures import FileStorage
from app.blueprints.feed.services import parse_and_update_feed, get_all_feeds, import_feeds_from_opml
from app.blueprints.feed.schemas import feeds_schema
from app.utils.query_params import get_pagination_params
from app.utils.error_exceptions import ValidationError
from app.utils.logger import get_logger

logger = get_logger(__name__)

def reparse_feed_controller(feed_id: int):
    """
    Controller to handle feed reparsing
    Coordinates the reparse operation and returns result
    """
    logger.info(f"Starting reparse for feed ID: {feed_id}")
    result = parse_and_update_feed(feed_id)
    logger.info(f"Completed reparse for feed ID: {feed_id} with status: {result.get('status')}")
    return result

def get_feeds_controller():
    """
    Controller to handle getting all feeds with pagination
    Coordinates between request parsing, service calls, and response formatting
    """
    # Get pagination parameters from query string
    page, limit = get_pagination_params(request, default_page=1, default_limit=10, max_limit=100)
    
    logger.info(f"Fetching feeds - page: {page}, limit: {limit}")
    
    # Get feeds with pagination from service
    result = get_all_feeds(page=page, limit=limit)
    
    # Serialize the data
    serialized_data = feeds_schema.dump(result["data"])
    
    logger.info(f"Successfully retrieved {len(serialized_data)} feeds")
    
    return {
        "data": serialized_data,
        "meta": result["meta"]
    }

def import_feeds_controller():
    """
    Controller to handle OPML file upload and feed import
    Coordinates file handling, validation, and import process
    """
    logger.info("Starting OPML feed import")
    
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
    
    logger.info(f"OPML import completed - imported: {result['imported']}, skipped: {result['skipped']}, failed: {result['failed']}")
    
    return result
