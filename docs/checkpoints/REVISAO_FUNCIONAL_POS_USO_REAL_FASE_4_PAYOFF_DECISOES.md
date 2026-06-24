# REVISAO FUNCIONAL POS USO REAL
# FASE 4 - INTEGRACAO DA ESTRUTURA MANUAL COM PAYOFF E DECISOES

## 1. Objetivo

Garantir que estrutura criada manualmente ou por cadastro assistido nao seja apenas visual, mas funcional.

A estrutura valida deve participar do fluxo de payoff e decisoes.

## 2. Problemas tratados

- Estrutura aparece na tela, mas nao gera payoff.
- Estrutura aparece na tela, mas nao participa de decisoes.
- structure_decisions fica com zero linhas.
- payoff_curve_points nao recebe dados.
- Pipeline pode ignorar estruturas manuais.

## 3. Pontos a investigar

- Tabela principal de estruturas.
- Tabela de legs.
- Relacao structure_id.
- Filtro mode=canonical.
- Campos obrigatorios para payoff.
- Campos obrigatorios para decisoes.
- Normalizacao de comprado e vendido.
- Status active.
- Motivo de rejeicao no pipeline.

## 4. Criterios de aceite

- Estrutura manual valida gera curva de payoff.
- Estrutura manual valida gera decisoes.
- structure_decisions recebe registros ou informa rejeicao.
- payoff_curve_points recebe pontos ou informa rejeicao.
- Sistema mostra motivo claro quando faltar dado.
- Logs indicam estruturas lidas, processadas, ignoradas e rejeitadas.

## 5. Buscas realizadas

A preencher com os comandos e resultados das buscas antes das alteracoes.

## 6. Arquivos analisados

A preencher apos investigacao.

## 7. Diagnostico inicial

A preencher apos reproducao e leitura do fluxo.

## 8. Alteracoes realizadas

Pendente.

## 9. Testes executados

Pendente.

## 10. Resultado

Pendente.

## 11. Commit

Pendente.
