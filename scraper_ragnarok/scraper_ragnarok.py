import re
from typing import Dict, List

import requests
from bs4 import BeautifulSoup


class RagnarokItemScraper:
    def __init__(self, id):
        self.url = f"https://site.heroragnarok.com/?module=item&action=view&id={id}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_page(self) -> str:
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()

            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a página: {e}")
            return None

    def extract_item_values(
        self, html: str, value: int, currency: str
    ) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        items = []

        table = soup.find("table", class_="shops-table")

        if table:
            rows = table.find_all("tr")[1:]

            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    try:
                        quantidade = cols[3].get_text(strip=True)
                        type_currency = cols[5].get_text(strip=True)

                        item_value = "".join(re.findall(r"\d", quantidade))

                        if int(item_value) <= value and type_currency == currency:
                            store_name = cols[0].get_text(strip=True)
                            refine = cols[1].get_text(strip=True)
                            qtd = cols[4].get_text(strip=True)

                            if store_name:
                                items.append(
                                    {
                                        "store": store_name,
                                        "item_value": item_value,
                                        "refine": refine,
                                        "type_currency": type_currency,
                                        "quantity": qtd,
                                    }
                                )
                    except (IndexError, AttributeError):
                        continue

        return items


# if __name__ == "__main__":
#     scraper = RagnarokItemScraper(6635)
#     html = scraper.fetch_page()

#     items = scraper.extract_item_values(html, 1000, "RMT")
#     print(items)
