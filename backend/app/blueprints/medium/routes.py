from flask import request, jsonify
from . import medium_bp


@medium_bp.route('', methods=['GET'])
def list_mediums():
    """
    List all media types
    GET /mediums
    """
    try:
        # TODO: Implement medium listing from database
        # Primary table: medium
        # Use case: Channels reference this table to define their content type - podcast, video, etc.
        
        return jsonify({
            'message': 'Mediums endpoint - implementation needed',
            'data': []
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve mediums',
            'message': str(e)
        }), 500 