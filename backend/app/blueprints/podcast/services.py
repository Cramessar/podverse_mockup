from app.models.podcast import Podcast
from app.extensions import db
from typing import List, Optional

class PodcastService:
    """Service layer for Podcast operations - minimal factory pattern implementation"""
    
    @staticmethod
    def get_all_podcasts() -> List[Podcast]:
        return Podcast.query.all()
    

# Factory function for service creation
def create_podcast_service() -> PodcastService:
    """Factory function to create podcast service instance"""
    return PodcastService()
