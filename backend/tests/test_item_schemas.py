import pytest
from app.extensions import ValidationError
from app.blueprints.item.schemas import ItemSchema, ItemFlagStatusSchema, StatsTrackEventItemSchema
from app.blueprints.stats.schemas import StatsItemSchema
from app.models.item import Item, ItemFlagStatus, StatsAggregatedItem, StatsTrackEventItem
from uuid import uuid4

class TestItemSchema:
    @pytest.fixture
    def valid_item_data(self):
        return {
            "id_text": "IT123456789",
            "channel_id": 1,
            "item_flag_status_id": 1,
            "title": "Test Item",
            "slug": "test-item",
            "guid": str(uuid4()),
            "guid_enclosure_url": "https://example.com/enclosure.mp3",
            "pub_date": "2023-10-01T12:00:00Z"
        }

    def invalid_item_data(self):
        return {
            "id_text": "IT123456789",
            "title": ""  # Invalid: title cannot be empty
        }

    def test_item_schema_valid_data(self, valid_item_data):
        result = ItemSchema().load(valid_item_data)
        assert isinstance(result, Item)
        assert result.id_text == "IT123456789"
        assert result.title == "Test Item"

    def test_item_schema_invalid_data(self):
        with pytest.raises(ValidationError):
            ItemSchema().load(self.invalid_item_data())
            
    class TestItemFlagStatusSchema:
        @pytest.fixture
        def valid_flag_status_data(self):
            return {
                "status": "active",
                "created_at": "2023-10-01T12:00:00Z"
            }

        def invalid_flag_status_data(self):
            return {
                "id": None,  # Invalid: item_id cannot be None
            }

        def test_item_flag_status_schema_valid_data(self, valid_flag_status_data):
            result = ItemFlagStatusSchema().load(valid_flag_status_data)
            assert isinstance(result, ItemFlagStatus)
            assert result.status == "active"

        def test_item_flag_status_schema_invalid_data(self):
            with pytest.raises(ValidationError):
                ItemFlagStatusSchema().load(self.invalid_flag_status_data())
                
    class TestStatsItemSchema:
        @pytest.fixture
        def valid_stats_data(self):
            return {
                "item_id": 1,
                "day_current_count": 10,
                "day_1_count": 5,
                "day_2_count": 3,
                "day_3_count": 2,
                "day_4_count": 1,
                "day_5_count": 0,
                "day_6_count": 0,
                "day_7_count": 0,
                "day_8_count": 0,
                "week_current_count": 20,
                "week_1_count": 15,
                "week_2_count": 10,
                "week_3_count": 5,
                "week_4_count": 0,
                "month_current_count": 50,
                "month_1_count": 40,
                "all_time_count": 100
            }
            
        def invalid_stats_data(self):
            return {
                "item_id": None
            }
            
        def test_stats_aggregated_item_schema_valid_data(self, valid_stats_data):
            result = StatsItemSchema().load(valid_stats_data)
            assert isinstance(result, StatsAggregatedItem)
            assert result.item_id == 1
            
        def test_stats_aggregated_item_schema_invalid_data(self):
            with pytest.raises(ValidationError):
                StatsItemSchema().load(self.invalid_stats_data())
                
    class TestStatsTrackEventItemSchema:
        @pytest.fixture
        def valid_event_data(self):
            return {
                "account_guid": str(uuid4()),
                "item_id": 1,
                "created_at": "2023-10-01T12:00:00Z"
            }

        def invalid_event_data(self):
            return {
                "account_guid": None,  # Invalid: account_guid cannot be None
                "item_id": None
            }

        def test_stats_track_event_item_schema_valid_data(self, valid_event_data):
            result = StatsTrackEventItemSchema().load(valid_event_data)
            assert isinstance(result, StatsTrackEventItem)
            assert result.item_id == 1

        def test_stats_track_event_item_schema_invalid_data(self):
            with pytest.raises(ValidationError):
                StatsTrackEventItemSchema().load(self.invalid_event_data())