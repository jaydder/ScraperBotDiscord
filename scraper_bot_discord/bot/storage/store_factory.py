from redis import Redis

from scraper_bot_discord.bot.storage.user_store import UserStore
from scraper_bot_discord.infrastructure.redis_storage import RedisStorage


class StoreFactory:
    def __new__(cls):
        redis_client = Redis(
            host='172.17.0.2',
            port=6379,
            db=0,
            decode_responses=True,
        )

        storage = RedisStorage(redis_client)
        return UserStore(storage)
