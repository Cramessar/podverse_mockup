from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db

db_test_bp = Blueprint('db_test', __name__)

@db_test_bp.route('/test-db', methods=['GET'])
def test_db():
    try:
        with db.engine.connect() as conn:
            # Run a simple test query
            result = conn.execute(text("SELECT NOW() as current_time"))
            current_time = result.scalar()  # Get first column of first row
        return jsonify({"status": "success", "current_time": str(current_time)}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# http://localhost:8000/test-db as a sanity check to ensure the database connection is working