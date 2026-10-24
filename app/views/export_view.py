"""Vue d'export : ecrit les produits dans un fichier CSV."""
import csv

import config
from app.models.produit import Produit


def exporter_csv(produits, nom_fichier=None):
    """Ecrit les produits dans exports/<nom>.csv et retourne le chemin."""
    config.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    chemin = config.EXPORT_DIR / (nom_fichier or config.CSV_NAME)
    colonnes = list(Produit.__dataclass_fields__.keys())

    # utf-8-sig + ';' : s'ouvre correctement dans Excel en francais
    with open(chemin, "w", newline="", encoding="utf-8-sig") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=colonnes, delimiter=";")
        writer.writeheader()
        for produit in produits:
            writer.writerow(produit.en_dict())
    return chemin