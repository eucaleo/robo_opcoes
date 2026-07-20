#!/usr/bin/env bash
set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

OUT_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43D_UI_TEXT_CLEANUP_E_GUARDRAIL"
LOG="$OUT_DIR/00_log_43D.txt"
REPORT="$OUT_DIR/01_relatorio_43D.md"
PYCOMPILE_LOG="$OUT_DIR/02_py_compile_43D.txt"
GREP_LOG="$OUT_DIR/03_guardrail_ui_tokens_43D.txt"
STATUS_LOG="$OUT_DIR/04_git_status_43D.txt"
DIFF_LOG="$OUT_DIR/05_diff_43D.txt"

mkdir -p "$OUT_DIR"

{
  echo "==> Rodada 43D - limpeza textual UI e guardrail"
  echo "Diretorio raiz: $ROOT"
  echo "Saida: $OUT_DIR"
  echo
} | tee "$LOG"

echo "==> criando backups" | tee -a "$LOG"
for f in \
  "UI/main_window.py" \
  "UI/components/details_panel.py" \
  "UI/components/structure_editor_dialog.py"
do
  if [ -f "$f" ]; then
    cp "$f" "$OUT_DIR/$(echo "$f" | sed 's#[/\\]#_#g').bak"
    echo "Backup: $f" | tee -a "$LOG"
  else
    echo "WARN: arquivo ausente: $f" | tee -a "$LOG"
  fi
done

echo | tee -a "$LOG"
echo "==> aplicando limpeza textual automatizada" | tee -a "$LOG"

python - <<'PY'
from pathlib import Path

replacements = {
    Path("UI/main_window.py"): {
        "chamar subprocess;": "chamar processos externos;",
        "a UI nao abre subprocess;": "a UI nao abre processos externos;",
    },
    Path("UI/components/details_panel.py"): {
        "Chamado pelo MainWindow ao finalizar o subprocess do pipeline.": (
            "Chamado pelo MainWindow ao finalizar o fluxo externo legado do pipeline."
        ),
    },
    Path("UI/components/structure_editor_dialog.py"): {
        "A UI nao sincroniza Excel nem chama subprocessos.": (
            "A UI nao sincroniza Excel nem chama processos externos."
        ),
    },
}

changed = []
for path, reps in replacements.items():
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in reps.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        changed.append(str(path))

print("Arquivos alterados:")
for item in changed:
    print(f"- {item}")

if not changed:
    print("- nenhum")
PY

PATCH_RC=$?
if [ "$PATCH_RC" -ne 0 ]; then
  echo "FAIL: patch textual falhou." | tee -a "$LOG"
  exit 1
fi

echo | tee -a "$LOG"
echo "==> executando py_compile" | tee -a "$LOG"
: > "$PYCOMPILE_LOG"

PY_FILES=(
  "UI/main_window.py"
  "UI/components/details_panel.py"
  "UI/components/structure_editor_dialog.py"
  "UI/components/terminal_vwap_payoff_dark_panel.py"
  "services/payoff_refresh_command_service.py"
  "services/pricing_execution_app_service.py"
  "services/pricing_execution_orchestration_service.py"
  "services/pricing_execution_persistence_service.py"
  "services/pricing_execution_service.py"
  "services/derived_payoff_persistence.py"
  "services/derived_service.py"
  "services/canonical_pricing_facade.py"
  "repositories/structures_repository.py"
  "scripts/recalculate_payoff_curve_points_once.py"
  "scripts/verify_commits_sequence_full_43B.sh"
)

PY_FAIL=0
for f in "${PY_FILES[@]}"; do
  if [ -f "$f" ] && [[ "$f" == *.py ]]; then
    {
      echo "== py_compile: $f =="
      python -m py_compile "$f"
      RC=$?
      if [ "$RC" -eq 0 ]; then
        echo "OK: $f"
      else
        echo "FAIL: $f"
        PY_FAIL=1
      fi
      echo
    } >> "$PYCOMPILE_LOG" 2>&1
  fi
done

cat "$PYCOMPILE_LOG" | tee -a "$LOG"

if grep -q "^FAIL:" "$PYCOMPILE_LOG"; then
  PY_FAIL=1
fi

echo "==> executando guardrail textual UI" | tee -a "$LOG"
: > "$GREP_LOG"

{
  echo "## Guardrail 43D - UI"
  echo
  echo "### Tokens fortes proibidos"
  echo
} >> "$GREP_LOG"

STRONG_TOKENS=(
  "compute_payoff_from_canonical_input"
  "_calculate_payoff_from_legs"
  "_calculate_payoff_points_for_range"
  "_calculate_leg_payoff"
  "_collect_payoff_strikes"
  "_calculate_payoff_spot_range"
  "subprocess.run"
  "subprocess.Popen"
  "os.system"
  "INSERT INTO payoff_curve_points"
  "INSERT INTO structure_decisions"
  "recalculate_payoff_curve_points_once"
)

GUARD_FAIL=0

for token in "${STRONG_TOKENS[@]}"; do
  {
    echo
    echo "-- token: $token --"
  } >> "$GREP_LOG"

  if grep -RInF "$token" UI 2>/dev/null >> "$GREP_LOG"; then
    GUARD_FAIL=1
  fi
done

{
  echo
  echo "### Busca informativa por termos sensiveis"
  echo
  grep -RInE "subprocess|execute_pricing|payoff_curve_points|structure_decisions" UI 2>/dev/null || true
} >> "$GREP_LOG"

cat "$GREP_LOG" | tee -a "$LOG"

echo | tee -a "$LOG"
echo "==> registrando git status e diff" | tee -a "$LOG"

{
  echo "BRANCH:"
  git branch --show-current
  echo
  echo "STATUS SHORT:"
  git status --short
  echo
  echo "DIFF STAT:"
  git diff --stat
} > "$STATUS_LOG" 2>&1

git diff -- UI/main_window.py UI/components/details_panel.py UI/components/structure_editor_dialog.py scripts/verify_commits_sequence_full_43B.sh > "$DIFF_LOG" 2>&1

cat "$STATUS_LOG" | tee -a "$LOG"

echo | tee -a "$LOG"
echo "==> gerando relatorio" | tee -a "$LOG"

{
  printf '# Rodada 43D - Limpeza textual UI e guardrail\n\n'

  printf '## Resultado\n\n'
  if [ "$PY_FAIL" -eq 0 ] && [ "$GUARD_FAIL" -eq 0 ]; then
    printf 'Status: **OK**\n\n'
    printf 'A UI ficou sem tokens fortes proibidos e os arquivos Python centrais compilaram.\n\n'
  else
    printf 'Status: **FAIL**\n\n'
    if [ "$PY_FAIL" -ne 0 ]; then
      printf -- '- Houve falha de py_compile.\n'
    fi
    if [ "$GUARD_FAIL" -ne 0 ]; then
      printf -- '- Foram encontrados tokens fortes proibidos na UI.\n'
    fi
    printf '\n'
  fi

  printf '## Arquivos gerados\n\n'
  printf -- '- Log: `%s`\n' "$LOG"
  printf -- '- PyCompile: `%s`\n' "$PYCOMPILE_LOG"
  printf -- '- Guardrail UI: `%s`\n' "$GREP_LOG"
  printf -- '- Git status: `%s`\n' "$STATUS_LOG"
  printf -- '- Diff: `%s`\n\n' "$DIFF_LOG"

  printf '## Restrições mantidas\n\n'
  printf -- '- Nao executar `git add`.\n'
  printf -- '- Nao executar `git commit`.\n'
  printf -- '- Nao executar `git push`.\n'
  printf -- '- Nao transformar script paralelo em fluxo oficial.\n'
  printf -- '- Nao recalcular payoff pela UI.\n'
} > "$REPORT"

echo "OK: relatorio salvo em: $REPORT" | tee -a "$LOG"

if [ "$PY_FAIL" -ne 0 ]; then
  echo "FAIL: houve falha de py_compile. Verifique: $PYCOMPILE_LOG" | tee -a "$LOG"
  exit 1
fi

if [ "$GUARD_FAIL" -ne 0 ]; then
  echo "FAIL: guardrail encontrou tokens fortes proibidos. Verifique: $GREP_LOG" | tee -a "$LOG"
  exit 1
fi

echo | tee -a "$LOG"
echo "OK: Rodada 43D concluida com guardrail OK." | tee -a "$LOG"
echo "Relatorio: $REPORT" | tee -a "$LOG"
echo "PyCompile: $PYCOMPILE_LOG" | tee -a "$LOG"
echo "Guardrail UI: $GREP_LOG" | tee -a "$LOG"
echo "Git status: $STATUS_LOG" | tee -a "$LOG"
echo "Diff: $DIFF_LOG" | tee -a "$LOG"
