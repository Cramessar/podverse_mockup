from app.extensions import ma
from app.models.podcast import Podcast

class PodcastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Podcast
        load_instance = True
        
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)