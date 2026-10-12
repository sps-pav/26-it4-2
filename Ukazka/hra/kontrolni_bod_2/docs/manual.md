# Uživatelský manuál: Houbař

> Rozpracovaná verze (2. kontrolní bod). Chybí popis obtížností, profilu a chybových stavů.

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
| Partie | košík ovládáš šipkami nebo klávesami A a D |
| Konec hry | uvidíš skóre a sebrané houby; Enter tě vrátí do menu |

Ovládání v partii:

| Klávesa | Akce |
|---------|------|
| ← / A | košík doleva |
| → / D | košík doprava |
| Esc | ukončit partii (výsledek se uloží) |

## 4. Web

| Stránka | Obsah |
|---------|-------|
| Úvod | popis hry a jak začít |
| Pravidla | pravidla a tabulka hub načtená z databáze |
| Žebříček | 20 nejlepších partií |
| O projektu | autor, technologie, diagramy |
