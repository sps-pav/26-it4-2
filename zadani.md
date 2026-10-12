# Projekt 4 – Samostatný projekt (4. ročník / maturitní)

## Cíl projektu

Samostatně vytvořit kompletní projekt propojující **web, hru/aplikaci a databázi**. Projekt je **podmínkou pro přistoupení k praktické maturitní zkoušce**.

---

## Varianty projektu

Projekt lze udělat ve dvou variantách. Variantu si vybíráš **do 1. kontrolního termínu** a napíšeš ji do svého `README.md`.

| | **Varianta A – Hra** (výchozí) | **Varianta B – E-shop** |
|---|---|---|
| **Co vzniká** | Hra nebo desktopová aplikace + webová prezentace + databáze | Webový obchod (katalog, košík, objednávky, administrace) + databáze |
| **Kde je hlavní logika** | Ve hře (herní smyčka, kolize, skóre) | Na serveru a v databázi (košík, objednávka, sklad) |
| **Databáze** | Základní požadavky (viz [3. Databáze](#3-databáze)) | Základní + **rozšířené požadavky** (viz [Rozšířené požadavky pro e-shop](#rozšířené-požadavky-na-databázi-pro-e-shop-varianta-b)) |
| **Testy** | min. 2 | min. **4**, z toho alespoň 2 nad databází |

> **Proč má e-shop přísnější databázi:** e-shop nemá herní část (smyčku, pohyb, kolize), takže by byl sám o sobě jednodušší. Tuto práci nahrazuje **větší a pečlivěji navržená databáze** a **administrace**. Rozsahem má být varianta B srovnatelná s variantou A – není to „lehčí cesta".

> **E-shop je školní projekt:** nezpracovává skutečné platby ani skutečné osobní údaje. Platba se jen simuluje (např. volbou „dobírka / převodem").

Ukázka obou variant ve všech kontrolních bodech je ve složce [Ukazka](Ukazka/) – viz [Ukázkový projekt](#ukázkový-projekt).

---

## Organizace práce

### Práce je **individuální**
- Každý žák pracuje **sám**
- Žák se přidá do **gitového úložiště** vytvořeného učitelem
- **Podobné téma** (hry i e-shopu – např. stejný typ hry nebo stejný sortiment) může mít nejvýše **4 žáci**, každý však na projektu pracuje **samostatně** – vlastní kód, databáze, web i dokumentace (sdílení kódu mezi žáky se považuje za opisování)
- AI lze použít **pouze** pro inspiraci, generování textů hry, **ne pro generování celých bloků kódu**

### Volba jazyka
- Projekt musí být realizován v **technologiích probíraných ve výuce**
- Výjimkou je **Godot Engine** – lze použít po dohodě s učitelem
- Na **začátku školního roku** je nutné ověřit, že projekt **půjde spustit v učebně VT6**
- Pokud potřebujete nainstalovat freeware software, **zažádejte nejpozději do konce října**
- Pokud se projekt nepodaří spustit na školních PC, je nutné **změnit prostředí/jazyk**

---

## Kontrolní termíny

| # | Období | Varianta A – Hra | Varianta B – E-shop |
|---|--------|------------------|---------------------|
| 1 | **Konec října** | Výběr tématu, funkční menu, návrh rozložení projektu (datové toky – co-kde-kam-odkud), návrh databáze, ER diagram | Výběr tématu (sortimentu), kostra webu s navigací, návrh rozložení projektu (datové toky), návrh databáze, ER diagram |
| 2 | **Konec listopadu** | Základní pohyb a logika hry, práce s databází, komunikace DB s webovou stránkou a hrou | Katalog z databáze (filtr, hledání, detail), registrace a přihlášení, košík, vytvoření objednávky |
| 3 | **Konec prosince** | **Finální odevzdání** – kompletní, funkční projekt | **Finální odevzdání** – kompletní, funkční projekt (včetně administrace) |

> **Důležité:** Říjnový a listopadový termín jsou **kontrolní** (průběžné). **Finální odevzdání celého projektu je až v prosinci.**

> **Pozn.:** Měsíce po odevzdání (leden a dále) jsou **procvičovací** – mohou sloužit k dalšímu rozvoji projektu nebo přípravě na maturitu, ale nehodnotí se jako nové odevzdání.

---

## Doporučený postup práce

Jedná se o individuální projekt – všechno děláte sami. Níže je doporučený harmonogram, **na co se soustředit v každé fázi**.

### 1. fáze (září – konec října)

| Oblast | Co dělat |
|--------|-----------|
| **Plánování** | Vybrat téma hry, navrhnout rozložení projektu (datové toky: co-kde-kam-odkud) |
| **Databáze** | Navrhnout a zakreslit **ER diagram**, vytvořit CREATE TABLE skripty |
| **Hra** | Funkční **hlavní menu** (start, ukončení), základní okno Pygame |
| **Web** | Založit strukturu HTML souborů, základní navigace |
| **Git** | Založit repozitář, pravidelně commitovat |

### 2. fáze (listopad – konec listopadu)

| Oblast | Co dělat |
|--------|-----------|
| **Hra** | **Základní pohyb a logika** – postava se pohybuje, reaguje na vstupy, herní smyčka funguje |
| **Databáze** | Vložit vzorová data (INSERT), napsat SELECT dotazy (JOIN, WHERE, ORDER BY) |
| **Propojení** | Hra ukládá skóre do DB, web čte data z DB |
| **Web** | Implementovat **login + registraci**, zobrazit herní výsledky z databáze |
| **Dokumentace** | Komentovat kód průběžně, začít uživatelský manuál |

### 3. fáze (prosinec – konec prosince = finální odevzdání)

| Oblast | Co dělat |
|--------|-----------|
| **Hra** | Doladit mechaniky, opravit bugy, hra se zeptá na jméno hráče |
| **Databáze** | Doplnit UPDATE, DELETE, ověřit **normalizaci (BCNF)** |
| **Web** | Aktualizovat obsah, přidat screenshoty ze hry, vývojové diagramy |
| **Testy** | Napsat minimálně **2 automatizované testy** na důležité funkce |
| **Dokumentace** | Dokončit komentáře u všech tříd/funkcí, finalizovat manuál |
| **Vše** | Finální testování – hra nepadá, web funguje, DB odpovídá, vše je propojené |
| **Git** | Vyčistit repozitář, zkontrolovat historii commitů |
| **Kvalita** | Zpětná vazba učitele zapracována, kód čitelný a komentovaný |

### Varianta B – E-shop: co dělat v jednotlivých fázích

Pro e-shop platí stejné fáze i termíny. Řádky **Hra** z tabulek výše nahraď takto (ostatní řádky – Databáze, Web, Testy, Dokumentace, Git – platí beze změny, jen s rozšířenými požadavky na DB):

| Fáze | Místo herní části udělej |
|------|--------------------------|
| **1. fáze** | Kostra webu: úvodní stránka, katalog (zatím klidně se statickými daty), navigace. Návrh **všech** tabulek včetně objednávek a položek. |
| **2. fáze** | Katalog čte z DB (kategorie, hledání, detail produktu). Registrace a přihlášení. **Košík** a **vytvoření objednávky** v jedné transakci (objednávka + položky + odečtení skladu). |
| **3. fáze** | **Administrace** (CRUD produktů, změna stavu objednávek, přehled tržeb). Historie objednávek zákazníka. Ošetření chyb (vyprodáno, prázdný košík, neplatné vstupy). |

### Procvičovací měsíce (leden a dále)

Měsíce po odevzdání jsou **procvičovací** – nehodnotí se jako nové odevzdání, ale žáci mohou:
- Opravit chyby nalezené při peer review
- Rozvíjet projekt nad rámec požadavků
- Připravovat se na praktickou maturitní zkoušku

> **Tip:** Pracujte průběžně a pravidelně commitujte. Nenechávejte vše na poslední chvíli – projekt je rozsáhlý a musí obsahovat všechny části.

---

## Funkční požadavky

### Projekt musí obsahovat VŠECHNY následující části:

> U **varianty B (e-shop)** se část 1 a 2 slévají do jedné webové aplikace – viz [2B. E-shop](#2b-e-shop-varianta-b). Části 3–6 platí pro obě varianty.

### 1. Webová prezentace
- Minimálně **4 HTML stránky** s navigační lištou
- **1 CSS soubor** pro jednotný design
- Obsahuje informace o hře, vývojové diagramy, pravidla, informace o autorovi
- **Login a registrace** uživatele
- **Zobrazení herních výsledků** z databáze
- Komunikuje s databází přes připravené dotazy

### 2. Hra / Desktopová aplikace
- **Hlavní smyčka** (event loop / update + render), menu, spuštění, ukončení
- **Interakce uživatele** (klávesnice/myš, formuláře, tlačítka)
- **Identifikace uživatele** (jméno hráče / přihlášení)
- **Ukládání dat do DB** (skóre / CRUD operace)
- Projekt **nesmí padat**

> 💡 **Příklad alternativy – Skladovací systém (PyQt6):**
>
> | Herní požadavek | Ekvivalent v aplikaci |
> |---|---|
> | Herní smyčka | Qt event loop |
> | Menu + ukončení | Hlavní okno s navigací |
> | Interakce hráče | Formuláře, tabulky, filtry |
> | Ukládání skóre | CRUD operace v DB |
> | Kdo hrál | Přihlášení / výběr uživatele |

### 2B. E-shop (varianta B)

E-shop nahrazuje **webovou prezentaci i hru** jednou webovou aplikací. Musí umět:

**Zákaznická část**
- **Katalog produktů** načítaný z databáze – filtrování podle kategorie, **vyhledávání** (LIKE), řazení (cena, název)
- **Detail produktu** (popis, cena, dostupnost na skladě)
- **Registrace a přihlášení** zákazníka, hesla uložená **jen jako hash**
- **Košík** – přidat, změnit množství, odebrat, celková cena
- **Objednávka** – vytvoření z košíku, kontrola skladu, simulovaná platba/doprava
- **Historie objednávek** přihlášeného zákazníka včetně položek a stavu

**Administrace** (jen pro uživatele s rolí administrátora)
- **CRUD produktů** – přidat, upravit, skrýt/smazat
- **Správa objednávek** – změna stavu (nová → zaplacená → odeslaná / zrušená)
- **Přehled** – alespoň 2 souhrnné statistiky z DB (např. tržby podle kategorie, nejprodávanější produkty)

**Obecně**
- Minimálně **6 stránek** se společnou navigací a **1 CSS soubor**
- Stránka „O projektu" s informacemi o autorovi, ER diagramem a vývojovými diagramy
- Vstupy z formulářů se **validují na serveru** (záporné množství, prázdná pole, neexistující produkt…)
- Projekt **nesmí padat** – chyba se uživateli zobrazí jako srozumitelná hláška

| Herní požadavek (varianta A) | Ekvivalent v e-shopu (varianta B) |
|---|---|
| Herní smyčka | Zpracování požadavků na serveru (request → logika → DB → odpověď) |
| Menu + ukončení | Navigace, přihlášení / odhlášení |
| Interakce hráče | Formuláře, košík, filtry, vyhledávání |
| Ukládání skóre | Objednávky, položky, změny skladu |
| Kdo hrál | Přihlášený zákazník / administrátor |
| Webová prezentace o hře | Stránka „O projektu" + samotný obchod |

### 3. Databáze

| Požadavek | Detail |
|-----------|--------|
| **ER diagram** | Zakreslen a přiložen k projektu |
| **Vztahy** | Využívá 1:N i M:N (tedy i JOIN při čtení dat) |
| **DDL skripty** | CREATE TABLE s atributy: datový typ, UNIQUE, NOT NULL, AUTO_INCREMENT, PK, FK, DEFAULT |
| **DML skripty** | INSERT – min. 3 vzorové záznamy do každé tabulky |
| **SELECT dotazy** | Včetně JOIN, filtrování (WHERE), řazení (ORDER BY), seskupování (GROUP BY), vyhledávání (LIKE) |
| **Úprava dat** | UPDATE a DELETE příkazy |
| **Normalizace** | Minimálně po **Boyceho-Coddovu normální formu (BCNF)** |
| **Komunikace** | S databází komunikuje web (přes PHP/jiný serverový jazyk) i hra (přes Python) |

#### Rozšířené požadavky na databázi pro e-shop (varianta B)

Všechno z tabulky výše **a navíc**:

| Požadavek | Detail |
|-----------|--------|
| **Rozsah** | Minimálně **7 tabulek** (typicky: uživatel, role/stav, kategorie, produkt, objednávka, položka objednávky + vazební tabulky) |
| **Vztahy M:N** | Minimálně **2 vztahy M:N**, z toho alespoň jedna vazební tabulka má **vlastní atributy** (např. položka objednávky: množství, cena za kus) |
| **Integritní omezení** | **CHECK** (cena ≥ 0, množství > 0, sklad ≥ 0…) a u každého cizího klíče **vědomě zvolené** chování při mazání (`ON DELETE CASCADE / RESTRICT / SET NULL`) – umět vysvětlit proč |
| **Transakce** | Vytvoření objednávky probíhá v **jedné transakci** (objednávka + položky + odečtení skladu). Při chybě se provede **ROLLBACK** a v DB nezůstane půlka objednávky |
| **Historie cen** | Cena v položce objednávky je **uložená v okamžiku nákupu** – pozdější zdražení produktu nesmí změnit staré objednávky |
| **Pohled (VIEW)** | Minimálně **1 pohled** použitý v aplikaci (např. přehled objednávek s celkovou cenou) |
| **Index** | Minimálně **1 vlastní index** (mimo PK/UNIQUE) se zdůvodněním, který dotaz zrychluje |
| **Pokročilé dotazy** | Navíc **LEFT JOIN**, **HAVING**, **vnořený dotaz** (poddotaz) a agregační funkce (SUM, COUNT, AVG) |
| **Bezpečnost** | Výhradně **parametrizované dotazy** (žádné skládání SQL z řetězců), hesla jako hash |
| **Dokumentace DB** | V dokumentaci zdůvodnění normalizace: u každé tabulky klíč a proč splňuje BCNF |

> Tyto požadavky lze (dobrovolně) splnit i ve variantě A – projeví se v hodnocení kvality SQL.

### 4. Propojení
- **Varianta A:** minimálně **2 ze 3 částí** spolu komunikují (DB↔hra, DB↔web, web↔hra)
- **Varianta B:** zákaznická část i administrace pracují nad **stejnou databází** – změna v administraci (cena, sklad, stav objednávky) se okamžitě projeví v obchodě

### 5. Automatizované testy (NAVÍC oproti skupinovému projektu)
- Minimálně **2 automatizované testy** (varianta B – e-shop: minimálně **4**, z toho alespoň **2 nad databází**, např. vytvoření objednávky a odmítnutí objednávky při nedostatku zboží)
- Testy musí být zaměřeny na **důležité funkce projektu**
- Testy musí jít spustit a musí procházet

### 6. Dokumentace

**Kód:**
- Komentáře u všech bloků, tříd a funkcí/metod
- Min. **5 commitů na fázi** s popisnými zprávami (`feat:`, `fix:`, `docs:`, `update:`)
- 3× vývojový diagram klíčové mechaniky

**Povinné soubory** (každý jako samostatný soubor – `.md`, `.pdf`, `.docx`, `.pptx` nebo HTML stránka):

| Soubor | Obsah |
|--------|-------|
| `dokumentace.*` | Účel, technologie, struktura projektu, spuštění, závislosti, omezení |
| `manual.*` | Postup spuštění, popis UI, příklady použití, chybové stavy |
| `prezentace.*` | Problém, řešení, cílová skupina, přínos, ukázka, možnosti rozvoje |
| `prehled.*` | Struktura kódu, datové toky, technologie, jak začít s vývojem, rizika |

---

## Ukázkový projekt

Ve složce [Ukazka](Ukazka/) je hotová ukázka **obou variant**, každá rozdělená podle kontrolních termínů:

| Složka | Co v ní je |
|--------|-----------|
| `Ukazka/hra/kontrolni_bod_1` … `kontrolni_bod_3` | Varianta A – hra *Houbař* (Pygame) + web + databáze |
| `Ukazka/eshop/kontrolni_bod_1` … `kontrolni_bod_3` | Varianta B – e-shop *Zelený kout* (pokojové rostliny) + databáze |

- Každý kontrolní bod je **samostatně spustitelný** a ukazuje, v jakém stavu má být projekt na konci dané fáze.
- V každé složce je `README.md` – co je hotové, co ještě chybí a **co který soubor dělá**.
- Ukázka slouží k pochopení **rozsahu a struktury**. Její témata (*Houbař*, *Zelený kout*) si **nelze zvolit** a její kód se **nesmí kopírovat** – platí pravidlo o vlastní práci.

---

## Povolené technologie

> **Projekt musí být realizován výhradně v technologiích probíraných ve výuce.** Výjimkou je **Godot Engine** – ten lze použít po dohodě s učitelem.

### ✅ Povoleno
- **Python 3** + **Pygame** (hra) – nebo jiný jazyk probíraný ve výuce po dohodě s učitelem
- **E-shop (varianta B):** serverová část v **PHP** nebo v jiném serverovém jazyce probíraném ve výuce; HTML šablony a vlastní CSS
- **Godot Engine** – po dohodě s učitelem
- **HTML 5** + **CSS 3** (webová prezentace)
- **SQL** (MySQL / MariaDB / SQLite – dle toho, co se probírá ve výuce)
- **PHP** nebo jiný serverový jazyk probíraný ve výuce
- **Git** (GitHub / GitLab)
- Standardní knihovny zvoleného jazyka
- Grafické editory pro tvorbu spritů
- Testovací frameworky probírané ve výuce (pytest, unittest apod.)

### ❌ Zakázáno
- Herní enginy (Unity, Unreal apod.) – Godot je výjimka po dohodě s učitelem
- Webové frameworky (React, Vue, Angular, Django, Flask apod.) – pokud nebyly probírány ve výuce
- CSS frameworky (Bootstrap, Tailwind apod.)
- ORM knihovny – SQL dotazy pište ručně
- NoSQL databáze (MongoDB apod.)
- Hotová e-shopová řešení a šablony (WooCommerce, PrestaShop, Shoptet apod.) a skutečné platební brány
- AI generátory kódu pro celé bloky
- Kopírování cizího kódu bez pochopení a úpravy

> **Porušení tohoto pravidla bude mít vliv na hodnocení. Cílem je prokázat vlastní zvládnutí všech technologií.**

---

## Hodnocení

### Známky
- Žák získá **až 3 známky** (1 za každý kontrolní termín)
- Kontrolní termíny jsou na konci října a na konci listopadu, **finální odevzdání na konci prosince** – po odevzdání jsou měsíce procvičovací

### Co se hodnotí

| Kritérium | Váha |
|-----------|:----:|
| Kompletnost (obsahuje všechny povinné části) | 3 |
| Funkčnost (běží, nepadá) | 3 |
| Kvalita kódu (čitelnost, komentáře, struktura) | 2 |
| Kvalita SQL (normalizace, dotazy, DDL/DML) | 2 |
| Dokumentace (4 soubory, diagramy, komentáře v kódu) | 2 |
| Celkový dojem (smysluplnost, přehlednost) | 2 |
| Testy (existují, procházejí) | 1 |
| Práce s Gitem (pravidelné commity, zprávy) | 1 |
| Komunikace s učitelem (reakce na zpětnou vazbu) | 1 |

> **Varianta B (e-shop):** kritérium **Kvalita SQL** má váhu **3** (místo 2) a hodnotí se podle rozšířených požadavků na databázi.

### Vzájemné hodnocení (peer review)

Při kontrolních termínech si žáci navzájem **kontrolují projekty spolužáků** a hledají chyby (nefunkční části, chyby v kódu, SQL problémy, rozbitý web, chybějící dokumentace apod.).

#### Nalezené chyby ve VAŠEM projektu (trest za špatnou kvalitu)
- Za každých **5 nalezených chyb** ve vašem projektu dostanete **známku 5** (váha 1)
- Motivace: testujte svůj projekt důkladně před odevzdáním

#### Nalezení chyb v CIZÍM projektu (odměna za pečlivost)
- Za každé **3 nalezené chyby** v projektu spolužáka dostanete **známku 1** (váha 1)
- Motivace: pečlivě kontrolujte práci ostatních – pomáháte jim i sobě

> **Pravidla peer review:**
> - Chyba musí být **reálná a ověřitelná** (učitel rozhoduje sporné případy)
> - Duplicitní hlášení stejné chyby se nepočítá
> - Chyby se zapisují do souboru **Issues.txt** v gitovém úložišti kontrolovaného projektu
> - **Commit** s nalezenou chybou musí být odeslán **do konce hodiny** po odprezentování ve třídě
> - Kdo pošle commit jako **první**, má přednost v případě nalezení stejné chyby
>
> **Formát zápisu do Issues.txt:**
> ```
> 1. Hra padá po 30 sekundách – nekontrolovaná vyjímka v herní smyčce (Koudelka)
> 2. Registrace na webu neumožňuje zadat heslo delší než 8 znaků (Novák)
> 3. SELECT dotaz na výsledky nezobrazuje jméno hráče (Dvořáková)
> ```
>
> **Formát commit zprávy:**
> ```
> git commit -m "Issue: hra padá po 30 sekundách – nekontrolovaná vyjímka"
> ```

### Podmínka pro maturitu
> Žák **musí tento projekt odevzdat**, aby byl z předmětu programování hodnocen a mohl přistoupit k **praktické maturitní zkoušce v řádném termínu**.

Hodnocení kompletního projektu v posledním termínu **začíná na stupni 4 (dostatečný)** – tím, že projekt obsahuje všechny části. Dále se hodnocení zlepšuje dle kvality zpracování na základě uvážení vyučujícího.

---

## Odevzdání

- Veškerá práce musí být v **gitovém úložišti**
- Učitel musí mít přístup k repozitáři
- Projekt musí jít **spustit na školních PC v učebně VT6**
- SQL skripty přiloženy v repozitáři
- ER diagram přiložen v repozitáři
- Testy musí jít spustit
- **Deadline (finální odevzdání): konec prosince**
- Měsíce po odevzdání jsou procvičovací – slouží k opravám a přípravě na maturitu
