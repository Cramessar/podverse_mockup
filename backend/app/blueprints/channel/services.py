from app.models.channel import Channel
from app.extensions import db
from typing import List, Optional

class ChannelService:
    """Service layer for Channel operations - minimal factory pattern implementation"""
    
    @staticmethod
    def get_all_channels() -> List[Channel]:
        return Channel.query.all()
    

# Factory function for service creation
def create_channel_service() -> ChannelService:
    """Factory function to create channel service instance"""
    return ChannelService()
