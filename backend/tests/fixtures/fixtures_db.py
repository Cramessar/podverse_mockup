import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.extensions import db

@pytest.fixture(scope="session")
def database_engine():
    pass