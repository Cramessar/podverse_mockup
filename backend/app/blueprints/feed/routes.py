from flask import request, jsonify
from faker import Faker
from . import feed_bp
from .schemas import feed_schema, feeds_schema  # ✅ Clean, non-circular
from app.models.feed import Feed
from app.extensions import db
from app.services.feed_parser import parse_rss_feed
from app.utils.logger import get_logger, log_request, log_database_operation
from marshmallow import ValidationError
from .services import create_feed_service, DuplicateFeedError
from sqlalchemy import select
from app.utils.error_exceptions import ValidationError as APIValidationError


fake = Faker()
logger = get_logger(__name__)

@feed_bp.route('/', methods=['POST'])
def create_feed():
    if not request.is_json:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400
    
    try:     
        # Validate the input data without creating an instance
        feed_data = feed_schema.load(request.get_json(), session=db.session) # validate and deserialize input
        # Controller passes to service
        feed = create_feed_service(feed_data)
        return jsonify(feed_schema.dump(feed)), 201
    
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400 
    
    except DuplicateFeedError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        db.session.rollback()  # Rollback to avoid leaving the session in a broken state
        logger.error(f"Error creating feed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@feed_bp.route('', methods=['GET'])
def get_all_feeds():
    log_request(logger, 'GET', '/feeds')
    query = select(Feed)
    feeds= db.session.execute(query).scalars().all()
    
    return jsonify(feeds_schema.dump(feeds)), 200
    
