# app/utils/error_handlers.py

from flask import jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.extensions import ValidationError as MarshmallowValidationError
from werkzeug.exceptions import HTTPException
from app.utils.error_exceptions import APIException, ValidationError, NotFoundError, DatabaseError
import traceback
from app.utils.logger import get_logger

logger = get_logger(__name__)

def register_error_handlers(app):
    
    @app.errorhandler(APIException)
    def handle_api_exception(e):
        response = {
            'error': {
                'message': e.message,
                'status_code': e.status_code
            }
        }
        if e.payload:
            response['error']['payload'] = e.payload
            
        return jsonify(response), e.status_code
    
    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_validation_error(e):
        response = {
            'error': {
                'message': 'Validation Error',
                'status_code': 400,
                'errors': e.messages
            }
        }
        return jsonify(response), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(e):
        current_app.logger.error(f"Database error: {str(e)}")
        
        if isinstance(e, IntegrityError):
            return jsonify({
                'error': {
                    'message': 'Data integrity constranit Error',
                    'status_code': 409
                }
            }), 409
            
        return jsonify({
            'error': {
                'message': 'Database operation failed',
                'status_code': 500
            }
        }), 500
        
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            'error': {
                'message': error.description,
                'status_code': error.code
            }
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        current_app.logger.error(f"Unhandled exception: {str(error)}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            'error': {
                'message': 'An unexpected error occurred',
                'status_code': 500
            }
        }), 500