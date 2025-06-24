from flask import request, jsonify
from app.blueprints.category import category_bp


@category_bp.route('', methods=['GET'])
def list_categories():
    """
    List podcast categories
    GET /categories
    """
    try:
        # TODO: Implement category listing from database
        # Primary table: category
        # Use case: Used to classify channels into hierarchical genres
        
        return jsonify({
            'message': 'Categories endpoint - implementation needed',
            'data': []
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve categories',
            'message': str(e)
        }), 500 