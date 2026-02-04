from redis import Redis

from scraper_bot_discord.abstract.storage import Storage


class RedisStorage(Storage):
    def __init__(self, redis: Redis):
        self.redis = redis

    def add(self, user_id: str, value: dict):
        self.redis.hset(name=user_id, mapping=value)

    def remove(self, key: str):
        self.redis.delete(key)

    def unschedule(self, value: str):
        self.redis.zrem('stalker:queue', value)

    def get_all(self, key: str):
        return self.redis.hgetall(key)

    def schedule(self, key: str, timer: str):
        self.redis.zadd('stalker:queue', {key: timer})

    def get_observable_user(self, key: str):
        return self.redis.keys(key)

    def get_due(self, time):
        return self.redis.zrangebyscore('stalker:queue', 0, time)
