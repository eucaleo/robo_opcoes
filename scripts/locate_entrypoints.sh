#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"

echo "## Entry points Python (main)"
( cd "$ROOT" && rg -n "if\s+__name__\s*==\s*['\"]__main__['\"]" -S . || true )
echo

echo "## Shell scripts / bat / make / task runners"
( cd "$ROOT" && {
  find . -maxdepth 4 -type f \( -name "*.sh" -o -name "*.bat" -o -name "Makefile" -o -name "*.ps1" -o -name "taskfile.yml" -o -name "Taskfile.yml" \) 2>/dev/null | sed 's|^\./||' || true
  echo
})

echo "## Pip/poetry entrypoints (setup.cfg/pyproject)"
( cd "$ROOT" && {
  ls -1 pyproject.toml setup.cfg setup.py 2>/dev/null || true
  echo
  rg -n "\[project\.scripts\]|\[tool\.poetry\.scripts\]|entry_points" -S pyproject.toml setup.cfg setup.py 2>/dev/null || true
  echo
})

echo "## Web server frameworks (FastAPI/Flask)"
( cd "$ROOT" && rg -n "FastAPI\(|APIRouter\(|Flask\(|Blueprint\(" -S . || true )
echo

echo "## Background jobs (Celery/RQ/etc.)"
( cd "$ROOT" && rg -n "Celery\(|@celery|rq|dramatiq|apscheduler" -S . || true )
echo
