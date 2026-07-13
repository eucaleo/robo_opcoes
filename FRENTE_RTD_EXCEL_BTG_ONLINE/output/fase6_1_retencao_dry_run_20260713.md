# Fase 6.1 - Dry-run de retenção, limpeza e consolidação

Marcador inicio: INICIO_FASE6_1_RETENCAO_DRY_RUN_20260713

Data de geração: 2026-07-13T13:53:27+00:00

## Natureza

Simulação operacional não destrutiva.

Este dry-run abre o banco SQLite em modo somente leitura.

## Banco

- Caminho: `dados\app.db`
- Existe: sim
- Tamanho em bytes: 1548288

## Guardrails

- Nenhum `DELETE` foi executado.
- Nenhum `UPDATE` foi executado.
- Nenhum `INSERT` foi executado.
- Nenhum `DROP` foi executado.
- Nenhum `ALTER` foi executado.
- Nenhum `VACUUM` foi executado.
- Nenhuma compactação foi executada.
- Nenhum dado foi removido.

## Resultado por tabela

| Tabela | Existe | Linhas | Coluna temporal | Corte simulado | Elegíveis simulados | Regra | Ação destrutiva |
|---|---:|---:|---|---|---:|---|---|
| rtd_option_quotes | sim | 10 |  |  | 0 | snapshot operacional atual: preservar integralmente | nenhuma |
| rtd_option_quotes_intraday_history | sim | 60 | captured_at | 2026-06-13T13:53:27+00:00 | 0 | histórico intraday bruto: candidato futuro apenas após validação de cobertura por candles; janela simulada: 30 dias | nenhuma |
| rtd_option_quotes_intraday_candles | sim | 110 |  |  | 0 | candles consolidados: preservar integralmente nesta etapa | nenhuma |
| rtd_underlying_quotes | sim | 2 | created_at | 2026-06-13T13:53:27+00:00 | 0 | cotações de ativo base: candidato futuro somente via política explícita; janela simulada: 30 dias | nenhuma |
| structure_snapshots | sim | 61 | created_at | 2026-04-14T13:53:27+00:00 | 0 | snapshots estruturais: candidato futuro com retenção mínima de auditoria; janela simulada: 90 dias | nenhuma |
| system_snapshots | não |  |  |  |  | tabela ausente | nenhuma |

## Total simulado

- Linhas potencialmente elegíveis em simulação: 0
- Linhas efetivamente removidas: 0

## Decisão

A Fase 6.1 define contrato e simulação.

A execução destrutiva permanece bloqueada até aprovação explícita em fase posterior.

Marcador fim: FIM_FASE6_1_RETENCAO_DRY_RUN_20260713
