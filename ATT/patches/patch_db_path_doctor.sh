#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

mkdir -p scripts docs ATT/reports

cat > scripts/db_path_doctor.py <<'PY'
#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import json
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[1]

def _candidates(name: str):
    return [
        REPO_ROOT / "data" / name,
        REPO_ROOT / "Data" / name,
        REPO_ROOT / name,
        *sorted(REPO_ROOT.rglob(name)),
    ]

def resolve_db(name: str) -> dict:
    seen = set()
    cand = []
    for p in _candidates(name):
        p = p.resolve()
        if p in seen:
            continue
        seen.add(p)
        cand.append(p)

    exists = [p for p in cand if p.exists() and p.is_file()]
    chosen = exists[0] if exists else None

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT))
        except Exception:
            return str(p)

    return {
        "name": name,
        "chosen": str(chosen) if chosen else None,
        "chosen_rel": rel(chosen) if chosen else None,
        "all_found": [rel(p) for p in exists],
    }

def main():
    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(REPO_ROOT),
        "env": {
            "APP_DB_PATH": os.environ.get("APP_DB_PATH"),
            "DERIVED_DB_PATH": os.environ.get("DERIVED_DB_PATH"),
        },
        "resolution": {
            "app.db": resolve_db("app.db"),
            "derived.db": resolve_db("derived.db"),
        }
    }

    print("=== DB PATH DOCTOR ===")
    print(f"Repo: {REPO_ROOT}\n")

    for k in ["app.db", "derived.db"]:
        r = report["resolution"][k]
        print(f"- {k}")
        print(f"  escolhido: {r['chosen_rel'] or 'NÃO ENCONTRADO'}")
        if r["all_found"]:
            print(f"  encontrados: {', '.join(r['all_found'])}")
        print("")

    out = REPO_ROOT / "ATT" / "reports" / "db_paths_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Relatório: {out.relative_to(REPO_ROOT)}")

    app_rel = report["resolution"]["app.db"]["chosen_rel"]
    der_rel = report["resolution"]["derived.db"]["chosen_rel"]
    if app_rel and der_rel:
        print("\nSugestão (opcional) para padronizar via env:")
        print(f'  export APP_DB_PATH="{app_rel}"')
        print(f'  export DERIVED_DB_PATH="{der_rel}"')

    return 0 if report["resolution"]["app.db"]["chosen"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
PY

chmod +x scripts/db_path_doctor.py

cat > docs/DB_PATHS.md <<'DOC'
# DB Paths (Fonte da Verdade)

Fonte (MAPA MODULOS ABAS.pdf):
- Raw DB: `dados/app.db`
- Derived DB: `dados/derived.db`
- Bridge: `bridge/*.csv` + `bridge/last_export.txt`

Diagnóstico:
```bash
python scripts/db_path_doctor.py
DOC