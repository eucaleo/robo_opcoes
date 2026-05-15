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

SCRIPTS = [
    "scripts/07_audit_snapshot_keys.py",
    "scripts/08_sanitize_audit_data.py",
    "scripts/09_check_database_consistency.py",
    "scripts/10_check_reports_consistency.py",
]


def archive_previous_summary() -> None:
    summary_file = BASE_DIR / "reports" / "smoke_summary.txt"
    if summary_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived = ATT_TEMP_DIR / f"smoke_summary_{timestamp}.txt"
        shutil.move(str(summary_file), str(archived))


def run_script(script: str) -> int:
    print(f"\n>>> Executando: {script}")
    result = subprocess.run([sys.executable, str(BASE_DIR / script)])
    print(f"<<< Exit code: {result.returncode}")
    return result.returncode


def main() -> int:
    archive_previous_summary()

    failures = []
    warnings = []

    for script in SCRIPTS:
        code = run_script(script)

        if code == 2:
            failures.append({"script": script, "exit_code": code})
        elif code == 1:
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
        summary_lines.append("Todos os smoke checks passaram com sucesso.")

    summary_file = BASE_DIR / "reports" / "smoke_summary.txt"
    summary_file.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    if warnings:
        print("\nWarnings detectados:")
        for item in warnings:
            print(f"- {item['script']}: exit_code={item['exit_code']}")

    if failures:
        print("\nFalhas detectadas:")
        for item in failures:
            print(f"- {item['script']}: exit_code={item['exit_code']}")
        return 1

    print("\nSmoke checks concluídos sem falha fatal.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
