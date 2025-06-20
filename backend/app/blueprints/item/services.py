from app.models.item import Item
from app.extensions import db
from typing import List, Optional
from sqlalchemy import select

class ItemService:
    """Service layer for Item operations - minimal factory pattern implementation"""

    @staticmethod
    def get_all_items() -> List[Item]:
        return db.session.execute(select(Item)).scalars().all()

    @staticmethod
    def get_item_by_id(item_id: int) -> Optional[Item]:
        return db.session.get(Item, item_id)

    @staticmethod
    def get_items_by_channel_id(channel_id: int) -> List[Item]:
        return db.session.execute(select(Item).where(Item.channel_id == channel_id)).scalars().all()
    
    @staticmethod
    def create_item(data: dict) -> Item:
        item = Item(**data)
        db.session.add(item)
        db.session.commit()
        return item
    
    @staticmethod
    def update_item(item_id: int, data: dict) -> Optional[Item]:
        item = db.session.get(Item, item_id)
        if not item:
            return None
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return item
    
    @staticmethod
    def delete_item(item_id: int) -> bool:
        item = db.session.get(Item, item_id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True
    
def create_item_service() -> ItemService:
    """Factory function to create item service instance"""
    return ItemService()