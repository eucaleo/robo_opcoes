import os
import sqlite3
import sys

symbol = sys.argv[1] if len(sys.argv) >= 2 else "PETRS424"
root = sys.argv[2] if len(sys.argv) >= 3 else "."

ignored_dirs = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
}

db_extensions = (".db", ".sqlite", ".sqlite3")

def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'

def is_text_candidate(col_type):
    t = (col_type or "").upper()
    return (
        t == ""
        or "TEXT" in t
        or "CHAR" in t
        or "CLOB" in t
        or "VARCHAR" in t
    )

print("=== Localizador de option quote em bancos SQLite ===")
print("Root:", os.path.abspath(root))
print("Symbol:", symbol)

db_files = []

for current_root, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in ignored_dirs]

    for file_name in files:
        lower = file_name.lower()
        if lower.endswith(db_extensions):
            db_files.append(os.path.join(current_root, file_name))

print("")
print("Bancos encontrados:", len(db_files))

if not db_files:
    print("Nenhum arquivo .db, .sqlite ou .sqlite3 encontrado")
    raise SystemExit(0)

found_any = False

for db_path in sorted(db_files):
    print("")
    print("============================================================")
    print("DB:", db_path)
    print("Absoluto:", os.path.abspath(db_path))

    try:
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
    except Exception as exc:
        print("Nao abriu:", repr(exc))
        continue

    try:
        tables = con.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()

        table_names = [row["name"] for row in tables]
        print("Tabelas:", table_names)

        if "rtd_option_quotes" in table_names:
            try:
                total = con.execute(
                    "SELECT COUNT(*) AS total FROM rtd_option_quotes"
                ).fetchone()["total"]
                print("Total rtd_option_quotes:", total)

                sample = con.execute(
                    "SELECT rowid, * FROM rtd_option_quotes LIMIT 20"
                ).fetchall()

                print("Amostra rtd_option_quotes:")
                for row in sample:
                    print(dict(row))
            except Exception as exc:
                print("Erro lendo rtd_option_quotes:", repr(exc))

        for table in table_names:
            try:
                cols = con.execute(
                    "PRAGMA table_info(" + quote_identifier(table) + ")"
                ).fetchall()
            except Exception:
                continue

            for col in cols:
                col_name = col["name"]
                col_type = col["type"]

                if not is_text_candidate(col_type):
                    continue

                table_q = quote_identifier(table)
                col_q = quote_identifier(col_name)

                sql = (
                    "SELECT * FROM " + table_q +
                    " WHERE UPPER(TRIM(CAST(" + col_q + " AS TEXT))) = UPPER(TRIM(?))" +
                    " OR UPPER(CAST(" + col_q + " AS TEXT)) LIKE ?" +
                    " LIMIT 20"
                )

                try:
                    rows = con.execute(
                        sql,
                        (symbol, "%" + symbol.upper() + "%"),
                    ).fetchall()
                except Exception:
                    continue

                if rows:
                    found_any = True
                    print("")
                    print("ACHOU POSSIVEL MATCH")
                    print("DB:", db_path)
                    print("Tabela:", table)
                    print("Coluna:", col_name)
                    print("Qtd:", len(rows))
                    for row in rows:
                        print(dict(row))

    finally:
        con.close()

print("")
print("============================================================")
if found_any:
    print("Resultado: encontrou pelo menos um match")
else:
    print("Resultado: nao encontrou o symbol em nenhum banco SQLite varrido")
