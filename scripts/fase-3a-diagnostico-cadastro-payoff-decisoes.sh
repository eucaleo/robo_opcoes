#!/usr/bin/env bash
set -euo pipefail

EVID_DIR="docs/checkpoints/evidencias"
OUT="$EVID_DIR/fase-3a-diagnostico-cadastro-payoff-decisoes.txt"

mkdir -p "$EVID_DIR"

{
    echo "== Fase 3A - Diagnostico cadastro manual, payoff e decisoes =="
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

    echo "2) Arquivos candidatos relacionados ao fluxo"
    echo
    find . \
        -path './.git' -prune -o \
        -path './.venv' -prune -o \
        -path './venv' -prune -o \
        -path './__pycache__' -prune -o \
        -type f \( -name '*.py' -o -name '*.md' \) -print \
        | sed 's#^\./##' \
        | grep -Ei 'structure|estrutura|payoff|decision|decis|pipeline|rtd|repository|service|dialog|editor|manual|leg' \
        | sort \
        | head -300
    echo

    echo "3) Ocorrencias relevantes no codigo"
    echo
    grep -RInE "structure_decisions|payoff_curve_points|manual|Manual|payoff|decision|decis|canonical|structure_id|Salvar|Aplicar Leg|must be numeric" . \
        --include='*.py' \
        --include='*.md' \
        2>/dev/null \
        | grep -vE '/.git/|__pycache__|.pytest_cache|docs/checkpoints/evidencias' \
        | head -500 || true
    echo

    echo "4) Diagnostico do banco dados/derived.db"
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

print()
print("Tabelas/views relacionadas:")
cur.execute("select name, type from sqlite_master where type in ('table', 'view') order by name")
objetos = cur.fetchall()

for row in objetos:
    name = row["name"]
    low = name.lower()
    if any(term in low for term in ["structure", "estrutura", "leg", "payoff", "decision", "decis", "rtd", "quote"]):
        print(f"{row['type']}: {name}")

print()
print("Contagens principais:")
for table in [
    "structures",
    "structure_legs",
    "legs",
    "payoff_curve_points",
    "structure_decisions",
    "rtd_option_quotes",
]:
    try:
        cur.execute(f"select count(*) as n from {table}")
        print(f"{table}: {cur.fetchone()['n']}")
    except Exception as exc:
        print(f"{table}: indisponivel ({exc})")

print()
print("Schema resumido de estruturas, legs, payoff e decisoes:")
for row in objetos:
    name = row["name"]
    low = name.lower()
    if any(term in low for term in ["structure", "estrutura", "leg", "payoff", "decision", "decis"]):
        try:
            cur.execute(f"pragma table_info({name})")
            cols = ", ".join([col["name"] for col in cur.fetchall()])
            print(f"{name}: {cols}")
        except Exception as exc:
            print(f"{name}: schema indisponivel ({exc})")

conn.close()
PY
    echo

    echo "5) Testes candidatos existentes"
    echo
    python - <<'PY'
from pathlib import Path

terms = ("structure", "estrutura", "payoff", "decision", "decis", "manual", "leg")
roots = [Path("tests"), Path("ATT/tests")]

for root in roots:
    if root.exists():
        print()
        print(root)
        for path in sorted(root.rglob("test*.py")):
            low = str(path).lower()
            if any(term in low for term in terms):
                print(path)
PY
    echo

    echo "6) Pytest focado em cadastro, structure, payoff, decision e leg"
    echo
    python -m pytest -q -k "manual or structure or payoff or decision or leg" || true
    echo

    echo "== Fim do diagnostico Fase 3A =="
} > "$OUT" 2>&1

echo "$OUT"
tail -80 "$OUT"
