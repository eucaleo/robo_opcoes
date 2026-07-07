# Escopo corrigido do M3 Terminal VWAP UI-only

Data de consolidacao: 2026-07-07 16:04:08

Branch auditada: audit/ui-modern-terminal-vwap

HEAD atual: c6eb642

## 1. Objetivo

Este documento corrige a lista automatica de arquivos aptos para o M3 Terminal VWAP UI-only.

A etapa anterior identificou 14 arquivos como aptos, mas a revisao manual mostrou que a classificacao automatica foi permissiva demais.

## 2. Estado Git

Branch:

audit/ui-modern-terminal-vwap

HEAD:

c6eb642

Status resumido:

LIMPO

Ultimos commits:

c6eb642 docs: classify terminal vwap m3 ui-only scope
104bf43 docs: inventory terminal vwap ui audit scope
f4faca0 docs: track macro ui audit strategy
bd08ff7 test: cover partial ui modern cli env precedence
3341dee test: document ui modern cli help options
a356a9b test: add ui modern cli invalid env fallback smoke
34a6e8d feat: honor ui modern launcher environment options
50fbf49 test: add ui modern cli help smoke
3ef66a5 test: add ui modern cli subprocess smoke
fedd676 test: add ui modern package entrypoint smoke
cf4e39c test: add ui modern launcher routing smoke
fafe28c test: add ui modern terminal vwap wiring smoke
ef7d17d docs: normalize decisions smoke record formatting
1e23db3 docs: record approved decisions ui smoke without backticks

## 3. Problema encontrado na classificacao automatica

A lista automatica incluiu arquivos em areas que nao devem ser alteradas no M3:

- `controllers/terminal_vwap_payoff_controller.py`
- `services/terminal_vwap_payoff_viewmodel_service.py`
- `scripts/*.sh`
- `tools/*.py`

Esses arquivos podem ser uteis como evidencia, mas nao devem ser modificados no primeiro pacote grande UI-only.

Tambem foi identificado que `UI/modern/dark_window.py`, apesar de ser arquivo de UI, importa componentes sensiveis para esta frente:

- `UI.components.terminal_vwap_payoff_dark_panel`
- `UI.models.ui_data`

Por isso, ele nao deve ser alterado no M3 sem uma reclassificacao especifica.

## 4. Arquivos explicitamente proibidos no M3

O M3 nao deve alterar:

- `infra/bootstrap_rtd_option_quotes_schema.py`
- `repositories/rtd_option_quotes_repository.py`
- `scripts/import_rtd_option_quotes_wide_csv.py`
- `UI/components/terminal_vwap_payoff_dark_panel.py`
- `UI/main_window.py`
- `UI/modern/main_window.py`
- `UI/modern/dark_window.py`
- `services/terminal_vwap_payoff_app_service.py`
- `services/terminal_vwap_payoff_viewmodel_service.py`
- `controllers/terminal_vwap_payoff_controller.py`
- `tools/audit_rtd_ui_flow.py`
- `tools/fix_structure_side_panel_patch.py`
- `tools/patch_structure_side_panel.py`
- `scripts/classificar_areas_ui.sh`
- `scripts/criar_registro_execucao_smoke_decisoes_ui.sh`
- `scripts/criar_smoke_manual_decisoes_ui.sh`
- `scripts/cruzar_matriz_areas_ui.sh`
- `scripts/documentar_matriz_equivalencia_ui.sh`
- `scripts/documentar_pendencias_ui.sh`
- `scripts/documentar_pendencias_ui_safe.sh`
- `scripts/inventariar_arquivos_ui.sh`

## 5. Whitelist corrigida para o M3

O M3 pode alterar codigo apenas em:

- `UI/components/terminal_vwap_payoff_panel.py`

O M3 pode criar ou alterar testes apenas em:

- `ATT/tests/`

O M3 pode criar documentacao de controle apenas em:

- `docs/auditoria/`

## 6. Escopo permitido no M3

O M3 pode atuar em:

- comportamento visual do painel Terminal VWAP legado/isolado;
- estado vazio;
- mensagem de status;
- fallback visual;
- renderizacao segura quando nao houver estruturas;
- renderizacao segura quando houver dados parciais;
- testes automatizados dos helpers e renderizadores seguros;
- documentacao da execucao.

## 7. Escopo proibido no M3

O M3 nao pode atuar em:

- banco;
- schema;
- pipeline;
- query;
- repository;
- service;
- controller;
- payoff;
- UIDataModel;
- janela moderna dark;
- painel dark Terminal VWAP;
- importador CSV;
- scripts de patch;
- ferramentas de auditoria.

## 8. Decisao operacional

A proxima etapa sera o M3 com escopo restrito.

Arquivos de codigo autorizados:

- `UI/components/terminal_vwap_payoff_panel.py`

Arquivos de teste autorizados:

- `ATT/tests/`

Qualquer necessidade de alterar `UI/modern/dark_window.py` ou `UI/components/terminal_vwap_payoff_dark_panel.py` deve parar o M3 e abrir nova reclassificacao.

Classificacao:

AUDITORIA_TERMINAL_VWAP

ESCOPO_M3_CORRIGIDO

UI_ONLY_RESTRITO
