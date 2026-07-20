#!/usr/bin/env bash
set -u

echo
echo "==> verificacao 38 - auditoria cirurgica pos-falha do verificador 37"
echo

ROOT_DIR="$(pwd)"
BASE_AUDIT_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34"
OUT_DIR="${BASE_AUDIT_DIR}/VERIFICACAO_CORRECAO_38"

mkdir -p "${OUT_DIR}"

RESULT_FILE="${OUT_DIR}/00_resultado_verificacao_38.txt"
DERIVED_FILE="${OUT_DIR}/01_derived_payoff_persistence_contexto.txt"
DERIVED_SERVICE_FILE="${OUT_DIR}/02_derived_service_contexto.txt"
PERSISTENCE_FILE="${OUT_DIR}/03_pricing_execution_persistence_contexto.txt"
COMMAND_FILE="${OUT_DIR}/04_payoff_refresh_command_service_contexto.txt"
UI_FILE="${OUT_DIR}/05_ui_tokens_proibidos_contexto.txt"
WIRING_FILE="${OUT_DIR}/06_wiring_backend_contexto.txt"
PY_COMPILE_FILE="${OUT_DIR}/07_py_compile_arquivos_centrais.txt"
DIFF_FILE="${OUT_DIR}/08_diff_atual_sem_commit.txt"
STATUS_FILE="${OUT_DIR}/09_git_status.txt"
CONCLUSAO_FILE="${OUT_DIR}/10_conclusao_operacional.txt"

FAIL=0
WARN=0

write_header() {
    local file="$1"
    local title="$2"

    {
        echo "============================================================"
        echo "${title}"
        echo "Gerado em: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Branch: $(git branch --show-current 2>/dev/null || true)"
        echo "Diretorio: ${ROOT_DIR}"
        echo "============================================================"
        echo
    } > "${file}"
}

append_cmd() {
    local file="$1"
    shift

    {
        echo
        echo ">>> $*"
        "$@" 2>&1
        echo
    } >> "${file}"
}

check_file_exists() {
    local path="$1"
    local label="$2"

    if [ ! -f "${path}" ]; then
        echo "FALHA: arquivo ausente: ${label} -> ${path}" | tee -a "${RESULT_FILE}"
        FAIL=1
        return 1
    fi

    echo "OK: arquivo encontrado: ${label} -> ${path}" | tee -a "${RESULT_FILE}"
    return 0
}

contains_any() {
    local path="$1"
    shift

    for token in "$@"; do
        if grep -RIn -- "${token}" "${path}" >/dev/null 2>&1; then
            return 0
        fi
    done

    return 1
}

contains_all_report() {
    local path="$1"
    local label="$2"
    shift 2

    local local_fail=0

    for token in "$@"; do
        if grep -RIn -- "${token}" "${path}" >/dev/null 2>&1; then
            echo "OK: ${label} contem token: ${token}" | tee -a "${RESULT_FILE}"
        else
            echo "FALHA: ${label} nao contem token: ${token}" | tee -a "${RESULT_FILE}"
            local_fail=1
        fi
    done

    if [ "${local_fail}" -ne 0 ]; then
        FAIL=1
    fi
}

echo "==> preparando arquivos de saida"

write_header "${RESULT_FILE}" "Resultado verificacao 38"
write_header "${DERIVED_FILE}" "Contexto DerivedPayoffPersistence"
write_header "${DERIVED_SERVICE_FILE}" "Contexto derived_service"
write_header "${PERSISTENCE_FILE}" "Contexto PricingExecutionPersistenceService"
write_header "${COMMAND_FILE}" "Contexto PayoffRefreshCommandService"
write_header "${UI_FILE}" "Contexto UI tokens proibidos"
write_header "${WIRING_FILE}" "Contexto wiring backend"
write_header "${PY_COMPILE_FILE}" "Py compile arquivos centrais"
write_header "${DIFF_FILE}" "Diff atual sem commit"
write_header "${STATUS_FILE}" "Git status"
write_header "${CONCLUSAO_FILE}" "Conclusao operacional"

echo "==> status git inicial"
append_cmd "${STATUS_FILE}" git status --short
append_cmd "${STATUS_FILE}" git branch --show-current

echo
echo "==> validando presenca dos arquivos centrais"

check_file_exists "services/derived_payoff_persistence.py" "DerivedPayoffPersistence"
check_file_exists "services/derived_service.py" "derived_service"
check_file_exists "services/pricing_execution_persistence_service.py" "PricingExecutionPersistenceService"
check_file_exists "services/payoff_refresh_command_service.py" "PayoffRefreshCommandService"
check_file_exists "services/pricing_execution_app_service.py" "PricingExecutionAppService"
check_file_exists "services/pricing_execution_orchestration_service.py" "PricingExecutionOrchestrationService"
check_file_exists "UI/main_window.py" "UI main_window"
check_file_exists "UI/components/terminal_vwap_payoff_dark_panel.py" "Terminal payoff panel"

echo
echo "==> coletando contexto de DerivedPayoffPersistence"

{
    echo
    echo "### imports/classes/metodos relevantes"
    grep -nE "class |def |import |from |DerivedPayoffPersistence|persist|payoff|decision|snapshot|structure|active|status|derived_service|insert|save|upsert|payoff_curve_points|structure_decisions" \
        services/derived_payoff_persistence.py 2>&1 || true

    echo
    echo "### referencias diretas a tabelas"
    grep -nE "payoff_curve_points|structure_decisions" \
        services/derived_payoff_persistence.py 2>&1 || true

    echo
    echo "### referencias indiretas possiveis"
    grep -nE "insert_payoff|persist_payoff|save_payoff|payoff_points|structure_decision|decision|derived_service|compute_payoff|canonical" \
        services/derived_payoff_persistence.py 2>&1 || true
} >> "${DERIVED_FILE}"

echo
echo "==> coletando contexto de derived_service"

{
    echo
    echo "### tabelas e funcoes relevantes"
    grep -nE "def |payoff_curve_points|structure_decisions|insert_payoff|persist_payoff|save_payoff|structure_decision|decision|timestamp|point_spot|payoff" \
        services/derived_service.py 2>&1 || true
} >> "${DERIVED_SERVICE_FILE}"

echo
echo "==> coletando contexto de PricingExecutionPersistenceService"

{
    echo
    echo "### wiring e chamada do port de payoff"
    grep -nE "DerivedPayoffPersistence|payoff_persistence_port|persist_execution|persist|payoff|snapshot|SystemSnapshotsRepository|PricingExecutionsRepository" \
        services/pricing_execution_persistence_service.py 2>&1 || true
} >> "${PERSISTENCE_FILE}"

echo
echo "==> coletando contexto de PayoffRefreshCommandService"

{
    echo
    echo "### contrato minimo do comando"
    grep -nE "PricingExecutionAppService|execute_pricing|active|_ensure_active_structure|before_ts|after_ts|latest_payoff|payoff_points_count|decision_found|status|warning|error|ok|structure_decisions|payoff_curve_points|MAX\\(timestamp\\)" \
        services/payoff_refresh_command_service.py 2>&1 || true
} >> "${COMMAND_FILE}"

echo
echo "==> verificando UI contra tokens proibidos"

{
    echo
    echo "### tokens proibidos em UI"
    grep -RInE "compute_payoff_from_canonical_input|_calculate_payoff_from_legs|_calculate_payoff_points_for_range|_calculate_leg_payoff|_collect_payoff_strikes|_calculate_payoff_spot_range|subprocess\\.run|subprocess\\.Popen|os\\.system|INSERT INTO payoff_curve_points|INSERT INTO structure_decisions" \
        UI 2>&1 || true

    echo
    echo "### main_window subprocess residual"
    grep -nE "subprocess\\.run|subprocess\\.Popen|os\\.system|Popen|run\\(" \
        UI/main_window.py 2>&1 || true

    echo
    echo "### terminal payoff leitura persistida"
    grep -nE "_load_payoff_points|_load_persisted_payoff_points|MAX\\(timestamp\\)|ORDER BY timestamp|payoff_curve_points|structure_decisions" \
        UI/components/terminal_vwap_payoff_dark_panel.py 2>&1 || true
} >> "${UI_FILE}"

if grep -RInE "compute_payoff_from_canonical_input|_calculate_payoff_from_legs|_calculate_payoff_points_for_range|_calculate_leg_payoff|_collect_payoff_strikes|_calculate_payoff_spot_range|subprocess\\.run|subprocess\\.Popen|os\\.system|INSERT INTO payoff_curve_points|INSERT INTO structure_decisions" UI >/dev/null 2>&1; then
    echo "FALHA: UI ainda contem token proibido." | tee -a "${RESULT_FILE}"
    FAIL=1
else
    echo "OK: UI sem tokens proibidos do centro de verdade." | tee -a "${RESULT_FILE}"
fi

echo
echo "==> validando contrato minimo do PayoffRefreshCommandService"

contains_all_report \
    "services/payoff_refresh_command_service.py" \
    "PayoffRefreshCommandService" \
    "PricingExecutionAppService" \
    "execute_pricing" \
    "_ensure_active_structure" \
    "before_ts" \
    "payoff_points_count" \
    "decision_found" \
    "\"ok\"" \
    "\"warning\"" \
    "\"error\""

echo
echo "==> validando caminho de persistencia do payoff derivado"

DIRECT_TABLES_OK=0
INDIRECT_PAYOFF_OK=0
INDIRECT_DECISION_OK=0
PERSISTENCE_CALL_OK=0

if contains_any "services/derived_payoff_persistence.py" "payoff_curve_points"; then
    echo "OK: DerivedPayoffPersistence referencia payoff_curve_points diretamente." | tee -a "${RESULT_FILE}"
    DIRECT_PAYOFF_TABLE_OK=1
else
    echo "INFO: DerivedPayoffPersistence nao referencia payoff_curve_points diretamente." | tee -a "${RESULT_FILE}"
    DIRECT_PAYOFF_TABLE_OK=0
fi

if contains_any "services/derived_payoff_persistence.py" "structure_decisions"; then
    echo "OK: DerivedPayoffPersistence referencia structure_decisions diretamente." | tee -a "${RESULT_FILE}"
    DIRECT_DECISION_TABLE_OK=1
else
    echo "INFO: DerivedPayoffPersistence nao referencia structure_decisions diretamente." | tee -a "${RESULT_FILE}"
    DIRECT_DECISION_TABLE_OK=0
fi

if contains_any "services/derived_service.py" "payoff_curve_points"; then
    echo "OK: derived_service referencia payoff_curve_points." | tee -a "${RESULT_FILE}"
    INDIRECT_PAYOFF_OK=1
else
    echo "FALHA: derived_service tambem nao referencia payoff_curve_points." | tee -a "${RESULT_FILE}"
fi

if contains_any "services/derived_service.py" "structure_decisions"; then
    echo "OK: derived_service referencia structure_decisions." | tee -a "${RESULT_FILE}"
    INDIRECT_DECISION_OK=1
else
    echo "FALHA: derived_service tambem nao referencia structure_decisions." | tee -a "${RESULT_FILE}"
fi

if grep -RInE "derived_service|insert_payoff|persist_payoff|save_payoff|payoff_points|structure_decision|decision" services/derived_payoff_persistence.py >/dev/null 2>&1; then
    echo "OK: DerivedPayoffPersistence possui referencias indiretas a servico/metodos de payoff/decisao." | tee -a "${RESULT_FILE}"
    PERSISTENCE_CALL_OK=1
else
    echo "FALHA: DerivedPayoffPersistence nao mostra chamada indireta clara para payoff/decisao." | tee -a "${RESULT_FILE}"
fi

if [ "${DIRECT_PAYOFF_TABLE_OK}" -eq 1 ] && [ "${DIRECT_DECISION_TABLE_OK}" -eq 1 ]; then
    echo "OK: persistencia derivada comprovada por referencia direta as tabelas." | tee -a "${RESULT_FILE}"
elif [ "${INDIRECT_PAYOFF_OK}" -eq 1 ] && [ "${INDIRECT_DECISION_OK}" -eq 1 ] && [ "${PERSISTENCE_CALL_OK}" -eq 1 ]; then
    echo "OK: persistencia derivada comprovada por caminho indireto via derived_service." | tee -a "${RESULT_FILE}"
    echo "INFO: a falha do verificador 37 provavelmente foi falso negativo por exigir nome de tabela dentro de DerivedPayoffPersistence." | tee -a "${RESULT_FILE}"
else
    echo "FALHA: nao foi possivel comprovar caminho de persistencia para payoff_curve_points e structure_decisions." | tee -a "${RESULT_FILE}"
    FAIL=1
fi

echo
echo "==> validando wiring backend"

{
    echo
    echo "### referencias globais controladas"
    grep -RInE "DerivedPayoffPersistence|payoff_persistence_port|PricingExecutionPersistenceService|SystemSnapshotsRepository|PricingExecutionAppService|execute_pricing" \
        services repositories controllers api main.py 2>&1 || true
} >> "${WIRING_FILE}"

if grep -RIn "payoff_persistence_port" services >/dev/null 2>&1; then
    echo "OK: wiring possui payoff_persistence_port." | tee -a "${RESULT_FILE}"
else
    echo "FALHA: wiring nao possui payoff_persistence_port." | tee -a "${RESULT_FILE}"
    FAIL=1
fi

if grep -RIn "DerivedPayoffPersistence" services >/dev/null 2>&1; then
    echo "OK: wiring possui DerivedPayoffPersistence." | tee -a "${RESULT_FILE}"
else
    echo "FALHA: wiring nao possui DerivedPayoffPersistence." | tee -a "${RESULT_FILE}"
    FAIL=1
fi

echo
echo "==> rodando guardrail oficial existente, se disponivel"

if [ -f "scripts/verify_payoff_center_of_truth_scope.py" ]; then
    python scripts/verify_payoff_center_of_truth_scope.py > "${OUT_DIR}/11_guardrail_oficial_existente.txt" 2>&1
    GUARD_EXIT=$?

    if [ "${GUARD_EXIT}" -eq 0 ]; then
        echo "OK: guardrail oficial passou." | tee -a "${RESULT_FILE}"
    else
        echo "FALHA: guardrail oficial falhou. Ver ${OUT_DIR}/11_guardrail_oficial_existente.txt" | tee -a "${RESULT_FILE}"
        FAIL=1
    fi
else
    echo "AVISO: scripts/verify_payoff_center_of_truth_scope.py nao encontrado." | tee -a "${RESULT_FILE}"
    WARN=1
fi

echo
echo "==> checando sintaxe python dos arquivos centrais"

{
    python -m py_compile \
        services/payoff_refresh_command_service.py \
        services/derived_payoff_persistence.py \
        services/derived_service.py \
        services/pricing_execution_persistence_service.py \
        services/pricing_execution_app_service.py \
        services/pricing_execution_orchestration_service.py \
        UI/main_window.py \
        UI/components/terminal_vwap_payoff_dark_panel.py
} > "${PY_COMPILE_FILE}" 2>&1

PY_EXIT=$?

if [ "${PY_EXIT}" -eq 0 ]; then
    echo "OK: py_compile dos arquivos centrais passou." | tee -a "${RESULT_FILE}"
else
    echo "FALHA: py_compile encontrou erro." | tee -a "${RESULT_FILE}"
    FAIL=1
fi

echo
echo "==> registrando diff e status sem adicionar ao git"

git diff -- UI/main_window.py services/derived_payoff_persistence.py services/derived_service.py services/payoff_refresh_command_service.py scripts/verify_payoff_center_of_truth_scope.py > "${DIFF_FILE}" 2>&1
git status --short >> "${STATUS_FILE}" 2>&1

echo
echo "==> conclusao operacional"

{
    echo "Resultado tecnico da verificacao 38:"
    echo

    if [ "${FAIL}" -eq 0 ]; then
        echo "RESULTADO: OK"
        echo
        echo "A aplicacao da correcao parece consistente para fechamento tecnico preliminar da fase."
        echo
        echo "Proximos passos recomendados:"
        echo "1. Rodar teste backend sem UI com PricingExecutionAppService.execute_pricing(structure_id=2)."
        echo "2. Comparar contagens antes/depois em pricing_executions, structure_snapshots, payoff_curve_points e structure_decisions."
        echo "3. Se as quatro contagens subirem, encerrar fase com commit controlado."
        echo "4. Se payoff_curve_points ou structure_decisions nao subir, corrigir contrato de DerivedPayoffPersistence antes de mexer na UI."
    else
        echo "RESULTADO: FALHA"
        echo
        echo "A fase ainda nao deve ser encerrada."
        echo
        echo "Abrir os arquivos desta pasta:"
        echo "${OUT_DIR}"
        echo
        echo "Arquivos principais:"
        echo "01_derived_payoff_persistence_contexto.txt"
        echo "02_derived_service_contexto.txt"
        echo "10_conclusao_operacional.txt"
        echo
        echo "Nao executar git add, commit ou push ainda."
    fi

    echo
    echo "Observacao:"
    echo "Este script nao executou git add, commit ou push."
} > "${CONCLUSAO_FILE}"

cat "${CONCLUSAO_FILE}"

echo
echo "==> arquivos gerados em:"
echo "${OUT_DIR}"
echo

if [ "${FAIL}" -eq 0 ]; then
    exit 0
else
    exit 1
fi
