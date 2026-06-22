#!/usr/bin/env bash
set -euo pipefail

PHASE_FILE="docs/checkpoints/FASE_6_VALIDACAO_INTEGRADA_FINAL.md"

mkdir -p docs/checkpoints

echo "[INFO] Criando checkpoint inicial da Fase 6 em: ${PHASE_FILE}"

cat > "${PHASE_FILE}" <<'MARKDOWN'
# Fase 6 - Validacao integrada final

## Objetivo

Executar a validacao integrada final da cadeia operacional do Sistema de Derivados - Analise de Decisoes.

Esta fase consolida as validacoes anteriores e confirma que o sistema esta pronto para uso controlado com:

- ingestao RTD;
- persistencia em derived.db;
- pipeline operacional;
- calculo de decisoes;
- persistencia de payoff;
- exibicao pela UI;
- resumo operacional;
- testes automatizados;
- consistencia de snapshots.

## Escopo

A Fase 6 cobre a validacao ponta a ponta dos seguintes componentes:

- Banco derivado dados/derived.db
- Importacao de cotacoes RTD
- Auditoria da tabela rtd_option_quotes
- Pipeline derived
- Estruturas manuais
- Decisoes persistidas
- Curvas de payoff
- Interface grafica
- Resumo operacional exibido ao usuario
- Suite automatizada de testes
- Compilacao dos modulos principais

## Pre-condicoes validadas

| Fase | Status | Evidencia |
|---|---|---|
| Fase 3F | Validada | Diagnostico de payoff |
| Fase 4 | Validada | Feedback operacional do pipeline |
| Fase 5F | Validada | UI do resumo operacional do pipeline |

## Estado inicial observado

A Fase 5F foi encerrada com sucesso.

Resumo operacional validado na UI:

    Pipeline executado com sucesso.

    Resumo operacional:
    - Estruturas: n/d
    - Decisoes: 2
    - Pontos de payoff: 202
    - Resumos de payoff: n/d
    - Execucoes de pricing: n/d
    - Cotacoes RTD atualizadas: 4
    - Avisos: 0
    - Erros: 0

## Checklist da Fase 6

### 1. Validacao de ambiente

- Confirmar branch ativa
- Confirmar estado limpo do Git
- Confirmar existencia de dados/derived.db
- Confirmar existencia dos scripts de pipeline
- Confirmar disponibilidade dos testes automatizados

### 2. Validacao automatizada

Comandos previstos:

    python -m pytest ATT/tests -q

    python -m compileall repositories services domain ATT/tests

Criterios de aceite:

- Suite de testes sem falhas
- Modulos principais compilando sem erro
- Nenhuma regressao em payoff
- Nenhuma regressao em RTD
- Nenhuma regressao em pipeline
- Nenhuma regressao em UI

### 3. Validacao do pipeline

Criterios de aceite:

- Pipeline executa com sucesso
- Importacao RTD retorna sem erros
- Auditoria de RTD retorna status ok
- Snapshots finais permanecem consistentes
- Resumo operacional apresenta decisoes
- Resumo operacional apresenta pontos de payoff
- Resumo operacional apresenta cotacoes RTD atualizadas
- Avisos igual a zero ou justificados
- Erros igual a zero

### 4. Validacao da UI

Criterios de aceite:

- UI abre sem erro
- Execucao pela UI permanece funcional
- Mensagem final de sucesso e exibida
- Resumo operacional e exibido ao usuario
- Decisoes aparecem na grade
- Curva de payoff permanece visivel
- Usuario consegue interpretar o resultado sem consultar terminal

### 5. Validacao de integridade

Criterios de aceite:

- derived.db permanece consistente
- Tabelas principais possuem dados esperados
- payoff_curve_points possui pontos persistidos
- structure_decisions possui decisoes persistidas
- rtd_option_quotes possui cotacoes atualizadas
- Nao ha acionamento indevido de Excel
- Nao ha acionamento de PowerShell pela UI

## Evidencias a preencher no encerramento

### Git

    A preencher durante o fechamento da Fase 6.

### Testes

    A preencher durante o fechamento da Fase 6.

### Compileall

    A preencher durante o fechamento da Fase 6.

### Pipeline

    A preencher durante o fechamento da Fase 6.

### UI

    A preencher durante o fechamento da Fase 6.

## Criterio de conclusao

A Fase 6 sera considerada concluida quando:

- os testes automatizados passarem;
- a compilacao passar;
- o pipeline executar sem erros;
- a UI exibir o resumo operacional corretamente;
- as decisoes e a curva de payoff permanecerem visiveis;
- o banco derived.db permanecer consistente;
- o Git estiver limpo apos o commit final da fase.

## Status

Aberta para validacao integrada final.
MARKDOWN

echo "[OK] Checkpoint inicial criado: ${PHASE_FILE}"
