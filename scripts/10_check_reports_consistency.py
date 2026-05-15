#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"

EXPECTED_REPORTS = [
    "audit_snapshot_keys.json",
    "sanitize_audit_data.json",
    "database_consistency.json",
]


def main() -> int:
    issues = []

    if not REPORTS_DIR.exists():
        print(f"ERRO: diretório de relatórios não encontrado: {REPORTS_DIR}", file=sys.stderr)
        return 2

    for report_name in EXPECTED_REPORTS:
        path = REPORTS_DIR / report_name
        if not path.exists():
            issues.append({
                "file": report_name,
                "type": "missing_report",
                "details": "Arquivo não encontrado.",
            })
            continue

        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append({
                "file": report_name,
                "type": "invalid_json",
                "details": str(exc),
            })

    output = {
        "reports_dir": str(REPORTS_DIR),
        "issues": issues,
    }

    output_file = REPORTS_DIR / "reports_consistency.json"
    output_file.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Relatório salvo em: {output_file}")
    print(f"Issues encontradas: {len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
