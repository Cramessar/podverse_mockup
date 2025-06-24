import pytest
from app.extensions import ValidationError
from app.blueprints.feed.schemas import FeedSchema, FeedFlagStatusSchema, FeedLogSchema
from app.models.feed import Feed, FeedFlagStatus, FeedLog


class TestFeedSchema:
    @pytest.fixture
    def valid_feed_data(self):
        return {
            "feed_flag_status_id": 1,
            "url": "http://example.com/feed",
            "last_parsed_file_hash": "abc123",
            "parsing_priority": 10,
            "container_id": "container123",
            "is_parsing": False
        }
        
    def invalid_feed_data(self):
        return {
            "id": None,  # Invalid: id cannot be None
            "feed_flag_status_id": 1,
            "url": "http://example.com/feed"
        }
        
    def test_feed_schema_valid_data(self, valid_feed_data):
        result = FeedSchema().load(valid_feed_data)
        assert isinstance(result, Feed)
        assert result.url == "http://example.com/feed"
        
    def test_feed_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            FeedSchema().load(self.invalid_feed_data())
            
class TestFeedFlagStatusSchema:
    @pytest.fixture
    def valid_feed_flag_status_data(self):
        return {
            "status": "active"
        }

    def invalid_feed_flag_status_data(self):
        return {
            "id": None,  # Invalid: id cannot be None
            "status": "active"
        }

    def test_feed_flag_status_schema_valid_data(self, valid_feed_flag_status_data):
        result = FeedFlagStatusSchema().load(valid_feed_flag_status_data)
        assert isinstance(result, FeedFlagStatus)
        assert result.status == "active"

    def test_feed_flag_status_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            FeedFlagStatusSchema().load(self.invalid_feed_flag_status_data())
            
class TestFeedLogSchema:
    @pytest.fixture
    def valid_feed_log_data(self):
        return {
            "feed_id": 1,
            "last_http_status": 200,
            "last_good_http_status_time": "2023-10-01T12:00:00Z",
            "last_finished_parse_time": "2023-10-01T12:00:00Z",
            "parse_errors": 0
        }

    def invalid_feed_log_data(self):
        return {
            "feed_id": None,  # Invalid: feed_id cannot be None
            "last_http_status": 200
        }

    def test_feed_log_schema_valid_data(self, valid_feed_log_data):
        result = FeedLogSchema().load(valid_feed_log_data)
        assert isinstance(result, FeedLog)
        assert result.last_http_status == 200

    def test_feed_log_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            FeedLogSchema().load(self.invalid_feed_log_data())
        
    