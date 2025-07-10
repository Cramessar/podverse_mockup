# app/utils/redis_lock.py

import redis
import time
import os
from contextlib import contextmanager
from backend.app.utils.request_logger import get_logger
from typing import Optional, Tuple, Generator
from redis import Redis
from app.utils.error_exceptions import RedisLockError

logger = get_logger(__name__)

def get_redis_client() -> Optional[Redis]:
    """
    Get Redis client instance from environment configuration
    
    Returns:
        Optional[Redis]: Redis client instance or None if connection fails
    """
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    try:
        return redis.from_url(redis_url)
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        return None

@contextmanager
def redis_lock(lock_name: str, 
              timeout: int = 300, 
              poll_interval: float = 0.1, 
              max_retries: int = 3) -> Generator[Tuple[bool, Optional[str]], None, None]:
    """
    Context manager for Redis distributed lock with improved error handling
    
    Args:
        lock_name: Name of the lock (e.g., 'auto_reparse_all')
        timeout: Lock timeout in seconds (default: 5 minutes)
        poll_interval: How often to check for lock availability in seconds
        max_retries: Maximum number of retries for lock acquisition
        
    Yields:
        Tuple[bool, Optional[str]]: (success, error_message)
    
    Raises:
        RedisLockError: If there are critical Redis errors
    """
    redis_client: Optional[Redis] = get_redis_client()
    if not redis_client:
        logger.warning("Redis client not available, proceeding without lock")
        yield True, None
        return
    
    lock_key: str = f"lock:{lock_name}"
    identifier: str = f"{os.getpid()}:{time.time()}"
    acquired: bool = False
    error_msg: Optional[str] = None
    
    for attempt in range(max_retries):
        try:
            # Try to acquire the lock
            acquired = bool(redis_client.set(lock_key, identifier, nx=True, ex=timeout))
            
            if acquired:
                logger.info(f"Acquired Redis lock: {lock_name}")
                break
            elif attempt < max_retries - 1:
                wait_time: float = poll_interval * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Lock acquisition attempt {attempt + 1} failed, waiting {wait_time}s")
                time.sleep(wait_time)
            else:
                error_msg = f"Failed to acquire lock after {max_retries} attempts"
                logger.warning(error_msg)
                
        except redis.RedisError as e:
            error_msg = f"Redis error during lock acquisition: {str(e)}"
            logger.error(error_msg)
            if attempt == max_retries - 1:
                raise RedisLockError(error_msg)
    
    try:
        yield acquired, error_msg
    except Exception as e:
        logger.error(f"Error in lock context for {lock_name}: {str(e)}")
        error_msg = str(e)
        raise
    finally:
        # Release the lock if we acquired it
        if acquired:
            try:
                # Use Lua script to safely release only our lock
                lua_script: str = """
                if redis.call("get", KEYS[1]) == ARGV[1] then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
                """
                redis_client.eval(lua_script, 1, lock_key, identifier)
                logger.info(f"Released Redis lock: {lock_name}")
            except Exception as e:
                logger.error(f"Error releasing Redis lock {lock_name}: {str(e)}")

def is_locked(lock_name: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a Redis lock is currently held
    
    Args:
        lock_name: Name of the lock to check
        
    Returns:
        Tuple[bool, Optional[str]]: (is_locked, error_message)
    """
    redis_client: Optional[Redis] = get_redis_client()
    if not redis_client:
        return False, "Redis client not available"
    
    lock_key: str = f"lock:{lock_name}"
    try:
        return bool(redis_client.exists(lock_key) > 0), None
    except Exception as e:
        error_msg: str = f"Error checking Redis lock {lock_name}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg 