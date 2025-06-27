# app/blueprints/channel/schemas.py

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
    
    # Include nested objects for list endpoint
    categories = fields.Method("get_categories")
    medium = fields.Method("get_medium")
    
    def get_categories(self, obj):
        """Extract category data from the channel_category relationship"""
        return [{'id': cc.category.id, 'parent_id': cc.category.parent_id, 
                'display_name': cc.category.display_name, 'slug': cc.category.slug,
                'mapping_key': cc.category.mapping_key} 
               for cc in obj.categories if cc.category] if obj.categories else []
    
    def get_medium(self, obj):
        """Extract medium data from the medium relationship"""
        return {'id': obj.medium.id, 'value': obj.medium.value} if obj.medium else None

# Detailed schema for individual channel endpoint with nested relationships
class ChannelDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Channel
        load_instance = False
        include_fk = True
        include_relationships = False
        
    # Include nested objects
    categories = fields.Method("get_categories")
    medium = fields.Method("get_medium")
    
    def get_categories(self, obj):
        """Extract category data from the channel_category relationship"""
        return [{'id': cc.category.id, 'parent_id': cc.category.parent_id, 
                'display_name': cc.category.display_name, 'slug': cc.category.slug,
                'mapping_key': cc.category.mapping_key} 
               for cc in obj.categories if cc.category] if obj.categories else []
    
    def get_medium(self, obj):
        """Extract medium data from the medium relationship"""
        return {'id': obj.medium.id, 'value': obj.medium.value} if obj.medium else None
        
channel_schema = ChannelSchema()
channels_schema = ChannelSchema(many=True)
channel_detail_schema = ChannelDetailSchema()

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

class ChannelExportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
           model = Channel
           load_instance = False
           include_fk = True
           include_relationships = False  # prevents full nested dumping

    medium_name = fields.Function(lambda obj: obj.medium.value if obj.medium else None)
    feed_url = fields.Function(lambda obj: obj.feed.url if obj.feed else None)
    feed_status = fields.Function(lambda obj: obj.feed.flag_status.status if obj.feed and obj.feed.flag_status else None)
    stats_all_time_count = fields.Function(lambda obj: obj.stats[0].all_time_count if obj.stats else 0)
    stats_month_current_count = fields.Function(lambda obj: obj.stats[0].month_current_count if obj.stats else 0)
    stats_week_current_count = fields.Function(lambda obj: obj.stats[0].week_current_count if obj.stats else 0)
    stats_day_current_count = fields.Function(lambda obj: obj.stats[0].day_current_count if obj.stats else 0)

channel_exports_schema = ChannelExportSchema(many=True)