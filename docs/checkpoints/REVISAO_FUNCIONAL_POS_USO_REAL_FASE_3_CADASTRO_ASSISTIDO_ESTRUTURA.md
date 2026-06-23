# Revisao funcional pos uso real — Fase 3 — Cadastro assistido de estrutura

## Status

Concluida por reconciliacao documental.

## Escopo

Esta fase cobre o cadastro assistido/manual de estruturas no estado atual da aplicacao, com foco no fluxo de criacao e edicao de estruturas via interface, montagem de legs e persistencia por repositorio/API interna.

## Situacao anterior no mapa

Antes desta reconciliacao, a fase constava no mapa como:

| Fase | Tema | Checkpoint | Situacao |
|---|---|---|---|
| Fase 3 | Cadastro assistido de estrutura | Sem checkpoint oficial | Necessita reconciliacao |

## Evidencias localizadas

Foram encontrados materiais documentais e evidencias relacionadas a cadastro, estrutura, payoff e schema canonico:

- `docs/checkpoints/evidencias/fase-3a-diagnostico-cadastro-payoff-decisoes.txt`
- `docs/checkpoints/evidencias/fase-3a-find-arquivos-estrutura-payoff-decisoes.txt`
- `docs/checkpoints/evidencias/fase-3a-gitls-arquivos-estrutura-payoff-decisoes.txt`
- `docs/checkpoints/evidencias/fase-3b-diagnostico-schema-canonico-estruturas.txt`
- `docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt`
- `docs/checkpoints/evidencias/fase-8-mapa-impacto-cadastro-estruturas-leg-minima.txt`
- `docs/evolucoes de fases/auditoria_fase_9_cadastro_estruturas.md`

Esses documentos indicam que a area de estruturas foi analisada em fases posteriores, mas a Fase 3 ainda nao possuia checkpoint oficial consolidado no mapa de estado atual.

## Arquivos tecnicos principais

Arquivos identificados como diretamente relacionados ao cadastro/editor de estrutura:

- `UI/components/structure_editor_dialog.py`
- `UI/components/structures_list_panel.py`
- `UI/main_window.py`
- `api/structures_controller.py`
- `repositories/structures_repository.py`
- `repositories/structure_events_repository.py`
- `services/structure_input_mapper.py`
- `services/structure_market_input_assembler.py`
- `services/structure_analysis_service.py`
- `services/structure_events_service.py`
- `infra/bootstrap_structures_schema.py`

## Teste automatizado principal

Teste executado:

- `ATT/tests/test_structure_editor_dialog.py`

Comando:

    python -m pytest ATT/tests/test_structure_editor_dialog.py -v

Resultado observado:

    35 passed in 0.27s

## Cenarios cobertos pelo teste principal

O teste `ATT/tests/test_structure_editor_dialog.py` cobre os seguintes pontos relevantes para a Fase 3:

- montagem de payload de legs;
- preservacao dos campos originais;
- multiplas legs sem contaminacao de indices;
- `leg_order` iniciando em 1;
- `leg_order` sequencial;
- lista vazia retornando lista vazia;
- preservacao de `legs_rows` original;
- carregamento de campos existentes via repositorio;
- carregamento de legs existentes;
- destruicao da janela quando estrutura nao e encontrada;
- criacao de estrutura com campos corretos;
- bloqueio de criacao quando `name` esta vazio;
- bloqueio de criacao quando `underlying` esta vazio;
- chamada de `replace_legs` apos criacao;
- marcacao de `saved = True` apos sucesso;
- modo edicao sem chamar criacao;
- atualizacao usando `structure_id` correto;
- `replace_legs` usando `structure_id` existente;
- existencia do arquivo da UI;
- existencia da classe principal;
- construtor aceitando `db_path`;
- construtor aceitando repositorio injetado;
- importacao do componente;
- ausencia de importacao direta de `sqlite3` no componente;
- normalizacao de `position_side` legado `long`/`short`;
- normalizacao de `strike` com virgula para `float`;
- normalizacao de `strike` com ponto para `float`;
- preservacao do valor original de `strike` ao normalizar;
- normalizacao de `premium` com virgula para `float`;
- normalizacao de `multiplier` com virgula para `float`;
- preservacao de `premium = None`;
- normalizacao de `quantity` inteiro valido;
- rejeicao de `quantity` invalido.

## Decisao

A Fase 3 pode ser considerada concluida por reconciliacao documental no estado atual.

A decisao se apoia em tres pontos:

1. O mapa indicava ausencia de checkpoint oficial, nao necessariamente ausencia de implementacao.
2. Foram encontradas evidencias documentais historicas relacionadas a cadastro, estruturas, schema canonico e legs.
3. O teste principal do editor de estruturas esta verde com 35 cenarios passando.

## Observacao

Esta reconciliacao nao altera codigo de producao. O objetivo e apenas formalizar o estado existente e alinhar o mapa documental da revisao funcional pos uso real.

## Proximo passo

Atualizar o mapa de estado atual para apontar esta fase para este checkpoint oficial.
