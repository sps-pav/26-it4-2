# Čtyři základní testy. Dva zkoušejí databázové objednávky.
import app as obchod
import pytest

# Každý test dostane vlastní prázdnou databázi, aby testy nepoškodily obchod.
@pytest.fixture
def priprava(tmp_path, monkeypatch):
    monkeypatch.setattr(obchod, 'DB_PATH', tmp_path / 'test.db')
    obchod.app.config.update(TESTING=True)
    obchod.priprav_db()
    return obchod.app.test_client()

# Test 1: úvodní stránka se zobrazí.
def test_uvod(priprava):
    odpoved = priprava.get('/')
    assert odpoved.status_code == 200
    assert 'KopačkyShop'.encode() in odpoved.data

# Test 2: vyhledávání najde kopačky podle názvu.
def test_hledani(priprava):
    odpoved = priprava.get('/produkty?hledat=Speed')
    assert b'Speed Pro' in odpoved.data
    assert b'Indoor Star' not in odpoved.data

# Test 3: správná objednávka se uloží a sníží sklad o jeden kus.
def test_objednavka_snizi_sklad(priprava):
    with obchod.db() as spojeni:
        puvodni = spojeni.execute('SELECT sklad FROM produkt_velikost WHERE produkt_id=1 AND velikost_id=1').fetchone()[0]
        uid = spojeni.execute('SELECT id FROM uzivatele WHERE email=?', ('zakaznik@demo.cz',)).fetchone()[0]
    cislo = obchod.vytvor_objednavku(uid, {'1:1': 1}, 'dobirka', 'kuryr')
    with obchod.db() as spojeni:
        novy = spojeni.execute('SELECT sklad FROM produkt_velikost WHERE produkt_id=1 AND velikost_id=1').fetchone()[0]
        polozky = spojeni.execute('SELECT COUNT(*) FROM polozky_objednavky WHERE objednavka_id=?', (cislo,)).fetchone()[0]
    assert novy == puvodni - 1
    assert polozky == 1

# Test 4: při nedostatku skladu se celá transakce vrátí zpět.
def test_objednavka_rollback(priprava):
    with obchod.db() as spojeni:
        pred = spojeni.execute('SELECT COUNT(*) FROM objednavky').fetchone()[0]
        uid = spojeni.execute('SELECT id FROM uzivatele WHERE email=?', ('zakaznik@demo.cz',)).fetchone()[0]
    with pytest.raises(ValueError):
        obchod.vytvor_objednavku(uid, {'1:1': 9999}, 'dobirka', 'kuryr')
    with obchod.db() as spojeni:
        potom = spojeni.execute('SELECT COUNT(*) FROM objednavky').fetchone()[0]
    assert pred == potom
