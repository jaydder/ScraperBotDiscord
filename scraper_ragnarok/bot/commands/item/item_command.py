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
        self,
        interaction: discord.Interaction,
        item_id: int,
        max_value: int,
        currency: str,
    ):

        await interaction.response.defer(ephemeral=True)
        try:
            embeds = self.item_service.get_item_embed(
                item_id, max_value, currency
            )

            user = await self.bot.fetch_user(interaction.user.id)
            await user.send(embed=embeds)

            await interaction.followup.send(
                f'✅ Item `{item_id}` achado',
                ephemeral=True,
            )

        except ValueError as e:
            await interaction.followup.send(f'❌ {str(e)}')

        except Exception as e:
            await interaction.followup.send(
                '❌ Erro inesperado ao buscar o item.'
            )
            print(e)
