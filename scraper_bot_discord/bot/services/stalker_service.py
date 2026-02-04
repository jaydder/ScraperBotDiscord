from scraper_bot_discord.model.schemas.ItemSchema import ItemSchema
from scraper_bot_discord.scraper.hero import Hero


class StalkerService:
    def __init__(self, embed_builder):
        self.embed_builder = embed_builder

    async def get_item_embed(self, schema: ItemSchema):
        try:
            scraper = Hero(schema.item_id)
            html = scraper.fetch_page()

            if not html:
                raise RuntimeError('Não consegui acessar a página do item.')

            items = scraper.extract_item_values(
                html, schema.max_value, schema.currency.upper()
            )

            if not items:
                raise ValueError('Nenhuma informação encontrada.')

            return self.embed_builder.build(schema.item_id, items)

        except Exception as e:
            print(f'[STALKER] Erro ({schema.user_id}): {e}')
