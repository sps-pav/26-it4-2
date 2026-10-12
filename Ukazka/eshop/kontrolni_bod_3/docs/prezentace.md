# Prezentace: Zelený kout

Osnova pro předvedení projektu ve třídě (cca 5 minut).

## 1. Problém
Malý prodejce rostlin přijímá objednávky e-mailem a sklad vede v sešitě. Stává se,
že prodá kytku, kterou už nemá, a neví, co se prodává nejlíp.

## 2. Řešení
- Obchod: katalog s filtrem a hledáním, košík, objednávka.
- Administrace: produkty, stavy objednávek, přehled tržeb.
- Databáze, která hlídá, co aplikace hlídat nemusí: sklad nejde do mínusu,
  objednávka se uloží celá nebo vůbec, prodaný produkt nejde smazat.

## 3. Cílová skupina
Malý obchod s desítkami až stovkami produktů a jedním člověkem, který ho spravuje.

## 4. Přínos
- Sklad se odečítá automaticky v okamžiku objednání.
- Staré objednávky ukazují ceny, za které se opravdu prodalo.
- Prodejce vidí tržby podle kategorie a nejprodávanější zboží.

## 5. Ukázka (co předvedu)
1. Katalog: kategorie, hledání „kaktus“, řazení podle ceny.
2. Vložení do košíku, pokus vložit víc kusů, než je skladem (objeví se hláška).
3. Objednávka jako zákazník, detail objednávky.
4. Administrace: nová objednávka v seznamu, ubylo ze skladu.
5. Zdražení produktu, stará objednávka má pořád původní cenu.
6. Zrušení objednávky, zboží se vrátilo na sklad.
7. Pokus smazat prodaný produkt, databáze to odmítne.
8. Spuštění testů: `python -m unittest`.

## 6. Možnosti rozvoje
- fotografie produktů a nahrávání obrázků v administraci,
- způsoby dopravy s cenou jako další číselník,
- hodnocení produktů zákazníky (další vztah M:N),
- slevové kódy,
- přechod na MySQL a nasazení na školní server.
