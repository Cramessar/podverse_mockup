from flask import request, jsonify
from faker import Faker
from . import feed_bp
from .schemas import feed_schema, feeds_schema
from app.models.feed import Feed
from app.extensions import db
from app.services.feed_parser import parse_rss_feed

fake = Faker()

@feed_bp.route('', methods=['GET'])
def get_feeds():
    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    # Query existing feeds from database using SQLAlchemy 2.0 session approach
    from sqlalchemy import select, func
    
    feeds_query = db.session.execute(
        select(Feed).offset(offset).limit(limit)
    ).scalars().all()
    
    total_count = db.session.execute(
        select(func.count(Feed.id))
    ).scalar()
    
    # Convert to dict format for JSON response
    feeds = []
    for feed in feeds_query:
        feeds.append({
            "id": feed.id,
            "url": feed.url,
            "feed_flag_status_id": feed.feed_flag_status_id,
            "is_parsing": feed.is_parsing.isoformat() if feed.is_parsing else None,
            "parsing_priority": feed.parsing_priority,
            "last_parsed_file_hash": feed.last_parsed_file_hash,
            "container_id": feed.container_id,
            "created_at": feed.created_at.isoformat() if feed.created_at else None,
            "updated_at": feed.updated_at.isoformat() if feed.updated_at else None
        })
    
    return jsonify({"data": feeds, "meta": {"total": total_count, "limit": limit, "offset": offset}}), 200

@feed_bp.route('/<int:feed_id>', methods=['GET'])
def get_feed_by_id(feed_id):
    # Query existing feed from database using SQLAlchemy 2.0 session approach
    from sqlalchemy import select
    from flask import abort
    
    feed = db.session.execute(
        select(Feed).where(Feed.id == feed_id)
    ).scalar_one_or_none()
    
    if feed is None:
        abort(404)
    
    return jsonify({
        "id": feed.id,
        "url": feed.url,
        "feed_flag_status_id": feed.feed_flag_status_id,
        "is_parsing": feed.is_parsing.isoformat() if feed.is_parsing else None,
        "parsing_priority": feed.parsing_priority,
        "last_parsed_file_hash": feed.last_parsed_file_hash,
        "container_id": feed.container_id,
        "created_at": feed.created_at.isoformat() if feed.created_at else None,
        "updated_at": feed.updated_at.isoformat() if feed.updated_at else None
    }), 200

@feed_bp.route('/<int:feed_id>/reparse', methods=['POST'])
def reparse_feed(feed_id):
    """
    Trigger RSS feed re-parse
    POST /feeds/{feed_id}/reparse
    """
    try:
        # TODO: Implement feed reparse logic
        # Set is_parsing field to current timestamp
        # Background job will handle actual parsing
        
        return jsonify({
            'message': 'Feed reparse has been scheduled.'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@feed_bp.route('/<int:feed_id>', methods=['PATCH'])
def update_feed(feed_id):
    """
    Update feed status or priority
    PATCH /feeds/{feed_id}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # TODO: Implement feed update logic
        # Update feed_flag_status_id or parsing_priority
        # Validate values: parsing_priority 0-5, valid feed_flag_status_id
        
        return jsonify({
            'message': 'Feed update endpoint - implementation needed',
            'feed_id': feed_id,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feed_bp.route('', methods=['POST'])
def create_feed():
    """
    Create a new feed
    POST /feeds
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # TODO: Implement proper feed creation with validation
        # Required fields: url, feed_flag_status_id
        # Validate URL is unique
        
        # For now, return placeholder response
        return jsonify({
            'message': 'Create feed endpoint - implementation needed',
            'data': data
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@feed_bp.route('/parse-feed', methods=['GET'])
def parse_feed():
    """
    API endpoint to parse an RSS feed URL and return the feed metadata and items. this is a test endpoint to teste the feed parser service on fly 

    Query Parameters:
    - url: The URL of the RSS feed to parse.

    Returns:
    - JSON response containing feed metadata and items.
    """
    # Get the RSS feed URL from query parameters
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    # Call the service function to parse the feed
    feed_info, items = parse_rss_feed(url)

    # Return the parsed data as a JSON response
    return jsonify({'feed_info': feed_info, 'items': items})