# salve como fix_db.py e execute: python fix_db.py
import sqlite3

conn = sqlite3.connect("dados/derived.db")
conn.row_factory = sqlite3.Row

antes = conn.execute(
    "SELECT id, aba, structure_id FROM structure_decisions WHERE structure_id IS NULL"
).fetchall()
print("ANTES:", [dict(r) for r in antes])

conn.execute("""
    UPDATE structure_decisions
    SET structure_id = CAST(
        REPLACE(aba, 'structure:', '') AS INTEGER
    )
    WHERE structure_id IS NULL
      AND aba LIKE 'structure:%'
""")
conn.commit()

depois = conn.execute(
    "SELECT id, aba, structure_id FROM structure_decisions WHERE id=58"
).fetchone()
print("DEPOIS:", dict(depois) if depois else "não encontrado")

n = conn.execute(
    "SELECT COUNT(*) as n FROM structure_decisions WHERE structure_id IS NULL"
).fetchone()["n"]
print(f"NULLs restantes: {n}")
conn.close()
