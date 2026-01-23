import discord

MAX_FIELD = 1020


class ItemEmbedBuilder:
    @staticmethod
    def build(item_id, items) -> discord.Embed:
        embed = discord.Embed(
            title=f'📊 Item ID: {item_id}',
            description=f'Encontradas **{len(items)}** loja(s) disponível(is)',
            color=discord.Color.blue(),
        )

        embed.set_footer(text='Ragnarok Item Scraper | Hero Ragnarok')

        current_value = ''
        field_counter = 1

        for item in items:
            entry = (
                f'**{item["store"]}**\n'
                f'  • Refino: {item["refine"]}\n'
                f'  • Quantidade (ROP): {item["item_value"]}\n'
                f'  • Tipo: {item["type_currency"]}\n'
                f'  • Qtd: {item["quantity"]}\n'
                f'  ─────────────────\n'
            )

            if len(current_value) + len(entry) > MAX_FIELD:
                embed.add_field(
                    name='Lojas'
                    if field_counter == 1
                    else f'Lojas (cont. {field_counter})',
                    value=current_value,
                    inline=False,
                )
                current_value = entry
                field_counter += 1
            else:
                current_value += entry

        if current_value:
            embed.add_field(
                name='Lojas'
                if field_counter == 1
                else f'Lojas (cont. {field_counter})',
                value=current_value,
                inline=False,
            )

        return [embed]
