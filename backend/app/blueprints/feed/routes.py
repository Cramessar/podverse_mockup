from flask import request, jsonify, abort
from faker import Faker
from . import feed_bp
from .schemas import feed_schema, feeds_schema, feed_log_schema
from app.models.feed import Feed, FeedLog
from app.extensions import db
from app.services.feed_parser import parse_rss_feed
from app.utils.logger import get_logger, log_request, log_database_operation
from datetime import datetime

fake = Faker()
logger = get_logger(__name__)

@feed_bp.route('', methods=['GET'])
def get_feeds():
    log_request(logger, 'GET', '/feeds')

    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)

    try:
        from sqlalchemy import select, func

        log_database_operation(logger, 'READ', 'feed')

        feeds_query = db.session.execute(select(Feed).offset(offset).limit(limit)).scalars().all()
        total_count = db.session.execute(select(func.count(Feed.id))).scalar()

        logger.info(f"Retrieved {len(feeds_query)} feeds (total: {total_count})")

        feeds = []
        for feed in feeds_query:
            feeds.append({
                "id": feed.id,
                "url": feed.url,
                "feed_flag_status_id": feed.feed_flag_status_id,
                "is_parsing": feed.is_parsing,
                "parsing_priority": feed.parsing_priority,
                "last_parsed_file_hash": feed.last_parsed_file_hash,
                "container_id": feed.container_id,
                "created_at": feed.created_at.isoformat() if isinstance(feed.created_at, datetime) else None,
                "updated_at": feed.updated_at.isoformat() if isinstance(feed.updated_at, datetime) else None
            })

        log_request(logger, 'GET', '/feeds', 200)
        return jsonify({"data": feeds, "meta": {"total": total_count, "limit": limit, "offset": offset}}), 200

    except Exception as e:
        logger.error(f"Error retrieving feeds: {str(e)}")
        log_request(logger, 'GET', '/feeds', 500)
        return jsonify({"error": "Internal server error"}), 500

@feed_bp.route('/<int:feed_id>', methods=['GET'])
def get_feed_by_id(feed_id):
    log_request(logger, 'GET', f'/feeds/{feed_id}')

    try:
        from sqlalchemy import select

        log_database_operation(logger, 'READ', 'feed', feed_id)

        feed = db.session.execute(select(Feed).where(Feed.id == feed_id)).scalar_one_or_none()

        if feed is None:
            logger.warning(f"Feed not found: ID {feed_id}")
            log_request(logger, 'GET', f'/feeds/{feed_id}', 404)
            abort(404)

        logger.info(f"Retrieved feed: {feed.url}")
        log_request(logger, 'GET', f'/feeds/{feed_id}', 200)

        return jsonify({
            "id": feed.id,
            "url": feed.url,
            "feed_flag_status_id": feed.feed_flag_status_id,
            "is_parsing": feed.is_parsing,
            "parsing_priority": feed.parsing_priority,
            "last_parsed_file_hash": feed.last_parsed_file_hash,
            "container_id": feed.container_id,
            "created_at": feed.created_at.isoformat() if isinstance(feed.created_at, datetime) else None,
            "updated_at": feed.updated_at.isoformat() if isinstance(feed.updated_at, datetime) else None
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving feed {feed_id}: {str(e)}")
        log_request(logger, 'GET', f'/feeds/{feed_id}', 500)
        return jsonify({"error": "Internal server error"}), 500

@feed_bp.route('/<int:feed_id>/logs', methods=['GET'])
def get_feed_logs(feed_id):
    log_request(logger, 'GET', f'/feeds/{feed_id}/logs')

    try:
        from sqlalchemy import select

        logs = db.session.execute(
            select(FeedLog).where(FeedLog.feed_id == feed_id).order_by(FeedLog.last_finished_parse_time.desc())
        ).scalars().all()

        return jsonify({
            "feed_id": feed_id,
            "logs": feed_log_schema.dump(logs, many=True)
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving logs for feed {feed_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@feed_bp.route('/<int:feed_id>/reparse', methods=['POST'])
def reparse_feed(feed_id):
    log_request(logger, 'POST', f'/feeds/{feed_id}/reparse')

    try:
        logger.info(f"Reparse requested for feed ID: {feed_id}")
        # TODO: Implement feed reparse logic

        log_request(logger, 'POST', f'/feeds/{feed_id}/reparse', 200)
        return jsonify({
            'message': 'Feed reparse has been scheduled.'
        }), 200

    except Exception as e:
        logger.error(f"Error scheduling reparse for feed {feed_id}: {str(e)}")
        log_request(logger, 'POST', f'/feeds/{feed_id}/reparse', 500)
        return jsonify({'error': str(e)}), 500

@feed_bp.route('/<int:feed_id>', methods=['PATCH'])
def update_feed(feed_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # TODO: Implement feed update logic
        return jsonify({
            'message': 'Feed update endpoint - implementation needed',
            'feed_id': feed_id,
            'data': data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feed_bp.route('', methods=['POST'])
def create_feed():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # TODO: Implement proper feed creation with validation
        return jsonify({
            'message': 'Create feed endpoint - implementation needed',
            'data': data
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@feed_bp.route('/parse-feed', methods=['GET'])
def parse_feed():
    log_request(logger, 'GET', '/feeds/parse-feed')

    url = request.args.get('url')
    if not url:
        logger.warning("Parse feed request missing URL parameter")
        log_request(logger, 'GET', '/feeds/parse-feed', 400)
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        logger.info(f"Parsing RSS feed: {url}")
        feed_info, items = parse_rss_feed(url)

        logger.info(f"Successfully parsed feed: {url} - Found {len(items)} items")
        log_request(logger, 'GET', '/feeds/parse-feed', 200)

        return jsonify({'feed_info': feed_info, 'items': items})

    except Exception as e:
        logger.error(f"Error parsing RSS feed {url}: {str(e)}")
        log_request(logger, 'GET', '/feeds/parse-feed', 500)
        return jsonify({'error': 'Failed to parse RSS feed'}), 500
