# validate_db.py
from db.sqlite import connect

conn = connect("dados/app.db")
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tabelas criadas:")
for table in tables:
    count = conn.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
    print(f"  {table[0]}: {count} linhas")
conn.close()
