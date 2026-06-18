# Fase 6.3 — Mapa de impacto e retomada funcional incremental pós-pipeline RTD

## Objetivo

Definir o mapa de impacto para retomada incremental do desenvolvimento após a consolidação do pipeline RTD wide/autobootstrap.

Esta fase existe para impedir alterações dispersas em UI, API, repositories ou serviços sem rastreabilidade e sem proteção de testes.

---

## Contexto

A Fase 6.2 foi concluída com sucesso.

Checkpoint anterior:

- `docs/checkpoints/fase-6-2-validacao-pos-correcao-pipeline-rtd-wide.md`

Commits relacionados:

- `700a716 Corrige pipeline RTD wide com autobootstrap de schema`
- `bc5ab65 docs: registra fase 6.2 validacao pos-correcao RTD wide`
- `f1986af docs: fecha fase 6.2 validacao RTD wide`

Resultados registrados na fase anterior:

- `16 passed in 0.43s`
- `19 passed, 630 deselected in 3.10s`

---

## Premissas consolidadas

1. O Excel permanece apenas como gateway RTD.
2. A tabela `rtd_option_quotes` é o ponto persistido para snapshots RTD.
3. O pipeline RTD wide/autobootstrap está validado.
4. Alterações funcionais devem ser incrementais e protegidas por testes.
5. Nenhuma mudança em UI, API, repository ou serviço deve ocorrer sem mapa de impacto.
6. Bancos locais continuam fora do versionamento.

---

## Escopo desta fase

Mapear:

1. consumidores atuais de `rtd_option_quotes`;
2. pontos de entrada operacionais do pipeline RTD;
3. dependências com precificação/canonical pricing;
4. dependências com auditoria;
5. arquivos candidatos a alteração;
6. testes existentes relacionados;
7. lacunas de teste antes da próxima alteração funcional.

---

## Fora de escopo

Nesta fase ainda não deve ocorrer:

1. alteração em layout de UI;
2. criação de nova API;
3. mudança de contrato em repository;
4. alteração funcional em serviço de precificação;
5. limpeza destrutiva de arquivos operacionais;
6. versionamento de banco local;
7. substituição do papel do Excel como gateway RTD.

---

## Comandos de inventário planejados

- `git status --short`
- `git grep -n -E "rtd_option_quotes|run_rtd_option_quotes_pipeline|audit_rtd_option_quotes|canonical_pricing" -- .`
- `python -m pytest ATT/tests -k "rtd_option_quotes"`
- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`

---

## Critérios de conclusão

A Fase 6.3 somente poderá ser encerrada quando houver registro de:

1. arquivos impactados;
2. módulos consumidores;
3. testes existentes;
4. lacunas identificadas;
5. decisão do próximo incremento funcional;
6. comandos executados;
7. resultados obtidos;
8. commit documental relacionado.

---

## Status

Iniciada documentalmente em 2026-06-18.

Pendente de execução dos comandos de inventário e definição do primeiro incremento funcional após a consolidação do pipeline RTD.

---

## Inventário executado

Comandos executados durante a Fase 6.3:

- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`
- `python -m pytest ATT/tests -k "rtd_option_quotes"`
- inventário focado por `git grep` excluindo `docs` e restringindo arquivos produtivos Python;
- inventário complementar de testes RTD.

Evidências registradas em:

- `docs/checkpoints/evidencias/fase-6-3-pytest-canonical-pricing-rtd-db-path.txt`
- `docs/checkpoints/evidencias/fase-6-3-pytest-rtd-option-quotes.txt`
- `docs/checkpoints/evidencias/fase-6-3-inventario-focado-rtd.md`
- `docs/checkpoints/evidencias/fase-6-3-inventario-testes-rtd.md`
- `docs/checkpoints/evidencias/fase-6-3-git-status-inicial.txt`
- `docs/checkpoints/evidencias/fase-6-3-git-status-pos-inventario.txt`

---

## Resultados dos testes

### Canonical pricing com caminho RTD

Comando:

- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`

Resultado:

- `6 passed in 1.53s`

### Testes relacionados a rtd_option_quotes

Comando:

- `python -m pytest ATT/tests -k "rtd_option_quotes"`

Resultado:

- `19 passed, 630 deselected in 2.92s`

---

## Mapa de impacto apurado

### Infraestrutura de schema

- `infra/bootstrap_rtd_option_quotes_schema.py`

Responsabilidade:

- criar e validar o schema da tabela `rtd_option_quotes`;
- garantir colunas obrigatórias antes da importação;
- manter o bootstrap idempotente.

### Repository de leitura

- `repositories/rtd_option_quotes_repository.py`

Responsabilidade:

- centralizar leitura da tabela `rtd_option_quotes`;
- evitar SQL espalhado em serviços consumidores;
- servir como camada controlada entre persistência RTD e regra funcional.

### Pipeline/importação/auditoria

- `scripts/import_rtd_option_quotes_wide_csv.py`
- `scripts/run_rtd_option_quotes_pipeline.py`
- `scripts/audit_rtd_option_quotes.py`
- `scripts/run_rtd_refresh_full.py`

Responsabilidade:

- importar o CSV wide gerado pelo gateway RTD;
- garantir bootstrap automático do schema;
- auditar qualidade da tabela;
- executar ciclo operacional de refresh.

### Scripts legados ou auxiliares

- `scripts/import_lista_rtd_excel_to_option_quotes.py`
- `scripts/import_rtd_links_to_option_quotes.py`
- `scripts/run_lista_rtd_option_quotes_pipeline.py`
- `scripts/seed_current_rtd_option_quotes.py`
- `scripts/build_rtd_symbols.py`
- `scripts/mapear_automacao_opcoes_rtd.py`

Responsabilidade:

- suporte histórico, migração, seed ou automação auxiliar;
- não devem ser priorizados para alteração funcional ampla sem nova decisão explícita.

### Consumidor funcional principal

- `services/canonical_pricing_facade.py`

Responsabilidade:

- resolver o banco correto que contém `rtd_option_quotes`;
- instanciar `RtdOptionQuotesRepository`;
- usar preços RTD como fonte controlada dentro da hierarquia de precificação;
- preservar fallback para preço manual explícito e preço original do snapshot.

---

## Testes existentes identificados

Testes diretamente relacionados ao escopo RTD/canonical pricing:

- `ATT/tests/test_audit_rtd_option_quotes.py`
- `ATT/tests/test_run_rtd_option_quotes_pipeline.py`
- `ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`

Cobertura atual observada:

- auditoria da tabela `rtd_option_quotes`;
- pipeline RTD wide/autobootstrap;
- resolução de caminho RTD no `canonical_pricing_facade`;
- integração básica entre facade e repository RTD.

---

## Lacunas identificadas

Antes de alteração funcional ampla, ainda devem ser protegidos explicitamente:

1. contrato público de leitura do `RtdOptionQuotesRepository`;
2. comportamento do `canonical_pricing_facade` quando:
   - existe preço RTD válido;
   - existe bid/ask válido;
   - existe último preço válido;
   - não existe preço RTD;
   - o banco RTD não possui a tabela;
3. precedência documental e testada entre:
   - preço manual explícito;
   - `rtd_option_quotes`;
   - preço original do snapshot;
4. decisão sobre scripts legados:
   - manter;
   - congelar;
   - substituir;
   - remover em fase futura.

---

## Decisão do próximo incremento funcional

A próxima fase recomendada é:

- Fase 6.4 — Proteção do contrato de leitura RTD para canonical pricing.

Escopo sugerido da Fase 6.4:

1. não alterar UI;
2. não criar nova API;
3. não alterar contrato externo de serviço;
4. fortalecer testes em torno de `repositories/rtd_option_quotes_repository.py`;
5. fortalecer testes de precedência RTD dentro de `services/canonical_pricing_facade.py`;
6. manter Excel exclusivamente como gateway RTD;
7. manter bancos locais fora do versionamento.

---

## Status atualizado

A Fase 6.3 produziu mapa de impacto, evidências de teste e decisão de próximo incremento.

Pendente apenas commit documental das evidências e deste fechamento.
