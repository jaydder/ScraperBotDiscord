from scraper.extractor import Extractor


class StalkerService:
    def __init__(self, embed_builder):
        self.embed_builder = embed_builder

    async def get_item_embed(
        self, user_id: int, item_id: int, max_value: int, currency: str
    ):
        try:
            scraper = Extractor(item_id)
            html = scraper.fetch_page()

            if not html:
                raise RuntimeError('Não consegui acessar a página do item.')

            items = scraper.extract_item_values(
                html, max_value, currency.upper()
            )

            if not items:
                raise ValueError('Nenhuma informação encontrada.')

            return self.embed_builder.build(item_id, items)

        except Exception as e:
            print(f'[STALKER] Erro ({user_id}): {e}')
