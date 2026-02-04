from dataclasses import asdict

from scraper_bot_discord.abstract.storage import Storage
from scraper_bot_discord.model.schemas.MonitorSchema import MonitorSchema


class UserStore:
    def __init__(self, storage: Storage):
        self.storage = storage

    def add(self, config: MonitorSchema):
        key = f'monitor:{config.user_id}:{config.item_id}'
        self.storage.add(key, asdict(config))

    def remove(self, user_id: int, item_id: int):
        key = f'monitor:{user_id}:{item_id}'
        self.storage.remove(key)

    def get_all(self, user_id: int, item_id: int):
        key = f'monitor:{user_id}:{item_id}'
        return self.storage.get_all(key)
