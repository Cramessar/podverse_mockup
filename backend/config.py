#backend/config/config.py

import os

# Each env uses the same DB URI by default, but can override with env vars
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    
    # Request size limits (16MB in bytes)
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

    # Feed parsing configuration - seconds
    FEED_ITEM_LIMIT = int(os.getenv('FEED_ITEM_LIMIT', 500))
    FEED_REQUEST_TIMEOUT = int(os.getenv('FEED_REQUEST_TIMEOUT', 10))
    FEED_REQUEST_RETRIES = int(os.getenv('FEED_REQUEST_RETRIES', 2))

    # Redis configuration
    REDIS_URL = os.getenv("REDIS_URL")  # Default Redis URL for all environments
    
    # Celery configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = os.getenv("REDIS_RESULT_BACKEND", REDIS_URL)
    CELERY_TASK_IGNORE_RESULT = True
  
    # Auth0 configuration
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    API_AUDIENCE = os.getenv("API_AUDIENCE")
    ALGORITHMS = [os.getenv("ALGORITHMS", "RS256")]


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    TESTING = True
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL")

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}