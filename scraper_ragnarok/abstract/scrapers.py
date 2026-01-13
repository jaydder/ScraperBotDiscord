from abc import ABCMeta, abstractmethod

from handlers.exceptions import MethodNotImplemented


class Scrapers(metaclasse=ABCMeta):
    @abstractmethod
    def fetch_page() -> Exception:
        raise MethodNotImplemented()

    @abstractmethod
    def extract_item_values() -> Exception:
        raise MethodNotImplemented()
