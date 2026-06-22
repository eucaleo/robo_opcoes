#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-5-diagnostico-rtd.txt"

{
  echo "============================================================"
  echo "FASE 5 - DIAGNOSTICO RTD"
  echo "Data:"
  date
  echo "Branch:"
  git branch --show-current
  echo "Commit atual:"
  git rev-parse --short HEAD
  echo "============================================================"
  echo

  echo "== Status git =="
  git status --short
  echo

  echo "== Busca por RTD no projeto =="
  grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ --exclude='*.pyc' \
    -E "RTD|rtd|rtd_option_quotes|option_quotes|quotes" . 2>/dev/null | head -300
  echo

  echo "== Busca por handlers Atualizar Dados / Pipeline =="
  grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ --exclude='*.pyc' \
    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
  echo

  echo "== Busca por conexão com bancos =="
  grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ --exclude='*.pyc' \
    -E "connect_raw|connect_derived|sqlite|derived.db|raw.db|rtd_option_quotes" db repositories services scripts UI 2>/dev/null | head -300
  echo

  echo "== Arquivos candidatos RTD =="
  find . -type f \
    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' \) \
    -not -path './.git/*' \
    -not -path './__pycache__/*' \
    | sort
  echo

  echo "== Schema derived.db via db.config.connect_derived =="
  python - <<'PY'
try:
    from db.config import connect_derived

    conn = connect_derived()
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()

        print("Tabelas:")
        for row in rows:
            name = row[0]
            print(f"- {name}")

        print()
        for target in ["rtd_option_quotes", "payoff_curve_points", "structure_decisions"]:
            exists = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (target,),
            ).fetchone()
            if not exists:
                print(f"Tabela {target}: inexistente")
                continue

            count = conn.execute(f'SELECT COUNT(*) FROM "{target}"').fetchone()[0]
            print(f"Tabela {target}: {count} linhas")

            cols = conn.execute(f'PRAGMA table_info("{target}")').fetchall()
            print(f"Colunas {target}:")
            for col in cols:
                print(f"  - {col[1]} {col[2]}")

            sample = conn.execute(f'SELECT * FROM "{target}" LIMIT 3').fetchall()
            print(f"Amostra {target}:")
            for item in sample:
                print(f"  {item}")
            print()
    finally:
        conn.close()
except Exception as e:
    print("ERRO_SCHEMA_DERIVED:", repr(e))
PY
  echo

  echo "== Schema raw/source se existir via db.config =="
  python - <<'PY'
try:
    import db.config as cfg

    candidates = [
        "connect_raw",
        "connect_source",
        "connect_market",
        "connect_app",
    ]

    found = False
    for name in candidates:
        fn = getattr(cfg, name, None)
        if not callable(fn):
            continue

        found = True
        print(f"Conector encontrado: {name}")
        try:
            conn = fn()
            try:
                rows = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                ).fetchall()
                for row in rows:
                    print(f"- {row[0]}")
            finally:
                conn.close()
        except Exception as e:
            print(f"Erro usando {name}: {repr(e)}")
        print()

    if not found:
        print("Nenhum conector raw/source conhecido encontrado em db.config")
except Exception as e:
    print("ERRO_SCHEMA_RAW:", repr(e))
PY
  echo

  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="
  sed -n '260,560p' UI/main_window.py 2>/dev/null
  echo

  echo "== Trecho scripts/run_derived_pipeline.py =="
  sed -n '1,240p' scripts/run_derived_pipeline.py 2>/dev/null
  echo

  echo "============================================================"
  echo "FIM DIAGNOSTICO FASE 5"
  echo "============================================================"
} > "$OUT" 2>&1

echo "Diagnostico Fase 5 gerado em: $OUT"
