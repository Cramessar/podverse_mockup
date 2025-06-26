from app.extensions import ma, fields, validate
from app.models.channel import Channel, StatsTrackEventChannel, ChannelCategory, StatsAggregatedChannel

class ChannelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Channel
        load_instance = True
        include_relationships = False
        include_fk = True
        
    title = fields.Str(
    required=True, 
    validate=validate.Length(min=1, max=255)
    )
        
channel_schema = ChannelSchema()
channels_schema = ChannelSchema(many=True)

class StatsTrackEventChannelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsTrackEventChannel
        load_instance = True
        include_fk = True
        
stats_track_event_channel_schema = StatsTrackEventChannelSchema()
stats_track_event_channels_schema = StatsTrackEventChannelSchema(many=True)
        
class ChannelCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChannelCategory
        load_instance = True
        include_fk = True

channel_category_schema = ChannelCategorySchema()
channel_categories_schema = ChannelCategorySchema(many=True)