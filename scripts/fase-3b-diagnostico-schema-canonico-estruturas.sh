#!/usr/bin/env bash
set -euo pipefail

EVID_DIR="docs/checkpoints/evidencias"
OUT="$EVID_DIR/fase-3b-diagnostico-schema-canonico-estruturas.txt"

mkdir -p "$EVID_DIR"

{
    echo "== Fase 3B - Diagnostico schema canonico de estruturas =="
    echo
    echo "Data:"
    date
    echo

    echo "1) Branch e estado git"
    echo
    git branch --show-current
    git status --short
    git log --oneline -8
    echo

    echo "2) Localizacao de definicoes CREATE TABLE structures e structure_legs"
    echo
    grep -RInE "CREATE TABLE.*structures|CREATE TABLE.*structure_legs|CREATE TABLE IF NOT EXISTS.*structures|CREATE TABLE IF NOT EXISTS.*structure_legs" . \
        --include='*.py' \
        --include='*.sql' \
        --include='*.md' \
        2>/dev/null \
        | grep -vE '/.git/|__pycache__|.pytest_cache|docs/checkpoints/evidencias' || true
    echo

    echo "3) Localizacao de bootstrap_structures_schema"
    echo
    grep -RInE "bootstrap_structures_schema|ensure.*structure|create.*structure|structure_legs" . \
        --include='*.py' \
        2>/dev/null \
        | grep -vE '/.git/|__pycache__|.pytest_cache|docs/checkpoints/evidencias' \
        | head -500 || true
    echo

    echo "4) Arquivos principais - cabecalhos e pontos relevantes"
    echo

    for file in \
        "infra/bootstrap_structures_schema.py" \
        "repositories/structures_repository.py" \
        "api/structures_controller.py" \
        "UI/components/structure_editor_dialog.py" \
        "UI/components/structures_list_panel.py" \
        "services/canonical_input_service.py" \
        "services/structure_market_input_assembler.py" \
        "services/pricing_input_service.py" \
        "services/derived_service.py" \
        "scripts/run_derived_pipeline.py"
    do
        echo
        echo "---- $file ----"
        if [ -f "$file" ]; then
            sed -n '1,260p' "$file"
        else
            echo "Arquivo nao encontrado"
        fi
    done
    echo

    echo "5) Caminhos de banco configurados no projeto"
    echo
    grep -RInE "derived.db|DB_PATH|DATABASE|sqlite3.connect|dados/" . \
        --include='*.py' \
        --include='*.md' \
        --include='*.env' \
        2>/dev/null \
        | grep -vE '/.git/|__pycache__|.pytest_cache|docs/checkpoints/evidencias' \
        | head -500 || true
    echo

    echo "6) Inspecao detalhada do banco dados/derived.db antes de qualquer alteracao"
    echo
    python - <<'PY'
from pathlib import Path
import sqlite3

db = Path("dados/derived.db")
print(f"DB: {db.resolve()}")
print(f"existe: {db.exists()}")

if not db.exists():
    raise SystemExit(0)

conn = sqlite3.connect(str(db))
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("select name, type, sql from sqlite_master where type in ('table', 'view', 'index', 'trigger') order by type, name")
rows = cur.fetchall()

print()
print("Objetos encontrados:")
for row in rows:
    print(f"{row['type']}: {row['name']}")

print()
print("SQL dos objetos relacionados:")
for row in rows:
    name = row["name"].lower()
    sql = row["sql"] or ""
    if any(term in name for term in ["structure", "leg", "payoff", "decision", "rtd", "quote"]):
        print()
        print(f"-- {row['type']}: {row['name']}")
        print(sql)

conn.close()
PY
    echo

    echo "7) Testes especificos de repository, api e editor de estruturas"
    echo
    python -m pytest ATT/tests/test_structures_repository.py ATT/tests/test_structures_api.py ATT/tests/test_structures_legs_endpoints.py ATT/tests/test_structure_editor_dialog.py ATT/tests/test_structure_editor_integration.py -q || true
    echo

    echo "== Fim do diagnostico Fase 3B =="
} > "$OUT" 2>&1

echo "$OUT"
tail -120 "$OUT"
