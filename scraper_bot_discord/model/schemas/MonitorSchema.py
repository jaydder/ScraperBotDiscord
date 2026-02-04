from dataclasses import dataclass


@dataclass
class MonitorSchema:
    user_id: int
    item_id: int
    interval: int
    max_value: int
    currency: str
