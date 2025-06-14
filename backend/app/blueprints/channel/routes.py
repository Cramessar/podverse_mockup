from flask import request, jsonify
from . import channel_bp
from .schemas import channel_schema, channels_schema
from .services import create_channel_service
from flask import Blueprint

# Create service instance using factory
channel_service = create_channel_service()

@channel_bp.route('/channels', methods=['GET'])
def get_channels():
    """Get all channels - Controller layer"""
    try:
        channels = channel_service.get_all_channels()
        return jsonify(channels_schema.dump(channels)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@channel_bp.route('/channels/<int:channel_id>', methods=['GET'])
def get_channel():
    """Get a specific channel by ID - Controller layer"""
    channel_id = request.args.get('channel_id', type=int)
    if not channel_id:
        return jsonify({'error': 'Channel ID is required'}), 400
    
    try:
        channel = channel_service.get_channel_by_id(channel_id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404
        return jsonify(channel_schema.dump(channel)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@channel_bp.route('/channels', methods=['POST'])
def create_channel():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        new_channel = channel_service.create_channel(data)
        return jsonify(channel_schema.dump(new_channel)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@channel_bp.route('/channels/<int:channel_id>', methods=['PUT'])
def update_channel(channel_id):
    if not channel_id:
        return jsonify({'error': 'Channel ID is required'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        channel = channel_service.get_channel_by_id(channel_id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404
        
        updated_channel = channel_service.update_channel(channel_id, data)
        return jsonify(channel_schema.dump(updated_channel)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@channel_bp.route('/channels/<int:channel_id>', methods=['DELETE'])
def delete_channel(channel_id):
    if not channel_id:
        return jsonify({'error': 'Channel ID is required'}), 400

    try:
        channel = channel_service.get_channel_by_id(channel_id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404
        
        channel_service.delete_channel(channel_id)
        return jsonify({'message': 'Channel deleted successfully'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500


