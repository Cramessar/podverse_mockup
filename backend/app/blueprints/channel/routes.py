from flask import request, jsonify
from . import channel_bp
from .schemas import channel_schema, channels_schema
from .services import create_channel_service

# Create service instance using factory
channel_service = create_channel_service()

@channel_bp.route('', methods=['GET'])
def get_channels():
    """
    Retrieve a list of channels
    GET /channels
    """
    try:
        # Get query parameters for pagination and filtering
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        search = request.args.get('search', '')
        sort_by = request.args.get('sort_by', 'id')
        sort_order = request.args.get('sort_order', 'desc')
        
        # TODO: Implement with proper pagination and filtering
        channels = channel_service.get_all_channels()
        
        return jsonify({
            'data': channels_schema.dump(channels),
            'meta': {
                'total': len(channels),
                'limit': limit,
                'offset': offset
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@channel_bp.route('/<int:id>', methods=['GET'])
def get_channel_by_id(id):
    """
    Retrieve a channel by ID
    GET /channels/{id}
    """
    try:
        channel = channel_service.get_channel_by_id(id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404
        return jsonify(channel_schema.dump(channel)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@channel_bp.route('/', methods=['POST'])
def create_channel():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        new_channel = channel_service.create_channel(data)
        return jsonify(channel_schema.dump(new_channel)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@channel_bp.route('/<int:channel_id>', methods=['PUT'])
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
    
@channel_bp.route('/<int:channel_id>', methods=['DELETE'])
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


