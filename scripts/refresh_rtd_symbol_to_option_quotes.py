#!/usr/bin/env python
"""
Atualiza uma opção avulsa via RTD Excel e importa para rtd_option_quotes.

Fluxo:
    symbol -> arquivo temporário de símbolos -> refresh_rtd_option_quotes_excel.ps1
    -> CSV temporário -> import_rtd_option_quotes_wide_csv.py -> SQLite

Exemplo:
    python scripts/refresh_rtd_symbol_to_option_quotes.py --symbol PETRS424 --db dados/app.db --visible --json
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PS1_SCRIPT = PROJECT_ROOT / "scripts" / "refresh_rtd_option_quotes_excel.ps1"
IMPORT_SCRIPT = PROJECT_ROOT / "scripts" / "import_rtd_option_quotes_wide_csv.py"


def run_command(command: list[str], *, cwd: Path, timeout_seconds: int = 45) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "").strip() if isinstance(exc.stderr, str) else "",
            "json": None,
            "ok": False,
            "timeout": True,
            "timeout_seconds": timeout_seconds,
        }

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

    parsed_json: Any = None

    if stdout:
        try:
            parsed_json = json.loads(stdout)
        except json.JSONDecodeError:
            parsed_json = None

    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "json": parsed_json,
        "ok": completed.returncode == 0,
        "timeout": False,
        "timeout_seconds": timeout_seconds,
    }


def fetch_quote(db_path: Path, symbol: str) -> dict[str, Any] | None:
    if not db_path.exists():
        return None

    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row

        row = con.execute(
            """
            SELECT *
            FROM rtd_option_quotes
            WHERE UPPER(TRIM(codigo_opcao)) = UPPER(TRIM(?))
            ORDER BY updated_at DESC, id DESC
            LIMIT 1
            """,
            (symbol,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Atualiza uma opção avulsa via RTD Excel e importa para rtd_option_quotes."
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Código da opção. Exemplo: PETRS424",
    )

    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite. Padrão: dados/app.db",
    )

    parser.add_argument(
        "--workbook",
        default="LISTA_RTD.xlsm",
        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
    )

    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=10,
        help="Timeout/espera do RTD. Padrão: 10.",
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Deixa o Excel visível durante o refresh.",
    )

    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=45,
        help="Timeout máximo do processo PowerShell/Excel. Padrão: 45.",
    )

    parser.add_argument(
        "--keep-files",
        action="store_true",
        help="Não remove os arquivos temporários de símbolo/CSV.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime resultado consolidado em JSON.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    symbol = str(args.symbol or "").strip().upper()

    db_path = Path(args.db)
    workbook_path = Path(args.workbook)

    if not db_path.is_absolute():
        db_path = PROJECT_ROOT / db_path

    if not workbook_path.is_absolute():
        workbook_path = PROJECT_ROOT / workbook_path

    tmp_dir = PROJECT_ROOT / "dados"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    symbols_path = tmp_dir / f"rtd_symbols_probe_{symbol}.txt"
    csv_path = tmp_dir / f"RTD_LINKS_probe_{symbol}.csv"

    result: dict[str, Any] = {
        "status": "ok",
        "symbol": symbol,
        "db": str(db_path),
        "workbook": str(workbook_path),
        "symbols_path": str(symbols_path),
        "csv_path": str(csv_path),
        "wait_seconds": int(args.wait_seconds),
        "visible": bool(args.visible),
        "steps": {
            "refresh_excel": None,
            "import_csv": None,
        },
        "quote": None,
        "errors": [],
    }

    try:
        if not symbol:
            raise ValueError("symbol vazio.")

        if not PS1_SCRIPT.exists():
            raise FileNotFoundError(f"PowerShell não encontrado: {PS1_SCRIPT}")

        if not IMPORT_SCRIPT.exists():
            raise FileNotFoundError(f"Importador não encontrado: {IMPORT_SCRIPT}")

        if not workbook_path.exists():
            raise FileNotFoundError(f"Workbook não encontrado: {workbook_path}")

        symbols_path.write_text(symbol + "\n", encoding="utf-8")

        if csv_path.exists():
            csv_path.unlink()

        refresh_command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(PS1_SCRIPT),
            "-WorkbookPath",
            str(workbook_path),
            "-SymbolsPath",
            str(symbols_path),
            "-CsvPath",
            str(csv_path),
            "-WaitSeconds",
            str(int(args.wait_seconds)),
        ]

        if args.visible:
            refresh_command.append("-Visible")

        refresh_result = run_command(
            refresh_command,
            cwd=PROJECT_ROOT,
            timeout_seconds=int(args.timeout_seconds),
        )
        result["steps"]["refresh_excel"] = refresh_result

        if not refresh_result["ok"]:
            result["status"] = "error"
            result["errors"].append("refresh_excel step failed")
            raise RuntimeError("refresh_excel step failed")

        import_command = [
            sys.executable,
            str(IMPORT_SCRIPT),
            "--csv",
            str(csv_path),
            "--db",
            str(db_path),
            "--json",
        ]

        import_result = run_command(
            import_command,
            cwd=PROJECT_ROOT,
            timeout_seconds=30,
        )
        result["steps"]["import_csv"] = import_result

        if not import_result["ok"]:
            result["status"] = "error"
            result["errors"].append("import_csv step failed")
            raise RuntimeError("import_csv step failed")

        quote = fetch_quote(db_path, symbol)
        result["quote"] = quote

        if quote is None:
            result["status"] = "error"
            result["errors"].append(f"quote not found after refresh: {symbol}")
            raise RuntimeError(f"quote not found after refresh: {symbol}")

    except Exception as exc:
        if result["status"] == "ok":
            result["status"] = "error"

        if not result["errors"]:
            result["errors"].append(f"{type(exc).__name__}: {exc}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        else:
            print("Refresh RTD symbol -> rtd_option_quotes")
            print(f"Status: {result['status']}")
            print(f"Symbol: {symbol}")
            for error in result["errors"]:
                print(f"- {error}")

        return 1

    finally:
        if not args.keep_files:
            try:
                if symbols_path.exists():
                    symbols_path.unlink()
            except Exception:
                pass

            try:
                if csv_path.exists():
                    csv_path.unlink()
            except Exception:
                pass

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print("Refresh RTD symbol -> rtd_option_quotes")
        print("Status: ok")
        print(f"Symbol: {symbol}")

        quote = result.get("quote") or {}

        if quote:
            print(f"Ativo base: {quote.get('ativo_base')}")
            print(f"Tipo: {quote.get('call_put')}")
            print(f"Strike: {quote.get('strike')}")
            print(f"Vencimento: {quote.get('vencimento')}")
            print(f"Updated at: {quote.get('updated_at')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
