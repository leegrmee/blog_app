import redis
import logging
from config.settings import settings

try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        encoding="UTF-8",
        decode_responses=True,
    )
    # Redis 연결 테스트
    redis_client.ping()
    logging.info("Redis connection established")

except redis.ConnectionError as e:
    logging.error(f"Redis connection error: {e}")

    # 메모리 기반 /    Fallback 대체 구현 (선택 사항)
    class FallbackCache:
        def __init__(self):
            self.cache = {}

        def setex(self, key, ttl, value):
            self.cache[key] = value
            # 실제 TTL은 구현하지 않음, 메모리에만 저장

        def get(self, key):
            return self.cache.get(key)

        def exists(self, key):
            return key in self.cache

    redis_client = FallbackCache()
    logging.warning("Using in-memory fallback cache instead of Redis")
