import os

# changed config to use postgresql instead of sqlite
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://podverse_admin:testest@database:5432/podverse_db"
    )
    DEBUG = True
    

class ProductionConfig:
    pass

class TestingConfig:
    pass
