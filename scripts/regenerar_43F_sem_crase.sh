#!/usr/bin/env bash
set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

BASE="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43F_CONSOLIDACAO_FINAL_PRE_COMMIT"

mkdir -p "$BASE"

LOG="$BASE/00_log_43F.txt"
REL="$BASE/01_relatorio_consolidacao_final_43F.md"
SEQ="$BASE/02_sequencia_full_desenvolvimento_correcao_43F.md"
COMMITS="$BASE/03_commits_anteriores_completos_43F.md"
INV="$BASE/04_inventario_artefatos_relevantes_43F.txt"
TESTES="$BASE/05_testes_finais_43F.txt"
GUARD="$BASE/06_guardrail_ui_final_43F.txt"
STATUS_DIFF="$BASE/07_git_status_diff_final_43F.txt"
MATRIZ="$BASE/08_matriz_evidencias_final_43F.md"
JSON="$BASE/09_resumo_tecnico_43F.json"

: > "$LOG"
exec > >(tee -a "$LOG") 2>&1

say() {
    printf '\n==> %s\n' "$*"
}

sanitize_file() {
    python - "$1" <<'PY'
from pathlib import Path
import sys

p = Path(sys.argv[1])
if not p.exists():
    sys.exit(0)

txt = p.read_text(encoding="utf-8", errors="replace")
txt = txt.replace(chr(96), "'")
p.write_text(txt, encoding="utf-8", newline="\n")
PY
}

sanitize_all() {
    find "$BASE" -type f \( -name "*.md" -o -name "*.txt" -o -name "*.json" \) -print0 |
    while IFS= read -r -d '' f
    do
        sanitize_file "$f"
    done
}

validate_no_crase() {
    python - "$BASE" <<'PY'
from pathlib import Path
import sys

base = Path(sys.argv[1])
bad = []

for p in base.rglob("*"):
    if p.is_file():
        txt = p.read_text(encoding="utf-8", errors="replace")
        if chr(96) in txt:
            bad.append(str(p))

if bad:
    print("FALHA: arquivos ainda contem crase:")
    for item in bad:
        print(" - " + item)
    sys.exit(1)

print("OK: nenhum arquivo 43F gerado contem crase.")
PY
}

NOW="$(date '+%Y-%m-%d %H:%M:%S %z')"
BRANCH="$(git branch --show-current 2>/dev/null || echo desconhecida)"
HEAD_SHORT="$(git rev-parse --short HEAD 2>/dev/null || echo desconhecido)"

say "Regenerando Rodada 43F sem crase"
printf 'Data: %s\n' "$NOW"
printf 'Raiz: %s\n' "$ROOT"
printf 'Branch: %s\n' "$BRANCH"
printf 'HEAD: %s\n' "$HEAD_SHORT"
printf 'Saida: %s\n' "$BASE"

say "Validando diretorios obrigatorios"

REQUIRED_DIRS=(
    "FRENTE_RTD_EXCEL_BTG_ONLINE"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/GUARDRAILS_36"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/UI_CLEANUP_35"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_BACKEND_EXECUTE_PRICING_42"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43C_UI_BLOCK_E_PRINTF_FIX"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43D_UI_TEXT_CLEANUP_E_GUARDRAIL"
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43E_DOCUMENTACAO_ENCERRAMENTO_FASE"
)

DIR_STATUS="OK"

for d in "${REQUIRED_DIRS[@]}"
do
    if [ -d "$d" ]; then
        printf 'OK: %s\n' "$d"
    else
        printf 'FALHA: diretorio ausente: %s\n' "$d"
        DIR_STATUS="FALHA"
    fi
done

say "Gerando inventario de artefatos relevantes"

{
    printf 'Inventario de artefatos relevantes - Rodada 43F\n'
    printf 'Data: %s\n' "$NOW"
    printf 'Branch: %s\n' "$BRANCH"
    printf 'HEAD: %s\n' "$HEAD_SHORT"
    printf '\nArquivos sob a frente de auditoria:\n\n'

    find FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34 \
        -type f \
        | sort \
        | sed 's/^/    - /'
} > "$INV"

say "Registrando commits anteriores completos"

{
    printf '# Commits anteriores completos - Rodada 43F\n\n'
    printf 'Data de geracao: %s\n\n' "$NOW"
    printf 'Branch: %s\n\n' "$BRANCH"
    printf 'HEAD: %s\n\n' "$HEAD_SHORT"
    printf '## Historico completo do Git\n\n'
    git log --date=iso --pretty=format:'commit %H%nData: %ad%nAutor: %an <%ae>%nAssunto: %s%n%n%b%n----%n' --all
    printf '\n'
} > "$COMMITS"

say "Gerando sequencia full de desenvolvimento e correcao"

{
    printf '# Sequencia full de desenvolvimento e correcao - Rodada 43F\n\n'

    printf '## Objetivo\n\n'
    printf 'Consolidar, em ordem historica e tecnica, a frente de centralizacao do payoff no backend, a limpeza da UI, os guardrails e as validacoes finais antes de qualquer commit controlado.\n\n'

    printf '## Centro de verdade consolidado\n\n'
    printf '    UI\n'
    printf '      -> PayoffRefreshCommandService\n'
    printf '        -> PricingExecutionAppService\n'
    printf '          -> PricingExecutionOrchestrationService\n'
    printf '            -> PricingExecutionService\n'
    printf '            -> PricingExecutionPersistenceService\n'
    printf '              -> PricingExecutionsRepository\n'
    printf '              -> SystemSnapshotsRepository\n'
    printf '              -> DerivedPayoffPersistence\n'
    printf '                -> payoff_curve_points\n'
    printf '                -> structure_decisions\n\n'

    printf '## Regra operacional final\n\n'
    printf '    UI:\n'
    printf '      - nao recalcula payoff\n'
    printf '      - nao executa pipeline local\n'
    printf '      - nao abre processos externos para recalc ou pipeline\n'
    printf '      - nao grava payoff_curve_points\n'
    printf '      - nao grava structure_decisions\n'
    printf '      - apenas rele dados persistidos e renderiza\n\n'

    printf '    Backend:\n'
    printf '      - executa pricing\n'
    printf '      - persiste snapshots\n'
    printf '      - persiste payoff derivado\n'
    printf '      - persiste decisoes\n'
    printf '      - valida estruturas active\n\n'

    printf '## Linha do tempo completa dos commits\n\n'
    git log --date=short --pretty=format:'    - %ad | %h | %s' --all
    printf '\n\n'

    printf '## Evidencias documentais consultadas\n\n'

    for d in "${REQUIRED_DIRS[@]}"
    do
        if [ -d "$d" ]; then
            printf '### %s\n\n' "$d"
            find "$d" -maxdepth 3 -type f | sort | sed 's/^/    - /'
            printf '\n'
        fi
    done

    printf '## Decisao tecnica\n\n'
    printf 'A fase fica apta para fechamento controlado somente se os testes finais 43F permanecerem OK.\n\n'
    printf 'Este documento nao executa git add, git commit ou git push.\n'
} > "$SEQ"

say "Executando testes finais 43F"

DIFF_OK="OK"
PYC_OK="OK"

{
    printf 'Testes finais - Rodada 43F\n\n'

    printf '1. git diff --check\n'
    printf '--------------------\n'
} > "$TESTES"

if git diff --check >> "$TESTES" 2>&1; then
    printf 'OK: git diff --check sem problemas.\n\n' >> "$TESTES"
else
    printf 'FALHA: git diff --check encontrou problemas.\n\n' >> "$TESTES"
    DIFF_OK="FALHA"
fi

{
    printf '2. py_compile arquivos centrais\n'
    printf '-------------------------------\n'
} >> "$TESTES"

PY_FILES=(
    "UI/main_window.py"
    "UI/components/details_panel.py"
    "UI/components/structure_editor_dialog.py"
    "UI/components/terminal_vwap_payoff_dark_panel.py"
    "UI/models/ui_data.py"
)

EXISTING_PY_FILES=()

for f in "${PY_FILES[@]}"
do
    if [ -f "$f" ]; then
        EXISTING_PY_FILES+=("$f")
    fi
done

if [ "${#EXISTING_PY_FILES[@]}" -gt 0 ]; then
    if python -m py_compile "${EXISTING_PY_FILES[@]}" >> "$TESTES" 2>&1; then
        printf 'OK: py_compile final passou.\n' >> "$TESTES"
    else
        printf 'FALHA: py_compile final falhou.\n' >> "$TESTES"
        PYC_OK="FALHA"
    fi
else
    printf 'FALHA: nenhum arquivo Python central encontrado para py_compile.\n' >> "$TESTES"
    PYC_OK="FALHA"
fi

say "Executando guardrail final UI"

GUARD_OK="OK"
TMP_GUARD="$BASE/.tmp_guardrail_hits_43F.txt"
: > "$TMP_GUARD"

TOKENS=(
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

{
    printf '# Guardrail UI final - Rodada 43F\n\n'
    printf '## Tokens fortes proibidos\n\n'
} > "$GUARD"

for token in "${TOKENS[@]}"
do
    printf 'Token analisado: %s\n' "$token" >> "$GUARD"

    if grep -RIn --include='*.py' --exclude-dir='__pycache__' -F "$token" UI >> "$TMP_GUARD" 2>/dev/null; then
        printf 'Resultado: FALHA, token encontrado em UI.\n\n' >> "$GUARD"
        GUARD_OK="FALHA"
    else
        printf 'Resultado: OK, token ausente em UI.\n\n' >> "$GUARD"
    fi
done

if [ -s "$TMP_GUARD" ]; then
    {
        printf '\n## Ocorrencias bloqueantes encontradas\n\n'
        sed 's/^/    /' "$TMP_GUARD"
    } >> "$GUARD"
fi

{
    printf '\n## Busca informativa permitida\n\n'
    grep -RInE 'structure_decisions|payoff_curve_points|PayoffRefreshCommandService|Executar Pipeline|run_pipeline|fluxo externo legado|processos externos' UI 2>/dev/null | sed 's/^/    /' || true
} >> "$GUARD"

rm -f "$TMP_GUARD"

say "Registrando status git e diff final"

{
    printf 'BRANCH:\n'
    git branch --show-current 2>/dev/null || true

    printf '\nHEAD:\n'
    git rev-parse --short HEAD 2>/dev/null || true

    printf '\nSTATUS SHORT:\n'
    git status --short

    printf '\nDIFF STAT:\n'
    git diff --stat

    printf '\nDIFF NAME-STATUS:\n'
    git diff --name-status

    printf '\nUNTRACKED FILES:\n'
    git ls-files --others --exclude-standard

    printf '\nDIFF UI FINAL:\n'
    git diff -- UI/components/details_panel.py UI/components/structure_editor_dialog.py UI/main_window.py
} > "$STATUS_DIFF"

say "Gerando matriz de evidencias final"

{
    printf '# Matriz de evidencias final - Rodada 43F\n\n'

    printf '## Evidencias obrigatorias\n\n'
    printf '    - %s\n' "$LOG"
    printf '    - %s\n' "$REL"
    printf '    - %s\n' "$SEQ"
    printf '    - %s\n' "$COMMITS"
    printf '    - %s\n' "$INV"
    printf '    - %s\n' "$TESTES"
    printf '    - %s\n' "$GUARD"
    printf '    - %s\n' "$STATUS_DIFF"
    printf '    - %s\n' "$MATRIZ"
    printf '    - %s\n' "$JSON"

    printf '\n## Evidencias anteriores verificadas\n\n'
    for d in "${REQUIRED_DIRS[@]}"
    do
        if [ -d "$d" ]; then
            printf '    - OK: %s\n' "$d"
        else
            printf '    - FALHA: %s\n' "$d"
        fi
    done

    printf '\n## Criterios de encerramento\n\n'
    printf '    - Diretorios obrigatorios presentes.\n'
    printf '    - Sequencia de commits anteriores registrada.\n'
    printf '    - Sequencia full de desenvolvimento e correcao gerada.\n'
    printf '    - git diff --check OK.\n'
    printf '    - py_compile OK.\n'
    printf '    - Guardrail UI OK.\n'
    printf '    - Nenhum git add, git commit ou git push executado por este script.\n'
    printf '    - Arquivos gerados sem crase.\n'
} > "$MATRIZ"

say "Gerando resumo JSON"

export JSON_PATH="$JSON"
export JSON_NOW="$NOW"
export JSON_BRANCH="$BRANCH"
export JSON_HEAD="$HEAD_SHORT"
export JSON_DIR_STATUS="$DIR_STATUS"
export JSON_DIFF_OK="$DIFF_OK"
export JSON_PYC_OK="$PYC_OK"
export JSON_GUARD_OK="$GUARD_OK"

python - <<'PY'
import json
import os
from pathlib import Path

data = {
    "rodada": "43F",
    "tipo": "consolidacao_final_pre_commit",
    "geracao": os.environ.get("JSON_NOW"),
    "branch": os.environ.get("JSON_BRANCH"),
    "head": os.environ.get("JSON_HEAD"),
    "status_diretorios": os.environ.get("JSON_DIR_STATUS"),
    "git_diff_check": os.environ.get("JSON_DIFF_OK"),
    "py_compile": os.environ.get("JSON_PYC_OK"),
    "guardrail_ui": os.environ.get("JSON_GUARD_OK"),
    "sem_git_add": True,
    "sem_git_commit": True,
    "sem_git_push": True,
    "sem_crase": True,
    "decisao": "apta para fechamento controlado posterior se todos os status forem OK"
}

Path(os.environ["JSON_PATH"]).write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)
PY

say "Gerando relatorio final"

FINAL_STATUS="OK"

if [ "$DIR_STATUS" != "OK" ]; then
    FINAL_STATUS="FALHA"
fi

if [ "$DIFF_OK" != "OK" ]; then
    FINAL_STATUS="FALHA"
fi

if [ "$PYC_OK" != "OK" ]; then
    FINAL_STATUS="FALHA"
fi

if [ "$GUARD_OK" != "OK" ]; then
    FINAL_STATUS="FALHA"
fi

{
    printf '# Rodada 43F - Consolidacao final pre-commit\n\n'

    printf '## Resultado\n\n'
    printf 'Status: %s\n\n' "$FINAL_STATUS"

    printf '## Escopo\n\n'
    printf '    - Verificar commits anteriores.\n'
    printf '    - Adicionar sequencia full de desenvolvimento e correcao.\n'
    printf '    - Conferir artefatos ja gerados nas pastas da frente RTD e centro de verdade.\n'
    printf '    - Reexecutar testes finais antes de qualquer fechamento controlado.\n'
    printf '    - Nao executar stage, commit ou push.\n'
    printf '    - Gerar documentacao sem crase para evitar arquivo incompleto.\n\n'

    printf '## Arquivos principais gerados\n\n'
    printf '    - Sequencia full: %s\n' "$SEQ"
    printf '    - Commits anteriores: %s\n' "$COMMITS"
    printf '    - Inventario: %s\n' "$INV"
    printf '    - Testes finais: %s\n' "$TESTES"
    printf '    - Guardrail UI: %s\n' "$GUARD"
    printf '    - Git status e diff: %s\n' "$STATUS_DIFF"
    printf '    - Matriz: %s\n' "$MATRIZ"
    printf '    - JSON: %s\n' "$JSON"

    printf '\n## Resultado dos controles\n\n'
    printf '    - Diretorios obrigatorios: %s\n' "$DIR_STATUS"
    printf '    - git diff --check: %s\n' "$DIFF_OK"
    printf '    - py_compile: %s\n' "$PYC_OK"
    printf '    - Guardrail UI: %s\n' "$GUARD_OK"
    printf '    - Sem crase nos arquivos gerados: validado ao final do script\n\n'

    printf '## Decisao\n\n'
    if [ "$FINAL_STATUS" = "OK" ]; then
        printf 'A fase permanece apta para fechamento controlado posterior.\n\n'
        printf 'Proxima etapa recomendada:\n\n'
        printf '    1. Revisar visualmente os arquivos 43F regenerados.\n'
        printf '    2. Confirmar que o diff final contem somente o escopo aprovado.\n'
        printf '    3. Avancar para encerramento da rota em etapa separada.\n'
    else
        printf 'A fase nao deve ser encerrada ate corrigir os itens com FALHA.\n'
    fi

    printf '\n## Restricoes mantidas\n\n'
    printf '    - Sem git add.\n'
    printf '    - Sem git commit.\n'
    printf '    - Sem git push.\n'
} > "$REL"

say "Sanitizando arquivos gerados para remover crase"

sanitize_all
validate_no_crase

say "Resultado final"

if [ "$FINAL_STATUS" = "OK" ]; then
    printf 'OK: Rodada 43F regenerada sem crase e apta para revisao final.\n'
    printf 'Relatorio: %s\n' "$REL"
    printf 'Sequencia full: %s\n' "$SEQ"
    printf 'Testes: %s\n' "$TESTES"
    printf 'Guardrail: %s\n' "$GUARD"
    printf 'Status diff: %s\n' "$STATUS_DIFF"
    exit 0
else
    printf 'FALHA: Rodada 43F regenerada, mas controles finais nao passaram.\n'
    printf 'Verifique: %s\n' "$REL"
    exit 1
fi
