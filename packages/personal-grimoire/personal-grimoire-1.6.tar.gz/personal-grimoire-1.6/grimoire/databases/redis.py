import redis


def get_redis():
    return redis.Redis(host="localhost", port=6378, db=0, decode_responses=True)
