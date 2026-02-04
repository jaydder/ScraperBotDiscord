from dataclasses import dataclass


@dataclass
class ItemSchema:
    user_id: int
    item_id: int
    max_value: int
    currency: str
