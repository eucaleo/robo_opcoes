# Contrato UI x Payoff x Recalculo

## Objetivo

Este documento define o contrato oficial entre a UI, o módulo de cálculo/payoff,
os snapshots persistidos e os botões relacionados a atualização/recalculo.

A UI não deve assumir função de cálculo. A UI deve apenas:

1. Exibir dados.
2. Solicitar atualização/recalculo ao módulo correto.
3. Consumir resultados persistidos ou retornados pelo serviço oficial.
4. Re-renderizar KPIs, gráficos, alertas e detalhes com base no resultado final.

---

## Regra central

**A UI NÃO calcula payoff.**

Cálculos de payoff, VWAP, estrutura, risco, breakeven ou qualquer cruzamento entre
dados operacionais devem ficar nos módulos competentes de cálculo/serviço.

A UI pode:

- Ler `payoff_curve_points`;
- Ler snapshots persistidos;
- Chamar callback/serviço oficial de recalculo;
- Recarregar estrutura aberta;
- Re-renderizar gráfico;
- Mostrar diferenças visuais/estado operacional.

A UI não pode:

- Recalcular payoff localmente;
- Criar curva estimada como fallback operacional;
- Substituir serviço de cálculo por lógica própria;
- Manter dupla função de tela + motor de cálculo.

---

## Semântica dos botões

### 1. Botão: Recalcular esta estrutura

Escopo: **somente a estrutura aberta/selecionada em tela**.

Fluxo esperado:

1. Capturar `structure_id` da estrutura atual.
2. Validar se existe estrutura ativa.
3. Solicitar recalculo ao módulo oficial.
4. Aguardar/receber confirmação.
5. Reler dados persistidos da estrutura.
6. Atualizar detalhes, payoff, KPIs, gráfico e alertas da estrutura aberta.

Não deve:

- Recalcular todas as estruturas.
- Executar cálculo dentro da UI.
- Usar fallback local.

Arquivos mapeados:

- `UI/components/details_panel.py`
  - Botão: `btn_recalculate`
  - Texto: `Recalcular esta estrutura`
  - Handler: `_on_recalculate_click`
  - Callback esperado: `_on_recalculate_cb(structure_id)`

---

### 2. Botão: Recalculo global / somente Recalculo

Escopo: **todo o sistema / todos os campos**.

Fluxo esperado:

1. Acionar comando global oficial.
2. Atualizar snapshots, payoff, decisões, VWAP/RTD e demais campos dependentes.
3. Persistir resultados.
4. UI deve apenas recarregar dados após conclusão.

Observação:

Nos arquivos enviados, o botão global de "Recalculo" não foi identificado de forma conclusiva.
É necessário auditar handlers contendo termos como:

- `recalculate`
- `refresh`
- `PayoffRefreshCommandService`
- `command=`
- `Atualizar`
- `Recalculo`
- `recalcular`

---

### 3. Botão: Atualizar payoff

Escopo: **somente a estrutura aberta em tela**.

Fluxo esperado:

1. Validar estrutura ativa.
2. Solicitar/reler atualização da estrutura aberta.
3. Consumir payoff persistido mais recente.
4. Atualizar KPIs, gráfico e alertas.
5. Mostrar se houve alteração relevante para tomada de decisão.

Não deve:

- Recalcular payoff dentro da UI.
- Recalcular o sistema inteiro.
- Alterar outras estruturas.

Arquivos mapeados:

- `UI/components/terminal_vwap_payoff_dark_panel.py`
  - Grupo: `_render_payoff_action_group`
  - Botão: `Atualizar payoff`
  - Handler: `recalculate_selected_structure`
  - Fluxo atual indicado nos arquivos:
    - `_refresh_selected_structure_from_store(silent=False)`
    - `_resolve_operational_payload(...)`
    - `_update_kpis(...)`
    - `_render_charts(...)`
    - `_render_alerts(...)`

Observação:

O nome `recalculate_selected_structure` foi mantido por compatibilidade, mas semanticamente
deve representar atualização/leitura da estrutura aberta, não cálculo local na UI.

---

## Auto-refresh

O auto-refresh deve ser leitura periódica de resultado pronto/snapshot persistido.

Arquivo mapeado:

- `UI/components/terminal_vwap_payoff_dark_panel.py`
  - `_start_auto_refresh_loop`
  - `_schedule_auto_refresh`
  - `_auto_refresh_tick`
  - `_refresh_selected_structure_from_store`

Contrato:

- Pode reler payoff persistido.
- Pode reler VWAP/RTD/snapshot.
- Pode re-renderizar gráfico.
- Não pode calcular payoff na UI.

---

## Pontos de atenção encontrados

### 1. Comentário contraditório em `terminal_vwap_payoff_dark_panel.py`

Foi encontrado comentário indicando que, quando não há curva persistida, a UI calcula curva estimada.

Isso viola o contrato atual.

Deve ser corrigido para:

- Sem curva persistida: mostrar alerta/estado vazio.
- Opcionalmente: solicitar geração ao serviço oficial.
- Nunca calcular fallback dentro da UI.

### 2. Cache em `UI/models/ui_data.py`

Existe cache de payoff:

- `_payoff_cache`
- `get_payoff_curve`
- `get_payoff_curve_info`

Ao recalcular ou atualizar payoff, o cache precisa ser invalidado ou bypassado para evitar gráfico velho.

Ponto importante:

- `refresh()` reconstrói colmap e estruturas, mas a validade do cache precisa ser confirmada.
- Existe `_payoff_cache = {}` em trecho posterior, mas o fluxo exato deve ser auditado.

### 3. Details Panel relê `app.db`

Arquivo:

- `UI/components/details_panel.py`

Fluxos:

- `_refresh_current_from_app_db(structure_id)`
- `_fetch_payoff_points_from_app_db(structure_id)`
- `_get_latest_snapshot_timestamp_for_structure(structure_id)`

Esse painel já indica intenção correta: depois do recalculo, reler estado persistido.

---

## Estado desejado final

1. UI sem cálculo local.
2. Botões com nomes e escopos claros.
3. Serviço oficial centralizado para recalculo.
4. Cache invalidado após recalculo/atualização.
5. Auto-refresh apenas relendo snapshots/payoff persistido.
6. Gráfico sempre refletindo dado vivo/persistido mais recente.
