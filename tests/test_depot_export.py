from pathlib import Path

import config
from app.models.depot import Depot
from app.models.produit import Produit
from app.views.export_view import exporter_csv

produits = [
    Produit("B0AAAAAAAA", "Casque Pro", "29,99 €", "4,5 sur 5", categorie="test"),
    Produit("B0BBBBBBBB", "Souris", "15,00 €", categorie="test"),
]

depot = Depot(Path("data") / "test.db")
depot.ajouter(produits)
depot.ajouter(produits)  # pas de doublons
print("Produits en base :", depot.compter())

chemin = exporter_csv(depot.tous(), "test.csv")
print("CSV cree :", chemin)