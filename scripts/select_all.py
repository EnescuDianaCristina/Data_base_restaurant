import json
from pathlib import Path
from app.db import run_select

sql = """
SELECT
    p.id,
    p.nume_reteta,
    p.id_ingrediente_reteta
FROM retete p
LEFT JOIN retete r ON r.id = p.id
GROUP BY p.id, p.nume_reteta, p.id_ingrediente_reteta;
"""

rows = run_select(sql)

data = []
for r in rows:
    data.append({
        "id": r[0],
        "nume": r[1],
        "reteta": r[2]
    })

out_path = Path("output") / "retete.json"
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding ="utf-8"
)
print(f"JSON salvat: {out_path}")