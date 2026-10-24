"""Parametres globaux du projet scraper tech Amazon."""
from pathlib import Path

# --- Chemins -----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"
IMAGES_DIR = BASE_DIR / "images"

DB_PATH = DATA_DIR / "produits.db"
CSV_NAME = "produits_tech.csv"

# --- Amazon ------------------------------------------------------------
AMAZON_URL = "https://www.amazon.fr"
SEARCH_URL = AMAZON_URL + "/s?k={mot_cle}&page={page}"

# Categorie tech : une recherche par mot-cle
MOTS_CLES_TECH = [
    "casque bluetooth",
    "souris gaming",
    "clavier mecanique",
    "ecran pc",
    "webcam",
]

# --- Scraping ----------------------------------------------------------
PAGES_MAX = 2                  # pages par mot-cle (reste raisonnable)
DELAI_ENTRE_REQUETES = (3, 6)  # pause aleatoire en secondes (min, max)
NB_TENTATIVES = 2              # essais par page

# --- Selenium (Chrome) -------------------------------------------------
HEADLESS = False               # False = Chrome visible (captcha resolvable a la main)
ATTENTE_PAGE = 60              # secondes max pour obtenir une vraie page de resultats


def creer_dossiers():
    """Cree les dossiers de sortie s'ils n'existent pas."""
    for dossier in (DATA_DIR, EXPORT_DIR, IMAGES_DIR):
        dossier.mkdir(parents=True, exist_ok=True)