import os
import sqlite3
import sys

symbol = sys.argv[1] if len(sys.argv) >= 2 else "PETRS424"
db_path = sys.argv[2] if len(sys.argv) >= 3 else "dados/app.db"

print("=== Diagnostico RTD option quote ===")
print("CWD:", os.getcwd())
print("DB informado:", db_path)
print("DB absoluto:", os.path.abspath(db_path))
print("Symbol:", symbol)

if not os.path.exists(db_path):
    print("ERRO: banco nao existe nesse caminho")
    raise SystemExit(1)

con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row

try:
    tables = con.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()

    table_names = [row["name"] for row in tables]

    print("")
    print("=== Tabelas encontradas ===")
    for name in table_names:
        print(name)

    if "rtd_option_quotes" not in table_names:
        print("")
        print("ERRO: tabela rtd_option_quotes nao existe neste banco")
        raise SystemExit(1)

    print("")
    print("=== Schema rtd_option_quotes ===")
    schema = con.execute("PRAGMA table_info(rtd_option_quotes)").fetchall()
    columns = [row["name"] for row in schema]

    for row in schema:
        print(dict(row))

    print("")
    print("Colunas:", columns)

    total = con.execute("SELECT COUNT(*) AS total FROM rtd_option_quotes").fetchone()["total"]
    print("")
    print("Total rtd_option_quotes:", total)

    print("")
    print("=== Primeiros registros da tabela ===")
    rows = con.execute("SELECT rowid, * FROM rtd_option_quotes LIMIT 50").fetchall()
    for row in rows:
        print(dict(row))

    if "codigo_opcao" not in columns:
        print("")
        print("ERRO: coluna codigo_opcao nao existe na tabela rtd_option_quotes")
        raise SystemExit(1)

    print("")
    print("=== Busca exata por codigo_opcao ===")
    rows = con.execute(
        "SELECT rowid, * FROM rtd_option_quotes WHERE codigo_opcao = ? LIMIT 20",
        (symbol,),
    ).fetchall()
    print("Qtd:", len(rows))
    for row in rows:
        print(dict(row))

    print("")
    print("=== Busca com UPPER/TRIM por codigo_opcao ===")
    rows = con.execute(
        """
        SELECT rowid, *
        FROM rtd_option_quotes
        WHERE UPPER(TRIM(CAST(codigo_opcao AS TEXT))) = UPPER(TRIM(?))
        LIMIT 20
        """,
        (symbol,),
    ).fetchall()
    print("Qtd:", len(rows))
    for row in rows:
        print(dict(row))

    print("")
    print("=== Busca parecida por prefixo ===")
    prefix = symbol[:5].upper()
    rows = con.execute(
        """
        SELECT rowid, *
        FROM rtd_option_quotes
        WHERE UPPER(CAST(codigo_opcao AS TEXT)) LIKE ?
        ORDER BY codigo_opcao
        LIMIT 50
        """,
        (f"%{prefix}%",),
    ).fetchall()
    print("Prefixo:", prefix)
    print("Qtd:", len(rows))
    for row in rows:
        print(dict(row))

finally:
    con.close()
