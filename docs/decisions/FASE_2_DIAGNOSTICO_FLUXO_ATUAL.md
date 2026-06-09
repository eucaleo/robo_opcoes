# Fase 2 — Diagnóstico do Fluxo Atual

## Objetivo

Entender como o sistema está funcionando atualmente antes de executar alterações técnicas.

## Perguntas principais

1. De onde o sistema lê as estruturas?
2. De onde ele lê as pernas das operações?
3. De onde vêm bid, ask, last, gregas e volatilidade?
4. Onde o sistema grava dados importados?
5. A UI lê do banco, CSV ou Excel?
6. Novas estruturas estão sendo persistidas?
7. O sistema depende de ANALISE_ROBO, ANALISE_ROBO_LEGS ou HIST_ROBO?

## Estado inicial

Branch em uso: limpeza-inicial-repositorio

Status esperado: working tree limpo antes da criação deste documento.

Situação da branch em relação à main: 0 atrás / 5 à frente.

## Escopo da auditoria

Nesta fase serão analisados:

- Excel;
- bridge;
- ingestão;
- banco;
- repositories;
- services;
- scripts;
- UI models;
- UI components.

## Achados

A preencher durante a auditoria.

## Mapa do fluxo atual

| Área | Fonte atual | Destino atual | Observação |
|---|---|---|---|
| Estruturas | A preencher | A preencher | A preencher |
| Pernas | A preencher | A preencher | A preencher |
| Cotações RTD | A preencher | A preencher | A preencher |
| Gregas | A preencher | A preencher | A preencher |
| UI | A preencher | A preencher | A preencher |
| Histórico | A preencher | A preencher | A preencher |
| Eventos | A preencher | A preencher | A preencher |

## Dependências legadas encontradas

| Fonte legada | Arquivos/funções dependentes | Tipo de dependência |
|---|---|---|
| ANALISE_ROBO | A preencher | A preencher |
| ANALISE_ROBO_LEGS | A preencher | A preencher |
| HIST_ROBO | A preencher | A preencher |
| CONFIGURACOES | A preencher | A preencher |
| ENCERRAMENTOS_MANUAIS | A preencher | A preencher |

## Testes executados

A preencher ao final da fase.

## Conclusão

A preencher ao final da fase.

## Decisão sobre fontes legadas e LISTA_RTD.xlsx

Durante o diagnóstico foi identificado que endurecer regras de domínio em torno de `alias_legacy_aba`, `ANALISE_ROBO`, `ANALISE_ROBO_LEGS` ou `HIST_ROBO` perpetua dependências legadas.

Decisão:

- `ANALISE_ROBO`, `ANALISE_ROBO_LEGS` e `HIST_ROBO` são fontes legadas/derivadas.
- Essas fontes podem ser usadas para diagnóstico, comparação ou migração pontual, mas não devem ser tratadas como cadastro canônico.
- `alias_legacy_aba` não deve ser requisito obrigatório no núcleo do repositório de estruturas.
- `LISTA_RTD.xlsx` passa a ser considerada candidata a fonte/gateway para o universo bruto RTD.
- O banco do sistema continua sendo a fonte da verdade para estruturas, legs, status operacional, auditoria e resultados.
- A integração RTD deve ser redesenhada para consumir uma camada bruta padronizada, sem depender das abas antigas como fonte de cadastro de operação.

Conclusão:

O fluxo novo não deve reconstruir o sistema em torno dos dados obsoletos. A Fase 2 deve mapear o legado existente e preparar a transição para um modelo onde a `LISTA_RTD.xlsx` alimenta dados RTD brutos, enquanto as estruturas operacionais nascem e vivem no banco do sistema.
