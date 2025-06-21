import pytest
from marshmallow import ValidationError
from app.models.channel import Channel
from app.blueprints.channel.schemas import ChannelSchema
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
        
        