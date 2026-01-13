import asyncio
import os
from datetime import datetime

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from scraper_ragnarok import RagnarokItemScraper
from scraper_ragnarok.keep_alive import keep_alive

load_dotenv()

keep_alive()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', '0'))  # Definir OWNER_ID no .env

monitored_users = {}


@bot.event
async def on_ready():
    print(f'✓ Bot conectado como {bot.user}')
    print(f'✓ Bot ID: {bot.user.id}')
    try:
        synced = await bot.tree.sync()
        print(f'✓ {len(synced)} comando(s) sincronizado(s)')
    except Exception as e:
        print(f'Erro ao sincronizar comandos: {e}')

    if not check_market_updates.is_running():
        check_market_updates.start()
        print('✓ Monitoramento de mercado iniciado')


@bot.tree.command(
    name='item', description='Busca informações de um item no Ragnarok'
)
async def search_item(interaction: discord.Interaction, item_id: int):
    await interaction.response.defer()

    try:
        await interaction.followup.send('🔍 Buscando informações do item...')

        scraper = RagnarokItemScraper(item_id)
        html = scraper.fetch_page()

        if not html:
            await interaction.followup.send(
                '❌ Erro: Não consegui acessar a página do item.'
            )
            return

        items = scraper.extract_item_values(html)

        if not items:
            await interaction.followup.send(
                f'❌ Nenhuma informação encontrada para o item ID: `{item_id}`'
            )
            return

        embed = discord.Embed(
            title=f'📊 Item ID: {item_id}',
            description=f'Encontradas **{len(items)}** loja(s) disponível(is)',
            color=discord.Color.blue(),
        )

        embed.set_footer(text='Ragnarok Item Scraper | Hero Ragnarok')

        current_field_value = ''
        field_counter = 1

        for idx, item in enumerate(items):
            loja_entry = (
                f'**{item["loja"]}**\n'
                f'  • Refino: {item["refino"]}\n'
                f'  • Quantidade (ROP): {item["quantidade_rops"]}\n'
                f'  • Tipo: {item["type_value"]}\n'
                f'  • Qtd: {item["qtd"]}\n'
                f'  ─────────────────\n'
            )

            if len(current_field_value) + len(loja_entry) > 1020:
                field_name = (
                    'Lojas'
                    if field_counter == 1
                    else f'Lojas (cont. {field_counter})'
                )
                embed.add_field(
                    name=field_name, value=current_field_value, inline=False
                )
                current_field_value = loja_entry
                field_counter += 1
            else:
                current_field_value += loja_entry

        if current_field_value:
            field_name = (
                'Lojas'
                if field_counter == 1
                else f'Lojas (cont. {field_counter})'
            )
            embed.add_field(
                name=field_name, value=current_field_value, inline=False
            )

        if len(embed.fields) > 25:
            embeds = [embed]
            remaining_items = items[len(items) // 2 :]

            for item in remaining_items:
                new_embed = discord.Embed(
                    title=f'📊 Item ID: {item_id} (Continuação)',
                    color=discord.Color.blue(),
                )
                loja_entry = (
                    f'**{item["loja"]}**\n'
                    f'  • Refino: {item["refino"]}\n'
                    f'  • Quantidade (ROP): {item["quantidade_rops"]}\n'
                    f'  • Tipo: {item["type_value"]}\n'
                    f'  • Qtd: {item["qtd"]}'
                )
                new_embed.add_field(
                    name='Loja', value=loja_entry, inline=False
                )
                embeds.append(new_embed)

            await interaction.followup.send(embeds=embeds)
        else:
            await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f'❌ Erro ao processar: {str(e)}')


@bot.tree.command(
    name='help_ragnarok',
    description='Mostra informações sobre os comandos disponíveis',
)
async def help_ragnarok(interaction: discord.Interaction):
    embed = discord.Embed(
        title='📖 Comandos Disponíveis - Ragnarok Bot',
        description='Lista de comandos para usar o bot',
        color=discord.Color.green(),
    )

    embed.add_field(
        name='/item <item_id>',
        value='Busca informações de um item no Ragnarok\nExemplo: `/item 547`',
        inline=False,
    )

    embed.add_field(
        name='/items <IDs>',
        value='Busca insformacoes de mais de um item no Ragnarok',
        inline=False,
    )

    embed.add_field(
        name='/monitorar <item_id> [intervalo_minutos]',
        value='Começa a monitorar um item e recebe atualizações em mensagem privada\nExemplo: `/monitorar 547 30` (a cada 30 minutos, padrão 60)',
        inline=False,
    )

    embed.add_field(
        name='/parar_monitorar',
        value='Para o monitoramento e deixa de receber atualizações',
        inline=False,
    )

    embed.add_field(
        name='/meu_monitoramento',
        value='Mostra qual item você está monitorando e o intervalo',
        inline=False,
    )

    embed.add_field(
        name='/restart',
        value='Reinicia o bot com as novas modificações (apenas admin)',
        inline=False,
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

    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name='restart',
    description='Reinicia o bot com as novas modificações (apenas para admin)',
)
async def restart_bot(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        embed = discord.Embed(
            title='❌ Acesso Negado',
            description='Apenas o proprietário do bot pode usar este comando.',
            color=discord.Color.red(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(
        title='🔄 Reiniciando Bot',
        description='O bot será reiniciado em alguns segundos...\n\n✅ Novas modificações serão carregadas',
        color=discord.Color.blue(),
    )

    await interaction.response.send_message(embed=embed)

    print('\n' + '=' * 60)
    print('🔄 Bot sendo reiniciado pelo usuário...')
    print('=' * 60 + '\n')

    await asyncio.sleep(2)

    await bot.close()


async def send_market_update(user_id: int, item_id: int, value: int):
    try:
        user = await bot.fetch_user(user_id)

        scraper = RagnarokItemScraper(item_id)
        html = scraper.fetch_page()

        if not html:
            await user.send('❌ Erro: Não consegui acessar a página do item.')
            return

        items = scraper.extract_item_values(html, value)

        if not items:
            await user.send(
                f'❌ Nenhuma informação encontrada para o item ID: `{item_id}`'
            )
            return

        embed = discord.Embed(
            title=f'📊 Atualização do Mercado - Item {item_id}',
            description=f'🕐 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nEncontradas **{len(items)}** loja(s)',
            color=discord.Color.gold(),
        )

        current_field_value = ''
        field_counter = 1

        for item in items:
            loja_entry = (
                f'**{item["loja"]}**\n'
                f'  • Refino: {item["refino"]}\n'
                f'  • Quantidade (ROP): {item["quantidade_rops"]}\n'
                f'  • Tipo: {item["type_value"]}\n'
                f'  • Qtd: {item["qtd"]}\n'
                f'  ─────────────────\n'
            )

            if len(current_field_value) + len(loja_entry) > 1020:
                field_name = (
                    'Lojas'
                    if field_counter == 1
                    else f'Lojas (cont. {field_counter})'
                )
                embed.add_field(
                    name=field_name, value=current_field_value, inline=False
                )
                current_field_value = loja_entry
                field_counter += 1
            else:
                current_field_value += loja_entry

        if current_field_value:
            field_name = (
                'Lojas'
                if field_counter == 1
                else f'Lojas (cont. {field_counter})'
            )
            embed.add_field(
                name=field_name, value=current_field_value, inline=False
            )

        embed.set_footer(text='Monitoramento Automático - Ragnarok Bot')

        await user.send(embed=embed)

    except Exception as e:
        print(f'Erro ao enviar atualização para usuário {user_id}: {e}')


@bot.tree.command(
    name='monitorar',
    description='Começa a monitorar um item e recebe atualizações em mensagem privada',
)
async def monitor_item(
    interaction: discord.Interaction,
    item_id: int,
    filter_minimum_value: int,
    intervalo_minutos: int = 60,
):
    await interaction.response.defer()

    user_id = interaction.user.id

    monitored_users[user_id] = {
        'item_id': item_id,
        'interval': intervalo_minutos,
    }

    await send_market_update(
        user_id=user_id, item_id=item_id, value=filter_minimum_value
    )

    embed = discord.Embed(
        title='✅ Monitoramento Iniciado',
        description=f'Você receberá atualizações do item **{item_id}** a cada **{intervalo_minutos} minuto(s)** em mensagem privada.',
        color=discord.Color.green(),
    )

    embed.add_field(
        name='💡 Dica',
        value='Use `/parar_monitorar` para parar de receber atualizações',
        inline=False,
    )

    await interaction.followup.send(embed=embed)


@bot.tree.command(
    name='parar_monitorar', description='Para o monitoramento de item'
)
async def stop_monitor(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in monitored_users:
        await interaction.response.send_message(
            '❌ Você não está monitorando nenhum item no momento.'
        )
        return

    item_id = monitored_users[user_id]['item_id']
    del monitored_users[user_id]

    embed = discord.Embed(
        title='⏹️ Monitoramento Parado',
        description=f'Você parou de receber atualizações do item **{item_id}**',
        color=discord.Color.red(),
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name='meu_monitoramento',
    description='Mostra qual item você está monitorando',
)
async def my_monitoring(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in monitored_users:
        await interaction.response.send_message(
            'ℹ️ Você não está monitorando nenhum item no momento.\n'
            'Use `/monitorar` para começar!'
        )
        return

    data = monitored_users[user_id]

    embed = discord.Embed(
        title='📡 Seu Monitoramento Ativo', color=discord.Color.blue()
    )

    embed.add_field(name='Item ID', value=str(data['item_id']), inline=True)
    embed.add_field(
        name='Intervalo', value=f'{data["interval"]} minuto(s)', inline=True
    )

    await interaction.response.send_message(embed=embed)


@tasks.loop(minutes=1)
async def check_market_updates():
    users_to_update = []

    for user_id, data in monitored_users.items():
        if not hasattr(check_market_updates, 'counters'):
            check_market_updates.counters = {}

        if user_id not in check_market_updates.counters:
            check_market_updates.counters[user_id] = 0

        check_market_updates.counters[user_id] += 1

        if check_market_updates.counters[user_id] >= data['interval']:
            users_to_update.append((user_id, data['item_id']))
            check_market_updates.counters[user_id] = 0

    for user_id, item_id in users_to_update:
        await send_market_update(user_id, item_id)


@bot.event
async def on_command_error(
    interaction: discord.Interaction, error: commands.CommandError
):
    if isinstance(error, commands.CommandNotFound):
        await interaction.response.send_message(
            '❌ Comando não encontrado. Use `/help_ragnarok` para ver os comandos disponíveis.'
        )
    else:
        await interaction.response.send_message(f'❌ Erro: {str(error)}')


def main():
    if not DISCORD_TOKEN:
        print('❌ Erro: DISCORD_TOKEN não encontrado em .env')
        print(
            'Por favor, crie um arquivo .env com: DISCORD_TOKEN=seu_token_aqui'
        )
        return

    print('🤖 Iniciando bot Discord...')
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
