import json
import random
from app.db import get_connection, run_select

user_id = run_select("SELECT id FROM users WHERE username = %s;", ("admin",))[0][0]

mese = [
    {"sku": "SKU-001", "qty":2},
    {"sku": "SKU-002", "qty":1},
    {"sku": "SKU-003", "qty":3},
]
mese_json = json.dumps(mese)

numar_locuri = random.randint(1, 6)

print("Apelam procedura create_rezervare...")

conn = get_connection()
cur = conn.cursor()

try:
    cur.execute("CALL create_rezervare(%s, %s, %s);", (user_id, mese_json, numar_locuri))

    row = cur.fetchone()
    rezervare_id = row[0]

    while cur.nextset():
        if cur.description is not None:
            cur.fetchall()

    conn.commit()
    print("OK: Comanda creata, rezervare_id:", rezervare_id)

finally:
    cur.close()
    conn.close()

print("\nVerificare in DB (mese_rezervate):")
rows = run_select("""
SELECT oi.rezervare_id, oi.sku, oi.numar_locuri
FROM mese_rezervate oi
JOIN rezervari p ON p.id = oi.rezervare_id
WHERE oi.rezervare_id = %s
ORDER BY oi.sku;
""", (rezervare_id,))

for r in rows:
    print(r)