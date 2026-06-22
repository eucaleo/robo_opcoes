#!/usr/bin/env bash
set -u

EVID="docs/checkpoints/evidencias/fase-3f-diagnostico-payoff-manual-canonico.txt"
AUDIT="docs/checkpoints/auditoria-revisao-funcional-pos-uso-real.md"

mkdir -p docs/checkpoints/evidencias
mkdir -p scripts

{
  echo "============================================================"
  echo "FASE 3F - DIAGNOSTICO PAYOFF ESTRUTURA MANUAL CANONICA"
  echo "Data:"
  date
  echo "Branch:"
  git branch --show-current
  echo "Commit atual:"
  git rev-parse --short HEAD
  echo "============================================================"
  echo

  echo "== Status git antes do diagnostico =="
  git status --short
  echo

  echo "== Busca por referencias a payoff_curve_points =="
  grep -RIn "payoff_curve_points" repositories services domain UI ATT scripts 2>/dev/null || true
  echo

  echo "== Busca por referencias a structure_decisions =="
  grep -RIn "structure_decisions" repositories services domain UI ATT scripts 2>/dev/null || true
  echo

  echo "== Busca por referencias a Payoff/payoff =="
  grep -RIn "payoff\|Payoff" repositories services domain UI ATT 2>/dev/null || true
  echo

  echo "== Busca por referencias a engine stub =="
  grep -RIn "stub\|engine" repositories services domain UI ATT 2>/dev/null || true
  echo

  echo "== Inspecao dos bancos e tabelas relevantes =="
  python - <<'PY'
from pathlib import Path
import sqlite3
import json

dbs = [
    Path("dados/app.db"),
    Path("dados/derived.db"),
]

def table_exists(conn, table):
    row = conn.execute(
        "select name from sqlite_master where type='table' and name=?",
        (table,),
    ).fetchone()
    return bool(row)

def columns(conn, table):
    try:
        return [r[1] for r in conn.execute(f"pragma table_info({table})").fetchall()]
    except Exception as exc:
        return [f"ERRO: {exc}"]

def count_rows(conn, table):
    try:
        return conn.execute(f"select count(*) from {table}").fetchone()[0]
    except Exception as exc:
        return f"ERRO: {exc}"

def count_by_structure_id(conn, table, structure_id=2):
    cols = columns(conn, table)
    if "structure_id" not in cols:
        return "SEM_COLUNA_structure_id"
    try:
        return conn.execute(
            f"select count(*) from {table} where structure_id=?",
            (structure_id,),
        ).fetchone()[0]
    except Exception as exc:
        return f"ERRO: {exc}"

for db in dbs:
    print(f"\n-- Banco: {db} --")
    if not db.exists():
        print("NAO_EXISTE")
        continue

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row

    tables = [
        r["name"]
        for r in conn.execute(
            "select name from sqlite_master where type='table' order by name"
        ).fetchall()
    ]

    print("Tabelas:")
    for t in tables:
        print(f"  - {t}")

    interesting = [
        "structures",
        "structure_legs",
        "pricing_executions",
        "structure_snapshots",
        "structure_leg_snapshots",
        "payoff_curve_points",
        "structure_decisions",
        "rtd_option_quotes",
    ]

    print("\nTabelas relevantes:")
    for table in interesting:
        if table_exists(conn, table):
            print(f"\nTabela: {table}")
            print("Colunas:", columns(conn, table))
            print("Total linhas:", count_rows(conn, table))
            print("Linhas structure_id=2:", count_by_structure_id(conn, table, 2))

            cols = columns(conn, table)
            order_col = None
            for candidate in ["id", "created_at", "updated_at", "snapshot_id"]:
                if candidate in cols:
                    order_col = candidate
                    break

            try:
                if "structure_id" in cols:
                    sql = f"select * from {table} where structure_id=?"
                    if order_col:
                        sql += f" order by {order_col} desc"
                    sql += " limit 5"
                    rows = conn.execute(sql, (2,)).fetchall()
                else:
                    sql = f"select * from {table}"
                    if order_col:
                        sql += f" order by {order_col} desc"
                    sql += " limit 3"
                    rows = conn.execute(sql).fetchall()

                print("Amostra:")
                for row in rows:
                    print(dict(row))
            except Exception as exc:
                print("Erro ao listar amostra:", exc)

    conn.close()
PY
  echo

  echo "== Execucao CanonicalPricingFacade para structure_id=2 =="
  python - <<'PY'
from pathlib import Path
import json
import traceback

try:
    from services.canonical_pricing_facade import CanonicalPricingFacade

    facade = CanonicalPricingFacade(db_path=Path("dados/app.db"))
    result = facade.execute_pricing(2)

    print("Tipo retorno:", type(result).__name__)
    print("Chaves raiz:", sorted(result.keys()) if isinstance(result, dict) else "NAO_DICT")

    if isinstance(result, dict):
        print("status:", result.get("status"))
        print("engine:", result.get("engine"))
        print("meta:", json.dumps(result.get("meta", {}), ensure_ascii=False, default=str, indent=2))
        print("persisted:", json.dumps(result.get("persisted", {}), ensure_ascii=False, default=str, indent=2))

        for key in [
            "payoff",
            "payoff_curve",
            "payoff_points",
            "curve",
            "points",
            "decisions",
            "decision_results",
            "result",
            "pricing_result",
        ]:
            value = result.get(key)
            if isinstance(value, list):
                print(f"{key}: lista com {len(value)} itens")
                print("amostra:", json.dumps(value[:3], ensure_ascii=False, default=str, indent=2))
            elif isinstance(value, dict):
                print(f"{key}: dict chaves {sorted(value.keys())}")
                print(json.dumps(value, ensure_ascii=False, default=str, indent=2)[:3000])
            else:
                print(f"{key}: {value!r}")

except Exception:
    traceback.print_exc()
PY
  echo

  echo "== Inspecao pos-execucao de payoff e decisoes =="
  python - <<'PY'
from pathlib import Path
import sqlite3

for db in [Path("dados/app.db"), Path("dados/derived.db")]:
    print(f"\n-- Banco: {db} --")
    if not db.exists():
        print("NAO_EXISTE")
        continue

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row

    tables = [
        "payoff_curve_points",
        "structure_decisions",
        "pricing_executions",
        "structure_snapshots",
        "structure_leg_snapshots",
    ]

    for table in tables:
        exists = conn.execute(
            "select name from sqlite_master where type='table' and name=?",
            (table,),
        ).fetchone()

        if not exists:
            print(f"{table}: NAO_EXISTE")
            continue

        cols = [r[1] for r in conn.execute(f"pragma table_info({table})").fetchall()]
        if "structure_id" in cols:
            count = conn.execute(
                f"select count(*) from {table} where structure_id=?",
                (2,),
            ).fetchone()[0]
            print(f"{table}: linhas structure_id=2 = {count}")
        else:
            count = conn.execute(f"select count(*) from {table}").fetchone()[0]
            print(f"{table}: total linhas = {count}")

    conn.close()
PY
  echo

  echo "============================================================"
  echo "FIM DO DIAGNOSTICO FASE 3F"
  echo "============================================================"

} > "$EVID" 2>&1

if [ ! -f "$AUDIT" ]; then
  cat > "$AUDIT" <<'MD'
# Auditoria - Revisao Funcional Pos Uso Real

Documento de acompanhamento da evolucao da revisao funcional pos uso real.

## Regras operacionais

- Banco de dados e fonte da verdade.
- Excel apenas como ponte RTD.
- UI nao deve depender de CSVs derivados antigos.
- Toda alteracao deve ser precedida de busca em arquivos e dados.
- Toda alteracao deve ser testada.
- Toda fase encerrada deve atualizar evidencias em docs.
- Toda alteracao concluida e testada deve ser commitada.

MD
fi

cat >> "$AUDIT" <<MD

## Fase 3F - Diagnostico payoff estrutura manual canonica

Data: $(date)

Branch: $(git branch --show-current)

Commit base: $(git rev-parse --short HEAD)

Objetivo:
Identificar por que a estrutura manual canonica structure_id=2 ainda nao gera pontos em payoff_curve_points.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-diagnostico-payoff-manual-canonico.txt

Status:
Diagnostico executado. Aguardando analise da evidencia para definir correcao.

MD

echo "Diagnostico Fase 3F gerado em:"
echo "$EVID"
echo
echo "Auditoria atualizada em:"
echo "$AUDIT"
