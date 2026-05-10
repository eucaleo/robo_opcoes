#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

echo "== Repo root: $(cd "$ROOT" && pwd)"
echo

echo "## 1) Onde read_structure_legs é definido e chamado"
( cd "$ROOT" && {
  rg -n "def\s+read_structure_legs\b|read_structure_legs\(" -S domain services scripts || true
  echo
})

echo "## 2) Onde manual_analise_robo_legs / rtd_analise_robo_legs aparecem"
( cd "$ROOT" && {
  rg -n "manual_analise_robo_legs|rtd_analise_robo_legs|robo_legs_snapshot|robo_snapshot" -S . || true
  echo
})

echo "## 3) Quem chama derived_service e onde ele é usado"
( cd "$ROOT" && {
  rg -n "from\s+services\.derived_service\s+import|import\s+services\.derived_service|derived_service\." -S . || true
  echo
})

echo "## 4) Pontos prováveis de entrada (jobs, cli, endpoints)"
( cd "$ROOT" && {
  rg -n "if\s+__name__\s*==\s*['\"]__main__['\"]|argparse|click|typer|FastAPI|Flask|APIRouter|@app\.|@router\.|Celery|cron|schedule" -S . || true
  echo
})

echo "## 5) Conexão/DB: quem usa connect_app e onde está definido"
( cd "$ROOT" && {
  rg -n "connect_app\(" -S . || true
  rg -n "def\s+connect_app\b|class\s+.*connect_app" -S db . || true
  echo
})

echo "## 6) Timestamp canônico e/ou regras de timestamp"
( cd "$ROOT" && {
  rg -n "canonical.*timestamp|timestamp\s*can(o|ô)n|MAX\(timestamp\)|latest_timestamp|get_latest" -S . || true
  echo
})

echo "== Done."
