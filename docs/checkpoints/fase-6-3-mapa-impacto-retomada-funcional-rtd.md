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
