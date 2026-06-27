from pathlib import Path
import argparse
import json
import sqlite3
import subprocess
import sys


def run_command(command):
    print()
    print(">>>", " ".join(str(part) for part in command))

    completed = subprocess.run(command)

    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def count_table(db_path):
    conn = sqlite3.connect(db_path)

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name
              FROM sqlite_master
             WHERE type = 'table'
               AND name = 'rtd_underlying_quotes'
            """
        )

        if cur.fetchone() is None:
            return {
                "exists": False,
                "count": 0,
                "max_updated_at": None,
            }

        cur.execute(
            """
            SELECT COUNT(*), MAX(updated_at)
              FROM rtd_underlying_quotes
            """
        )

        row = cur.fetchone()

        return {
            "exists": True,
            "count": row[0] if row else 0,
            "max_updated_at": row[1] if row else None,
        }

    finally:
        conn.close()


def count_symbols_file(path):
    path = Path(path)

    if not path.exists():
        return 0, []

    symbols = [
        line.strip()
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if line.strip()
    ]

    return len(symbols), symbols


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline completo RTD para ativos-base."
    )
    parser.add_argument("--db", default="dados/app.db")
    parser.add_argument("--symbols", default="dados/rtd_underlying_symbols.txt")
    parser.add_argument("--csv", default="dados/RTD_UNDERLYING_QUOTES.csv")
    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
    parser.add_argument("--wait-seconds", type=int, default=25)
    parser.add_argument("--skip-excel", action="store_true")
    parser.add_argument("--visible", action="store_true")
    parser.add_argument("--allow-empty", action="store_true")

    args = parser.parse_args()

    root = Path.cwd()
    db_path = Path(args.db)
    symbols_path = Path(args.symbols)
    csv_path = Path(args.csv)
    workbook_path = Path(args.workbook)

    print("=== RTD Underlying Refresh Full ===")
    print("Root:", root)
    print("DB:", db_path)
    print("Symbols:", symbols_path)
    print("CSV:", csv_path)
    print("Workbook:", workbook_path)
    print("Skip Excel:", "SIM" if args.skip_excel else "NAO")

    if not db_path.exists():
        raise SystemExit(f"Banco nao encontrado: {db_path}")

    print()
    print("Estado antes:")
    print(json.dumps(count_table(db_path), ensure_ascii=False, indent=2))

    build_command = [
        sys.executable,
        "scripts/build_rtd_underlying_symbols.py",
        "--db",
        str(db_path),
        "--out",
        str(symbols_path),
    ]

    if args.allow_empty:
        build_command.append("--allow-empty")

    run_command(build_command)

    symbol_count, symbols = count_symbols_file(symbols_path)

    print()
    print(f"Ativos-base no arquivo: {symbol_count}")

    for symbol in symbols[:20]:
        print(f"- {symbol}")

    if len(symbols) > 20:
        print(f"... mais {len(symbols) - 20}")

    if symbol_count == 0 and not args.allow_empty:
        raise SystemExit("Nenhum ativo-base encontrado.")

    if not args.skip_excel:
        ps_command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(Path("scripts/refresh_rtd_underlying_quotes_excel.ps1").resolve()),
            "-WorkbookPath",
            str(workbook_path.resolve()),
            "-SymbolsPath",
            str(symbols_path.resolve()),
            "-CsvPath",
            str(csv_path.resolve()),
            "-WaitSeconds",
            str(args.wait_seconds),
        ]

        if args.visible:
            ps_command.append("-Visible")

        run_command(ps_command)

    import_command = [
        sys.executable,
        "scripts/import_rtd_underlying_quotes_csv.py",
        "--csv",
        str(csv_path),
        "--db",
        str(db_path),
        "--json",
    ]

    run_command(import_command)

    print()
    print("Estado depois:")
    print(json.dumps(count_table(db_path), ensure_ascii=False, indent=2))

    print()
    print("OK: pipeline RTD de ativos-base finalizado.")


if __name__ == "__main__":
    main()
