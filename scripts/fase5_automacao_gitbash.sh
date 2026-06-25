#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

CHECKPOINT_DIR="docs/checkpoints"
AUDITORIA_DIR="docs/auditoria"
SCRIPTS_DIR="scripts"

FASE5_DOC="$CHECKPOINT_DIR/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_ATUALIZAR_DADOS_PIPELINE.md"
AUDITORIA_DOC="$AUDITORIA_DIR/AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL.md"
EVOLUCAO_DOC="docs/EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL.md"

RELATORIO_FLUXO="$CHECKPOINT_DIR/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_DIAGNOSTICO_ATUALIZAR_DADOS.md"
RELATORIO_CONTRATO="$CHECKPOINT_DIR/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_CONTRATO_RESUMO_PIPELINE.md"

BUSCA_SCRIPT="$SCRIPTS_DIR/fase5_buscar_fluxo_atualizar_dados.sh"
CONTRATO_SCRIPT="$SCRIPTS_DIR/fase5_checar_resumo_pipeline.sh"

mkdir -p "$CHECKPOINT_DIR" "$AUDITORIA_DIR" "$SCRIPTS_DIR"

git_add_if_exists() {
  for path in "$@"; do
    if [ -e "$path" ]; then
      git add "$path"
    else
      echo "Aviso: arquivo não encontrado para git add: $path"
    fi
  done
}

commit_if_needed() {
  local message="$1"

  if git diff --cached --quiet; then
    echo "Nada staged para commit: $message"
    return 0
  fi

  git commit -m "$message"
}

prepare_docs() {
  echo "Preparando documentos da Fase 5 e registros de encerramento..."

  if [ ! -f "$FASE5_DOC" ] || [ "${OVERWRITE_DOCS:-0}" = "1" ]; then
    cat > "$FASE5_DOC" <<'MD'
# REVISÃO FUNCIONAL PÓS-USO REAL — FASE 5 — ATUALIZAR DADOS E RESUMO DO PIPELINE

## Status

Aberta para diagnóstico.

---

## Objetivo da fase

Auditar e melhorar o comportamento do botão Atualizar Dados, garantindo que a ação executada pelo usuário seja rastreável, compreensível e verificável.

O sistema deve informar claramente:

- o que foi executado;
- quais dados foram lidos;
- quais dados foram processados;
- quais dados foram ignorados;
- quais dados foram atualizados;
- quais decisões foram geradas;
- quais pontos de payoff foram gerados;
- quais cotações RTD foram atualizadas;
- se houve avisos;
- se houve erros;
- se a execução ocorreu, mas não gerou dados novos.

---

## Origem

Esta fase faz parte da rota:

    NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL

Ela é iniciada após o encerramento da Fase 4, que validou a integração das estruturas manuais com payoff e decisões.

---

## Problema central

O botão Atualizar Dados pode executar ações importantes do pipeline, mas o usuário pode não receber feedback suficiente sobre o resultado.

O risco principal é o sistema exibir uma mensagem genérica de sucesso, mesmo quando:

- nenhuma estrutura foi processada;
- nenhuma cotação RTD foi atualizada;
- nenhum ponto de payoff foi gerado;
- nenhuma decisão foi criada;
- todos os contadores retornaram zero;
- ocorreu erro parcial;
- houve rejeições ou avisos não exibidos.

---

## Regra principal da fase

Se o pipeline executar corretamente, mas todos os resultados forem zero, o sistema não deve exibir apenas uma mensagem genérica de sucesso.

Deve informar algo equivalente a:

    Atualização executada, mas nenhum dado novo foi gerado.

E, quando possível, detalhar os contadores.

---

## Pontos a investigar

1. Onde está o botão Atualizar Dados.
2. Qual função é chamada pelo clique.
3. Qual serviço ou script é acionado.
4. Quais pipelines são executados.
5. Quais contadores já existem.
6. Quais contadores precisam ser criados.
7. Como erros são capturados.
8. Como avisos são tratados.
9. Onde a mensagem final é montada.
10. Se a tela é atualizada após a execução.
11. Se existe diferença entre sucesso com dados e sucesso sem dados novos.

---

## Informações mínimas esperadas no resumo

| Campo | Descrição |
|---|---|
| Estruturas lidas | Quantidade de estruturas consideradas |
| Estruturas processadas | Quantidade de estruturas efetivamente processadas |
| Estruturas ignoradas | Quantidade de estruturas ignoradas |
| Pontos de payoff gerados | Quantidade de registros gerados em payoff_curve_points |
| Decisões geradas | Quantidade de registros gerados em structure_decisions |
| Cotações RTD atualizadas | Quantidade de cotações atualizadas |
| Avisos | Lista ou quantidade de avisos |
| Erros | Lista ou quantidade de erros |
| Status final | Sucesso, sucesso sem dados novos, aviso ou erro |

---

## Arquivos inicialmente relacionados

Arquivos candidatos para investigação:

    scripts/run_derived_pipeline.py
    scripts/run_rtd_option_quotes_pipeline.py
    scripts/run_rtd_refresh_full.py
    scripts/refresh_rtd_option_quotes_excel.ps1
    repositories/rtd_option_quotes_repository.py
    UI/components/structure_editor_dialog.py
    ATT/tests/test_run_rtd_option_quotes_pipeline.py
    ATT/tests/test_run_derived_pipeline_rtd_integration.py
    ATT/tests/test_rtd_option_quotes_repository_contract.py
    ATT/tests/test_structure_leg_rtd_enrichment_service.py

Também foi identificado que o caminho antigo abaixo não representa mais necessariamente o fluxo atual:

    scripts/refresh_rtd_symbol_to_option_quotes.py

---

## Critérios de aceite

| Critério | Status inicial |
|---|---|
| Botão Atualizar Dados localizado | A validar |
| Handler do botão identificado | A validar |
| Pipeline acionado identificado | A validar |
| Resumo de execução identificado ou criado | A validar |
| Contadores de RTD identificados ou criados | A validar |
| Contadores de payoff identificados ou criados | A validar |
| Contadores de decisões identificados ou criados | A validar |
| Mensagem de sucesso detalhada | A validar |
| Execução sem dados novos não mostra sucesso genérico | A validar |
| Erros técnicos são registrados | A validar |
| Usuário recebe mensagem clara em caso de erro | A validar |
| Tela é atualizada após sucesso quando aplicável | A validar |
| Testes são criados ou ajustados | A validar |
| Auditoria é atualizada | A validar |
| Commit final é gerado | A validar |

---

## Plano de execução

1. Localizar o botão Atualizar Dados na interface.
2. Identificar o handler chamado pelo botão.
3. Mapear o fluxo até o pipeline real.
4. Verificar se o pipeline retorna resumo estruturado.
5. Levantar os contadores existentes.
6. Criar ou ajustar resumo de execução, se necessário.
7. Padronizar mensagens em Português Brasil.
8. Diferenciar sucesso com dados, sucesso sem dados novos, sucesso com avisos e erro.
9. Garantir atualização da tela após execução bem-sucedida.
10. Adicionar ou ajustar testes automatizados.
11. Atualizar auditoria.
12. Executar testes.
13. Gerar commit final da Fase 5.

---

## Estado inicial

A Fase 5 está aberta.

A prioridade inicial é diagnosticar o fluxo real do botão Atualizar Dados e confirmar quais pipelines ele aciona.
MD
  else
    echo "Documento da Fase 5 já existe. Mantido sem sobrescrever: $FASE5_DOC"
  fi

  if [ ! -f "$AUDITORIA_DOC" ]; then
    cat > "$AUDITORIA_DOC" <<'MD'
# AUDITORIA — REVISÃO FUNCIONAL PÓS-USO REAL

MD
  fi

  if ! grep -Fq "Registro de Auditoria — Fase 4 — Payoff e Decisões" "$AUDITORIA_DOC"; then
    cat >> "$AUDITORIA_DOC" <<'MD'

---

# Registro de Auditoria — Fase 4 — Payoff e Decisões

## Data

24/06/2026

## Status

Concluída.

---

## Branch

    reinicio-normalizacao-idioma-ptbr

---

## Objetivo auditado

Validar se estruturas criadas manualmente estão corretamente integradas ao fluxo funcional do sistema, especialmente nos pontos de:

- geração de payoff;
- geração de pontos em payoff_curve_points;
- participação no fluxo de decisões;
- geração ou justificativa em structure_decisions;
- rastreabilidade de rejeições ou ausência de dados;
- normalização correta dos pontos de payoff.

---

## Resultado da auditoria

A auditoria da Fase 4 considera a etapa aprovada.

Não foram identificados bloqueios para avanço à Fase 5.

---

## Decisão

A Fase 4 está oficialmente encerrada.

A próxima etapa da rota será:

    Fase 5 — Atualizar Dados e Resumo do Pipeline

---

## Commit documental sugerido

    docs: fecha fase 4 payoff e decisoes
MD
  else
    echo "Auditoria da Fase 4 já registrada."
  fi

  if [ -f "$EVOLUCAO_DOC" ]; then
    if ! grep -Fq "Fase 4 — Payoff e Decisões — Concluída" "$EVOLUCAO_DOC"; then
      cat >> "$EVOLUCAO_DOC" <<'MD'

---

## Fase 4 — Payoff e Decisões — Concluída

A Fase 4 foi encerrada funcional e documentalmente.

Foram validados:

- geração de payoff para estruturas manuais válidas;
- participação no fluxo de decisões;
- gravação ou rastreabilidade de pontos de payoff;
- gravação ou rastreabilidade de decisões;
- correção de normalização de pontos de payoff;
- diagnóstico para identificar estruturas processadas, ignoradas ou rejeitadas.

Evidências finais:

    669 testes aprovados
    2 testes pulados
    Aplicação iniciada sem erro
    Working tree limpa
    Branch sincronizada com origin

Próxima fase:

    Fase 5 — Atualizar Dados e Resumo do Pipeline
MD
    else
      echo "Evolução da Fase 4 já registrada."
    fi
  else
    echo "Aviso: documento de evolução não encontrado: $EVOLUCAO_DOC"
  fi
}

create_verifiers() {
  echo "Criando scripts de verificação da Fase 5..."

  cat > "$BUSCA_SCRIPT" <<'SH2'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

OUT="docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_DIAGNOSTICO_ATUALIZAR_DADOS.md"
mkdir -p "docs/checkpoints"

SCAN_PATHS=()

for path in UI scripts repositories services ATT tests; do
  if [ -e "$path" ]; then
    SCAN_PATHS+=("$path")
  fi
done

if [ "${#SCAN_PATHS[@]}" -eq 0 ]; then
  SCAN_PATHS=(".")
fi

write_section() {
  local title="$1"
  echo ""
  echo "## $title"
  echo ""
}

run_grep() {
  local pattern="$1"

  grep -RInE \
    --exclude-dir=.git \
    --exclude-dir=.venv \
    --exclude-dir=venv \
    --exclude-dir=__pycache__ \
    --exclude-dir=.pytest_cache \
    --exclude-dir=node_modules \
    "$pattern" \
    "${SCAN_PATHS[@]}" 2>/dev/null || true
}

{
  echo "# DIAGNÓSTICO FASE 5 — BOTÃO ATUALIZAR DADOS"
  echo ""
  echo "## Status"
  echo ""
  echo "Diagnóstico gerado automaticamente."
  echo ""
  echo "## Diretórios analisados"
  echo ""
  for path in "${SCAN_PATHS[@]}"; do
    echo "- $path"
  done

  write_section "Candidatos de botão"
  run_grep "Atualizar Dados|atualizar dados|Atualizar|atualizar|Refresh|refresh"

  write_section "Candidatos de handler"
  run_grep "clicked.connect|command=|on_click|callback|handler|handle|atualizar|refresh"

  write_section "Candidatos de pipeline"
  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"

  write_section "Candidatos de resumo e contadores"
  run_grep "summary|resumo|processed|processadas|ignored|ignoradas|created|generated|updated|warnings|avisos|errors|erros|nenhum dado novo|sem dados"

  write_section "Próximos passos"
  echo "- Confirmar qual ocorrência representa o botão real Atualizar Dados."
  echo "- Confirmar o handler chamado pelo clique."
  echo "- Confirmar o pipeline acionado."
  echo "- Confirmar se existe resumo estruturado."
  echo "- Confirmar se há contadores de RTD, payoff e decisões."
  echo "- Confirmar se sucesso sem dados novos é tratado diferente de sucesso com dados."
} > "$OUT"

echo "Relatório gerado: $OUT"
SH2

  cat > "$CONTRATO_SCRIPT" <<'SH2'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

OUT="docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_CONTRATO_RESUMO_PIPELINE.md"
mkdir -p "docs/checkpoints"

FILES=(
  "scripts/run_derived_pipeline.py"
  "scripts/run_rtd_option_quotes_pipeline.py"
  "scripts/run_rtd_refresh_full.py"
  "UI/components/structure_editor_dialog.py"
)

check_term() {
  local label="$1"
  local pattern="$2"
  local found="Não"

  for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
      if grep -InE "$pattern" "$file" >/dev/null 2>&1; then
        found="Sim"
      fi
    fi
  done

  echo "| $label | $found |"
}

write_occurrences() {
  local label="$1"
  local pattern="$2"

  echo ""
  echo "### $label"
  echo ""

  local any="0"

  for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
      local result
      result="$(grep -InE "$pattern" "$file" 2>/dev/null || true)"
      if [ -n "$result" ]; then
        any="1"
        echo "$result"
      fi
    fi
  done

  if [ "$any" = "0" ]; then
    echo "- Nenhuma ocorrência encontrada."
  fi
}

{
  echo "# VERIFICAÇÃO FASE 5 — CONTRATO MÍNIMO DO RESUMO DO PIPELINE"
  echo ""
  echo "## Status"
  echo ""
  echo "Verificação gerada automaticamente."
  echo ""
  echo "## Arquivos analisados"
  echo ""

  for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
      echo "- $file: existe"
    else
      echo "- $file: não encontrado"
    fi
  done

  echo ""
  echo "## Conceitos verificados"
  echo ""
  echo "| Conceito | Encontrado |"
  echo "|---|---|"

  check_term "Estruturas lidas" "structures_read|estruturas_lidas|structures|structure|estrutura"
  check_term "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
  check_term "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
  check_term "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
  check_term "Decisões" "decisions|structure_decisions|decisoes|decisões"
  check_term "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
  check_term "Avisos" "warnings|avisos|warning"
  check_term "Erros" "errors|erros|exception|traceback"
  check_term "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"

  echo ""
  echo "## Ocorrências"

  write_occurrences "Estruturas lidas" "structures_read|estruturas_lidas|structures|structure|estrutura"
  write_occurrences "Estruturas processadas" "structures_processed|estruturas_processadas|processed|processadas"
  write_occurrences "Estruturas ignoradas" "structures_ignored|estruturas_ignoradas|ignored|ignoradas"
  write_occurrences "Pontos de payoff" "payoff_points|payoff_curve_points|pontos_payoff|pontos de payoff"
  write_occurrences "Decisões" "decisions|structure_decisions|decisoes|decisões"
  write_occurrences "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
  write_occurrences "Avisos" "warnings|avisos|warning"
  write_occurrences "Erros" "errors|erros|exception|traceback"
  write_occurrences "Sucesso sem dados novos" "nenhum dado novo|no new data|sem dados|nothing|zero"

  echo ""
  echo "## Leitura esperada"
  echo ""
  echo "A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:"
  echo ""
  echo "- estruturas lidas;"
  echo "- estruturas processadas;"
  echo "- estruturas ignoradas;"
  echo "- pontos de payoff gerados;"
  echo "- decisões geradas;"
  echo "- cotações RTD atualizadas;"
  echo "- avisos;"
  echo "- erros;"
  echo "- execução sem dados novos."
} > "$OUT"

echo "Relatório gerado: $OUT"
SH2

  chmod +x "$BUSCA_SCRIPT" "$CONTRATO_SCRIPT"
}

run_verify() {
  echo "Executando verificações da Fase 5..."
  bash "$BUSCA_SCRIPT"
  bash "$CONTRATO_SCRIPT"

  echo ""
  echo "Verificações concluídas."
  echo "Relatórios:"
  echo "- $RELATORIO_FLUXO"
  echo "- $RELATORIO_CONTRATO"
}

commit_docs() {
  prepare_docs

  git_add_if_exists \
    "$FASE5_DOC" \
    "$AUDITORIA_DOC" \
    "$EVOLUCAO_DOC" \
    "$CHECKPOINT_DIR/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_4_PAYOFF_DECISOES.md"

  commit_if_needed "docs: fecha fase 4 e abre fase 5 atualizar dados"
}

commit_verifiers() {
  create_verifiers
  run_verify

  git_add_if_exists \
    "$BUSCA_SCRIPT" \
    "$CONTRATO_SCRIPT" \
    "$RELATORIO_FLUXO" \
    "$RELATORIO_CONTRATO"

  commit_if_needed "chore: adiciona verificadores fase 5 atualizar dados"
}

show_status() {
  echo ""
  echo "Status atual:"
  git status --short
}

case "${1:-help}" in
  prepare)
    prepare_docs
    create_verifiers
    show_status
    ;;
  verify)
    create_verifiers
    run_verify
    show_status
    ;;
  commit-docs)
    commit_docs
    show_status
    ;;
  commit-verifiers)
    commit_verifiers
    show_status
    ;;
  all)
    prepare_docs
    create_verifiers
    run_verify
    show_status
    ;;
  help|*)
    echo "Uso:"
    echo "  bash scripts/fase5_automacao_gitbash.sh prepare"
    echo "  bash scripts/fase5_automacao_gitbash.sh verify"
    echo "  bash scripts/fase5_automacao_gitbash.sh commit-docs"
    echo "  bash scripts/fase5_automacao_gitbash.sh commit-verifiers"
    echo "  bash scripts/fase5_automacao_gitbash.sh all"
    ;;
esac
