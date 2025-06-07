import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///podverse.db"
    DEBUG = True
    
class ProductionConfig:
    pass

class TestingConfig:
    pass