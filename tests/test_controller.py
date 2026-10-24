"""Test hors ligne : verifie toute la chaine avec de faux produits (sans Amazon)."""
from pathlib import Path

import config
from app.controllers.scraping_controller import ScrapingController
from app.models.depot import Depot
from app.scraper.amazon_scraper import AmazonScraper


class FauxClient:
    def get(self, url):
        return "".join(
            f'<div data-asin="B0TEST{i:04d}" data-component-type="s-search-result">'
            f'<h2><span>Produit tech {i}</span></h2>'
            f'<span class="a-offscreen">{10 + i},99 €</span></div>'
            for i in range(3)
        )

    def pause(self):
        pass

    def telecharger_image(self, url, chemin):
        return False


config.MOTS_CLES_TECH = ["test"]
config.PAGES_MAX = 1

controller = ScrapingController(
    scraper=AmazonScraper(FauxClient()),
    depot=Depot(Path("data") / "test_controller.db"),
)
controller.executer("test.csv")