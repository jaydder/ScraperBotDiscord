from redis import Redis, from_url

from scraper_bot_discord.bot.storage.user_store import UserStore
from scraper_bot_discord.infrastructure.redis_storage import RedisStorage
from scraper_bot_discord.model.settings import Settings


class StoreFactory:
    settings = Settings()

    def __new__(cls):
        redis_client = None
        if cls.settings.DEBUG == 1:
            redis_client = Redis(
                host=cls.settings.URL_DATABASE,
                port=cls.settings.PORT_DATABASE,
                db=0,
                decode_responses=True,
            )
        else:
            redis_client = from_url(
                url=cls.settings.URL_DATABASE,
                port=cls.settings.PORT_DATABASE,
                db=0,
                decode_responses=True,
            )

        storage = RedisStorage(redis_client)
        return UserStore(storage)
