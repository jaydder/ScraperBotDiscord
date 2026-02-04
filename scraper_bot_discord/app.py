import discord
from bot.commands.help.help_command import (
    HelpCommand,
)
from bot.commands.help.help_factory import HelpFactory
from bot.commands.item.item_command import ItemCommand
from bot.commands.item.item_factory import ItemFactory
from bot.commands.stalker.stalker_command import (
    StalkerCommands,
)
from bot.commands.stalker.stalker_factory import (
    StalkerFactory,
)
from bot.storage.store_factory import StoreFactory
from discord.ext import commands
from model.settings import Settings

settings = Settings()


class RagnarokBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self) -> None:

        await self.add_cog(HelpCommand(self, HelpFactory()))
        await self.add_cog(ItemCommand(self, ItemFactory()))

        await self.add_cog(
            StalkerCommands(self, StalkerFactory(), StoreFactory())
        )

        synced = await self.tree.sync()
        print(f'✓ {len(synced)} comando(s) sincronizado(s)')

        for cmd in self.tree.get_commands():
            print(f'- {cmd.name}')


def main() -> None:
    if not settings.DISCORD_TOKEN:
        print('❌ Erro: DISCORD_TOKEN não encontrado em .env')
        return

    print('🤖 Iniciando bot Discord...')
    bot = RagnarokBot()
    bot.run(settings.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
