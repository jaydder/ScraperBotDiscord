from bot.services.item_service import ItemService
from bot.views.embeds.item_embed import ItemEmbedBuilder
from discord.ext import commands


class ItemFactory(commands.Bot):
    def __new__(cls):
        embed_builder = ItemEmbedBuilder()
        item_service = ItemService(embed_builder)

        return item_service
