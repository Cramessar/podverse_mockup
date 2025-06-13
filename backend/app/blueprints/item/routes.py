from flask import request, jsonify
from . import item_bp
from .schemas import item_schema, items_schema
from .services import create_item_service

item_service = create_item_service()

@item_bp.route('', methods=['GET'])
def get_items():
    """Get all items - Controller layer"""
    try:
        items = item_service.get_all_items()
        return jsonify(items_schema.dump(items)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@item_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item():
    item_id = request.args.get('id', type=int)
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400

    try:
        item = item_service.get_item_by_id(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify(item_schema.dump(item)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@item_bp.route('/items/channel/<int:channel_id>', methods=['GET'])
def get_items_by_channel():
    channel_id = request.args.get('channel_id', type=int)
    if not channel_id:
        return jsonify({'error': 'Channel ID is required'}), 400

    try:
        items = item_service.get_items_by_channel_id(channel_id)
        return jsonify(items_schema.dump(items)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@item_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        item = item_service.create_item(data)
        return jsonify(item_schema.dump(item)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@item_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        item = item_service.update_item(item_id, data)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify(item_schema.dump(item)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@item_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        success = item_service.delete_item(item_id)
        if not success:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500