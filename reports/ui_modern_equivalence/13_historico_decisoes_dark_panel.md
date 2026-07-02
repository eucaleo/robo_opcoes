# Historico de decisoes no painel dark

## 1. Objetivo

Registrar decisoes operacionais por estrutura diretamente no painel dark da UI moderna.

## 2. Escopo

A alteracao adicionou persistencia e exibicao local das ultimas decisoes operacionais da estrutura selecionada.

Decisoes cobertas:

- HOLD / Manter
- ADJUST / Ajustar
- CLOSE / Encerrar

## 3. Arquivo alterado

- UI/components/terminal_vwap_payoff_dark_panel.py

## 4. Banco de dados

Foi criada tabela local, quando inexistente:

- structure_decisions

Campos principais:

- id
- structure_id
- decision
- label
- note
- created_at

Foi criado indice:

- idx_structure_decisions_structure_id

## 5. Resultado funcional

O painel dark passou a:

- registrar decisao operacional por estrutura;
- salvar label amigavel;
- salvar data e hora local;
- exibir bloco ULTIMAS DECISOES no painel lateral;
- preservar comportamento de CLOSE arquivando a estrutura.

## 6. Validacao executada

Validacao manual:

- python -m UI.modern

Resultado observado:

- UI moderna abriu em modo dark;
- estruturas reais foram carregadas;
- estrutura ID 2 foi carregada;
- decisao HOLD foi registrada;
- historico apareceu na interface com data e hora;
- registro foi confirmado em dados/app.db na tabela structure_decisions.

Registro observado:

- structure_id: 2
- decision: HOLD
- label: Manter
- created_at: 2026-07-02 11:07:16

## 7. Commit funcional associado

- 2830b8c Adiciona historico de decisoes no painel dark

## 8. Restricoes preservadas

A alteracao nao:

- elimina a UI atual;
- troca o entrypoint principal;
- migra para web;
- cria sincronismo entre derived.db e app.db;
- altera calculo de payoff;
- altera RTD;
- altera contratos canonicos.

## 9. Observacao arquitetural

Esta entrega melhora o fluxo operacional de decisoes por estrutura, mas nao encerra a lacuna maior registrada na secao 30 da auditoria.

Continuam pendentes para equivalencia funcional da UI atual:

- filtros globais de decisoes;
- tabela/listagem global de decisoes;
- selecao de decisao;
- detalhe da decisao;
- rationale/why JSON;
- payoff acionado a partir de decisao selecionada.
