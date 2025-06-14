from flask import request, jsonify
from . import feed_bp
from .schemas import feed_schema, feeds_schema
from .services import create_feed_service

feed_service = create_feed_service()

@feed_bp.route('', methods=['GET'])
def get_feeds():
    """Get all feeds - Controller layer"""
    try:
        feeds = feed_service.get_all_feeds()
        return jsonify(feeds_schema.dump(feeds)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@feed_bp.route('/feeds/<int:feed_id>', methods=['GET'])
def get_feed(feed_id):
    if not feed_id:
        return jsonify({'error': 'Feed ID is required'}), 400

    try:
        feed = feed_service.get_feed_by_id(feed_id)
        if not feed:
            return jsonify({'error': 'Feed not found'}), 404
        return jsonify(feed_schema.dump(feed)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@feed_bp.route('/feeds', methods=['POST'])
def create_feed():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        feed = feed_service.create_feed(data)
        return jsonify(feed_schema.dump(feed)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@feed_bp.route('/feeds/<int:feed_id>', methods=['PUT'])
def update_feed(feed_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    try:
        feed = feed_service.update_feed(feed_id, data)
        if not feed:
            return jsonify({'error': 'Feed not found'}), 404
        return jsonify(feed_schema.dump(feed)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@feed_bp.route('/feeds/<int:feed_id>', methods=['DELETE'])
def delete_feed(feed_id):
    if not feed_id:
        return jsonify({'error': 'Feed ID is required'}), 400

    try:
        success = feed_service.delete_feed(feed_id)
        if not success:
            return jsonify({'error': 'Feed not found'}), 404
        return jsonify({'message': 'Feed deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
