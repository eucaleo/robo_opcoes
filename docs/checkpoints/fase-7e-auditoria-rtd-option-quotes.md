# Checkpoint — Fase 7E — Auditoria da tabela rtd_option_quotes

## Contexto

Esta fase adiciona uma auditoria operacional para a tabela:

- rtd_option_quotes

O objetivo é validar se a tabela de cotações RTD de opções está íntegra, consultável e pronta para alimentar as próximas etapas do robô.

## Arquivos adicionados

- scripts/audit_rtd_option_quotes.py
- ATT/tests/test_audit_rtd_option_quotes.py

## Validações implementadas

O auditor verifica:

- existência do arquivo de banco SQLite;
- existência da tabela rtd_option_quotes;
- presença das colunas obrigatórias;
- quantidade total de registros;
- quantidade de códigos distintos;
- códigos de opção ausentes ou vazios;
- códigos duplicados;
- registros antigos com base em updated_at;
- saída em formato humano;
- saída em JSON;
- exit codes úteis para automação.

## Comandos testados

Teste específico da auditoria:

- python -m pytest ATT/tests/test_audit_rtd_option_quotes.py -q

Resultado:

- 7 passed

Teste combinado com o importador RTD:

- python -m pytest ATT/tests/test_import_rtd_links_to_option_quotes.py ATT/tests/test_audit_rtd_option_quotes.py -q

Resultado:

- 12 passed

## Execução no banco real

Comando:

- python scripts/audit_rtd_option_quotes.py --db dados/app.db

Resultado observado:

- status: warn
- row_count: 1
- distinct_codigo_count: 1
- duplicate_codigo_count: 0
- missing_codigo_count: 0
- stale_rows: 1

Interpretação:

O aviso de stale_rows indica que o registro atual da tabela está antigo em relação ao limite padrão de 30 minutos. Isso não representa erro estrutural; representa apenas uma condição operacional de dado não atualizado recentemente.

## Commit relacionado

- cd1f06b feat: adiciona auditoria da tabela rtd option quotes

## Status

Fase 7E concluída com sucesso.

- Auditor criado.
- Testes automatizados criados.
- Testes passando.
- Auditor validado contra dados/app.db.
- Branch sincronizada com o remoto.
