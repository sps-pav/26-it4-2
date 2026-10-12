"""Testy práce s databází (db.py).

Každý test dostane novou prázdnou databázi v paměti (":memory:") vytvořenou
ze schema.sql a data.sql. Skutečný soubor houbar.db se testy nikdy nezmění.
"""
import sqlite3
import unittest

import db


class TestDatabaze(unittest.TestCase):
    def setUp(self):
        """Před každým testem: čerstvá databáze se vzorovými daty."""
        self.spojeni = db.pripoj(":memory:")
        db.vytvor_databazi(self.spojeni)

    def tearDown(self):
        """Po každém testu připojení zavřeme."""
        self.spojeni.close()

    # účty
    def test_registrace_a_prihlaseni(self):
        db.registruj_hrace(self.spojeni, "novacek", "tajneheslo")
        hrac = db.prihlas_hrace(self.spojeni, "novacek", "tajneheslo")
        self.assertEqual(hrac["jmeno"], "novacek")
        self.assertIsNone(db.prihlas_hrace(self.spojeni, "novacek", "spatne"))

    def test_heslo_se_neuklada_citelne(self):
        db.registruj_hrace(self.spojeni, "novacek", "tajneheslo")
        radek = self.spojeni.execute("SELECT heslo_hash FROM hrac WHERE jmeno = 'novacek'").fetchone()
        self.assertNotIn("tajneheslo", radek["heslo_hash"])

    def test_registrace_odmitne_obsazene_jmeno_a_kratke_heslo(self):
        with self.assertRaises(ValueError):
            db.registruj_hrace(self.spojeni, "pepa", "tajneheslo")      # pepa je ve vzorových datech
        with self.assertRaises(ValueError):
            db.registruj_hrace(self.spojeni, "novacek", "123")

    # partie
    def test_ulozena_partie_se_objevi_v_zebricku(self):
        hrac_id = db.registruj_hrace(self.spojeni, "rekordman", "tajneheslo")
        db.uloz_partii(self.spojeni, hrac_id, obtiznost_id=2, skore=999, trvani_s=60, sebrane={1: 30, 4: 1})

        prvni = db.zebricek(self.spojeni, limit=1)[0]
        self.assertEqual((prvni["jmeno"], prvni["skore"]), ("rekordman", 999))

        houby = {h["nazev"]: h["celkem"] for h in db.statistika_hub(self.spojeni, hrac_id)}
        self.assertEqual(houby, {"Hřib smrkový": 30, "Muchomůrka červená": 1})

    def test_partie_s_neexistujicim_druhem_se_neulozi_vubec(self):
        """Transakce: když selže zápis hub, nesmí v DB zůstat ani samotná partie."""
        pred = self.spojeni.execute("SELECT COUNT(*) FROM partie").fetchone()[0]
        with self.assertRaises(sqlite3.IntegrityError):
            db.uloz_partii(self.spojeni, 1, 2, skore=50, trvani_s=30, sebrane={999: 1})
        po = self.spojeni.execute("SELECT COUNT(*) FROM partie").fetchone()[0]
        self.assertEqual(pred, po)

    def test_zebricek_filtruje_podle_obtiznosti_a_jmena(self):
        tezka = db.zebricek(self.spojeni, obtiznost_id=3)
        self.assertEqual([r["obtiznost"] for r in tezka], ["Těžká"])
        self.assertEqual({r["jmeno"] for r in db.zebricek(self.spojeni, hledat="ani")}, {"anicka"})

    def test_smazat_jde_jen_vlastni_partii(self):
        self.assertFalse(db.smaz_partii(self.spojeni, partie_id=3, hrac_id=1))   # partie 3 patří hráči 2
        self.assertTrue(db.smaz_partii(self.spojeni, partie_id=1, hrac_id=1))
        zbylo = self.spojeni.execute("SELECT COUNT(*) FROM partie_houba WHERE partie_id = 1").fetchone()[0]
        self.assertEqual(zbylo, 0)                                              # CASCADE smazal i houby


if __name__ == "__main__":
    unittest.main()
