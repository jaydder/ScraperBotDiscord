from abc import ABCMeta, abstractmethod
from typing import Any

from scraper_ragnarok.handlers.exceptions import MethodNotImplemented


class Storage(metaclass=ABCMeta):
    @abstractmethod
    def add(self) -> Any:
        raise MethodNotImplemented()

    @abstractmethod
    def remove(self) -> Any:
        raise MethodNotImplemented()
