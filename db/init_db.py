# db/init_db.py
from db.sqlite import connect
from db.schema import SCHEMA_SQL

def init_db(db_path):
    conn = connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db("dados/app.db")
    print("OK: banco inicializado em dados/app.db")
