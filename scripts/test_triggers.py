from app.db import run_update, run_select
print("TEST TRIGGER BEFORE INSERT (stoc)")
id_ingr = run_select("SELECT id FROM ingrediente LIMIT 1;")[0][0]
print("Inserare valida (qty = 5)")

try:
    run_update(
        "INSERT INTO stoc (nr_ingrediente, id_ingredient) VALUES(%s, %s);",
        (5, id_ingr))
    print("OK: Inserarea valida a reusit")
except Exception as e:
    print("EROARE (nu trebuia):", e)
print("\nInserare invalida (qty = -3)")
try:
    run_update(
        "INSERT INTO stoc (nr_ingrediente, id_ingredient) VALUES(%s, %s);",
        (-3, id_ingr))
    print("EROARE: Inserare invalida a trecut (trigger NU functioneaza)")
except Exception as e:
    print("OK: inserare invalida a fost respinda de trigger")
    print("Mesaj DB: ", e)

print("\nTEST TRIGGER AFTER UPDATE")
print("Facem update pe ingrediente")
run_update(
    "UPDATE stoc SET nr_ingrediente = %s WHERE id = %s;",
    (10, id_ingr))
print("Verificam log-urile")
logs = run_select(
    "SELECT action FROM user_log ORDER BY id DESC LIMIT 3;")
for l in logs:
    print("-", l[0])
print("\nTEST TRIGGER FINALIZAT")