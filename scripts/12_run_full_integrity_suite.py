#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ATT_TEMP_DIR = BASE_DIR / "ATT" / "temporario"
ATT_TEMP_DIR.mkdir(parents=True, exist_ok=True)

PIPELINE = [
    "scripts/07_audit_snapshot_keys.py",
    "scripts/08_sanitize_audit_data.py",
    "scripts/09_check_database_consistency.py",
    "scripts/10_check_reports_consistency.py",
    "scripts/11_smoke_validate_system.py",
]


def archive_previous_summary() -> None:
    summary_file = BASE_DIR / "reports" / "full_integrity_summary.txt"
    if summary_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived = ATT_TEMP_DIR / f"full_integrity_summary_{timestamp}.txt"
        shutil.move(str(summary_file), str(archived))


def main() -> int:
    archive_previous_summary()

    warnings = []
    failures = []

    for script in PIPELINE:
        print(f"\n===== Executando {script} =====")
        result = subprocess.run([sys.executable, str(BASE_DIR / script)])
        code = result.returncode

        if code == 2:
            failures.append({"script": script, "exit_code": code})
            print(f"\nPipeline interrompido em {script} com erro técnico {code}")
            break

        if code == 1:
            warnings.append({"script": script, "exit_code": code})

    summary_lines = []

    if warnings:
        summary_lines.append("WARNINGS:")
        for item in warnings:
            summary_lines.append(f"- {item['script']}: exit_code={item['exit_code']}")

    if failures:
        summary_lines.append("FAILURES:")
        for item in failures:
            summary_lines.append(f"- {item['script']}: exit_code={item['exit_code']}")

    if not warnings and not failures:
        summary_lines.append("Suite completa executada com sucesso.")

    summary_file = BASE_DIR / "reports" / "full_integrity_summary.txt"
    summary_file.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    if failures:
        return 1

    print("\nSuite completa executada sem falha fatal.")
    if warnings:
        print("Há warnings pendentes, revisar relatórios.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
