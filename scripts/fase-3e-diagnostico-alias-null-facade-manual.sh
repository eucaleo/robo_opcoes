#!/usr/bin/env bash
set -euo pipefail

EVID_DIR="docs/checkpoints/evidencias"
OUT="$EVID_DIR/fase-3e-diagnostico-alias-null-facade-manual.txt"

mkdir -p "$EVID_DIR"

{
    echo "== Fase 3E - Diagnostico alias null e facade manual =="
    echo
    date
    echo

    echo "1) Branch e git"
    git branch --show-current
    git status --short
    git log --oneline -8
    echo

    echo "2) Estruturas cadastradas"
    python - <<'PY'
from pathlib import Path
import sqlite3

db = Path("dados/app.db")
print("app.db:", db.resolve(), "existe:", db.exists())

con = sqlite3.connect(str(db))
con.row_factory = sqlite3.Row

rows = con.execute("""
    SELECT
        s.id,
        s.name,
        s.underlying_asset,
        s.alias_legacy_aba,
        s.status,
        COUNT(l.id) AS n_legs
    FROM structures s
    LEFT JOIN structure_legs l ON l.structure_id = s.id
    GROUP BY s.id
    ORDER BY s.id
""").fetchall()

for r in rows:
    print(dict(r))

con.close()
PY
    echo

    echo "3) Chamada direta CanonicalPricingFacade.execute_pricing no banco real"
    python - <<'PY'
from pathlib import Path
import json
import sqlite3
import traceback

from services.canonical_pricing_facade import CanonicalPricingFacade

db = Path("dados/app.db")

con = sqlite3.connect(str(db))
con.row_factory = sqlite3.Row
row = con.execute("""
    SELECT s.id
    FROM structures s
    JOIN structure_legs l ON l.structure_id = s.id
    GROUP BY s.id
    HAVING COUNT(l.id) > 0
    ORDER BY s.id
    LIMIT 1
""").fetchone()
con.close()

if not row:
    raise SystemExit("Sem estrutura com legs.")

sid = int(row["id"])
print("structure_id:", sid)

try:
    facade = CanonicalPricingFacade(db_path=db)
    result = facade.execute_pricing(sid)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
except Exception:
    traceback.print_exc()
PY
    echo

    echo "4) Chamada direta PricingInputService para mesma estrutura"
    python - <<'PY'
from pathlib import Path
import json
import sqlite3
import inspect
import traceback

try:
    from services.pricing_input_service import PricingInputService

    db = Path("dados/app.db")

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    row = con.execute("""
        SELECT s.id
        FROM structures s
        JOIN structure_legs l ON l.structure_id = s.id
        GROUP BY s.id
        HAVING COUNT(l.id) > 0
        ORDER BY s.id
        LIMIT 1
    """).fetchone()
    con.close()

    sid = int(row["id"])
    print("PricingInputService signature:", inspect.signature(PricingInputService))

    try:
        svc = PricingInputService(db_path=db)
    except TypeError:
        svc = PricingInputService()

    print("instance:", svc)
    print("build_pricing_payload signature:", inspect.signature(svc.build_pricing_payload))

    payload = svc.build_pricing_payload(structure_id=sid)
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))

except Exception:
    traceback.print_exc()
PY
    echo

    echo "5) Trechos relevantes"
    echo
    grep -RIn "alias_legacy_aba is null\|def _get_structure_info\|class CanonicalPricingFacade\|def execute_pricing" services/canonical_pricing_facade.py services/pricing_input_service.py services/canonical_input_service.py 2>/dev/null || true
    echo
    sed -n '1,430p' services/canonical_pricing_facade.py
    echo

    echo "== Fim Fase 3E diagnostico =="
} > "$OUT" 2>&1

echo "$OUT"
tail -160 "$OUT"
