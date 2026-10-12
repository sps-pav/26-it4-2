"""Testy nad databází: objednávky, sklad a administrace produktů.

Každý test dostane novou databázi v paměti (":memory:") vytvořenou ze
schema.sql a data.sql. Skutečný soubor eshop.db se testy nikdy nezmění.

Ve vzorových datech: uživatel 4 = Lucie (zatím bez objednávky),
produkt 1 = Monstera (349 Kč, 12 ks), produkt 5 = Orchidej (319 Kč, 4 ks).
"""
import unittest

import db
import katalog
import objednavky

ADRESA = "Lucie Dvořáková, Polní 8, 266 01 Beroun"


class TestObjednavky(unittest.TestCase):
    def setUp(self):
        """Před každým testem: čerstvá databáze se vzorovými daty."""
        self.spojeni = db.pripoj(":memory:")
        db.vytvor_databazi(self.spojeni)

    def tearDown(self):
        """Po každém testu připojení zavřeme."""
        self.spojeni.close()

    def sklad(self, produkt_id):
        """Pomocná funkce: kolik kusů produktu je teď skladem."""
        return self.spojeni.execute("SELECT sklad FROM produkt WHERE id = ?", (produkt_id,)).fetchone()[0]

    def pocet_objednavek(self):
        return self.spojeni.execute("SELECT COUNT(*) FROM objednavka").fetchone()[0]

    def test_objednavka_odecte_sklad_a_spocita_cenu(self):
        cislo = objednavky.vytvor_objednavku(self.spojeni, 4, {"1": 2, "5": 1}, ADRESA, "dobirka")

        self.assertEqual(self.sklad(1), 10)
        self.assertEqual(self.sklad(5), 3)
        objednavka, polozky = objednavky.najdi_objednavku(self.spojeni, cislo)
        self.assertEqual(objednavka["celkem_kc"], 2 * 349 + 319)
        self.assertEqual(objednavka["stav"], "nová")
        self.assertEqual(len(polozky), 2)

    def test_nedostatek_zbozi_zrusi_celou_objednavku(self):
        """Transakce: Monstera je skladem, Orchideje jsou jen 4. Nesmí se uložit ani půlka objednávky."""
        pred = self.pocet_objednavek()
        with self.assertRaises(ValueError):
            objednavky.vytvor_objednavku(self.spojeni, 4, {"1": 2, "5": 5}, ADRESA, "dobirka")

        self.assertEqual(self.pocet_objednavek(), pred)     # objednávka nevznikla
        self.assertEqual(self.sklad(1), 12)                 # Monstera se vrátila na sklad
        self.assertEqual(self.sklad(5), 4)

    def test_neplatne_udaje_objednavku_nevytvori(self):
        for kosik, adresa, platba in [({}, ADRESA, "dobirka"), ({"1": 1}, "x", "dobirka"), ({"1": 1}, ADRESA, "bitcoin")]:
            with self.assertRaises(ValueError):
                objednavky.vytvor_objednavku(self.spojeni, 4, kosik, adresa, platba)

    def test_zdrazeni_nezmeni_starou_objednavku(self):
        cislo = objednavky.vytvor_objednavku(self.spojeni, 4, {"1": 1}, ADRESA, "prevod")
        self.spojeni.execute("UPDATE produkt SET cena_kc = 999 WHERE id = 1")

        objednavka, _ = objednavky.najdi_objednavku(self.spojeni, cislo)
        self.assertEqual(objednavka["celkem_kc"], 349)

    def test_zruseni_vrati_zbozi_na_sklad_a_dal_uz_nejde_menit(self):
        cislo = objednavky.vytvor_objednavku(self.spojeni, 4, {"1": 3, "5": 2}, ADRESA, "dobirka")
        objednavky.zmen_stav(self.spojeni, cislo, objednavky.STAV_ZRUSENA)

        self.assertEqual((self.sklad(1), self.sklad(5)), (12, 4))
        with self.assertRaises(ValueError):
            objednavky.zmen_stav(self.spojeni, cislo, objednavky.STAV_NOVA)

    def test_prodany_produkt_nejde_smazat_jen_skryt(self):
        with self.assertRaises(ValueError):
            katalog.smaz_produkt(self.spojeni, 1)           # Monstera je v objednávce č. 1
        katalog.nastav_aktivni(self.spojeni, 1, False)
        nazvy = [p["nazev"] for p in katalog.hledej_produkty(self.spojeni)]
        self.assertNotIn("Monstera deliciosa", nazvy)

    def test_hledani_a_filtr_kategorie(self):
        nalezeno = [p["nazev"] for p in katalog.hledej_produkty(self.spojeni, hledat="kaktus")]
        self.assertEqual(nalezeno, ["Kaktus Mammillaria"])
        sukulenty = katalog.hledej_produkty(self.spojeni, kategorie_id=4, razeni="cena")
        self.assertEqual([p["nazev"] for p in sukulenty], ["Echeveria", "Kaktus Mammillaria", "Aloe vera"])


if __name__ == "__main__":
    unittest.main()
