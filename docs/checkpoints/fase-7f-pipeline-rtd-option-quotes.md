# Checkpoint — Fase 7F — Pipeline RTD option quotes

## Contexto

Esta fase adiciona um pipeline operacional único para executar o fluxo de cotações RTD de opções.

Fluxo implementado:

- dados/RTD_LINKS.csv
- importação para rtd_option_quotes
- auditoria da tabela rtd_option_quotes

## Arquivos adicionados

- scripts/run_rtd_option_quotes_pipeline.py
- ATT/tests/test_run_rtd_option_quotes_pipeline.py

## Funcionalidades implementadas

O pipeline executa:

1. Importador RTD:
   - scripts/import_rtd_links_to_option_quotes.py

2. Auditoria RTD:
   - scripts/audit_rtd_option_quotes.py

## Argumentos disponíveis

O pipeline aceita:

- --csv
- --db
- --dry-run
- --max-age-minutes
- --json-audit
- --fail-on-warn

## Comportamento operacional

### Execução normal

Executa importação e depois auditoria.

Quando a auditoria retorna status warn, o pipeline ainda conclui com sucesso, desde que --fail-on-warn não seja usado.

### Dry-run

Quando executado com --dry-run:

- roda apenas o importador;
- não grava alterações;
- não executa auditoria.

### Fail on warn

Quando executado com --fail-on-warn:

- warnings da auditoria passam a gerar retorno operacional de falha.

## Testes executados

Teste específico do pipeline:

- python -m pytest ATT/tests/test_run_rtd_option_quotes_pipeline.py -q

Resultado:

- 9 passed

Teste combinado da fase RTD option quotes:

- python -m pytest ATT/tests/test_import_rtd_links_to_option_quotes.py ATT/tests/test_audit_rtd_option_quotes.py ATT/tests/test_run_rtd_option_quotes_pipeline.py -q

Resultado:

- 21 passed

## Execuções manuais validadas

Help:

- python scripts/run_rtd_option_quotes_pipeline.py --help

Dry-run:

- python scripts/run_rtd_option_quotes_pipeline.py --dry-run

Resultado observado:

- importador executado;
- auditoria não executada;
- nenhuma alteração gravada.

Execução real:

- python scripts/run_rtd_option_quotes_pipeline.py

Resultado observado:

- importador executado;
- auditoria executada;
- auditoria retornou status warn por stale_rows;
- pipeline concluiu com sucesso porque --fail-on-warn não foi usado.

## Observação técnica

Mesmo após o importador indicar registro atualizado, a auditoria ainda reportou:

- stale_rows: 1

Isso sugere que o campo updated_at pode estar sendo preservado antigo ou preenchido a partir da origem, em vez de ser renovado no momento do upsert.

Essa investigação fica recomendada para a próxima fase.

## Commit relacionado

- a2aef25 feat: adiciona pipeline rtd option quotes

## Status

Fase 7F concluída com sucesso.

- Pipeline criado.
- Testes automatizados criados.
- Testes passando.
- Execução dry-run validada.
- Execução real validada.
- Branch sincronizada com o remoto.
