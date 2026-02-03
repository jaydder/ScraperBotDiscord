from scraper_bot_discord.abstract.storage import Storage


class UserStore(Storage):
    def __init__(self):
        self.monitored_users: dict[int, dict] = {}

    def add(
        self,
        user_id: int,
        item_id: int,
        interval: int,
        max_value: int,
        currency: str,
    ):
        self.monitored_users[user_id] = {
            'item_id': item_id,
            'interval': interval,
            'max_value': max_value,
            'currency': currency,
        }

    def remove(self, user_id: int):
        self.monitored_users.pop(user_id, None)
