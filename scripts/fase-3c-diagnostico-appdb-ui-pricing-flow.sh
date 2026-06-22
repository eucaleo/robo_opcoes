#!/usr/bin/env bash
set -euo pipefail

EVID_DIR="docs/checkpoints/evidencias"
OUT="$EVID_DIR/fase-3c-diagnostico-appdb-ui-pricing-flow.txt"

mkdir -p "$EVID_DIR"

{
    echo "== Fase 3C - Diagnostico app.db, UI e fluxo pricing/payoff =="
    echo
    echo "Data:"
    date
    echo

    echo "1) Branch e estado git"
    echo
    git branch --show-current
    git status --short
    git log --oneline -10
    echo

    echo "2) Inspecao de bancos app.db e derived.db"
    echo
    python - <<'PY'
from pathlib import Path
import sqlite3

for db_name in ["dados/app.db", "dados/derived.db"]:
    db = Path(db_name)
    print()
    print("=" * 80)
    print(f"DB: {db.resolve()}")
    print(f"existe: {db.exists()}")

    if not db.exists():
        continue

    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT name, type, sql
        FROM sqlite_master
        WHERE type IN ('table', 'view', 'index', 'trigger')
        ORDER BY type, name
    """)
    rows = cur.fetchall()

    print()
    print("Objetos:")
    for row in rows:
        print(f"{row['type']}: {row['name']}")

    print()
    print("Contagens principais:")
    for table in [
        "structures",
        "structure_legs",
        "structure_events",
        "structure_audit_log",
        "structure_snapshots",
        "structure_leg_snapshots",
        "pricing_executions",
        "payoff_curve_points",
        "structure_decisions",
        "rtd_option_quotes",
        "manual_analise_robo_legs",
        "rtd_analise_robo_legs",
    ]:
        try:
            cur.execute(f"SELECT COUNT(*) AS n FROM {table}")
            print(f"{table}: {cur.fetchone()['n']}")
        except Exception as exc:
            print(f"{table}: indisponivel ({exc})")

    print()
    print("Schema relacionado:")
    for row in rows:
        low = row["name"].lower()
        if any(t in low for t in ["structure", "leg", "pricing", "payoff", "decision", "rtd", "manual"]):
            print()
            print(f"-- {row['type']}: {row['name']}")
            print(row["sql"])

    print()
    print("Amostra structures com contagem de legs:")
    try:
        cur.execute("""
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
            ORDER BY s.id DESC
            LIMIT 20
        """)
        for row in cur.fetchall():
            print(dict(row))
    except Exception as exc:
        print(f"indisponivel ({exc})")

    conn.close()
PY
    echo

    echo "3) Trechos relevantes de UI/main_window.py"
    echo
    if [ -f "UI/main_window.py" ]; then
        grep -nE "_db_path|app.db|derived.db|StructuresListPanel|StructureEditorDialog|structure" UI/main_window.py | head -250 || true
        echo
        echo "---- UI/main_window.py inicio ----"
        sed -n '1,180p' UI/main_window.py
        echo
        echo "---- UI/main_window.py area estruturas candidata 1 ----"
        sed -n '180,420p' UI/main_window.py
        echo
        echo "---- UI/main_window.py area estruturas candidata 2 ----"
        sed -n '420,700p' UI/main_window.py
    else
        echo "UI/main_window.py nao encontrado"
    fi
    echo

    echo "4) Ocorrencias de passagem de db_path para componentes de estruturas"
    echo
    grep -RInE "StructureEditorDialog\\(|StructuresListPanel\\(|db_path=.*derived|db_path=.*app|_db_path" UI api services repositories ATT/tests \
        --include='*.py' \
        2>/dev/null \
        | grep -vE '__pycache__|.pytest_cache' \
        | head -500 || true
    echo

    echo "5) Smoke somente leitura: repository e canonical/pricing input"
    echo
    python - <<'PY'
from pathlib import Path
import sqlite3
import traceback

app_db = Path("dados/app.db")
print(f"app_db existe: {app_db.exists()} - {app_db.resolve()}")

if not app_db.exists():
    raise SystemExit(0)

try:
    from repositories.structures_repository import StructuresRepository

    repo = StructuresRepository(app_db)
    rows = repo.list_structures(include_archived=True)
    print(f"StructuresRepository.list_structures: {len(rows)} estruturas")

    candidate_id = None
    for row in rows:
        sid = row["id"]
        try:
            detail = repo.get_structure(sid)
            n_legs = len(detail.get("legs") or []) if detail else 0
            print(f"structure_id={sid} name={row.get('name')} n_legs={n_legs}")
            if candidate_id is None and n_legs > 0:
                candidate_id = sid
        except Exception as exc:
            print(f"erro lendo structure_id={sid}: {exc}")

    print(f"candidate_id_com_legs: {candidate_id}")

    if candidate_id is not None:
        print()
        print("Tentando CanonicalInputService.build_structure_market_input...")
        try:
            from services.canonical_input_service import CanonicalInputService
            svc = CanonicalInputService(repository=repo)
            canonical = svc.build_structure_market_input(candidate_id)
            print("canonical OK")
            print("structure:", canonical.get("structure"))
            print("market:", canonical.get("market"))
            print("meta:", canonical.get("meta"))
        except Exception:
            print("canonical ERRO")
            traceback.print_exc()

        print()
        print("Tentando PricingInputService.build_pricing_payload...")
        try:
            from services.pricing_input_service import PricingInputService
            from services.canonical_input_service import CanonicalInputService
            canonical_svc = CanonicalInputService(repository=repo)
            pricing_svc = PricingInputService(canonical_input_service=canonical_svc)
            payload = pricing_svc.build_pricing_payload(candidate_id)
            print("pricing payload OK")
            print(payload)
        except Exception:
            print("pricing payload ERRO")
            traceback.print_exc()

except Exception:
    print("smoke repository/canonical ERRO")
    traceback.print_exc()
PY
    echo

    echo "6) Testes focados UI main_window, editor, repository, canonical e pricing input"
    echo
    python -m pytest -q \
        ATT/tests/test_structure_editor_dialog.py \
        ATT/tests/test_structure_editor_integration.py \
        ATT/tests/test_structures_repository.py \
        ATT/tests/test_canonical_input_service.py \
        ATT/tests/test_pricing_input_service.py \
        ATT/tests/test_pricing_execution_app_service.py \
        ATT/tests/test_pricing_execution_orchestration_service.py \
        ATT/tests/test_pricing_execution_persistence_service.py \
        ATT/tests/test_pricing_execution_service.py \
        || true
    echo

    echo "== Fim do diagnostico Fase 3C =="
} > "$OUT" 2>&1

echo "$OUT"
tail -140 "$OUT"
