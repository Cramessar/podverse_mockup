# app/__init__.py

from flask import Flask
from .extensions import ma, db
from .blueprints import register_blueprints

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    # initialize extensions
    ma.init_app(app)
    db.init_app(app)
    
    # register all blueprints
    register_blueprints(app)
    
    return app
