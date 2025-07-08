import pytest
from app.extensions import ValidationError
from app.blueprints.channel.schemas import StatsTrackEventChannelSchema, StatsTrackEventChannel
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