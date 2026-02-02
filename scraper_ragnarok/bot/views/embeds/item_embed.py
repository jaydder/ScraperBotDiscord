import discord

from scraper_ragnarok.bot.views.templates.market import EmbedMarket


class ItemEmbedBuilder:
    @staticmethod
    def build(item_id, items) -> discord.Embed:
        return EmbedMarket(item_id, items)
