from typing import List, Optional
from ..models.category import Category


class CategoryService:
    """Service layer for category operations"""
    
    @staticmethod
    def get_all_categories() -> List[Category]:
        """
        Retrieve all categories with parent-child relationships
        """
        # TODO: Implement database query
        # Primary table: category
        # Return hierarchical structure of categories - cocuk parent ilişkisi olacak
        pass
    
    @staticmethod
    def get_category_by_id(category_id: int) -> Optional[Category]:
        """
        Retrieve category by ID
        """
        # TODO: Implement database query - burada 
        pass 