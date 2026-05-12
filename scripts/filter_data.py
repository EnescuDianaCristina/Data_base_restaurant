import json
from pathlib import Path
from app.db import run_select
from scripts.select_all import out_path

DENUMIRE = "porc a la inginer"

sql = """
SELECT
    p.id,
    p.nume_reteta
FROM retete p
LEFT JOIN retete r ON r.id = p.id
GROUP BY p.id, p.nume_reteta
HAVING nume_reteta >= %s
ORDER BY nume_reteta DESC;
"""

rows = run_select(sql, (DENUMIRE,))

data = []
for r in rows:
    data.append({
        "sku": r[0],
        "nume": r[1]
    })

out_path = Path("output") / "retete_filtrate.json"
out_path.write_text(json.dumps({
    "ingrediente": DENUMIRE,
    "results": data
}, indent=2, ensure_ascii=False), encoding="utf-8")

print (f"JSON salvat: {out_path}")