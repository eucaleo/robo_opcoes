# Fase 6.4 — Proteção do contrato de leitura RTD para canonical pricing

## Objetivo

Fortalecer, de forma incremental e testada, o contrato de leitura de preços RTD entre:

- `repositories/rtd_option_quotes_repository.py`
- `services/canonical_pricing_facade.py`

A fase deve preservar o desenho consolidado nas Fases 6.2 e 6.3:

- Excel permanece exclusivamente como gateway RTD;
- `rtd_option_quotes` é a tabela operacional de cotações RTD;
- `RtdOptionQuotesRepository` centraliza a leitura;
- `canonical_pricing_facade` é o consumidor funcional principal;
- bancos locais continuam fora do versionamento;
- nenhuma alteração em UI/API sem decisão explícita.

## Escopo permitido

1. Adicionar ou fortalecer testes automatizados.
2. Documentar contrato esperado de leitura RTD.
3. Ajustar código apenas se algum teste revelar comportamento frágil ou ambíguo.
4. Manter compatibilidade com o pipeline RTD wide já validado.

## Escopo proibido nesta fase

1. Não alterar UI.
2. Não criar nova API.
3. Não alterar formato do CSV wide.
4. Não versionar banco SQLite local.
5. Não remover scripts legados.
6. Não refatorar fluxo amplo de precificação fora do contrato RTD.

## Pontos de contrato a proteger

1. Leitura por `codigo_opcao`.
2. Tratamento de tabela ausente.
3. Tratamento de registro ausente.
4. Escolha entre `bid`, `ask`, `ultimo_preco` e campos disponíveis.
5. Precedência entre:
   - preço manual explícito;
   - preço RTD;
   - preço original do snapshot.
6. Persistência/rastreamento da origem de preço quando aplicável.

## Baseline de testes requerido

Antes de alteração funcional, executar:

- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`
- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py`
- `python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py`
- `python -m pytest ATT/tests/test_pricing_execution_price_source_persistence.py`
- `python -m pytest ATT/tests -k "rtd_option_quotes"`

## Critério de fechamento

A Fase 6.4 poderá ser encerrada quando houver:

1. baseline de testes registrado;
2. lacunas reais de contrato identificadas;
3. testes novos ou reforçados, se necessário;
4. eventuais correções pequenas documentadas;
5. decisão explícita sobre seguir para integração funcional seguinte ou manter congelamento.

---

## Baseline executado

Data de execução: 2026-06-18.

Comandos executados:

- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`
- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py`
- `python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py`
- `python -m pytest ATT/tests/test_pricing_execution_price_source_persistence.py`
- `python -m pytest ATT/tests -k "rtd_option_quotes"`

Evidências registradas em:

- `docs/checkpoints/evidencias/fase-6-4-pytest-rtd-db-path.txt`
- `docs/checkpoints/evidencias/fase-6-4-pytest-rtd-price-resolution.txt`
- `docs/checkpoints/evidencias/fase-6-4-pytest-rtd-execute-pricing-integration.txt`
- `docs/checkpoints/evidencias/fase-6-4-pytest-price-source-persistence.txt`
- `docs/checkpoints/evidencias/fase-6-4-pytest-rtd-option-quotes.txt`
- `docs/checkpoints/evidencias/fase-6-4-git-status-inicial.txt`

## Resultado do baseline

Todos os testes executados passaram.

Resultados observados:

- `6 passed in 1.57s`
- `21 passed in 1.09s`
- `1 passed in 1.08s`
- `5 passed in 0.24s`
- `19 passed, 630 deselected in 2.87s`

## Decisão após baseline

O contrato RTD/canonical pricing possui baseline verde antes de qualquer alteração funcional.

Nenhuma alteração produtiva deve ser feita ainda.

Próxima atividade da Fase 6.4:

1. inventariar os testes existentes de contrato RTD;
2. identificar lacunas reais;
3. decidir se a fase exige apenas documentação/testes adicionais ou pequena correção de contrato.


---

## Branch de trabalho

A Fase 6.4 passou a ser conduzida em branch própria para evitar ambiguidade operacional com o fechamento da Fase 6.3.

Branch:

- `fase-6-4-contrato-rtd-canonical-pricing`

Base de criação:

- `efbb778 docs: fecha fase 6.3 mapa impacto RTD`

Racional:

- manter a branch `fase-12-fechamento-ciclo` como linha documental fechada até a Fase 6.3;
- isolar a proteção do contrato RTD/canonical pricing;
- reduzir risco de interpretação equivocada entre fases.


---

## Inventário inicial de cobertura

Foi executado inventário dos testes relacionados ao contrato RTD/canonical pricing.

Evidência:

- `docs/checkpoints/evidencias/fase-6-4-inventario-testes-contrato-rtd.md`

Resultado observado:

- há cobertura explícita para escolha de preço RTD;
- há cobertura para precedência de preço manual;
- há cobertura para fallback para snapshot;
- há cobertura para quote ausente;
- há cobertura para erro no repository;
- há cobertura para preço RTD inválido;
- há cobertura para divergência de ativo-base;
- há cobertura para quote vencida;
- há cobertura para rastreabilidade RTD no payload;
- há cobertura para persistência de `price_source` e metadados RTD.

Decisão provisória:

- a Fase 6.4 parece já possuir cobertura relevante;
- antes de alterar código produtivo, deve-se verificar se existe lacuna específica no contrato público do `RtdOptionQuotesRepository`.
