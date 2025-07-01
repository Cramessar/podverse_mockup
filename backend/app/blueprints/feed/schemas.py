#app/blueprints/feed/schemas.py

from app.extensions import ma
from app.models.feed import Feed, FeedFlagStatus, FeedLog
from marshmallow import fields

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
        
feed_log_schema = FeedLogSchema()
feed_logs_schema = FeedLogSchema(many=True)



class FeedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feed
        load_instance = True
        include_relationships = False  
        include_fk = True
    
    # Explicitly include only the relationships we want
    flag_status = fields.Nested(FeedFlagStatusSchema, dump_only=True)
    logs = fields.Nested(FeedLogSchema, many=True, dump_only=True)
        
feed_schema = FeedSchema()
feeds_schema = FeedSchema(many=True)