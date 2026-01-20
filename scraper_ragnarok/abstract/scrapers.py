from abc import ABCMeta, abstractmethod
from typing import Any

from scraper_ragnarok.handlers.exceptions import MethodNotImplemented


class Scrapers(metaclass=ABCMeta):
    def __init__(self, item_id):
        self.item_id = item_id
        self.headers = {}
        self.url = None

    @abstractmethod
    def fetch_page(self, **kwargs) -> Any:
        raise MethodNotImplemented()

    @abstractmethod
    def extract_item_values(self, **kwargs) -> Any:
        raise MethodNotImplemented()
