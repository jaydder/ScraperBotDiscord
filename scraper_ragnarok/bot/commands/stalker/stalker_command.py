import discord
from bot.services.stalker_service import StalkerService
from discord import app_commands
from discord.ext import commands, tasks

from scraper_ragnarok.bot.storage.user_store import UserStore


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

        if not self.loop.is_running():
            self.loop.start()

        self.storage.add(
            interaction.user.id,
            item_id,
            interval,
            max_value,
            currency,
        )
        try:
            embeds = await self.service.get_item_embed(
                interaction.user.id, item_id, max_value, currency
            )
            await interaction.followup.send(
                f'✅ Monitoramento iniciado para o item `{item_id}`',
                ephemeral=True,
            )

            user = await self.bot.fetch_user(interaction.user.id)
            await user.send(embed=embeds)

        except Exception as e:
            await interaction.followup.send(
                '❌ Erro inesperado ao buscar o item.'
            )
            print(e)

    @app_commands.command(name='stalkerless')
    async def stalkerless(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        self.storage.remove(user_id)
        self.counters.pop(user_id, None)

        await interaction.response.send_message(
            '🛑 Monitoramento encerrado.',
        )
        self.loop.cancel()

    @tasks.loop(minutes=1)
    async def loop(self):
        users_to_update, data, user_id = [], {}, None

        for user_id, data in self.storage.monitored_users.items():
            if not self.counters:
                self.counters = {}

        if user_id not in self.counters:
            self.counters[user_id] = 0

        self.counters[user_id] += 1

        if self.counters[user_id] >= data['interval']:
            users_to_update.append((user_id, data['item_id']))
            self.counters[user_id] = 0

        for user_id, _ in users_to_update:
            embed = await self.service.get_item_embed(
                user_id,
                data['item_id'],
                data['max_value'],
                data['currency'],
            )
            if not embed:
                continue

            try:
                user = await self.bot.fetch_user(user_id)
                await user.send(embed=embed)

            except discord.Forbidden:
                self.storage.remove(user_id)

    @loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()
