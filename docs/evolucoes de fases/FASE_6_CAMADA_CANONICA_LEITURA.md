# Fase 6 - Camada Canônica de Leitura

## Objetivo

Criar ou consolidar uma camada canônica de leitura para esconder tabelas físicas `rtd_*` e `manual_*` atrás de repositórios, interfaces ou serviços estáveis.

Esta fase preserva o comportamento atual e não altera regra de negócio.

## Base de referência

Documentos anteriores:

- `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md`
- `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md`

Branch esperada:

- `limpeza-tests-scripts-checks`

## Diagnóstico herdado da Fase 5

A Fase 5 definiu que:

- Excel direto é adaptador legado.
- Bridge CSV é adaptador legado operacional ativo.
- Tabelas `rtd_*` são staging operacional.
- Tabelas `manual_*` representam dados mantidos/editados pela aplicação.
- Domínio e serviços devem evitar dependência direta de arquivos, bridge, CSV, Excel ou COM.

## 1. Problema arquitetural atual

Ainda existem referências físicas a tabelas `rtd_*` e `manual_*` fora de uma fronteira canônica clara.

A Fase 6 não remove essas referências de imediato. O objetivo é classificar onde elas são aceitáveis e onde devem ser reduzidas progressivamente.

## 2. Auditoria executada

Foram executados comandos `git grep` para mapear referências a:

- `rtd_analise*`
- `rtd_consolidacoes`
- `rtd_rolls*`
- `rtd_hist*`
- `rtd_encerramentos*`
- `manual_analise*`
- demais ocorrências amplas de `rtd_*`

A auditoria foi feita excluindo progressivamente:

- `docs/**`
- `ATT/tests/**`
- `bridge_ingest_csv.py`

## 3. Resultado da auditoria

### 3.1 Adaptador bridge

Arquivo identificado:

- `bridge_ingest_csv.py`

Tabelas staging populadas pelo bridge:

- `rtd_analise_raiox`
- `rtd_consolidacoes`
- `rtd_analise_robo`
- `rtd_analise_robo_legs`
- `rtd_rolls_detectados`
- `rtd_hist_robo`
- `rtd_encerramentos_manuais`

Classificação:

- Referência aceitável.
- O arquivo é o adaptador legado operacional responsável por popular staging `rtd_*`.

## 3.2 Repositórios

Arquivos identificados:

- `repositories/market_snapshot_repository.py`
- `repositories/robo_legs_repository.py`
- `repositories/robo_legs_status_repository.py`
- `repositories/rtd_option_quotes_repository.py`

Tabelas físicas observadas:

- `rtd_analise_robo`
- `rtd_analise_robo_legs`
- `manual_analise_robo_legs`
- `rtd_option_quotes`

Classificação:

- Referência aceitável nesta fase.
- Repositórios são a fronteira adequada para conhecer tabelas físicas.
- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.

Regra de precedência observada:

- `manual_analise_robo_legs > rtd_analise_robo_legs`

Essa regra deve ser preservada.

## 3.3 Testes

Arquivos identificados:

- `ATT/tests/test_robo_legs_repository.py`
- `ATT/tests/test_robo_legs_status_repository.py`

Classificação:

- Referência aceitável.
- Os testes criam tabelas físicas para validar comportamento atual dos repositórios.

## 3.4 UI

Arquivo identificado:

- `UI/models/ui_data.py`

Ocorrências observadas:

- `rtd_consolidacoes`
- `rtd_consolidations`
- `rtd_decisions`
- `rtd_payoff_points`
- `rtd_payoff_curva`

Classificação:

- Referência a reduzir.
- A UI ainda conhece nomes físicos ou derivados com prefixo `rtd_*`.
- Idealmente deve consumir serviço ou repositório canônico.

## 3.5 Domínio

Arquivo identificado:

- `domain/market_snapshot.py`

Ocorrência observada:

- `rtd_analise_robo`

Classificação:

- Referência textual/documental a reduzir.
- Mesmo quando não há dependência executável direta, o domínio ainda carrega vocabulário físico de staging.

## 3.6 Serviços

Arquivos identificados:

- `services/canonical_pricing_facade.py`
- `services/market_snapshot_selector.py`
- `services/robo_legs_status_service.py`

Classificação:

- Referência parcialmente aceitável, mas deve ser observada.

Detalhes:

- `services/canonical_pricing_facade.py` possui exemplos/documentação citando `rtd_analise_robo`.
- `services/market_snapshot_selector.py` usa nomes como `get_rtd_legs` e `rtd_by_ativo`, refletindo origem do dado.
- `services/robo_legs_status_service.py` usa nomes como `rtd_latest`, refletindo status da origem RTD.

Decisão preliminar:

- Não alterar agora.
- Na refatoração futura, avaliar troca de nomes para termos canônicos como `external`, `market`, `staged` ou `provider`.

## 4. Fronteira canônica proposta

Referências aceitáveis nesta fase:

- `bridge_ingest_csv.py`
- `repositories/*`
- `ATT/tests/*`

Referências a reduzir progressivamente:

- `UI/*`
- `domain/*`
- `services/*`

Motivo:

- `bridge_ingest_csv.py` é adaptador de ingestão.
- `repositories/*` encapsulam persistência.
- `ATT/tests/*` validam comportamento atual.
- UI, domínio e serviços devem depender de conceitos canônicos, não de nomes físicos de staging.

## 5. Estratégia técnica segura

### Etapa 1 - Preservar repositórios atuais

Os repositórios existentes formam a primeira camada canônica prática:

- `repositories/market_snapshot_repository.py`
- `repositories/robo_legs_repository.py`
- `repositories/robo_legs_status_repository.py`
- `repositories/rtd_option_quotes_repository.py`

### Etapa 2 - Evitar mudança de schema

Nesta fase não deve haver:

- renomeação de tabelas;
- migração de banco;
- remoção de tabelas `rtd_*`;
- remoção de tabelas `manual_*`.

### Etapa 3 - Reduzir vazamento progressivamente

Candidatos futuros:

- `UI/models/ui_data.py`
- `domain/market_snapshot.py`
- `services/canonical_pricing_facade.py`
- `services/market_snapshot_selector.py`
- `services/robo_legs_status_service.py`

### Etapa 4 - Preservar comportamento com testes

Testes executados com sucesso:

- `pytest ATT/tests/test_robo_legs_repository.py ATT/tests/test_robo_legs_status_repository.py`
- Resultado: `8 passed`

Suíte completa executada com sucesso:

- `pytest`
- Resultado: `445 passed, 2 skipped`

## 6. Critério de saída da Fase 6

A Fase 6 é considerada concluída com a definição objetiva de:

- quais referências físicas `rtd_*` e `manual_*` são aceitáveis;
- quais referências devem ser reduzidas;
- quais repositórios formam a primeira camada canônica;
- qual regra de precedência deve ser preservada;
- quais pontos serão candidatos à refatoração incremental na próxima fase.

## 7. Decisão final da Fase 6

Decisão:

- A camada canônica inicial será formada pelos repositórios existentes.
- O acesso direto a `rtd_*` e `manual_*` é aceitável nos repositórios e no adaptador bridge.
- O acesso direto ou vocabulário físico em UI, domínio e serviços deve ser reduzido progressivamente.
- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.
- A regra `manual_analise_robo_legs > rtd_analise_robo_legs` deve ser preservada.

## 8. Próxima fase recomendada

Fase 7 - Refatoração incremental dos vazamentos de `rtd_*` e `manual_*` fora da camada de repositórios/adaptadores.
