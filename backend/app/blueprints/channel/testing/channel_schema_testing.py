import pytest
from app.extensions import ValidationError
from app.models.channel import Channel,  StatsTrackEventChannel
from app.blueprints.channel.schemas import ChannelSchema, StatsTrackEventChannelSchema
from uuid import uuid4

class TestChannelSchema:
    @pytest.fixture
    def valid_channel_data(self):
        return {
            "id_text": "CH123456789",
            "title": "Test Podcast Channel",
            "slug": "test-podcast-channel",
            "feed_id": 1,
            "podcast_index_id": 12345,
            "podcast_guid": str(uuid4()),
            "sortable_title": "Test Podcast Channel",
            "medium_id": 1,
            "has_podcast_index_value": True,
            "has_value_time_splits": False
        }
        
    def invalid_channel_data(self):
        return {
            "id_text": "CH123456789",
            "title": "",  # Invalid: title cannot be empty
            "slug": "test-podcast-channel",
            "feed_id": 1,
            "podcast_index_id": 12345,
            "podcast_guid": str(uuid4()),
            "sortable_title": "Test Podcast Channel",
            "medium_id": 1,
            "has_podcast_index_value": True,
            "has_value_time_splits": False
        }
    
    def test_channel_schema_valid_data(self, valid_channel_data):
        result = ChannelSchema().load(valid_channel_data)
        assert isinstance(result, Channel)
        assert result.id_text == "CH123456789"
        assert result.title == "Test Podcast Channel"
        
    def test_channel_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            ChannelSchema().load(self.invalid_channel_data())
            
    class TestStatsTrackEventChannelSchema:
        @pytest.fixture
        def valid_stats_data(self):
            return {
                "account_guid": str(uuid4()),
                "channel_id": 1,
                "created_at": "2023-10-01T12:00:00Z"
            }
            
        def invalid_stats_data(self):
            return {
                "account_guid": str(uuid4()),
                "channel_id": None,  # Invalid: channel_id cannot be None
                "created_at": "2023-10-01T12:00:00Z"
            }

        def test_stats_track_event_channel_schema_valid_data(self, valid_stats_data):
            result = StatsTrackEventChannelSchema().load(valid_stats_data)
            assert isinstance(result, StatsTrackEventChannel)
            assert result.channel_id == 1
            
        def test_stats_track_event_channel_schema_invalid_data(self):
            with pytest.raises(ValidationError):
                StatsTrackEventChannelSchema().load(self.invalid_stats_data())
        
        