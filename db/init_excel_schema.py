# db/init_excel_schema.py

from db.sqlite import connect
from db.schema_excel import SCHEMA_EXCEL_SQL

def main():
    conn = connect()
    conn.executescript(SCHEMA_EXCEL_SQL)
    conn.commit()
    conn.close()
    print("OK: schema_excel aplicado")

if __name__ == "__main__":
    main()
