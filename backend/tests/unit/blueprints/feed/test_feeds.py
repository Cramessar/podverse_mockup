import os
import pytest
from app import create_app
from app.extensions import db
from app.models.feed import Feed, FeedFlagStatus

@pytest.fixture
def app():
    # Store original environment variables
    original_database_url = os.environ.get('DATABASE_URL')
    original_test_database_url = os.environ.get('TEST_DATABASE_URL')
    
    # Set the test database URL and clear any conflicting DATABASE_URL
    os.environ['TEST_DATABASE_URL'] = 'postgresql://podverse_admin:testest@database:5432/podverse_db'
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    try:
        # Create the app with testing config
        app = create_app('testing')
        
        with app.app_context():
            # Import only the models we need for feed tests
            from app.models.feed import Feed, FeedFlagStatus, FeedLog
            
            # Reset database schema - only create the tables we need
            db.drop_all()
            
            # Create tables manually for just the feed-related models
            FeedFlagStatus.__table__.create(db.engine, checkfirst=True)
            Feed.__table__.create(db.engine, checkfirst=True)
            FeedLog.__table__.create(db.engine, checkfirst=True)
            
            # Get or create feed flag status
            status = db.session.query(FeedFlagStatus).filter_by(status='active').first()
            if not status:
                status = FeedFlagStatus(status='active')
                db.session.add(status)
                db.session.commit()
            
            yield app
            
            # Clean up - but keep the database structure
            db.session.query(Feed).delete()
            db.session.commit()
    
    finally:
        # Restore original environment variables
        if original_database_url is not None:
            os.environ['DATABASE_URL'] = original_database_url
        if original_test_database_url is not None:
            os.environ['TEST_DATABASE_URL'] = original_test_database_url
        else:
            if 'TEST_DATABASE_URL' in os.environ:
                del os.environ['TEST_DATABASE_URL']

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def feed_flag_status(app):
    with app.app_context():
        status = db.session.query(FeedFlagStatus).filter_by(status='active').first()
        return status

def test_create_feed_success(client, feed_flag_status):
    """Test successful feed creation"""
    # Arrange
    test_feed_data = {
        "url": "http://example.com/feed.xml",
        "feed_flag_status_id": feed_flag_status.id,
        "parsing_priority": 1,
        "is_parsing": None  # Feed is not currently being parsed
    }
    
    # Act
    response = client.post('/admin/feeds/', json=test_feed_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json['url'] == test_feed_data['url']
    assert response.json['feed_flag_status_id'] == feed_flag_status.id

def test_create_feed_duplicate_url(client, feed_flag_status):
    """Test handling of duplicate feed URLs"""
    # Arrange
    test_feed_data = {
        "url": "http://example.com/feed.xml",
        "feed_flag_status_id": feed_flag_status.id,
        "parsing_priority": 1,
        "is_parsing": None  # Feed is not currently being parsed
    }
    
    # Create first feed
    client.post('/admin/feeds/', json=test_feed_data)
    
    # Act - try to create duplicate
    response = client.post('/admin/feeds/', json=test_feed_data)
    
    # Assert
    assert response.status_code == 400
    assert "already exists" in response.json.get('error', '')

def test_create_feed_invalid_json(client):
    """Test handling of invalid JSON input"""
    # Act
    response = client.post('/admin/feeds/', data='invalid json')
    
    # Assert
    assert response.status_code == 400
    assert "Invalid or missing JSON body" in response.json.get('error', '')

def test_create_feed_missing_required_fields(client):
    """Test handling of missing required fields"""
    # Act
    response = client.post('/admin/feeds/', json={})
    
    # Assert
    assert response.status_code == 400
    assert 'url' in str(response.json)  # Validation error for missing url
    assert 'feed_flag_status_id' in str(response.json)  # Validation error for missing status

# Add more tests for other failure cases