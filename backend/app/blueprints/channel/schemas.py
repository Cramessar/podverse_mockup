from app.extensions import ma
from app.models.channel import Channel

class ChannelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Channel
        load_instance = True
        include_relationships = False  
channel_schema = ChannelSchema()
channels_schema = ChannelSchema(many=True)






# from app.extensions import ma
# from app.models.account import Account, SharableStatus, StatsTrackAccountGuid
# from app.models.category import Category
# from app.models.channel import Channel, StatsAggreatedChannel, StatsTrackEventChannel, ChannelCategory
# from app.models.feed import Feed, FeedFlagStatus, FeedLog
# from app.models.item import Item, ItemFlagStatus, StatsAggregatedItem, StatsTrackEventItem
# from app.models.medium import Medium

# # Channel Related Schemas
# class StatsAggregatedChannelSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = StatsAggreatedChannel
#         load_instance = True

# class StatsTrackEventChannelSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = StatsTrackEventChannel
#         load_instance = True
    
#     created_at = ma.DateTime(format='%Y-%m-%d %H:%M:%S')

# class ChannelCategorySchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = ChannelCategory
#         load_instance = True
    
#     # Exclude channels since we're already in the channel model
#     category = ma.Nested(CategorySchema, exclude=('channels',))

# class ChannelSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Channel
#         load_instance = True
#         include_relationships = True
    
#     feed = ma.Nested(FeedSchema, exclude=('channels',))
#     medium = ma.Nested(MediumSchema)
#     categories = ma.Nested(ChannelCategorySchema, many=True)
#     items = ma.Nested(ItemListSchema, many=True)
#     stats = ma.Nested(StatsAggregatedChannelSchema)
#     events = ma.Nested(StatsTrackEventChannelSchema, many=True)
#     category_names = ma.Method('get_category_names')
    
#     def get_category_names(self, obj):
#         return [cat.category.display_name for cat in obj.categories]
        
# channel_schema = ChannelSchema()
# channels_schema = ChannelSchema(many=True)