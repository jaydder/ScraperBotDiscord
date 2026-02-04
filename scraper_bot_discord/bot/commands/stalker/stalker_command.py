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
        self.schema = None
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

        if not self.loop.is_running():
            self.loop.start()

        self.schema = MonitorSchema(
            interaction.user.id,
            item_id,
            interval,
            max_value,
            currency,
        )

        self.storage.add(self.schema)
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

            user = await self.bot.fetch_user(self.schema.user_id)
            await user.send(embed=embeds)

        except Exception as e:
            await interaction.followup.send(
                '❌ Erro inesperado ao buscar o item.'
            )
            print(e)

    @app_commands.command(name='stalkerless')
    async def stalkerless(self, interaction: discord.Interaction):
        self.storage.remove(self.schema.user_id, self.schema.item_id)
        self.counters.pop(self.schema.user_id, None)

        await interaction.response.send_message(
            '🛑 Monitoramento encerrado.',
        )
        self.loop.cancel()

    @tasks.loop(minutes=1)
    async def loop(self):
        users_to_update = []
        data = self.storage.get_all(self.schema.user_id, self.schema.item_id)

        if self.schema.user_id not in self.counters:
            self.counters[self.schema.user_id] = 0

        self.counters[self.schema.user_id] += 1

        if self.counters[self.schema.user_id] >= int(data['interval']):
            users_to_update.append((self.schema.user_id, data['item_id']))
            self.counters[self.schema.user_id] = 0

        for user_id, _ in users_to_update:
            new_schema = ItemSchema(
                self.schema.user_id,
                data['item_id'],
                data['max_value'],
                data['currency'],
            )
            embed = await self.service.get_item_embed(new_schema)
            if not embed:
                continue

            user = await self.bot.fetch_user(self.schema.user_id)
            await user.send(embed=embed)

    @loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()
