# AUDITORIA ROTA_MESTRE_2

Arquivo vivo de auditoria da ROTA_MESTRE_2.

Este documento deve ser atualizado ao final de cada fase, registrando comandos executados, testes, resultados, decisões, pendências e commit relacionado.

## Regras de auditoria

Para cada fase encerrada, registrar obrigatoriamente:

- fase
- objetivo
- arquivos auditados
- arquivos alterados
- comandos executados
- testes executados
- resultado
- pendências
- decisão tomada
- commit relacionado

Antes de qualquer alteração funcional, deve existir mapa de impacto contendo:

- arquivos que serão alterados
- arquivos apenas auditados
- risco esperado
- testes que validarão a mudança
- plano de reversão

---

## Fase 0 — Marco de Controle e Congelamento da Rota

### Status

Em preparação para encerramento.

### Data/hora

13/06/2026 18:38 BRT

### Objetivo

Formalizar a ROTA_MESTRE_2 como documento norteador do novo ciclo de desenvolvimento, preservando o encerramento da ROTA_MESTRE_1 e impedindo reabertura indevida de fases anteriores.

### Arquivos auditados

- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
- docs/AUDITORIA_ROTA_MESTRE_2.md

### Arquivos alterados

- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
- docs/AUDITORIA_ROTA_MESTRE_2.md

### Alterações funcionais

Nenhuma.

### Mapa de impacto

#### Arquivos que serão alterados

- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
- docs/AUDITORIA_ROTA_MESTRE_2.md

#### Arquivos apenas auditados

- docs/
- estado do Git

#### Risco esperado

Baixo. Alteração exclusivamente documental.

Não há impacto em:

- UI
- banco de dados
- repositórios
- serviços
- cálculo
- ingestão
- bridge
- scripts operacionais

#### Testes que validarão a mudança

- Conferência de existência dos arquivos documentais.
- Conferência do conteúdo mínimo da ROTA_MESTRE_2.
- Conferência do conteúdo mínimo da auditoria.
- Conferência de diff antes do commit.
- Conferência de status do Git.

#### Plano de reversão

Restaurar os arquivos documentais pelo Git ou remover o arquivo de auditoria caso ainda não esteja versionado.

### Comandos executados

```bash
git status
git branch --show-current
test -f docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
test -f docs/AUDITORIA_ROTA_MESTRE_2.md
grep -n "INICIO ROTA_MESTRE_2" docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
grep -n "Fase 0" docs/AUDITORIA_ROTA_MESTRE_2.md
git diff -- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md docs/AUDITORIA_ROTA_MESTRE_2.md

---

## Fase 1 — Mapeamento automatizado de RTD, Excel, Bridge, Serviços e UI

### Status

Iniciada.

### Objetivo

Executar mapeamento amplo de referências relacionadas a RTD, Excel, bridge, opções, persistência, serviços, cálculo e UI.

### Arquivos alterados

- `scripts/mapear_automacao_opcoes_rtd.py`
- `docs/mapeamento_automacao_opcoes_rtd.md`
- `docs/mapeamento_automacao_opcoes_rtd.json`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Alterações funcionais

Nenhuma.

### Testes executados

```bash
python -m py_compile scripts/mapear_automacao_opcoes_rtd.py
python scripts/mapear_automacao_opcoes_rtd.py
test -f docs/mapeamento_automacao_opcoes_rtd.md
test -f docs/mapeamento_automacao_opcoes_rtd.json
grep -n "Mapeamento automação opções RTD" docs/mapeamento_automacao_opcoes_rtd.md
git status --short

---

## Fase 1 — Encerramento com lista priorizada

### Status

Encerrada.

### Base utilizada

- `docs/mapeamento_automacao_opcoes_rtd.md`
- `docs/mapeamento_automacao_opcoes_rtd.json`
- `docs/lista_priorizada_automacao_opcoes_rtd.md`

### Resultado do mapeamento bruto

O mapeamento automatizado identificou alto volume de candidatos, incluindo documentação, testes e arquivos derivados.

Resumo do relatório bruto:

- Total de achados: 200
- Candidatos fortes: 152
- Candidatos médios: 33
- Candidatos baixos: 15

### Decisão de priorização

Foi criada lista priorizada separando arquivos operacionais de ruído documental/histórico.

Prioridade máxima para as próximas fases:

- `dados/RTD_LINKS.csv`
- `repositories/rtd_option_quotes_repository.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`
- `repositories/market_snapshot_repository.py`
- `services/structure_market_input_assembler.py`
- `services/canonical_input_service.py`

### Alterações funcionais

Nenhuma.

### Arquivos alterados nesta etapa

- `docs/lista_priorizada_automacao_opcoes_rtd.md`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Testes/conferências executados

```bash
sed -n '1,220p' docs/lista_priorizada_automacao_opcoes_rtd.md
git status --short
git diff --stat


---

## Fase 1 — Encerramento com lista priorizada

### Status

Encerrada.

### Base utilizada

- `docs/mapeamento_automacao_opcoes_rtd.md`
- `docs/mapeamento_automacao_opcoes_rtd.json`
- `docs/lista_priorizada_automacao_opcoes_rtd.md`

### Resultado do mapeamento bruto

O mapeamento automatizado identificou alto volume de candidatos, incluindo documentação, testes e arquivos derivados.

Resumo do relatório bruto:

- Total de achados: 200
- Candidatos fortes: 152
- Candidatos médios: 33
- Candidatos baixos: 15

### Decisão de priorização

Foi criada lista priorizada separando arquivos operacionais de ruído documental/histórico.

Prioridade máxima para as próximas fases:

- `dados/RTD_LINKS.csv`
- `repositories/rtd_option_quotes_repository.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`
- `repositories/market_snapshot_repository.py`
- `services/structure_market_input_assembler.py`
- `services/canonical_input_service.py`

### Alterações funcionais

Nenhuma.

### Arquivos alterados nesta etapa

- `docs/lista_priorizada_automacao_opcoes_rtd.md`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Testes/conferências executados

```bash
sed -n '1,220p' docs/lista_priorizada_automacao_opcoes_rtd.md
git status --short
git diff --stat


---

## Fase 2 — Auditoria do contrato RTD/Excel e arquivos de entrada

### Status

Iniciada.

### Objetivo

Auditar o contrato entre RTD, Excel e arquivos locais de entrada, sem alteração funcional.

### Base da fase anterior

- `docs/lista_priorizada_automacao_opcoes_rtd.md`

### Arquivos principais sob auditoria

- `dados/RTD_LINKS.csv`
- `bridge/analise_robo.csv`
- `bridge/analise_robo_legs.csv`
- `bridge/hist_robo.csv`
- `bridge/configuracoes.csv`
- `OPERACOES_E_OPCOES.xlsm`

### Arquivos gerados nesta etapa

- `docs/fase_2_auditoria_contrato_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.json`

### Alterações funcionais

Nenhuma.

### Testes/conferências executados

```bash
sed -n '1,220p' docs/fase_2_diagnostico_csvs_rtd_excel.md
git status --short
git diff --stat

---

## Fase 2 — Encerramento com mapa do contrato RTD/Excel

### Status

Encerrada.

### Base utilizada

- `docs/fase_2_auditoria_contrato_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.json`
- `docs/fase_2_mapa_contrato_rtd_excel.md`

### Achados principais

A Fase 2 identificou dois formatos principais de contrato:

1. Contrato atributo/valor:
   - `dados/RTD_LINKS.csv`

2. Contratos tabulares operacionais/exportados:
   - `bridge/analise_robo_legs.csv`
   - `bridge/analise_robo.csv`
   - `bridge/hist_robo.csv`
   - demais arquivos `bridge/*.csv`

### Arquivos classificados como prioritários

- `dados/RTD_LINKS.csv`
- `bridge/analise_robo_legs.csv`
- `bridge/analise_robo.csv`
- `bridge/hist_robo.csv`

### Achados de compatibilidade

Foram registrados:

- divergência de delimitador em `bridge/encerramentos_manuais.csv`
- sinais de encoding inconsistente em `bridge/configuracoes.csv`
- sinais de encoding inconsistente em `bridge/rolls_detectados.csv`
- diferença de nomes de colunas entre contratos RTD e bridge
- provável dependência indireta do Excel `.xlsm`

### Alterações funcionais

Nenhuma.

### Arquivos alterados nesta etapa

- `docs/fase_2_mapa_contrato_rtd_excel.md`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Testes/conferências executados

```bash
sed -n '1,260p' docs/fase_2_mapa_contrato_rtd_excel.md
git status --short
git diff --stat
```

### Decisão tomada

A Fase 2 está encerrada.

A próxima fase deve auditar a persistência de cotações RTD/opções, com foco em:

- `repositories/rtd_option_quotes_repository.py`
- `repositories/market_snapshot_repository.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`

Nenhuma alteração em UI, banco, schema, cálculo, ingestão, serviços operacionais, CSVs ou Excel operacional foi realizada.


---

## Checkpoint reconciliado — subciclo técnico SQL/timestamp clean

### Contexto

Durante a evolução da branch `ciclo-2-testes-evolucao`, foi executado um subciclo técnico identificado na interação assistida como:

- Fase 5;
- Fase 6A;
- Fase 6B;
- Fase 6C;
- Fase 6D;
- Fase 6E;
- Fase 6F.

Essas fases não foram gravadas com esses rótulos nos assuntos dos commits, mas estão reconciliadas oficialmente no checkpoint:

`docs/checkpoints/ciclo-2-sql-timestamp-clean.md`

### Mapeamento oficial

| Fase técnica | Commit | Descrição |
|---|---|---|
| Fase 5 | `233fe8b` | Ordena snapshots de mercado cronologicamente |
| Fase 6A | `46463fb` | Explicita colunas de execuções de pricing |
| Fase 6B | `3f01728` | Explicita colunas de eventos e snapshots |
| Fase 6C | `5a2fd34` | Normaliza consultas derived legadas com `StructureRef` |
| Fase 6D | `d7291ae` | Ordena leituras derived por timestamp em Python |
| Fase 6E | `0d75092` | Remove `SELECT *` real restante de `robo_legs_repository.py` |
| Fase 6F | `14483c2` | Remove literais SQL inseguros remanescentes em comentários |

### Tag de fechamento

`ciclo-2-sql-timestamp-clean`

### Commit documental posterior

`4283d67 docs: registra checkpoint sql timestamp clean`

### Decisão de rota

A partir deste registro, a continuidade da rota deve considerar como ponto de partida o estado posterior ao checkpoint `ciclo-2-sql-timestamp-clean`.

Não deve ser aberta uma nova frente baseada em fases antigas ou em numeração histórica sem reconciliar previamente com:

- histórico Git;
- checkpoint;
- auditoria da rota;
- testes executados;
- estado atual da branch.

### Status

Checkpoint técnico reconciliado documentalmente.


---

## Fase 8E — Cobertura regressiva da resolução de db path RTD no CanonicalPricingFacade

### Objetivo

Adicionar cobertura automatizada para garantir que o `CanonicalPricingFacade` resolva corretamente o banco efetivo da tabela `rtd_option_quotes`, preservando a separação entre banco principal de execução/cálculo e banco operacional onde residem as cotações RTD de opções.

Esta etapa dá continuidade direta à Fase 8D, que integrou `rtd_option_quotes` ao `CanonicalPricingFacade` e corrigiu a resolução de caminho entre `dados/derived.db` e `dados/app.db`.

### Arquivos auditados

- `services/canonical_pricing_facade.py`
- `repositories/rtd_option_quotes_repository.py`
- `docs/checkpoints/fase-8e-auditoria-testes-rtd-facade.txt`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Arquivos previstos para alteração

- `ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Arquivos apenas auditados

- `services/canonical_pricing_facade.py`
- `repositories/rtd_option_quotes_repository.py`

### Arquivos que não devem ser alterados nesta etapa

- Arquivos de UI
- Arquivos de schema ou migração
- Arquivos em `dados/`
- Arquivos em `bridge/`
- Importadores RTD
- Motor de cálculo

### Mapa de impacto

A alteração prevista é restrita a teste automatizado e documentação.

O teste deve validar:

- existência segura de tabela SQLite via `_sqlite_table_exists`;
- escolha de `dados/app.db` quando o banco primário não possui `rtd_option_quotes` e o `app.db` possui;
- preferência pelo banco primário quando ele já possui `rtd_option_quotes`;
- fallback conservador para o banco primário quando nenhum candidato possui a tabela;
- inicialização do `CanonicalPricingFacade` com `_rtd_option_quotes_db_path` resolvido corretamente.

### Risco esperado

Baixo.

A etapa não altera código funcional, schema, UI, banco operacional ou importadores. O risco principal é o teste depender de detalhes internos do `CanonicalPricingFacade`, mas isso é aceitável nesta fase porque a Fase 8D introduziu comportamento interno relevante para evitar regressão de caminho de banco.

### Testes planejados

- `python -m py_compile services/canonical_pricing_facade.py ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`
- `pytest -q ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`
- `pytest -q`

### Comandos já executados

```bash
git status --short
git log --oneline --decorate -12
git branch --show-current
ls docs
ls docs/checkpoints 2>/dev/null || true
test -f docs/AUDITORIA_ROTA_MESTRE_2.md && echo "AUDITORIA existe" || echo "AUDITORIA ausente"
git log --oneline --decorate --all --grep="fase-8" -20
git log --oneline --decorate --all --grep="8d" -20
git show --name-only --oneline 2b4cb1f
git show --name-only --oneline 3de5680
git show --name-only --oneline 179b936
```

### Resultado dos comandos

- Branch atual: `ciclo-2-testes-evolucao`
- Arquivo obrigatório de auditoria encontrado:
  - `docs/AUDITORIA_ROTA_MESTRE_2.md`
- Working tree continha checkpoint novo ainda não versionado:
  - `docs/checkpoints/fase-8e-auditoria-testes-rtd-facade.txt`
- Histórico Git confirma continuidade direta da Fase 8D.
- Commits recentes relacionados:
  - `2b4cb1f fase-8d: integrar rtd option quotes no canonical pricing facade`
  - `3de5680 fase-8d: resolver db path correto para rtd option quotes`
  - `179b936 docs: registrar resumo final da fase 8d`
- Arquivo funcional alterado na Fase 8D:
  - `services/canonical_pricing_facade.py`
- Arquivos documentais/checkpoints alterados na Fase 8D:
  - `docs/checkpoints/fase-8d-patch-integracao-rtd-option-quotes.diff.txt`
  - `docs/checkpoints/fase-8d-before-rtd-db-path-fix.py`
  - `docs/checkpoints/fase-8d-final-summary.txt`

### Decisão tomada

Prosseguir com a Fase 8E como etapa de cobertura regressiva da Fase 8D.

A próxima alteração permitida é somente:

- criação de teste automatizado;
- atualização documental da auditoria;
- eventual checkpoint documental.

Não está autorizado nesta etapa:

- alterar UI;
- alterar schema;
- alterar banco operacional;
- alterar importadores RTD;
- alterar `bridge/`;
- alterar `dados/`;
- alterar motor de cálculo.

### Plano de reversão

Caso o teste introduzido seja inadequado ou incompatível com a estrutura atual da suíte:

1. Remover `ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`.
2. Reverter a seção da Fase 8E em `docs/AUDITORIA_ROTA_MESTRE_2.md`.
3. Preservar intacto o código funcional já commitado da Fase 8D.
4. Não alterar bancos locais nem arquivos operacionais.

### Pendências

- Criar teste regressivo dedicado.
- Executar teste direcionado.
- Executar suíte completa.
- Registrar resultado final.
- Commitar a Fase 8E.

### Commit relacionado

Pendente.

## Fase 8E - Resultado final

### Arquivo de teste criado

- `ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`

### Validações executadas

```bash
python -m py_compile services/canonical_pricing_facade.py ATT/tests/test_canonical_pricing_facade_rtd_db_path.py
pytest -q ATT/tests/test_canonical_pricing_facade_rtd_db_path.py
pytest -q
```

### Resultado do teste direcionado

```text
6 passed in 1.67s
```

### Resultado da suíte completa

```text
591 passed, 10 skipped in 36.54s
```

### Conclusão

A Fase 8E adiciona cobertura regressiva para a resolução do banco correto de `rtd_option_quotes` no `CanonicalPricingFacade`, sem alterar código funcional, schema, UI, importadores, arquivos em `dados/`, arquivos em `bridge/` ou motor de cálculo.

## Fase 10B — Persistência da rastreabilidade da origem do preço RTD

Data/hora: 15/06/2026 15:09 BRT

### Objetivo

Garantir que a origem efetiva do preço de opção usado no cálculo seja preservada também na persistência da execução de pricing.

### Arquivos alterados

- ATT/tests/test_pricing_execution_price_source_persistence.py

### Arquivos auditados

- repositories/pricing_executions_repository.py
- services/pricing_execution_persistence_service.py
- services/canonical_pricing_facade.py

### Comandos executados

```bash
git diff --name-status fase-10a-rastreabilidade-preco-rtd...HEAD
git show --name-status --stat --oneline d3a9dcc
python -m pytest ATT/tests/test_pricing_execution_price_source_persistence.py -v
python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v

```

### Resultados

```text
git diff --name-status fase-10a-rastreabilidade-preco-rtd...HEAD
A       ATT/tests/test_pricing_execution_price_source_persistence.py
```

```text
python -m pytest ATT/tests/test_pricing_execution_price_source_persistence.py -v
3 passed in 0.27s
```

```text
python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v
4 passed in 1.52s
```

### Decisão tomada

A Fase 10B foi validada como alteração isolada sobre a Fase 10A.

A rastreabilidade da origem do preço RTD agora está coberta também na camada de persistência de execuções de pricing.

### Pendências

- Abrir PR empilhado contra `fase-10a-rastreabilidade-preco-rtd`.
- Prosseguir para a Fase 10C em branch empilhada sobre esta fase.

### Commits relacionados

```text
d3a9dcc test: preserve option price source in pricing execution persistence
8eb79f8 docs: registra fechamento fase 10b rastreabilidade preco rtd
```

## Fase 10C — Validação da execução com preço RTD rastreável

### Objetivo

Validar que o preço efetivo oriundo de `rtd_option_quotes` é aplicado ao payload canônico de pricing e que os metadados de rastreabilidade da cotação RTD permanecem disponíveis na execução.

### Alterações realizadas

- `_resolve_effective_leg_price` passou a preservar metadados de rastreabilidade da cotação RTD.
- Legs com preço resolvido por `rtd_option_quotes` passaram a carregar rastreabilidade da origem do preço.
- O payload canônico de pricing passou a refletir o preço RTD efetivo e sua origem.
- Testes unitários e de integração foram atualizados para validar o contrato.

### Arquivos alterados

~~~text
M       ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py
M       ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py
M       services/canonical_pricing_facade.py
~~~

### Testes executados

~~~text
python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py -v
12 passed in 1.32s
~~~

~~~text
python -m pytest ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py -v
1 passed in 1.24s
~~~

~~~text
python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v
16 passed in 1.44s
~~~

### Decisão tomada

A Fase 10C foi validada como branch empilhada sobre a Fase 10B.

A execução de pricing agora preserva a rastreabilidade da cotação RTD usada para resolver o preço efetivo da leg.

### Commits relacionados

~~~text
7800e70 feat: preserve rtd option quote traceability in pricing payload
b16c6c2 docs: registra fechamento fase 10c rastreabilidade preco rtd
~~~

### Pendências

- Abrir PR empilhado contra `fase-10b-rastreabilidade-preco-rtd-persistencia`.
- Prosseguir para a Fase 10D a partir de `fase-10d-endurecimento-rastreabilidade-preco-rtd`.

## Fase 10D — Endurecimento da rastreabilidade do preço RTD

Data/hora: 15/06/2026 16:16 BRT

### Objetivo

Endurecer a rastreabilidade do preço efetivo de opção resolvido a partir de `rtd_option_quotes`, garantindo que o payload canônico de pricing informe não apenas que o preço veio do RTD, mas também qual campo da cotação foi usado e qual registro RTD originou o preço.

### Contexto operacional

Nesta fase, o RTD foi ativado com Excel como ponte operacional, alimentando os arquivos de banco de dados em tempo real. A validação técnica desta fase focou em transformar essa disponibilidade operacional em contrato auditável no backend.

### Alterações realizadas

- Criada a função `_pick_rtd_option_price_with_trace`, que retorna o preço RTD efetivo e o campo/critério usado.
- Mantida compatibilidade da função `_pick_rtd_option_price`, preservando a API anterior que retorna apenas o preço.
- `_resolve_effective_leg_price` passou a expor metadados adicionais de rastreabilidade quando a origem efetiva do preço é `rtd_option_quotes`.
- O payload canônico passou a carregar os campos adicionais de rastreabilidade RTD nas legs.
- Foram adicionados testes regressivos para:
  - preservar preço manual explícito sem consultar RTD;
  - usar RTD quando a leg não é manual;
  - registrar campo usado da cotação RTD;
  - registrar código da opção e ativo-base da cotação RTD;
  - cair para snapshot quando a cotação RTD existe, mas não possui preço utilizável;
  - impedir vazamento de metadados RTD em legs manuais.

### Campos de rastreabilidade RTD consolidados

Quando `price_source` é `rtd_option_quotes`, a leg pode carregar:

~~~text
price_source = rtd_option_quotes
rtd_price_field = ultimo_preco | price | last_price | bid_ask_mid | bid | ask
rtd_quote_codigo_opcao = código da opção cotada
rtd_quote_ativo_base = ativo base da opção
rtd_price_source = source da cotação RTD
rtd_price_updated_at = timestamp de atualização da cotação
rtd_price_created_at = timestamp de criação da cotação
~~~

### Arquivos alterados

~~~text
M       ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py
M       ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py
M       services/canonical_pricing_facade.py
~~~

### Testes executados

~~~bash
python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v
~~~

Resultado:

~~~text
19 passed in 1.56s
~~~

### Evidências principais

- O preço original do snapshot controlado era `5.55`.
- A cotação persistida em `rtd_option_quotes.ultimo_preco` era `9.99`.
- O payload canônico executado pelo pricing passou a usar `9.99`.
- A leg manteve `price_source = rtd_option_quotes`.
- A leg passou a informar `rtd_price_field = ultimo_preco`.
- A leg passou a informar `rtd_quote_codigo_opcao = ABCD11`.
- A leg passou a informar `rtd_quote_ativo_base = ABCD`.
- A persistência recebeu o payload com os mesmos metadados de rastreabilidade.
- Legs manuais preservaram `price_source = manual` e não receberam metadados RTD.

### Decisão tomada

A Fase 10D foi validada como endurecimento incremental sobre a Fase 10C.

A resolução de preço RTD agora é auditável em nível de campo utilizado e registro de cotação, reduzindo ambiguidade entre preço manual, preço de snapshot e preço vindo de `rtd_option_quotes`.

### Commits relacionados

~~~text
ee927c5 feat: harden rtd option quote price traceability
57daefa docs: registra fechamento fase 10d rastreabilidade preco rtd
~~~

### Pendências

- Abrir PR empilhado da branch `fase-10d-endurecimento-rastreabilidade-preco-rtd`.
- Validar em ambiente operacional real com RTD/Excel ativo que legs reais carregam os campos:
  - `price_source`;
  - `rtd_price_field`;
  - `rtd_quote_codigo_opcao`;
  - `rtd_quote_ativo_base`;
  - `rtd_price_updated_at`.


## Fase 10E — Validação operacional da rastreabilidade RTD persistida

Data/hora: 15/06/2026 20:47 BRT

### Objetivo

Validar que a rastreabilidade completa do preço RTD, já consolidada na Fase 10D no payload canônico de pricing, também é preservada nas camadas de persistência, consulta e snapshot do sistema.

Esta fase garante que os metadados RTD não se perdem após a execução de pricing ser salva e posteriormente recuperada.

### Contexto operacional

A Fase 10D consolidou a exposição dos campos de rastreabilidade RTD no payload de pricing.

A Fase 10E adiciona cobertura regressiva sobre a persistência dessa rastreabilidade, validando que os campos permanecem disponíveis em:

- `PricingExecutionsRepository.get_execution`;
- `PricingExecutionsRepository.list_executions`;
- `PricingExecutionPersistenceService`;
- `SystemSnapshotsRepository`;
- `operation_state_json`.

### Arquivos alterados

~~~text
M       ATT/tests/test_pricing_execution_price_source_persistence.py
~~~

### Arquivos auditados

~~~text
repositories/pricing_executions_repository.py
services/pricing_execution_persistence_service.py
services/canonical_pricing_facade.py
repositories/market_snapshot_repository.py
~~~

### Alterações realizadas

Foram adicionados testes regressivos para validar que uma leg com preço vindo de `rtd_option_quotes` preserva os seguintes campos após persistência e recuperação:

~~~text
price_source
rtd_price_field
rtd_quote_codigo_opcao
rtd_quote_ativo_base
rtd_price_source
rtd_price_updated_at
rtd_price_created_at
~~~

A validação cobre:

- gravação da execução de pricing;
- leitura individual por `get_execution`;
- listagem por `list_executions`;
- envio das legs ao snapshot do sistema;
- preservação dentro de `operation_state_json["pricing_payload"]["legs"]`.

### Testes executados

~~~bash
python -m pytest ATT/tests/test_pricing_execution_price_source_persistence.py -v
~~~

Resultado:

~~~text
5 passed in 0.26s
~~~

~~~bash
python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v
~~~

Resultado:

~~~text
21 passed in 1.37s
~~~

### Evidências principais

- Uma leg com `price_source = rtd_option_quotes` foi persistida com metadados RTD completos.
- A leitura por `get_execution` preservou todos os campos de rastreabilidade RTD.
- A leitura por `list_executions` preservou todos os campos de rastreabilidade RTD.
- O snapshot operacional recebeu a leg com os mesmos campos RTD.
- O `operation_state_json` preservou o `pricing_payload` com a rastreabilidade RTD completa.
- Não houve alteração funcional em serviços, repositórios, schema, UI, bridge ou arquivos operacionais em `dados/`.

### Decisão tomada

A Fase 10E foi validada como camada regressiva operacional sobre a Fase 10D.

A rastreabilidade do preço RTD agora é considerada preservada desde a resolução do preço no payload canônico até a persistência da execução, recuperação posterior e geração de snapshot do sistema.

### Pendências

- Abrir PR empilhado da branch `fase-10e-validacao-operacional-rastreabilidade-preco-rtd`.
- Prosseguir apenas após decisão da próxima fase técnica com novo mapa de impacto.

### Commit relacionado

~~~text
2133966 test: valida rastreabilidade RTD persistida na fase 10E
~~~

## Fase 10F — Validação operacional fim-a-fim da rastreabilidade RTD/Excel

Data/hora: 15/06/2026 21:03 BRT

### Objetivo

Validar, em cenário operacional mais próximo do real, que uma cotação RTD alimentada via Excel chega ao backend, é usada na resolução do preço da opção, entra no payload canônico de pricing e permanece rastreável após persistência.

### Contexto

As Fases 10C, 10D e 10E consolidaram a rastreabilidade do preço RTD em três camadas:

- resolução do preço efetivo no payload canônico;
- exposição dos metadados RTD usados na resolução;
- preservação desses metadados na persistência, consulta e snapshot operacional.

A Fase 10F busca validar o fluxo fim-a-fim com foco operacional, sem introduzir alteração funcional pesada.

### Escopo de validação

Validar o caminho:

~~~text
Excel / RTD
rtd_option_quotes
CanonicalPricingFacade
pricing payload
pricing_executions
operation_state_json
system snapshot
~~~

### Campos mínimos esperados

~~~text
price_source = rtd_option_quotes
rtd_price_field
rtd_quote_codigo_opcao
rtd_quote_ativo_base
rtd_price_source
rtd_price_updated_at
rtd_price_created_at
~~~

### Restrições

- Não alterar schema.
- Não alterar UI.
- Não alterar bridge.
- Não versionar bancos locais ou arquivos operacionais em `dados/`.
- Não alterar importadores.
- Não introduzir mudança funcional sem teste regressivo.
- Priorizar evidência operacional, teste controlado ou smoke test auditável.

### Pendências

- Identificar o ponto mais seguro para executar a validação fim-a-fim.
- Confirmar qual banco local contém `rtd_option_quotes` alimentado pelo Excel/RTD.
- Executar consulta de inspeção sobre cotações RTD disponíveis.
- Executar pricing usando opção com cotação RTD disponível.
- Validar payload e persistência com os campos de rastreabilidade.
- Registrar evidências e resultado final.

### Commit relacionado

Pendente.

---

## Fase 11 — Testes integrados RTD ponta a ponta

### Status

Concluída.

### Branch

`fase-11-testes-integrados-rtd`

### Objetivo

Adicionar cobertura integrada para validar o fluxo controlado:

RTD_LINKS.csv -> importação -> rtd_option_quotes -> CanonicalPricingFacade -> pricing_payload -> pricing_executions -> system snapshot/query

A fase deve comprovar que o preço efetivo oriundo de `rtd_option_quotes.ultimo_preco` é usado pelo pricing e que a rastreabilidade operacional é preservada durante persistência e consulta posterior.

### Mapa de impacto antes de alteração funcional

#### Arquivos que poderão ser alterados

- `docs/AUDITORIA_ROTA_MESTRE_2.md`
- `ATT/tests/test_fase_11_rtd_integrated_flow.py`

#### Arquivos apenas auditados

- `scripts/import_rtd_links_to_option_quotes.py`
- `scripts/run_rtd_option_quotes_pipeline.py`
- `repositories/rtd_option_quotes_repository.py`
- `repositories/pricing_executions_repository.py`
- `services/canonical_pricing_facade.py`
- `services/pricing_execution_app_service.py`
- `services/pricing_execution_orchestration_service.py`
- `services/pricing_execution_persistence_service.py`
- `services/pricing_execution_query_service.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`
- `services/structure_market_input_assembler.py`
- `ATT/tests/test_import_rtd_links_to_option_quotes.py`
- `ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py`
- `ATT/tests/test_pricing_execution_price_source_persistence.py`

#### Escopo permitido

- Criar teste integrado novo usando banco temporário.
- Criar fixtures locais ao teste.
- Criar CSV temporário simulando `RTD_LINKS.csv`.
- Validar importação, leitura via repository, execução de pricing, persistência e rastreabilidade.

#### Escopo proibido nesta fase inicial

- Não alterar UI.
- Não alterar schema produtivo.
- Não alterar arquivos em `dados/`.
- Não alterar motor de cálculo.
- Não alterar importador produtivo.
- Não alterar comportamento funcional existente.
- Não executar pipeline contra banco real.

#### Risco esperado

Baixo a médio.

O risco principal está em montar um teste integrado que dependa de muitos detalhes internos do banco temporário. A mitigação será reutilizar padrões já existentes nos testes atuais e manter o teste isolado em `tmp_path`.

#### Testes que validarão a mudança

Regressão-base:

`python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v`

Novo teste da fase:

`python -m pytest ATT/tests/test_fase_11_rtd_integrated_flow.py -v`

Suíte combinada da fase:

`python -m pytest ATT/tests/test_fase_11_rtd_integrated_flow.py ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v`

#### Plano de reversão

Antes de commit:

`git restore docs/AUDITORIA_ROTA_MESTRE_2.md`

`rm -f ATT/tests/test_fase_11_rtd_integrated_flow.py`

Depois de commit:

`git revert <hash_do_commit>`

### Auditoria inicial executada

Comandos executados:

- `git checkout -b fase-11-testes-integrados-rtd`
- `git status -sb`
- `git branch --show-current`
- `test -f docs/AUDITORIA_ROTA_MESTRE_2.md && sed -n '1,260p' docs/AUDITORIA_ROTA_MESTRE_2.md || echo "NAO_EXISTE"`
- `find ATT/tests -maxdepth 1 -type f | grep -Ei "rtd|pricing|snapshot|execution|canonical|ui"`
- `git grep -n "price_resolution_status\|rtd_quote_found\|rtd_validation_status\|rtd_validation_message\|price_source\|rtd_option_quotes" -- services repositories ATT/tests docs`
- `git grep -n "class \|def " -- repositories/rtd_option_quotes_repository.py repositories/pricing_executions_repository.py services/canonical_pricing_facade.py services/pricing_execution_persistence_service.py services/pricing_execution_query_service.py services/pricing_execution_app_service.py services/pricing_execution_orchestration_service.py services/market_snapshot_provider.py services/market_snapshot_selector.py services/structure_market_input_assembler.py`
- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v`

Resultado inicial:

`26 passed`

### Decisão inicial

Avançar criando apenas teste integrado novo e documentação, sem alteração funcional produtiva.


### Implementação executada

Criado o teste integrado controlado `ATT/tests/test_fase_11_rtd_integrated_flow.py`.

O teste usa banco temporário em `tmp_path`, CSV temporário simulando `RTD_LINKS.csv` e não acessa banco real nem arquivos operacionais em `dados/`.

Fluxo validado:

`RTD_LINKS.csv -> import_csv_to_db -> rtd_option_quotes -> CanonicalPricingFacade.execute_pricing -> pricing_payload -> pricing_executions -> structure_snapshots/system snapshot query`

### Evidências validadas

- Importação do CSV temporário para `rtd_option_quotes`.
- Normalização de uma opção RTD.
- UPSERT controlado com `source = rtd_links`.
- Leitura posterior da cotação importada.
- Uso efetivo de `rtd_option_quotes.ultimo_preco` como preço da perna.
- Substituição do preço original do snapshot operacional pelo preço RTD importado.
- Preservação de `price_source = rtd_option_quotes`.
- Preservação de metadados de rastreabilidade RTD no `pricing_payload`.
- Persistência da execução em `pricing_executions`.
- Consulta posterior da execução persistida.
- Criação de snapshot operacional via `SystemSnapshotsRepository`.
- Consulta posterior do snapshot.
- Preservação da rastreabilidade no `operation_state_json` e no `raw_json` da perna do snapshot.

### Testes executados após implementação

Teste novo da fase:

`python -m pytest ATT/tests/test_fase_11_rtd_integrated_flow.py -v`

Resultado:

`1 passed`

Suíte combinada da fase:

`python -m pytest ATT/tests/test_fase_11_rtd_integrated_flow.py ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_execution_price_source_persistence.py -v`

Resultado:

`27 passed`

### Resultado final

Fase 11 concluída com sucesso.

O fluxo RTD ponta a ponta está coberto por teste integrado isolado, auditável e sem dependência de banco real.

### Commit relacionado

Pendente.

