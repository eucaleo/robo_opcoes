# Fase 6.1 - Contrato de retenção com dry-run obrigatório

Marcador inicio: INICIO_AUDITORIA_FASE6_1_CONTRATO_RETENCAO_DRY_RUN_20260713

Data: 13/07/2026

## Natureza

Contrato operacional e técnico para a Fase 6.1 da frente RTD Excel BTG Online.

Esta fase define regras, guardrails e simulação de retenção, limpeza e consolidação sem executar ação destrutiva.

## Objetivo

Estabelecer uma política inicial de retenção e simulação obrigatória antes de qualquer limpeza real no banco SQLite operacional.

## Guardrails obrigatórios

- Proibido executar `DELETE`.
- Proibido executar `UPDATE`.
- Proibido executar `DROP`.
- Proibido executar `ALTER`.
- Proibido executar `VACUUM`.
- Proibido compactar banco.
- Proibido remover registros.
- Proibido alterar schema.
- Banco deve ser aberto em modo somente leitura durante o dry-run.
- Qualquer execução destrutiva deve ficar bloqueada até fase posterior explicitamente aprovada.

## Escopo de tabelas avaliadas

- `rtd_option_quotes`
- `rtd_option_quotes_intraday_history`
- `rtd_option_quotes_intraday_candles`
- `rtd_underlying_quotes`
- `structure_snapshots`
- `system_snapshots`

## Política inicial

### `rtd_option_quotes`

Tabela de snapshot operacional atual.

Decisão da Fase 6.1:

- preservar integralmente;
- não considerar para limpeza;
- não remover linhas.

### `rtd_option_quotes_intraday_candles`

Tabela de candles consolidados.

Decisão da Fase 6.1:

- preservar integralmente;
- não considerar para limpeza nesta etapa;
- usar como base futura de validação de cobertura do histórico bruto.

### `rtd_option_quotes_intraday_history`

Tabela de histórico intraday bruto.

Decisão da Fase 6.1:

- simular elegibilidade futura acima de 30 dias;
- não apagar nada;
- não permitir limpeza real enquanto não houver validação de cobertura por candles;
- manter caminho conservador.

### `rtd_underlying_quotes`

Tabela de cotações do ativo base.

Decisão da Fase 6.1:

- simular janela futura de 30 dias se houver coluna temporal;
- não apagar nada;
- exigir política específica antes de qualquer limpeza real.

### `structure_snapshots`

Tabela de snapshots estruturais.

Decisão da Fase 6.1:

- simular janela futura de 90 dias se houver coluna temporal;
- não apagar nada;
- preservar rastreabilidade operacional.

### `system_snapshots`

Tabela de snapshots sistêmicos.

Decisão da Fase 6.1:

- simular janela futura de 90 dias se houver coluna temporal;
- não apagar nada;
- preservar rastreabilidade operacional.

## Critério de aceite

A Fase 6.1 só é considerada válida se:

- o dry-run for executado sem erro;
- o relatório de simulação for gerado;
- os testes direcionados forem executados;
- nenhum dado for removido;
- nenhum schema for alterado;
- o commit registrar explicitamente o caráter não destrutivo.

## Resultado esperado

Ao final da Fase 6.1, o projeto deve ter:

- contrato de retenção documentado;
- script de dry-run read-only;
- relatório de simulação;
- evidência de testes;
- nenhum efeito destrutivo no banco.

Marcador fim: FIM_AUDITORIA_FASE6_1_CONTRATO_RETENCAO_DRY_RUN_20260713
