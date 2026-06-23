# Revisao funcional pos uso real - Fase 4 - Payoff e decisoes para estrutura manual

## Objetivo

Garantir que uma estrutura criada manualmente ou por cadastro assistido seja funcional no pipeline de payoff e decisoes.

## Problemas tratados

- Estrutura aparece na tela, mas nao gera payoff.
- Estrutura aparece na tela, mas nao participa de decisoes.
- structure_decisions fica com zero linhas.
- payoff_curve_points nao recebe dados.
- Pipeline pode ignorar estruturas manuais.

## Pontos investigados

- Tabela principal de estruturas.
- Tabela de legs.
- Relacao structure_id.
- Filtro mode=canonical.
- Campos obrigatorios para payoff.
- Campos obrigatorios para decisoes.
- Normalizacao de comprado e vendido.
- Status active.
- Motivo de rejeicao no pipeline.

## Criterios de aceite

- Estrutura manual valida gera curva de payoff.
- Estrutura manual valida gera decisoes.
- structure_decisions recebe registros ou informa rejeicao.
- payoff_curve_points recebe pontos ou informa rejeicao.
- Sistema mostra motivo claro quando faltar dado.
- Logs indicam estruturas lidas, processadas, ignoradas e rejeitadas.

## Evidencias

A preencher apos implementacao e validacao.

## Resultado

Pendente.

## Commit

Pendente.
