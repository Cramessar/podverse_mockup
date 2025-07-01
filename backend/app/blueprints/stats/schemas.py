# backend/app/blueprints/stats/schemas.py

from app.extensions import ma, fields, validate
from app.models.channel import Channel
from app.models.item import Item
from app.models.stats import StatsAggregatedChannel, StatsAggregatedItem

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

class ChannelDailyStatsOnlySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsAggregatedChannel
        load_instance = True
        include_relationships = False
        include_fk = True
        fields = ('id', 'channel_id', 'day_current_count', 'day_1_count', 'day_2_count', 'day_3_count',
                  'day_4_count', 'day_5_count', 'day_6_count', 'day_7_count', 'day_8_count')
        
class ChannelWeeklyStatsOnlySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsAggregatedChannel
        load_instance = True
        include_relationships = False
        include_fk = True
        fields = ('id', 'channel_id', 'week_current_count', 'week_1_count', 'week_2_count', 'week_3_count',
                  'week_4_count')
        
class ChannelStatsFilterSchema(ma.Schema):
    # Channel filtering
    channel_id = fields.Int()
    channel_ids = fields.List(fields.Int())
    
    # Count range filtering
    min_daily_total = fields.Int()
    max_daily_total = fields.Int()
    min_weekly_total = fields.Int()
    max_weekly_total = fields.Int()
    min_all_time = fields.Int()
    max_all_time = fields.Int()
    
    # Specific period filtering
    min_current_day = fields.Int()
    max_current_day = fields.Int()
    min_current_week = fields.Int()
    max_current_week = fields.Int()
    min_current_month = fields.Int()
    max_current_month = fields.Int()
    
    # Response format options
    view = fields.Str(
        missing='default',
        validate=validate.OneOf(['default', 'details', 'daily', 'weekly'])
    )
    
    # Pagination
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=10, validate=validate.Range(min=1, max=100))
    
    # Sorting
    sort_by = fields.Str(
        missing='channel_id',
        validate=validate.OneOf([
            'channel_id', 'day_current_count', 'week_current_count', 
            'month_current_count', 'all_time_count'
        ])
    )
    sort_order = fields.Str(missing='desc', validate=validate.OneOf(['asc', 'desc']))
    
        
class ItemDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_relationships = True
        include_fk = True
        include_fields = ('id', 'title', 'guid', 'pub_date', 'stats', 'raw_event_count')

class ChannelDailyStatsOnlySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsAggregatedChannel
        load_instance = True
        include_relationships = False
        include_fk = True
        fields = (
            'id', 'channel_id', 'day_current_count', 'day_1_count', 'day_2_count', 'day_3_count',
            'day_4_count', 'day_5_count', 'day_6_count', 'day_7_count', 'day_8_count'
        )

class ChannelWeeklyStatsOnlySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StatsAggregatedChannel
        load_instance = True
        include_relationships = False
        include_fk = True
        fields = (
            'id', 'channel_id', 'week_current_count', 'week_1_count', 'week_2_count', 'week_3_count',
            'week_4_count'
        )

class ChannelStatsFilterSchema(ma.Schema):
    # Channel filtering
    channel_id = fields.Int()
    channel_ids = fields.List(fields.Int())

    # Count range filtering
    min_daily_total = fields.Int()
    max_daily_total = fields.Int()
    min_weekly_total = fields.Int()
    max_weekly_total = fields.Int()
    min_all_time = fields.Int()
    max_all_time = fields.Int()

    # Specific period filtering
    min_current_day = fields.Int()
    max_current_day = fields.Int()
    min_current_week = fields.Int()
    max_current_week = fields.Int()
    min_current_month = fields.Int()
    max_current_month = fields.Int()

    # Response format options
    view = fields.Str(
        missing='default',
        validate=validate.OneOf(['default', 'details', 'daily', 'weekly'])
    )

    # Pagination
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=10, validate=validate.Range(min=1, max=100))

    # Sorting
    sort_by = fields.Str(
        missing='channel_id',
        validate=validate.OneOf([
            'channel_id', 'day_current_count', 'week_current_count', 
            'month_current_count', 'all_time_count'
        ])
    )
    sort_order = fields.Str(missing='desc', validate=validate.OneOf(['asc', 'desc']))

# Schema exports
stats_channel_schema = StatsChannelSchema()
stats_channel_schema_many = StatsChannelSchema(many=True)

stats_item_schema = StatsItemSchema()
stats_item_schema_many = StatsItemSchema(many=True)

channel_details_schema = ChannelDetailsSchema()
item_details_schema = ItemDetailsSchema()

channel_daily_stats_only_schema = ChannelDailyStatsOnlySchema()
channel_weekly_stats_only_schema = ChannelWeeklyStatsOnlySchema()
channel_stats_filter_schema = ChannelStatsFilterSchema()