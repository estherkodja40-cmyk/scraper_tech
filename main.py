"""Point d'entree. Usage :
    python main.py                  -> tous les mots-cles tech de config.py
    python main.py "casque gamer"   -> une seule recherche
"""
import sys

import config
from app.controllers.scraping_controller import ScrapingController


def main():
    if len(sys.argv) > 1:
        config.MOTS_CLES_TECH = [" ".join(sys.argv[1:])]
    ScrapingController().executer()


if __name__ == "__main__":
    main()