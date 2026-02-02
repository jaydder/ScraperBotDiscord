from bot.services.stalker_service import StalkerService
from bot.views.embeds.stalker_embed import StalkerEmbedBuilder
from discord.ext import commands


class StalkerFactory(commands.Bot):
    def __new__(cls):
        embed_builder = StalkerEmbedBuilder()
        item_service = StalkerService(embed_builder)

        return item_service
