import discord
from discord import app_commands
from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot, help_service):
        self.bot = bot
        self.help_service = help_service

    @app_commands.command(
        name='help_ragnarok',
        description='Mostra informações sobre os comandos disponíveis',
    )
    async def help_ragnarok(self, interaction: discord.Interaction):
        embed = self.help_service.get_help_embed()
        await interaction.response.send_message(embed=embed)
