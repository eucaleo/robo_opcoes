#!/usr/bin/env bash
set -u

ROOT="$(pwd)"
BASE="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34"
OUT="$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43F_CONSOLIDACAO_FINAL_PRE_COMMIT"

LOG="$OUT/00_log_43F.txt"
REL="$OUT/01_relatorio_consolidacao_final_43F.md"
SEQ="$OUT/02_sequencia_full_desenvolvimento_correcao_43F.md"
COMMITS="$OUT/03_commits_anteriores_completos_43F.md"
ART="$OUT/04_inventario_artefatos_relevantes_43F.txt"
TESTS="$OUT/05_testes_finais_43F.txt"
GUARD="$OUT/06_guardrail_ui_final_43F.txt"
STATUS="$OUT/07_git_status_diff_final_43F.txt"
MATRIX="$OUT/08_matriz_evidencias_final_43F.md"
JSON="$OUT/09_resumo_tecnico_43F.json"

mkdir -p "$OUT"
: > "$LOG"

log() {
  printf '%s\n' "$*" | tee -a "$LOG"
}

section() {
  printf '\n==> %s\n' "$*" | tee -a "$LOG"
}

section "Rodada 43F - consolidacao final pre-commit"
log "Data: $(date)"
log "Diretorio raiz: $ROOT"
log "Saida: $OUT"

section "validando diretorios obrigatorios"

DIRS=(
  "FRENTE_RTD_EXCEL_BTG_ONLINE"
  "$BASE"
  "$BASE/GUARDRAILS_36"
  "$BASE/UI_CLEANUP_35"
  "$BASE/VERIFICACAO_BACKEND_EXECUTE_PRICING_42"
  "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43"
  "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43C_UI_BLOCK_E_PRINTF_FIX"
  "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43D_UI_TEXT_CLEANUP_E_GUARDRAIL"
  "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43E_DOCUMENTACAO_ENCERRAMENTO_FASE"
)

DIR_FAIL=0
for d in "${DIRS[@]}"; do
  if [ -d "$d" ]; then
    log "OK: $d"
  else
    log "FALTA: $d"
    DIR_FAIL=1
  fi
done

section "inventariando artefatos relevantes"
{
  echo "Inventario de artefatos relevantes - Rodada 43F"
  echo
  echo "Raiz:"
  echo "    $ROOT"
  echo
  echo "Diretorios principais:"
  for d in "${DIRS[@]}"; do
    echo "    $d"
  done
  echo
  echo "Arquivos encontrados nas frentes relevantes:"
  find \
    "FRENTE_RTD_EXCEL_BTG_ONLINE" \
    "$BASE/GUARDRAILS_36" \
    "$BASE/UI_CLEANUP_35" \
    "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43" \
    -maxdepth 5 \
    -type f \
    2>/dev/null \
    | sort \
    | sed 's/^/    /'
} > "$ART"
log "OK: inventario salvo em: $ART"

section "registrando commits anteriores completos"
{
  echo "# Commits anteriores completos - Rodada 43F"
  echo
  echo "Branch atual:"
  echo
  echo '```text'
  git branch --show-current
  echo '```'
  echo
  echo "## Ultimos 140 commits"
  echo
  echo '```text'
  git log -140 --date=iso-local --pretty=format:'%h | %ad | %an | %s'
  echo
  echo '```'
  echo
  echo "## Commits com estatistica curta desde 2026-07-09"
  echo
  echo '```text'
  git log --since='2026-07-09 00:00:00' --stat --oneline --date=iso-local
  echo '```'
} > "$COMMITS"
log "OK: commits salvos em: $COMMITS"

section "gerando sequencia full de desenvolvimento e correcao"
{
  echo "# Sequencia full de desenvolvimento e correcao - Rodada 43F"
  echo
  echo "## Objetivo"
  echo
  echo "Consolidar, em ordem historica e tecnica, a frente de centralizacao do payoff no backend,"
  echo "a limpeza da UI, os guardrails e as validacoes finais antes de qualquer commit controlado."
  echo
  echo "## Centro de verdade consolidado"
  echo
  echo '```text'
  echo "UI"
  echo "  -> PayoffRefreshCommandService"
  echo "    -> PricingExecutionAppService"
  echo "      -> PricingExecutionOrchestrationService"
  echo "        -> PricingExecutionService"
  echo "        -> PricingExecutionPersistenceService"
  echo "          -> PricingExecutionsRepository"
  echo "          -> SystemSnapshotsRepository"
  echo "          -> DerivedPayoffPersistence"
  echo "            -> payoff_curve_points"
  echo "            -> structure_decisions"
  echo '```'
  echo
  echo "## Regra operacional final"
  echo
  echo '```text'
  echo "UI:"
  echo "  - nao recalcula payoff"
  echo "  - nao executa pipeline local"
  echo "  - nao abre processos externos para recalc/pipeline"
  echo "  - nao grava payoff_curve_points"
  echo "  - nao grava structure_decisions"
  echo "  - apenas rele dados persistidos e renderiza"
  echo
  echo "Backend:"
  echo "  - executa pricing"
  echo "  - persiste snapshots"
  echo "  - persiste payoff derivado"
  echo "  - persiste decisoes"
  echo "  - valida estruturas active"
  echo '```'
  echo
  echo "## Linha do tempo sintetica"
  echo
  echo "### Base RTD / Excel / BD unico"
  echo
  git log --since='2026-07-09 00:00:00' --until='2026-07-13 23:59:59' \
    --reverse --date=short --pretty=format:'    - %ad | %h | %s'
  echo
  echo
  echo "### Evolucao payoff persistido e snapshots"
  echo
  git log --since='2026-07-15 00:00:00' --until='2026-07-15 23:59:59' \
    --reverse --date=short --pretty=format:'    - %ad | %h | %s'
  echo
  echo
  echo "### Centro de verdade, backend e bloqueios UI"
  echo
  git log --since='2026-07-17 00:00:00' --until='2026-07-17 23:59:59' \
    --reverse --date=short --pretty=format:'    - %ad | %h | %s'
  echo
  echo
  echo "### Guardrails, cleanup e encerramento"
  echo
  git log --since='2026-07-20 00:00:00' \
    --reverse --date=short --pretty=format:'    - %ad | %h | %s'
  echo
  echo
  echo "## Evidencias documentais consultadas"
  echo
  echo '```text'
  for p in \
    "$BASE/GUARDRAILS_36" \
    "$BASE/UI_CLEANUP_35" \
    "$BASE/VERIFICACAO_BACKEND_EXECUTE_PRICING_42" \
    "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43C_UI_BLOCK_E_PRINTF_FIX" \
    "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43D_UI_TEXT_CLEANUP_E_GUARDRAIL" \
    "$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43/43E_DOCUMENTACAO_ENCERRAMENTO_FASE"
  do
    echo "$p"
    find "$p" -maxdepth 2 -type f 2>/dev/null | sort | sed 's/^/    /'
    echo
  done
  echo '```'
  echo
  echo "## Decisao tecnica"
  echo
  echo "A fase fica apta para fechamento controlado somente se os testes finais 43F permanecerem OK."
  echo
  echo "Este documento nao executa git add, git commit ou git push."
} > "$SEQ"
log "OK: sequencia full salva em: $SEQ"

section "executando testes finais 43F"

TEST_FAIL=0
: > "$TESTS"

{
  echo "Testes finais - Rodada 43F"
  echo
  echo "1. git diff --check"
  echo "--------------------"
} >> "$TESTS"

if git diff --check >> "$TESTS" 2>&1; then
  log "OK: git diff --check sem problemas."
  echo "OK: git diff --check sem problemas." >> "$TESTS"
else
  log "FALHA: git diff --check encontrou problemas."
  echo "FALHA: git diff --check encontrou problemas." >> "$TESTS"
  TEST_FAIL=1
fi

{
  echo
  echo "2. py_compile arquivos centrais"
  echo "-------------------------------"
} >> "$TESTS"

if python -m py_compile \
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
  scripts/recalculate_payoff_curve_points_once.py \
  >> "$TESTS" 2>&1
then
  log "OK: py_compile final passou."
  echo "OK: py_compile final passou." >> "$TESTS"
else
  log "FALHA: py_compile final falhou."
  echo "FALHA: py_compile final falhou." >> "$TESTS"
  TEST_FAIL=1
fi

section "executando guardrail final UI"

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

GUARD_FAIL=0
{
  echo "# Guardrail UI final - Rodada 43F"
  echo
  echo "## Tokens fortes proibidos"
  echo
} > "$GUARD"

for token in "${TOKENS[@]}"; do
  {
    echo
    echo "-- token: $token --"
  } >> "$GUARD"

  if grep -RInF -- "$token" UI >> "$GUARD" 2>/dev/null; then
    GUARD_FAIL=1
  fi
done

{
  echo
  echo "## Busca informativa permitida"
  echo
  grep -RInE "payoff_curve_points|structure_decisions|PayoffRefreshCommandService|pipeline|processos externos|fluxo externo legado" UI 2>/dev/null || true
} >> "$GUARD"

if [ "$GUARD_FAIL" -eq 0 ]; then
  log "OK: guardrail UI sem tokens fortes proibidos."
else
  log "FALHA: guardrail UI encontrou token forte proibido."
  TEST_FAIL=1
fi

section "registrando status git e diff final"

{
  echo "BRANCH:"
  git branch --show-current
  echo
  echo "STATUS SHORT:"
  git status --short
  echo
  echo "DIFF STAT:"
  git diff --stat
  echo
  echo "DIFF NAME-STATUS:"
  git diff --name-status
  echo
  echo "UNTRACKED FILES:"
  git ls-files --others --exclude-standard
  echo
  echo "DIFF UI FINAL:"
  git diff -- UI/main_window.py UI/components/details_panel.py UI/components/structure_editor_dialog.py
} > "$STATUS"

log "OK: status/diff salvos em: $STATUS"

section "gerando matriz de evidencias final"

{
  echo "# Matriz de evidencias final - Rodada 43F"
  echo
  echo "## Evidencias obrigatorias"
  echo
  for f in "$LOG" "$REL" "$SEQ" "$COMMITS" "$ART" "$TESTS" "$GUARD" "$STATUS" "$JSON"; do
    echo "- \`$f\`"
  done
  echo
  echo "## Evidencias anteriores verificadas"
  echo
  for d in "${DIRS[@]}"; do
    if [ -d "$d" ]; then
      echo "- OK: \`$d\`"
    else
      echo "- FALTA: \`$d\`"
    fi
  done
  echo
  echo "## Criterios de encerramento"
  echo
  echo "- Diretorios obrigatorios presentes."
  echo "- Sequencia de commits anteriores registrada."
  echo "- Sequencia full de desenvolvimento/correcao gerada."
  echo "- \`git diff --check\` OK."
  echo "- \`py_compile\` OK."
  echo "- Guardrail UI OK."
  echo "- Nenhum \`git add\`, \`git commit\` ou \`git push\` executado por este script."
} > "$MATRIX"

log "OK: matriz final salva em: $MATRIX"

section "gerando resumo JSON"

STATUS_FINAL="ok"
if [ "$DIR_FAIL" -ne 0 ] || [ "$TEST_FAIL" -ne 0 ]; then
  STATUS_FINAL="fail"
fi

cat > "$JSON" <<JSON_EOF
{
  "rodada": "43F",
  "status": "$STATUS_FINAL",
  "branch": "$(git branch --show-current)",
  "saida": "$OUT",
  "validacoes": {
    "diretorios_obrigatorios": $([ "$DIR_FAIL" -eq 0 ] && echo true || echo false),
    "git_diff_check": $([ "$TEST_FAIL" -eq 0 ] && echo true || echo false),
    "py_compile": $([ "$TEST_FAIL" -eq 0 ] && echo true || echo false),
    "guardrail_ui": $([ "$GUARD_FAIL" -eq 0 ] && echo true || echo false)
  },
  "restricoes": {
    "git_add": false,
    "git_commit": false,
    "git_push": false
  }
}
JSON_EOF

log "OK: resumo JSON salvo em: $JSON"

section "gerando relatorio final"

{
  echo "# Rodada 43F - Consolidacao final pre-commit"
  echo
  echo "## Resultado"
  echo
  if [ "$STATUS_FINAL" = "ok" ]; then
    echo "Status: **OK**"
  else
    echo "Status: **FALHA**"
  fi
  echo
  echo "## Escopo"
  echo
  echo "- Verificar commits anteriores."
  echo "- Adicionar sequencia full de desenvolvimento e correcao."
  echo "- Conferir artefatos ja gerados nas pastas da frente RTD/centro de verdade."
  echo "- Reexecutar testes finais antes de qualquer fechamento controlado."
  echo "- Nao executar stage, commit ou push."
  echo
  echo "## Arquivos principais gerados"
  echo
  echo "- Sequencia full: \`$SEQ\`"
  echo "- Commits anteriores: \`$COMMITS\`"
  echo "- Inventario: \`$ART\`"
  echo "- Testes finais: \`$TESTS\`"
  echo "- Guardrail UI: \`$GUARD\`"
  echo "- Git status/diff: \`$STATUS\`"
  echo "- Matriz: \`$MATRIX\`"
  echo "- JSON: \`$JSON\`"
  echo
  echo "## Decisao"
  if [ "$STATUS_FINAL" = "ok" ]; then
    echo "A fase permanece apta para fechamento controlado posterior."
    echo
    echo "Proxima etapa recomendada:"
    echo
    echo "1. Revisar visualmente os arquivos 43F."
    echo "2. Confirmar que o diff final contem somente o escopo aprovado."
    echo "3. Somente depois preparar commit controlado em etapa separada."
  else
    echo "A fase nao deve ser fechada ate corrigir as falhas registradas."
  fi
  echo
  echo "## Restricoes mantidas"
  echo
  echo "- Sem \`git add\`."
  echo "- Sem \`git commit\`."
  echo "- Sem \`git push\`."
} > "$REL"

log "OK: relatorio salvo em: $REL"

section "resultado final"
if [ "$STATUS_FINAL" = "ok" ]; then
  log "OK: Rodada 43F concluida com consolidacao final apta."
  log "Relatorio: $REL"
  log "Sequencia full: $SEQ"
  log "Commits: $COMMITS"
  log "Testes: $TESTS"
  log "Guardrail: $GUARD"
  exit 0
else
  log "FALHA: Rodada 43F encontrou pendencias."
  log "Verifique: $LOG"
  exit 1
fi
