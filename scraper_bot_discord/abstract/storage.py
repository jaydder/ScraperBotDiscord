from abc import ABCMeta, abstractmethod
from typing import Any

from scraper_bot_discord.handlers.exceptions import MethodNotImplemented


class Storage(metaclass=ABCMeta):
    @abstractmethod
    def add(self, user_id, schema: dict[str, str | int]) -> Any:
        raise MethodNotImplemented()

    @abstractmethod
    def remove(self, user_id) -> Any:
        raise MethodNotImplemented()

    @abstractmethod
    def get_all(self, key: str) -> Any:
        raise MethodNotImplemented()
