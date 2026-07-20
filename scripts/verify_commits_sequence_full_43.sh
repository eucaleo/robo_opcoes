#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(pwd)"
BASE="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34"
OUT="$BASE/VERIFICACAO_COMMITS_SEQUENCIA_FULL_43"
LOG="$OUT/00_log_execucao_43.txt"
SEQ="$OUT/01_sequencia_full_desenvolvimento_correcao_43.md"
COMMITS="$OUT/02_commits_anteriores_43.txt"
STATUS_OUT="$OUT/03_git_status_diff_43.txt"
PASTAS_OUT="$OUT/04_arquivos_gerados_frente_43.txt"
CONTRATO_OUT="$OUT/05_auditoria_payoff_refresh_command_service_43.txt"
BACKEND_OUT="$OUT/06_auditoria_backend_wiring_43.txt"
UI_OUT="$OUT/07_auditoria_ui_contaminacao_43.txt"
SCRIPTS_OUT="$OUT/08_auditoria_scripts_paralelos_43.txt"
PYCOMPILE_OUT="$OUT/09_pycompile_arquivos_centrais_43.txt"
GUARDRAIL_OUT="$OUT/10_guardrail_oficial_43.txt"
RESUMO="$OUT/99_resumo_operacional_43.txt"

mkdir -p "$OUT"

log() {
  printf '%s\n' "$*" | tee -a "$LOG"
}

section() {
  printf '\n==> %s\n' "$*" | tee -a "$LOG"
}

write_header() {
  {
    printf 'Rodada 43 - Verificacao de commits e sequencia full\n'
    printf 'Data local: '
    date
    printf 'Diretorio raiz: %s\n' "$ROOT"
    printf 'Saida: %s\n' "$OUT"
    printf '\n'
  } > "$LOG"
}

append_result() {
  printf '%s\n' "$*" >> "$RESUMO"
}

check_token() {
  local file="$1"
  local token="$2"
  local label="$3"

  if [ ! -f "$file" ]; then
    printf 'ERRO: arquivo nao encontrado: %s\n' "$file" >> "$CONTRATO_OUT"
    return 1
  fi

  if grep -Fq "$token" "$file"; then
    printf 'OK: %s contem token: %s\n' "$label" "$token" >> "$CONTRATO_OUT"
    return 0
  fi

  printf 'PENDENTE: %s nao contem token esperado: %s\n' "$label" "$token" >> "$CONTRATO_OUT"
  return 1
}

write_sequence_full() {
  cat > "$SEQ" <<'EOF'
# Rodada 43 - Sequencia full de desenvolvimento e correcao

## Centro de verdade mantido

UI
  -> PayoffRefreshCommandService
    -> PricingExecutionAppService
      -> PricingExecutionOrchestrationService
        -> PricingExecutionService
        -> PricingExecutionPersistenceService
          -> PricingExecutionsRepository
          -> SystemSnapshotsRepository
          -> DerivedPayoffPersistence
            -> payoff_curve_points
            -> structure_decisions

## Estado confirmado antes desta rodada

- Verificacao 38: aplicacao tecnica consistente.
- Verificacao 39: py_compile dos arquivos centrais passou.
- Verificacao 40: UI/main_window.py passou no py_compile.
- Correcao 41: erro de sintaxe em UI/main_window.py removido.
- Verificacao 42: execute_pricing sem UI aumentou as quatro contagens:
  - pricing_executions
  - structure_snapshots
  - payoff_curve_points
  - structure_decisions

## Regra operacional desta fase

- Nao executar git add.
- Nao executar git commit.
- Nao executar git push.
- Nao criar motor paralelo de payoff.
- Nao transformar script de manutencao em fluxo oficial.
- Nao corrigir UI antes de validar comando oficial.
- Nao permitir sucesso silencioso quando payoff_points_count for zero.

## Sequencia full recomendada

### 1. Verificar commits anteriores

Objetivo:
- entender a linha recente de desenvolvimento;
- evitar refazer patch ja aplicado;
- identificar arquivos alterados e nao rastreados.

Saidas esperadas:
- log recente;
- branch atual;
- status;
- diff sem stage.

### 2. Auditar arquivos ja gerados na frente

Pastas principais:
- FRENTE_RTD_EXCEL_BTG_ONLINE
- FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/GUARDRAILS_36
- FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/UI_CLEANUP_35

Objetivo:
- reaproveitar diagnosticos existentes;
- evitar duplicidade de auditoria;
- confirmar se os arquivos anteriores apontam pendencias ainda abertas.

### 3. Consolidar PayoffRefreshCommandService

Arquivo principal:
- services/payoff_refresh_command_service.py

Contrato esperado:
- valida structure_id;
- bloqueia estruturas nao active;
- captura timestamp antes;
- chama PricingExecutionAppService.execute_pricing;
- captura timestamp depois;
- conta pontos persistidos;
- valida decisao correspondente;
- retorna status ok, warning ou error;
- nunca retorna ok se payoff_points_count for zero.

### 4. Validar backend e wiring

Arquivos:
- services/pricing_execution_app_service.py
- services/pricing_execution_orchestration_service.py
- services/pricing_execution_persistence_service.py
- services/derived_payoff_persistence.py
- services/derived_service.py
- services/canonical_pricing_facade.py

Objetivo:
- confirmar que DerivedPayoffPersistence esta conectado ao fluxo oficial;
- confirmar que nao ha persistencia paralela desalinhada;
- classificar canonical_pricing_facade como fluxo oficial, fachada alternativa ou legado compativel.

### 5. Quarentenar script paralelo

Arquivo:
- scripts/recalculate_payoff_curve_points_once.py

Classificacao:
- manutencao;
- emergencia;
- legado operacional;
- nao fluxo oficial.

Regras:
- nao deve ser chamado pela UI;
- nao deve substituir PayoffRefreshCommandService;
- nao deve ser usado como motor produtivo.

### 6. Limpar UI somente depois do comando validado

Arquivo principal:
- UI/components/terminal_vwap_payoff_dark_panel.py

Pendencias esperadas:
- remover ou bloquear calculo local;
- remover fallback local;
- separar atualizar visual de recalcular payoff;
- UI deve apenas chamar comando oficial e reler snapshot persistido.

Metodos proibidos na UI:
- _calculate_payoff_from_legs
- _calculate_payoff_points_for_range
- _calculate_leg_payoff
- _collect_payoff_strikes
- _calculate_payoff_spot_range

### 7. Padronizar leitura do ultimo snapshot

Regra:
- buscar primeiro o ultimo timestamp por structure_id;
- carregar pontos somente daquele timestamp;
- buscar structure_decisions correspondente ao mesmo timestamp.

### 8. Criar ou reforcar guardrail automatico

O guardrail deve falhar se encontrar na UI:
- compute_payoff_from_canonical_input
- _calculate_payoff_from_legs
- _calculate_payoff_points_for_range
- _calculate_leg_payoff
- subprocess.run
- subprocess.Popen
- os.system
- INSERT INTO payoff_curve_points
- INSERT INTO structure_decisions

Tambem deve validar:
- PayoffRefreshCommandService existe;
- chama PricingExecutionAppService;
- chama execute_pricing;
- leitura usa ultimo timestamp;
- scripts legados nao sao chamados pela UI.

## Criterio de encerramento da fase

A fase so deve ser encerrada quando:

1. PayoffRefreshCommandService passar no contrato.
2. Backend continuar gerando as quatro persistencias.
3. Script paralelo estiver classificado como manutencao.
4. UI estiver sem calculo local ou com calculo local bloqueado por erro explicito.
5. Guardrail oficial passar.
6. py_compile dos arquivos centrais passar.
7. Git status estiver revisado conscientemente.
8. Somente entao decidir git add, commit e push controlados.
EOF
}

write_header
: > "$RESUMO"

section "verificacao 43 - commits anteriores e sequencia full"
log "Diretorio raiz: $ROOT"
log "Saida: $OUT"

section "gravando sequencia full"
write_sequence_full
log "OK: sequencia full salva em: $SEQ"

section "coletando commits anteriores"
{
  printf '== branch atual ==\n'
  git branch --show-current 2>&1
  printf '\n== upstream/status curto ==\n'
  git status -sb 2>&1
  printf '\n== ultimos 30 commits ==\n'
  git log --oneline --decorate -n 30 2>&1
  printf '\n== ultimos 10 commits com arquivos ==\n'
  git log --name-status --oneline -n 10 2>&1
} > "$COMMITS"
log "OK: commits anteriores salvos em: $COMMITS"

section "registrando git status e diff sem stage"
{
  printf '== git status ==\n'
  git status 2>&1
  printf '\n== git diff --stat ==\n'
  git diff --stat 2>&1
  printf '\n== git diff -- UI/main_window.py ==\n'
  git diff -- UI/main_window.py 2>&1
} > "$STATUS_OUT"
log "OK: status e diff salvos em: $STATUS_OUT"

section "inventariando arquivos ja gerados na frente"
{
  printf '== diretorios principais ==\n'
  for d in \
    "FRENTE_RTD_EXCEL_BTG_ONLINE" \
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34" \
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/GUARDRAILS_36" \
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/UI_CLEANUP_35" \
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_BACKEND_EXECUTE_PRICING_42" \
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_CORRECAO_38" \
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_PYCOMPILE_39" \
    "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/CORRECAO_PYCOMPILE_UI_41"
  do
    if [ -d "$d" ]; then
      printf 'OK: diretorio encontrado: %s\n' "$d"
    else
      printf 'INFO: diretorio nao encontrado: %s\n' "$d"
    fi
  done

  printf '\n== arquivos da frente, profundidade controlada ==\n'
  find FRENTE_RTD_EXCEL_BTG_ONLINE -maxdepth 4 -type f 2>/dev/null | sort
} > "$PASTAS_OUT"
log "OK: inventario salvo em: $PASTAS_OUT"

section "auditando PayoffRefreshCommandService"
{
  printf '== arquivo alvo ==\n'
  printf 'services/payoff_refresh_command_service.py\n\n'
} > "$CONTRATO_OUT"

CONTRACT_RC=0
check_token "services/payoff_refresh_command_service.py" "PricingExecutionAppService" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "execute_pricing" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "_ensure_active_structure" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "before_ts" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "after_ts" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "payoff_points_count" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "decision_found" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "\"ok\"" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "\"warning\"" "PayoffRefreshCommandService" || CONTRACT_RC=1
check_token "services/payoff_refresh_command_service.py" "\"error\"" "PayoffRefreshCommandService" || CONTRACT_RC=1

{
  printf '\n== funcoes/classes detectadas ==\n'
  grep -nE '^(class |    def |def )' services/payoff_refresh_command_service.py 2>&1 || true

  printf '\n== referencias a payoff_curve_points e structure_decisions ==\n'
  grep -nE 'payoff_curve_points|structure_decisions|MAX\\(timestamp\\)|ORDER BY timestamp|LIMIT 1' services/payoff_refresh_command_service.py 2>&1 || true
} >> "$CONTRATO_OUT"

if [ "$CONTRACT_RC" -eq 0 ]; then
  log "OK: contrato textual do PayoffRefreshCommandService parece completo."
  append_result "OK: PayoffRefreshCommandService contem tokens essenciais do contrato."
else
  log "PENDENTE: contrato textual do PayoffRefreshCommandService precisa revisao."
  append_result "PENDENTE: PayoffRefreshCommandService nao contem todos os tokens esperados."
fi

section "auditando backend e wiring"
{
  printf '== arquivos centrais ==\n'
  for f in \
    "services/pricing_execution_app_service.py" \
    "services/pricing_execution_orchestration_service.py" \
    "services/pricing_execution_persistence_service.py" \
    "services/derived_payoff_persistence.py" \
    "services/derived_service.py" \
    "services/canonical_pricing_facade.py"
  do
    if [ -f "$f" ]; then
      printf 'OK: arquivo encontrado: %s\n' "$f"
    else
      printf 'ERRO: arquivo ausente: %s\n' "$f"
    fi
  done

  printf '\n== referencias DerivedPayoffPersistence ==\n'
  grep -RIn "DerivedPayoffPersistence" services 2>/dev/null || true

  printf '\n== referencias PricingExecutionPersistenceService ==\n'
  grep -RIn "PricingExecutionPersistenceService" services 2>/dev/null || true

  printf '\n== referencias payoff_persistence_port ==\n'
  grep -RIn "payoff_persistence_port" services 2>/dev/null || true

  printf '\n== entrypoints execute_pricing ==\n'
  grep -RIn "execute_pricing" services UI api controllers scripts 2>/dev/null || true
} > "$BACKEND_OUT"
log "OK: auditoria backend salva em: $BACKEND_OUT"

section "auditando UI contra contaminacao de calculo local"
{
  printf '== tokens proibidos ou pendentes na UI ==\n'
  for token in \
    "compute_payoff_from_canonical_input" \
    "_calculate_payoff_from_legs" \
    "_calculate_payoff_points_for_range" \
    "_calculate_leg_payoff" \
    "_collect_payoff_strikes" \
    "_calculate_payoff_spot_range" \
    "subprocess.run" \
    "subprocess.Popen" \
    "os.system" \
    "INSERT INTO payoff_curve_points" \
    "INSERT INTO structure_decisions"
  do
    printf '\n-- token: %s --\n' "$token"
    grep -RInF "$token" UI 2>/dev/null || true
  done

  printf '\n== chamadas especificas do fallback local ==\n'
  grep -RInE '_load_payoff_points|_load_persisted_payoff_points|_calculate_payoff_points_for_range' UI/components/terminal_vwap_payoff_dark_panel.py 2>/dev/null || true

  printf '\n== leitura ultimo timestamp em UI ==\n'
  grep -RInE 'MAX\\(timestamp\\)|ORDER BY timestamp DESC|latest.*timestamp|ultimo_timestamp' UI 2>/dev/null || true
} > "$UI_OUT"
log "OK: auditoria UI salva em: $UI_OUT"

section "auditando scripts paralelos"
{
  printf '== script de recalc paralelo ==\n'
  if [ -f "scripts/recalculate_payoff_curve_points_once.py" ]; then
    printf 'OK: arquivo encontrado: scripts/recalculate_payoff_curve_points_once.py\n'
    printf '\n== cabecalho inicial ==\n'
    sed -n '1,80p' scripts/recalculate_payoff_curve_points_once.py
    printf '\n== tokens de motor paralelo ==\n'
    grep -nE 'structure_legs|rtd_option_quotes|rtd_underlying_quotes|payoff_curve_points|INSERT|calculate|grid|spot|bid|ask|mid|vwap' scripts/recalculate_payoff_curve_points_once.py 2>&1 || true
  else
    printf 'INFO: script nao encontrado.\n'
  fi

  printf '\n== UI chamando scripts ou subprocess ==\n'
  grep -RInE 'recalculate_payoff_curve_points_once|subprocess|os.system|Popen' UI 2>/dev/null || true
} > "$SCRIPTS_OUT"
log "OK: auditoria scripts salva em: $SCRIPTS_OUT"

section "executando py_compile dos arquivos centrais"
{
  PY_FILES=(
    "UI/main_window.py"
    "UI/components/terminal_vwap_payoff_dark_panel.py"
    "services/payoff_refresh_command_service.py"
    "services/pricing_execution_app_service.py"
    "services/pricing_execution_orchestration_service.py"
    "services/pricing_execution_persistence_service.py"
    "services/derived_payoff_persistence.py"
    "services/derived_service.py"
    "services/canonical_pricing_facade.py"
    "scripts/recalculate_payoff_curve_points_once.py"
    "scripts/verify_payoff_center_of_truth_scope.py"
  )

  PY_RC=0

  for f in "${PY_FILES[@]}"; do
    printf '\n== py_compile: %s ==\n' "$f"
    if [ -f "$f" ]; then
      python -m py_compile "$f" 2>&1
      rc=$?
      if [ "$rc" -eq 0 ]; then
        printf 'OK: %s\n' "$f"
      else
        printf 'ERRO: %s rc=%s\n' "$f" "$rc"
        PY_RC=1
      fi
    else
      printf 'INFO: arquivo ausente: %s\n' "$f"
    fi
  done

  printf '\nPY_RC=%s\n' "$PY_RC"
  exit "$PY_RC"
} > "$PYCOMPILE_OUT" 2>&1
PYCOMPILE_RC=$?

if [ "$PYCOMPILE_RC" -eq 0 ]; then
  log "OK: py_compile dos arquivos centrais passou."
  append_result "OK: py_compile dos arquivos centrais passou."
else
  log "ERRO: py_compile encontrou falha. Ver arquivo: $PYCOMPILE_OUT"
  append_result "ERRO: py_compile encontrou falha."
fi

section "executando guardrail oficial, se existir"
if [ -f "scripts/verify_payoff_center_of_truth_scope.py" ]; then
  python scripts/verify_payoff_center_of_truth_scope.py > "$GUARDRAIL_OUT" 2>&1
  GUARDRAIL_RC=$?
  if [ "$GUARDRAIL_RC" -eq 0 ]; then
    log "OK: guardrail oficial passou."
    append_result "OK: guardrail oficial passou."
  else
    log "PENDENTE: guardrail oficial falhou. Ver arquivo: $GUARDRAIL_OUT"
    append_result "PENDENTE: guardrail oficial falhou."
  fi
else
  {
    printf 'INFO: scripts/verify_payoff_center_of_truth_scope.py nao encontrado.\n'
  } > "$GUARDRAIL_OUT"
  GUARDRAIL_RC=0
  log "INFO: guardrail oficial nao encontrado."
  append_result "INFO: guardrail oficial nao encontrado."
fi

section "resumo operacional"
{
  printf 'Rodada 43 - Resumo operacional\n'
  printf 'Data local: '
  date
  printf '\n'
  cat "$RESUMO"
  printf '\nArquivos gerados em:\n%s\n' "$OUT"
  printf '\nNenhum git add, commit ou push foi executado.\n'
  printf '\nProxima decisao tecnica:\n'
  printf '1. Se PayoffRefreshCommandService estiver completo, rodar teste funcional do comando oficial.\n'
  printf '2. Se o comando oficial passar, iniciar correcao UI para remover fallback local.\n'
  printf '3. Se o comando oficial falhar, corrigir somente services/payoff_refresh_command_service.py ou wiring backend.\n'
} > "$RESUMO"

cat "$RESUMO" | tee -a "$LOG"

section "status git final"
git status --short | tee -a "$LOG"

FINAL_RC=0
if [ "$PYCOMPILE_RC" -ne 0 ]; then
  FINAL_RC=1
fi
if [ "${GUARDRAIL_RC:-0}" -ne 0 ]; then
  FINAL_RC=1
fi

if [ "$FINAL_RC" -eq 0 ]; then
  log ""
  log "RESULTADO: OK"
  log "Verificacao 43 concluida sem falha bloqueante automatica."
else
  log ""
  log "RESULTADO: PENDENTE"
  log "Ha falha bloqueante ou pendencia automatica. Ver arquivos da rodada 43."
fi

log ""
log "Nenhum git add, commit ou push foi executado por este script."

exit "$FINAL_RC"
