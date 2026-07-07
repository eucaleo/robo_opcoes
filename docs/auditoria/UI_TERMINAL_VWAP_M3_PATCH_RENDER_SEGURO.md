# M3.1 - Patch de renderizacao segura Terminal VWAP UI-only

Data: 2026-07-07 16:16:15

Branch: audit/ui-modern-terminal-vwap

HEAD base: 6f43081

## 1. Objetivo

Aplicar o primeiro patch real do M3 restrito no painel autorizado do Terminal VWAP Payoff.

O foco foi tornar a renderizacao mais defensiva contra dados parciais, ausentes ou malformados, sem alterar regra de negocio, controller, service, repository, banco, payoff ou janela moderna dark.

## 2. Arquivos alterados

Codigo autorizado:

    UI/components/terminal_vwap_payoff_panel.py

Testes autorizados:

    ATT/tests/test_terminal_vwap_payoff_panel_helpers.py

Documentacao autorizada:

    docs/auditoria/UI_TERMINAL_VWAP_M3_PATCH_RENDER_SEGURO.md

## 3. Alteracoes principais

Foram adicionados helpers defensivos de UI:

    _as_mapping
    _iter_mappings

Foram reforcadas as rotas de renderizacao/helper:

    _extract_leg_table_rows
    _extract_payoff_table_rows
    _summarize_viewmodel
    reload_structures
    load_selected_structure
    _render_structures
    render_viewmodel
    _render_payoff
    _render_warnings

## 4. Garantias de escopo

Este patch nao altera:

    banco
    schema
    query
    repository
    service
    controller
    app service
    viewmodel service
    payoff
    importador CSV
    painel dark Terminal VWAP
    janela moderna dark
    UIDataModel
    scripts
    tools

## 5. Estado Git antes do commit

Status:

    M UI/components/terminal_vwap_payoff_panel.py
    ?? ATT/tests/test_terminal_vwap_payoff_panel_helpers.py

Diff stat:

    UI/components/terminal_vwap_payoff_panel.py | 70 ++++++++++++++++++++++++-----
     1 file changed, 58 insertions(+), 12 deletions(-)

## 6. Classificacao

    M3_PATCH_RENDER_SEGURO
    UI_ONLY_RESTRITO
