from bot.services.help_service import HelpService
from bot.views.embeds.help_embed import HelpEmbedBuilder
from discord.ext import commands


class HelpFactory(commands.Bot):
    def __new__(cls):
        embed_builder = HelpEmbedBuilder()
        help_service = HelpService(embed_builder)
        return help_service
