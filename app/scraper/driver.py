"""Driver : pilote Chrome avec Selenium et recupere le HTML des pages."""
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import config


def est_captcha(html):
    texte = html.lower()
    return (
        "validatecaptcha" in texte
        or "enter the characters you see" in texte
        or "saisissez les caract" in texte
    )


def page_valide(html):
    """Une vraie page de resultats contient des fiches produit et pas de captcha."""
    return "s-search-result" in html and not est_captcha(html)


class DriverChrome:
    def __init__(self):
        self.driver = None

    def demarrer(self):
        """Lance Chrome."""
        options = Options()
        if config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1366,768")
        options.add_argument("--lang=fr-FR")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

    def pause(self):
        """Pause aleatoire entre deux pages."""
        mini, maxi = config.DELAI_ENTRE_REQUETES
        time.sleep(random.uniform(mini, maxi))

    def _attendre_page_valide(self):
        """Attend une vraie page de resultats (laisse le temps de resoudre un captcha)."""
        debut = time.time()
        message_affiche = False
        while time.time() - debut < config.ATTENTE_PAGE:
            html = self.driver.page_source
            if page_valide(html):
                return html
            if est_captcha(html) and not message_affiche:
                print("[driver] Captcha detecte : resous-le dans la fenetre Chrome...")
                message_affiche = True
            time.sleep(2)
        return None

    def get(self, url):
        """Retourne le HTML de la page, ou None si elle reste bloquee."""
        if self.driver is None:
            self.demarrer()
        for essai in range(1, config.NB_TENTATIVES + 1):
            self.driver.get(url)
            html = self._attendre_page_valide()
            if html:
                return html
            print(f"[driver] essai {essai} : page non valide")
            self.pause()
        return None

    def telecharger_image(self, url, chemin):
        """Ouvre l'image dans Chrome et l'enregistre (PNG). Retourne True si reussi."""
        try:
            self.driver.get(url)
            image = self.driver.find_element(By.TAG_NAME, "img")
            chemin.write_bytes(image.screenshot_as_png)
            return True
        except Exception as erreur:
            print(f"[driver] image non telechargee ({erreur})")
            return False

    def fermer(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None