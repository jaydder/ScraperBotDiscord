import pytest
from scraper_ragnarok import RagnarokItemScraper

MOCK_HTML = '''
<table class="shops-table">
    <tr>
        <th>Store</th><th>Refine</th><th>Other</th><th>Quantidade</th><th>Qtd</th><th>Currency</th>
    </tr>
    <tr>
        <td>Shop1</td><td>+5</td><td>---</td><td>500</td><td>2</td><td>RMT</td>
    </tr>
    <tr>
        <td>Shop2</td><td>+7</td><td>---</td><td>1500</td><td>1</td><td>Zeny</td>
    </tr>
    <tr>
        <td>Shop3</td><td>+0</td><td>---</td><td>800</td><td>5</td><td>RMT</td>
    </tr>
</table>
'''

def test_extract_item_values_filters_by_value_and_currency():
    scraper = RagnarokItemScraper(1)
    items = scraper.extract_item_values(MOCK_HTML, value=1000, currency="RMT")
    assert len(items) == 2
    assert items[0]["store"] == "Shop1"
    assert items[0]["item_value"] == "500"
    assert items[0]["type_currency"] == "RMT"
    assert items[1]["store"] == "Shop3"
    assert items[1]["item_value"] == "800"
    assert items[1]["type_currency"] == "RMT"

def test_extract_item_values_empty_when_no_match():
    scraper = RagnarokItemScraper(1)
    items = scraper.extract_item_values(MOCK_HTML, value=400, currency="RMT")
    assert items == []

def test_extract_item_values_different_currency():
    scraper = RagnarokItemScraper(1)
    items = scraper.extract_item_values(MOCK_HTML, value=2000, currency="Zeny")
    assert len(items) == 1
    assert items[0]["store"] == "Shop2"
    assert items[0]["type_currency"] == "Zeny"
