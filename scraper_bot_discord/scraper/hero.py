import re
from typing import Any, override

import requests
from bs4 import BeautifulSoup

from scraper_bot_discord.abstract.scrapers import Scrapers


class Hero(Scrapers):
    def __init__(self, item_id):
        super().__init__(item_id)
        self.url = (
            'https://site.heroragnarok.com/'
            + '?module=item'
            + '&action=view'
            + f'&id={item_id}'
        )
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            + 'AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Connection': 'keep-alive',
        }

    @override
    def fetch_page(self) -> str | None:
        """
        monta um request com header personalizado e envia para a URL setada no
        constructor da class
        Returns:
            str: HTML da pagina requesitada
            None: Erro ao acessar a pagina
        """
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()

            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Erro ao acessar a página: {e}')
            return None

    @override
    def extract_item_values(
        self, html: str, max_value: int = 0, currency: str = ''
    ):
        """
        Extrai os itens da página HTML, aplicando filtros opcionais de valor
        máximo e tipo de moeda.
        Args:
            html (str): HTML da página.
            max_value (int, opcional): Valor máximo do item para filtrar.
            currency (str, opcional): Tipo de moeda para filtrar
            (RMT, ROPS, Zeny).
        Returns:
            list[dict]: Lista de itens filtrados.
        """
        soup = BeautifulSoup(html, 'html.parser')
        items = []

        table = soup.find('table', class_='shops-table')

        COLUMNS = 6

        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= COLUMNS:
                    item = self.handler_columns_to_dict(cols)
                    currencies = ['RMT', 'ROPS', 'Zeny']
                    if (
                        currency in currencies
                        and item['type_currency'].lower() != currency.lower()
                    ):
                        continue
                    try:
                        item_value_int = int(item['item_value'])
                    except Exception:
                        item_value_int = None
                    if (
                        max_value is not None
                        and item_value_int is not None
                        and item_value_int > max_value
                    ):
                        continue
                    items.append(item)
        return items

    @staticmethod
    def handler_columns_to_dict(cols) -> dict[str, Any]:
        store_name = cols[0].get_text(strip=True)
        refine = cols[1].get_text(strip=True)
        quantidade = cols[3].get_text(strip=True)
        qtd = cols[4].get_text(strip=True)
        type_currency = cols[5].get_text(strip=True)

        item_value = ''.join(re.findall(r'\d', quantidade))

        return {
            'store': store_name,
            'item_value': item_value,
            'refine': refine,
            'type_currency': type_currency,
            'quantity': qtd,
        }


# if __name__ == '__main__':
#     scraper = Extractor(6635)
#     html = scraper.fetch_page()
#     items = scraper.extract_item_values(html, 1000, 'ROPS')
#     print(items)
