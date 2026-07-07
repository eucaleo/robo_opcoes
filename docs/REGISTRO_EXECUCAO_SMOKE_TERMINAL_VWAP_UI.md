# Registro de execucao smoke Terminal VWAP UI

Data: 2026-07-06

Branch:

    audit/terminal-vwap-ui

Commit base:

    a19cbf1

Classificacao:

    REGRESSAO_UI

Status:

    CONCLUIDO_VALIDACAO_MINIMA

## 1. Escopo executado

Smoke manual observacional do Terminal VWAP.

Componente principal provavel:

    UI/components/terminal_vwap_payoff_dark_panel.py

## 2. Estrutura tecnica observada antes da execucao

Classes encontradas no componente principal:

- linha 129: TerminalVWAPPayoffDarkPanel

Funcoes e metodos encontrados no componente principal:

- linha 59: _q
- linha 63: _norm
- linha 67: _first_col
- linha 75: _to_float
- linha 99: _money
- linha 106: _number
- linha 122: decision_label
- linha 130: __init__
- linha 155: _setup_style
- linha 182: _setup_layout
- linha 195: _configure_layout_grid
- linha 201: _build_rail_panel
- linha 209: _build_rail_container
- linha 219: _build_rail_toggle_button
- linha 233: _build_rail_reload_button
- linha 247: _build_rail_new_button
- linha 261: _build_rail_actions_button
- linha 275: _build_rail_open_button
- linha 290: _build_side_panel
- linha 300: _build_main_panel
- linha 310: _build_main_header
- linha 319: _build_kpi_panel
- linha 334: _build_chart_panels
- linha 349: _build_bottom_panel
- linha 376: _build_legs_table
- linha 412: _build_alerts_box
- linha 423: _create_kpi
- linha 449: toggle_structures_panel
- linha 460: reload_structures
- linha 465: _connect
- linha 473: _tables_cols
- linha 485: _find_structures_table
- linha 505: _load_structures
- linha 545: _render_structures_list
- linha 558: _render_structures_list_actions
- linha 570: _render_structures_list_header
- linha 589: _build_structures_scroll
- linha 597: _render_empty_structures_message
- linha 606: _render_structure_list_item
- linha 624: select_structure
- linha 655: _find_legs_table
- linha 676: _load_legs
- linha 700: _load_legs_schema
- linha 705: _resolve_legs_columns
- linha 719: _build_legs_select_parts
- linha 731: _fetch_legs_rows
- linha 746: _load_market
- linha 765: _empty_market_result
- linha 784: _normalize_market_asset
- linha 790: _build_market_query
- linha 817: _market_column_map
- linha 850: _market_select_parts
- linha 872: _market_order_sql
- linha 885: _market_result_from_rows
- linha 918: _market_series_from_rows
- linha 937: _load_payoff_points
- linha 947: _load_persisted_payoff_points
- linha 981: _calculate_payoff_from_legs
- linha 990: _collect_payoff_strikes
- linha 994: _calculate_payoff_spot_range
- linha 1002: _calculate_payoff_points_for_range
- linha 1022: _calculate_leg_payoff
- linha 1043: _is_short_payoff_leg
- linha 1051: _breakevens
- linha 1074: _update_kpis
- linha 1114: _render_legs
- linha 1134: _set_alerts
- linha 1141: _render_alerts
- linha 1163: _clear_canvas
- linha 1172: _figure
- linha 1183: _render_empty_charts
- linha 1187: _render_charts
- linha 1196: _render_vwap_chart
- linha 1201: _render_vwap_chart_stage_1
- linha 1208: _render_vwap_chart_stage_2
- linha 1246: _render_vwap_chart_stage_3
- linha 1256: _render_payoff_chart
- linha 1295: _build_payoff_export_button
- linha 1315: export_payoff_png
- linha 1354: _safe_status
- linha 1359: _get_db_path
- linha 1367: _clear_side
- linha 1372: _require_selected_structure
- linha 1384: _side_section_title
- linha 1395: _side_button
- linha 1408: _ensure_structure_decisions_table
- linha 1429: _insert_structure_decision
- linha 1458: _load_structure_decisions
- linha 1484: _render_decision_history
- linha 1501: _build_decision_history_box
- linha 1510: _render_decision_history_error
- linha 1521: _render_empty_decision_history
- linha 1532: _render_decision_history_item
- linha 1554: _render_structure_actions
- linha 1578: _format_active_structure_summary
- linha 1585: _render_side_panel_title
- linha 1595: _render_side_info_card
- linha 1608: _render_side_notice_card
- linha 1622: _render_payoff_action_group
- linha 1631: _render_structure_management_action_group
- linha 1652: _render_structure_decision_action_group
- linha 1673: _render_back_to_structures_button
- linha 1682: _render_adjust_structure_block
- linha 1698: _format_adjust_structure_summary
- linha 1704: _render_adjust_structure_notice
- linha 1710: _render_adjust_structure_actions
- linha 1738: new_structure
- linha 1763: edit_selected_structure
- linha 1783: _is_structure_editor_available
- linha 1794: _open_structure_editor
- linha 1803: _handle_structure_editor_saved
- linha 1818: duplicate_selected_structure
- linha 1845: _is_structures_repository_available
- linha 1856: _load_structure_for_duplication
- linha 1869: _create_duplicate_structure
- linha 1878: _duplicate_structure_legs
- linha 1884: _build_duplicate_legs_payload
- linha 1894: _refresh_after_structure_duplication
- linha 1907: recalculate_selected_structure
- linha 1938: archive_selected_structure
- demais funcoes ou metodos omitidos nesta visao: 14

## 3. Checklist de execucao manual

Preencher manualmente depois de abrir a UI.

| Item | Validacao | Resultado | Observacao |
| --- | --- | --- | --- |
| 1 | UI abre pelo entrypoint atual | PENDENTE | |
| 2 | Janela principal abre sem erro visivel | PENDENTE | |
| 3 | Modo dark permanece visualmente consistente | PENDENTE | |
| 4 | Area Terminal VWAP e acessivel | PENDENTE | |
| 5 | Painel Terminal VWAP renderiza sem excecao visivel | PENDENTE | |
| 6 | Estruturas aparecem quando ha dados | PENDENTE | |
| 7 | Estado vazio nao quebra a UI | PENDENTE | |
| 8 | Selecao de estrutura funciona | PENDENTE | |
| 9 | Detalhes da estrutura aparecem quando aplicavel | PENDENTE | |
| 10 | Pernas aparecem quando aplicavel | PENDENTE | |
| 11 | Ausencia de pernas e tratada sem quebra | PENDENTE | |
| 12 | KPIs aparecem quando aplicavel | PENDENTE | |
| 13 | Graficos aparecem quando aplicavel | PENDENTE | |
| 14 | Alertas aparecem quando aplicavel | PENDENTE | |
| 15 | Mensagens de status aparecem quando aplicavel | PENDENTE | |
| 16 | Botoes sem selecao nao quebram a UI | PENDENTE | |
| 17 | Botoes com selecao nao travam a UI | PENDENTE | |
| 18 | Navegacao para outra area e retorno funciona | PENDENTE | |
| 19 | UI permanece responsiva durante o fluxo | PENDENTE | |
| 20 | Resultado final registrado | PENDENTE | |

## 4. Resultado da execucao

Resultado final:

    APROVADO_COM_RESSALVA_OPERACIONAL

Horario de inicio:

    2026-07-06 21:37:58

Horario de fim:

    2026-07-06 21:50:42

Operador:

    Carlos Rubio

## 5. Falhas encontradas

Nenhuma falha visivel observada na abertura operacional minima.

## 6. Ressalvas

Nao houve smoke manual detalhado item a item. A conclusao registra somente abertura operacional minima da UI, sem problema visivel e sem alteracao funcional.

## 7. Evidencias

Relato do operador: sistema abriu normalmente, nenhuma alteracao ou problema visivel observado.

## 8. Decisao de continuidade

Frente Terminal VWAP UI considerada concluida nesta etapa de auditoria e validacao operacional minima. Nao houve patch funcional.

## 9. Observacao de controle

Este registro foi criado antes da execucao manual.

A execucao manual detalhada nao foi realizada por decisao operacional. Foi registrada validacao minima de abertura da UI sem problema visivel.

Nao houve alteracao funcional nesta etapa.
