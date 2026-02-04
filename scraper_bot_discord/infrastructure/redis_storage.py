from redis import Redis

from scraper_bot_discord.abstract.storage import Storage


class RedisStorage(Storage):
    def __init__(self, redis: Redis):
        self.redis = redis

    def add(self, user_id: str, value: dict):
        self.redis.hset(name=user_id, mapping=value)

    def remove(self, key: str):
        self.redis.delete(key)

    def get_all(self, key: str):
        return self.redis.hgetall(key)
