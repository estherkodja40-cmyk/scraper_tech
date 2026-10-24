"""Entite Produit : represente un article scrape sur Amazon."""
from dataclasses import dataclass, asdict


@dataclass
class Produit:
    asin: str
    titre: str = ""
    prix: str = ""
    note: str = ""
    url: str = ""
    image_url: str = ""
    image_path: str = ""   # chemin local de l'image telechargee
    categorie: str = ""    # mot-cle tech utilise pour la recherche

    def en_dict(self):
        """Retourne le produit sous forme de dictionnaire (pour CSV/DB)."""
        return asdict(self)

    def est_complet(self):
        """Un produit est exploitable s'il a au moins un titre et un prix."""
        return bool(self.titre and self.prix)