"""Depot : stocke et relit les produits dans une base SQLite."""
import sqlite3
from dataclasses import fields

import config
from app.models.produit import Produit

COLONNES = [champ.name for champ in fields(Produit)]


class Depot:
    def __init__(self, db_path=None):
        self.db_path = db_path or config.DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._creer_table()

    def _connexion(self):
        return sqlite3.connect(self.db_path)

    def _creer_table(self):
        conn = self._connexion()
        with conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS produits (
                    asin TEXT PRIMARY KEY,
                    titre TEXT,
                    prix TEXT,
                    note TEXT,
                    url TEXT,
                    image_url TEXT,
                    image_path TEXT,
                    categorie TEXT
                )"""
            )
        conn.close()

    def ajouter(self, produits):
        """Enregistre les produits (met a jour si l'asin existe deja)."""
        lignes = [tuple(getattr(p, c) for c in COLONNES) for p in produits]
        marques = ", ".join("?" for _ in COLONNES)
        conn = self._connexion()
        with conn:
            conn.executemany(
                f"INSERT OR REPLACE INTO produits ({', '.join(COLONNES)}) "
                f"VALUES ({marques})",
                lignes,
            )
        conn.close()
        return len(lignes)

    def tous(self):
        """Retourne tous les produits sous forme de liste de Produit."""
        conn = self._connexion()
        lignes = conn.execute(
            f"SELECT {', '.join(COLONNES)} FROM produits ORDER BY categorie, titre"
        ).fetchall()
        conn.close()
        return [Produit(*ligne) for ligne in lignes]

    def compter(self):
        conn = self._connexion()
        total = conn.execute("SELECT COUNT(*) FROM produits").fetchone()[0]
        conn.close()
        return total