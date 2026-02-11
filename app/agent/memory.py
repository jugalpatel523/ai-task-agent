import json
import redis
from app.config import settings

class MemoryStore:
    """
    Short-term memory per user stored in Redis.
    """
    def __init__(self):
        self.r = redis.from_url(settings.redis_url, decode_responses=True)

    def key(self, user_id: str) -> str:
        return f"mem:{user_id}"

    def append(self, user_id: str, item: dict, max_items: int = 20):
        k = self.key(user_id)
        self.r.rpush(k, json.dumps(item))
        self.r.ltrim(k, -max_items, -1)

    def get_all(self, user_id: str) -> list[dict]:
        k = self.key(user_id)
        raw = self.r.lrange(k, 0, -1)
        return [json.loads(x) for x in raw]
