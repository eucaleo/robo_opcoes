#!/usr/bin/env bash
set -u
set -o pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR" || exit 1

BASE_OUT="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43"
OUT_DIR="$BASE_OUT/43B_PYCOMPILE_E_DECISAO"

mkdir -p "$OUT_DIR"

LOG="$OUT_DIR/09_py_compile_central_43B.txt"
SUMMARY="$OUT_DIR/10_sumario_decisao_43B.md"
STATUS="$OUT_DIR/11_git_status_pos_43B.txt"
FRONT_FILES="$OUT_DIR/12_inventario_frentes_relevantes_43B.txt"

: > "$LOG"
: > "$SUMMARY"
: > "$STATUS"
: > "$FRONT_FILES"

printf '\n==> Rodada 43B - py_compile, inventario e decisao\n'
printf 'Diretorio raiz: %s\n' "$ROOT_DIR"
printf 'Saida: %s\n' "$OUT_DIR"

printf '\n==> registrando status git sem stage\n'
{
    printf 'BRANCH:\n'
    git branch --show-current || true

    printf '\nSTATUS SHORT:\n'
    git status --short || true

    printf '\nDIFF STAT:\n'
    git diff --stat || true

    printf '\nSTAGED DIFF STAT:\n'
    git diff --cached --stat || true
} > "$STATUS"

printf 'OK: status salvo em: %s\n' "$STATUS"

printf '\n==> inventariando arquivos das frentes relevantes\n'
{
    printf '### FRENTE_RTD_EXCEL_BTG_ONLINE\n'
    find FRENTE_RTD_EXCEL_BTG_ONLINE -maxdepth 3 -type f 2>/dev/null | sort || true

    printf '\n### GUARDRAILS_36\n'
    find FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/GUARDRAILS_36 -maxdepth 3 -type f 2>/dev/null | sort || true

    printf '\n### UI_CLEANUP_35\n'
    find FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/UI_CLEANUP_35 -maxdepth 3 -type f 2>/dev/null | sort || true

    printf '\n### VERIFICACAO_COMMITS_SEQUENCIA_FULL_43\n'
    find "$BASE_OUT" -maxdepth 3 -type f 2>/dev/null | sort || true
} > "$FRONT_FILES"

printf 'OK: inventario salvo em: %s\n' "$FRONT_FILES"

printf '\n==> executando py_compile dos arquivos centrais\n'

PYTHON_BIN=""
if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
elif command -v py >/dev/null 2>&1; then
    PYTHON_BIN="py -3"
else
    printf 'ERRO: python nao encontrado no PATH.\n' | tee -a "$LOG"
    exit 2
fi

FILES_TO_COMPILE=(
    "services/payoff_refresh_command_service.py"
    "services/pricing_execution_app_service.py"
    "services/pricing_execution_orchestration_service.py"
    "services/pricing_execution_persistence_service.py"
    "services/pricing_execution_service.py"
    "services/derived_payoff_persistence.py"
    "services/derived_service.py"
    "services/canonical_pricing_facade.py"
    "repositories/structures_repository.py"
    "UI/components/terminal_vwap_payoff_dark_panel.py"
    "scripts/recalculate_payoff_curve_points_once.py"
)

COMPILE_FAIL=0

{
    printf 'Rodada 43B - py_compile central\n'
    printf 'ROOT_DIR=%s\n' "$ROOT_DIR"
    printf 'PYTHON_BIN=%s\n\n' "$PYTHON_BIN"
} >> "$LOG"

for file in "${FILES_TO_COMPILE[@]}"; do
    if [ ! -f "$file" ]; then
        printf 'SKIP: arquivo nao encontrado: %s\n' "$file" | tee -a "$LOG"
        continue
    fi

    printf 'Compilando: %s\n' "$file" | tee -a "$LOG"

    if $PYTHON_BIN -m py_compile "$file" >> "$LOG" 2>&1; then
        printf 'OK: %s\n\n' "$file" | tee -a "$LOG"
    else
        printf 'FAIL: %s\n\n' "$file" | tee -a "$LOG"
        COMPILE_FAIL=1
    fi
done

printf '\n==> gerando sumario decisorio\n'

{
    printf '# Rodada 43B - Sumario decisorio\n\n'

    printf '## Objetivo\n\n'
    printf 'Complementar a Rodada 43, confirmando compilacao dos arquivos centrais, estado do Git e inventario das frentes ja geradas, sem executar git add, commit ou push.\n\n'

    printf '## Resultado py_compile\n\n'
    if [ "$COMPILE_FAIL" -eq 0 ]; then
        printf 'Status: **OK**\n\n'
        printf 'Todos os arquivos centrais existentes compilaram com sucesso.\n\n'
    else
        printf 'Status: **FAIL**\n\n'
        printf 'Houve falha de compilacao em pelo menos um arquivo central. Corrigir antes de qualquer nova alteracao funcional.\n\n'
    fi

    printf 'Arquivo detalhado: `%s`\n\n' "$LOG"

    printf '## Arquivos de apoio gerados\n\n'
    printf -- '- Status Git: `%s`\n' "$STATUS"
    printf -- '- Inventario das frentes: `%s`\n' "$FRONT_FILES"
    printf -- '- Log py_compile: `%s`\n\n' "$LOG"

    printf '## Decisao recomendada\n\n'
    if [ "$COMPILE_FAIL" -eq 0 ]; then
        printf '1. Prosseguir para teste backend controlado sem UI.\n'
        printf '2. Confirmar se `PricingExecutionAppService.execute_pricing()` aumenta `payoff_curve_points` e `structure_decisions`.\n'
        printf '3. Se backend estiver OK, limpar/bloquear calculo local na UI.\n'
        printf '4. Se backend nao gerar payoff, corrigir contrato entre `PricingExecutionPersistenceService` e `DerivedPayoffPersistence`.\n'
    else
        printf '1. Parar desenvolvimento funcional.\n'
        printf '2. Corrigir primeiro os erros de sintaxe/indentacao apontados no py_compile.\n'
        printf '3. Reexecutar esta Rodada 43B.\n'
    fi

    printf '\n## Restricoes mantidas\n\n'
    printf -- '- Nao executar `git add`.\n'
    printf -- '- Nao executar `git commit`.\n'
    printf -- '- Nao executar `git push`.\n'
    printf -- '- Nao transformar script paralelo em fluxo oficial.\n'
    printf -- '- Nao recalcular payoff pela UI.\n'
} > "$SUMMARY"

printf 'OK: sumario salvo em: %s\n' "$SUMMARY"

if [ "$COMPILE_FAIL" -eq 0 ]; then
    printf '\nOK: Rodada 43B concluida sem falhas de py_compile.\n'
    exit 0
else
    printf '\nFAIL: Rodada 43B encontrou falhas de py_compile. Verifique: %s\n' "$LOG"
    exit 1
fi
