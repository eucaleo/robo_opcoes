# Revisao funcional pos uso real - Fase 3 - Cadastro assistido de estrutura

## Objetivo

Permitir que o usuario cadastre uma estrutura informando apenas os campos principais, enquanto o sistema preenche automaticamente os dados tecnicos da leg a partir do simbolo da opcao.

## Campos informados pelo usuario

### Estrutura

- Nome da estrutura.

### Leg

- Lado: compra ou venda.
- Tipo: put ou call.
- Quantidade executada.
- Valor executado.
- Simbolo da opcao.

## Campos preenchidos pelo sistema

- Ativo objeto.
- Strike.
- Vencimento.
- Multiplicador.
- Metadados necessarios para payoff.
- Metadados necessarios para decisoes.

## Criterios de aceite

- Simbolo reconhecido preenche dados automaticamente.
- Simbolo nao encontrado gera mensagem clara.
- Divergencia entre tipo informado e tipo detectado bloqueia ou pede confirmacao.
- Estrutura so pode ser salva como funcional se tiver dados minimos.
- Teste manual ou automatizado registrado.

## Evidencias

A preencher apos implementacao e validacao.

## Resultado

Pendente.

## Commit

Pendente.
