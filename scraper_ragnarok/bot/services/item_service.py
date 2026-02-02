from scraper.hero import Hero


class ItemService:
    def __init__(self, embed_builder):
        self.embed_builder = embed_builder

    def get_item_embed(self, item_id, max_value, currency):
        scraper = Hero(item_id)
        html = scraper.fetch_page()

        if not html:
            raise RuntimeError('Não consegui acessar a página do item.')

        items = scraper.extract_item_values(html, max_value, currency.upper())

        if not items:
            raise ValueError('Nenhuma informação encontrada.')

        return self.embed_builder.build(item_id, items)
