import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple
from backend.app.utils.request_logger import get_logger

logger = get_logger(__name__)

class FSError(Exception):
    """Custom exception for filesystem operations"""
    pass

def check_directory_permissions(directory: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a directory exists and has proper read/write permissions
    
    Args:
        directory: Path to the directory to check
        
    Returns:
        Tuple[bool, Optional[str]]: (is_writable, error_message)
    """
    try:
        path = Path(directory)
        
        # Create directory if it doesn't exist
        if not path.exists():
            path.mkdir(parents=True, mode=0o755)
            return True, None
            
        # Check if it's a directory
        if not path.is_dir():
            return False, f"{directory} exists but is not a directory"
            
        # Check read permission
        if not os.access(directory, os.R_OK):
            return False, f"No read permission for {directory}"
            
        # Check write permission
        if not os.access(directory, os.W_OK):
            return False, f"No write permission for {directory}"
            
        # Try to create a test file
        test_file = path / ".permissions_test"
        try:
            test_file.touch()
            test_file.unlink()
        except Exception as e:
            return False, f"Failed to write test file in {directory}: {str(e)}"
            
        return True, None
        
    except Exception as e:
        return False, f"Error checking directory {directory}: {str(e)}"
    
    

def get_export_directory(primary_dir: str = None) -> Tuple[str, bool]:
    """
    Get a writable export directory, falling back to temp directory if needed
    
    Args:
        primary_dir: Primary directory to try first
        
    Returns:
        Tuple[str, bool]: (directory_path, is_fallback)
        
    Raises:
        FSError: If no writable directory can be found
    """
    if primary_dir:
        is_writable, error = check_directory_permissions(primary_dir)
        if is_writable:
            logger.info(f"Using primary export directory: {primary_dir}")
            return primary_dir, False
        logger.warning(f"Primary export directory not usable: {error}")
    
    # Try app-specific temp directory
    temp_dir = os.path.join(tempfile.gettempdir(), 'podverse_exports')
    is_writable, error = check_directory_permissions(temp_dir)
    
    if is_writable:
        logger.info(f"Using fallback export directory: {temp_dir}")
        return temp_dir, True
        
    raise FSError(f"No writable export directory available. Errors: Primary: {error}")



def safe_write_file(filepath: str, write_func) -> Tuple[bool, Optional[str]]:
    """
    Safely write a file using a write function
    
    Args:
        filepath: Path to the file to write
        write_func: Function that takes a file object and writes to it
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    temp_file = None
    try:
        # Create temporary file in the same directory
        directory = os.path.dirname(filepath)
        with tempfile.NamedTemporaryFile(mode='w', 
                                       dir=directory,
                                       prefix='._tmp_',
                                       delete=False) as temp_file:
            # Write to temporary file
            write_func(temp_file)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            
        # Atomic rename
        shutil.move(temp_file.name, filepath)
        return True, None
        
    except Exception as e:
        error_msg = f"Error writing file {filepath}: {str(e)}"
        logger.error(error_msg)
        
        # Clean up temp file if it exists
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception as cleanup_error:
                logger.error(f"Error cleaning up temp file: {str(cleanup_error)}")
                
        return False, error_msg 