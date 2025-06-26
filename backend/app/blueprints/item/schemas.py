from app.extensions import ma
from app.models.item import Item, ItemFlagStatus, StatsAggregatedItem, StatsTrackEventItem

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        include_relationships = False
        include_fk = True
    
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

class ItemFlagStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemFlagStatus
        load_instance = True
        include_relationships = False
        include_fk = True
        
item_flag_status_schema = ItemFlagStatusSchema()
item_flag_statuses_schema = ItemFlagStatusSchema(many=True)

class StatsTrackEventItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsTrackEventItem
        load_instance = True
        include_relationships = False
        include_fk = True
        
stats_track_event_item_schema = StatsTrackEventItemSchema()
stats_track_event_items_schema = StatsTrackEventItemSchema(many=True)

