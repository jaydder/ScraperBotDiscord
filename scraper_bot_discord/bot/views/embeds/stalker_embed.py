import discord

from scraper_bot_discord.bot.views.templates.market import EmbedMarket


class StalkerEmbedBuilder:
    @staticmethod
    def build(item_id: int, items: list[dict]) -> discord.Embed:
        return EmbedMarket(item_id, items)
