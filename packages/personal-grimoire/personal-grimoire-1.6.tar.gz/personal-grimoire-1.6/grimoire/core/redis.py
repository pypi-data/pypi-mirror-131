import logging

import redis


class SimpleKeyValueDb:
    def __init__(self):
        self.redis = redis.Redis(host="localhost", port=6378, db=0)

    def load(self, key):
        result = self.redis.get(key)

        if not result:
            return None

        logging.info(f"Key {key} found in redis")

        return result.decode("utf-8")

    def save(self, key, value):
        return self.redis.set(key, value)
