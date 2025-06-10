from flask import request, jsonify
from . import channel_bp
from .schemas import channel_schema, channels_schema
from .services import create_channel_service
from flask import Blueprint

# Create service instance using factory
channel_service = create_channel_service()

@channel_bp.route('', methods=['GET'])
def get_channels():
    """Get all channels - Controller layer"""
    try:
        channels = channel_service.get_all_channels()
        return jsonify(channels_schema.dump(channels)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

