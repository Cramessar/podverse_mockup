# backend/app/__init__.py

from flask import Flask
from app.extensions import ma, db, limiter, migrate
from app.blueprints import register_blueprints
from flask_cors import CORS
from config import config_by_name
from app.utils.request_logger import register_logging
from app.utils.error_handlers import register_error_handlers
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    

    # initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    
    # secure CORS configuration for frontend-backend communication
    CORS(app, 
         origins=os.getenv("CORS_ORIGINS", "").split(","), # Allow both local and Docker network access
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    
    register_logging(app)
    
    register_error_handlers(app)
    register_blueprints(app)

    return app
