# Flask zobrazí HTML stránky a propojí je s databází.
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
# SQLite je databáze, která nepotřebuje zvláštní server.
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import DB_PATH

app = Flask(__name__)
# V reálném provozu nastav vlastní tajný klíč přes proměnnou prostředí.
import os
app.secret_key = os.environ.get('SECRET_KEY', 'skolni-projekt-zmenit-klic')

# Každé spojení zapne cizí klíče a umožní přístup ke sloupcům podle jména.
def db():
    spojeni = sqlite3.connect(DB_PATH)
    spojeni.row_factory = sqlite3.Row
    spojeni.execute('PRAGMA foreign_keys = ON')
    return spojeni

# Při prvním spuštění připravíme tabulky a vzorové kopačky.
def priprav_db():
    with db() as spojeni:
        spojeni.executescript((DB_PATH.parent / 'databaze/schema.sql').read_text(encoding='utf-8'))
        spojeni.executescript((DB_PATH.parent / 'databaze/data.sql').read_text(encoding='utf-8'))
        # Založíme ukázkové účty s bezpečně zahashovaným heslem.
        if not spojeni.execute('SELECT 1 FROM uzivatele LIMIT 1').fetchone():
            pro_roli = [('Zakaznik', 'zakaznik@demo.cz', 'zakaznik'), ('Administrator', 'admin@demo.cz', 'admin'), ('Skladnik', 'sklad@demo.cz', 'spravce_skladu')]
            for jmeno, email, role in pro_roli:
                role_id = spojeni.execute('SELECT id FROM role WHERE nazev=?', (role,)).fetchone()['id']
                spojeni.execute('INSERT INTO uzivatele(jmeno,email,heslo,role_id) VALUES(?,?,?,?)', (jmeno, email, generate_password_hash('demo1234'), role_id))
            # Tři vzorové objednávky doplňují školní ukázková data.
            zakaznik_id = spojeni.execute('SELECT id FROM uzivatele WHERE email=?', ('zakaznik@demo.cz',)).fetchone()['id']
            for produkt_id, velikost_id in [(1,1),(2,2),(3,3)]:
                cena = spojeni.execute('SELECT cena FROM produkty WHERE id=?', (produkt_id,)).fetchone()['cena']
                spojeni.execute("INSERT INTO objednavky(uzivatel_id,stav,platba,doprava) VALUES(?,'odeslana','dobirka','kuryr')", (zakaznik_id,))
                oid = spojeni.execute('SELECT last_insert_rowid()').fetchone()[0]
                spojeni.execute('INSERT INTO polozky_objednavky(objednavka_id,produkt_id,velikost_id,mnozstvi,cena_za_kus) VALUES(?,?,?,?,?)', (oid,produkt_id,velikost_id,1,cena))

# V šablonách bude vždy přístupné jméno a role přihlášeného uživatele.
@app.context_processor
def uzivatel_sablony():
    return {'prihlaseny': session.get('jmeno'), 'je_admin': session.get('role') == 'admin'}

# Tento obal zastaví nepřihlášeného zákazníka.
def vyzaduje_login(f):
    @wraps(f)
    def funkce(*args, **kwargs):
        if not session.get('uid'):
            flash('Nejdřív se přihlas.')
            return redirect(url_for('prihlaseni'))
        return f(*args, **kwargs)
    return funkce

# Tenhle obal navíc hlídá, aby administraci neotevřel zákazník.
def vyzaduje_admin(f):
    @wraps(f)
    def funkce(*args, **kwargs):
        if session.get('role') != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return funkce

# Pomocná funkce převede číslo z formuláře bezpečně na celé číslo.
def cele_cislo(hodnota, vychozi=0):
    try:
        return int(hodnota)
    except (ValueError, TypeError):
        return vychozi

# Košík je uložený v relaci prohlížeče, aby zůstal po přechodu mezi stránkami.
def kosik_data():
    return dict(session.get('kosik', {}))

# Spočítáme položky košíku podle aktuální ceny a dostupných velikostí.
def polozky_kosiku():
    vysledek = []
    with db() as spojeni:
        for klic, pocet in kosik_data().items():
            pid, vid = map(int, klic.split(':'))
            produkt = spojeni.execute('''SELECT p.id, p.nazev, p.cena, v.cislo AS velikost, pv.sklad
                FROM produkty p JOIN produkt_velikost pv ON pv.produkt_id=p.id
                JOIN velikosti v ON v.id=pv.velikost_id
                WHERE p.id=? AND v.id=? AND p.aktivni=1''', (pid, vid)).fetchone()
            if produkt and pocet > 0:
                vysledek.append({'klic':klic,'nazev':produkt['nazev'],'cena':produkt['cena'],
                                 'velikost':produkt['velikost'],'mnozstvi':pocet,'sklad':produkt['sklad'],
                                 'soucet':produkt['cena'] * pocet})
    return vysledek

# Úvodní stránka ukáže tři produkty.
@app.route('/')
def index():
    with db() as spojeni:
        produkty = spojeni.execute('SELECT * FROM produkty WHERE aktivni=1 ORDER BY id DESC LIMIT 6').fetchall()
    return render_template('index.html', produkty=produkty)

# Katalog má filtr, hledání a řazení; hodnoty jdou do SQL jen pomocí parametrů.
# Tato stránka zobrazuje všechny kopačky.
@app.route('/produkty')
def produkty():

    # Získáme text, který zákazník napsal do hledání.
    hledat = request.args.get('hledat', '').strip()

    # Zjistíme, kterou kategorii zákazník vybral.
    kategorie = cele_cislo(request.args.get('kategorie'))

    # Zjistíme, jak chce produkty seřadit.
    razeni = request.args.get('razeni', 'nazev')

    # Připravíme možnosti řazení.
    poradi = {
        'nazev': 'p.nazev ASC',
        'nejlevnejsi': 'p.cena ASC',
        'nejdrazsi': 'p.cena DESC'
    }

    # Hledáme podle názvu, značky, popisu nebo kategorie.
    sql = '''
        SELECT p.*, k.nazev AS kategorie
        FROM produkty p
        JOIN kategorie k ON p.kategorie_id = k.id
        WHERE p.aktivni = 1
        AND (
            p.nazev LIKE ?
            OR p.znacka LIKE ?
            OR p.popis LIKE ?
            OR k.nazev LIKE ?
        )
    '''

    # Procenta znamenají, že hledaný text může být i část slova.
    text = '%' + hledat + '%'

    # Stejný text hledáme ve čtyřech sloupcích.
    parametry = [text, text, text, text]

    # Pokud zákazník vybral kategorii, omezíme výsledky.
    if kategorie > 0:
        sql += ' AND k.id = ?'
        parametry.append(kategorie)

    # Přidáme bezpečně zvolený způsob řazení.
    sql += ' ORDER BY ' + poradi.get(razeni, poradi['nazev'])

    # Otevřeme databázi.
    with db() as spojeni:

        # Načteme kopačky, které odpovídají hledání.
        seznam = spojeni.execute(sql, parametry).fetchall()

        # Načteme kategorie do výběrového políčka.
        kategorie_list = spojeni.execute(
            'SELECT * FROM kategorie'
        ).fetchall()

    # Výsledky pošleme do HTML stránky.
    return render_template(
        'produkty.html',
        produkty=seznam,
        kategorie_list=kategorie_list,
        hledat=hledat,
        zvolena_kategorie=kategorie,
        razeni=razeni
    )

# Detail ukáže popis a dostupné velikosti vybraných kopaček.
@app.route('/produkt/<int:pid>')
def detail(pid):
    with db() as spojeni:
        produkt = spojeni.execute('SELECT * FROM produkty WHERE id=? AND aktivni=1', (pid,)).fetchone()
        velikosti = spojeni.execute('''SELECT v.id, v.cislo, pv.sklad FROM produkt_velikost pv
            JOIN velikosti v ON v.id=pv.velikost_id WHERE pv.produkt_id=? ORDER BY v.cislo''', (pid,)).fetchall()
    if not produkt:
        abort(404)
    return render_template('detail.html', produkt=produkt, velikosti=velikosti)

# Registrace kontroluje jméno, e-mail a minimální délku hesla.
@app.route('/registrace', methods=['GET','POST'])
def registrace():
    if request.method == 'POST':
        jmeno = request.form.get('jmeno','').strip()
        email = request.form.get('email','').strip().lower()
        heslo = request.form.get('heslo','')
        if not jmeno or '@' not in email or len(heslo) < 6:
            flash('Vyplň jméno, platný e-mail a heslo alespoň 6 znaků.')
        else:
            try:
                with db() as spojeni:
                    spojeni.execute('INSERT INTO uzivatele(jmeno,email,heslo,role_id) VALUES(?,?,?,1)',
                                   (jmeno,email,generate_password_hash(heslo)))
                flash('Účet vytvořen, můžeš se přihlásit.')
                return redirect(url_for('prihlaseni'))
            except sqlite3.IntegrityError:
                flash('Tento e-mail už někdo používá.')
    return render_template('registrace.html')

# Při přihlášení nikdy nesrovnáváme hesla jako obyčejný text.
@app.route('/prihlaseni', methods=['GET','POST'])
def prihlaseni():
    if request.method == 'POST':
        with db() as spojeni:
            u = spojeni.execute('''SELECT u.*, r.nazev AS role FROM uzivatele u
              JOIN role r ON r.id=u.role_id WHERE u.email=?''', (request.form.get('email','').strip().lower(),)).fetchone()
        if not u or not check_password_hash(u['heslo'], request.form.get('heslo','')):
            flash('Nesprávný e-mail nebo heslo.')
        else:
            kosik = kosik_data()
            session.clear()
            session.update(uid=u['id'], jmeno=u['jmeno'], role=u['role'], kosik=kosik)
            return redirect(url_for('index'))
    return render_template('prihlaseni.html')

# Odhlášení smaže přihlašovací údaje, ale nechá zákazníkovi košík.
@app.route('/odhlaseni', methods=['POST'])
def odhlaseni():
    kosik = kosik_data()
    session.clear()
    session['kosik'] = kosik
    return redirect(url_for('index'))

# Produkt vložíme do košíku jen při existující velikosti a dostatečném skladu.
@app.route('/do-kosiku/<int:pid>', methods=['POST'])
def pridat_kosik(pid):
    vid = cele_cislo(request.form.get('velikost'))
    pocet = cele_cislo(request.form.get('mnozstvi'))
    with db() as spojeni:
        zaznam = spojeni.execute('''SELECT pv.sklad FROM produkt_velikost pv JOIN produkty p ON p.id=pv.produkt_id
            WHERE pv.produkt_id=? AND pv.velikost_id=? AND p.aktivni=1''', (pid,vid)).fetchone()
    klic = f'{pid}:{vid}'
    kosik = kosik_data()
    if not zaznam or pocet < 1 or kosik.get(klic,0)+pocet > zaznam['sklad']:
        flash('Neplatná velikost, množství nebo nedostatek kusů.')
    else:
        kosik[klic] = kosik.get(klic,0) + pocet
        session['kosik'] = kosik
        flash('Kopačky jsou v košíku.')
    return redirect(url_for('kosik'))

# Tady košík pouze zobrazíme.
@app.route('/kosik')
def kosik():
    polozky = polozky_kosiku()
    return render_template('kosik.html', polozky=polozky, celkem=sum(x['soucet'] for x in polozky))

# Změna množství: nula znamená odebrat položku.
@app.route('/kosik/upravit', methods=['POST'])
def upravit_kosik():
    klic = request.form.get('klic','')
    pocet = cele_cislo(request.form.get('mnozstvi'), -1)
    kosik = kosik_data()
    if klic in kosik and pocet >= 0:
        if pocet == 0:
            kosik.pop(klic)
        else:
            kosik[klic] = pocet
        session['kosik'] = kosik
    else:
        flash('Zadej platné množství.')
    return redirect(url_for('kosik'))

# Objednávka je JEDNA transakce. Když něco nevyjde, vrátíme všechny změny.
def vytvor_objednavku(uid, kosik, platba, doprava):
    if not kosik or platba not in ('dobirka','prevod') or doprava not in ('kuryr','vydejni_misto'):
        raise ValueError('Zkontroluj košík, platbu a dopravu.')
    spojeni = db()
    try:
        spojeni.execute('BEGIN IMMEDIATE')  # Zamkneme zápis, ať se neprodá poslední kus dvakrát.
        spojeni.execute('INSERT INTO objednavky(uzivatel_id,platba,doprava) VALUES(?,?,?)', (uid,platba,doprava))
        oid = spojeni.execute('SELECT last_insert_rowid()').fetchone()[0]
        for klic, pocet in kosik.items():
            try:
                pid, vid = map(int, klic.split(':'))
            except (ValueError, AttributeError):
                raise ValueError('Košík obsahuje neplatnou položku.')
            if not isinstance(pocet, int) or pocet < 1:
                raise ValueError('Množství musí být větší než nula.')
            produkt = spojeni.execute('''SELECT p.cena, pv.sklad FROM produkty p JOIN produkt_velikost pv
                ON pv.produkt_id=p.id WHERE p.id=? AND pv.velikost_id=? AND p.aktivni=1''', (pid,vid)).fetchone()
            if not produkt or produkt['sklad'] < pocet:
                raise ValueError('Některé kopačky už nejsou v požadovaném množství skladem.')
            spojeni.execute('''UPDATE produkt_velikost SET sklad=sklad-?
                WHERE produkt_id=? AND velikost_id=?''', (pocet,pid,vid))
            spojeni.execute('''INSERT INTO polozky_objednavky
                (objednavka_id,produkt_id,velikost_id,mnozstvi,cena_za_kus)
                VALUES(?,?,?,?,?)''', (oid,pid,vid,pocet,produkt['cena']))
        spojeni.commit()  # Všechno dopadlo dobře, změny uložíme.
        return oid
    except (ValueError, sqlite3.Error):
        spojeni.rollback()  # Při chybě vrátíme sklad i objednávku do původního stavu.
        raise
    finally:
        spojeni.close()

# Formulář objednávky ukazuje součet a volbu simulované platby.
@app.route('/objednat', methods=['GET','POST'])
@vyzaduje_login
def objednat():
    polozky = polozky_kosiku()
    if not polozky:
        flash('Košík je prázdný.')
        return redirect(url_for('kosik'))
    if request.method == 'POST':
        try:
            oid = vytvor_objednavku(session['uid'], kosik_data(), request.form.get('platba'), request.form.get('doprava'))
            session['kosik'] = {}
            flash(f'Objednávka číslo {oid} byla vytvořena. Platba je jen ukázková.')
            return redirect(url_for('moje_objednavky'))
        except (ValueError, sqlite3.Error) as chyba:
            flash(str(chyba) if isinstance(chyba, ValueError) else 'Databáze teď objednávku nemůže uložit.')
    return render_template('objednat.html', polozky=polozky, celkem=sum(x['soucet'] for x in polozky))

# Zákazník vidí jen svoje objednávky, nikdy objednávky ostatních.

@app.route('/moje-objednavky')
@vyzaduje_login
def moje_objednavky():
    with db() as spojeni:
        objednavky = spojeni.execute('SELECT * FROM prehled_objednavek WHERE uzivatel_id=? ORDER BY id DESC', (session['uid'],)).fetchall()
        polozky = spojeni.execute('''SELECT po.objednavka_id, p.nazev, v.cislo AS velikost, po.mnozstvi, po.cena_za_kus
            FROM polozky_objednavky po JOIN produkty p ON p.id=po.produkt_id
            JOIN velikosti v ON v.id=po.velikost_id JOIN objednavky o ON o.id=po.objednavka_id
            WHERE o.uzivatel_id=?''', (session['uid'],)).fetchall()
    return render_template('objednavky.html', objednavky=objednavky, polozky=polozky)

# Tato část umožní zákazníkovi zrušit jeho objednávku.
@app.route('/zrusit-objednavku/<int:oid>', methods=['POST'])
@vyzaduje_login
def zrusit_objednavku(oid):

    # Připojíme se k databázi.
    spojeni = db()

    try:
        # Zamkneme zápis, aby objednávku nikdo neměnil zároveň s námi.
        spojeni.execute('BEGIN IMMEDIATE')

        # Najdeme objednávku, ale pouze pokud patří přihlášenému zákazníkovi.
        objednavka = spojeni.execute(
            'SELECT stav FROM objednavky WHERE id=? AND uzivatel_id=?',
            (oid, session['uid'])
        ).fetchone()

        # Cizí nebo neexistující objednávku nepovolíme zrušit.
        if objednavka is None:
            flash('Tato objednávka neexistuje.')
            return redirect(url_for('moje_objednavky'))

        # Zrušit může zákazník jen objednávku ve stavu "nova".
        if objednavka['stav'] != 'nova':
            flash('Tuto objednávku už nejde zrušit.')
            return redirect(url_for('moje_objednavky'))

        # Načteme všechny kopačky z dané objednávky.
        polozky = spojeni.execute(
            'SELECT * FROM polozky_objednavky WHERE objednavka_id=?',
            (oid,)
        ).fetchall()

        # Projdeme všechny objednané kopačky.
        for polozka in polozky:

            # Vrátíme objednané kusy a velikosti zpět na sklad.
            spojeni.execute(
                '''UPDATE produkt_velikost
                   SET sklad = sklad + ?
                   WHERE produkt_id=? AND velikost_id=?''',
                (
                    polozka['mnozstvi'],
                    polozka['produkt_id'],
                    polozka['velikost_id']
                )
            )

        # Změníme stav objednávky na "zrusena".
        spojeni.execute(
            "UPDATE objednavky SET stav='zrusena' WHERE id=?",
            (oid,)
        )

        # Uložíme změnu objednávky i skladu najednou.
        spojeni.commit()

        # Vypíšeme zákazníkovi zprávu.
        flash('Objednávka byla úspěšně zrušena.')

    except sqlite3.Error:

        # Pokud se něco pokazí, vrátíme všechny databázové změny.
        spojeni.rollback()
        flash('Objednávku se nepodařilo zrušit.')

    finally:

        # Nakonec vždy zavřeme připojení k databázi.
        spojeni.close()

    # Vrátíme zákazníka na přehled jeho objednávek.
    return redirect(url_for('moje_objednavky'))

# Admin uvidí produkty, objednávky a dvě statistiky z databáze.
@app.route('/admin')
@vyzaduje_admin
def admin():
    with db() as spojeni:
        produkty = spojeni.execute('SELECT * FROM produkty ORDER BY id').fetchall()
        objednavky = spojeni.execute('''SELECT v.*, u.email FROM prehled_objednavek v
            JOIN uzivatele u ON u.id=v.uzivatel_id ORDER BY v.id DESC''').fetchall()
        trzby = spojeni.execute("SELECT COALESCE(SUM(celkem),0) FROM prehled_objednavek WHERE stav!='zrusena'").fetchone()[0]
        prodeje = spojeni.execute('SELECT COALESCE(SUM(mnozstvi),0) FROM polozky_objednavky').fetchone()[0]
        sklady = spojeni.execute('SELECT * FROM velikosti ORDER BY cislo').fetchall()
        kategorie = spojeni.execute('SELECT * FROM kategorie').fetchall()
        statistika = spojeni.execute('''SELECT p.nazev, COALESCE(SUM(po.mnozstvi),0) AS kusy
            FROM produkty p LEFT JOIN polozky_objednavky po ON po.produkt_id=p.id
            GROUP BY p.id ORDER BY kusy DESC LIMIT 3''').fetchall()
    return render_template('admin.html', produkty=produkty, objednavky=objednavky, trzby=trzby,
                           prodeje=prodeje, sklady=sklady, kategorie=kategorie, statistika=statistika)

# Admin může přidat nový produkt nebo upravit název, cenu a sklad stávajícího.
@app.route('/admin/produkt', methods=['POST'])
@vyzaduje_admin
def admin_produkt():
    pid = cele_cislo(request.form.get('id'))
    nazev = request.form.get('nazev','').strip()
    znacka = request.form.get('znacka','').strip()
    popis = request.form.get('popis','').strip()
    cena = cele_cislo(request.form.get('cena'), -1)
    kid = cele_cislo(request.form.get('kategorie_id'))
    vid = cele_cislo(request.form.get('velikost_id'))
    sklad = cele_cislo(request.form.get('sklad'), -1)
    if not nazev or not znacka or not popis or cena < 0 or sklad < 0:
        flash('Vyplň všechna pole. Cena a sklad nesmí být záporné.')
        return redirect(url_for('admin'))
    try:
        with db() as spojeni:
            if pid:
                # Upravíme jen existující produkt a velikost.
                zmena = spojeni.execute('''UPDATE produkty SET nazev=?,znacka=?,popis=?,cena=?,kategorie_id=?
                    WHERE id=?''', (nazev,znacka,popis,cena,kid,pid))
                if not zmena.rowcount:
                    raise ValueError('Produkt neexistuje.')
            else:
                spojeni.execute('''INSERT INTO produkty(nazev,znacka,popis,cena,kategorie_id)
                    VALUES(?,?,?,?,?)''', (nazev,znacka,popis,cena,kid))
                pid = spojeni.execute('SELECT last_insert_rowid()').fetchone()[0]
            spojeni.execute('''INSERT INTO produkt_velikost(produkt_id,velikost_id,sklad) VALUES(?,?,?)
                ON CONFLICT(produkt_id,velikost_id) DO UPDATE SET sklad=excluded.sklad''', (pid,vid,sklad))
        flash('Produkt uložen.')
    except (ValueError, sqlite3.IntegrityError) as chyba:
        flash('Produkt se nepodařilo uložit: ' + str(chyba))
    return redirect(url_for('admin'))

# Místo smazání produktu ho skryjeme, aby zůstaly staré objednávky.
@app.route('/admin/skryt/<int:pid>', methods=['POST'])
@vyzaduje_admin
def admin_skryt(pid):
    with db() as spojeni:
        spojeni.execute('UPDATE produkty SET aktivni=0 WHERE id=?', (pid,))
    flash('Produkt je skrytý.')
    return redirect(url_for('admin'))

# Admin změní stav objednávky; zrušení vrátí kusy na sklad.
@app.route('/admin/stav/<int:oid>', methods=['POST'])
@vyzaduje_admin
def admin_stav(oid):
    novy = request.form.get('stav')
    if novy not in ('nova','zaplacena','odeslana','zrusena'):
        flash('Neplatný stav.')
        return redirect(url_for('admin'))
    with db() as spojeni:
        stary = spojeni.execute('SELECT stav FROM objednavky WHERE id=?', (oid,)).fetchone()
        if not stary:
            flash('Objednávka neexistuje.')
        elif stary['stav']=='zrusena' and novy!='zrusena':
            flash('Zrušenou objednávku už nejde obnovit.')
        else:
            if novy=='zrusena' and stary['stav']!='zrusena':
                polozky = spojeni.execute('SELECT * FROM polozky_objednavky WHERE objednavka_id=?', (oid,)).fetchall()
                for polozka in polozky:
                    spojeni.execute('''UPDATE produkt_velikost SET sklad=sklad+?
                        WHERE produkt_id=? AND velikost_id=?''', (polozka['mnozstvi'],polozka['produkt_id'],polozka['velikost_id']))
            spojeni.execute('UPDATE objednavky SET stav=? WHERE id=?', (novy,oid))
            flash('Stav objednávky změněn.')
    return redirect(url_for('admin'))

# Stránka popisuje, kdo projekt vytvořil a jak funguje.
@app.route('/o-projektu')
def o_projektu():
    return render_template('o_projektu.html')

# Když něco chybí nebo člověk nemá přístup, zobrazíme normální chybovou stránku.
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def chyba(err):
    return render_template('chyba.html', zprava={403:'Sem smí jen administrátor.',404:'Stránku nebo produkt jsme nenašli.',500:'Něco se pokazilo.'}.get(err.code,'Chyba')), err.code

# Tento blok se spustí při příkazu python app.py.
if __name__ == '__main__':
    priprav_db()
    app.run(debug=True)
