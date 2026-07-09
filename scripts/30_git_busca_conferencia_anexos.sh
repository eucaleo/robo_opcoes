#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

TS="$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="reports"
BAK_DIR="BAK"
PATCH_DIR="patches"
REPORT_FILE="${REPORT_DIR}/git_busca_conferencia_anexos_${TS}.md"

mkdir -p "$REPORT_DIR" "$BAK_DIR" "$PATCH_DIR"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  :
else
  echo "ERRO: diretório atual não é um repositório git."
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current 2>/dev/null || echo 'DETACHED')"
CURRENT_COMMIT="$(git rev-parse HEAD 2>/dev/null || echo 'UNKNOWN')"

{
  echo "# Relatório de busca e conferência com anexos"
  echo
  echo "- Data/Hora: ${TS}"
  echo "- Projeto: ${PROJECT_ROOT}"
  echo "- Branch atual: ${CURRENT_BRANCH}"
  echo "- Commit atual: ${CURRENT_COMMIT}"
  echo
  echo "## 1. Atualização do git"
} > "$REPORT_FILE"

echo "[1/10] Atualizando referências remotas..." | tee -a "$REPORT_FILE"
git fetch --all --prune >> "$REPORT_FILE" 2>&1 || true

{
  echo
  echo '```bash'
  git status --short || true
  echo '```'
  echo
  echo "## 2. Branches e últimos commits"
  echo
  echo '```bash'
  git branch -a || true
  echo
  git log --oneline --decorate -n 20 || true
  echo '```'
  echo
  echo "## 3. Diretórios relevantes encontrados"
  echo
  echo '```bash'
  find . -maxdepth 2 -type d | sort
  echo '```'
  echo
  echo "## 4. Arquivos-chave citados nos anexos"
  echo
} >> "$REPORT_FILE"

KEY_FILES=(
  "scripts/run_derived_pipeline.py"
  "services/derived_service.py"
  "domain/payoff.py"
  "domain/decision.py"
  "repositories/robo_legs_repository.py"
  "repositories/robo_legs_status_repository.py"
  "services/robo_legs_service.py"
  "services/robo_legs_status_service.py"
  "utils/leg_normalizers.py"
  "infra/bootstrap_structures_schema.py"
  "repositories/structures_repository.py"
  "scripts/10_smoke_structures_repository.py"
  "api/pricing_execution_controller.py"
  "services/pricing_input_service.py"
  "services/pricing_execution_service.py"
  "services/pricing_execution_persistence_service.py"
  "services/pricing_execution_query_service.py"
  "services/pricing_execution_orchestration_service.py"
  "services/pricing_execution_app_service.py"
  "repositories/pricing_executions_repository.py"
  "UI/main_window.py"
  "UI/models/ui_data.py"
  "docs/ROTEIRO_MIGRACAO_ESTRUTURAS.md"
  "docs/baseline_v1b_unificado.md"
)

for f in "${KEY_FILES[@]}"; do
  if [[ -e "$f" ]]; then
    echo "- OK: $f" >> "$REPORT_FILE"
  else
    echo "- FALTA: $f" >> "$REPORT_FILE"
  fi
done

{
  echo
  echo "## 5. Busca por paths e nomes citados nos anexos"
  echo
  echo "### 5.1 Referências a dados/app.db e dados/derived.db"
  echo
  echo '```bash'
} >> "$REPORT_FILE"

grep -RInE "dados/app\.db|dados/derived\.db" . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=__pycache__ \
  --exclude="*.pyc" >> "$REPORT_FILE" 2>/dev/null || true

{
  echo '```'
  echo
  echo "### 5.2 Referências a tabelas/raw/derived relevantes"
  echo
  echo '```bash'
} >> "$REPORT_FILE"

grep -RInE "rtd_analise_robo_legs|manual_analise_robo_legs|rtd_analise_robo|structure_decisions|payoff_curve_points|structures|structure_legs" . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=__pycache__ \
  --exclude="*.pyc" >> "$REPORT_FILE" 2>/dev/null || true

{
  echo '```'
  echo
  echo "### 5.3 Referências a aba, timestamp, alias_legacy_aba"
  echo
  echo '```bash'
} >> "$REPORT_FILE"

grep -RInE "alias_legacy_aba|aba|timestamp" . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=__pycache__ \
  --exclude="*.pyc" >> "$REPORT_FILE" 2>/dev/null || true

{
  echo '```'
  echo
  echo "### 5.4 Referências a pricing executions"
  echo
  echo '```bash'
} >> "$REPORT_FILE"

grep -RInE "pricing_execution|pricing_executions|PricingExecution" . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=__pycache__ \
  --exclude="*.pyc" >> "$REPORT_FILE" 2>/dev/null || true

{
  echo '```'
  echo
  echo "## 6. Arquivos modificados no branch atual"
  echo
  echo '```bash'
  git diff --name-only || true
  echo '```'
  echo
  echo "## 7. Arquivos não rastreados"
  echo
  echo '```bash'
  git ls-files --others --exclude-standard || true
  echo '```'
  echo
  echo "## 8. Histórico recente que pode corresponder aos anexos"
  echo
  echo '```bash'
} >> "$REPORT_FILE"

git log --oneline --decorate --all \
  --grep="robo legs" \
  --grep="datetime normalization" \
  --grep="structures" \
  --grep="pricing" \
  --grep="persist" \
  --grep="query" \
  --grep="error" \
  --grep="facade" \
  -i -n 100 >> "$REPORT_FILE" 2>/dev/null || true

{
  echo '```'
  echo
  echo "## 9. Patches existentes"
  echo
  echo '```bash'
  find "$PATCH_DIR" -maxdepth 2 -type f | sort || true
  echo '```'
  echo
  echo "## 10. Conclusão automática"
  echo
} >> "$REPORT_FILE"

HAS_DATA=0
HAS_DADOS=$(grep -RIl "dados/app.db\|dados/derived.db" . --exclude-dir=.git --exclude-dir=.venv --exclude="*.pyc" | wc -l | tr -d ' ')

{
  echo "- Arquivos com referência a \`data/*\`: ${HAS_DATA}"
  echo "- Arquivos com referência a \`dados/*\`: ${HAS_DADOS}"
  echo
  if [[ "$HAS_DATA" -gt 0 && "$HAS_DADOS" -gt 0 ]]; then
    echo "> Atenção: há coexistência de referências a \`data/\` e \`dados/\`. Isso deve ser conferido antes de novos patches."
  fi
  echo
  echo "Relatório gerado em: \`${REPORT_FILE}\`"
} >> "$REPORT_FILE"

echo
echo "OK: relatório gerado em ${REPORT_FILE}"
