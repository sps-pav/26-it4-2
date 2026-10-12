# Prezentace: Houbař

Osnova pro předvedení projektu ve třídě (cca 5 minut).

## 1. Problém
Chtěl jsem malou hru, kterou jde zahrát za minutu o přestávce, a zároveň si
u ní porovnat výsledky se spolužáky, ne jen na jednom počítači v jednom okně.

## 2. Řešení
- Hra v Pygame: chytání padajících hub do košíku, 60 sekund na partii.
- Web ve Flasku: registrace, žebříček, profil se statistikami.
- Databáze SQLite, kterou hra i web sdílí přes jeden soubor `db.py`.

## 3. Cílová skupina
Spolužáci a kdokoli, kdo chce krátkou hru bez instalace něčeho velkého.

## 4. Přínos
- Obtížnosti a druhy hub jsou v databázi, novou houbu přidám jedním `INSERT`, bez zásahu do kódu.
- Statistika „co jsem nasbíral“ ukazuje využití vztahu M:N v praxi.
- Pravidla hry jsou oddělená od kreslení, takže jdou testovat automaticky.

## 5. Ukázka (co předvedu)
1. Registrace nového hráče na webu.
2. Přihlášení ve hře, výběr obtížnosti, krátká partie, pauza.
3. Obrazovka s výsledkem a nejlepšími hráči.
4. Žebříček na webu s filtrem, profil se sebranými houbami.
5. Smazání partie v profilu, zmizí i ze žebříčku.
6. Spuštění testů: `python -m unittest`.

## 6. Možnosti rozvoje
- zvuky a obrázky hub místo kreslených tvarů,
- úspěchy (achievementy) za nasbírané houby,
- vzácné bonusové houby (zpomalení času, život navíc),
- přechod na MySQL, aby šlo hrát z více počítačů proti jedné databázi.
