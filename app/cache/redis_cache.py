# app/cache/redis_cache.py
import redis
import json
from app.config import settings

def get_cache():
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def set_cache(key: str, value: dict, ttl: int = 3600):
    """Store a dict in Redis with expiration."""
    cache = get_cache()
    cache.setex(key, ttl, json.dumps(value))

def get_cache_value(key: str):
    """Retrieve a dict from Redis."""
    cache = get_cache()
    data = cache.get(key)
    if data:
        return json.loads(data)
    return None