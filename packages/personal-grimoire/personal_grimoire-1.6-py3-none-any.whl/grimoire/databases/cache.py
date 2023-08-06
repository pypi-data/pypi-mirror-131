from grimoire.databases.redis import get_redis


class Cache:
    _namespace = "cache"

    def __init__(self):
        self._redis = get_redis()

    def set(self, key, value):
        self._redis.hset(Cache._namespace, key, value)

    def get(self, key):
        return self._redis.hget(Cache._namespace, key)

    def unset(self, key):
        self._redis.hdel(Cache._namespace, key)
