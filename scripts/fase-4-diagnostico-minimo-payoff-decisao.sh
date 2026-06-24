#!/usr/bin/env bash
set -u

OUT="docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_4_MINIMO_PAYOFF_DECISAO.txt"
mkdir -p docs/evidencias

BASE="${1:-ff0810a}"

if ! git cat-file -e "$BASE^{commit}" 2>/dev/null; then
  BASE="$(git rev-list -n 1 --before='3 days ago' HEAD 2>/dev/null || true)"
fi

TMP_ALL="$(mktemp)"
TMP_CODE="$(mktemp)"
TMP_CORE="$(mktemp)"

cleanup() {
  rm -f "$TMP_ALL" "$TMP_CODE" "$TMP_CORE"
}
trap cleanup EXIT

git diff --name-only "$BASE"..HEAD 2>/dev/null \
  | grep -Ev '^(docs/evidencias/|\.pytest_cache/|__pycache__/)' \
  | sort -u > "$TMP_ALL"

grep -E '\.(py|sql|json|toml|yaml|yml|ini)$' "$TMP_ALL" \
  | grep -Ev '(^docs/|/docs/|\.md$|\.txt$)' \
  | sort -u > "$TMP_CODE"

grep -Ei '(canonical_pricing_facade|derived_payoff_persistence|derived_service|ui_data|main_window|pricing_execution|structure_analysis|payoff|decision|decisao|decisão)' "$TMP_CODE" \
  | sort -u > "$TMP_CORE"

{
  echo "== Fase 4 - Diagnostico minimo payoff/decisao =="
  date
  echo

  echo "== Base usada =="
  echo "BASE=$BASE"
  echo "HEAD=$(git rev-parse --short HEAD)"
  echo "BRANCH=$(git branch --show-current)"
  echo

  echo "== Git status curto =="
  git status --short
  echo

  echo "== Commits desde a base, sem docs/evidencias =="
  git log --oneline "$BASE"..HEAD -- . ':!docs/evidencias' | head -n 80
  echo

  echo "== Quantidade de arquivos alterados desde a base =="
  echo "TOTAL_ALTERADOS=$(wc -l < "$TMP_ALL")"
  echo "TOTAL_CODIGO=$(wc -l < "$TMP_CODE")"
  echo "TOTAL_CORE_PAYOFF_DECISAO=$(wc -l < "$TMP_CORE")"
  echo

  echo "== Arquivos de codigo alterados por pasta =="
  awk -F/ '{print $1}' "$TMP_CODE" | sort | uniq -c | sort -nr
  echo

  echo "== Arquivos centrais alterados =="
  cat "$TMP_CORE"
  echo

  echo "== Diff estatistico somente dos arquivos centrais =="
  if [ -s "$TMP_CORE" ]; then
    git diff --stat "$BASE"..HEAD -- $(cat "$TMP_CORE")
  else
    echo "Nenhum arquivo central alterado."
  fi
  echo

  echo "== Linhas alteradas relevantes nos arquivos centrais =="
  if [ -s "$TMP_CORE" ]; then
    while IFS= read -r f; do
      [ -f "$f" ] || continue
      echo
      echo "-- FILE: $f"
      git diff -U0 "$BASE"..HEAD -- "$f" \
        | grep -Ei '^(\+\+\+|---|@@|[+-].*(payoff|decision|decisao|decisão|canonical|structure_id|manual|derived|execution|pricing|payload|result|alias_legacy_aba|payoff_curve_points|structure_decisions))' \
        | head -n 160
    done < "$TMP_CORE"
  else
    echo "Nenhum arquivo central alterado."
  fi
  echo

  echo "== Banco - consistencia por structure_id =="
  python - <<'PY'
from pathlib import Path
import sqlite3

app = Path("dados/app.db")
der = Path("dados/derived.db")

if not app.exists():
    print("APP_DB_AUSENTE=dados/app.db")

if not der.exists():
    print("DERIVED_DB_AUSENTE=dados/derived.db")

if app.exists() and der.exists():
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.execute("attach database ? as app", (str(app),))
    con.execute("attach database ? as der", (str(der),))

    def table_exists(schema, table):
        return con.execute(
            f"select 1 from {schema}.sqlite_master where type='table' and name=?",
            (table,),
        ).fetchone() is not None

    def cols(schema, table):
        if not table_exists(schema, table):
            return []
        return [r["name"] for r in con.execute(f"pragma {schema}.table_info({table})")]

    print("APP_DB=dados/app.db")
    print("DERIVED_DB=dados/derived.db")

    app_struct_cols = cols("app", "structures")
    app_leg_cols = cols("app", "structure_legs")
    app_exec_cols = cols("app", "pricing_executions")
    pay_cols = cols("der", "payoff_curve_points")
    dec_cols = cols("der", "structure_decisions")

    for schema, table in [
        ("app", "structures"),
        ("app", "structure_legs"),
        ("app", "pricing_executions"),
        ("der", "payoff_curve_points"),
        ("der", "structure_decisions"),
    ]:
        if table_exists(schema, table):
            n = con.execute(f"select count(*) as n from {schema}.{table}").fetchone()["n"]
            print(f"COUNT {schema}.{table}={n}")
        else:
            print(f"MISSING {schema}.{table}")

    print()
    print("== Estruturas app e derivados correspondentes ==")

    if table_exists("app", "structures") and "id" in app_struct_cols:
        order_col = "created_at" if "created_at" in app_struct_cols else "id"

        select_cols = [c for c in [
            "id", "created_at", "updated_at", "name", "underlying_asset",
            "asset", "strategy_type", "structure_type", "status"
        ] if c in app_struct_cols]

        sql = (
            "select " + ", ".join(select_cols) +
            f" from app.structures order by {order_col} desc limit 20"
        )

        rows = list(con.execute(sql))

        for r in rows:
            sid = str(r["id"])
            info = dict(r)

            legs = None
            if table_exists("app", "structure_legs") and "structure_id" in app_leg_cols:
                legs = con.execute(
                    "select count(*) as n from app.structure_legs where cast(structure_id as text)=?",
                    (sid,),
                ).fetchone()["n"]

            exec_total = None
            exec_success = None
            exec_error = None
            exec_last = None

            if table_exists("app", "pricing_executions") and "structure_id" in app_exec_cols:
                exec_total = con.execute(
                    "select count(*) as n from app.pricing_executions where cast(structure_id as text)=?",
                    (sid,),
                ).fetchone()["n"]

                if "execution_status" in app_exec_cols:
                    exec_success = con.execute(
                        """
                        select count(*) as n
                        from app.pricing_executions
                        where cast(structure_id as text)=?
                          and lower(coalesce(execution_status, '')) in ('success', 'ok', 'completed', 'sucesso')
                        """,
                        (sid,),
                    ).fetchone()["n"]

                    exec_error = con.execute(
                        """
                        select count(*) as n
                        from app.pricing_executions
                        where cast(structure_id as text)=?
                          and lower(coalesce(execution_status, '')) in ('error', 'erro', 'failed', 'failure')
                        """,
                        (sid,),
                    ).fetchone()["n"]

                if "created_at" in app_exec_cols:
                    exec_last = con.execute(
                        """
                        select max(created_at) as v
                        from app.pricing_executions
                        where cast(structure_id as text)=?
                        """,
                        (sid,),
                    ).fetchone()["v"]

            payoff_total = None
            payoff_last = None

            if table_exists("der", "payoff_curve_points") and "structure_id" in pay_cols:
                payoff_total = con.execute(
                    "select count(*) as n from der.payoff_curve_points where cast(structure_id as text)=?",
                    (sid,),
                ).fetchone()["n"]

                time_col = "timestamp" if "timestamp" in pay_cols else None
                if time_col:
                    payoff_last = con.execute(
                        f"""
                        select max({time_col}) as v
                        from der.payoff_curve_points
                        where cast(structure_id as text)=?
                        """,
                        (sid,),
                    ).fetchone()["v"]

            decision_total = None
            decision_last = None

            if table_exists("der", "structure_decisions") and "structure_id" in dec_cols:
                decision_total = con.execute(
                    "select count(*) as n from der.structure_decisions where cast(structure_id as text)=?",
                    (sid,),
                ).fetchone()["n"]

                time_col = "timestamp" if "timestamp" in dec_cols else None
                if time_col:
                    decision_last = con.execute(
                        f"""
                        select max({time_col}) as v
                        from der.structure_decisions
                        where cast(structure_id as text)=?
                        """,
                        (sid,),
                    ).fetchone()["v"]

            print(
                "STRUCTURE_CHECK",
                f"id={sid}",
                f"info={info}",
                f"legs={legs}",
                f"exec_total={exec_total}",
                f"exec_success={exec_success}",
                f"exec_error={exec_error}",
                f"exec_last={exec_last}",
                f"payoff_points={payoff_total}",
                f"payoff_last={payoff_last}",
                f"decisions={decision_total}",
                f"decision_last={decision_last}",
            )

    print()
    print("== Possiveis derivados orfaos ==")

    if (
        table_exists("der", "payoff_curve_points")
        and "structure_id" in pay_cols
        and table_exists("app", "structures")
        and "id" in app_struct_cols
    ):
        rows = con.execute(
            """
            select p.structure_id as structure_id, count(*) as total
            from der.payoff_curve_points p
            left join app.structures s
              on cast(s.id as text)=cast(p.structure_id as text)
            where s.id is null
            group by p.structure_id
            order by total desc
            limit 20
            """
        ).fetchall()

        if rows:
            for r in rows:
                print("ORFAO_PAYOFF", dict(r))
        else:
            print("ORFAO_PAYOFF=0")

    if (
        table_exists("der", "structure_decisions")
        and "structure_id" in dec_cols
        and table_exists("app", "structures")
        and "id" in app_struct_cols
    ):
        rows = con.execute(
            """
            select d.structure_id as structure_id, count(*) as total
            from der.structure_decisions d
            left join app.structures s
              on cast(s.id as text)=cast(d.structure_id as text)
            where s.id is null
            group by d.structure_id
            order by total desc
            limit 20
            """
        ).fetchall()

        if rows:
            for r in rows:
                print("ORFAO_DECISION", dict(r))
        else:
            print("ORFAO_DECISION=0")

    con.close()
PY

} > "$OUT" 2>&1

echo "$OUT"
