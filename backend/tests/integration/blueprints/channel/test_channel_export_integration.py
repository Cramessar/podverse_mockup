import pytest
from unittest.mock import patch
import csv
import io
from flask import Flask

from app.models.channel import Channel
from app.models.medium import Medium
from app.models.feed import Feed


class TestChannelExportIntegration:
    """Integration tests for channel export functionality."""
    
    @pytest.fixture
    def client(self, app):
        """Create a test client for the Flask application."""
        return app.test_client()
    
    @pytest.fixture
    def auth_headers(self):
        """Mock authorization headers for testing."""
        return {'Authorization': 'Bearer valid.jwt.token'}
    
    @pytest.fixture
    def mock_auth_success(self):
        """Mock successful authentication."""
        with patch('app.blueprints.channel.routes.requires_auth') as mock_auth:
            def decorator(f):
                return f
            mock_auth.return_value = decorator
            yield mock_auth
    
    @pytest.fixture
    def sample_channels(self, app):
        """Create sample channels for testing."""
        with app.app_context():
            from app.extensions import db
            
            # Create sample medium
            medium = Medium(id=1, name='podcast', slug='podcast')
            db.session.add(medium)
            
            # Create sample feed
            feed = Feed(
                id=1,
                url='https://example.com/feed.xml',
                status='active',
                title='Test Feed'
            )
            db.session.add(feed)
            
            # Create sample channels
            channels = [
                Channel(
                    id=1,
                    id_text='ch001',
                    title='Test Channel 1',
                    sortable_title='test channel 1',
                    slug='test-channel-1',
                    medium_id=1,
                    feed_id=1,
                    podcast_index_id=12345,
                    podcast_guid='guid-123',
                    has_podcast_index_value=True,
                    has_value_time_splits=False
                ),
                Channel(
                    id=2,
                    id_text='ch002',
                    title='Test Channel 2',
                    sortable_title='test channel 2',
                    slug='test-channel-2',
                    medium_id=1,
                    feed_id=None,
                    podcast_index_id=None,
                    podcast_guid=None,
                    has_podcast_index_value=False,
                    has_value_time_splits=True
                )
            ]
            
            for channel in channels:
                db.session.add(channel)
            
            db.session.commit()
            
            yield channels
            
            # Cleanup
            db.session.query(Channel).delete()
            db.session.query(Feed).delete()
            db.session.query(Medium).delete()
            db.session.commit()
    
    def test_export_channels_complete_flow(self, client, auth_headers, mock_auth_success, sample_channels):
        """Test complete export flow with real data."""
        response = client.get('/channels/export', headers=auth_headers)
        
        # Check response
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
        assert 'Content-Disposition' in response.headers
        assert 'attachment' in response.headers['Content-Disposition']
        assert 'channels_export_' in response.headers['Content-Disposition']
        
        # Parse CSV content
        csv_content = response.get_data(as_text=True)
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        
        # Should have 2 channels
        assert len(rows) == 2
        
        # Check first channel data
        channel1 = rows[0]
        assert channel1['id'] == '1'
        assert channel1['title'] == 'Test Channel 1'
        assert channel1['id_text'] == 'ch001'
        assert channel1['medium_name'] == 'podcast'
        assert channel1['feed_url'] == 'https://example.com/feed.xml'
        assert channel1['has_podcast_index_value'] == 'True'
        
        # Check second channel data
        channel2 = rows[1]
        assert channel2['id'] == '2'
        assert channel2['title'] == 'Test Channel 2'
        assert channel2['id_text'] == 'ch002'
        assert channel2['medium_name'] == 'podcast'
        assert channel2['feed_url'] == ''  # No feed associated
        assert channel2['has_value_time_splits'] == 'True'
    
    def test_export_channels_with_search_filter(self, client, auth_headers, mock_auth_success, sample_channels):
        """Test export with search filtering."""
        response = client.get('/channels/export?search=Channel 1', headers=auth_headers)
        
        assert response.status_code == 200
        
        # Parse CSV content
        csv_content = response.get_data(as_text=True)
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        
        # Should only have 1 channel (filtered)
        assert len(rows) == 1
        assert rows[0]['title'] == 'Test Channel 1'
    
    def test_export_channels_with_sorting(self, client, auth_headers, mock_auth_success, sample_channels):
        """Test export with sorting."""
        response = client.get('/channels/export?sort_by=title&sort_order=desc', headers=auth_headers)
        
        assert response.status_code == 200
        
        # Parse CSV content
        csv_content = response.get_data(as_text=True)
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        
        # Should have 2 channels in descending order by title
        assert len(rows) == 2
        assert rows[0]['title'] == 'Test Channel 2'  # Comes first in desc order
        assert rows[1]['title'] == 'Test Channel 1'
    
    def test_export_channels_with_max_rows_limit(self, client, auth_headers, mock_auth_success, sample_channels):
        """Test export with max_rows parameter."""
        response = client.get('/channels/export?max_rows=1', headers=auth_headers)
        
        assert response.status_code == 200
        
        # Parse CSV content
        csv_content = response.get_data(as_text=True)
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        
        # Should only have 1 channel (limited)
        assert len(rows) == 1
    
    def test_export_channels_empty_results(self, client, auth_headers, mock_auth_success):
        """Test export when no channels match filters."""
        response = client.get('/channels/export?search=nonexistent', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
        
        # Should return empty CSV
        csv_content = response.get_data(as_text=True)
        assert csv_content == ''
    
    def test_export_channels_csv_headers_complete(self, client, auth_headers, mock_auth_success, sample_channels):
        """Test that all expected CSV headers are present."""
        response = client.get('/channels/export', headers=auth_headers)
        
        assert response.status_code == 200
        
        # Parse CSV content
        csv_content = response.get_data(as_text=True)
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        # Check that all expected headers are present
        expected_headers = [
            'id', 'id_text', 'title', 'sortable_title', 'slug',
            'podcast_index_id', 'podcast_guid', 'has_podcast_index_value',
            'has_value_time_splits', 'created_at', 'updated_at',
            'medium_id', 'medium_name', 'feed_id', 'feed_url', 'feed_status',
            'stats_all_time_count', 'stats_month_current_count',
            'stats_week_current_count', 'stats_day_current_count'
        ]
        
        for header in expected_headers:
            assert header in csv_reader.fieldnames, f"Missing header: {header}"
    
    def test_export_channels_rate_limiting(self, client, auth_headers, mock_auth_success):
        """Test that export endpoint has appropriate rate limiting."""
        # This test would need to be adjusted based on your actual rate limiting implementation
        # For now, just verify that multiple requests within reasonable bounds work
        
        for i in range(3):  # Within the 10/minute limit
            response = client.get('/channels/export', headers=auth_headers)
            assert response.status_code == 200
    
    def test_export_channels_authentication_required(self, client):
        """Test that export requires authentication."""
        response = client.get('/channels/export')
        
        # Should return 401 or redirect to login
        assert response.status_code in [401, 302]
    
    @patch('app.blueprints.channel.services.get_channels_for_export')
    def test_export_channels_database_error_handling(self, mock_get_channels, client, auth_headers, mock_auth_success):
        """Test handling of database errors during export."""
        mock_get_channels.side_effect = Exception("Database connection failed")
        
        response = client.get('/channels/export', headers=auth_headers)
        
        # Should return 500 error
        assert response.status_code == 500 