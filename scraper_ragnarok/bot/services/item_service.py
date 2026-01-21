from scraper.extractor import Extractor


class ItemService:
    def __init__(self, embed_builder):
        self.embed_builder = embed_builder

    def get_item_embed(self, item_id):
        scraper = Extractor(item_id)
        html = scraper.fetch_page()

        if not html:
            raise RuntimeError('Não consegui acessar a página do item.')

        items = scraper.extract_item_values(html)
        breakpoint()

        if not items:
            raise ValueError('Nenhuma informação encontrada.')

        return self.embed_builder.build(item_id, items)
