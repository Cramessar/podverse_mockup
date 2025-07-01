import pytest
from app import create_app
from app.extensions import db as _db

@pytest.fixture(scope='session')
def app():
    """Create a Flask app context for the tests."""
    app = create_app('testing')
    
    # Create an application context
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def db(app):
    """Create a database for the tests."""
    _db.create_all()
    yield _db
    _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    
    db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove() 