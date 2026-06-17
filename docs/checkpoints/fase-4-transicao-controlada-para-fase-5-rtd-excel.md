# Fase 4 — Transição controlada para Fase 5 RTD/Excel

## Contexto

Esta evidência registra a transição controlada da reconciliação de caminhos de banco e schema para a etapa de reconciliação RTD/Excel, conforme a ROTA_MESTRE_3.

## Branch

fase-12-fechamento-ciclo

## Commit técnico validado

d56ec27 fix: isola resolucao do banco rtd option quotes

## Alteração validada

A função _resolve_rtd_option_quotes_db_path, em services/canonical_pricing_facade.py, foi ajustada para resolver o banco de rtd_option_quotes sem depender de caminho absoluto global de app.db.

A prioridade validada passou a ser:

1. banco primário, se possuir rtd_option_quotes;
2. app.db no mesmo diretório do banco primário;
3. dados/app.db relativo ao diretório corrente;
4. fallback conservador para o banco primário.

## Evidências de validação

Foram executadas validações sintáticas e testes focados.

### Compilação

Comando:

python -m py_compile services/canonical_pricing_facade.py

Resultado:

sem erro.

### Teste isolado

Comando:

python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_db_path.py

Resultado:

6 passed.

### Bateria focada RTD option quotes

Comando:

python -m pytest ATT/tests/test_audit_rtd_option_quotes.py ATT/tests/test_canonical_pricing_facade_rtd_db_path.py ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_import_rtd_links_to_option_quotes.py ATT/tests/test_pricing_execution_price_source_persistence.py ATT/tests/test_run_rtd_option_quotes_pipeline.py ATT/tests/test_fase_11_rtd_integrated_flow.py

Resultado:

54 passed.

Arquivo de evidência:

docs/checkpoints/evidencias/fase-6-testes-focados-rtd-option-quotes.txt

## Restrições preservadas

Nesta transição:

- não houve criação de tabela;
- não houve versionamento de banco local;
- não houve limpeza destrutiva;
- não houve alteração em UI;
- não houve alteração em API;
- não houve alteração em repository;
- não houve mudança no papel do Excel como gateway RTD.

## Decisão

A reconciliação incremental de caminhos de banco relacionada a rtd_option_quotes está validada e publicada no remoto.

A próxima etapa autorizada é iniciar a Fase 5 — Reconciliação RTD/Excel, inicialmente em modo somente leitura.

## Próximo escopo autorizado

A Fase 5 deve iniciar por inventário da ponte RTD oficial:

LISTA_RTD.xlsm

O inventário deve registrar:

- localização do arquivo;
- hash;
- tamanho;
- abas declaradas;
- presença ou ausência de macros;
- presença de fórmulas ou referências RTD;
- arquivos internos relevantes do workbook.

Nenhuma alteração funcional no Excel, em banco, UI, API, repository ou serviço está autorizada sem checkpoint posterior.
