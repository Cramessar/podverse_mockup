# app/__init__.py

from flask import Flask
from .extensions import ma, db #,migrate
from .blueprints import register_blueprints
from flask_cors import CORS
from config import config_by_name

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
    
    # register all blueprints
    register_blueprints(app)
    
    return app
