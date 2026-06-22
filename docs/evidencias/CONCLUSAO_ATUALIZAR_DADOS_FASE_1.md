# Conclusão - Atualizar Dados - Fase 1

## Resultado observado

A reprodução funcional mostrou que o uso de Arquivo > Atualizar Dados não altera os bancos dados/app.db e dados/derived.db.

O diff entre snapshot antes e depois alterou apenas:

- título do snapshot;
- horário de geração.

Não houve alteração em:

- contagem de structures;
- contagem de structure_legs;
- contagem de rtd_option_quotes;
- contagem de pricing_executions;
- contagem de structure_decisions;
- contagem de payoff_curve_points;
- últimas execuções de pricing;
- últimas decisões;
- grupos de payoff.

## Evidência de código

Foi localizado em UI/main_window.py:

    file_menu.add_command(label="Atualizar Dados", command=self.refresh_data)

Portanto, o comando Atualizar Dados chama refresh_data.

## Diagnóstico

O comportamento observado explica por que os snapshots não mudaram: o comando atual recarrega dados já persistidos para a interface, mas não executa atualização automática, pipeline, pricing, consolidação ou geração de payoff.

## Correção de entendimento funcional

A expectativa correta do produto não é depender de atualização manual.

Como o RTD atualiza continuamente, o sistema deve refletir essas alterações automaticamente em intervalo controlado, por exemplo a cada 30 segundos, evitando loop excessivo e sobrecarga da interface.

O botão Atualizar Dados não deve ser o mecanismo principal de atualização do sistema.

## Direção funcional correta

O sistema deve ter atualização automática para:

- cotações RTD;
- dados exibidos na interface;
- estado das estruturas;
- informações dependentes de preço de mercado.

O intervalo deve ser controlado para evitar sobrecarga, por exemplo 30 segundos, com proteção contra reentrância quando uma atualização anterior ainda estiver em execução.

## Recalculo

O recalculo deve ficar restrito ao payoff e análises estimadas.

Esse recalculo deve servir para cenários analíticos, simulações e curvas de payoff, e não para substituir o fluxo normal de atualização de dados.

## Cadastro de pernas

A inclusão de pernas da estrutura deve ser orientada por símbolo.

Exemplo:

    PRIOH125

Ao informar o símbolo da opção, o sistema deve buscar ou inferir os dados necessários da perna, como ativo, vencimento, strike, tipo da opção, cotação e demais campos operacionais.

O usuário não deveria precisar preencher manualmente todos os campos derivados quando o símbolo já identifica a opção.

## Problema de produto identificado

A existência de múltiplos botões com nomes próximos, como Atualizar Dados, Executar Pipeline e Recalcular, cria ambiguidade funcional.

Na prática, isso faz com que nenhum deles represente claramente uma responsabilidade específica para o usuário.

## Recomendação

Substituir a dependência de botões manuais por um fluxo automático:

- atualização automática em intervalo controlado;
- botão manual apenas para forçar atualização imediata, se necessário;
- recalculo limitado a payoff e análises;
- cadastro de pernas por símbolo de opção;
- logs claros quando uma atualização, consolidação ou cálculo não puder ser executado.

