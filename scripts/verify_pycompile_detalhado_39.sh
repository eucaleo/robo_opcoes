#!/usr/bin/env bash
set -u

echo
echo "==> verificacao 39 - diagnostico detalhado de py_compile"
echo

ROOT_DIR="$(pwd)"
BASE_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34"
OUT_DIR="${BASE_DIR}/VERIFICACAO_PYCOMPILE_39"

mkdir -p "${OUT_DIR}"

SUMMARY="${OUT_DIR}/00_resumo_pycompile_39.txt"
STATUS_FILE="${OUT_DIR}/01_status_git_inicial.txt"
FILES_FILE="${OUT_DIR}/02_arquivos_testados.txt"
FAIL_RAW="${OUT_DIR}/03_py_compile_falhas_raw.txt"
FAIL_CONTEXT="${OUT_DIR}/04_py_compile_falhas_contexto.txt"
PASS_FILE="${OUT_DIR}/05_py_compile_ok.txt"
DIFF_FILE="${OUT_DIR}/06_diff_atual_sem_stage.txt"
CONCLUSION="${OUT_DIR}/07_conclusao_operacional.txt"

: > "${SUMMARY}"
: > "${STATUS_FILE}"
: > "${FILES_FILE}"
: > "${FAIL_RAW}"
: > "${FAIL_CONTEXT}"
: > "${PASS_FILE}"
: > "${DIFF_FILE}"
: > "${CONCLUSION}"

log() {
    echo "$1"
    echo "$1" >> "${SUMMARY}"
}

log "==> verificacao 39 - diagnostico detalhado de py_compile"
log "Data local: $(date)"
log "Diretorio raiz: ${ROOT_DIR}"
log ""

log "==> status git inicial"
git status --short > "${STATUS_FILE}" 2>&1
cat "${STATUS_FILE}"
log ""

FILES_TO_TEST=(
    "UI/main_window.py"
    "UI/components/terminal_vwap_payoff_dark_panel.py"
    "services/derived_payoff_persistence.py"
    "services/derived_service.py"
    "services/pricing_execution_persistence_service.py"
    "services/payoff_refresh_command_service.py"
    "services/pricing_execution_app_service.py"
    "services/pricing_execution_orchestration_service.py"
    "scripts/recalculate_payoff_curve_points_once.py"
    "scripts/verify_payoff_center_of_truth_scope.py"
)

log "==> validando presenca dos arquivos"
missing=0

for f in "${FILES_TO_TEST[@]}"; do
    echo "${f}" >> "${FILES_FILE}"

    if [ -f "${f}" ]; then
        log "OK: arquivo encontrado: ${f}"
    else
        log "FALHA: arquivo ausente: ${f}"
        missing=1
    fi
done

log ""

if [ "${missing}" -ne 0 ]; then
    log "RESULTADO: FALHA por arquivo ausente."
    {
        echo "RESULTADO: FALHA"
        echo
        echo "Existe arquivo central ausente. Verifique:"
        echo "${FILES_FILE}"
        echo
        echo "Nenhum git add, commit ou push foi executado."
    } > "${CONCLUSION}"

    echo
    cat "${CONCLUSION}"
    echo
    echo "Arquivos gerados em: ${OUT_DIR}"
    echo "EXIT_CODE=1"
    read -r -p "Pressione ENTER para fechar..."
    exit 1
fi

log "==> executando py_compile arquivo por arquivo"
fail_count=0

for f in "${FILES_TO_TEST[@]}"; do
    tmp="${OUT_DIR}/tmp_pycompile_stderr.txt"
    : > "${tmp}"

    echo
    echo "==> py_compile: ${f}"

    if python -m py_compile "${f}" > "${tmp}" 2>&1; then
        echo "OK: ${f}"
        echo "OK: ${f}" >> "${PASS_FILE}"
    else
        echo "FALHA: ${f}"
        fail_count=$((fail_count + 1))

        {
            echo "============================================================"
            echo "ARQUIVO: ${f}"
            echo "============================================================"
            cat "${tmp}"
            echo
        } >> "${FAIL_RAW}"

        line_num="$(
            sed -n 's/.*line \([0-9][0-9]*\).*/\1/p' "${tmp}" | head -n 1
        )"

        {
            echo "============================================================"
            echo "ARQUIVO: ${f}"
            echo "============================================================"
            echo "Erro bruto:"
            cat "${tmp}"
            echo

            if [ -n "${line_num}" ]; then
                echo "Contexto aproximado da linha ${line_num}:"
                start=$((line_num - 12))
                end=$((line_num + 12))

                if [ "${start}" -lt 1 ]; then
                    start=1
                fi

                awk -v start="${start}" -v end="${end}" '
                    NR >= start && NR <= end {
                        marker = "   "
                        if (NR == int((start + end) / 2)) {
                            marker = "   "
                        }
                        printf "%s%6d: %s\n", marker, NR, $0
                    }
                ' "${f}"
            else
                echo "Nao foi possivel extrair numero de linha automaticamente."
            fi

            echo
        } >> "${FAIL_CONTEXT}"
    fi

    rm -f "${tmp}"
done

log ""
log "==> registrando diff atual sem stage"
git diff -- UI/main_window.py > "${DIFF_FILE}" 2>&1
git diff --stat >> "${DIFF_FILE}" 2>&1

log ""
log "==> resultado final"

if [ "${fail_count}" -eq 0 ]; then
    {
        echo "RESULTADO: OK"
        echo
        echo "Todos os arquivos centrais passaram em py_compile."
        echo
        echo "Proxima etapa sugerida:"
        echo "1. Rodar novamente scripts/verify_aplicacao_correcao_38.sh"
        echo "2. Se passar, rodar o verificador oficial:"
        echo "   python scripts/verify_payoff_center_of_truth_scope.py"
        echo "3. Somente depois decidir encerramento da fase."
        echo
        echo "Nenhum git add, commit ou push foi executado."
    } > "${CONCLUSION}"

    cat "${CONCLUSION}"
    echo
    echo "Arquivos gerados em: ${OUT_DIR}"
    echo "EXIT_CODE=0"
    read -r -p "Pressione ENTER para fechar..."
    exit 0
else
    {
        echo "RESULTADO: FALHA"
        echo
        echo "py_compile falhou em ${fail_count} arquivo(s)."
        echo
        echo "Abrir principalmente:"
        echo "${FAIL_RAW}"
        echo "${FAIL_CONTEXT}"
        echo
        echo "Nao executar git add, commit ou push ainda."
        echo "Corrigir primeiro o erro de sintaxe apontado no contexto."
        echo
        echo "Nenhum git add, commit ou push foi executado."
    } > "${CONCLUSION}"

    cat "${CONCLUSION}"
    echo
    echo "Arquivos gerados em: ${OUT_DIR}"
    echo "EXIT_CODE=1"
    read -r -p "Pressione ENTER para fechar..."
    exit 1
fi
