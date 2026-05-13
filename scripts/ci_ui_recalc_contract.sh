#!/usr/bin/env bash
set -euo pipefail

PY="${PYTHON:-python}"

fail=0
check_file() { [[ -f "$1" ]] || { echo "[FAIL] Missing file: $1"; fail=1; }; }
check_grep() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -nE -- "$pattern" "$file" >/dev/null 2>&1; then
    echo "[OK]   $label"
  else
    echo "[FAIL] $label  (file=$file pattern=$pattern)"
    fail=1
  fi
}

echo "[INFO] UI recalc contract checks"

check_file "UI/components/details_panel.py"
check_file "UI/main_window.py"
check_file "scripts/run_derived_pipeline.py"

echo ""
echo "[INFO] 1) DetailsPanel B4/B5"
check_grep "UI/components/details_panel.py" "_recalc_in_progress" "DetailsPanel lock local"
check_grep "UI/components/details_panel.py" "_last_recalc_signature" "DetailsPanel dedupe signature"
check_grep "UI/components/details_panel.py" "def _get_latest_snapshot_timestamp_for_aba\\(" "DetailsPanel timestamp canônico (raw)"
check_grep "UI/components/details_panel.py" "def on_recalc_finished\\(" "DetailsPanel recebe callback de fim"
check_grep "UI/components/details_panel.py" "Snapshot não mudou; recálculo desnecessário" "Mensagem de dedupe (UX)"

echo ""
echo "[INFO] 2) MainWindow executor único"
check_grep "UI/main_window.py" "def recalculate_aba\\(self, aba: str\\)" "Existe recalculate_aba"
check_grep "UI/main_window.py" "_recalc_in_progress" "MainWindow lock global"
check_grep "UI/main_window.py" "threading\\.Thread\\(target=worker" "Roda subprocess em thread"
check_grep "UI/main_window.py" "subprocess\\.run\\(" "Chama subprocess.run"
check_grep "UI/main_window.py" "--aba" "Passa flag --aba"
check_grep "UI/main_window.py" "details_panel\\.on_recalc_finished" "Notifica DetailsPanel ao finalizar"

echo ""
echo "[INFO] 3) run_pipeline robusto (scripts/ vs Scripts/)"
check_grep "UI/main_window.py" "project_root / \"scripts\" / \"run_derived_pipeline\\.py\"" "run_pipeline tenta scripts/"
check_grep "UI/main_window.py" "project_root / \"Scripts\" / \"run_derived_pipeline\\.py\"" "run_pipeline fallback Scripts/"

echo ""
echo "[INFO] 4) py_compile"
if "$PY" -m py_compile UI/main_window.py UI/components/details_panel.py scripts/run_derived_pipeline.py; then
  echo "[OK]   py_compile passou"
else
  echo "[FAIL] py_compile falhou"
  fail=1
fi

echo ""
if [[ "$fail" -eq 0 ]]; then
  echo "[PASS] UI recalc contract OK"
  exit 0
else
  echo "[FAIL] UI recalc contract FAILED"
  exit 1
fi
