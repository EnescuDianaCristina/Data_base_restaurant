import json
from pathlib import Path
from app.db import run_select

sql = """
    SELECT
        i.id,
        COUNT(id) AS nr_ingr,
        AVG(i.nr_ingrediente) AS nr_ingrediente_avg
    FROM stoc i
    GROUP BY i.data_stocare
    ORDER BY nr_ingrediente_avg DESC;
"""

rows = run_select(sql)

data = []
for row in rows:
    data.append({
        'id': row[0],
        'nr_ingrediente_avg': row[1]
    })

out_path = Path("output") / "stoc_avg.json"
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"JSON salvat: {out_path}")