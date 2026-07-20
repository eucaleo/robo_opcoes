#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

BASE_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34"
OUT_DIR="$BASE_DIR/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43E_DOCUMENTACAO_ENCERRAMENTO_FASE"

LOG="$OUT_DIR/00_log_43E.txt"
REPORT="$OUT_DIR/01_relatorio_encerramento_43E.md"
COMMITS_MD="$OUT_DIR/02_sequencia_commits_git_43E.md"
INVENTORY="$OUT_DIR/03_inventario_artefatos_43E.txt"
PYCOMPILE_LOG="$OUT_DIR/04_py_compile_final_43E.txt"
GUARDRAIL_LOG="$OUT_DIR/05_guardrail_ui_final_43E.txt"
GIT_LOG="$OUT_DIR/06_git_status_diff_final_43E.txt"
DIFF_CHECK_LOG="$OUT_DIR/07_diff_check_43E.txt"
UI_DIFF_LOG="$OUT_DIR/08_diff_ui_final_43E.txt"
EVIDENCE_MD="$OUT_DIR/09_matriz_evidencias_43E.md"
SUMMARY_JSON="$OUT_DIR/10_resumo_tecnico_43E.json"

mkdir -p "$OUT_DIR"

: > "$LOG"

log_step() {
    printf '\n==> %s\n' "$1" | tee -a "$LOG"
}

run_and_log() {
    printf '\n$ %s\n' "$*" >> "$LOG"
    "$@" >> "$LOG" 2>&1
}

log_step "Rodada 43E - documentacao de encerramento da fase"
{
    printf 'Data: '
    date
    printf 'Diretorio raiz: %s\n' "$ROOT"
    printf 'Saida: %s\n' "$OUT_DIR"
} | tee -a "$LOG"

log_step "validando diretorios de referencia"
{
    printf 'Diretorios solicitados:\n'
    printf -- '- %s\n' "FRENTE_RTD_EXCEL_BTG_ONLINE"
    printf -- '- %s\n' "$BASE_DIR/GUARDRAILS_36"
    printf -- '- %s\n' "$BASE_DIR/UI_CLEANUP_35"
    printf -- '- %s\n' "$BASE_DIR/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43"
    printf '\nExistencia:\n'

    for d in \
        "FRENTE_RTD_EXCEL_BTG_ONLINE" \
        "$BASE_DIR/GUARDRAILS_36" \
        "$BASE_DIR/UI_CLEANUP_35" \
        "$BASE_DIR/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43"
    do
        if [ -d "$d" ]; then
            printf 'OK: %s\n' "$d"
        else
            printf 'WARN: ausente: %s\n' "$d"
        fi
    done
} | tee -a "$LOG"

log_step "inventariando artefatos existentes"
{
    printf '# Inventario de artefatos da frente\n\n'
    printf 'ROOT=%s\n\n' "$ROOT"

    printf '## Pastas principais\n\n'
    find "FRENTE_RTD_EXCEL_BTG_ONLINE" -maxdepth 3 -type d 2>/dev/null | sort

    printf '\n\n## Arquivos de auditoria/documentacao relevantes\n\n'
    find "FRENTE_RTD_EXCEL_BTG_ONLINE" \
        -type f \
        \( -name '*.md' -o -name '*.txt' -o -name '*.log' -o -name '*.json' \) \
        2>/dev/null | sort

    printf '\n\n## Scripts gerados em scripts/\n\n'
    find "scripts" \
        -maxdepth 1 \
        -type f \
        \( -name '*37*.sh' -o -name '*38*.sh' -o -name '*39*.sh' -o -name '*40*.sh' -o -name '*41*.sh' -o -name '*42*.sh' -o -name '*43*.sh' \) \
        2>/dev/null | sort
} > "$INVENTORY"

printf 'OK: inventario salvo em: %s\n' "$INVENTORY" | tee -a "$LOG"

log_step "registrando sequencia de commits anteriores"
{
    printf '# Sequencia de commits Git - Rodada 43E\n\n'
    printf 'Branch atual: `%s`\n\n' "$(git branch --show-current)"
    printf '## Ultimos 80 commits\n\n'
    printf '```text\n'
    git log --date=iso --pretty=format:'%h | %ad | %an | %s' -n 80
    printf '\n```\n\n'

    printf '## Commits com estatistica curta\n\n'
    printf '```text\n'
    git log --oneline --stat -n 30
    printf '\n```\n'
} > "$COMMITS_MD"

printf 'OK: sequencia de commits salva em: %s\n' "$COMMITS_MD" | tee -a "$LOG"

log_step "executando git diff --check"
set +e
git diff --check > "$DIFF_CHECK_LOG" 2>&1
DIFF_CHECK_RC=$?
set -e

if [ "$DIFF_CHECK_RC" -eq 0 ]; then
    printf 'OK: git diff --check sem problemas.\n' | tee -a "$LOG"
else
    printf 'FAIL: git diff --check encontrou problemas. Verifique: %s\n' "$DIFF_CHECK_LOG" | tee -a "$LOG"
fi

log_step "executando py_compile final"
set +e
{
    python -m py_compile \
        UI/main_window.py \
        UI/components/details_panel.py \
        UI/components/structure_editor_dialog.py \
        UI/components/terminal_vwap_payoff_dark_panel.py \
        services/payoff_refresh_command_service.py \
        services/pricing_execution_app_service.py \
        services/pricing_execution_orchestration_service.py \
        services/pricing_execution_persistence_service.py \
        services/pricing_execution_service.py \
        services/derived_payoff_persistence.py \
        services/derived_service.py \
        services/canonical_pricing_facade.py \
        repositories/structures_repository.py \
        scripts/recalculate_payoff_curve_points_once.py
} > "$PYCOMPILE_LOG" 2>&1
PYCOMPILE_RC=$?
set -e

if [ "$PYCOMPILE_RC" -eq 0 ]; then
    printf 'OK: py_compile final passou.\n' | tee -a "$LOG"
else
    printf 'FAIL: py_compile final falhou. Verifique: %s\n' "$PYCOMPILE_LOG" | tee -a "$LOG"
fi

log_step "executando guardrail final de tokens fortes na UI"
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

GUARDRAIL_FAIL=0

{
    printf '# Guardrail final UI - Rodada 43E\n\n'
    printf '## Tokens fortes proibidos\n\n'

    for token in "${STRONG_TOKENS[@]}"; do
        printf '\n-- token: %s --\n' "$token"
        set +e
        grep -RInF -- "$token" UI 2>/dev/null
        RC=$?
        set -e

        if [ "$RC" -eq 0 ]; then
            GUARDRAIL_FAIL=1
        fi
    done

    printf '\n\n## Busca informativa por tabelas e termos permitidos de leitura\n\n'
    grep -RInE "payoff_curve_points|structure_decisions|execute_pricing|PayoffRefreshCommandService|processos externos|pipeline|rec.lculo" UI 2>/dev/null || true
} > "$GUARDRAIL_LOG"

if [ "$GUARDRAIL_FAIL" -eq 0 ]; then
    printf 'OK: guardrail final sem tokens fortes proibidos na UI.\n' | tee -a "$LOG"
else
    printf 'FAIL: guardrail final encontrou tokens fortes proibidos. Verifique: %s\n' "$GUARDRAIL_LOG" | tee -a "$LOG"
fi

log_step "registrando status git, diff stat e diff final"
{
    printf 'BRANCH:\n'
    git branch --show-current

    printf '\nSTATUS SHORT:\n'
    git status --short

    printf '\nDIFF STAT:\n'
    git diff --stat

    printf '\nDIFF NAME-STATUS:\n'
    git diff --name-status

    printf '\nUNTRACKED FILES:\n'
    git ls-files --others --exclude-standard
} > "$GIT_LOG"

{
    printf '# Diff final UI - Rodada 43E\n\n'
    printf '```diff\n'
    git diff -- UI/main_window.py UI/components/details_panel.py UI/components/structure_editor_dialog.py
    printf '\n```\n'
} > "$UI_DIFF_LOG"

printf 'OK: git status/diff salvos.\n' | tee -a "$LOG"

log_step "montando matriz de evidencias"
{
    printf '# Matriz de evidencias - Rodada 43E\n\n'

    printf '## Evidencias consultadas/geradas nesta rodada\n\n'
    printf -- '- `%s`\n' "$LOG"
    printf -- '- `%s`\n' "$REPORT"
    printf -- '- `%s`\n' "$COMMITS_MD"
    printf -- '- `%s`\n' "$INVENTORY"
    printf -- '- `%s`\n' "$PYCOMPILE_LOG"
    printf -- '- `%s`\n' "$GUARDRAIL_LOG"
    printf -- '- `%s`\n' "$GIT_LOG"
    printf -- '- `%s`\n' "$DIFF_CHECK_LOG"
    printf -- '- `%s`\n' "$UI_DIFF_LOG"

    printf '\n## Evidencias anteriores esperadas\n\n'
    for f in \
        "$BASE_DIR/VERIFICACAO_BACKEND_EXECUTE_PRICING_42" \
        "$BASE_DIR/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43C_UI_BLOCK_E_PRINTF_FIX" \
        "$BASE_DIR/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43D_UI_TEXT_CLEANUP_E_GUARDRAIL" \
        "$BASE_DIR/GUARDRAILS_36" \
        "$BASE_DIR/UI_CLEANUP_35"
    do
        if [ -e "$f" ]; then
            printf -- '- OK: `%s`\n' "$f"
        else
            printf -- '- WARN: ausente: `%s`\n' "$f"
        fi
    done

    printf '\n## Criterios de encerramento tecnico\n\n'
    printf -- '- `git diff --check` sem problemas.\n'
    printf -- '- `py_compile` final sem falha.\n'
    printf -- '- Guardrail UI sem tokens fortes proibidos.\n'
    printf -- '- Backend `execute_pricing()` validado previamente sem UI pela verificacao 42.\n'
    printf -- '- UI bloqueada para recalc/pipeline local.\n'
    printf -- '- Nenhum `git add`, `git commit` ou `git push` executado por esta rodada.\n'
} > "$EVIDENCE_MD"

printf 'OK: matriz de evidencias salva em: %s\n' "$EVIDENCE_MD" | tee -a "$LOG"

log_step "gerando resumo tecnico JSON"
python - <<PY
import json
from pathlib import Path
import subprocess

root = Path(r"$ROOT")
out = Path(r"$SUMMARY_JSON")

def cmd(args):
    try:
        return subprocess.check_output(args, cwd=root, text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as exc:
        return exc.output.strip()

summary = {
    "rodada": "43E",
    "tipo": "documentacao_encerramento_fase",
    "branch": cmd(["git", "branch", "--show-current"]),
    "diff_check_rc": $DIFF_CHECK_RC,
    "pycompile_rc": $PYCOMPILE_RC,
    "guardrail_fail": $GUARDRAIL_FAIL,
    "arquivos_alterados_versionados": cmd(["git", "diff", "--name-only"]).splitlines(),
    "restricoes": {
        "git_add": False,
        "git_commit": False,
        "git_push": False,
        "recalculo_payoff_ui": False,
        "subprocess_ui": False
    },
    "artefatos": {
        "log": r"$LOG",
        "relatorio": r"$REPORT",
        "commits": r"$COMMITS_MD",
        "inventario": r"$INVENTORY",
        "pycompile": r"$PYCOMPILE_LOG",
        "guardrail": r"$GUARDRAIL_LOG",
        "git": r"$GIT_LOG",
        "diff_check": r"$DIFF_CHECK_LOG",
        "diff_ui": r"$UI_DIFF_LOG",
        "evidencias": r"$EVIDENCE_MD"
    }
}

out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK: resumo JSON salvo em: {out}")
PY

log_step "gerando relatorio final"
{
    printf '# Rodada 43E - Encerramento documentado da fase\n\n'

    printf '## Resultado\n\n'
    if [ "$DIFF_CHECK_RC" -eq 0 ] && [ "$PYCOMPILE_RC" -eq 0 ] && [ "$GUARDRAIL_FAIL" -eq 0 ]; then
        printf 'Status: **OK**\n\n'
        printf 'A fase está apta para encerramento documental, mantendo as restrições operacionais definidas.\n\n'
    else
        printf 'Status: **FAIL**\n\n'
        printf 'A fase ainda possui pendências técnicas. Verificar logs indicados abaixo.\n\n'
    fi

    printf '## Escopo consolidado\n\n'
    printf -- '- UI não recalcula payoff.\n'
    printf -- '- UI não executa pipeline local.\n'
    printf -- '- UI não abre processos externos para recálculo/pipeline.\n'
    printf -- '- Centro de verdade permanece no backend: `PayoffRefreshCommandService` -> `PricingExecutionAppService`.\n'
    printf -- '- Persistência backend validada previamente com incremento de `payoff_curve_points` e `structure_decisions`.\n\n'

    printf '## Validações finais desta rodada\n\n'

    if [ "$DIFF_CHECK_RC" -eq 0 ]; then
        printf -- '- `git diff --check`: **OK**\n'
    else
        printf -- '- `git diff --check`: **FAIL** - `%s`\n' "$DIFF_CHECK_LOG"
    fi

    if [ "$PYCOMPILE_RC" -eq 0 ]; then
        printf -- '- `py_compile`: **OK**\n'
    else
        printf -- '- `py_compile`: **FAIL** - `%s`\n' "$PYCOMPILE_LOG"
    fi

    if [ "$GUARDRAIL_FAIL" -eq 0 ]; then
        printf -- '- Guardrail UI tokens fortes: **OK**\n'
    else
        printf -- '- Guardrail UI tokens fortes: **FAIL** - `%s`\n' "$GUARDRAIL_LOG"
    fi

    printf '\n## Arquivos versionados alterados no working tree\n\n'
    printf '```text\n'
    git diff --name-only
    printf '```\n\n'

    printf '## Artefatos gerados\n\n'
    printf -- '- Log: `%s`\n' "$LOG"
    printf -- '- Sequência de commits: `%s`\n' "$COMMITS_MD"
    printf -- '- Inventário de artefatos: `%s`\n' "$INVENTORY"
    printf -- '- PyCompile final: `%s`\n' "$PYCOMPILE_LOG"
    printf -- '- Guardrail final UI: `%s`\n' "$GUARDRAIL_LOG"
    printf -- '- Git status/diff: `%s`\n' "$GIT_LOG"
    printf -- '- Diff check: `%s`\n' "$DIFF_CHECK_LOG"
    printf -- '- Diff UI final: `%s`\n' "$UI_DIFF_LOG"
    printf -- '- Matriz de evidências: `%s`\n' "$EVIDENCE_MD"
    printf -- '- Resumo JSON: `%s`\n' "$SUMMARY_JSON"

    printf '\n## Restrições mantidas\n\n'
    printf -- '- Não executar `git add` nesta etapa.\n'
    printf -- '- Não executar `git commit` nesta etapa.\n'
    printf -- '- Não executar `git push` nesta etapa.\n'
    printf -- '- Não transformar script paralelo em fluxo oficial.\n'
    printf -- '- Não recalcular payoff pela UI.\n'
    printf -- '- Não executar pipeline pela UI.\n'

    printf '\n## Decisão recomendada\n\n'
    if [ "$DIFF_CHECK_RC" -eq 0 ] && [ "$PYCOMPILE_RC" -eq 0 ] && [ "$GUARDRAIL_FAIL" -eq 0 ]; then
        printf '1. Revisar os artefatos `43E`.\n'
        printf '2. Confirmar visualmente o diff final da UI.\n'
        printf '3. Se aprovado, preparar etapa posterior de fechamento controlado/commit, ainda sem automatizar commit neste script.\n'
    else
        printf '1. Corrigir pendências indicadas nos logs.\n'
        printf '2. Reexecutar esta Rodada 43E.\n'
        printf '3. Não avançar para fechamento/commit enquanto houver falha.\n'
    fi
} > "$REPORT"

printf 'OK: relatorio salvo em: %s\n' "$REPORT" | tee -a "$LOG"

log_step "resultado final"
if [ "$DIFF_CHECK_RC" -eq 0 ] && [ "$PYCOMPILE_RC" -eq 0 ] && [ "$GUARDRAIL_FAIL" -eq 0 ]; then
    printf 'OK: Rodada 43E concluida com documentacao de encerramento apta.\n' | tee -a "$LOG"
    printf 'Relatorio: %s\n' "$REPORT" | tee -a "$LOG"
    printf 'Commits: %s\n' "$COMMITS_MD" | tee -a "$LOG"
    printf 'Inventario: %s\n' "$INVENTORY" | tee -a "$LOG"
    printf 'Evidencias: %s\n' "$EVIDENCE_MD" | tee -a "$LOG"
    exit 0
else
    printf 'FAIL: Rodada 43E encontrou pendencias.\n' | tee -a "$LOG"
    printf 'Relatorio: %s\n' "$REPORT" | tee -a "$LOG"
    exit 1
fi
