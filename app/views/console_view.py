"""Vue console : tout ce qui s'affiche dans le terminal."""


def afficher_message(message):
    print(message)


def afficher_titre(titre):
    print("\n" + "=" * 50)
    print(titre)
    print("=" * 50)


def afficher_produits(produits, limite=10):
    """Affiche un apercu des premiers produits."""
    if not produits:
        print("Aucun produit a afficher.")
        return
    for p in produits[:limite]:
        print(f"{p.prix:>10} | {p.note[:12]:<12} | {p.titre[:55]}")
    if len(produits) > limite:
        print(f"... et {len(produits) - limite} autres produits")


def afficher_resume(nb_scrapes, nb_en_base, chemin_csv, dossier_images):
    afficher_titre("Resume")
    print(f"Produits scrapes cette fois : {nb_scrapes}")
    print(f"Produits en base (SQLite)   : {nb_en_base}")
    print(f"Fichier CSV                 : {chemin_csv}")
    print(f"Dossier des images          : {dossier_images}")