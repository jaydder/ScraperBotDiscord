import discord
from bot.commands.help.help_command import (
    HelpCommand,
)
from bot.commands.help.help_factory import HelpFactory
from discord.ext import commands
from model.settings import Settings

settings = Settings()


class RagnarokBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self) -> None:
        await self.add_cog(HelpCommand(self, HelpFactory()))

        # 🔹 Sync (DEV: use guild)
        synced = await self.tree.sync(
            guild=discord.Object(id=settings.GUILD_ID)
        )
        print(f'✓ {len(synced)} comando(s) sincronizado(s)')


def main() -> None:
    if not settings.DISCORD_TOKEN:
        print('❌ Erro: DISCORD_TOKEN não encontrado em .env')
        return

    print('🤖 Iniciando bot Discord...')
    bot = RagnarokBot()
    bot.run(settings.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
