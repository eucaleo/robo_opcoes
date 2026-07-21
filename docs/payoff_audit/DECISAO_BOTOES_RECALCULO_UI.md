# Decisão final: UI, payoff e recalculo

## Regra principal

A UI não calcula payoff, estrutura, preço, decisão, gregas ou qualquer campo derivado.

A UI apenas:
- identifica a estrutura aberta ou selecionada;
- solicita o recalculo ou atualização ao serviço correto;
- invalida caches locais quando necessário;
- relê o snapshot persistido;
- atualiza tela, KPIs, tabela e gráfico.

O centro de verdade permanece nos módulos de cálculo e serviços de backend.

## Botão: Recalcular esta estrutura

Escopo:
- somente a estrutura aberta ou selecionada em tela.

Comportamento esperado:
1. Capturar structure_id da estrutura atual.
2. Validar que a estrutura está ativa.
3. Chamar o serviço oficial de recalculo de estrutura.
4. Não calcular nada na UI.
5. Invalidar cache local relacionado ao payoff e decisão.
6. Reler o estado persistido.
7. Atualizar detalhes, gráfico, KPIs e status.

Não deve:
- recalcular todas as estruturas;
- gerar curva na UI;
- usar cálculo local alternativo;
- depender de snapshot antigo em cache.

## Botão: Recalculo global

Escopo:
- todo o sistema;
- todas as estruturas elegíveis;
- todos os campos derivados necessários.

Comportamento esperado:
1. Chamar serviço global oficial.
2. O serviço global deve percorrer estruturas ativas/elegíveis.
3. Para cada estrutura, chamar o fluxo oficial de backend.
4. Persistir payoff, decisão e demais campos derivados pelos módulos competentes.
5. A UI apenas acompanha status e relê dados no final.

Observação:
Nos relatórios atuais, o botão global de recalculo não foi identificado de forma conclusiva na UI.
Portanto, o entrypoint de backend deve existir, mas a ligação visual será feita somente quando o botão real for localizado ou criado de forma explícita.

## Botão: Atualizar payoff

Escopo:
- somente a estrutura aberta em tela.

Comportamento esperado:
1. Capturar structure_id da estrutura aberta.
2. Chamar o serviço oficial de refresh de payoff para essa estrutura.
3. Não calcular payoff na UI.
4. Invalidar cache local.
5. Reler o payoff persistido mais recente.
6. Redesenhar o gráfico.
7. Informar no status se houve novo snapshot, warning ou erro.

Finalidade:
- conferir se existe alteração relevante no gráfico para tomada de decisão;
- manter o gráfico refletindo dado vivo/persistido mais recente.

## Auto-refresh

O auto-refresh não é recalculo global.

O auto-refresh deve permanecer ligado ao fluxo operacional de atualização visual, VWAP, RTD e gráfico.
Ele pode reler dados persistidos ou dados finais recebidos do pipeline, mas não deve calcular payoff na UI.

## Serviços oficiais

Para refresh operacional de payoff por estrutura:
- services/payoff_refresh_command_service.py
- classe PayoffRefreshCommandService
- método refresh_payoff_for_structure

Para recalculo global:
- deve existir serviço dedicado de comando global;
- esse serviço pode reutilizar PayoffRefreshCommandService para cada estrutura ativa;
- a UI não deve implementar loop de cálculo global.

