import pytest
from app.extensions import ValidationError
from app.blueprints.channel.schemas import ChannelSchema, StatsTrackEventChannelSchema, ChannelCategorySchema
from app.blueprints.stats.schemas import StatsChannelSchema
from app.models.channel import Channel, StatsTrackEventChannel, StatsAggregatedChannel, ChannelCategory
from uuid import uuid4
    
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
            "title": ""  # Invalid: title cannot be empty
        }
    
    def test_channel_schema_valid_data(self, valid_channel_data):
        result = ChannelSchema().load(valid_channel_data)
        assert isinstance(result, Channel)
        assert result.id_text == "CH123456789"
        assert result.title == "Test Podcast Channel"
        
    def test_channel_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            ChannelSchema().load(self.invalid_channel_data())
            
class TestStatsChannelSchema:
    @pytest.fixture
    def valid_aggregated_data(self):
        return {
            "channel_id": 1,
            "day_current_count": 100,
            "day_1_count": 90,
            "day_2_count": 80,
            "day_3_count": 70,
            "day_4_count": 60,
            "day_5_count": 50,
            "day_6_count": 40,
            "day_7_count": 30,
            "day_8_count": 20,
            "week_current_count": 300,
            "week_1_count": 280,
            "week_2_count": 260,
            "week_3_count": 240,
            "week_4_count": 220,
            "month_current_count": 1000,
            "month_1_count": 900,
            "all_time_count": 5000
        }

    def invalid_aggregated_data(self):
        return {
            "channel_id": None
        }

    def test_stats_channel_schema_valid_data(self, valid_aggregated_data):
        result = StatsChannelSchema().load(valid_aggregated_data)
        assert isinstance(result, StatsAggregatedChannel)
        assert result.channel_id == 1

    def test_stats_channel_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            StatsChannelSchema().load(self.invalid_aggregated_data())
            
class TestChannelCategorySchema:
    @pytest.fixture
    def valid_category_data(self):
        return {
            "channel_id": 1,
            "category_id": 2
        }

    def invalid_category_data(self):
        return {
            "channel_id": None,  # Invalid: channel_id cannot be None
            "category_id": 2
        }

    def test_channel_category_schema_valid_data(self, valid_category_data):
        result = ChannelCategorySchema().load(valid_category_data)
        assert isinstance(result, ChannelCategory)
        assert result.channel_id == 1

    def test_channel_category_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            ChannelCategorySchema().load(self.invalid_category_data())
        
        