"""Testy košíku (kosik.py): čisté funkce bez databáze a bez Flasku."""
import unittest

import kosik


class TestKosik(unittest.TestCase):
    def test_pridani_stejneho_produktu_scita_mnozstvi(self):
        obsah = kosik.pridej({}, 7, 2)
        obsah = kosik.pridej(obsah, 7, 1)
        self.assertEqual(obsah, {"7": 3})
        self.assertEqual(kosik.pocet_kusu(obsah), 3)

    def test_nastaveni_nuly_produkt_odebere(self):
        obsah = kosik.nastav({"7": 3, "9": 1}, 7, 0)
        self.assertEqual(obsah, {"9": 1})

    def test_nesmyslne_mnozstvi_je_odmitnuto(self):
        for spatne in ("abc", "-1", "1000", None, "2.5"):
            with self.assertRaises(ValueError, msg=f"prošlo množství {spatne!r}"):
                kosik.nastav({}, 7, spatne)

    def test_celkova_cena_a_preskoceni_zmizeleho_produktu(self):
        produkty = {7: {"nazev": "Echeveria", "cena_kc": 79}, 9: {"nazev": "Aloe vera", "cena_kc": 149}}
        obsah = {"7": 3, "9": 1, "404": 5}           # produkt 404 už v nabídce není
        polozky, celkem = kosik.sestav_polozky(obsah, produkty)
        self.assertEqual(len(polozky), 2)
        self.assertEqual(celkem, 3 * 79 + 149)


if __name__ == "__main__":
    unittest.main()
