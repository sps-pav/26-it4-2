"""E-shop Zelený kout (Flask):  python app.py, web pak běží na http://127.0.0.1:5000

Tento soubor řeší jen "dopravu": přijme požadavek z prohlížeče, zavolá funkci
z katalog.py / kosik.py / objednavky.py / ucty.py a výsledek pošle do šablony.
Žádné SQL tu není.
"""
import sqlite3

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for

import db
import katalog
import kosik
import objednavky
import ucty

app = Flask(__name__)
# Klíč, kterým Flask podepisuje cookie s přihlášením a košíkem. Na skutečném
# serveru by musel být tajný a nesměl by být v gitu.
app.config["SECRET_KEY"] = "vyvojovy-klic-jen-pro-skolni-projekt"
app.config["DATABAZE"] = None       # None = výchozí soubor eshop.db (testy si nastaví vlastní)


# Pomocné funkce
@app.template_filter("kc")
def format_kc(castka):
    """Filtr do šablon: z čísla 1299 udělá "1 299 Kč". Použití: {{ produkt.cena_kc | kc }}"""
    return f"{castka:,}".replace(",", " ") + " Kč"


def spojeni():
    """Vrátí připojení k databázi pro právě zpracovávaný požadavek."""
    if "spojeni" not in g:
        g.spojeni = db.pripoj(app.config["DATABAZE"])
        db.vytvor_databazi(g.spojeni)
    return g.spojeni


@app.teardown_appcontext
def zavri_spojeni(chyba):
    """Po vyřízení požadavku připojení zavře (Flask volá automaticky)."""
    pripojeni = g.pop("spojeni", None)
    if pripojeni is not None:
        pripojeni.close()


def nacti_kosik():
    """Vrátí kopii košíku ze session (slovník {id produktu: množství})."""
    return dict(session.get("kosik", {}))


def prihlaseny_id():
    """Vrátí id přihlášeného uživatele; nepřihlášeného pošle chybou 401 na přihlášení."""
    if "uzivatel_id" not in session:
        abort(401)
    return session["uzivatel_id"]


def jen_admin():
    """Pustí dál jen administrátora, ostatním vrátí chybu 403 (zakázáno)."""
    prihlaseny_id()
    if not session.get("je_admin"):
        abort(403)


@app.context_processor
def spolecna_data():
    """Data dostupná ve všech šablonách: počet kusů v košíku pro navigaci."""
    return {"kusu_v_kosiku": kosik.pocet_kusu(session.get("kosik", {}))}


# Obchod: úvod, katalog, detail produktu
@app.route("/")
def index():
    """Úvodní stránka."""
    return render_template("index.html", kategorie=katalog.kategorie(spojeni()))


@app.route("/katalog")
def stranka_katalog():
    """Seznam produktů."""
    # Filtr přichází v adrese: /katalog?kategorie=4&hledat=kaktus&razeni=cena
    hledat = request.args.get("hledat", "").strip()
    kategorie_id = request.args.get("kategorie", type=int)      # ze špatné hodnoty bude None
    razeni = request.args.get("razeni", "nazev")
    return render_template(
        "katalog.html",
        produkty=katalog.hledej_produkty(spojeni(), kategorie_id, hledat, razeni),
        kategorie=katalog.kategorie(spojeni()),
        hledat=hledat,
        kategorie_id=kategorie_id,
        razeni=razeni,
    )


@app.route("/produkt/<int:produkt_id>")
def detail_produktu(produkt_id):
    """Detail jednoho produktu."""
    produkt = katalog.najdi_produkt(spojeni(), produkt_id)
    if produkt is None:
        abort(404)
    return render_template(
        "produkt.html",
        produkt=produkt,
        kategorie=katalog.kategorie_produktu(spojeni(), produkt_id),
    )


@app.route("/doprava")
def doprava():
    """Informace o dopravě a platbě."""
    return render_template("doprava.html")


@app.route("/o-projektu")
def o_projektu():
    """Informace o autorovi, technologiích a diagramy."""
    return render_template("o_projektu.html")


# Košík
@app.route("/kosik")
def zobraz_kosik():
    """Obsah košíku s cenami z databáze."""
    obsah = nacti_kosik()
    produkty = katalog.produkty_podle_id(spojeni(), [int(klic) for klic in obsah])
    polozky, celkem = kosik.sestav_polozky(obsah, produkty)
    return render_template("kosik.html", polozky=polozky, celkem=celkem)


@app.route("/kosik/pridat", methods=["POST"])
def pridat_do_kosiku():
    """Přidá produkt do košíku (formulář u produktu)."""
    produkt_id = request.form.get("produkt_id", type=int)
    produkt = katalog.najdi_produkt(spojeni(), produkt_id)
    if produkt is None:
        abort(404)
    try:
        obsah = kosik.pridej(nacti_kosik(), produkt_id, request.form.get("mnozstvi", 1))
        if obsah.get(str(produkt_id), 0) > produkt["sklad"]:
            raise ValueError(f"Produkt {produkt['nazev']} je skladem jen {produkt['sklad']} ks.")
    except ValueError as chyba:
        flash(str(chyba), "chyba")
    else:
        session["kosik"] = obsah
        flash(f"{produkt['nazev']} je v košíku.", "ok")
    return redirect(url_for("zobraz_kosik"))


@app.route("/kosik/zmenit", methods=["POST"])
def zmenit_kosik():
    """Změní množství produktu v košíku; nula ho odebere."""
    produkt_id = request.form.get("produkt_id", type=int)
    if produkt_id is None:
        abort(404)
    try:
        session["kosik"] = kosik.nastav(nacti_kosik(), produkt_id, request.form.get("mnozstvi"))
    except ValueError as chyba:
        flash(str(chyba), "chyba")
    return redirect(url_for("zobraz_kosik"))


@app.route("/objednat", methods=["GET", "POST"])
def objednat():
    """GET zobrazí shrnutí a formulář s adresou, POST objednávku vytvoří."""
    uzivatel_id = prihlaseny_id()
    obsah = nacti_kosik()

    if request.method == "POST":
        try:
            objednavka_id = objednavky.vytvor_objednavku(
                spojeni(), uzivatel_id, obsah,
                request.form.get("adresa", ""), request.form.get("zpusob_platby", ""),
            )
        except ValueError as chyba:
            flash(str(chyba), "chyba")
        else:
            session["kosik"] = {}
            flash(f"Děkujeme! Objednávka č. {objednavka_id} je přijatá.", "ok")
            return redirect(url_for("detail_objednavky", objednavka_id=objednavka_id))

    produkty = katalog.produkty_podle_id(spojeni(), [int(klic) for klic in obsah])
    polozky, celkem = kosik.sestav_polozky(obsah, produkty)
    if not polozky:
        flash("Košík je prázdný.", "chyba")
        return redirect(url_for("zobraz_kosik"))
    return render_template("objednat.html", polozky=polozky, celkem=celkem,
                           zpusoby_platby=objednavky.ZPUSOBY_PLATBY)


# Účet: registrace, přihlášení, odhlášení
@app.route("/registrace", methods=["GET", "POST"])
def registrace():
    """GET zobrazí formulář, POST vytvoří účet."""
    if request.method == "POST":
        heslo = request.form.get("heslo", "")
        if heslo != request.form.get("heslo_znovu", ""):
            flash("Hesla se neshodují.", "chyba")
        else:
            try:
                ucty.registruj(spojeni(), request.form.get("email", ""), request.form.get("jmeno", ""), heslo)
            except ValueError as chyba:
                flash(str(chyba), "chyba")
            else:
                flash("Účet je vytvořený, můžeš se přihlásit.", "ok")
                return redirect(url_for("prihlaseni"))
    return render_template("registrace.html")


@app.route("/prihlaseni", methods=["GET", "POST"])
def prihlaseni():
    """GET zobrazí formulář, POST ověří e-mail a heslo."""
    if request.method == "POST":
        uzivatel = ucty.prihlas(spojeni(), request.form.get("email", ""), request.form.get("heslo", ""))
        if uzivatel is None:
            flash("Špatný e-mail nebo heslo.", "chyba")
        else:
            # Do session si uložíme, kdo je přihlášený. Košík v session zůstává.
            session["uzivatel_id"] = uzivatel["id"]
            session["jmeno"] = uzivatel["jmeno"]
            session["je_admin"] = bool(uzivatel["je_admin"])
            flash(f"Vítej, {uzivatel['jmeno']}!", "ok")
            return redirect(url_for("stranka_katalog"))
    return render_template("prihlaseni.html")


@app.route("/odhlaseni")
def odhlaseni():
    """Zapomene přihlášeného uživatele i jeho košík."""
    session.clear()
    flash("Odhlášeno.", "ok")
    return redirect(url_for("index"))


# Moje objednávky
@app.route("/objednavky")
def moje_objednavky():
    """Historie objednávek přihlášeného zákazníka."""
    return render_template(
        "objednavky.html",
        objednavky=objednavky.objednavky_uzivatele(spojeni(), prihlaseny_id()),
    )


@app.route("/objednavka/<int:objednavka_id>")
def detail_objednavky(objednavka_id):
    """Detail objednávky. Vidí ho jen její zákazník a administrátor."""
    uzivatel_id = prihlaseny_id()
    objednavka, polozky = objednavky.najdi_objednavku(spojeni(), objednavka_id)
    if objednavka is None or (objednavka["uzivatel_id"] != uzivatel_id and not session.get("je_admin")):
        abort(404)      # cizí objednávka se tváří, že neexistuje
    return render_template("objednavka.html", objednavka=objednavka, polozky=polozky,
                           zpusoby_platby=objednavky.ZPUSOBY_PLATBY)


# Administrace
@app.route("/admin")
def admin_prehled():
    """Přehled obchodu: souhrnná čísla a statistiky prodejů."""
    jen_admin()
    return render_template(
        "admin_prehled.html",
        souhrn=objednavky.souhrn(spojeni()),
        trzby=objednavky.trzby_podle_kategorie(spojeni()),
        nejprodavanejsi=objednavky.nejprodavanejsi(spojeni()),
    )


@app.route("/admin/produkty")
def admin_produkty():
    """Tabulka všech produktů včetně skrytých."""
    jen_admin()
    return render_template("admin_produkty.html", produkty=katalog.vsechny_produkty(spojeni()))


@app.route("/admin/produkt/novy", methods=["GET", "POST"])
@app.route("/admin/produkt/<int:produkt_id>", methods=["GET", "POST"])
def admin_produkt(produkt_id=None):
    """Formulář pro nový produkt (bez id) nebo úpravu existujícího (s id)."""
    jen_admin()
    produkt = None
    vybrane = set()
    if produkt_id is not None:
        produkt = katalog.najdi_produkt(spojeni(), produkt_id, jen_aktivni=False)
        if produkt is None:
            abort(404)
        vybrane = {k["id"] for k in katalog.kategorie_produktu(spojeni(), produkt_id)}

    if request.method == "POST":
        try:
            katalog.uloz_produkt(spojeni(), request.form, request.form.getlist("kategorie"), produkt_id)
        except ValueError as chyba:
            flash(str(chyba), "chyba")
            # Formulář vykreslíme znovu s tím, co uživatel napsal, ať to nemusí psát celé znovu.
            produkt = request.form
            vybrane = set(request.form.getlist("kategorie", type=int))
        else:
            flash("Produkt je uložený.", "ok")
            return redirect(url_for("admin_produkty"))

    return render_template(
        "admin_produkt.html",
        produkt=produkt,
        produkt_id=produkt_id,
        vybrane=vybrane,
        kategorie=katalog.kategorie(spojeni()),
        dodavatele=katalog.dodavatele(spojeni()),
    )


@app.route("/admin/produkt/<int:produkt_id>/aktivni", methods=["POST"])
def admin_produkt_aktivni(produkt_id):
    """Skryje produkt z nabídky, nebo ho vrátí zpět."""
    jen_admin()
    katalog.nastav_aktivni(spojeni(), produkt_id, request.form.get("aktivni") == "1")
    return redirect(url_for("admin_produkty"))


@app.route("/admin/produkt/<int:produkt_id>/smazat", methods=["POST"])
def admin_produkt_smazat(produkt_id):
    """Smaže produkt, pokud ho nikdo neobjednal."""
    jen_admin()
    try:
        katalog.smaz_produkt(spojeni(), produkt_id)
    except ValueError as chyba:
        flash(str(chyba), "chyba")
    else:
        flash("Produkt je smazaný.", "ok")
    return redirect(url_for("admin_produkty"))


@app.route("/admin/objednavky")
def admin_objednavky():
    """Všechny objednávky s filtrem podle stavu."""
    jen_admin()
    stav_id = request.args.get("stav", type=int)
    return render_template(
        "admin_objednavky.html",
        objednavky=objednavky.vsechny_objednavky(spojeni(), stav_id),
        stavy=objednavky.stavy(spojeni()),
        stav_id=stav_id,
    )


@app.route("/admin/objednavka/<int:objednavka_id>/stav", methods=["POST"])
def admin_zmena_stavu(objednavka_id):
    """Změní stav objednávky (zrušení vrátí zboží na sklad)."""
    jen_admin()
    try:
        objednavky.zmen_stav(spojeni(), objednavka_id, request.form.get("stav", type=int))
    except ValueError as chyba:
        flash(str(chyba), "chyba")
    else:
        flash(f"Stav objednávky č. {objednavka_id} je změněný.", "ok")
    return redirect(url_for("admin_objednavky"))


# Chybové stránky: web nesmí spadnout na nesrozumitelnou hlášku
@app.errorhandler(401)
def chyba_neprihlasen(chyba):
    """Na stránku jen pro přihlášené přišel někdo nepřihlášený."""
    flash("Nejdřív se přihlas.", "chyba")
    return redirect(url_for("prihlaseni"))


@app.errorhandler(403)
def chyba_zakazano(chyba):
    """Do administrace se dostal běžný zákazník."""
    return render_template("chyba.html", zprava="Sem má přístup jen administrátor."), 403


@app.errorhandler(404)
def chyba_nenalezeno(chyba):
    """Neexistující adresa, produkt nebo objednávka."""
    return render_template("chyba.html", zprava="Tohle jsme nenašli."), 404


@app.errorhandler(sqlite3.Error)
def chyba_databaze(chyba):
    """Databáze selhala (chybí soubor, je poškozená apod.)."""
    app.logger.exception("Chyba databáze")
    return render_template("chyba.html", zprava="Databáze teď neodpovídá, zkus to později."), 500


if __name__ == "__main__":
    # debug=True: server se po úpravě kódu sám restartuje a ukáže chyby. Jen pro vývoj!
    app.run(debug=True)
