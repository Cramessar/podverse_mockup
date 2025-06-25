# app/utils/query_helpers.py
# Query-logic utils - # Apply logic to SQLAlchemy queries

def paginate_query(query, page, limit):
    """
        Apply offset and limit to a SQLAlchemy query and return results with metadata.

        Args:
            query: SQLAlchemy query object
            page (int): Page number (1-based)
            limit (int): Number of items per page

        Returns:
            tuple: (items, pagination_metadata)
    """
    # Total number of results before pagination (important for frontend)
    total_items = query.order_by(None).count() # order_by(None) remve order by for faster count()

    # Fetch paginated subset using offset and limit
    items = query.offset((page-1) * limit).limit(limit).all()
    
    # Calculate pagination metadata
    total_pages = (total_items +(limit -1)) //limit 
    has_next = page < total_pages
    has_prev = page > 1
    
    pagination_metadata = {
        'page': page,
        'limit': limit,
        'total_items': total_items,
        'total_pages': total_pages,
        'has_next': has_next,
        'has_prev': has_prev
    }
    
    return items, pagination_metadata

def apply_sorting(query, model, sort_by, sort_order='asc'):
    """
        Safely apply dynamic sorting to a SQLAlchemy query by validating that the given field (sort_by) exists on the model before applying the sort order (asc or desc).

        Args:
            query: SQLAlchemy query object
            model: SQLAlchemy model class
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')    

        Returns:
            SQLAlchemy query object with applied sorting
    """

    # Try to get the attribute named sort_by(liek title) from the model. If it doesn’t exist, return None instead of raising an error.
    column = getattr(model, sort_by, None)
    if column is None:
        raise ValueError(f"Invalid sort field: '{sort_by}' is not a column on model '{model.__name__}'.")
    
    
    if sort_order == 'desc':
        return query.order_by(column.desc())
    return query.order_by(column.asc())