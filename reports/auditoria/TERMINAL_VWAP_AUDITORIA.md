# Auditoria UI Terminal VWAP

Data de abertura: 2026-07-06

Branch:

    audit/terminal-vwap-ui

Classificacao:

    REGRESSAO_UI

## 1. Objetivo

Abrir frente propria para auditar Terminal VWAP sem misturar escopo com Decisoes dark panel, payoff, UIDataModel, banco, regra de negocio, services, repositories ou controllers.

## 2. Situacao inicial

A fatia Decisoes dark panel foi concluida como entrega parcial operacional.

Terminal VWAP permanece fora do escopo da branch Decisoes dark panel e deve ser tratado em frente propria.

## 3. Escopo permitido desta fase

Esta fase pode avaliar:

- abertura da UI pelo caminho atual do projeto;
- acesso ao Terminal VWAP;
- fluxo completo de estruturas;
- fluxo completo de pernas;
- alertas;
- KPIs;
- graficos;
- estados vazios;
- acoes operacionais proprias do terminal;
- mensagens de status;
- validacao visual em dark mode;
- pontos de regressao manual especificos do terminal.

## 4. Escopos proibidos nesta fase

Nao esta autorizado nesta fase:

- alterar banco;
- alterar schema;
- alterar regra de negocio;
- alterar services;
- alterar repositories;
- alterar controllers;
- alterar pipeline de dados;
- sincronizar app.db com derived.db;
- sincronizar derived.db com app.db;
- resolver payoff fora do necessario para observacao visual;
- declarar equivalencia global da UI moderna dark;
- alterar o entrypoint principal;
- eliminar a UI atual.

## 5. Primeira etapa autorizada

A primeira etapa desta frente e somente auditoria e inventario.

Nenhuma correcao funcional deve ser aplicada antes de registrar:

- arquivos envolvidos;
- componentes de UI relacionados;
- fluxos observados;
- pontos de validacao manual;
- pendencias encontradas;
- criterio minimo para smoke manual do Terminal VWAP.

## 6. Criterio minimo de continuidade

Antes de qualquer patch, esta auditoria deve responder:

- qual componente renderiza o Terminal VWAP;
- qual modelo de dados alimenta o terminal;
- quais acoes sao apenas UI;
- quais acoes dependem de regra de negocio;
- quais validacoes podem ser feitas sem banco ou pipeline;
- quais riscos exigem frente propria fora da UI.

## 7. Status

ABERTO
