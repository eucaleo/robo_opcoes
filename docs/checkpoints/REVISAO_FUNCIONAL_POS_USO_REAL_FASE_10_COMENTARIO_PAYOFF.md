# Revisão Funcional Pós Uso Real - Fase 10 - Comentário do gráfico de payoff

## Data

2026-06-26 11:47:20 -0300

## Branch

reinicio-normalizacao-idioma-ptbr

## Commit base

4e3fda8

## Objetivo

Adicionar interpretação textual ao gráfico de payoff, em Português Brasil, sem prometer resultado financeiro.

## Problemas tratados

- Gráfico mostra curva, mas não explica posição.
- Usuário precisa saber região de ganho, perda e melhor cenário.
- Quando não houver dados suficientes, a interface deve explicar o motivo.

## Escopo permitido

- Interface desktop atual.
- Componente de payoff existente.
- Textos interpretativos em Português Brasil.
- Uso dos dados já calculados pelo sistema.

## Escopo proibido

- Migração para web.
- Alteração de regra financeira sem evidência.
- Promessa de lucro ou recomendação financeira.
- Mudança fora do gráfico de payoff e da exibição relacionada.

## Critérios de aceite

- Comentário aparece junto ao payoff.
- Comentário usa Português Brasil.
- Comentário não promete resultado financeiro.
- Comentário depende dos dados calculados pelo sistema.
- Se não houver payoff, explica o motivo.
- Testes existentes continuam aprovados.
- Compilação sem erro.

## Arquivos inicialmente previstos para análise

- UI/components/payoff_chart.py
- ATT/tests/test_payoff_chart.py

## Situação inicial

Fase iniciada após encerramento funcional da Fase 9.

Commit anterior:

4e3fda8
