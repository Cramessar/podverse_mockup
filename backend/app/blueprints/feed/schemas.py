from app.extensions import ma
from app.models.feed import Feed, FeedFlagStatus, FeedLog

class FeedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feed
        load_instance = True
        include_relationships = False
        include_fk = True
        
feed_schema = FeedSchema()
feeds_schema = FeedSchema(many=True)

class FeedFlagStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FeedFlagStatus
        load_instance = True
        include_relationships = False
        include_fk = True
        
feed_flag_status_schema = FeedFlagStatusSchema()
feed_flag_statuses_schema = FeedFlagStatusSchema(many=True)

class FeedLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FeedLog
        load_instance = True
        include_relationships = False
        include_fk = True