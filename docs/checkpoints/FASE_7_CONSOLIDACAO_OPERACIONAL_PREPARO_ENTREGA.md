# Fase 7 - Consolidacao operacional e preparo de entrega

## Objetivo

Consolidar o estado operacional apos a validacao integrada final da Fase 6, preparando o projeto para entrega, merge ou uso controlado.

## Ponto de partida

- Fase 6 encerrada com sucesso.
- Tag criada: fase-6-validacao-integrada-final.
- Branch enviada ao remoto.
- Status Git limpo no inicio da fase.

## Escopo da Fase 7

- Revisar documentacao de checkpoints.
- Conferir scripts auxiliares em scripts/dev.
- Confirmar fluxo operacional do pipeline.
- Verificar ausencia de pendencias Git.
- Preparar decisao de entrega, merge ou continuidade.

## Checklist inicial

- [ ] Confirmar branch atual.
- [ ] Confirmar ultimo commit da Fase 6.
- [ ] Confirmar tag da Fase 6.
- [ ] Confirmar status Git limpo.
- [ ] Revisar documentacao operacional.
- [ ] Definir criterio de encerramento da Fase 7.

## Comandos de referencia

git status --short
git log --oneline -5
git tag --list "fase-6*"

## Inventario operacional inicial

### Estado Git

- Branch atual: fase-3a4-auto-pricing-manual-save
- Ultimo commit: ce96bf3 docs: abre fase 7 de consolidacao operacional
- Status Git: limpo apos registro e commit do inventario

### Tags da Fase 6 presentes

- fase-6-10-restauracao-documental-rota-mestre-3
- fase-6-9-rtd-canonical-pricing
- fase-6-validacao-integrada-final

### Checkpoints presentes

- docs/checkpoints/FASE_5F_VALIDACAO_UI_PIPELINE.md
- docs/checkpoints/FASE_6_VALIDACAO_INTEGRADA_FINAL.md
- docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md
- docs/checkpoints/auditoria-revisao-funcional-pos-uso-real.md
- docs/checkpoints/fase-6-11-retomada-funcional-pos-restauracao-documental.md
- docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md
- docs/checkpoints/fase-6-8-guardrail-matriz-diagnostico-rtd.md
- docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md

### Scripts auxiliares presentes

- scripts/dev/close_phase_5f_ui_pipeline.sh
- scripts/dev/close_phase_6_integrated_validation.sh
- scripts/dev/open_phase_6_integrated_validation.sh
- scripts/dev/open_phase_7_operational_consolidation.sh
- scripts/dev/register_phase_7_operational_inventory.sh

### Conclusao inicial

- A Fase 7 iniciou com branch remota atualizada.
- A Fase 6 possui tag final preservada.
- O repositorio esta em estado limpo no inicio da consolidacao operacional.

## Baseline tecnica operacional

### Estado do repositorio

- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit atual: 295e3bf docs: registra inventario operacional da fase 7
- Arquivos versionados: 435
- Status Git: limpo apos registro e commit da baseline

### Estrutura principal identificada

- .gitignore
- .pytest_cache
- ATT
- LISTA_RTD.xlsx
- OPERACOES_E_OPCOES.xlsm
- UI
- __pycache__
- _resgate_db
- _usage_audit
- api
- backups
- bridge
- bridge_ingest_csv.py
- create_payoff_summary_table.py
- dados
- data
- db
- docs
- domain
- dto
- find_structure.sh
- infra
- limpar_repositorio_seguro.sh
- main.py
- mapear_repositorio.sh
- repositories
- run_ui.py
- scripts
- services
- src
- utils
- validate_db.py
- validators

### Arquivos de manifesto e configuracao encontrados

- Nenhum manifesto conhecido encontrado ate profundidade 3

### Scripts de desenvolvimento versionados

- scripts/dev/close_phase_5f_ui_pipeline.sh
- scripts/dev/close_phase_6_integrated_validation.sh
- scripts/dev/open_phase_6_integrated_validation.sh
- scripts/dev/open_phase_7_operational_consolidation.sh
- scripts/dev/register_phase_7_operational_inventory.sh
- scripts/dev/register_phase_7_technical_baseline.sh

### Conclusao da baseline

- A baseline tecnica foi registrada sem alteracao funcional.
- O objetivo desta etapa e preparar a revisao operacional e a entrega controlada.

## Revisao de higiene operacional

### Escopo

- Revisao documental de higiene operacional.
- Nenhum arquivo funcional foi alterado ou removido nesta etapa.
- A revisao serve para orientar a preparacao de entrega controlada.

### Estado de referencia

- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base da revisao: 8ac307c docs: registra baseline tecnica operacional da fase 7
- Arquivos versionados no momento da revisao: 436

### Possiveis candidatos a limpeza ou verificacao

- Nenhum candidato evidente encontrado nos padroes avaliados

### Arquivos de dados ou binarios na raiz

- LISTA_RTD.xlsx
- OPERACOES_E_OPCOES.xlsm

### Observacoes

- Itens listados como candidatos nao devem ser removidos automaticamente.
- Cada item deve ser avaliado quanto a necessidade operacional, historico e impacto na entrega.
- Caso algum item seja essencial ao projeto, ele deve permanecer versionado e documentado.
- Caso algum item seja artefato local, deve ser tratado em etapa propria com commit separado.

### Conclusao da revisao

- A revisao de higiene operacional foi registrada sem alteracao funcional.
- A Fase 7 segue pronta para avaliacao controlada de limpeza, documentacao e empacotamento.

## Classificacao dos arquivos de dados na raiz

### Escopo

- Classificacao documental dos arquivos de dados ou binarios localizados na raiz.
- Nenhum arquivo foi alterado, removido ou movido nesta etapa.
- O objetivo e orientar a decisao de entrega sem risco funcional.

### Estado de referencia

- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base da classificacao: 5c60d94 docs: registra revisao de higiene operacional da fase 7

### Arquivos avaliados

- Arquivo: LISTA_RTD.xlsx
  - Tamanho em bytes: 14551
  - Ultimo commit relacionado: 5b4c3bc chore: padroniza nome da lista rtd
  - Classificacao preliminar: artefato de dados operacional
  - Acao recomendada: manter documentado ate decisao funcional explicita
- Arquivo: OPERACOES_E_OPCOES.xlsm
  - Tamanho em bytes: 247837
  - Ultimo commit relacionado: 0496b78 data: atualiza planilhas e arquivos bridge
  - Classificacao preliminar: artefato de dados operacional
  - Acao recomendada: manter documentado ate decisao funcional explicita

### Diretriz de tratamento

- Arquivos de planilha na raiz podem representar insumos operacionais, exemplos, bases manuais ou artefatos locais.
- A remocao ou movimentacao deve ocorrer somente apos confirmacao de dependencia funcional.
- Caso sejam essenciais, devem permanecer versionados e documentados.
- Caso sejam apenas artefatos locais, devem ser removidos ou movidos em etapa propria, com commit separado.
- Caso contenham dados sensiveis, devem ser tratados antes da entrega externa.

### Conclusao da classificacao

- A classificacao dos arquivos de dados da raiz foi registrada sem alteracao funcional.
- A Fase 7 segue preparada para revisao de dependencias operacionais e empacotamento controlado.

## Revisao de dependencias dos arquivos de dados da raiz

### Escopo

- Revisao documental de referencias a arquivos de dados ou planilhas.
- Nenhum arquivo foi alterado, removido ou movido nesta etapa.
- O objetivo e identificar possiveis dependencias antes de qualquer decisao de limpeza ou empacotamento.

### Estado de referencia

- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base da revisao: b0503e4 docs: classifica arquivos de dados da raiz na fase 7

### Arquivos de dados previamente classificados

- LISTA_RTD.xlsx
- OPERACOES_E_OPCOES.xlsm

### Referencias encontradas no repositorio

- .gitignore:10:OPERACOES_E_OPCOES.xlsm
- .gitignore:11:OPERACOES_E_OPCOES.xlsx
- .gitignore:12:LISTA_RTD.xlsx
- ATT/checks/check_api_routes.py:13:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- ATT/checks/check_api_routes.py:14:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- ATT/checks/check_api_routes.py:27:        "Nenhum workbook principal encontrado: OPERACOES_E_OPCOES.xlsm/xlsx"
- ATT/checks/check_end_to_end.py:10:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- ATT/checks/check_end_to_end.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- ATT/checks/check_structures.py:10:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- ATT/checks/check_structures.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- ATT/tests/test_run_derived_pipeline_rtd_integration.py:113:    assert "lista_rtd.xlsm" not in command_text
- db/import_excel.py:6:XLSX_PATH = "OPERACOES_E_OPCOES.xlsx"  # ajuste se estiver em outra pasta
- docs/checkpoints/evidencias/fase-5-diagnostico-rtd.txt:16:./.gitignore:12:LISTA_RTD.xlsx
- docs/checkpoints/evidencias/fase-5-diagnostico-rtd.txt:792:./LISTA_RTD.xlsx
- docs/checkpoints/evidencias/fase-5-diagnostico-rtd.txt:793:./backups/LISTA_RTD_fase12_rtd_option_quotes_ok.xlsm
- docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt:26:LISTA_RTD.xlsx
- docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt:634:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:180:    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
- docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt:635:scripts/refresh_rtd_option_quotes_excel.ps1.bak:2:    [string]$WorkbookPath = "C:\Users\eucal\projeto\LISTA_RTD.xlsm",
- docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt:644:scripts/refresh_rtd_option_quotes_excel.ps1.fix-param.bak:5:    [string]$WorkbookPath = "C:\Users\eucal\projeto\LISTA_RTD.xlsm",
- docs/checkpoints/evidencias/fase-5c-restauracao-rtd-historico.txt:1166:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
- docs/checkpoints/evidencias/fase-5c-restauracao-rtd-historico.txt:1308:    [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:516:scripts/create_rtd_option_quotes_sheet.py:40:        description="Cria/atualiza aba RTD_OPTION_QUOTES tabular em LISTA_RTD.xlsm."
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:517:scripts/create_rtd_option_quotes_sheet.py:42:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:589:scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:180:    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:667:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:668:scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:674:scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:685:scripts/import_lista_rtd_excel_to_option_quotes.py:588:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:686:scripts/import_lista_rtd_excel_to_option_quotes.py:600:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:689:scripts/import_lista_rtd_excel_to_option_quotes.py:694:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:690:scripts/import_lista_rtd_excel_to_option_quotes.py:704:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:731:scripts/refresh_rtd_option_quotes_excel.ps1:2:    [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:739:scripts/refresh_rtd_option_quotes_excel.ps1.bak:2:    [string]$WorkbookPath = "C:\Users\eucal\projeto\LISTA_RTD.xlsm",
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:747:scripts/refresh_rtd_option_quotes_excel.ps1.fix-param.bak:5:    [string]$WorkbookPath = "C:\Users\eucal\projeto\LISTA_RTD.xlsm",
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:757:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:765:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:766:scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:767:scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:770:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:771:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
- docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt:789:scripts/run_rtd_refresh_full.py:82:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
- docs/checkpoints/evidencias/fase-5e-validacao-integracao-rtd-derived-pipeline.txt:376:    assert "lista_rtd.xlsm" not in command_text
- docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt:101:- LISTA_RTD.xlsx
- docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:209:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:147:ATT/checks/check_structures.py:10:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:210:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:148:ATT/checks/check_structures.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1576:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:147:ATT/checks/check_structures.py:10:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- docs/checkpoints/evidencias/fase-8-diagnostico-cadastro-estruturas-leg-minima.txt:1577:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:148:ATT/checks/check_structures.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:73:## Decisão sobre fontes legadas e LISTA_RTD.xlsx
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:82:- 'LISTA_RTD.xlsx' passa a ser considerada candidata a fonte/gateway para o universo bruto RTD.
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:88:O fluxo novo não deve reconstruir o sistema em torno dos dados obsoletos. A Fase 2 deve mapear o legado existente e preparar a transição para um modelo onde a 'LISTA_RTD.xlsx' alimenta dados RTD brutos, enquanto as estruturas operacionais nascem e vivem no banco do sistema.
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:98:- 'LISTA_RTD'
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:106:| 'db/import_excel.py' | Importa 'OPERACOES_E_OPCOES.xlsx' e suas abas legadas para tabelas SQLite auxiliares | Legado isolado / importador antigo |
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:113:- 'db/import_excel.py' não consome 'LISTA_RTD.xlsx'.
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:114:- 'db/import_excel.py' ainda aponta para 'OPERACOES_E_OPCOES.xlsx'.
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:128:- criar posteriormente um gateway específico para 'LISTA_RTD.xlsx';
- docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:150:| 'db/import_excel.py' | Importador das abas legadas de 'OPERACOES_E_OPCOES.xlsx' | Legado isolado |
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:92:O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:166:LISTA_RTD.xlsm
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:178:LISTA_RTD.xlsm
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:239:A planilha 'LISTA_RTD.xlsm' foi preservada como ponte RTD oficial e testada.
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:241:A planilha RTD legada abolida foi removida do versionamento. A entrada 'LISTA_RTD.xlsx' deixou de ser tratada como ponte RTD oficial.
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:253:## Nota de supersessão — LISTA_RTD.xlsx
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:255:Esta auditoria pode conter referências históricas a 'LISTA_RTD.xlsx' feitas durante a reconciliação da ponte RTD.
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:257:A interpretação atual consolidada está definida em 'docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md':
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:259:- 'LISTA_RTD.xlsm' é a ponte RTD operacional oficial.
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:260:- 'LISTA_RTD.xlsx' é referência legada/histórica.
- docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md:261:- Referências anteriores a 'LISTA_RTD.xlsx' nesta auditoria devem ser lidas como evidência do processo de reconciliação, não como contrato operacional vigente.
- docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:396:OPERACOES_E_OPCOES
- docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:476:OPERACOES_E_OPCOES.xlsm
- docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:52:OPERACOES_E_OPCOES.xlsm
- docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:286:| 'OPERACOES_E_OPCOES.xlsm' | entrada bruta/configuração | separar dados de mercado, operação e parâmetros |
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:133:ATT/checks/check_api_routes.py:13:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:134:ATT/checks/check_api_routes.py:14:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:135:ATT/checks/check_api_routes.py:27:        "Nenhum workbook principal encontrado: OPERACOES_E_OPCOES.xlsm/xlsx"
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:145:ATT/checks/check_end_to_end.py:10:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:146:ATT/checks/check_end_to_end.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:147:ATT/checks/check_structures.py:10:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:148:ATT/checks/check_structures.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:150:db/import_excel.py:6:XLSX_PATH = "OPERACOES_E_OPCOES.xlsx"  # ajuste se estiver em outra pasta
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:195:- Ele lê diretamente 'OPERACOES_E_OPCOES.xlsx' usando 'pd.read_excel'.
- docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:203:- Os arquivos em 'ATT/checks/' fazem validações locais envolvendo workbook Excel, 'win32com' ou presença de 'OPERACOES_E_OPCOES.xlsm/xlsx'.
- docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:58:Ler diretamente OPERACOES_E_OPCOES.xlsx e importar abas específicas para tabelas internas.
- docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:64:OPERACOES_E_OPCOES.xlsx
- docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:364:git grep -n "import_excel\|bridge_ingest_csv\|read_excel\|read_csv\|BRIDGE_DIR\|OPERACOES_E_OPCOES"
- docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:376:git grep -n "win32com\|Excel.Application\|openpyxl\|xlsx\|xlsm"
- docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:47:Classificar LISTA_RTD.xlsm e _usage_audit/ antes de qualquer limpeza.
- docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:202:## Nota de supersessão — LISTA_RTD.xlsx
- docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:204:A partir da reconciliação registrada em 'docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md' e 'docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md', a ponte RTD operacional oficial é 'LISTA_RTD.xlsm'.
- docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:206:Referências anteriores a 'LISTA_RTD.xlsx' devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.
- docs/evolucoes de fases/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:210:- 'docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md'
- docs/evolucoes de fases/baseline_v1.md:180:*	run_once(xlsx_path, db_path, max_rows=10)
- docs/evolucoes de fases/baseline_v1.md:182:*	run_loop(xlsx_path, db_path, interval_s=300)
- docs/validacoes/fase-17-mapa-pastas-arquivos.md:126:LISTA_RTD.xlsx
- docs/validacoes/fase-17-mapa-pastas-arquivos.md:127:OPERACOES_E_OPCOES.xlsm
- docs/validacoes/fase-17-mapa-pastas-arquivos.md:144:- 'OPERACOES_E_OPCOES.xlsm' está versionado.
- docs/validacoes/fase-17-mapa-pastas-arquivos.md:145:- 'LISTA_RTD.xlsx' está versionado.
- docs/validacoes/fase-17-mapa-pastas-arquivos.md:156:| 'OPERACOES_E_OPCOES.xlsm' | Sim | Versionado |
- docs/validacoes/fase-17-mapa-pastas-arquivos.md:157:| 'LISTA_RTD.xlsx' | Sim | Versionado |
- limpar_repositorio_seguro.sh:11:#   ./limpar_repositorio_seguro.sh --apply --remove-xlsx-duplicado
- limpar_repositorio_seguro.sh:29:    --remove-xlsx-duplicado)
- limpar_repositorio_seguro.sh:99:  if [ -e "./OPERACOES_E_OPCOES.xlsx" ]; then
- limpar_repositorio_seguro.sh:100:    echo "./OPERACOES_E_OPCOES.xlsx" >> "$TARGETS_FILE"
- limpar_repositorio_seguro.sh:141:  echo "Para aplicar e remover também OPERACOES_E_OPCOES.xlsx:"
- limpar_repositorio_seguro.sh:142:  echo "  ./limpar_repositorio_seguro.sh --apply --remove-xlsx-duplicado"
- mapear_repositorio.sh:206:      -iname "*.xlsx" -o \
- mapear_repositorio.sh:207:      -iname "*.xlsm" -o \
- mapear_repositorio.sh:208:      -iname "*.xls" -o \
- scripts/create_rtd_option_quotes_sheet.py:40:        description="Cria/atualiza aba RTD_OPTION_QUOTES tabular em LISTA_RTD.xlsm."
- scripts/create_rtd_option_quotes_sheet.py:42:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
- scripts/dev/register_phase_7_operational_hygiene_review.sh:23:  git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls|csv|db|sqlite|sqlite3)$' || true
- scripts/dev/register_phase_7_root_data_files_classification.sh:18:  git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls|csv|db|sqlite|sqlite3)$' || true
- scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:180:    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
- scripts/fase-5e-integrar-rtd-derived-pipeline.sh:463:    assert "lista_rtd.xlsm" not in command_text
- scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
- scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
- scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
- scripts/import_lista_rtd_excel_to_option_quotes.py:588:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
- scripts/import_lista_rtd_excel_to_option_quotes.py:600:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
- scripts/import_lista_rtd_excel_to_option_quotes.py:694:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
- scripts/import_lista_rtd_excel_to_option_quotes.py:704:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
- scripts/mapear_automacao_opcoes_rtd.py:43:    ".xlsm",
- scripts/mapear_automacao_opcoes_rtd.py:44:    ".xlsx",
- scripts/mapear_automacao_opcoes_rtd.py:45:    ".xls",
- scripts/mapear_automacao_opcoes_rtd.py:59:    "excel": ["excel", "xlsm", "xlsx", "analise_robo", "hist_robo"],
- scripts/refresh_rtd_option_quotes_excel.ps1:2:    [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
- scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
- scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
- scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
- scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
- scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
- scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
- scripts/run_rtd_refresh_full.py:82:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")

### Interpretacao operacional

- Referencias textuais indicam possivel dependencia operacional, documental ou historica.
- Ausencia de referencia textual nao garante ausencia de dependencia, pois planilhas podem ser usadas manualmente ou por configuracao externa.
- Arquivos xlsx e xlsm devem ser avaliados com cuidado especial antes de remocao, movimentacao ou substituicao.
- Arquivos com macro devem ser tratados como artefatos operacionais sensiveis para entrega.

### Conclusao da revisao

- A revisao de dependencias dos arquivos de dados da raiz foi registrada sem alteracao funcional.
- A Fase 7 segue preparada para decisao explicita sobre manutencao, documentacao ou tratamento desses artefatos.

## Revisao de aderencia entre workbooks referenciados e versionados

### Escopo

- Revisao documental de aderencia entre workbooks citados e arquivos efetivamente presentes ou versionados.
- Nenhum arquivo foi alterado, removido, criado ou movido nesta etapa.
- O objetivo e identificar lacunas antes de decisao de empacotamento, limpeza ou entrega.

### Estado de referencia

- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base da revisao: 71b56c0 docs: normaliza referencias da revisao de dependencias da fase 7

### Workbooks versionados na raiz

- LISTA_RTD.xlsx
- OPERACOES_E_OPCOES.xlsm

### Matriz de presenca dos workbooks relevantes

- Arquivo: LISTA_RTD.xlsx
  - Existe no diretorio de trabalho: sim
  - Versionado pelo Git: sim
  - Ignorado pelo Git: nao
  - Quantidade de referencias textuais: 22
  - Ultimo commit relacionado: 5b4c3bc chore: padroniza nome da lista rtd
- Arquivo: LISTA_RTD.xlsm
  - Existe no diretorio de trabalho: nao
  - Versionado pelo Git: nao
  - Ignorado pelo Git: nao
  - Quantidade de referencias textuais: 46
  - Ultimo commit relacionado: nao aplicavel
- Arquivo: OPERACOES_E_OPCOES.xlsm
  - Existe no diretorio de trabalho: sim
  - Versionado pelo Git: sim
  - Ignorado pelo Git: nao
  - Quantidade de referencias textuais: 19
  - Ultimo commit relacionado: 0496b78 data: atualiza planilhas e arquivos bridge
- Arquivo: OPERACOES_E_OPCOES.xlsx
  - Existe no diretorio de trabalho: nao
  - Versionado pelo Git: nao
  - Ignorado pelo Git: sim
  - Quantidade de referencias textuais: 21
  - Ultimo commit relacionado: nao aplicavel

### Pontos de atencao operacional

- Referencias a workbooks ausentes ou nao versionados podem indicar dependencia historica, dependencia externa ou lacuna de empacotamento.
- Arquivos presentes e versionados, mas tambem ignorados, podem representar artefatos rastreados antes da regra de ignore.
- Divergencias entre extensoes xlsx e xlsm devem ser tratadas com cuidado, pois arquivos xlsm podem conter macros e fluxos operacionais manuais.
- Nenhuma decisao automatica de remocao, inclusao ou renomeacao deve ser tomada apenas por esta revisao.

### Conclusao da revisao

- A aderencia entre workbooks referenciados e versionados foi registrada sem alteracao funcional.
- A Fase 7 segue preparada para uma decisao explicita de empacotamento e tratamento de artefatos Excel.

## Diretriz provisoria de empacotamento dos artefatos Excel

### Escopo

- Registro documental de diretriz provisoria para tratamento de arquivos Excel na entrega.
- Nenhum arquivo foi alterado, removido, criado ou movido nesta etapa.
- A diretriz se baseia nas revisoes de classificacao, dependencias e aderencia entre referencias e arquivos versionados.

### Estado de referencia

- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base da diretriz: 411cd31 docs: revisa aderencia dos workbooks da fase 7

### Diretriz por artefato

- Arquivo: LISTA_RTD.xlsx
  - Estado observado: presente e versionado na raiz.
  - Leitura operacional: artefato legado ou historico, com referencias documentais relevantes.
  - Diretriz provisoria: manter no repositorio ate decisao funcional explicita.
  - Restricao para entrega externa: revisar conteudo antes de empacotar, pois pode conter dados operacionais ou sensiveis.

- Arquivo: LISTA_RTD.xlsm
  - Estado observado: referenciado com frequencia, mas ausente e nao versionado na raiz.
  - Leitura operacional: possivel dependencia operacional externa, historica ou nao empacotada.
  - Diretriz provisoria: nao criar, nao renomear e nao substituir automaticamente.
  - Restricao para entrega externa: registrar como lacuna ou pre-requisito externo caso ainda seja necessario ao fluxo real.

- Arquivo: OPERACOES_E_OPCOES.xlsm
  - Estado observado: presente e versionado na raiz.
  - Leitura operacional: artefato de dados operacional com potencial uso em validacoes locais e fluxos legados.
  - Diretriz provisoria: manter versionado ate decisao funcional explicita.
  - Restricao para entrega externa: revisar conteudo e macros antes de empacotar.

- Arquivo: OPERACOES_E_OPCOES.xlsx
  - Estado observado: referenciado, ausente, nao versionado e ignorado pelo Git.
  - Leitura operacional: referencia legada ou alternativa ao workbook principal.
  - Diretriz provisoria: nao incluir na entrega sem decisao explicita.
  - Restricao para entrega externa: se necessario, documentar como arquivo local esperado ou substituir por fixture controlada.

### Regras provisorias para entrega

- Nao empacotar arquivos Excel com dados reais sem revisao de conteudo.
- Nao empacotar arquivos com macro sem revisao especifica de seguranca e necessidade operacional.
- Nao substituir extensoes xlsx por xlsm, ou xlsm por xlsx, sem validacao funcional.
- Nao inferir que arquivo ausente deve ser criado apenas por haver referencia textual.
- Caso a entrega precise ser reproduzivel sem planilhas reais, criar etapa futura para fixtures anonimizadas ou dados de exemplo.

### Conclusao da diretriz

- A diretriz provisoria de empacotamento dos artefatos Excel foi registrada sem alteracao funcional.
- A Fase 7 segue preparada para revisao de sensibilidade dos artefatos versionados e definicao final de pacote de entrega.
