import sqlite3 

with open("databaze\seed_catalog.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

with sqlite3.connect("databaze\eshop.db") as conn:
    cursor = conn.cursor()
    cursor.executescript(sql_script)