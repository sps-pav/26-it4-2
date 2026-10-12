"""Testy herních pravidel (hra/logika.py).

Logika nepotřebuje Pygame ani okno, takže testy běží všude a jsou hotové
za zlomek sekundy.
"""
import random
import unittest

from hra.logika import StavHry, rychlost_padu, vyber_druh

# Druhy hub pro testy, stejné klíče, jaké mají řádky z tabulky druh_houby.
HRIB = {"id": 1, "nazev": "Hřib", "body": 10, "jedla": 1, "cetnost": 4}
MUCHOMURKA = {"id": 2, "nazev": "Muchomůrka", "body": 0, "jedla": 0, "cetnost": 1}


class TestStavHry(unittest.TestCase):
    """Počítání skóre a životů."""

    def test_jedla_houba_prida_body_krat_nasobic(self):
        stav = StavHry(zivoty=3, nasobic_bodu=2)
        stav.seber(HRIB)
        self.assertEqual(stav.skore, 20)
        self.assertEqual(stav.zivoty, 3)

    def test_jedovata_houba_ubere_zivot_a_body_neprida(self):
        stav = StavHry(zivoty=3)
        stav.seber(MUCHOMURKA)
        self.assertEqual(stav.skore, 0)
        self.assertEqual(stav.zivoty, 2)

    def test_hra_konci_po_ztrate_vsech_zivotu(self):
        stav = StavHry(zivoty=2)
        stav.seber(MUCHOMURKA)
        self.assertFalse(stav.je_konec)
        stav.seber(MUCHOMURKA)
        self.assertTrue(stav.je_konec)

    def test_sebrane_houby_se_pocitaji_podle_druhu(self):
        stav = StavHry(zivoty=3)
        stav.seber(HRIB)
        stav.seber(HRIB)
        stav.seber(MUCHOMURKA)
        self.assertEqual(stav.sebrane, {1: 2, 2: 1})


class TestNahodaARychlost(unittest.TestCase):
    """Výběr druhu houby a zrychlování."""

    def test_castejsi_druh_pada_casteji(self):
        nahoda = random.Random(42)          # pevné "semínko" = test dopadne vždy stejně
        vybrane = [vyber_druh([HRIB, MUCHOMURKA], nahoda)["id"] for _ in range(1000)]
        # Hřib má četnost 4, muchomůrka 1, takže hřibů má být zhruba 80 %.
        self.assertGreater(vybrane.count(1), 700)
        self.assertGreater(vybrane.count(2), 100)

    def test_rychlost_roste_kazdych_10_sekund(self):
        self.assertEqual(rychlost_padu(4.0, 0), 4.0)
        self.assertEqual(rychlost_padu(4.0, 9.9), 4.0)
        self.assertAlmostEqual(rychlost_padu(4.0, 10), 4.4)
        self.assertAlmostEqual(rychlost_padu(4.0, 35), 5.2)


if __name__ == "__main__":
    unittest.main()
