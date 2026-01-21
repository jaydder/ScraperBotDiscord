import discord
from discord import app_commands
from discord.ext import commands


class ItemCommand(commands.Cog):
    def __init__(self, bot, item_service):
        self.bot = bot
        self.item_service = item_service

    @app_commands.command(
        name='item', description='Busca informações de um item no Ragnarok'
    )
    async def item_search(
        self, interaction: discord.Interaction, item_id: int
    ):
        try:
            embeds = self.item_service.get_item_embed(item_id)
            await interaction.followup.send(embeds=embeds)

        except ValueError as e:
            await interaction.followup.send(f'❌ {str(e)}')

        except Exception as e:
            await interaction.followup.send(
                '❌ Erro inesperado ao buscar o item.'
            )
            print(e)
