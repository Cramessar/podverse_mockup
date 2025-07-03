# backend/app/__init__.py

from flask import Flask, request, g
from app.extensions import ma, db, limiter, migrate
from app.blueprints import register_blueprints
from flask_cors import CORS
from config import config_by_name
from app.utils.logger import get_logger, log_request_start, log_request_end
from app.utils.error_handlers import register_error_handlers
from app.utils.auth import AuthError
import os

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Load Auth0-related config into app.config
    app.config['AUTH0_DOMAIN'] = os.getenv("AUTH0_DOMAIN")
    app.config['API_AUDIENCE'] = os.getenv("API_AUDIENCE")
    app.config['ALGORITHMS'] = os.getenv("ALGORITHMS", "RS256")

    # initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)
    
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
        log_request_start(logger)
    
    @app.after_request
    def after_request(response):
        """Log response and completion time"""
        return log_request_end(logger, response)
    
    # Register custom AuthError handler for JWT-related failures
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return {"error": ex.error}, ex.status_code
    
    # register error handlers
    register_error_handlers(app)
    
    # register all blueprints
    register_blueprints(app)
    
    return app
