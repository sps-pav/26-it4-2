"""Testy webu přes testovacího klienta Flasku, bez spouštění serveru a prohlížeče."""
import os
import tempfile
import unittest

import app as web


class TestWeb(unittest.TestCase):
    def setUp(self):
        """Každý test má vlastní dočasný soubor s databází."""
        self.slozka = tempfile.TemporaryDirectory()
        web.app.config.update(TESTING=True, DATABAZE=os.path.join(self.slozka.name, "test.db"))
        self.klient = web.app.test_client()

    def tearDown(self):
        self.slozka.cleanup()

    def prihlas(self, email, heslo):
        return self.klient.post("/prihlaseni", data={"email": email, "heslo": heslo}, follow_redirects=True)

    def test_cely_nakup_od_kosiku_po_objednavku(self):
        self.prihlas("lucie@example.com", "heslo123")
        self.klient.post("/kosik/pridat", data={"produkt_id": 7, "mnozstvi": 2})
        odpoved = self.klient.post(
            "/objednat",
            data={"adresa": "Lucie Dvořáková, Polní 8, 266 01 Beroun", "zpusob_platby": "dobirka"},
            follow_redirects=True,
        )
        self.assertIn("Objednávka č. 5 je přijatá", odpoved.text)
        self.assertIn("Echeveria", odpoved.text)
        self.assertIn("Košík (0)", odpoved.text)            # košík se po objednání vyprázdnil

    def test_objednat_bez_prihlaseni_presmeruje_na_prihlaseni(self):
        odpoved = self.klient.get("/objednat", follow_redirects=True)
        self.assertIn("Nejdřív se přihlas", odpoved.text)

    def test_administrace_jen_pro_admina(self):
        self.prihlas("jana@example.com", "heslo123")
        self.assertEqual(self.klient.get("/admin").status_code, 403)
        self.klient.get("/odhlaseni")
        self.prihlas("admin@zelenykout.example", "admin123")
        self.assertEqual(self.klient.get("/admin").status_code, 200)

    def test_cizi_objednavka_neni_videt(self):
        self.prihlas("petr@example.com", "heslo123")
        self.assertEqual(self.klient.get("/objednavka/1").status_code, 404)    # č. 1 patří Janě
        self.assertEqual(self.klient.get("/objednavka/3").status_code, 200)


if __name__ == "__main__":
    unittest.main()
