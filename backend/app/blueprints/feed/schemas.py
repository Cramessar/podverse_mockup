# backend/app/blueprints/feed/schemas.py

from app.extensions import ma
from app.models.feed import Feed, FeedFlagStatus, FeedLog
from datetime import datetime

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

    def get_recent_logs(self, feed_obj):
        """
        Get the two most recent feed logs for the given feed, sorted by last_finished_parse_time (descending).
        Args:
            feed_obj (Feed): Feed instance with related logs
        Returns:
            List[dict]: Serialized recent feed logs (max 2 entries)
        """
        sorted_logs = sorted(
            feed_obj.logs or [],
            key=lambda log: log.last_finished_parse_time or datetime.min,
            reverse=True
        )
        return FeedLogSchema(many=True).dump(sorted_logs[:2])

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

# Without this schema i woulf get nested schmas in export. this flattens data with simple fileds 
class FeedExportSchema(ma.SQLAlchemyAutoSchema):
    flag_status = ma.Method("get_flag_status")
    channel_title = ma.Method("get_channel_title")
    
    class Meta:
        model = Feed
        load_instance = False
        include_fk = True
        fields = ('id', 'url', 'parsing_priority', 'is_parsing', 'created_at', 'updated_at', 'flag_status', 'channel_title')
    
    def get_flag_status(self, feed_obj):
        return feed_obj.flag_status.status if feed_obj.flag_status else None
    
    def get_channel_title(self, feed_obj):
        return feed_obj.channels[0].title if feed_obj.channels else None

feed_export_schema = FeedExportSchema()
feeds_export_schema = FeedExportSchema(many=True)

