# Uživatelský manuál: Houbař

## 1. Spuštění

```bash
pip install -r requirements.txt
python web.py        # web na adrese http://127.0.0.1:5000
python main.py       # hra (spusť v druhém okně terminálu)
```

Databáze `houbar.db` se vytvoří sama při prvním spuštění hry nebo webu.

## 2. Vytvoření účtu
1. Otevři v prohlížeči `http://127.0.0.1:5000`.
2. Klikni na **Registrace**, zadej jméno (3 až 20 znaků) a dvakrát heslo (min. 6 znaků).
3. K vyzkoušení jsou připravené účty `pepa`, `anicka` a `houbar`, všechny s heslem `heslo123`.

## 3. Hra

| Obrazovka | Co na ní uděláš |
|-----------|-----------------|
| Menu | **Hrát** (nebo Enter) spustí hru, **Konec** (nebo Esc) ji zavře |
| Přihlášení | zadej jméno a heslo z webu; Tab přepíná pole, Enter potvrdí |
| Výběr obtížnosti | klikni na Lehká / Normální / Těžká |
| Partie | košík ovládáš šipkami nebo klávesami A a D |
| Konec hry | uvidíš skóre a sebrané houby; Enter tě vrátí do menu |

Ovládání v partii:

| Klávesa | Akce |
|---------|------|
| ← / A | košík doleva |
| → / D | košík doprava |
| P | pauza |
| Esc | ukončit partii (výsledek se uloží) |

## 4. Web

| Stránka | Obsah |
|---------|-------|
| Úvod | popis hry a jak začít |
| Pravidla | pravidla a tabulka hub načtená z databáze |
| Žebříček | nejlepší partie, filtr podle obtížnosti a jména, souhrn hráčů |
| Profil | moje partie, nasbírané houby, změna hesla, smazání partie nebo účtu |
| O projektu | autor, technologie, diagramy |

## 5. Příklad použití
1. Zaregistruji se na webu jako `novacek`.
2. Spustím hru, přihlásím se jako `novacek`, vyberu obtížnost **Normální**.
3. Za 60 sekund nasbírám 120 bodů.
4. Na webu v **Žebříčku** vidím svou partii, v **Profilu** kolik kterých hub jsem chytil.

## 6. Chybové stavy

| Co se stalo | Co uvidíš | Co s tím |
|-------------|-----------|----------|
| špatné jméno nebo heslo | „Špatné jméno nebo heslo.“ | zkus to znovu, případně se zaregistruj na webu |
| jméno je při registraci obsazené | „Toto jméno už někdo používá.“ | zvol jiné jméno |
| hesla při registraci nejsou stejná | „Hesla se neshodují.“ | napiš obě hesla znovu |
| profil bez přihlášení | přesměrování na přihlášení | přihlas se |
| neexistující adresa | stránka „Tahle stránka neexistuje.“ | vrať se na úvod |
| výsledek nejde uložit do databáze | ve hře „Výsledek se nepodařilo uložit.“ | podrobnosti jsou v souboru `houbar.log` |
| `ModuleNotFoundError: pygame` | hra se nespustí | `pip install -r requirements.txt` |
