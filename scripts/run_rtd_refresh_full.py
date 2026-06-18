import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, cwd=None, capture=False):
    print("")
    print(">>>", " ".join(str(x) for x in cmd))

    if capture:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.stdout:
            print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")

        if result.stderr:
            print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr)

        return result

    return subprocess.run(cmd, cwd=cwd)


def count_quotes(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    try:
        row = cur.execute("""
            SELECT
                COUNT(*),
                MAX(updated_at)
            FROM rtd_option_quotes
        """).fetchone()

        return {
            "count": row[0] if row else 0,
            "max_updated_at": row[1] if row else None,
        }
    except sqlite3.Error:
        return {
            "count": None,
            "max_updated_at": None,
        }
    finally:
        con.close()


def count_symbols_file(path):
    p = Path(path)

    if not p.exists():
        return 0, []

    symbols = [
        line.strip()
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip()
    ]

    return len(symbols), symbols


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
    )

    parser.add_argument("--db", default="dados/app.db")
    parser.add_argument("--symbols", default="dados/rtd_symbols.txt")
    parser.add_argument("--csv", default="dados/RTD_LINKS.csv")
    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
    parser.add_argument("--wait-seconds", type=int, default=25)
    parser.add_argument("--visible", action="store_true", default=True)
    parser.add_argument("--hidden", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Usa somente structure_legs como fonte de símbolos.")
    parser.add_argument("--skip-excel", action="store_true", help="Pula o refresh do Excel e importa o CSV existente.")
    parser.add_argument("--allow-empty", action="store_true", help="Permite lista vazia de símbolos.")
    parser.add_argument("--dry-run", action="store_true", help="Mostra o que faria, sem executar.")
    args = parser.parse_args()

    root = Path.cwd()

    db_path = Path(args.db)
    symbols_path = Path(args.symbols)
    csv_path = Path(args.csv)
    workbook_path = Path(args.workbook)

    build_script = Path("scripts/build_rtd_symbols.py")
    import_script = Path("scripts/import_rtd_option_quotes_wide_csv.py")
    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")

    print("=== RTD Refresh Full ===")
    print(f"Root: {root}")
    print(f"DB: {db_path}")
    print(f"Symbols: {symbols_path}")
    print(f"CSV: {csv_path}")
    print(f"Workbook: {workbook_path}")
    print(f"Modo strict: {'SIM' if args.strict else 'NÃO'}")
    print(f"Skip Excel: {'SIM' if args.skip_excel else 'NÃO'}")

    required = [build_script, import_script]

    if not args.skip_excel:
        required.append(ps1_script)

    missing = [str(p) for p in required if not p.exists()]

    if missing:
        print("")
        print("ERRO: arquivos obrigatórios não encontrados:")
        for item in missing:
            print(f"- {item}")
        return 1

    before = count_quotes(db_path)
    print("")
    print("Estado antes:")
    print(json.dumps(before, ensure_ascii=False, indent=2))

    build_cmd = [
        sys.executable,
        str(build_script),
        "--db",
        str(db_path),
        "--out",
        str(symbols_path),
    ]

    if args.strict:
        build_cmd += ["--no-existing-quotes", "--no-snapshots"]

    if args.allow_empty:
        build_cmd += ["--allow-empty"]

    if args.dry_run:
        print("")
        print("DRY-RUN: comandos que seriam executados:")
        print(" ".join(build_cmd))

        if not args.skip_excel:
            ps_cmd = [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ps1_script.resolve()),
                "-WorkbookPath",
                str(workbook_path.resolve()),
                "-SymbolsPath",
                str(symbols_path.resolve()),
                "-CsvPath",
                str(csv_path.resolve()),
                "-WaitSeconds",
                str(args.wait_seconds),
            ]

            if not args.hidden:
                ps_cmd.append("-Visible")

            print(" ".join(ps_cmd))

        import_cmd = [
            sys.executable,
            str(import_script),
            "--csv",
            str(csv_path),
            "--db",
            str(db_path),
            "--json",
        ]

        print(" ".join(import_cmd))
        return 0

    result = run_cmd(build_cmd)

    if result.returncode != 0:
        print("")
        print("Pipeline interrompido na geração de símbolos.")
        print("")
        print("Observação:")
        print("- Em modo --strict, isso é esperado se não houver registros em structure_legs.")
        print("- Cadastre uma estrutura pelo sistema ou rode sem --strict para usar fallback de rtd_option_quotes.")
        return result.returncode

    symbol_count, symbols = count_symbols_file(symbols_path)

    print("")
    print(f"Símbolos no arquivo: {symbol_count}")

    if symbol_count == 0 and not args.allow_empty:
        print("")
        print("Pipeline interrompido: nenhum símbolo para consultar no RTD.")
        return 2

    if symbols:
        print("Primeiros símbolos:")
        for symbol in symbols[:20]:
            print(f"- {symbol}")

        if len(symbols) > 20:
            print(f"... mais {len(symbols) - 20}")

    if not args.skip_excel:
        ps_cmd = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ps1_script.resolve()),
            "-WorkbookPath",
            str(workbook_path.resolve()),
            "-SymbolsPath",
            str(symbols_path.resolve()),
            "-CsvPath",
            str(csv_path.resolve()),
            "-WaitSeconds",
            str(args.wait_seconds),
        ]

        if not args.hidden:
            ps_cmd.append("-Visible")

        result = run_cmd(ps_cmd)

        if result.returncode != 0:
            print("")
            print("Pipeline interrompido no refresh Excel/RTD.")
            return result.returncode
    else:
        print("")
        print("Refresh Excel/RTD pulado por --skip-excel.")

    import_cmd = [
        sys.executable,
        str(import_script),
        "--csv",
        str(csv_path),
        "--db",
        str(db_path),
        "--json",
    ]

    result = run_cmd(import_cmd, capture=True)

    if result.returncode != 0:
        print("")
        print("Pipeline interrompido na importação do CSV.")
        return result.returncode

    after = count_quotes(db_path)

    print("")
    print("Estado depois:")
    print(json.dumps(after, ensure_ascii=False, indent=2))

    print("")
    print("OK: pipeline RTD finalizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
