#!/usr/bin/env python
"""
Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.

Executa:
    1. scripts/import_lista_rtd_excel_to_option_quotes.py
    2. scripts/audit_rtd_option_quotes.py

Uso:
    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS
    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS --json
    python scripts/run_lista_rtd_option_quotes_pipeline.py --dry-run --json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


IMPORT_SCRIPT = Path("scripts/import_lista_rtd_excel_to_option_quotes.py")
AUDIT_SCRIPT = Path("scripts/audit_rtd_option_quotes.py")


def run_command(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )

    parsed_json: Any = None

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

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
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
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
        "--sheet",
        default=None,
        help=(
            "Aba RTD. Se omitida, o importador tenta RTD_OPTION_QUOTES "
            "e depois RTD_PROBE_OPTIONS."
        ),
    )

    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=5,
        help="Espera após abrir o workbook. Padrão: 5.",
    )

    parser.add_argument(
        "--max-age-minutes",
        type=int,
        default=30,
        help="Idade máxima permitida para updated_at na auditoria. Padrão: 30.",
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Deixa o Excel visível durante a importação.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa a importação em dry-run e não roda auditoria final.",
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

    result: dict[str, Any] = {
        "status": "ok",
        "db": args.db,
        "workbook": args.workbook,
        "sheet": args.sheet,
        "dry_run": bool(args.dry_run),
        "steps": {
            "import": None,
            "audit": None,
        },
        "errors": [],
    }

    if not IMPORT_SCRIPT.exists():
        result["status"] = "error"
        result["errors"].append(f"script not found: {IMPORT_SCRIPT}")

    if not AUDIT_SCRIPT.exists():
        result["status"] = "error"
        result["errors"].append(f"script not found: {AUDIT_SCRIPT}")

    if result["errors"]:
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        else:
            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
            print("Status: error")
            for error in result["errors"]:
                print(f"- {error}")
        return 1

    import_command = [
        sys.executable,
        str(IMPORT_SCRIPT),
        "--db",
        args.db,
        "--workbook",
        args.workbook,
        "--wait-seconds",
        str(int(args.wait_seconds)),
        "--json",
    ]

    if args.sheet:
        import_command.extend(["--sheet", args.sheet])

    if args.visible:
        import_command.append("--visible")

    if args.dry_run:
        import_command.append("--dry-run")

    import_result = run_command(import_command)
    result["steps"]["import"] = import_result

    if not import_result["ok"]:
        result["status"] = "error"
        result["errors"].append("import step failed")

    if not args.dry_run and import_result["ok"]:
        audit_command = [
            sys.executable,
            str(AUDIT_SCRIPT),
            "--db",
            args.db,
            "--max-age-minutes",
            str(int(args.max_age_minutes)),
            "--fail-on-warn",
            "--json",
        ]

        audit_result = run_command(audit_command)
        result["steps"]["audit"] = audit_result

        if not audit_result["ok"]:
            result["status"] = "error"
            result["errors"].append("audit step failed")

    if args.dry_run:
        result["steps"]["audit"] = {
            "skipped": True,
            "reason": "dry-run mode",
        }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
        print(f"Status: {result['status']}")
        print(f"DB: {args.db}")
        print(f"Workbook: {args.workbook}")
        print(f"Aba: {args.sheet or '(auto)'}")
        print(f"Dry-run: {'sim' if args.dry_run else 'não'}")
        print("")

        import_json = import_result.get("json") or {}
        import_stats = import_json.get("stats") or {}

        print("Importação:")
        print(f"- returncode: {import_result['returncode']}")

        if import_stats:
            for key, value in import_stats.items():
                print(f"- {key}: {value}")

        audit_step = result["steps"].get("audit")

        if audit_step and not audit_step.get("skipped"):
            audit_json = audit_step.get("json") or {}
            audit_metrics = audit_json.get("metrics") or {}

            print("")
            print("Auditoria:")
            print(f"- returncode: {audit_step['returncode']}")
            print(f"- status: {audit_json.get('status')}")

            if audit_metrics:
                for key in sorted(audit_metrics):
                    print(f"- {key}: {audit_metrics[key]}")

        elif audit_step and audit_step.get("skipped"):
            print("")
            print("Auditoria:")
            print("- skipped: dry-run mode")

        if result["errors"]:
            print("")
            print("Erros:")
            for error in result["errors"]:
                print(f"- {error}")

    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
