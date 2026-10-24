from app.scraper.parsing import parser_produits

html = """<div data-asin="B0ABCDEFGH" data-component-type="s-search-result">
<h2><span>Casque Pro</span></h2>
<span class="a-offscreen">29,99 €</span></div>"""

print(parser_produits(html, "test"))