from typing import List, Optional
from app.models.medium import Medium


class MediumService:
    """Service layer for medium operations"""
    
    @staticmethod
    def get_all_mediums() -> List[Medium]:
        """
        Retrieve all medium types (podcast, video, blog, etc.)
        """
        # TODO: Implement database query
        # Primary table: medium
        pass
    
    @staticmethod
    def get_medium_by_id(medium_id: int) -> Optional[Medium]:
        """
        Retrieve medium by ID
        """
        # TODO: Implement database query
        pass 