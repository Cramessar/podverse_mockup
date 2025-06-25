from app.extensions import ma
from app.models.channel import StatsAggregatedChannel
from app.models.channel import Channel
from app.models.item import StatsAggregatedItem

class StatsChannelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsAggregatedChannel
        load_instance = True
        include_relationships = False
        include_fk = True

class StatsItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsAggregatedItem
        load_instance = True
        include_relationships = False
        include_fk = True

class ChannelDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Channel
        include_relationships = True
        include_fk = True
        include_fields = ('id', 'title', 'slug', 'description', 'stats', 'raw_event_count')
        
stats_channel_schema = StatsChannelSchema()
stats_item_schema = StatsItemSchema()
channel_details_schema = ChannelDetailsSchema()