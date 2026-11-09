# Cesta k databázi je na jednom místě, abychom ji nemuseli hledat v celém projektu.
from pathlib import Path

# Soubor obchod.db se vytvoří při prvním spuštění aplikace.
DB_PATH = Path(__file__).parent / "obchod.db"
