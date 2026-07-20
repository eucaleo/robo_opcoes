#!/usr/bin/env bash
set -u
set -o pipefail

echo "==> Rodada 43C - corrigir printf Git Bash e bloquear recalc/pipeline via UI"
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR" || exit 1

OUT_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43C_UI_BLOCK_E_PRINTF_FIX"
mkdir -p "$OUT_DIR"

LOG="$OUT_DIR/00_log_43C.txt"
PATCH_REPORT="$OUT_DIR/01_relatorio_patch_43C.md"
PYCOMPILE_LOG="$OUT_DIR/02_py_compile_43C.txt"
GREP_LOG="$OUT_DIR/03_grep_ui_tokens_pos_43C.txt"
STATUS_LOG="$OUT_DIR/04_git_status_pos_43C.txt"

: > "$LOG"
: > "$PATCH_REPORT"
: > "$PYCOMPILE_LOG"
: > "$GREP_LOG"
: > "$STATUS_LOG"

ts="$(date +%Y%m%d_%H%M%S)"

echo "Diretorio raiz: $ROOT_DIR" | tee -a "$LOG"
echo "Saida: $OUT_DIR" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "==> criando backups" | tee -a "$LOG"

if [ -f "scripts/verify_commits_sequence_full_43B.sh" ]; then
  cp "scripts/verify_commits_sequence_full_43B.sh" "$OUT_DIR/verify_commits_sequence_full_43B.sh.$ts.bak"
  echo "Backup: scripts/verify_commits_sequence_full_43B.sh" | tee -a "$LOG"
fi

if [ -f "UI/main_window.py" ]; then
  cp "UI/main_window.py" "$OUT_DIR/main_window.py.$ts.bak"
  echo "Backup: UI/main_window.py" | tee -a "$LOG"
else
  echo "ERRO: UI/main_window.py nao encontrado" | tee -a "$LOG"
  exit 1
fi

echo "" | tee -a "$LOG"
echo "==> aplicando correcoes automatizadas via Python" | tee -a "$LOG"

python - <<'PY'
from pathlib import Path
import re

report = []

# 1) Corrigir printf no script 43B para compatibilidade com Git Bash.
sh_path = Path("scripts/verify_commits_sequence_full_43B.sh")
if sh_path.exists():
    text = sh_path.read_text(encoding="utf-8", errors="replace")
    original = text

    # Corrige apenas printf cujo primeiro argumento literal começa com hífen.
    text = re.sub(
        r"(^[ \t]*)printf\s+'- ",
        r"\1printf -- '- ",
        text,
        flags=re.MULTILINE,
    )

    if text != original:
        sh_path.write_text(text, encoding="utf-8", newline="\n")
        report.append("- Corrigido `scripts/verify_commits_sequence_full_43B.sh`: `printf '- ...'` -> `printf -- '- ...'`.")
    else:
        report.append("- Nenhuma alteracao necessaria em `scripts/verify_commits_sequence_full_43B.sh` para `printf --`.")
else:
    report.append("- Aviso: `scripts/verify_commits_sequence_full_43B.sh` nao encontrado.")

# 2) Bloquear recalc/pipeline via UI/main_window.py.
py_path = Path("UI/main_window.py")
text = py_path.read_text(encoding="utf-8", errors="replace")
original_text = text
lines = text.splitlines()

def replace_method(lines, method_name, new_block):
    start = None
    pattern = f"    def {method_name}("
    for i, line in enumerate(lines):
        if line.startswith(pattern):
            start = i
            break

    if start is None:
        raise RuntimeError(f"Metodo nao encontrado: {method_name}")

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("    def ") and not lines[j].startswith("        "):
            end = j
            break

    new_lines = new_block.strip("\n").splitlines()
    return lines[:start] + new_lines + lines[end:]

new_recalculate_structure = r'''
    def recalculate_structure(self, structure_id: str):
        """
        Recalculo via UI bloqueado.

        Centro de verdade:
            UI -> PayoffRefreshCommandService -> PricingExecutionAppService

        A UI nao deve:
        - chamar scripts externos;
        - chamar subprocess;
        - executar pipeline local;
        - recalcular payoff diretamente;
        - substituir o comando oficial de backend.

        Esta rotina permanece como bloqueio explicito para evitar sucesso
        silencioso ou contaminacao por fluxo paralelo.
        """
        msg = (
            "Recálculo via UI bloqueado. "
            "Use o comando oficial PayoffRefreshCommandService no backend; "
            "a UI deve apenas reler dados persistidos."
        )

        try:
            self._recalc_in_progress = False
        except Exception:
            pass

        try:
            self.status_bar.config(text=msg)
        except Exception:
            pass

        try:
            if hasattr(self, "details_panel") and hasattr(
                self.details_panel, "on_recalc_finished"
            ):
                self.details_panel.on_recalc_finished(
                    structure_id,
                    ok=False,
                    message=msg,
                )
        except Exception as e:
            print("[UI] Erro notificando bloqueio de recalc:", e)

        try:
            messagebox.showwarning("Recálculo bloqueado", msg)
        except Exception:
            pass
'''

new_run_pipeline = r'''
    def run_pipeline(self):
        """
        Execucao de pipeline via UI bloqueada.

        Regra operacional:
        - a UI nao executa scripts;
        - a UI nao abre subprocess;
        - a UI nao recalcula payoff;
        - o fluxo oficial deve passar pelo PayoffRefreshCommandService/backend.
        """
        msg = (
            "Pipeline via UI bloqueado. "
            "Execute o fluxo oficial pelo backend/PayoffRefreshCommandService; "
            "a UI deve apenas atualizar a leitura dos dados persistidos."
        )

        try:
            self.status_bar.config(text=msg)
        except Exception:
            pass

        try:
            messagebox.showwarning("Pipeline bloqueado", msg)
        except Exception:
            pass
'''

lines = replace_method(lines, "recalculate_structure", new_recalculate_structure)
lines = replace_method(lines, "run_pipeline", new_run_pipeline)

new_text = "\n".join(lines) + "\n"

if new_text != original_text:
    py_path.write_text(new_text, encoding="utf-8", newline="\n")
    report.append("- Alterado `UI/main_window.py`: `recalculate_structure()` agora bloqueia recálculo via UI.")
    report.append("- Alterado `UI/main_window.py`: `run_pipeline()` agora bloqueia execução de pipeline via UI.")
else:
    report.append("- Nenhuma alteracao aplicada em `UI/main_window.py`.")

Path("FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43C_UI_BLOCK_E_PRINTF_FIX/01_relatorio_patch_43C.md").write_text(
    "# Rodada 43C - Relatorio de patch\n\n" + "\n".join(report) + "\n",
    encoding="utf-8",
    newline="\n",
)
PY

PY_RC=$?
if [ "$PY_RC" -ne 0 ]; then
  echo "ERRO: patch Python falhou com RC=$PY_RC" | tee -a "$LOG"
  exit "$PY_RC"
fi

echo "OK: patch aplicado" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "==> validando py_compile" | tee -a "$LOG"

PYTHON_BIN=""
if command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "ERRO: python nao encontrado" | tee -a "$LOG"
  exit 2
fi

FILES=(
  "UI/main_window.py"
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
)

COMPILE_FAIL=0

for f in "${FILES[@]}"; do
  echo "" | tee -a "$PYCOMPILE_LOG"
  echo "== py_compile: $f ==" | tee -a "$PYCOMPILE_LOG"

  if [ ! -f "$f" ]; then
    echo "WARN: arquivo nao encontrado: $f" | tee -a "$PYCOMPILE_LOG"
    continue
  fi

  if "$PYTHON_BIN" -m py_compile "$f" >> "$PYCOMPILE_LOG" 2>&1; then
    echo "OK: $f" | tee -a "$PYCOMPILE_LOG"
  else
    echo "FAIL: $f" | tee -a "$PYCOMPILE_LOG"
    COMPILE_FAIL=1
  fi
done

echo "" | tee -a "$LOG"
echo "==> grep pos-patch de tokens sensiveis na UI" | tee -a "$LOG"

{
  echo "## Tokens proibidos fortes"
  grep -RInE "subprocess\.run|subprocess\.Popen|os\.system|recalculate_payoff_curve_points_once|INSERT INTO payoff_curve_points|INSERT INTO structure_decisions|compute_payoff_from_canonical_input|_calculate_payoff_from_legs|_calculate_payoff_points_for_range|_calculate_leg_payoff|_collect_payoff_strikes|_calculate_payoff_spot_range" UI 2>/dev/null || true

  echo ""
  echo "## Referencias gerais a subprocess/execute_pricing/payoff/decisions na UI"
  grep -RInE "subprocess|execute_pricing|payoff_curve_points|structure_decisions" UI 2>/dev/null || true
} > "$GREP_LOG"

echo "OK: grep salvo em: $GREP_LOG" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "==> git status pos-patch" | tee -a "$LOG"

{
  echo "BRANCH:"
  git branch --show-current || true

  echo ""
  echo "STATUS SHORT:"
  git status --short || true

  echo ""
  echo "DIFF STAT:"
  git diff --stat || true

  echo ""
  echo "DIFF UI/main_window.py:"
  git diff -- UI/main_window.py || true

  echo ""
  echo "DIFF scripts/verify_commits_sequence_full_43B.sh:"
  git diff -- scripts/verify_commits_sequence_full_43B.sh || true
} > "$STATUS_LOG"

echo "OK: status salvo em: $STATUS_LOG" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "==> resultado final" | tee -a "$LOG"

if [ "$COMPILE_FAIL" -eq 0 ]; then
  echo "OK: Rodada 43C concluida com py_compile OK." | tee -a "$LOG"
  echo "Relatorio: $PATCH_REPORT" | tee -a "$LOG"
  echo "PyCompile: $PYCOMPILE_LOG" | tee -a "$LOG"
  echo "Grep UI: $GREP_LOG" | tee -a "$LOG"
  echo "Git status: $STATUS_LOG" | tee -a "$LOG"
  exit 0
else
  echo "FAIL: houve falha de py_compile. Verifique: $PYCOMPILE_LOG" | tee -a "$LOG"
  exit 1
fi
