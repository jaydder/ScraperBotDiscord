import discord
from bot.commands.help.help_factory import create_command as help_command
from discord.ext import commands
from dotenv import load_dotenv

from scraper_ragnarok.model.settings import Settings

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

settings = Settings()


@bot.event
async def on_ready():
    print(f'✓ Bot conectado como {bot.user}')
    print(f'✓ Bot ID: {bot.user.id}')
    try:
        # bot.tree.clear_commands(guild=None)

        guild = discord.Object(id=settings.GUILD_ID)

        # REMOVE TODOS OS COMANDOS DA GUILD
        bot.tree.clear_commands(guild=guild)

        synced = await bot.tree.sync(
            guild=discord.Object(id=settings.GUILD_ID)
        )
        print(f'✓ {len(synced)} comando(s) sincronizado(s)')
    except Exception as e:
        print(f'Erro ao sincronizar comandos: {e}')


def registry_command():
    bot.tree.add_command(help_command())


def main() -> None:

    if not settings.DISCORD_TOKEN:
        print('❌ Erro: DISCORD_TOKEN não encontrado em .env')
        print(
            'Por favor, crie um arquivo .env com: DISCORD_TOKEN=seu_token_aqui'
        )
        return

    print('🤖 Iniciando bot Discord...')

    registry_command()

    bot.run(settings.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
