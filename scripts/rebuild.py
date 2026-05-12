from app.db import run_update
from scripts.create_tables import create_tables

print("Stergem tabelele existente (daca exista)")

run_update("DROP TABLE IF EXISTS mese_rezervate;")
run_update("DROP TABLE IF EXISTS rezervari;")
run_update("DROP TABLE IF EXISTS user_log;")
run_update("DROP TABLE IF EXISTS retete;")
run_update("DROP TABLE IF EXISTS stoc;")
run_update("DROP TABLE IF EXISTS ingredient;")
run_update("DROP TABLE IF EXISTS users;")


print("Creez tabelele din schema sql...")
create_tables()

print("Rebuild gata!")