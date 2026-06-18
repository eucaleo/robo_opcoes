#!/usr/bin/env python
"""
Executa o pipeline operacional de cotações RTD de opções.

Fluxo:

    dados/RTD_LINKS.csv -> rtd_option_quotes -> auditoria

Uso típico:

    python scripts/run_rtd_option_quotes_pipeline.py
    python scripts/run_rtd_option_quotes_pipeline.py --csv dados/RTD_LINKS.csv --db dados/app.db
    python scripts/run_rtd_option_quotes_pipeline.py --dry-run
    python scripts/run_rtd_option_quotes_pipeline.py --fail-on-warn
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent

IMPORT_SCRIPT = SCRIPTS_DIR / "import_rtd_option_quotes_wide_csv.py"
AUDIT_SCRIPT = SCRIPTS_DIR / "audit_rtd_option_quotes.py"


def build_import_command(
    csv_path: str,
    db_path: str,
    dry_run: bool = False,
) -> list[str]:
    command = [
        sys.executable,
        str(IMPORT_SCRIPT),
        "--csv",
        csv_path,
        "--db",
        db_path,
    ]

    if dry_run:
        command.append("--dry-run")

    return command


def build_audit_command(
    db_path: str,
    max_age_minutes: int = 30,
    json_output: bool = False,
    fail_on_warn: bool = False,
) -> list[str]:
    command = [
        sys.executable,
        str(AUDIT_SCRIPT),
        "--db",
        db_path,
        "--max-age-minutes",
        str(int(max_age_minutes)),
    ]

    if json_output:
        command.append("--json")

    if fail_on_warn:
        command.append("--fail-on-warn")

    return command


def run_command(command: list[str]) -> int:
    completed = subprocess.run(command, cwd=REPO_ROOT)
    return int(completed.returncode)


def print_command(title: str, command: list[str]) -> None:
    print("")
    print(title)
    print("-" * len(title))
    print(" ".join(command))


def run_pipeline(
    csv_path: str = "dados/RTD_LINKS.csv",
    db_path: str = "dados/app.db",
    dry_run: bool = False,
    max_age_minutes: int = 30,
    json_audit: bool = False,
    fail_on_warn: bool = False,
) -> int:
    print("Pipeline RTD option quotes")
    print(f"CSV: {csv_path}")
    print(f"DB: {db_path}")
    print(f"Dry-run: {dry_run}")

    import_command = build_import_command(
        csv_path=csv_path,
        db_path=db_path,
        dry_run=dry_run,
    )

    print_command("Etapa 1 — Importação", import_command)
    import_code = run_command(import_command)

    if import_code != 0:
        print("")
        print(f"Pipeline interrompido: importador retornou código {import_code}.")
        return import_code

    if dry_run:
        print("")
        print("Pipeline concluído em dry-run. Auditoria não executada porque nada foi gravado.")
        return 0

    audit_command = build_audit_command(
        db_path=db_path,
        max_age_minutes=max_age_minutes,
        json_output=json_audit,
        fail_on_warn=fail_on_warn,
    )

    print_command("Etapa 2 — Auditoria", audit_command)
    audit_code = run_command(audit_command)

    if audit_code != 0:
        print("")
        print(f"Pipeline concluído com alerta/erro operacional. Auditor retornou código {audit_code}.")
        return audit_code

    print("")
    print("Pipeline concluído com sucesso.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Executa importação e auditoria de rtd_option_quotes."
    )
    parser.add_argument(
        "--csv",
        default="dados/RTD_LINKS.csv",
        help="Caminho do CSV RTD_LINKS.csv. Padrão: dados/RTD_LINKS.csv",
    )
    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite. Padrão: dados/app.db",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa somente validação/normalização do importador, sem gravar e sem auditar.",
    )
    parser.add_argument(
        "--max-age-minutes",
        type=int,
        default=30,
        help="Idade máxima esperada para updated_at na auditoria. Use 0 para desabilitar.",
    )
    parser.add_argument(
        "--json-audit",
        action="store_true",
        help="Executa a auditoria com saída JSON.",
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Faz o pipeline retornar falha quando a auditoria retornar warn.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    return run_pipeline(
        csv_path=args.csv,
        db_path=args.db,
        dry_run=args.dry_run,
        max_age_minutes=args.max_age_minutes,
        json_audit=args.json_audit,
        fail_on_warn=args.fail_on_warn,
    )


if __name__ == "__main__":
    raise SystemExit(main())
