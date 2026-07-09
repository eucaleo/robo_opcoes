# Verificacao de Retomada - RTD Excel BTG Online

Data/hora: 09/07/2026 18:26:34
Projeto: C:\Users\eucal\projeto
Branch: refactor/bd-unico-appdb
Diretorio de evidencias: FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634

## Resultado geral

Status: OK_COM_ALERTAS

## Checks

- OK | CRITICO | repositorio_git_detectado | root=C:\Users\eucal\projeto
- OK | CRITICO | frente_documental_existe | FRENTE_RTD_EXCEL_BTG_ONLINE
- OK | CRITICO | pasta_output_frente_existe | FRENTE_RTD_EXCEL_BTG_ONLINE/output
- OK | INFORMATIVO | branch_atual_identificada | refactor/bd-unico-appdb
- FALHA | INFORMATIVO | working_tree_sem_alteracoes_previas | existem alteracoes antes ou durante a verificacao
- OK | CRITICO | workbook_lista_rtd_existe_na_raiz | LISTA_RTD.xlsm
- OK | CRITICO | script_diagnose_excel_com_existe | scripts/diagnose_excel_com.py
- OK | CRITICO | script_probe_excel_rtd_workbook_existe | scripts/probe_excel_rtd_workbook.py
- OK | CRITICO | frente_documental_tem_arquivos | arquivos_listados=32
- OK | INFORMATIVO | busca_referencias_projeto_executada | ocorrencias=5001
- OK | CRITICO | excel_com_diagnostico_executado | returncode=0
- OK | CRITICO | probe_workbook_default_ok | returncode=0
- OK | CRITICO | probe_rtd_option_quotes_ok | returncode=0
- OK | INFORMATIVO | probe_rtd_btg_lista_ok | returncode=0
- OK | CRITICO | workbook_contem_aba_rtd_option_quotes | sheets=['RTD_OPTION_QUOTES', 'RTD-BTG LISTA']
- OK | CRITICO | aba_rtd_option_quotes_selecionada | selected_sheet=RTD_OPTION_QUOTES
- OK | CRITICO | headers_obrigatorios_rtd_option_quotes | ok
- OK | CRITICO | rtd_option_quotes_tem_linhas | row_count=2
- OK | CRITICO | rtd_option_quotes_tem_colunas | col_count=16

## Arquivos de evidencia

- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/git_rev_parse_root.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/git_branch.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/git_status_short.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/git_log_last_20.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/frente_files.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/frente_output_files.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/project_search_hits.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/diagnose_excel_com.stdout.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/diagnose_excel_com.stderr.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/probe_excel_rtd_workbook_default.stdout.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/probe_excel_rtd_workbook_default.stderr.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/probe_excel_rtd_option_quotes.stdout.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/probe_excel_rtd_option_quotes.stderr.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/probe_excel_rtd_btg_lista.stdout.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/probe_excel_rtd_btg_lista.stderr.txt
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/retomada_check.json
- FRENTE_RTD_EXCEL_BTG_ONLINE/output/retomada_20260709_182634/retomada_check.md

## Pendencias criticas

- Nenhuma pendencia critica identificada.

## Observacao

Este script apenas verifica o estado de retomada.
Ele nao altera logica operacional do sistema.
Ele utiliza os probes existentes para confirmar Excel COM, workbook e abas RTD.
