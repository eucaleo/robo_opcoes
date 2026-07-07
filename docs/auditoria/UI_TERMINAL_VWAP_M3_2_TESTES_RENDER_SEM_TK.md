# M3.2 - Testes de renderizacao sem Tk real Terminal VWAP UI-only

Data: 2026-07-07 16:23:13

Branch: audit/ui-modern-terminal-vwap

HEAD base: 82cbae7

## 1. Objetivo

Adicionar cobertura de testes para os metodos de renderizacao do painel nativo Terminal VWAP Payoff sem abrir janela Tkinter, sem instanciar widgets reais e sem alterar codigo produtivo.

O foco foi validar que a camada de UI consegue renderizar ViewModel normalizado e entradas parciais usando objetos fake de arvore, texto e variavel.

## 2. Arquivos alterados

Testes autorizados:

    ATT/tests/test_terminal_vwap_payoff_panel_rendering.py

Documentacao autorizada:

    docs/auditoria/UI_TERMINAL_VWAP_M3_2_TESTES_RENDER_SEM_TK.md

## 3. Metodos cobertos

Foram cobertos testes sem Tk real para:

    render_viewmodel
    _render_structures
    _render_payoff
    _render_warnings
    _set_status

Tambem foram exercitados indiretamente:

    _render_legs
    _summarize_viewmodel
    _extract_leg_table_rows
    _extract_payoff_table_rows
    formatadores defensivos

## 4. Objetos fake usados

Os testes usam objetos simples em memoria:

    FakeVar
    FakeTree
    FakeText

Esses objetos simulam apenas a interface minima usada pelo painel.

## 5. Garantias de escopo

Este patch nao altera:

    codigo produtivo
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

## 6. Estado Git antes do commit

Status:

    ?? ATT/tests/test_terminal_vwap_payoff_panel_rendering.py

Diff stat:

    LIMPO

## 7. Classificacao

    M3_2_TESTES_RENDER_SEM_TK
    UI_ONLY_RESTRITO
    TESTS_ONLY
