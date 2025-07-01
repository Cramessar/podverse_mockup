# backend/app/blueprints/feed/schemas.py

from app.extensions import ma
from app.models.feed import Feed, FeedFlagStatus, FeedLog

class FeedLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FeedLog
        load_instance = True
        include_relationships = False
        include_fk = True

# Export single and many versions
feed_log_schema = FeedLogSchema()
feed_logs_schema = FeedLogSchema(many=True)

class FeedSchema(ma.SQLAlchemyAutoSchema):
    recent_logs = ma.Method("get_recent_logs")

    class Meta:
        model = Feed
        load_instance = True
        include_relationships = False
        include_fk = True

    def get_recent_logs(self, obj):
        return FeedLogSchema(many=True).dump(obj.recent_logs or [])

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
