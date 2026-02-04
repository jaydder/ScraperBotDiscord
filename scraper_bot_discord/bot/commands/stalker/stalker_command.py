import discord
from discord import app_commands
from discord.ext import commands, tasks

from scraper_bot_discord.bot.services.stalker_service import StalkerService
from scraper_bot_discord.bot.storage.user_store import UserStore
from scraper_bot_discord.model.schemas.ItemSchema import ItemSchema
from scraper_bot_discord.model.schemas.MonitorSchema import MonitorSchema


class StalkerCommands(commands.Cog):
    def __init__(
        self, bot, stalker_service: StalkerService, storage: UserStore
    ):
        self.bot = bot
        self.service = stalker_service
        self.storage = storage
        self.counters = {}

    @app_commands.command(name='stalker')
    async def monitorar(
        self,
        interaction: discord.Interaction,
        item_id: int,
        interval: int = 60,
        max_value: int = 0,
        currency: str = '',
    ):
        await interaction.response.defer(ephemeral=True)

        schema = MonitorSchema(
            interaction.user.id,
            item_id,
            float(interval),
            max_value,
            currency,
        )

        self.storage.add(schema)
        self.storage.schedule(
            schema.user_id,
            schema.item_id,
            schema.interval,
        )
        try:
            item_schema = ItemSchema(
                interaction.user.id,
                item_id,
                max_value,
                currency,
            )
            embeds = await self.service.get_item_embed(item_schema)

            await interaction.followup.send(
                f'✅ Monitoramento iniciado para o item `{item_id}`',
                ephemeral=True,
            )

            user = await self.bot.fetch_user(schema.user_id)
            await user.send(embed=embeds)

        except Exception as e:
            await interaction.followup.send(
                '❌ Erro inesperado ao buscar o item.'
            )
            print(e)

    @app_commands.command(name='stalkerless')
    async def stalkerless(
        self, interaction: discord.Interaction, item_id: int
    ):
        self.storage.remove(interaction.user.id, item_id)
        self.storage.unschedule(interaction.user.id, item_id)

        await interaction.response.send_message(
            '🛑 Monitoramento encerrado.', ephemeral=True
        )

    @tasks.loop(seconds=10)
    async def loop(self):
        entries = self.storage.get_due()

        for entry in entries:
            user_id, item_id = map(int, entry.split(':'))

            data = self.storage.get_all(user_id, item_id)
            if not data:
                continue

            schema = ItemSchema(
                user_id,
                data['item_id'],
                data['max_value'],
                data['currency'],
            )

            embed = await self.service.get_item_embed(schema)
            if not embed:
                continue

            try:
                user = await self.bot.fetch_user(user_id)
                await user.send(embed=embed)
            except Exception:
                continue

            self.storage.schedule(user_id, item_id, float(data['interval']))

    @loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()
