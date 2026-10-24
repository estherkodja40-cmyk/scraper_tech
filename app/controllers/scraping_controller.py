"""Controller : le coeur du projet. Il orchestre scraper, depot et vues."""
import config
from app.models.depot import Depot
from app.scraper.amazon_scraper import AmazonScraper
from app.views import console_view
from app.views.export_view import exporter_csv


class ScrapingController:
    def __init__(self, scraper=None, depot=None):
        self.scraper = scraper or AmazonScraper()
        self.depot = depot or Depot()

    def executer(self, nom_csv=None):
        config.creer_dossiers()

        console_view.afficher_titre("Scraping Amazon - categorie tech")
        try:
            produits = self.scraper.scraper_categorie_tech()
            produits = [p for p in produits if p.est_complet()]
            if produits:
                console_view.afficher_message("\nTelechargement des images...")
                self.scraper.telecharger_images(produits)
        finally:
            self.scraper.fermer()  # ferme Chrome meme en cas d'erreur

        if not produits:
            console_view.afficher_message(
                "\nAucun produit recupere (Amazon a probablement bloque la page). "
                "Reessaie plus tard."
            )
            return []

        self.depot.ajouter(produits)
        tous = self.depot.tous()
        chemin_csv = exporter_csv(tous, nom_csv)

        console_view.afficher_titre("Apercu")
        console_view.afficher_produits(produits)
        console_view.afficher_resume(
            len(produits), self.depot.compter(), chemin_csv, config.IMAGES_DIR
        )
        return produits