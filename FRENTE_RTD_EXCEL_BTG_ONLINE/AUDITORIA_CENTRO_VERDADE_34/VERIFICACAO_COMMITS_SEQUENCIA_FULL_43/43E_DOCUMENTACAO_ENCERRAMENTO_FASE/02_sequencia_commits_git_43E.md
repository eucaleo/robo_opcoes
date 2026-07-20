# Sequencia de commits Git - Rodada 43E

Branch atual: `fix/payoff-centro-verdade-32`

## Ultimos 80 commits

```text
148aac4 | 2026-07-20 10:51:57 -0300 | eucaleo | chore(payoff): add center of truth guardrails
def6c25 | 2026-07-20 10:46:15 -0300 | eucaleo | docs(audit): add UI cleanup evidence
a0be3eb | 2026-07-20 10:44:46 -0300 | eucaleo | refactor(ui): remove payoff calc and decision writes
2bb988a | 2026-07-17 21:30:57 -0300 | eucaleo | test: fix backend validation import path 34
2aa154c | 2026-07-17 21:27:13 -0300 | eucaleo | docs: add centro de verdade audit 34 backend validation
7251d42 | 2026-07-17 21:18:00 -0300 | eucaleo | fix: block archived structure payoff refresh before loading data
010ac64 | 2026-07-17 21:00:07 -0300 | eucaleo | chore(audit): preserve round 32 helper scripts history
a7a2073 | 2026-07-17 20:42:43 -0300 | eucaleo | fix: restore ui syntax and keep payoff calculation backend only
68b229c | 2026-07-17 20:40:21 -0300 | eucaleo | fix: repair ui payoff block syntax
22a796d | 2026-07-17 20:38:33 -0300 | eucaleo | fix: block local payoff calculation in ui
d5cec48 | 2026-07-17 20:36:35 -0300 | eucaleo | audit: quarantine parallel payoff script and inspect ui scope
8bb1880 | 2026-07-17 20:31:34 -0300 | eucaleo | audit: test payoff refresh command service real flow
2f1936a | 2026-07-17 20:28:36 -0300 | eucaleo | audit: validate payoff refresh command service
6e823af | 2026-07-17 20:26:09 -0300 | eucaleo | fix: stabilize derived payoff decision persistence
27d12a4 | 2026-07-17 20:22:00 -0300 | eucaleo | fix: recover structure_id when saving derived decisions
0f496d7 | 2026-07-17 14:16:47 -0300 | eucaleo | Bloqueia payoff e decisões para estruturas arquivadas
4bd7364 | 2026-07-15 20:06:52 -0300 | eucaleo | Automatiza recálculo e validação de payoff RTD
6ea72a6 | 2026-07-15 19:28:36 -0300 | eucaleo | fix: force payoff snapshot refresh when recalculation is unchanged
8e217f1 | 2026-07-15 18:51:47 -0300 | eucaleo | fix(payoff): carregar último snapshot persistido por timestamp
83fbf03 | 2026-07-15 18:51:17 -0300 | eucaleo | fix(payoff): carregar último snapshot persistido por timestamp
381ba5e | 2026-07-15 16:05:38 -0300 | eucaleo | fix(ui): consumir payoff persistido e adicionar auto-refresh sem cálculo local
a34763f | 2026-07-13 21:54:51 -0300 | eucaleo | docs: encerra documentalmente fase 7 reconciliada ate 7.4
c6fb0ae | 2026-07-13 21:29:48 -0300 | eucaleo | docs: reconcilia fase 7.4 de decisao explicavel
24e68e4 | 2026-07-13 20:38:06 -0300 | eucaleo | docs: fecha fase 7.3 de regressao somente leitura
036e576 | 2026-07-13 20:16:09 -0300 | eucaleo | test: skip operational Excel RTD check when unavailable
bf0f0ef | 2026-07-13 18:51:50 -0300 | eucaleo | chore: remove generated rtd artifacts from tracking
0388da6 | 2026-07-13 18:43:13 -0300 | eucaleo | docs: registra regressao focada da fase 7.3
32f13f9 | 2026-07-13 18:28:06 -0300 | eucaleo | docs: registra auditoria textual da fase 7.3
ad1c74e | 2026-07-13 18:22:35 -0300 | eucaleo | docs: registra evidencia inicial da fase 7.3
8d1aeea | 2026-07-13 16:37:44 -0300 | eucaleo | docs: abre fase 7.3 de regressao somente leitura
32c84ea | 2026-07-13 16:34:48 -0300 | eucaleo | docs: fecha fase 7.2 de contratos minimos
e9433a4 | 2026-07-13 16:32:33 -0300 | eucaleo | docs: classifica contratos minimos da fase 7.2
1b2b815 | 2026-07-13 16:24:17 -0300 | eucaleo | docs: ajusta documentos da fase 7 para blocos indentados
93be050 | 2026-07-13 16:19:39 -0300 | eucaleo | docs: abre contrato minimo de decisao e alertas da fase 7.2
9678c2b | 2026-07-13 16:18:36 -0300 | eucaleo | docs: adiciona auditoria de rebaseline da fase 7.1
08ca918 | 2026-07-13 15:38:51 -0300 | eucaleo | Atualiza rota apos encerramento tecnico da Fase 6 RTD Excel
ef39bab | 2026-07-13 14:53:53 -0300 | eucaleo | Encerra frente retencao limpeza Fase 6.15 RTD Excel
01483e4 | 2026-07-13 14:45:14 -0300 | eucaleo | Valida pos-limpeza e performance Fase 6.14 RTD Excel
5c367fd | 2026-07-13 14:37:17 -0300 | eucaleo | Regulariza execucao real controlada Fase 6.13 RTD Excel
32a7a1c | 2026-07-13 14:11:55 -0300 | eucaleo | Prepara execucao real com rollback Fase 6.12 RTD Excel
a79d068 | 2026-07-13 13:46:28 -0300 | eucaleo | Cria backup fisico controlado Fase 6.11 RTD Excel
1c4ff63 | 2026-07-13 13:33:57 -0300 | eucaleo | Prepara plano controlado de limpeza Fase 6.10 RTD Excel
c7dd69a | 2026-07-13 13:26:56 -0300 | eucaleo | Simula limpeza canonica timezone local Fase 6.9 RTD Excel
64f4902 | 2026-07-13 13:20:05 -0300 | eucaleo | Valida regra canonica de timezone local Fase 6.8 RTD Excel
7d103dd | 2026-07-13 11:35:21 -0300 | eucaleo | Diagnostica coortes temporais de cobertura Fase 6.7 RTD Excel
51ef7a4 | 2026-07-13 11:31:03 -0300 | eucaleo | Valida offset temporal de cobertura Fase 6.6 RTD Excel
1cd2d0d | 2026-07-13 11:28:17 -0300 | eucaleo | Diagnostica lacunas de cobertura Fase 6.5 RTD Excel
56cbc8a | 2026-07-13 11:21:14 -0300 | eucaleo | Define regra explicita de cobertura Fase 6.4 RTD Excel
89a59cb | 2026-07-13 11:14:12 -0300 | eucaleo | Mapeia schema para cobertura de candles Fase 6.3 RTD Excel
7541367 | 2026-07-13 11:10:04 -0300 | eucaleo | Valida cobertura de candles antes da limpeza Fase 6.2 RTD Excel
555fa69 | 2026-07-13 11:06:25 -0300 | eucaleo | Define contrato dry-run da Fase 6.1 RTD Excel
75d70f9 | 2026-07-13 10:48:39 -0300 | eucaleo | Inicia auditoria da Fase 6 RTD Excel
1c852fd | 2026-07-13 10:19:11 -0300 | eucaleo | Registra encerramento operacional da Fase 5 RTD Excel
69f9973 | 2026-07-13 09:57:53 -0300 | eucaleo | Remove generated RTD output artifacts from repository
c84ad96 | 2026-07-13 09:52:10 -0300 | eucaleo | Wire Excel RTD option quotes into terminal VWAP payoff flow
989821f | 2026-07-10 13:18:40 -0300 | Carlos Pereira | Merge pull request #26 from eucaleo/refactor/bd-unico-appdb
30df982 | 2026-07-10 13:13:51 -0300 | eucaleo | docs: auditar encerramento bd unico appdb
eab23c8 | 2026-07-10 13:02:00 -0300 | eucaleo | chore: limpar residuos textuais de bancos legados
a269d5a | 2026-07-10 12:58:32 -0300 | eucaleo | refactor: limitar snapshots do details panel ao app db canonico
96d3cf2 | 2026-07-10 12:50:38 -0300 | eucaleo | fix: evitar sombra de metodo app_db_path no details panel
f572091 | 2026-07-10 12:44:19 -0300 | eucaleo | refactor: usar db_path do dialogo no fluxo RTD
9477a1a | 2026-07-10 10:56:47 -0300 | eucaleo | refactor: remove sincronizacao RTD Excel da UI
4581c95 | 2026-07-10 10:45:08 -0300 | eucaleo | refactor: formaliza snapshot RTD centralizado
12601f8 | 2026-07-10 10:35:01 -0300 | eucaleo | refactor: remove subprocess RTD operacional do editor de estrutura
d3979cd | 2026-07-10 10:28:36 -0300 | eucaleo | docs: registra auditoria de fechamento da fase 1 RTD Excel
5af5813 | 2026-07-10 10:25:35 -0300 | eucaleo | docs: registra auditoria de retorno ao roteiro RTD Excel
647360d | 2026-07-10 09:50:36 -0300 | eucaleo | refactor: conclui centralizacao COM operacional RTD Excel
3b9ef80 | 2026-07-10 09:30:18 -0300 | eucaleo | fix: restaura modelo de status RTD Excel
6869b73 | 2026-07-10 09:27:07 -0300 | eucaleo | fix: aplica centralizacao COM Excel RTD
0337f8d | 2026-07-10 09:25:04 -0300 | eucaleo | refactor: centraliza acesso COM Excel RTD
7ead120 | 2026-07-10 09:22:01 -0300 | eucaleo | chore: padroniza line endings do projeto
a2059bb | 2026-07-10 09:19:45 -0300 | eucaleo | refactor: centraliza schema RTD option quotes
244bb49 | 2026-07-10 08:58:55 -0300 | eucaleo | feat: adiciona status RTD Excel no menu ajuda
ec00d4e | 2026-07-10 08:17:25 -0300 | eucaleo | feat: expose Excel RTD status payload
dbc0c83 | 2026-07-10 08:12:31 -0300 | eucaleo | feat: add Excel RTD connection status service
6e7a532 | 2026-07-09 22:57:44 -0300 | eucaleo | chore: guard against generated RTD artifacts
ff4318e | 2026-07-09 22:48:59 -0300 | eucaleo | refactor: move Excel RTD reader to RTD bridge
cf0aacd | 2026-07-09 22:45:35 -0300 | eucaleo | test: validate RTD option quotes bridge
129b0e1 | 2026-07-09 21:22:57 -0300 | eucaleo | feat: sincronizar excel rtd com snapshot de opcoes
3955156 | 2026-07-09 21:06:21 -0300 | eucaleo | fix: normalizar vencimento rtd excel para data brasileira
```

## Commits com estatistica curta

```text
148aac4 chore(payoff): add center of truth guardrails
 .../GUARDRAILS_36/00_resumo_guardrails_36.txt      |  14 ++
 .../01_payoff_refresh_command_service.txt          |  61 +++++++
 .../02_derived_payoff_persistence.txt              |  44 +++++
 .../GUARDRAILS_36/03_wiring_backend.txt            |  32 ++++
 .../GUARDRAILS_36/04_ui_terminal_payoff_scope.txt  |  12 ++
 .../05_script_recalculate_parallel_engine.txt      |  20 +++
 .../06_verify_payoff_center_of_truth_scope.txt     |   3 +
 scripts/verify_payoff_center_of_truth_scope.py     | 196 +++++++++++++++++++++
 8 files changed, 382 insertions(+)
def6c25 docs(audit): add UI cleanup evidence
 .../00_grep_ui_payoff_decisions_antes.txt          |  25 +++
 .../01_chamada_load_payoff_points.txt              |  51 ++++++
 .../UI_CLEANUP_35/02_load_e_calculo_payoff.txt     | 186 +++++++++++++++++++++
 .../03_insert_structure_decisions.txt              |  58 +++++++
 .../UI_CLEANUP_35/04_load_structure_decisions.txt  |  41 +++++
 .../UI_CLEANUP_35/05_debug_payoff_hook.txt         |  61 +++++++
 6 files changed, 422 insertions(+)
a0be3eb refactor(ui): remove payoff calc and decision writes
 UI/components/terminal_vwap_payoff_dark_panel.py | 134 +++++------------------
 1 file changed, 30 insertions(+), 104 deletions(-)
2bb988a test: fix backend validation import path 34
 .../RESULTADO_BACKEND_SEM_UI_34.md                 | 181 ++++++++++++++++++--
 .../resultado_backend_sem_ui_34.json               | 186 ++++++++++++++++++++-
 .../validar_backend_sem_ui_34.py                   |  19 +++
 3 files changed, 368 insertions(+), 18 deletions(-)
2aa154c docs: add centro de verdade audit 34 backend validation
 .../01_payoff_refresh_command_service_achados.txt  |  32 ++
 .../02_derived_payoff_persistence_achados.txt      |  37 ++
 ...icing_execution_persistence_service_achados.txt |  12 +
 ...ing_execution_orchestration_service_achados.txt |  13 +
 .../05_canonical_pricing_facade_achados.txt        |  17 +
 ..._terminal_vwap_payoff_dark_panel_ui_achados.txt |  14 +
 ...ate_payoff_curve_points_once_script_achados.txt |  11 +
 .../RESULTADO_BACKEND_SEM_UI_34.md                 |  46 ++
 .../RESUMO_AUDITORIA_CENTRO_VERDADE_34.md          |  43 ++
 .../auditar_centro_verdade_34.py                   | 320 ++++++++++++++
 .../resultado_backend_sem_ui_34.json               |  24 +
 .../validar_backend_sem_ui_34.py                   | 484 +++++++++++++++++++++
 12 files changed, 1053 insertions(+)
7251d42 fix: block archived structure payoff refresh before loading data
 UI/components/terminal_vwap_payoff_dark_panel.py | 8 ++++++++
 1 file changed, 8 insertions(+)
010ac64 chore(audit): preserve round 32 helper scripts history
 scripts/audit/history_32/README.md                 |  15 ++
 .../apply_patch_32_5_fix_decision_structure_id.py  | 119 ++++++++++++
 ...pply_patch_32_6_harden_decision_structure_id.py | 141 ++++++++++++++
 ...h_32_7_recover_structure_id_in_save_decision.py | 167 +++++++++++++++++
 .../history_32/fix_32_7_indent_derived_service.py  |  65 +++++++
 .../history_32/verificar_docs_removidos_hoje.py    | 207 +++++++++++++++++++++
 6 files changed, 714 insertions(+)
a7a2073 fix: restore ui syntax and keep payoff calculation backend only
 ..._2_AUDIT_UI_SYNTAX_AND_BACKEND_PAYOFF_ONLY.json |  33 ++
 ...13_2_AUDIT_UI_SYNTAX_AND_BACKEND_PAYOFF_ONLY.md |  29 ++
 ..._2_PATCH_RESTORE_UI_AND_BLOCK_LOCAL_PAYOFF.json |  43 +++
 ...13_2_PATCH_RESTORE_UI_AND_BLOCK_LOCAL_PAYOFF.md |  37 +++
 UI/components/terminal_vwap_payoff_dark_panel.py   |  70 +++--
 ...ch_32_13_2_restore_ui_and_block_local_payoff.py | 337 +++++++++++++++++++++
 ...it_32_13_2_ui_syntax_and_backend_payoff_only.py | 218 +++++++++++++
 scripts/audit/run_32_13_2_next_steps.sh            |  64 ++++
 8 files changed, 806 insertions(+), 25 deletions(-)
68b229c fix: repair ui payoff block syntax
 ...3_1_AUDIT_UI_SYNTAX_AND_LOCAL_PAYOFF_BLOCK.json |   9 +
 ..._13_1_AUDIT_UI_SYNTAX_AND_LOCAL_PAYOFF_BLOCK.md |  27 +++
 ...3_1_PATCH_FIX_UI_LOCAL_PAYOFF_BLOCK_SYNTAX.json |  13 ++
 ..._13_1_PATCH_FIX_UI_LOCAL_PAYOFF_BLOCK_SYNTAX.md |  25 ++
 ...tch_32_13_1_fix_ui_local_payoff_block_syntax.py | 252 +++++++++++++++++++++
 ...dit_32_13_1_ui_syntax_and_local_payoff_block.py | 184 +++++++++++++++
 scripts/audit/run_32_13_1_next_steps.sh            |  68 ++++++
 7 files changed, 578 insertions(+)
22a796d fix: block local payoff calculation in ui
 ...ATORIO_32_13_AUDIT_UI_LOCAL_PAYOFF_BLOCKED.json |  11 +
 ...ELATORIO_32_13_AUDIT_UI_LOCAL_PAYOFF_BLOCKED.md |  31 +++
 ...13_PATCH_BLOCK_UI_LOCAL_PAYOFF_CALCULATION.json |  40 +++
 ...2_13_PATCH_BLOCK_UI_LOCAL_PAYOFF_CALCULATION.md |  28 ++
 UI/components/terminal_vwap_payoff_dark_panel.py   |  77 ++----
 ...atch_32_13_block_ui_local_payoff_calculation.py | 226 ++++++++++++++++
 .../audit/audit_32_13_ui_local_payoff_blocked.py   | 289 +++++++++++++++++++++
 scripts/audit/run_32_13_next_steps.sh              |  49 ++++
 8 files changed, 699 insertions(+), 52 deletions(-)
d5cec48 audit: quarantine parallel payoff script and inspect ui scope
 ...1_AUDIT_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.json |  51 +++++
 ..._11_AUDIT_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.md |  45 ++++
 ...1_PATCH_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.json |  10 +
 ..._11_PATCH_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.md |  21 ++
 ...ELATORIO_32_12_AUDIT_UI_LOCAL_PAYOFF_SCOPE.json | 110 +++++++++
 .../RELATORIO_32_12_AUDIT_UI_LOCAL_PAYOFF_SCOPE.md |  56 +++++
 ...tch_32_11_quarantine_parallel_payoff_scripts.py | 146 ++++++++++++
 ...dit_32_11_quarantine_parallel_payoff_scripts.py | 194 ++++++++++++++++
 scripts/audit/audit_32_12_ui_local_payoff_scope.py | 250 +++++++++++++++++++++
 scripts/audit/run_32_11_32_12_next_steps.sh        |  59 +++++
 scripts/recalculate_payoff_curve_points_once.py    |  23 ++
 11 files changed, 965 insertions(+)
8bb1880 audit: test payoff refresh command service real flow
 ...0_TEST_PAYOFF_REFRESH_COMMAND_SERVICE_REAL.json | 280 +++++++++++++++++++++
 ..._10_TEST_PAYOFF_REFRESH_COMMAND_SERVICE_REAL.md |  48 ++++
 2 files changed, 328 insertions(+)
2f1936a audit: validate payoff refresh command service
 ..._32_9_AUDIT_PAYOFF_REFRESH_COMMAND_SERVICE.json | 22 ++++++++++
 ...IO_32_9_AUDIT_PAYOFF_REFRESH_COMMAND_SERVICE.md | 47 ++++++++++++++++++++++
 2 files changed, 69 insertions(+)
6e823af fix: stabilize derived payoff decision persistence
 .../RELATORIO_32_1_AUDITORIA_POS_PATCH.md          |    6 +-
 .../RELATORIO_32_1_TESTE_BACKEND_PAYOFF_FLOW.json  |   24 +-
 .../RELATORIO_32_3_CONTEXTO_CORRECAO_BACKEND.md    | 1496 ++++++++++++++++++++
 .../RELATORIO_32_5_FIX_DECISION_STRUCTURE_ID.md    |   12 +
 .../RELATORIO_32_6_HARDEN_DECISION_STRUCTURE_ID.md |   19 +
 ...O_32_8_1_FIX_INDENT_COSMETIC_DERIVED_SERVICE.md |   13 +
 ...ATORIO_32_8_FIX_DERIVED_SERVICE_RETURN_PATHS.md |   36 +
 services/derived_payoff_persistence.py             |    3 +
 services/derived_service.py                        |   18 +-
 9 files changed, 1603 insertions(+), 24 deletions(-)
27d12a4 fix: recover structure_id when saving derived decisions
 .../RELATORIO_32_1_AUDITORIA_POS_PATCH.md          |   312 +
 .../RELATORIO_32_1_TESTE_BACKEND_PAYOFF_FLOW.json  |    29 +
 ...TORIO_32_2_DIAGNOSE_PAYOFF_PERSISTENCE_GAP.json | 16775 +++++++++++++++++++
 ...LATORIO_32_2_DIAGNOSE_PAYOFF_PERSISTENCE_GAP.md |  2746 +++
 .../RELATORIO_32_4_PATCH_WIRE_DERIVED_PAYOFF.md    |    34 +
 .../RELATORIO_32_7_1_FIX_INDENT_DERIVED_SERVICE.md |    14 +
 ...O_32_7_RECOVER_STRUCTURE_ID_IN_SAVE_DECISION.md |    16 +
 .../audit/apply_patch_32_4_wire_derived_payoff.py  |   208 +
 scripts/audit/auditoria_pos_patch_32.py            |   293 +
 scripts/audit/collect_backend_fix_context_32_3.py  |   283 +
 .../audit/diagnose_payoff_persistence_gap_32_2.py  |   349 +
 scripts/audit/run_pos_patch_32.sh                  |    32 +
 scripts/audit/run_pos_patch_32_2.sh                |    19 +
 scripts/audit/test_backend_payoff_flow_32.py       |   134 +
 services/derived_service.py                        |   109 +-
 .../pricing_execution_orchestration_service.py     |     2 +
 16 files changed, 21346 insertions(+), 9 deletions(-)
0f496d7 Bloqueia payoff e decisões para estruturas arquivadas
 scripts/recalculate_payoff_curve_points_once.py |  55 +++-
 services/derived_payoff_persistence.py          | 171 +++++++++++-
 services/payoff_refresh_command_service.py      | 330 ++++++++++++++++++++++++
 3 files changed, 544 insertions(+), 12 deletions(-)
4bd7364 Automatiza recálculo e validação de payoff RTD
 .gitignore                            |   1 +
 scripts/payoff_rtd_batch.py           | 187 ++++++++++++++++++++++++++++
 scripts/payoff_rtd_refresh.sh         |  43 +++++++
 scripts/validate_payoff_rtd_latest.py | 224 ++++++++++++++++++++++++++++++++++
 4 files changed, 455 insertions(+)
6ea72a6 fix: force payoff snapshot refresh when recalculation is unchanged
 UI/components/terminal_vwap_payoff_dark_panel.py   |  72 +++++
 scripts/diagnose_payoff_curve_points.py            | 174 +++++++++++
 ...recalculate_payoff_curve_points_once_checked.py | 340 +++++++++++++++++++++
 scripts/run_rtd_and_payoff_auto_refresh_loop.py    |   2 +-
 4 files changed, 587 insertions(+), 1 deletion(-)
8e217f1 fix(payoff): carregar último snapshot persistido por timestamp
 scripts/recalculate_payoff_curve_points_once.py | 159 +++++++++++++++++++
 scripts/run_rtd_and_payoff_auto_refresh_loop.py | 121 +++++++++++++++
 scripts/verify_payoff_refresh_architecture.py   | 193 ++++++++++++++++++++++++
 3 files changed, 473 insertions(+)
83fbf03 fix(payoff): carregar último snapshot persistido por timestamp
 UI/components/terminal_vwap_payoff_dark_panel.py | 28 ++++++++++++++++--------
 1 file changed, 19 insertions(+), 9 deletions(-)
381ba5e fix(ui): consumir payoff persistido e adicionar auto-refresh sem cálculo local
 UI/components/terminal_vwap_payoff_dark_panel.py | 229 +++++++++++++---
 scripts/patch_ui_payoff_refresh_architecture.py  | 326 +++++++++++++++++++++++
 2 files changed, 521 insertions(+), 34 deletions(-)
a34763f docs: encerra documentalmente fase 7 reconciliada ate 7.4
 ...ncerramento_documental_reconciliado_20260713.md | 74 ++++++++++++++++++++++
 1 file changed, 74 insertions(+)
c6fb0ae docs: reconcilia fase 7.4 de decisao explicavel
 ...04_reconciliacao_decisao_explicavel_20260713.md | 171 +++++++++++++++++++++
 1 file changed, 171 insertions(+)
24e68e4 docs: fecha fase 7.3 de regressao somente leitura
 ...regressao_contratos_somente_leitura_20260713.md | 30 ++++++++++++++++++++++
 1 file changed, 30 insertions(+)
036e576 test: skip operational Excel RTD check when unavailable
 .../test_ui_modern_dark_window_excel_rtd_status_menu.py      | 12 +++++++-----
 1 file changed, 7 insertions(+), 5 deletions(-)
bf0f0ef chore: remove generated rtd artifacts from tracking
 .gitignore                                         |   5 +-
 .../fase6_10_manifesto_ids_elegiveis_20260713.json | 570 ---------------------
 ...10_plano_execucao_controlada_backup_20260713.md |  77 ---
 .../output/fase6_10_pytest_20260713.txt            |   2 -
 ...fase6_11_backup_fisico_controlado_20260713.json |  37 --
 .../fase6_11_backup_fisico_controlado_20260713.md  |  62 ---
 .../output/fase6_11_pytest_20260713.txt            |   2 -
 ...12_prepara_execucao_real_rollback_20260713.json | 124 -----
 ...6_12_prepara_execucao_real_rollback_20260713.md |  93 ----
 .../output/fase6_12_pytest_20260713.txt            |   2 -
 ..._execucao_real_limpeza_controlada_20260713.json | 151 ------
 ...13_execucao_real_limpeza_controlada_20260713.md |  90 ----
 .../output/fase6_13_pytest_20260713.txt            |   2 -
 .../output/fase6_14_pytest_20260713.txt            |   2 -
 ...validacao_pos_limpeza_performance_20260713.json |  91 ----
 ...4_validacao_pos_limpeza_performance_20260713.md |  79 ---
 ...ramento_frente_consolidacao_final_20260713.json |  84 ---
 ...erramento_frente_consolidacao_final_20260713.md | 108 ----
 .../output/fase6_15_pytest_20260713.txt            |   2 -
 .../output/fase6_1_pytest_20260713.txt             |   2 -
 .../output/fase6_1_retencao_dry_run_20260713.md    |  52 --
 .../output/fase6_2_pytest_20260713.txt             |   2 -
 ...fase6_2_validacao_cobertura_candles_20260713.md |  94 ----
 ...fase6_3_mapeamento_schema_cobertura_20260713.md |  98 ----
 .../output/fase6_3_pytest_20260713.txt             |   2 -
 .../output/fase6_4_pytest_20260713.txt             |   2 -
 .../fase6_4_regra_explicita_cobertura_20260713.md  |  69 ---
 ...se6_5_diagnostico_lacunas_cobertura_20260713.md | 216 --------
 .../output/fase6_5_pytest_20260713.txt             |   2 -
 .../output/fase6_6_pytest_20260713.txt             |   2 -
 ...validacao_offset_temporal_cobertura_20260713.md | 106 ----
 ...nostico_coortes_temporais_cobertura_20260713.md | 145 ------
 .../output/fase6_7_pytest_20260713.txt             |   2 -
 .../output/fase6_8_pytest_20260713.txt             |   2 -
 ...dacao_regra_canonica_timezone_local_20260713.md | 132 -----
 ...run_limpeza_canonica_timezone_local_20260713.md | 146 ------
 .../output/fase6_9_pytest_20260713.txt             |   2 -
 37 files changed, 3 insertions(+), 2656 deletions(-)
0388da6 docs: registra regressao focada da fase 7.3
 ...regressao_contratos_somente_leitura_20260713.md | 99 ++++++++++++++++++++++
 1 file changed, 99 insertions(+)
32f13f9 docs: registra auditoria textual da fase 7.3
 ...regressao_contratos_somente_leitura_20260713.md | 44 ++++++++++++++++++++++
 1 file changed, 44 insertions(+)
ad1c74e docs: registra evidencia inicial da fase 7.3
 ...regressao_contratos_somente_leitura_20260713.md | 33 ++++++++++++++++++++++
 1 file changed, 33 insertions(+)
8d1aeea docs: abre fase 7.3 de regressao somente leitura
 ...regressao_contratos_somente_leitura_20260713.md | 158 +++++++++++++++++++++
 1 file changed, 158 insertions(+)

```
