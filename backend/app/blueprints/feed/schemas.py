from app.extensions import ma
from app.models.feed import Feed

class FeedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feed
        load_instance = True
        
feed_schema = FeedSchema()
feeds_schema = FeedSchema(many=True)