"""Scraper Amazon : parcourt les mots-cles tech, les pages, et recupere les images."""
from urllib.parse import quote_plus

import config
from app.models.produit import Produit
from app.scraper.driver import DriverChrome
from app.scraper.parsing import parser_produits


class AmazonScraper:
    def __init__(self, client=None):
        self.client = client or DriverChrome()

    def scraper_mot_cle(self, mot_cle):
        """Scrape toutes les pages (jusqu'a PAGES_MAX) pour un mot-cle."""
        produits = []
        for page in range(1, config.PAGES_MAX + 1):
            url = config.SEARCH_URL.format(mot_cle=quote_plus(mot_cle), page=page)
            print(f"[scraper] {mot_cle} - page {page}")

            html = self.client.get(url)
            if html is None:
                print("[scraper] page inaccessible, on passe au mot-cle suivant")
                break

            trouves = parser_produits(html, categorie=mot_cle)
            print(f"[scraper]   -> {len(trouves)} produits")
            if not trouves:
                break
            produits.extend(trouves)
            self.client.pause()
        return produits

    def scraper_categorie_tech(self):
        """Scrape tous les mots-cles tech de config.py, sans doublons (asin)."""
        vus = {}
        for mot_cle in config.MOTS_CLES_TECH:
            for produit in self.scraper_mot_cle(mot_cle):
                vus.setdefault(produit.asin, produit)
            self.client.pause()
        return list(vus.values())

    def telecharger_images(self, produits):
        """Telecharge l'image de chaque produit dans le dossier images."""
        config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        for produit in produits:
            if not produit.image_url:
                continue
            chemin = config.IMAGES_DIR / f"{produit.asin}.png"
            if chemin.exists() or self.client.telecharger_image(produit.image_url, chemin):
                produit.image_path = str(chemin.relative_to(config.BASE_DIR))
        return produits

    def fermer(self):
        """Ferme Chrome (si le client sait le faire)."""
        fermer = getattr(self.client, "fermer", None)
        if fermer:
            fermer()