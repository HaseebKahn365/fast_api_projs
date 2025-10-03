import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_cache(key: str):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value, ttl: int = 300):
    r.setex(key, ttl, json.dumps(value))