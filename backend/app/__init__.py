# app/__init__.py

from flask import Flask, request, g
from app.extensions import ma, db #,migrate
from app.blueprints import register_blueprints
from flask_cors import CORS
from config import config_by_name
from app.utils.logger import get_logger, log_request, log_security_event
import time

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # initialize extensions
    ma.init_app(app)
    db.init_app(app)
    #migrate.init_app(app, db)
    
    # secure CORS configuration for frontend-backend communication
    CORS(app, 
         origins=["http://localhost:3000", "http://frontend:3000"],  # Allow both local and Docker network access
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    
    # Setup global request logging
    logger = get_logger(__name__)
    
    @app.before_request
    def before_request():
        """Log incoming requests and start timer"""
        g.start_time = time.time()
        
        # Log the incoming requst
        endpoint = request.endpoint or request.path
        logger.info(f"REQUEST START: {request.method} {request.path}")
        
        # Log security-relevant headers
        user_agent = request.headers.get('User-Agent', 'Unknown')
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        logger.info(f"REQUEST INFO: IP={ip}, User-Agent={user_agent[:100]}")
        
        # Check for potential security issues
        if len(request.path) > 1000:
            log_security_event(logger, 'SUSPICIOUS_REQUEST', details=f'Very long path: {len(request.path)} chars')
        
        # Log authentication header presence (without revealing token details)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            logger.info(f"REQUEST AUTH: Authorization header present")
        else:
            logger.info(f"REQUEST AUTH: No authorization header")
    
    @app.after_request
    def after_request(response):
        """Log response and completion time"""
        total_time = time.time() - g.start_time if hasattr(g, 'start_time') else 0
        
        logger.info(f"RESPONSE: {request.method} {request.path} - {response.status_code} - {total_time:.3f}s")
        
        # Log error responses
        if response.status_code >= 400:
            logger.warning(f"ERRORR RESPONSE: {request.method} {request.path} - {response.status_code}")
            
        # Log security events for suspicious status codes
        if response.status_code in [401, 403]:
            log_security_event(logger, 'ACCESS_DENIED', 
                             details=f'{request.method} {request.path} returned {response.status_code}')
        elif response.status_code == 429:
            log_security_event(logger, 'RATE_LIMIT_HIT', 
                             details=f'{request.method} {request.path}')
        
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        """Log 404 errors"""
        logger.warning(f"404 NOT FOUND: {request.method} {request.path}")
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Log 500 errors"""
        logger.error(f"500 INTERNAL ERROR: {request.method} {request.path} - {str(error)}")
        return {'error': 'Internal server error'}, 500
    
    # register all blueprints
    register_blueprints(app)
    
    return app
