# app/utils/query_params.py
#Request-parsing utils - Parse request.args safely

from flask import request
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Query
from sqlalchemy import desc

from app.utils.error_exceptions import ValidationError
from app.utils.request_logger import get_logger


logger = get_logger(__name__)


def get_pagination_params(request, default_page=1, default_limit=10, max_limit=50):
    """
        Extract and validate pagination parameters from request arguments
        
        Args:
            request: Flask request object, which includes the query parameters (what's after ? in a URL)
            default_page (int): Default page if none is provided
            default_limit (int): Default number of items per page
            max_limit (int): Maximum allowed limit to prevent abuse
        
        Returns:
            tuple: (page, limit)
    """
    
    # Get 'page' from the query string (?page=2), default to 1 if missing
    page = request.args.get('page', default_page, type=int) 
    limit = request.args.get('limit', default_limit, type=int) 
    
    # Ensure page is always at least 1
    page = max(1, page)

    # writing this way so if limit exceed we can raise error with logging prevent abuse (not limit = min(limit, max_limit))
    if limit > max_limit:
        logger.warning(f"Client requested too many items: {limit}, capped to {max_limit}")
        limit = max_limit
    return page, limit

def get_sorting_params(request, allowed_fields, default_field='id', default_order='asc'):
    """
        Extract and validate sorting parameters from request arguments.
        
        Args:
            request: Flask request object
            allowed_fields (list): List of model field names allowed to be used for sorting
            default_field (str): Default field to sort by if input is invalid or missing
            default_order (str): Default sort order ('asc' or 'desc')
        
        Returns:
            tuple: (sort_by, sort_order)
    """
    
    sort_by = request.args.get('sort_by', default_field, type=str) # Try to get 'sort_by' from query params (e.g. ?sort_by=title), or use default
    sort_order = request.args.get('sort_order', default_order, type=str)
    
    #validate input - # If user passes an invalid field name (e.g. ?sort_by=hack), fallback to default
    if sort_by not in allowed_fields:
        sort_by = default_field
    if sort_order not in ['asc', 'desc']:
        sort_order = default_order
    
    # Return cleaned values to be used by query logic (e.g. in order_by)
    return sort_by, sort_order
    
    
def get_filter_param(request, key, default=None, type_func=str):
    """
        Extract and validate single filter parameter from request arguments
        
        Args:
            request: Flask request object
            key (str): Query parameter name (e.g. 'status')
            default: Default value if param is not provided
            type_func: Type to cast the value into (e.g. str, int, bool)
            
        Returns:
            tuple: (filter_value, filter_type)
    """

    # Param-specific filters like: ?status=active → key='status', returns 'active' as str
    # or ?medium_id=3 → key='medium_id', type_func=int → returns 3
    return request.args.get(key, default, type=type_func)

def get_multi_filter_param(request, key, default=None, type_func=str): # mesela ?tags=1,2,3
    """
        Extract and validate a comma-separated multi-value filter parameter.

        Args:
            request: Flask request object
            key (str): The query parameter to extract (e.g. 'tags')
            default: Default (empty list) list if param is missing or invalid
            type_func: a function to convert each value. Defaults to str, but you can pass int or float if needed.

        Returns:
            list: List of typed values (e.g. [1, 2, 3])
    """
    
    #Get the raw query string value for the key, e.g. ?tags=1,2,3
    raw_value = request.args.get(key)
    # If the param is missing, return default or empty list
    if raw_value is None:
        return default if default is not None else []
    
    try:
        # Split the raw value by commas and convert each to the specified type - type_func(cleaned_value)
        return [type_func(val.strip()) for val in raw_value.split(',') if val.strip()]
    except (ValueError, TypeError):
        logger.warning(f"Invalid multi-filter param for key: {key}")
        return default if default is not None else []
    
def get_search_query(request, default_search='', type_func=str, max_length=100):
    """
    Extract and validate search parameter from request arguments.
        
    Parameters:
        request: The incoming HTTP request object.
        default_search (str, optional): The fallback value if 'search' param is not provided. Defaults to ''.
        type_func (callable, optional): A function to cast the value. Defaults to str.
        max_length (int, optional): Maximum allowed length for search term. Defaults to 100.
        
    Returns:
        str: The cleaned and type-converted search term to apply in filtering logic.
        
    Raises:
        ValidationError: If search term exceeds max length or contains invalid characters
    """

    # Get the search term from the query string (?search=term)
    search = request.args.get('search', default_search, type=type_func)
    
    # Validate length
    if len(search) > max_length:
        raise ValidationError(f"Search query exceeds maximum length of {max_length} characters")
    
    # Escape special SQL LIKE characters to prevent SQL injection via LIKE
    search = search.replace('%', r'\%').replace('_', r'\_')
    
    return search
