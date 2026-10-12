"""Herní pravidla bez Pygame.

Tady je všechno, co se dá spočítat bez okna a bez kreslení: výběr druhu houby,
počítání skóre a životů, zrychlování. Díky tomu jdou tyto funkce snadno
automaticky testovat (viz tests/test_logika.py).
"""
import random

from hra import nastaveni as n


def vyber_druh(druhy, nahoda=random):
    """Náhodně vybere druh houby. Druh s vyšší četností padá častěji.

    druhy:  seznam záznamů z tabulky druh_houby (musí mít klíč "cetnost")
    nahoda: generátor náhody; v testech sem dáváme random.Random(cislo),
            aby byl výsledek pokaždé stejný
    """
    vahy = [druh["cetnost"] for druh in druhy]
    return nahoda.choices(druhy, weights=vahy, k=1)[0]


def rychlost_padu(zakladni_rychlost, uplynulo_s):
    """Vrátí rychlost padání hub. Každých 10 sekund se o kousek zvýší."""
    stupen = int(uplynulo_s) // 10
    return zakladni_rychlost * (1 + n.ZRYCHLENI_ZA_10_S * stupen)


class StavHry:
    """Pamatuje si průběh jedné partie: skóre, životy a kolik čeho hráč sebral."""

    def __init__(self, zivoty, nasobic_bodu=1):
        self.skore = 0
        self.zivoty = zivoty
        self.nasobic_bodu = nasobic_bodu
        self.sebrane = {}            # slovník {id druhu houby: počet sebraných kusů}

    def seber(self, druh):
        """Hráč chytil houbu: jedlá přidá body, jedovatá ubere život."""
        self.sebrane[druh["id"]] = self.sebrane.get(druh["id"], 0) + 1
        if druh["jedla"]:
            self.skore += druh["body"] * self.nasobic_bodu
        else:
            self.zivoty -= 1

    @property
    def je_konec(self):
        """True, pokud hráči došly životy."""
        return self.zivoty <= 0
