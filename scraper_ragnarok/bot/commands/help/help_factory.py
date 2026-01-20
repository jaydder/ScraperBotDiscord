from bot.commands.help.help_command import build_help_command
from bot.services.help_service import HelpService
from bot.views.embeds.help_embed import HelpEmbedBuilder


def create_command():
    embed_builder = HelpEmbedBuilder()
    service = HelpService(embed_builder)

    return build_help_command(service)
