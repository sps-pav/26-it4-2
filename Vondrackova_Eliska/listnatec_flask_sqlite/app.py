import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Cesta k souboru SQLite databaze ve stejne slozce jako app.py
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "listnatec.db")


# Pomocna funkce, ktera vrati pripojeni k SQLite databazi
def pripoj_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializuj_db():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS kategorie (
            id_kategorie INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev TEXT NOT NULL UNIQUE,
            popis TEXT
        );

        CREATE TABLE IF NOT EXISTS produkt (
            id_produkt INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev TEXT NOT NULL,
            popis TEXT,
            cena REAL NOT NULL CHECK (cena >= 0),
            sklad INTEGER NOT NULL DEFAULT 0 CHECK (sklad >= 0),
            svetlo TEXT,
            zalivka TEXT,
            teplota TEXT,
            obrazek TEXT,
            viditelny INTEGER NOT NULL DEFAULT 1,
            doporuceny INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS produkt_kategorie (
            id_produkt INTEGER NOT NULL,
            id_kategorie INTEGER NOT NULL,
            PRIMARY KEY (id_produkt, id_kategorie),
            FOREIGN KEY (id_produkt) REFERENCES produkt(id_produkt) ON DELETE CASCADE,
            FOREIGN KEY (id_kategorie) REFERENCES kategorie(id_kategorie) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS kosik_polozka (
            id_produkt INTEGER PRIMARY KEY,
            mnozstvi INTEGER NOT NULL DEFAULT 1 CHECK (mnozstvi > 0),
            FOREIGN KEY (id_produkt) REFERENCES produkt(id_produkt) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS objednavka (
            id_objednavka INTEGER PRIMARY KEY AUTOINCREMENT,
            datum_vytvoreni TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            jmeno_prijemce TEXT NOT NULL,
            adresa TEXT NOT NULL,
            mesto TEXT NOT NULL,
            psc TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS polozka_objednavky (
            id_objednavka INTEGER NOT NULL,
            id_produkt INTEGER NOT NULL,
            mnozstvi INTEGER NOT NULL CHECK (mnozstvi > 0),
            cena_za_kus REAL NOT NULL CHECK (cena_za_kus >= 0),
            PRIMARY KEY (id_objednavka, id_produkt),
            FOREIGN KEY (id_objednavka) REFERENCES objednavka(id_objednavka) ON DELETE CASCADE,
            FOREIGN KEY (id_produkt) REFERENCES produkt(id_produkt) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS kontaktni_zprava (
            id_zprava INTEGER PRIMARY KEY AUTOINCREMENT,
            jmeno TEXT NOT NULL,
            email TEXT NOT NULL,
            zprava TEXT NOT NULL,
            datum TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)

    pocet = cursor.execute("SELECT COUNT(*) AS pocet FROM produkt").fetchone()["pocet"]
    if pocet == 0:
        cursor.executemany(
            "INSERT INTO kategorie (nazev, popis) VALUES (?, ?)",
            [
                ("Listové rostliny", "Rostliny pěstované kvůli dekorativním listům"),
                ("Sukulenty a kaktusy", "Nenáročné rostliny, které zadržují vodu"),
                ("Palmy", "Větší rostliny do světlých místností"),
                ("Kvetoucí rostliny", "Rostliny s okrasnými květy"),
            ],
        )

        cursor.executemany(
            """
            INSERT INTO produkt (nazev, popis, cena, sklad, svetlo, zalivka, teplota, obrazek, viditelny, doporuceny)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                ("Monstera", "Velké listy s dírami. Snese i polostín.", 399.0, 15, "Hodně světla, ale ne přímé slunce", "Když je půda nahoře suchá", "18 až 25 °C", "monstera.jpg", 1, 1),
                ("Kaktus", "Nenáročná rostlina, zalévá se málo.", 129.0, 40, "Plné slunce", "Jednou za 2-3 týdny", "15 až 30 °C", "kaktus.jpg", 1, 1),
                ("Zamioculcas", "Přežije i hodně málo světla.", 349.0, 10, "I stín", "Zřídka", "16 až 28 °C", "zamioculcas.jpg", 1, 1),
                ("Pilea", "Malá rostlina s kulatými lístky.", 179.0, 25, "Světlé místo", "Mírně vlhká půda", "18 až 24 °C", "pilea.jpg", 1, 0),
                ("Areka", "Palma, která potřebuje hodně světla.", 459.0, 5, "Hodně světla", "Pravidelně", "18 až 26 °C", "areka.jpg", 1, 0),
                ("Orchidej", "Dlouho kvete, ale musí se opatrně zalévat.", 299.0, 12, "Světlo bez přímého slunce", "Ponořením jednou týdně", "18 až 25 °C", "orchidej.jpg", 1, 0),
            ],
        )

        cursor.executemany(
            "INSERT INTO produkt_kategorie (id_produkt, id_kategorie) VALUES (?, ?)",
            [
                (1, 1),
                (2, 2),
                (3, 1),
                (3, 2),
                (4, 1),
                (5, 3),
                (6, 4),
            ],
        )

    conn.commit()
    cursor.close()
    conn.close()


@app.route("/")
def index():
    conn = pripoj_db()
    cursor = conn.cursor()
    doporucene = cursor.execute(
        "SELECT id_produkt, nazev, popis, cena, obrazek FROM produkt WHERE viditelny = 1 AND doporuceny = 1 ORDER BY id_produkt"
    ).fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", doporucene=doporucene)


@app.route("/katalog")
def katalog():
    kategorie_id = request.args.get("kategorie", "")
    max_cena = request.args.get("max_cena", "")
    hledat = request.args.get("hledat", "").strip()
    jen_skladem = request.args.get("skladem", "")

    conn = pripoj_db()
    cursor = conn.cursor()

    kategorie = cursor.execute("SELECT id_kategorie, nazev FROM kategorie ORDER BY nazev").fetchall()

    sql = "SELECT DISTINCT p.id_produkt, p.nazev, p.popis, p.cena, p.sklad, p.obrazek FROM produkt p"
    parametry = []

    if kategorie_id != "":
        sql += " JOIN produkt_kategorie pk ON pk.id_produkt = p.id_produkt"

    sql += " WHERE p.viditelny = 1"

    if kategorie_id != "":
        sql += " AND pk.id_kategorie = ?"
        parametry.append(int(kategorie_id))

    if max_cena != "":
        try:
            cena_cislo = float(max_cena)
            if cena_cislo >= 0:
                sql += " AND p.cena <= ?"
                parametry.append(cena_cislo)
        except ValueError:
            pass

    if jen_skladem == "1":
        sql += " AND p.sklad > 0"

    if hledat != "":
        sql += " AND p.nazev LIKE ?"
        parametry.append(hledat + "%")

    sql += " ORDER BY p.nazev ASC"

    produkty = cursor.execute(sql, parametry).fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "katalog.html",
        kategorie=kategorie,
        produkty=produkty,
        vybrana_kategorie=kategorie_id,
        max_cena=max_cena,
        hledat=hledat,
        jen_skladem=jen_skladem,
    )


@app.route("/detail/<int:id_produkt>")
def detail(id_produkt):
    conn = pripoj_db()
    cursor = conn.cursor()
    produkt = cursor.execute(
        "SELECT * FROM produkt WHERE id_produkt = ? AND viditelny = 1",
        (id_produkt,),
    ).fetchone()
    cursor.close()
    conn.close()

    if produkt is None:
        return redirect(url_for("katalog"))

    return render_template("detail.html", produkt=produkt)


@app.route("/o-nas")
def o_nas():
    return render_template("o-nas.html")


@app.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    odeslano = False
    if request.method == "POST":
        jmeno = request.form.get("jmeno", "").strip()
        email = request.form.get("email", "").strip()
        zprava = request.form.get("zprava", "").strip()

        if jmeno and email and zprava:
            conn = pripoj_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO kontaktni_zprava (jmeno, email, zprava) VALUES (?, ?, ?)",
                (jmeno, email, zprava),
            )
            conn.commit()
            cursor.close()
            conn.close()
            odeslano = True

    return render_template("kontakt.html", odeslano=odeslano)


@app.route("/kosik/pridat/<int:id_produkt>", methods=["POST"])
def pridat_do_kosiku(id_produkt):
    conn = pripoj_db()
    cursor = conn.cursor()
    produkt = cursor.execute(
        "SELECT id_produkt, sklad FROM produkt WHERE id_produkt = ? AND viditelny = 1",
        (id_produkt,),
    ).fetchone()

    if produkt is not None and produkt["sklad"] > 0:
        existujici = cursor.execute(
            "SELECT mnozstvi FROM kosik_polozka WHERE id_produkt = ?",
            (id_produkt,),
        ).fetchone()
        if existujici is None:
            cursor.execute(
                "INSERT INTO kosik_polozka (id_produkt, mnozstvi) VALUES (?, 1)",
                (id_produkt,),
            )
        else:
            nove_mnozstvi = min(existujici["mnozstvi"] + 1, produkt["sklad"])
            cursor.execute(
                "UPDATE kosik_polozka SET mnozstvi = ? WHERE id_produkt = ?",
                (nove_mnozstvi, id_produkt),
            )
        conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("kosik"))


@app.route("/kosik")
def kosik():
    conn = pripoj_db()
    cursor = conn.cursor()
    polozky = cursor.execute(
        """
        SELECT p.id_produkt, p.nazev, p.cena, k.mnozstvi, (p.cena * k.mnozstvi) AS celkem
        FROM kosik_polozka k
        JOIN produkt p ON p.id_produkt = k.id_produkt
        ORDER BY p.nazev
        """
    ).fetchall()
    celkova_cena = sum(item["celkem"] for item in polozky)
    cursor.close()
    conn.close()
    return render_template("kosik.html", polozky=polozky, celkova_cena=celkova_cena)


@app.route("/objednat", methods=["POST"])
def objednat():
    jmeno = request.form.get("jmeno_prijemce", "").strip()
    adresa = request.form.get("adresa", "").strip()
    mesto = request.form.get("mesto", "").strip()
    psc = request.form.get("psc", "").strip()

    conn = pripoj_db()
    cursor = conn.cursor()
    try:
        conn.execute("BEGIN")
        polozky = cursor.execute(
            """
            SELECT p.id_produkt, p.sklad, p.cena, k.mnozstvi
            FROM kosik_polozka k
            JOIN produkt p ON p.id_produkt = k.id_produkt
            """
        ).fetchall()

        if len(polozky) == 0 or not jmeno or not adresa or not mesto or not psc:
            raise ValueError("Chybí údaje nebo je košík prázdný.")

        for polozka in polozky:
            if polozka["mnozstvi"] > polozka["sklad"]:
                raise ValueError("Nedostatek kusů na skladě.")

        cursor.execute(
            """
            INSERT INTO objednavka (jmeno_prijemce, adresa, mesto, psc)
            VALUES (?, ?, ?, ?)
            """,
            (jmeno, adresa, mesto, psc),
        )
        id_objednavka = cursor.lastrowid

        for polozka in polozky:
            cursor.execute(
                """
                INSERT INTO polozka_objednavky (id_objednavka, id_produkt, mnozstvi, cena_za_kus)
                VALUES (?, ?, ?, ?)
                """,
                (id_objednavka, polozka["id_produkt"], polozka["mnozstvi"], polozka["cena"]),
            )
            cursor.execute(
                "UPDATE produkt SET sklad = sklad - ? WHERE id_produkt = ?",
                (polozka["mnozstvi"], polozka["id_produkt"]),
            )

        cursor.execute("DELETE FROM kosik_polozka")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Chyba při vytváření objednávky:", e)
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("kosik"))


if __name__ == "__main__":
    inicializuj_db()
    app.run(debug=True)
