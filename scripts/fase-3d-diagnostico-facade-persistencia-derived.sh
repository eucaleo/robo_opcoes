#!/usr/bin/env bash
set -euo pipefail

EVID_DIR="docs/checkpoints/evidencias"
OUT="$EVID_DIR/fase-3d-diagnostico-facade-persistencia-derived.txt"

mkdir -p "$EVID_DIR"

{
    echo "== Fase 3D - Diagnostico facade, pricing e persistencia derived =="
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

    echo "2) Trecho _reprice_structure_after_save em UI/main_window.py"
    echo
    sed -n '690,780p' UI/main_window.py || true
    echo

    echo "3) Ocorrencias CanonicalPricingFacade e persistencia payoff/decision"
    echo
    grep -RInE "class CanonicalPricingFacade|def .*price|def .*pricing|def .*persist|save_payoff|save_decision|structure_decisions|payoff_curve_points|PricingExecution|Derived|derived" \
        services repositories db domain UI scripts ATT/tests \
        --include='*.py' \
        2>/dev/null \
        | grep -vE '__pycache__|.pytest_cache' \
        | head -800 || true
    echo

    echo "4) Cabecalhos/trechos de arquivos principais"
    echo

    for f in \
        services/canonical_pricing_facade.py \
        services/derived_payoff_persistence.py \
        services/payoff_persistence_port.py \
        services/pricing_execution_app_service.py \
        services/pricing_execution_orchestration_service.py \
        services/pricing_execution_persistence_service.py \
        services/pricing_execution_service.py \
        db/derived_repo.py \
        services/derived_service.py
    do
        if [ -f "$f" ]; then
            echo
            echo "---- $f ----"
            sed -n '1,260p' "$f"
        else
            echo
            echo "---- $f nao encontrado ----"
        fi
    done
    echo

    echo "5) Introspeccao Python da CanonicalPricingFacade"
    echo
    python - <<'PY'
import inspect
import traceback

try:
    from services.canonical_pricing_facade import CanonicalPricingFacade

    print("Classe:", CanonicalPricingFacade)
    print("Assinatura __init__:", inspect.signature(CanonicalPricingFacade))

    print()
    print("Métodos públicos:")
    for name, obj in inspect.getmembers(CanonicalPricingFacade):
        if name.startswith("_"):
            continue
        if callable(obj):
            try:
                sig = inspect.signature(obj)
            except Exception:
                sig = "<?>"
            print(f"- {name}{sig}")

    print()
    print("Fonte da classe CanonicalPricingFacade:")
    print(inspect.getsource(CanonicalPricingFacade))

except Exception:
    print("ERRO na introspeccao da facade")
    traceback.print_exc()
PY
    echo

    echo "6) Estado antes da execucao controlada"
    echo
    python - <<'PY'
from pathlib import Path
import sqlite3

for db_name in ["dados/app.db", "dados/derived.db"]:
    print()
    print(f"DB: {db_name}")
    db = Path(db_name)
    print("existe:", db.exists())
    if not db.exists():
        continue

    con = sqlite3.connect(str(db))
    cur = con.cursor()
    for table in [
        "structures",
        "structure_legs",
        "pricing_executions",
        "structure_snapshots",
        "structure_leg_snapshots",
        "payoff_curve_points",
        "structure_decisions",
    ]:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            print(f"{table}: {cur.fetchone()[0]}")
        except Exception as exc:
            print(f"{table}: indisponivel ({exc})")
    con.close()
PY
    echo

    echo "7) Execucao controlada em COPIAS dos bancos"
    echo
    python - <<'PY'
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import os
import textwrap

root = Path.cwd()
tmp_dir = root / "docs" / "checkpoints" / "evidencias" / "_fase3d_tmp"
tmp_dir.mkdir(parents=True, exist_ok=True)

src_app = root / "dados" / "app.db"
src_derived = root / "dados" / "derived.db"
tmp_app = tmp_dir / "app_fase3d.db"
tmp_derived = tmp_dir / "derived_fase3d.db"

if src_app.exists():
    shutil.copy2(src_app, tmp_app)
if src_derived.exists():
    shutil.copy2(src_derived, tmp_derived)

print("tmp_app:", tmp_app)
print("tmp_derived:", tmp_derived)

code = r'''
from pathlib import Path
import inspect
import sqlite3
import traceback
import json

app_db = Path(r"__TMP_APP__")
derived_db = Path(r"__TMP_DERIVED__")

print("APP_DB_PATH runtime:", app_db)
print("DERIVED_DB_PATH runtime:", derived_db)

def count_table(db, table):
    try:
        con = sqlite3.connect(str(db))
        cur = con.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        n = cur.fetchone()[0]
        con.close()
        return n
    except Exception as exc:
        return f"ERR: {exc}"

print()
print("Contagens antes:")
for db, tables in [
    (app_db, ["pricing_executions", "structure_snapshots", "structure_leg_snapshots"]),
    (derived_db, ["payoff_curve_points", "structure_decisions"]),
]:
    print("DB", db)
    for t in tables:
        print(t, count_table(db, t))

try:
    from repositories.structures_repository import StructuresRepository
    repo = StructuresRepository(app_db)
    rows = repo.list_structures(include_archived=True)
    print()
    print("structures:", rows)

    candidate_id = None
    for row in rows:
        detail = repo.get_structure(row["id"])
        n_legs = len((detail or {}).get("legs") or [])
        print("candidate?", row["id"], row["name"], "legs", n_legs)
        if candidate_id is None and n_legs > 0:
            candidate_id = row["id"]

    print("candidate_id:", candidate_id)

    if candidate_id is None:
        raise SystemExit("Sem estrutura com legs para teste")

    from services.canonical_pricing_facade import CanonicalPricingFacade
    facade = CanonicalPricingFacade(db_path=app_db)

    print()
    print("Facade instance:", facade)

    methods = []
    for name in dir(facade):
        if name.startswith("_"):
            continue
        attr = getattr(facade, name)
        if callable(attr):
            try:
                sig = inspect.signature(attr)
            except Exception:
                sig = None
            methods.append((name, sig))

    print("Métodos públicos da instância:")
    for name, sig in methods:
        print("-", name, sig)

    preferred_names = [
        "price_structure",
        "price_and_persist",
        "execute",
        "run",
        "reprice_structure",
        "calculate",
        "calculate_structure",
        "run_pricing",
        "price",
    ]

    called = False
    for name in preferred_names:
        if not hasattr(facade, name):
            continue

        fn = getattr(facade, name)
        sig = inspect.signature(fn)
        print()
        print(f"Tentando chamar facade.{name}{sig}")

        try:
            kwargs = {}
            params = sig.parameters

            if "structure_id" in params:
                kwargs["structure_id"] = candidate_id
            elif len(params) == 1:
                # método bound com 1 parâmetro posicional provável
                result = fn(candidate_id)
                print("RESULT:", result)
                called = True
                break
            else:
                print("SKIP: assinatura nao reconhecida")
                continue

            result = fn(**kwargs)
            print("RESULT:", result)
            called = True
            break

        except Exception:
            print(f"ERRO chamando {name}:")
            traceback.print_exc()

    if not called:
        print()
        print("Nenhum método preferencial foi chamado. Verifique nomes acima.")

except Exception:
    print("ERRO geral na execução controlada:")
    traceback.print_exc()

print()
print("Contagens depois:")
for db, tables in [
    (app_db, ["pricing_executions", "structure_snapshots", "structure_leg_snapshots"]),
    (derived_db, ["payoff_curve_points", "structure_decisions"]),
]:
    print("DB", db)
    for t in tables:
        print(t, count_table(db, t))

print()
print("Amostras depois:")
for db, table in [
    (app_db, "pricing_executions"),
    (app_db, "structure_snapshots"),
    (derived_db, "payoff_curve_points"),
    (derived_db, "structure_decisions"),
]:
    print()
    print("TABLE", db, table)
    try:
        con = sqlite3.connect(str(db))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT 5")
        for row in cur.fetchall():
            print(dict(row))
        con.close()
    except Exception as exc:
        print("ERR:", exc)
'''

code = code.replace("__TMP_APP__", str(tmp_app))
code = code.replace("__TMP_DERIVED__", str(tmp_derived))

env = os.environ.copy()
env["APP_DB_PATH"] = str(tmp_app)
env["DERIVED_DB_PATH"] = str(tmp_derived)

res = subprocess.run(
    [sys.executable, "-c", code],
    cwd=str(root),
    env=env,
    capture_output=True,
    text=True,
)

print("RETURN_CODE:", res.returncode)
print()
print("STDOUT:")
print(res.stdout)
print()
print("STDERR:")
print(res.stderr)
PY
    echo

    echo "8) Testes focados facade/persistencia/derived"
    echo
    python -m pytest -q \
        ATT/tests/test_canonical_pricing_facade.py \
        ATT/tests/test_pricing_execution_app_service.py \
        ATT/tests/test_pricing_execution_orchestration_service.py \
        ATT/tests/test_pricing_execution_persistence_service.py \
        ATT/tests/test_pricing_execution_service.py \
        ATT/tests/test_system_snapshots_repository.py \
        ATT/tests/test_system_snapshots_schema.py \
        || true
    echo

    echo "== Fim do diagnostico Fase 3D =="
} > "$OUT" 2>&1

echo "$OUT"
tail -180 "$OUT"
