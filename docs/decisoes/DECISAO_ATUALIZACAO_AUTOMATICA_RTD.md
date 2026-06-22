# Decisão - Atualização Automática baseada no RTD

## Contexto

Foi identificado que o comando Arquivo > Atualizar Dados apenas recarrega dados já persistidos na interface.

Esse comportamento não atende ao funcionamento esperado do produto, pois o RTD atualiza as cotações continuamente e o sistema deve acompanhar essa dinâmica de forma automática e controlada.

## Decisão funcional

O sistema deve atualizar automaticamente os dados dependentes do RTD em intervalo controlado.

O intervalo inicial recomendado é de 30 segundos.

A atualização automática deve evitar reentrância. Se uma atualização anterior ainda estiver em execução, a próxima rodada deve ser ignorada ou adiada.

## Comportamento esperado

O usuário não deve depender de ação manual para que dados vivos sejam refletidos na interface.

A atualização automática deve cobrir:

- leitura ou sincronização de dados RTD;
- atualização dos dados apresentados na interface;
- atualização do estado visual das estruturas;
- atualização de informações dependentes de preço de mercado.

## Botão Atualizar Dados

O botão Atualizar Dados não deve ser o fluxo principal do sistema.

Caso permaneça na interface, sua função deve ser apenas forçar uma atualização imediata da tela ou dos dados já disponíveis.

Uma alternativa mais clara é renomear o comando para Recarregar Tela ou Atualizar Agora.

## Recalculo

O recalculo deve ser reservado para payoff e análises estimadas.

O recalculo não deve ser confundido com atualização geral de dados, pipeline, sincronização RTD ou persistência operacional.

## Pipeline

O pipeline não deve ser acionado de forma ambígua por botões genéricos.

Se houver necessidade de execução de pipeline, ela deve ter responsabilidade clara, logs próprios e proteção contra execução repetida involuntária.

## Cadastro de pernas

A inclusão de pernas de estrutura deve ser orientada por símbolo da opção.

Exemplo:

    PRIOH125

Ao informar o símbolo, o sistema deve buscar, inferir ou preencher os dados derivados necessários, como ativo base, vencimento, strike, tipo da opção, preço e demais campos operacionais.

## Regra de produto

A interface deve privilegiar o uso natural:

- dados vivos atualizados automaticamente;
- cadastro de perna por símbolo;
- payoff recalculado sob demanda;
- logs claros;
- botões com responsabilidade única.

