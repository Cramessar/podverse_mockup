from app.models.channel import Channel
from app.extensions import db
from typing import List, Optional

class ChannelService:
    """Service layer for Channel operations - minimal factory pattern implementation"""
    
    @staticmethod
    def get_all_channels() -> List[Channel]:
        return Channel.query.all()
    
    @staticmethod
    def get_channel_by_id(channel_id: int) -> Optional[Channel]:
        return Channel.query.get(channel_id)
    
    @staticmethod
    def create_channel(data: dict) -> Channel:
        new_channel = Channel(**data)
        
        if new_channel == {}:
            raise ValueError("No data provided for channel creation")
        
        # Should we validate other fields here?
        
        db.session.add(new_channel)
        db.session.commit()
        return new_channel
    
    @staticmethod
    def update_channel(channel_id: int, data: dict) -> Channel:
        channel = Channel.query.get(channel_id)
        if not channel:
            raise ValueError("Channel not found")
        
        for key, value in data.items():
            setattr(channel, key, value)
        
        db.session.commit()
        return channel
    
    @staticmethod
    def delete_channel(channel_id: int) -> None:
        channel = Channel.query.get(channel_id)
        if not channel:
            raise ValueError("Channel not found")

        db.session.delete(channel)
        db.session.commit()
    

# Factory function for service creation
def create_channel_service() -> ChannelService:
    """Factory function to create channel service instance"""
    return ChannelService()
