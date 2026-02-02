import discord


class HelpEmbedBuilder:
    @staticmethod
    def build() -> discord.Embed:
        embed = discord.Embed(
            title='📜 Comandos Disponíveis - Ragnarok Bot',
            description='Lista de comandos para usar o bot',
            color=discord.Color.green(),
        )

        embed.add_field(
            name='/help_ragnarok',
            value='Mostra esta mensagem de ajuda',
            inline=False,
        )

        embed.add_field(
            name='❓ Como usar?',
            value='Digite o comando na barra de mensagens e pressione Enter',
            inline=False,
        )

        embed.set_footer(text='Ragnarok Item Scraper Bot')

        return embed
