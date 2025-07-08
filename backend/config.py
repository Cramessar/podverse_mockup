import os

# Each env uses the same DB URI by default, but can override with env vars
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    
    # Feed parsing configuration
    FEED_ITEM_LIMIT = 500
    FEED_REQUEST_TIMEOUT = 10  # seconds
    FEED_REQUEST_RETRIES = 2


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://podverse_admin:testest@database:5432/podverse_db"
    )
    DEBUG = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://podverse_admin:testest@database:5432/podverse_db"
    )
    TESTING = True
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "PROD_DATABASE_URL",
        "postgresql://podverse_admin:testest@database:5432/podverse_db"
    )

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}