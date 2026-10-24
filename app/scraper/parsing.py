"""Extraction des produits depuis le HTML, avec le module re (sans BS4)."""
import html as html_lib
import re

from app.models.produit import Produit
import config

RE_FICHE = re.compile(r'<div[^>]*data-component-type="s-search-result"[^>]*>')
RE_ASIN = re.compile(r'data-asin="([A-Z0-9]{10})"')
RE_TITRE = re.compile(r"<h2[^>]*>.*?<span[^>]*>(.*?)</span>", re.S)
RE_PRIX = re.compile(r'<span class="a-offscreen">(.*?)</span>', re.S)
RE_NOTE = re.compile(r'<span class="a-icon-alt">(.*?)</span>', re.S)
RE_IMAGE = re.compile(r'<img[^>]*class="[^"]*s-image[^"]*"[^>]*src="(.*?)"', re.S)
RE_LIEN = re.compile(r'href="(/[^"]*?/dp/[A-Z0-9]{10}[^"]*)"')
RE_BALISES = re.compile(r"<[^>]+>")


def nettoyer(texte):
    """Enleve les balises, les entites HTML (&amp;, &nbsp;...) et les espaces en trop."""
    texte = RE_BALISES.sub("", texte)
    texte = html_lib.unescape(texte).replace("\xa0", " ")
    return " ".join(texte.split())


def _premier(motif, bloc):
    """Retourne le premier groupe trouve par le motif, ou '' s'il n'y en a pas."""
    trouve = motif.search(bloc)
    return nettoyer(trouve.group(1)) if trouve else ""


def parser_produits(html, categorie=""):
    """Retourne une liste de Produit extraits d'une page de resultats."""
    produits = []
    balises = list(RE_FICHE.finditer(html))

    for i, balise in enumerate(balises):
        debut = balise.start()
        fin = balises[i + 1].start() if i + 1 < len(balises) else len(html)
        bloc = html[debut:fin]

        asin = RE_ASIN.search(balise.group(0))
        if not asin:
            continue

        lien = RE_LIEN.search(bloc)
        url = config.AMAZON_URL + html_lib.unescape(lien.group(1)).split("?")[0] if lien else ""

        produits.append(Produit(
            asin=asin.group(1),
            titre=_premier(RE_TITRE, bloc),
            prix=_premier(RE_PRIX, bloc),
            note=_premier(RE_NOTE, bloc),
            url=url,
            image_url=_premier(RE_IMAGE, bloc),
            categorie=categorie,
        ))

    return produits