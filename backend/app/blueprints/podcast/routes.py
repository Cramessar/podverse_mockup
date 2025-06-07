from flask import request, jsonify
from . import podcast_bp
from .schemas import podcast_schema, podcasts_schema
from .services import create_podcast_service
from flask import Blueprint

# Create service instance using factory
podcast_service = create_podcast_service()

@podcast_bp.route('', methods=['GET'])
def get_podcasts():
    """Get all podcasts - Controller layer"""
    try:
        podcasts = podcast_service.get_all_podcasts()
        return jsonify(podcasts_schema.dump(podcasts)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

