# Scraper tech Amazon

Scraping de la categorie tech d'Amazon avec Selenium, extraction avec `re`
(sans BeautifulSoup), architecture MVC, stockage SQLite, export CSV et images.

## Installation
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

## Utilisation
python main.py                  (tous les mots-cles de config.py)
python main.py "casque gamer"   (une seule recherche)

## Roadmap
- [x] config.py
- [x] models : produit.py, depot.py (SQLite)
- [x] scraper : driver.py (Selenium), parsing.py (re), amazon_scraper.py
- [x] views : console_view.py, export_view.py (CSV)
- [x] controller : scraping_controller.py
- [x] main.py
- [x] Telechargement des images dans images/
- [ ] Gerer plus finement les blocages Amazon
- [ ] Tests supplementaires

## Git
git init / git add . / git commit -m "message"
Branche : git switch -c feature/nom
Merge : git switch main puis git merge feature/nom
Rebase : git switch feature/nom puis git rebase main