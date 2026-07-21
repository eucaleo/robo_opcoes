# Plano de Correção UI Payoff

## Fase 1 — Documentação e auditoria

Status: planejado.

Ações:

- Formalizar contrato UI x cálculo.
- Mapear botões e handlers.
- Identificar onde a UI ainda calcula, estima ou faz fallback.
- Identificar onde o botão global de recalculo está implementado.
- Identificar a ligação com `PayoffRefreshCommandService`.

Entregáveis:

- `docs/payoff_audit/CONTRATO_UI_PAYOFF.md`
- `tools/reports/payoff_ui_bridge_audit.txt`

---

## Fase 2 — Correção de semântica dos botões

### Botão "Recalcular esta estrutura"

Deve chamar o serviço oficial apenas para `structure_id` ativo.

Possível origem:

- `UI/components/details_panel.py`
- `_on_recalculate_click`
- `_start_recalculate_callback`
- `_on_recalculate_cb(structure_id)`

Correção esperada:

- Garantir que callback esteja ligado ao serviço oficial.
- Garantir reload da estrutura após retorno.
- Garantir invalidação de cache de payoff.

---

### Botão "Atualizar payoff"

Origem provável:

- `UI/components/terminal_vwap_payoff_dark_panel.py`
- `_render_payoff_action_group`
- `recalculate_selected_structure`
- `_refresh_selected_structure_from_store`

Correção esperada:

- Manter escopo somente estrutura aberta.
- Remover qualquer cálculo local.
- Reler payoff persistido/snapshot.
- Atualizar gráfico e KPIs.
- Renomear internamente, se possível, para reduzir ambiguidade:
  - de `recalculate_selected_structure`
  - para `refresh_selected_structure_payoff`
  
Caso o nome antigo seja necessário por compatibilidade, manter wrapper com comentário explícito.

---

### Botão "Recalculo" global

Ainda precisa ser localizado no código.

Correção esperada:

- Deve chamar serviço global.
- Deve atualizar todo o sistema.
- UI deve aguardar/receber resultado e recarregar telas.

---

## Fase 3 — Remover cálculo/fallback da UI

Arquivo crítico:

- `UI/components/terminal_vwap_payoff_dark_panel.py`

Ações:

- Remover fallback estimado de payoff, se existir no código.
- Quando não houver payoff persistido:
  - mostrar alerta "payoff sem pontos";
  - manter gráfico vazio;
  - opcionalmente oferecer ação para solicitar cálculo ao serviço oficial.

---

## Fase 4 — Cache e consistência

Arquivo crítico:

- `UI/models/ui_data.py`

Ações:

- Confirmar invalidação de `_payoff_cache` após:
  - recalculo de estrutura;
  - recalculo global;
  - atualização manual do payoff;
  - reload de decisões.
- Se necessário, criar método público:
  - `clear_payoff_cache()`
  - `invalidate_payoff_cache(structure_id=None)`

---

## Fase 5 — Testes

Testes mínimos:

1. Atualizar payoff com estrutura aberta:
   - não chama cálculo local;
   - relê payoff persistido;
   - gráfico muda se o banco mudou.

2. Recalcular esta estrutura:
   - chama serviço oficial com `structure_id`;
   - não altera demais estruturas;
   - invalida cache;
   - recarrega tela.

3. Recalculo global:
   - chama serviço global;
   - atualiza todo o sistema;
   - telas refletem novos dados.

4. Sem payoff persistido:
   - UI não calcula fallback;
   - mostra estado vazio/alerta.

