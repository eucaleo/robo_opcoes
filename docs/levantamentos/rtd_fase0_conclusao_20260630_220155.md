# Conclusão Fase 0 RTD Excel Vivo

Atualizado em: 20260630_220155

## Arquivos analisados

    docs/levantamentos/rtd_fase0_mapa_bancos_20260630_215847.txt
    docs/levantamentos/rtd_fase0_mapa_excel_subprocess_20260630_215903.txt
    docs/levantamentos/rtd_fase0_arquivos_candidatos_20260630_215918.txt
    docs/levantamentos/rtd_fase0_sqlite_tabelas_20260630_215939.txt

## Contagens principais

Referências a derived.db:
211

Referências a app.db:
349

Referências a rtd_option_quotes:
918

Referências a rtd_underlying_quotes:
17

Referências a subprocess:
39

Referências a LISTA_RTD:
91

## Tabelas SQLite

================================================================================
DB: dados\app.db
EXISTS: True

TABLES:
  pricing_executions
  rtd_option_quotes
  rtd_option_quotes_backup_scope_20260626_184057
  rtd_underlying_quotes
  sqlite_sequence
  structure_audit_log
  structure_events
  structure_leg_snapshots
  structure_legs
  structure_snapshots
  structures

TABLES OF INTEREST:
  rtd_option_quotes: YES
    count: 11
    columns:
      (0, 'id', 'INTEGER', 0, None, 1)
      (1, 'codigo_opcao', 'TEXT', 1, None, 0)
      (2, 'ativo_base', 'TEXT', 0, None, 0)
      (3, 'call_put', 'TEXT', 0, None, 0)
      (4, 'strike', 'REAL', 0, None, 0)
      (5, 'vencimento', 'TEXT', 0, None, 0)
      (6, 'ultimo_preco', 'REAL', 0, None, 0)
      (7, 'ultima_quantidade', 'REAL', 0, None, 0)
      (8, 'bid', 'REAL', 0, None, 0)
      (9, 'ask', 'REAL', 0, None, 0)
      (10, 'volume', 'REAL', 0, None, 0)
      (11, 'iv', 'REAL', 0, None, 0)
      (12, 'delta', 'REAL', 0, None, 0)
      (13, 'gamma', 'REAL', 0, None, 0)
      (14, 'theta', 'REAL', 0, None, 0)
      (15, 'vega', 'REAL', 0, None, 0)
      (16, 'source', 'TEXT', 1, "'rtd_links'", 0)
      (17, 'raw_json', 'TEXT', 0, None, 0)
      (18, 'updated_at', 'TEXT', 1, 'CURRENT_TIMESTAMP', 0)
      (19, 'created_at', 'TEXT', 1, 'CURRENT_TIMESTAMP', 0)
      (20, 'vwap', 'REAL', 0, None, 0)
  rtd_underlying_quotes: YES
    count: 2
    columns:
      (0, 'id', 'INTEGER', 0, None, 1)
      (1, 'ativo', 'TEXT', 1, None, 0)
      (2, 'ultimo_preco', 'REAL', 0, None, 0)
      (3, 'bid', 'REAL', 0, None, 0)
      (4, 'ask', 'REAL', 0, None, 0)
      (5, 'close_price', 'REAL', 0, None, 0)
      (6, 'prev_close', 'REAL', 0, None, 0)
      (7, 'open_price', 'REAL', 0, None, 0)
      (8, 'high_price', 'REAL', 0, None, 0)
      (9, 'low_price', 'REAL', 0, None, 0)
      (10, 'volume', 'REAL', 0, None, 0)
      (11, 'change_percent', 'REAL', 0, None, 0)
      (12, 'source', 'TEXT', 0, None, 0)
      (13, 'updated_at', 'TEXT', 0, None, 0)
      (14, 'created_at', 'TEXT', 0, None, 0)
      (15, 'vwap', 'REAL', 0, None, 0)
      (16, 'raw_json', 'TEXT', 0, None, 0)
================================================================================
DB: dados\derived.db
EXISTS: True

TABLES:
  payoff_curve_points
  pricing_executions
  rtd_option_quotes
  rtd_underlying_quotes
  sqlite_sequence
  structure_audit_log
  structure_decisions
  structure_leg_snapshots
  structure_legs
  structure_snapshots
  structures

TABLES OF INTEREST:
  rtd_option_quotes: YES
    count: 11
    columns:
      (0, 'id', 'INTEGER', 0, None, 1)
      (1, 'codigo_opcao', 'TEXT', 1, None, 0)
      (2, 'ativo_base', 'TEXT', 0, None, 0)
      (3, 'call_put', 'TEXT', 0, None, 0)
      (4, 'strike', 'REAL', 0, None, 0)
      (5, 'vencimento', 'TEXT', 0, None, 0)
      (6, 'ultimo_preco', 'REAL', 0, None, 0)
      (7, 'ultima_quantidade', 'REAL', 0, None, 0)
      (8, 'bid', 'REAL', 0, None, 0)
      (9, 'ask', 'REAL', 0, None, 0)
      (10, 'volume', 'REAL', 0, None, 0)
      (11, 'iv', 'REAL', 0, None, 0)
      (12, 'delta', 'REAL', 0, None, 0)
      (13, 'gamma', 'REAL', 0, None, 0)
      (14, 'theta', 'REAL', 0, None, 0)
      (15, 'vega', 'REAL', 0, None, 0)
      (16, 'source', 'TEXT', 1, "'rtd_links'", 0)
      (17, 'raw_json', 'TEXT', 0, None, 0)
      (18, 'updated_at', 'TEXT', 1, 'CURRENT_TIMESTAMP', 0)
      (19, 'created_at', 'TEXT', 1, 'CURRENT_TIMESTAMP', 0)
      (20, 'vwap', 'REAL', 0, None, 0)
  rtd_underlying_quotes: YES
    count: 2
    columns:
      (0, 'id', 'INTEGER', 0, None, 1)
      (1, 'ativo', 'TEXT', 1, None, 0)
      (2, 'ultimo_preco', 'REAL', 0, None, 0)
      (3, 'bid', 'REAL', 0, None, 0)
      (4, 'ask', 'REAL', 0, None, 0)
      (5, 'vwap', 'REAL', 0, None, 0)
      (6, 'volume', 'REAL', 0, None, 0)
      (7, 'source', 'TEXT', 0, None, 0)
      (8, 'raw_json', 'TEXT', 0, None, 0)
      (9, 'updated_at', 'TEXT', 0, None, 0)
      (10, 'created_at', 'TEXT', 0, None, 0)
      (11, 'close_price', 'REAL', 0, None, 0)
      (12, 'prev_close', 'REAL', 0, None, 0)
      (13, 'open_price', 'REAL', 0, None, 0)
      (14, 'high_price', 'REAL', 0, None, 0)
      (15, 'low_price', 'REAL', 0, None, 0)
      (16, 'change_percent', 'REAL', 0, None, 0)

## Arquivos com mais ocorrências no mapa de bancos

    174 docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt
     74 docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt
     57 docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt
     50 docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt
     47 docs/checkpoints/evidencias/fase-2a-grep-strike.txt
     42 docs/AUDITORIA_RTD_EXCEL_VIVO.md
     39 docs/checkpoints/evidencias/fase-6-11-mapa-impacto-integracao-rtd-option-quotes-pricing-runtime.txt
     34 docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt
     31 docs/checkpoints/evidencias/fase-6-7-inventario-diagnostico-rtd-canonical.txt
     29 docs/checkpoints/evidencias/fase-1-indice-trechos-runtime.txt
     28 docs/checkpoints/evidencias/fase-1-trechos-rtd-runtime.txt
     27 docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_db_path.from-bcb6ddb.py.txt
     27 docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_db_path_from_bcb6ddb.py.txt
     25 docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt
     24 docs/ARQUITETURA_BANCOS.md
     21 docs/PLANO_RTD_EXCEL_VIVO.md
     21 ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py
     20 docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md
     19 ATT/tests/test_rtd_live_db_guardrail.py
     18 docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt
     16 docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md
     15 tools/audit_rtd_ui_flow.py
     15 UI/components/details_panel.py
     14 docs/ROTA_DESENVOLVIMENTO.md
     13 scripts/rtd_mapa_alvos_fase0.py
     13 docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md
     13 docs/checkpoints/fase-6-11-retomada-funcional-pos-restauracao-documental.md
     13 docs/checkpoints/evidencias/fase-2a-grep-strike-python-focado.txt
     13 docs/checkpoints/evidencias/fase-2a-grep-editor-dialog.txt
     13 docs/checkpoints/evidencias/fase-1-mapa-strike-codigo-atual.txt
     13 docs/AUDITORIA_DESENVOLVIMENTO.md
     13 ATT/tests/test_market_snapshot_selector.py
     12 scripts/rtd_reconciliar_app_para_derived.py
     12 scripts/refresh_rtd_symbol_to_option_quotes.py
     12 docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
     12 docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_execute_pricing_rtd_integration.from-b492f16.py.txt
     12 docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_execute_pricing_rtd_integration_from_b492f16.py.txt
     12 docs/auditoria_rtd_nova_ui_bovak900.md
     11 repositories/market_snapshot_repository.py
     11 docs/evolucoes de fases/executed_v1.md
     11 docs/checkpoints/evidencias/fase-6-11-mapa-runtime-leitura-rtd-pricing.txt
     10 docs/evolucoes de fases/baseline_v1a.md
     10 docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt
     10 docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt
     10 docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt
      9 infra/bootstrap_rtd_option_quotes_schema.py
      9 docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md
      9 docs/checkpoints/evidencias/fase-6-11-simbolos-atuais-rtd-pricing.txt
      8 scripts/validate_derived_db.py
      8 scripts/rtd_consulta_projeto.sh
      8 repositories/rtd_option_quotes_repository.py
      8 docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md
      7 scripts/import_rtd_option_quotes_wide_csv.py
      7 docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md
      7 docs/checkpoints/evidencias/rtd_historico_preview/test_pricing_execution_price_source_persistence.from-d3a9dcc.py.txt
      7 docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_pricing_execution_price_source_persistence_from_d3a9dcc.py.txt
      7 docs/INDICE_DOCUMENTACAO.md
      7 ATT/tests/test_canonical_pricing_facade.py
      6 services/market_snapshot_selector.py
      6 services/canonical_pricing_facade.py
      6 docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_price_resolution.from-0c7e123.py.txt
      6 docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_price_resolution_from_0c7e123.py.txt
      6 UI/components/terminal_vwap_payoff_dark_panel.py
      6 UI/components/structure_editor_dialog.py
      5 scripts/repair_derived_db_consistency.py
      5 scripts/check_rota_desenvolvimento.py
      5 docs/validacoes/fase-17-mapa-pastas-arquivos.md
      5 docs/evolucoes de fases/roteiro_v2.md
      5 docs/evolucoes de fases/FASE_6_CAMADA_CANONICA_LEITURA.md
      5 docs/checkpoints/evidencias/fase-9-encerramento-enriquecimento-legs-rtd-e-position-side.md
      5 docs/checkpoints/evidencias/fase-6-11-matriz-compatibilidade-testes-rtd-historicos.txt
      5 docs/checkpoints/evidencias/fase-1-mapa-strike-runtime-codigo-atual.txt
      5 ATT/tests/test_system_snapshots_repository.py
      5 ATT/tests/test_robo_legs_repository.py
      4 services/structure_leg_rtd_enrichment_service.py
      4 docs/checkpoints/evidencias/fase-8-mapa-impacto-cadastro-estruturas-leg-minima.txt
      4 docs/checkpoints/evidencias/fase-6-11-evidencia-guardrails-rtd-option-quotes-repository.txt
      3 scripts/rtd_importar_underlying_csv.py
      3 scripts/rtd_enriquecer_underlying_csv.py
      3 scripts/purge_derived_snapshots.py

## Arquivos com mais ocorrências no mapa Excel/subprocess

     87 docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md
     43 docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt
     35 docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md
     32 docs/auditoria_ui_terminal_vwap_payoff.md
     27 docs/ui_terminal_vwap_payoff_plano.md
     26 scripts/refresh_rtd_symbol_to_option_quotes.py
     24 docs/PLANO_RTD_EXCEL_VIVO.md
     23 docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt
     21 scripts/rtd_auditoria_fase0.sh
     18 docs/evolucoes de fases/baseline_v1.md
     18 docs/AUDITORIA_RTD_EXCEL_VIVO.md
     16 docs/validacoes/fase-17-mapa-pastas-arquivos.md
     15 ATT/checks/check_legs.py
     14 docs/evolucoes de fases/baseline_v1a.md
     14 bridge_ingest_csv.py
     13 scripts/import_rtd_option_quotes_wide_csv.py
     12 scripts/rtd_importar_underlying_csv.py
     12 docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md
     11 scripts/rtd_enriquecer_underlying_csv.py
     11 docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
     11 docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md
     11 docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md
     10 scripts/rtd_mapa_alvos_fase0.py
      9 scripts/refresh_rtd_option_quotes_excel.ps1
      9 docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt
      9 docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt
      9 ATT/checks/check_api_routes.py
      8 tools/audit_rtd_ui_flow.py
      8 docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md
      8 docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt
      8 docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt
      7 scripts/check_rota_desenvolvimento.py
      7 docs/ROTA_DESENVOLVIMENTO.md
      7 ATT/checks/check_cleanup_residuals.py
      6 docs/evolucoes de fases/FASE_6_CAMADA_CANONICA_LEITURA.md
      6 docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt
      4 utils/leg_normalizers.py
      4 mapear_repositorio.sh
      4 docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt
      4 docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt
      4 docs/auditoria_rtd_nova_ui_bovak900.md
      4 docs/INDICE_DOCUMENTACAO.md
      4 UI/models/ui_data.py
      4 UI/components/structure_editor_dialog.py
      4 ATT/checks/check_structures.py
      4 .gitignore
      3 scripts/rtd_consulta_projeto.sh
      3 docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md
      3 ATT/checks/check_end_to_end.py
      2 services/terminal_vwap_payoff_app_service.py
      2 scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
      2 docs/evolucoes de fases/executed_v1.md
      2 docs/evolucoes de fases/auditoria_fase_9_cadastro_estruturas.md
      2 docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md
      2 ATT/checks/run_all_checks.py
      1 services/terminal_vwap_payoff_viewmodel_service.py
      1 docs/evolucoes de fases/roteiro_v2.md
      1 docs/evolucoes de fases/baseline_v2.md
      1 docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md
      1 docs/evolucoes de fases/FASE_7_ISOLAMENTO_NOMES_FISICOS_LEGADOS.md
      1 docs/evolucoes de fases/DB_PATHS.md
      1 docs/evolucoes de fases/AUDITORIA_FASE_11_SNAPSHOTS_HISTORICO.md
      1 docs/checkpoints/fase-6-11-retomada-funcional-pos-restauracao-documental.md
      1 docs/checkpoints/evidencias/fase-9-encerramento-enriquecimento-legs-rtd-e-position-side.md
      1 docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt
      1 docs/checkpoints/evidencias/fase-2a-grep-strike.txt
      1 docs/checkpoints/evidencias/fase-1-trechos-atualizar-dados-runtime.txt
      1 docs/checkpoints/alteracoes/fase-6-11-autoalteracao-ajuste-enquadramento-em-documento-existente.txt
      1 docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md
      1 docs/AUDITORIA_DESENVOLVIMENTO.md
      1 db/import_excel.py
      1 controllers/terminal_vwap_payoff_controller.py
      1 UI/components/details_panel.py
      1 ATT/tests/test_rtd_live_db_guardrail.py

## Ocorrências críticas envolvendo derived.db e RTD

186:docs/AUDITORIA_RTD_EXCEL_VIVO.md:70:    dados/derived.db:rtd_option_quotes
264:docs/auditoria_rtd_nova_ui_bovak900.md:23:    - rtd_option_quotes existe em dados/derived.db.
705:docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt:89:Os registros funcionais de rtd_option_quotes estão equivalentes entre dados/app.db e dados/derived.db.
710:docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt:148:No estado atual, rtd_option_quotes existe em dados/app.db e dados/derived.db, com 4 registros funcionais equivalentes oriundos de BTG_RTD_EXCEL.
1140:docs/checkpoints/fase-6-11-retomada-funcional-pos-restauracao-documental.md:137:- `rtd_option_quotes` existe em `dados/app.db` e `dados/derived.db`.
1371:scripts/rtd_reconciliar_app_para_derived.py:48:    print("Reconciliando app.db:rtd_option_quotes -> derived.db:rtd_option_quotes")

## Ocorrências envolvendo app.db e RTD

22:ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:118:    db_path = tmp_path / "app.db"
29:ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:208:    db_path = tmp_path / "app.db"
33:ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:288:    db_path = tmp_path / "app.db"
36:ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:312:    db_path = tmp_path / "app.db"
72:ATT/tests/test_rtd_live_db_guardrail.py:58:    O repositório operacional de rtd_option_quotes deve apontar por padrão para dados/app.db.
146:docs/ARQUITETURA_BANCOS.md:53:    dados/app.db.rtd_option_quotes
147:docs/ARQUITETURA_BANCOS.md:54:    dados/app.db.rtd_underlying_quotes
177:docs/AUDITORIA_RTD_EXCEL_VIVO.md:28:    rtd_option_quotes -> dados/app.db
178:docs/AUDITORIA_RTD_EXCEL_VIVO.md:29:    rtd_underlying_quotes -> dados/app.db
187:docs/AUDITORIA_RTD_EXCEL_VIVO.md:76:    dados/app.db:rtd_option_quotes é a fonte operacional de opções RTD
188:docs/AUDITORIA_RTD_EXCEL_VIVO.md:77:    dados/app.db:rtd_underlying_quotes é a fonte operacional de underlyings RTD
192:docs/AUDITORIA_RTD_EXCEL_VIVO.md:96:    rtd_option_quotes pertence operacionalmente a dados/app.db
193:docs/AUDITORIA_RTD_EXCEL_VIVO.md:97:    rtd_underlying_quotes pertence operacionalmente a dados/app.db
197:docs/AUDITORIA_RTD_EXCEL_VIVO.md:111:    confirmar existência operacional de rtd_option_quotes em app.db
198:docs/AUDITORIA_RTD_EXCEL_VIVO.md:112:    confirmar existência operacional de rtd_underlying_quotes em app.db
203:docs/AUDITORIA_RTD_EXCEL_VIVO.md:128:    verificar presença de rtd_option_quotes -> dados/app.db
204:docs/AUDITORIA_RTD_EXCEL_VIVO.md:129:    verificar presença de rtd_underlying_quotes -> dados/app.db
214:docs/AUDITORIA_RTD_EXCEL_VIVO.md:311:    validação de presença da decisão rtd_option_quotes -> app.db
215:docs/AUDITORIA_RTD_EXCEL_VIVO.md:312:    validação de presença da decisão rtd_underlying_quotes -> app.db
227:docs/PLANO_RTD_EXCEL_VIVO.md:42:    dados/app.db.rtd_option_quotes
228:docs/PLANO_RTD_EXCEL_VIVO.md:43:    dados/app.db.rtd_underlying_quotes
230:docs/PLANO_RTD_EXCEL_VIVO.md:51:    rtd_option_quotes -> app.db
231:docs/PLANO_RTD_EXCEL_VIVO.md:52:    rtd_underlying_quotes -> app.db
249:docs/ROTA_DESENVOLVIMENTO.md:51:    rtd_option_quotes disponível em app.db
250:docs/ROTA_DESENVOLVIMENTO.md:52:    rtd_underlying_quotes disponível em app.db
263:docs/auditoria_rtd_nova_ui_bovak900.md:22:    - rtd_option_quotes existe em dados/app.db.
523:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:2292:./repositories/rtd_option_quotes_repository.py:18:    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
705:docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt:89:Os registros funcionais de rtd_option_quotes estão equivalentes entre dados/app.db e dados/derived.db.
710:docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt:148:No estado atual, rtd_option_quotes existe em dados/app.db e dados/derived.db, com 4 registros funcionais equivalentes oriundos de BTG_RTD_EXCEL.
825:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1530:docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:501:- fonte atual: app.db, rtd_option_quotes, rtd_analise_robo_legs e provider temporário
1140:docs/checkpoints/fase-6-11-retomada-funcional-pos-restauracao-documental.md:137:- `rtd_option_quotes` existe em `dados/app.db` e `dados/derived.db`.
1164:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:541:    python scripts/audit_rtd_option_quotes.py --db dados/app.db
1185:docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:501:- fonte atual: app.db, rtd_option_quotes, rtd_analise_robo_legs e provider temporário
1205:docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:17:rtd_option_quotes: ausente em dados/app.db
1273:infra/bootstrap_rtd_option_quotes_schema.py:136:        default="dados/app.db",
1274:infra/bootstrap_rtd_option_quotes_schema.py:137:        help="Caminho do banco SQLite. Padrão: dados/app.db",
1296:repositories/rtd_option_quotes_repository.py:18:    - dados/app.db: dados persistentes da aplicacao/estruturas
1297:repositories/rtd_option_quotes_repository.py:19:    - dados/app.db: cache RTD operacional
1298:repositories/rtd_option_quotes_repository.py:22:    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
1371:scripts/rtd_reconciliar_app_para_derived.py:48:    print("Reconciliando app.db:rtd_option_quotes -> derived.db:rtd_option_quotes")

## Ocorrências relevantes de subprocesso, Excel e PowerShell

1:.gitignore:9:# Excel local / arquivos operacionais
2:.gitignore:12:LISTA_RTD.xlsx
3:.gitignore:15:bridge/*.csv
4:.gitignore:99:LISTA_RTD.xlsm
5:ATT/checks/check_api_routes.py:6:    import win32com.client
6:ATT/checks/check_api_routes.py:8:    win32com = None
7:ATT/checks/check_api_routes.py:33:        log("INFO", "Iniciando check local do runtime Excel")
8:ATT/checks/check_api_routes.py:35:        if win32com is None:
9:ATT/checks/check_api_routes.py:41:        excel = win32com.client.Dispatch("Excel.Application")
10:ATT/checks/check_api_routes.py:43:        log("OK", "Excel COM iniciado com sucesso")
11:ATT/checks/check_api_routes.py:45:        wb = excel.Workbooks.Open(str(workbook_path))
12:ATT/checks/check_api_routes.py:61:        log("OK", "Check de Excel local concluído com sucesso")
13:ATT/checks/check_api_routes.py:65:        log("FAIL", f"Erro no check de Excel local: {e}")
14:ATT/checks/check_cleanup_residuals.py:2:import subprocess
15:ATT/checks/check_cleanup_residuals.py:89:    result = subprocess.run(
16:ATT/checks/check_cleanup_residuals.py:93:        stdout=subprocess.PIPE,
17:ATT/checks/check_cleanup_residuals.py:94:        stderr=subprocess.PIPE,
18:ATT/checks/check_cleanup_residuals.py:108:    result = subprocess.run(
19:ATT/checks/check_cleanup_residuals.py:112:        stdout=subprocess.PIPE,
20:ATT/checks/check_cleanup_residuals.py:113:        stderr=subprocess.PIPE,
21:ATT/checks/check_end_to_end.py:15:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
22:ATT/checks/check_end_to_end.py:16:    ROOT_DIR / "bridge" / "analise_robo.csv",
23:ATT/checks/check_end_to_end.py:17:    ROOT_DIR / "bridge" / "analise_raiox.csv",
24:ATT/checks/check_legs.py:2:import csv
25:ATT/checks/check_legs.py:12:    BRIDGE_DIR / "analise_robo_legs.csv",
26:ATT/checks/check_legs.py:13:    BRIDGE_DIR / "analise_robo.csv",
27:ATT/checks/check_legs.py:14:    BRIDGE_DIR / "analise_raiox.csv",
28:ATT/checks/check_legs.py:34:def read_csv_rows(path: Path):
29:ATT/checks/check_legs.py:39:        dialect = csv.Sniffer().sniff(sample, delimiters=";,")
30:ATT/checks/check_legs.py:41:        rows = list(csv.reader(StringIO(text), dialect))
31:ATT/checks/check_legs.py:42:    except csv.Error:
32:ATT/checks/check_legs.py:45:        rows = list(csv.reader(StringIO(text), delimiter=delimiter))
33:ATT/checks/check_legs.py:50:def validate_csv(path: Path) -> None:
34:ATT/checks/check_legs.py:51:    rows, delimiter, encoding = read_csv_rows(path)
35:ATT/checks/check_legs.py:73:        found_csv = False
36:ATT/checks/check_legs.py:76:                validate_csv(path)
37:ATT/checks/check_legs.py:77:                found_csv = True
38:ATT/checks/check_legs.py:79:        if not found_csv:
39:ATT/checks/check_structures.py:15:    ROOT_DIR / "bridge" / "analise_robo.csv",
40:ATT/checks/check_structures.py:16:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
41:ATT/checks/check_structures.py:17:    ROOT_DIR / "bridge" / "configurações.csv",
42:ATT/checks/check_structures.py:18:    ROOT_DIR / "bridge" / "consolidações.csv",
43:ATT/checks/run_all_checks.py:2:import subprocess
44:ATT/checks/run_all_checks.py:26:        result = subprocess.run([sys.executable, str(script_path)], cwd=str(CHECKS_DIR.parent))
45:ATT/tests/test_rtd_live_db_guardrail.py:14:    "scripts/import_rtd_option_quotes_wide_csv.py",
46:UI/components/details_panel.py:735:        """Chamado pelo MainWindow ao finalizar o subprocess do pipeline."""
47:UI/components/structure_editor_dialog.py:4:import subprocess
48:UI/components/structure_editor_dialog.py:412:        """Atualiza uma opcao via RTD/Excel e grava o cache em dados/app.db."""
49:UI/components/structure_editor_dialog.py:438:            completed = subprocess.run(
50:UI/components/structure_editor_dialog.py:448:        except subprocess.TimeoutExpired:
51:UI/models/ui_data.py:11:import csv
52:UI/models/ui_data.py:600:    def export_to_csv(self, data: List[Dict], filename: str):
53:UI/models/ui_data.py:608:                w = csv.DictWriter(f, fieldnames=headers)
54:UI/models/ui_data.py:614:            w = csv.DictWriter(f, fieldnames=headers)
55:bridge_ingest_csv.py:1:#bridge_ingest_csv.py
56:bridge_ingest_csv.py:6:import subprocess
57:bridge_ingest_csv.py:33:    CsvSpec("analise_raiox.csv",          "rtd_analise_raiox",          "replace"),
58:bridge_ingest_csv.py:34:    CsvSpec("consolidacoes.csv",           "rtd_consolidacoes",           "replace"),
59:bridge_ingest_csv.py:35:    CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),
60:bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),
61:bridge_ingest_csv.py:37:    CsvSpec("configuracoes.csv",           "rtd_configuracoes",           "replace"),
62:bridge_ingest_csv.py:39:    CsvSpec("rolls_detectados.csv",        "rtd_rolls_detectados",        "append"),
63:bridge_ingest_csv.py:40:    CsvSpec("hist_robo.csv",               "rtd_hist_robo",               "append"),
64:bridge_ingest_csv.py:41:    CsvSpec("encerramentos_manuais.csv",   "rtd_encerramentos_manuais",   "append"),
65:bridge_ingest_csv.py:75:    p = subprocess.run(cmd, cwd=str(PROJECT_DIR), capture_output=True, text=True)
66:bridge_ingest_csv.py:89:        df = pd.read_csv(
67:bridge_ingest_csv.py:106:def read_csv(path: Path) -> pd.DataFrame:
68:bridge_ingest_csv.py:203:            df = read_csv(path)
69:controllers/terminal_vwap_payoff_controller.py:9:- não acessar Excel, RTD bruto, CSV antigo ou arquivos operacionais.
70:db/import_excel.py:71:    # drop colunas lixo do Excel
71:docs/AUDITORIA_DESENVOLVIMENTO.md:84:    implementar detecção do Excel LISTA_RTD.xlsm aberto
72:docs/AUDITORIA_RTD_EXCEL_VIVO.md:1:# Auditoria RTD Excel Vivo
73:docs/AUDITORIA_RTD_EXCEL_VIVO.md:7:Acompanhar a implementação da arquitetura RTD sempre online com Excel aberto, app.db como fonte oficial de mercado vivo e derived.db restrito a resultados derivados e artefatos regeneráveis.
74:docs/AUDITORIA_RTD_EXCEL_VIVO.md:44:    LISTA_RTD.xlsm permanece aberto como antena RTD viva
75:docs/AUDITORIA_RTD_EXCEL_VIVO.md:45:    coletor Python observa o Excel e atualiza app.db
76:docs/AUDITORIA_RTD_EXCEL_VIVO.md:93:    LISTA_RTD.xlsm deve existir na raiz e permanecer aberto durante a operação
77:docs/AUDITORIA_RTD_EXCEL_VIVO.md:94:    fluxo antigo sob demanda via subprocess, PowerShell, Excel COM, CSV e import SQLite deixa de ser fluxo principal
78:docs/AUDITORIA_RTD_EXCEL_VIVO.md:99:    Terminal VWAP Payoff não deve acessar Excel diretamente
79:docs/AUDITORIA_RTD_EXCEL_VIVO.md:101:    subprocessos podem permanecer apenas para manutenção, diagnóstico, importação emergencial ou recuperação operacional
80:docs/AUDITORIA_RTD_EXCEL_VIVO.md:106:    confirmar manualmente Excel aberto
81:docs/AUDITORIA_RTD_EXCEL_VIVO.md:108:    confirmar LISTA_RTD.xlsm aberto
82:docs/AUDITORIA_RTD_EXCEL_VIVO.md:145:    manter LISTA_RTD.xlsm aberto
83:docs/AUDITORIA_RTD_EXCEL_VIVO.md:146:    detectar Excel aberto
84:docs/AUDITORIA_RTD_EXCEL_VIVO.md:150:    eliminar subprocesso para preencher leg
85:docs/AUDITORIA_RTD_EXCEL_VIVO.md:154:    sistema lê dados vivos do Excel
86:docs/AUDITORIA_RTD_EXCEL_VIVO.md:157:    preenchimento de leg usa snapshot, não subprocesso por símbolo
87:docs/AUDITORIA_RTD_EXCEL_VIVO.md:281:Correção documental para alinhar a auditoria com o PDF de arquitetura RTD Excel Vivo.
88:docs/AUDITORIA_RTD_EXCEL_VIVO.md:300:    validar operacionalmente Excel aberto
89:docs/AUDITORIA_RTD_EXCEL_VIVO.md:302:    validar LISTA_RTD.xlsm aberto
90:docs/INDICE_DOCUMENTACAO.md:7:### Plano RTD Excel Vivo
91:docs/INDICE_DOCUMENTACAO.md:15:    descreve a arquitetura alvo com Excel LISTA_RTD.xlsm aberto, coletor Python online, snapshot em app.db, histórico intraday, candles, VWAP e UI operacional viva
92:docs/INDICE_DOCUMENTACAO.md:57:Excel RTD vivo:
93:docs/INDICE_DOCUMENTACAO.md:59:    LISTA_RTD.xlsm
94:docs/PLANO_RTD_EXCEL_VIVO.md:1:# Plano RTD Excel Vivo
95:docs/PLANO_RTD_EXCEL_VIVO.md:7:Este documento define a rota oficial para transformar o RTD em uma fonte viva de dados para o sistema, mantendo o Excel LISTA_RTD.xlsm aberto durante a operação e usando o banco correto para cada tipo de informação.
96:docs/PLANO_RTD_EXCEL_VIVO.md:73:## Papel do Excel LISTA_RTD.xlsm
97:docs/PLANO_RTD_EXCEL_VIVO.md:75:O Excel LISTA_RTD.xlsm deve permanecer aberto junto com o sistema durante o uso operacional.
98:docs/PLANO_RTD_EXCEL_VIVO.md:80:    Excel recebe os dados em tempo quase real
99:docs/PLANO_RTD_EXCEL_VIVO.md:81:    Excel mantém uma tabela viva de símbolos monitorados
100:docs/PLANO_RTD_EXCEL_VIVO.md:82:    coletor Python observa o Excel
101:docs/PLANO_RTD_EXCEL_VIVO.md:89:O sistema não deve depender de subprocesso para consultar uma opção individual sob demanda.
102:docs/PLANO_RTD_EXCEL_VIVO.md:91:O botão de preenchimento por RTD deve ler o último estado conhecido no snapshot, e não abrir Excel, salvar CSV ou chamar script externo para cada símbolo.
103:docs/PLANO_RTD_EXCEL_VIVO.md:100:    Excel LISTA_RTD.xlsm
104:docs/PLANO_RTD_EXCEL_VIVO.md:106:        detecta Excel aberto
105:docs/PLANO_RTD_EXCEL_VIVO.md:265:    Excel aberto
106:docs/PLANO_RTD_EXCEL_VIVO.md:276:Excel pode virar gargalo.
107:docs/PLANO_RTD_EXCEL_VIVO.md:322:    abrir LISTA_RTD.xlsm
108:docs/PLANO_RTD_EXCEL_VIVO.md:327:    verificar se o Excel está aberto
109:docs/PLANO_RTD_EXCEL_VIVO.md:337:    RTD atualiza Excel
110:docs/PLANO_RTD_EXCEL_VIVO.md:357:    manter LISTA_RTD.xlsm aberto
111:docs/PLANO_RTD_EXCEL_VIVO.md:358:    detectar Excel aberto
112:docs/PLANO_RTD_EXCEL_VIVO.md:362:    eliminar subprocesso para preencher leg
113:docs/PLANO_RTD_EXCEL_VIVO.md:366:    ter o sistema lendo dados vivos do Excel
114:docs/PLANO_RTD_EXCEL_VIVO.md:463:    Excel aberto o tempo todo como receptor RTD
115:docs/PLANO_RTD_EXCEL_VIVO.md:470:    nada de subprocesso para consultar opção individual
116:docs/PLANO_RTD_EXCEL_VIVO.md:471:    subprocessos apenas para manutenção, importação ou recuperação emergencial
117:docs/PLANO_RTD_EXCEL_VIVO.md:477:    menos subprocessos
118:docs/ROTA_DESENVOLVIMENTO.md:17:Excel operacional:
119:docs/ROTA_DESENVOLVIMENTO.md:19:    LISTA_RTD.xlsm aberto durante o uso do sistema
120:docs/ROTA_DESENVOLVIMENTO.md:73:### Marco 4: Excel RTD vivo
121:docs/ROTA_DESENVOLVIMENTO.md:77:    manter LISTA_RTD.xlsm aberto
122:docs/ROTA_DESENVOLVIMENTO.md:78:    detectar Excel aberto
123:docs/ROTA_DESENVOLVIMENTO.md:85:    sistema detecta Excel
124:docs/ROTA_DESENVOLVIMENTO.md:102:    subprocesso por opção deixa de ser caminho principal
125:docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md:25:•	Excel é apenas ponte RTD.
126:docs/auditoria_rtd_nova_ui_bovak900.md:14:    - O Excel/RTD atua apenas como ponte dinamica.
127:docs/auditoria_rtd_nova_ui_bovak900.md:39:A nova UI consulta o cache rtd_option_quotes, mas nao aciona antes a ponte RTD/Excel para hidratar o ticker solicitado.
128:docs/auditoria_rtd_nova_ui_bovak900.md:51:        -> solicitar ou hidratar ticker na ponte RTD/Excel
129:docs/auditoria_rtd_nova_ui_bovak900.md:64:Significa que BOVAK900 ainda nao foi persistido no banco consultado e a nova UI nao chamou a rotina que deveria buscar o ticker no RTD/Excel e gravar no banco.
130:docs/auditoria_ui_terminal_vwap_payoff.md:27:- O Excel permanece apenas como ponte RTD.
131:docs/auditoria_ui_terminal_vwap_payoff.md:58:Arquivo Excel informado como ponte:
132:docs/auditoria_ui_terminal_vwap_payoff.md:60:    LISTA_RTD.xlsm
133:docs/auditoria_ui_terminal_vwap_payoff.md:315:- Excel fechado;
134:docs/auditoria_ui_terminal_vwap_payoff.md:555:- substituição do Excel como ponte RTD.
135:docs/auditoria_ui_terminal_vwap_payoff.md:563:    LISTA_RTD.xlsx aparece como deletado no Git, mas é arquivo legado.
136:docs/auditoria_ui_terminal_vwap_payoff.md:564:    LISTA_RTD.xlsm aparece como arquivo operacional vigente da ponte RTD com macros.
137:docs/auditoria_ui_terminal_vwap_payoff.md:572:    Não restaurar LISTA_RTD.xlsx.
138:docs/auditoria_ui_terminal_vwap_payoff.md:573:    Não tratar LISTA_RTD.xlsx como ponte RTD vigente.
139:docs/auditoria_ui_terminal_vwap_payoff.md:574:    Preservar LISTA_RTD.xlsm como evolução consolidada.
140:docs/auditoria_ui_terminal_vwap_payoff.md:577:    Não incluir alterações de Excel no mesmo commit de documentação.
141:docs/auditoria_ui_terminal_vwap_payoff.md:582:    git restore LISTA_RTD.xlsx
142:docs/auditoria_ui_terminal_vwap_payoff.md:640:    Sem alteração intencional em arquivos Excel.
143:docs/auditoria_ui_terminal_vwap_payoff.md:644:    Excel permanece apenas como ponte RTD.
144:docs/auditoria_ui_terminal_vwap_payoff.md:649:    LISTA_RTD.xlsx
145:docs/auditoria_ui_terminal_vwap_payoff.md:650:    LISTA_RTD.xlsm
146:docs/auditoria_ui_terminal_vwap_payoff.md:700:    Excel permanece apenas como ponte RTD.
147:docs/auditoria_ui_terminal_vwap_payoff.md:701:    LISTA_RTD.xlsx permanece tratado como legado e não deve ser restaurado.
148:docs/auditoria_ui_terminal_vwap_payoff.md:705:    LISTA_RTD.xlsx
149:docs/auditoria_ui_terminal_vwap_payoff.md:706:    LISTA_RTD.xlsm
150:docs/auditoria_ui_terminal_vwap_payoff.md:711:    Alterações de Excel, reports, spikes e scripts locais não fazem parte deste registro documental.
151:docs/auditoria_ui_terminal_vwap_payoff.md:755:            LISTA_RTD.xlsx
152:docs/auditoria_ui_terminal_vwap_payoff.md:760:            LISTA_RTD.xlsx permanece classificado como legado e não deve ser restaurado.
153:docs/auditoria_ui_terminal_vwap_payoff.md:768:            LISTA_RTD.xlsm
154:docs/auditoria_ui_terminal_vwap_payoff.md:774:            LISTA_RTD.xlsm permanece como ponte RTD operacional local, sem versionamento.
155:docs/auditoria_ui_terminal_vwap_payoff.md:815:    Não houve restauração de LISTA_RTD.xlsx.
156:docs/auditoria_ui_terminal_vwap_payoff.md:816:    Não houve inclusão de arquivo Excel operacional no commit funcional.
157:docs/auditoria_ui_terminal_vwap_payoff.md:827:    LISTA_RTD.xlsx:
158:docs/auditoria_ui_terminal_vwap_payoff.md:831:    LISTA_RTD.xlsm:
159:docs/auditoria_ui_terminal_vwap_payoff.md:841:    Excel permanece apenas como ponte RTD.
160:docs/auditoria_ui_terminal_vwap_payoff.md:864:    Manter LISTA_RTD.xlsm fora do versionamento.
161:docs/auditoria_ui_terminal_vwap_payoff.md:865:    Não restaurar LISTA_RTD.xlsx.
162:docs/checkpoints/alteracoes/fase-6-11-autoalteracao-ajuste-enquadramento-em-documento-existente.txt:77:            - nao depender de Excel real
163:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:126:./bridge_ingest_csv.py:33:    CsvSpec("analise_raiox.csv",          "rtd_analise_raiox",          "replace"),
164:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:127:./bridge_ingest_csv.py:34:    CsvSpec("consolidacoes.csv",           "rtd_consolidacoes",           "replace"),
165:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:128:./bridge_ingest_csv.py:35:    CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),
166:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:129:./bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),
167:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:130:./bridge_ingest_csv.py:37:    CsvSpec("configuracoes.csv",           "rtd_configuracoes",           "replace"),
168:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:131:./bridge_ingest_csv.py:39:    CsvSpec("rolls_detectados.csv",        "rtd_rolls_detectados",        "append"),
169:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:132:./bridge_ingest_csv.py:40:    CsvSpec("hist_robo.csv",               "rtd_hist_robo",               "append"),
170:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:133:./bridge_ingest_csv.py:41:    CsvSpec("encerramentos_manuais.csv",   "rtd_encerramentos_manuais",   "append"),
171:docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt:268:./UI/main_window.py:509:* Excel RTD  CSV Bridge
172:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:1:./bridge_ingest_csv.py:33:    CsvSpec("analise_raiox.csv",          "rtd_analise_raiox",          "replace"),
173:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:2:./bridge_ingest_csv.py:34:    CsvSpec("consolidacoes.csv",           "rtd_consolidacoes",           "replace"),
174:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:3:./bridge_ingest_csv.py:35:    CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),
175:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:4:./bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),
176:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:5:./bridge_ingest_csv.py:37:    CsvSpec("configuracoes.csv",           "rtd_configuracoes",           "replace"),
177:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:6:./bridge_ingest_csv.py:39:    CsvSpec("rolls_detectados.csv",        "rtd_rolls_detectados",        "append"),
178:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:7:./bridge_ingest_csv.py:40:    CsvSpec("hist_robo.csv",               "rtd_hist_robo",               "append"),
179:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:8:./bridge_ingest_csv.py:41:    CsvSpec("encerramentos_manuais.csv",   "rtd_encerramentos_manuais",   "append"),
180:docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt:143:./UI/main_window.py:509:* Excel RTD  CSV Bridge
181:docs/checkpoints/evidencias/fase-1-trechos-atualizar-dados-runtime.txt:95:        file_menu.add_command(label="Exportar CSV...", command=self.export_csv)
182:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:47:./ATT/checks/check_api_routes.py:8:    win32com = None
183:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:50:./ATT/checks/check_api_routes.py:35:        if win32com is None:
184:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:80:./ATT/checks/check_legs.py:50:def validate_csv(path: Path) -> None:
185:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:417:./bridge_ingest_csv.py:22:DERIVED_DEBOUNCE_SEC = float(os.getenv("DERIVED_DEBOUNCE_SEC", "3"))
186:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:418:./bridge_ingest_csv.py:46:    s = str(col).strip()
187:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:419:./bridge_ingest_csv.py:47:    s = s.replace("\n", " ").replace("\r", " ")
188:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:420:./bridge_ingest_csv.py:51:    s = re.sub(r"_+", "_", s).strip("_")
189:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:421:./bridge_ingest_csv.py:69:        print(f"[DERIVED] pipeline não encontrado: {DERIVED_PIPELINE}")
190:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:422:./bridge_ingest_csv.py:73:    print(f"[DERIVED] executando: {' '.join(cmd)}")
191:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:423:./bridge_ingest_csv.py:78:        print(p.stdout.rstrip())
192:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:424:./bridge_ingest_csv.py:80:        print(p.stderr.rstrip())
193:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:425:./bridge_ingest_csv.py:82:    print(f"[DERIVED] returncode={p.returncode}")
194:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:426:./bridge_ingest_csv.py:87:    """Tenta ler o CSV com sep e enc dados. Retorna DataFrame ou None."""
195:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:427:./bridge_ingest_csv.py:99:        return None
196:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:428:./bridge_ingest_csv.py:101:        return None
197:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:429:./bridge_ingest_csv.py:103:        return None
198:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:430:./bridge_ingest_csv.py:114:    df = None
199:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:431:./bridge_ingest_csv.py:115:    used_enc = None
200:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:432:./bridge_ingest_csv.py:116:    used_sep = None
201:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:433:./bridge_ingest_csv.py:121:            if candidate is not None:
202:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:434:./bridge_ingest_csv.py:126:        if df is not None:
203:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:435:./bridge_ingest_csv.py:129:    if df is None:
204:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:436:./bridge_ingest_csv.py:135:    print(f"[INGEST] {path.name}: encoding={used_enc} sep='{used_sep}' colunas={list(df.columns)}")
205:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:437:./bridge_ingest_csv.py:138:    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
206:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:438:./bridge_ingest_csv.py:200:                print(f"[INGEST] Arquivo não encontrado, pulando: {spec.filename}")
207:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:439:./bridge_ingest_csv.py:210:            print(f"[INGEST] {spec.filename} -> {spec.table} ({spec.mode}): {len(df)} linhas")
208:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:440:./bridge_ingest_csv.py:219:def main(argv=None):
209:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:441:./bridge_ingest_csv.py:241:        print(f"[INGEST] Criado sentinela: {control}")
210:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:442:./bridge_ingest_csv.py:243:    print(f"[INGEST] Bridge dir: {BRIDGE_DIR}")
211:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:443:./bridge_ingest_csv.py:244:    print(f"[INGEST] Raw DB:     {RAW_DB}")
212:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:444:./bridge_ingest_csv.py:255:                print("[DERIVED] WARNING: pipeline falhou (ingest ok).")
213:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:445:./bridge_ingest_csv.py:257:            print("[DERIVED] debounce: ignorando disparo muito próximo do anterior.")
214:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:446:./bridge_ingest_csv.py:262:        print(f"[INGEST] import concluído, linhas processadas: {rows}")
215:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:447:./bridge_ingest_csv.py:267:    print("[INGEST] aguardando last_export.txt ...")
216:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:448:./bridge_ingest_csv.py:275:                print(f"[INGEST] import concluído, linhas processadas: {rows}")
217:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:449:./bridge_ingest_csv.py:279:                    print("[INGEST] --once: finalizando.")
218:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:1202:./docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt:258:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py:300:def _write_rtd_links_csv(csv_path: Path) -> None:
219:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:1850:./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:300:def _write_rtd_links_csv(csv_path: Path) -> None:
220:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:1878:./docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:300:def _write_rtd_links_csv(csv_path: Path) -> None:
221:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:1897:./docs/evolucoes de fases/baseline_v1.md:274:import win32com.clientexcel = win32com.client.Dispatch("Excel.Application")print(excel.Version)excel.Quit()
222:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:1915:./docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:123:bridge_ingest_csv.py:243:    print(f"[INGEST] Bridge dir: {BRIDGE_DIR}")
223:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:1916:./docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:132:ATT/checks/check_api_routes.py:8:    win32com = None
224:docs/checkpoints/evidencias/fase-2a-grep-conversoes-validacoes.txt:1917:./docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:137:ATT/checks/check_api_routes.py:35:        if win32com is None:
225:docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt:356:./docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:30:docs/auditoria_fase_9_cadastro_estruturas.md:5:Validar e corrigir o fluxo de cadastro e persistência de estruturas, garantindo que uma nova estrutura criada no sistema seja gravada no banco, tenha pernas persistidas, seja recuperada pela UI e possa alimentar o fluxo de cálculo sem edição manual no Excel.
226:docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt:392:./docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1626:docs/auditoria_fase_9_cadastro_estruturas.md:5:Validar e corrigir o fluxo de cadastro e persistência de estruturas, garantindo que uma nova estrutura criada no sistema seja gravada no banco, tenha pernas persistidas, seja recuperada pela UI e possa alimentar o fluxo de cálculo sem edição manual no Excel.
227:docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt:441:./docs/evolucoes de fases/auditoria_fase_9_cadastro_estruturas.md:5:Validar e corrigir o fluxo de cadastro e persistência de estruturas, garantindo que uma nova estrutura criada no sistema seja gravada no banco, tenha pernas persistidas, seja recuperada pela UI e possa alimentar o fluxo de cálculo sem edição manual no Excel.
228:docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt:442:./docs/evolucoes de fases/auditoria_fase_9_cadastro_estruturas.md:9:Nova estrutura criada no sistema aparece corretamente na UI sem edição manual no Excel.
229:docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt:448:./docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:70:Podem mudar de formato, depender de Excel, RTD, exportação manual ou captura externa.
230:docs/checkpoints/evidencias/fase-2a-grep-fluxo-manual.txt:467:./docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:344:Mapear todos os SELECT/INSERT/UPDATE envolvendo rtd_*, manual_* e tabelas legadas do Excel.
231:docs/checkpoints/evidencias/fase-2a-grep-strike.txt:151:./dados/RTD_LINKS.csv:1:﻿codigo_opcao;ativo_base;call_put;strike;vencimento;ultimo_preco;ultima_quantidade;bid;ask;volume;iv;delta;gamma;theta;vega
232:docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt:37:import csv
233:docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt:258:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py:300:def _write_rtd_links_csv(csv_path: Path) -> None:
234:docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt:262:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py:352:    csv_path = tmp_path / "RTD_LINKS.csv"
235:docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt:266:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py:357:    _write_rtd_links_csv(csv_path)
236:docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt:101:- LISTA_RTD.xlsx
237:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:30:docs/auditoria_fase_9_cadastro_estruturas.md:5:Validar e corrigir o fluxo de cadastro e persistência de estruturas, garantindo que uma nova estrutura criada no sistema seja gravada no banco, tenha pernas persistidas, seja recuperada pela UI e possa alimentar o fluxo de cálculo sem edição manual no Excel.
238:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:204:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:75:ATT/checks/check_structures.py:15:    ROOT_DIR / "bridge" / "analise_robo.csv",
239:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:205:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:76:ATT/checks/check_structures.py:16:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
240:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:381:ATT/checks/check_end_to_end.py:15:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
241:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:382:ATT/checks/check_legs.py:12:    BRIDGE_DIR / "analise_robo_legs.csv",
242:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:383:ATT/checks/check_structures.py:16:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
243:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1392:bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),
244:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1523:docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:474:bridge/analise_robo_legs.csv
245:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1532:docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:513:- bridge/analise_robo.csv, bridge/analise_robo_legs.csv e bridge/analise_raiox.csv ainda aparecem em checks
246:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1542:docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:142:bridge/analise_robo_legs.csv
247:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1551:docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:282:| `bridge/analise_robo_legs.csv` | legado | manter apenas enquanto houver consumidor |
248:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1554:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:69:ATT/checks/check_end_to_end.py:15:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
249:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1555:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:72:ATT/checks/check_legs.py:12:    BRIDGE_DIR / "analise_robo_legs.csv",
250:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1556:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:75:ATT/checks/check_structures.py:15:    ROOT_DIR / "bridge" / "analise_robo.csv",
251:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1557:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:76:ATT/checks/check_structures.py:16:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
252:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1558:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:81:bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),
253:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1572:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:113:ATT/checks/check_legs.py:12:    BRIDGE_DIR / "analise_robo_legs.csv",
254:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1579:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:232:analise_robo_legs.csv
255:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1587:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:372:analise_robo_legs.csv
256:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1592:docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:111:analise_robo_legs.csv
257:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1626:docs/auditoria_fase_9_cadastro_estruturas.md:5:Validar e corrigir o fluxo de cadastro e persistência de estruturas, garantindo que uma nova estrutura criada no sistema seja gravada no banco, tenha pernas persistidas, seja recuperada pela UI e possa alimentar o fluxo de cálculo sem edição manual no Excel.
258:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1642:docs/baseline_v1a.md:85:Input: ler rtd_analise_robo_legs (em vez de COM/Excel)
259:docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1739:docs/validacoes/fase-17-mapa-pastas-arquivos.md:159:| `bridge/analise_robo_legs.csv` | Sim | Versionado |
260:docs/checkpoints/evidencias/fase-9-encerramento-enriquecimento-legs-rtd-e-position-side.md:34:- não acoplar UI diretamente ao Excel;
261:docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt:1373:./.pytest_cache/v/cache/nodeids:91:  "ATT/tests/test_import_rtd_links_to_option_quotes.py::test_import_csv_to_db_dry_run_does_not_write",
262:docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt:1374:./.pytest_cache/v/cache/nodeids:92:  "ATT/tests/test_import_rtd_links_to_option_quotes.py::test_import_csv_to_db_upsert_is_idempotent_and_updates_existing_row",
263:docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt:1375:./.pytest_cache/v/cache/nodeids:93:  "ATT/tests/test_import_rtd_links_to_option_quotes.py::test_load_and_normalize_vertical_csv",
264:docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt:1387:./.pytest_cache/v/cache/nodeids:302:  "ATT/tests/test_run_rtd_option_quotes_pipeline.py::test_build_import_command_uses_csv_db_and_script_path",
265:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:1:import csv
266:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:300:def _write_rtd_links_csv(csv_path: Path) -> None:
267:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:301:    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
268:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:302:        writer = csv.writer(f)
269:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:352:    csv_path = tmp_path / "RTD_LINKS.csv"
270:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:357:    _write_rtd_links_csv(csv_path)
271:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:359:    import_stats = importer.import_csv_to_db(
272:docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt:360:        csv_path=csv_path,
273:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:1:import csv
274:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:300:def _write_rtd_links_csv(csv_path: Path) -> None:
275:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:301:    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
276:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:302:        writer = csv.writer(f)
277:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:352:    csv_path = tmp_path / "RTD_LINKS.csv"
278:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:357:    _write_rtd_links_csv(csv_path)
279:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:359:    import_stats = importer.import_csv_to_db(
280:docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt:360:        csv_path=csv_path,
281:docs/checkpoints/fase-6-11-retomada-funcional-pos-restauracao-documental.md:102:- nao depender de Excel real
282:docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md:7:Esta microfatia não altera UI/API e mantém o Excel apenas como gateway RTD.
283:docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md:154:3. Excel permanece apenas como gateway RTD;
284:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:13:5. A UI lê do banco, CSV ou Excel?
285:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:29:- Excel;
286:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:73:## Decisão sobre fontes legadas e LISTA_RTD.xlsx
287:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:82:- `LISTA_RTD.xlsx` passa a ser considerada candidata a fonte/gateway para o universo bruto RTD.
288:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:88:O fluxo novo não deve reconstruir o sistema em torno dos dados obsoletos. A Fase 2 deve mapear o legado existente e preparar a transição para um modelo onde a `LISTA_RTD.xlsx` alimenta dados RTD brutos, enquanto as estruturas operacionais nascem e vivem no banco do sistema.
289:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:98:- `LISTA_RTD`
290:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:113:- `db/import_excel.py` não consome `LISTA_RTD.xlsx`.
291:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:128:- criar posteriormente um gateway específico para `LISTA_RTD.xlsx`;
292:docs/evolucoes de fases/AUDITORIA_FASE_11_SNAPSHOTS_HISTORICO.md:12:Substituir o histórico gerado pelo Excel por histórico gerado pelo próprio sistema.
293:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:22:10. O Excel permanece apenas como gateway RTD.
294:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:92:O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:
295:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:166:LISTA_RTD.xlsm
296:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:178:LISTA_RTD.xlsm
297:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:239:A planilha `LISTA_RTD.xlsm` foi preservada como ponte RTD oficial e testada.
298:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:241:A planilha RTD legada abolida foi removida do versionamento. A entrada `LISTA_RTD.xlsx` deixou de ser tratada como ponte RTD oficial.
299:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:253:## Nota de supersessão — LISTA_RTD.xlsx
300:docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:255:Esta auditoria pode conter referências históricas a `LISTA_RTD.xlsx` feitas durante a reconciliação da ponte RTD.

## Arquivos candidatos RTD, Excel, snapshot, market e quote

./ATT/tests/__pycache__/test_audit_rtd_option_quotes.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_import_rtd_links_to_option_quotes.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_market_snapshot_provider.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_market_snapshot_repository_rtd_option_quotes.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_market_snapshot_selector.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_rtd_legacy_canonical_pricing_input_guardrail.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_rtd_live_db_guardrail.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_rtd_option_quotes_repository_contract.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_run_derived_pipeline_rtd_integration.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_run_rtd_option_quotes_pipeline.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_structure_leg_rtd_enrichment_service.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_structure_market_input_assembler.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_system_snapshots_repository.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_system_snapshots_schema.cpython-313-pytest-9.0.3.pyc
./ATT/tests/test_market_snapshot_provider.py
./ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py
./ATT/tests/test_market_snapshot_selector.py
./ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py
./ATT/tests/test_rtd_live_db_guardrail.py
./ATT/tests/test_structure_leg_rtd_enrichment_service.py
./ATT/tests/test_structure_market_input_assembler.py
./ATT/tests/test_system_snapshots_repository.py
./ATT/tests/test_system_snapshots_schema.py
./LISTA_RTD.xlsm
./audit_rtd_ui_flow.log
./backups/LISTA_RTD_fase12_rtd_option_quotes_ok.xlsm
./backups/app_fase12_rtd_option_quotes_ok.db
./backups/app_fase12_rtd_option_quotes_ok.sql
./dados/RTD_LINKS.csv
./dados/RTD_LINKS_probe.csv
./dados/RTD_UNDERLYING_QUOTES.csv
./dados/backups/app_antes_bootstrap_structure_snapshots_20260627_125921.db
./dados/rtd_symbols.strict.tmp.txt
./dados/rtd_symbols.txt
./dados/rtd_symbols_probe.txt
./dados/rtd_underlying_symbols.txt
./db/import_excel.py
./db/init_excel_schema.py
./db/schema_excel.py
./docs/AUDITORIA_RTD_EXCEL_VIVO.md
./docs/PLANO_RTD_EXCEL_VIVO.md
./docs/auditoria_rtd_nova_ui_bovak900.md
./docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt
./docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt
./docs/checkpoints/evidencias/fase-1-trechos-rtd-runtime.txt
./docs/checkpoints/evidencias/fase-6-11-analise-estatica-testes-rtd-historicos.txt
./docs/checkpoints/evidencias/fase-6-11-auditoria-testes-rtd-historicos-git.txt
./docs/checkpoints/evidencias/fase-6-11-datas-exclusao-testes-rtd-historicos.txt
./docs/checkpoints/evidencias/fase-6-11-decisao-final-testes-rtd-historicos.txt
./docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt
./docs/checkpoints/evidencias/fase-6-11-evidencia-fechamento-rtd-option-quotes-pricing-runtime.txt
./docs/checkpoints/evidencias/fase-6-11-evidencia-guardrails-rtd-option-quotes-repository.txt
./docs/checkpoints/evidencias/fase-6-11-evidencia-integracao-rtd-option-quotes-pricing-runtime.txt
./docs/checkpoints/evidencias/fase-6-11-evidencia-pr-rtd-option-quotes-pricing-runtime.txt
./docs/checkpoints/evidencias/fase-6-11-evidencia-repository-rtd-option-quotes.txt
./docs/checkpoints/evidencias/fase-6-11-importabilidade-testes-rtd-historicos-sanitizados.txt
./docs/checkpoints/evidencias/fase-6-11-inventario-testes-rtd-option-canonical.txt
./docs/checkpoints/evidencias/fase-6-11-mapa-impacto-integracao-rtd-option-quotes-pricing-runtime.txt
./docs/checkpoints/evidencias/fase-6-11-mapa-runtime-leitura-rtd-pricing.txt
./docs/checkpoints/evidencias/fase-6-11-matriz-compatibilidade-testes-rtd-historicos.txt
./docs/checkpoints/evidencias/fase-6-11-pytest-collect-only-testes-rtd-historicos-sanitizados.txt
./docs/checkpoints/evidencias/fase-6-11-pytest-collect-only-testes-rtd-historicos.txt
./docs/checkpoints/evidencias/fase-6-11-pytest-rtd-canonical-pricing-input-baseline.txt
./docs/checkpoints/evidencias/fase-6-11-pytest-rtd-canonical-pricing-input-guardrail.txt
./docs/checkpoints/evidencias/fase-6-11-recorte-rtd-canonical-pricing-input.txt
./docs/checkpoints/evidencias/fase-6-11-regressao-disponivel-rtd-canonical-pricing.txt
./docs/checkpoints/evidencias/fase-6-11-simbolos-atuais-rtd-pricing.txt
./docs/checkpoints/evidencias/fase-6-11-sintaxe-testes-rtd-historicos.txt
./docs/checkpoints/evidencias/fase-6-11-testes-rtd-historicos-ausentes.txt
./docs/checkpoints/evidencias/fase-6-7-inventario-diagnostico-rtd-canonical.txt
./docs/checkpoints/evidencias/fase-6-7-pytest-baseline-canonical-rtd.txt
./docs/checkpoints/evidencias/fase-6-7-pytest-baseline-rtd-option-quotes.txt
./docs/checkpoints/evidencias/fase-6-7-recorte-funcional-rtd-canonical.txt
./docs/checkpoints/evidencias/fase-6-8-pytest-guardrail-matriz-diagnostico-rtd.txt
./docs/checkpoints/evidencias/fase-6-9-pytest-canonical-pricing-rtd-number-formats.txt
./docs/checkpoints/evidencias/fase-7-execucao-testes-rtd-vigentes.txt
./docs/checkpoints/evidencias/fase-7-fechamento-validacao-regressiva-rtd-vigente.txt
./docs/checkpoints/evidencias/fase-7-validacao-regressiva-rtd-vigente.txt
./docs/checkpoints/evidencias/fase-9-encerramento-enriquecimento-legs-rtd-e-position-side.md
./docs/checkpoints/evidencias/fase-9-implementacao-enriquecimento-legs-rtd.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_execute_pricing_rtd_integration_from_b492f16.py.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_db_path_from_bcb6ddb.py.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_price_resolution_from_0c7e123.py.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_execute_pricing_rtd_integration.from-b492f16.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_db_path.from-bcb6ddb.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_price_resolution.from-0c7e123.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt
./docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md
./docs/checkpoints/fase-6-8-guardrail-matriz-diagnostico-rtd.md
./docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md
./docs/evolucoes de fases/AUDITORIA_FASE_11_SNAPSHOTS_HISTORICO.md
./docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md
./docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md
./docs_rtd_run.log
./domain/__pycache__/market_snapshot.cpython-313.pyc
./domain/market_snapshot.py
./infra/__pycache__/bootstrap_rtd_option_quotes_schema.cpython-313.pyc
./infra/bootstrap_rtd_option_quotes_schema.py
./reports/payoff_conferencia/db_path_ui_snapshots_20260627_125228.txt
./reports/payoff_conferencia/fontes_snapshot_metricas_perna_20260627_124640.txt
./reports/payoff_conferencia/orfaos_structure_leg_snapshots_20260627_125813.txt
./reports/payoff_conferencia/schema_real_snapshots_20260627_125139.txt
./reports/payoff_conferencia/schema_snapshot_metricas_perna_20260627_124651.txt
./reports/rtd_vwap_audit/csv_rtd_links_vwap_audit.json
./reports/rtd_vwap_audit/workbook_rtd_vwap_audit.json
./repositories/__pycache__/market_snapshot_repository.cpython-313.pyc
./repositories/__pycache__/rtd_option_quotes_repository.cpython-313.pyc
./repositories/__pycache__/system_snapshots_repository.cpython-313.pyc
./repositories/market_snapshot_repository.py
./repositories/rtd_option_quotes_repository.py
./repositories/system_snapshots_repository.py
./scripts/__pycache__/audit_rtd_option_quotes.cpython-313.pyc
./scripts/__pycache__/import_rtd_links_to_option_quotes.cpython-313.pyc
./scripts/__pycache__/import_rtd_option_quotes_wide_csv.cpython-313.pyc
./scripts/__pycache__/purge_derived_snapshots.cpython-313.pyc
./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes.cpython-313.pyc
./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes_fallback.cpython-313.pyc
./scripts/__pycache__/rtd_enriquecer_underlying_csv.cpython-313.pyc
./scripts/__pycache__/rtd_importar_underlying_csv.cpython-313.pyc
./scripts/__pycache__/rtd_inspecionar_app_derived.cpython-313.pyc
./scripts/__pycache__/rtd_mapa_alvos_fase0.cpython-313.pyc
./scripts/__pycache__/rtd_reconciliar_app_para_derived.cpython-313.pyc
./scripts/__pycache__/run_rtd_option_quotes_pipeline.cpython-313.pyc
./scripts/import_rtd_option_quotes_wide_csv.py
./scripts/purge_derived_snapshots.py
./scripts/refresh_rtd_option_quotes_excel.ps1
./scripts/refresh_rtd_symbol_to_option_quotes.py
./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
./scripts/rtd_auditoria_fase0.sh
./scripts/rtd_consulta_projeto.sh
./scripts/rtd_enriquecer_underlying_csv.py
./scripts/rtd_importar_underlying_csv.py
./scripts/rtd_inspecionar_app_derived.py
./scripts/rtd_mapa_alvos_fase0.py
./scripts/rtd_mapa_alvos_fase0.sh
./scripts/rtd_reconciliar_app_para_derived.py
./scripts/rtd_rodar_fase0.sh
./services/__pycache__/market_snapshot_provider.cpython-313.pyc
./services/__pycache__/market_snapshot_selector.cpython-313.pyc
./services/__pycache__/market_time.cpython-313.pyc
./services/__pycache__/structure_leg_rtd_enrichment_service.cpython-313.pyc
./services/__pycache__/structure_market_input_assembler.cpython-313.pyc
./services/market_snapshot_provider.py
./services/market_snapshot_selector.py
./services/structure_leg_rtd_enrichment_service.py
./services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd
./services/structure_market_input_assembler.py
./tools/audit_rtd_ui_flow.py
