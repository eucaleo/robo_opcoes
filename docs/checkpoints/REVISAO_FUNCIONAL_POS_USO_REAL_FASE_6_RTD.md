# FASE 6 — EXECUÇÃO RTD

## Objetivo

Garantir que conexão RTD aberta resulte em coleta efetiva, persistência em banco e atualização visível na UI.

## Base da fase

- Branch: reinicio-normalizacao-idioma-ptbr
- Commit base:
4dd23509422c08f5f586ababca4287230c4a3207

## Pontos previstos na rota

- Adaptador RTD.
- Serviço de atualização RTD.
- Integração com botão Atualizar Dados.
- Persistência em rtd_option_quotes.
- Normalização de tickers.
- Atualização da tela após coleta.
- Mensagem quando RTD não retorna dados.

## Arquivos e referências RTD encontradas

UI/components/structure_editor_dialog.py:38:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
UI/components/structure_editor_dialog.py:39:from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
UI/components/structure_editor_dialog.py:393:        repo = RtdOptionQuotesRepository(getattr(self, "_db_path", "dados/app.db"))
UI/components/structure_editor_dialog.py:394:        service = StructureLegRtdEnrichmentService(repo)
UI/components/structure_editor_dialog.py:400:        """Compatibilidade: permite leg manual completa mesmo sem cotacao RTD."""
UI/components/structure_editor_dialog.py:419:            preserva compatibilidade e nao acessa RTD.
UI/components/structure_editor_dialog.py:434:                self._refresh_rtd_quote_for_symbol(symbol)
UI/components/structure_editor_dialog.py:446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
UI/components/structure_editor_dialog.py:447:        """Atualiza uma opção avulsa no RTD/Excel e importa para o cache local."""
UI/components/structure_editor_dialog.py:459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
UI/components/structure_editor_dialog.py:460:        workbook_path = project_root / "LISTA_RTD.xlsm"
UI/components/structure_editor_dialog.py:474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
UI/components/structure_editor_dialog.py:477:            raise ValueError(f"Workbook RTD não encontrado: {workbook_path}")
UI/components/structure_editor_dialog.py:515:                "Não foi possível atualizar a cotação RTD para "
Binary file UI/components/__pycache__/structure_editor_dialog.cpython-313.pyc matches
UI/main_window.py:55:        # Controle de atualização automática da UI/RTD.
UI/main_window.py:601:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
UI/main_window.py:702:* Excel RTD  CSV Bridge
Binary file UI/__pycache__/main_window.cpython-313.pyc matches
scripts/audit_rtd_option_quotes.py:3:Audita a tabela rtd_option_quotes em um banco SQLite.
scripts/audit_rtd_option_quotes.py:7:    python scripts/audit_rtd_option_quotes.py --db dados/app.db
scripts/audit_rtd_option_quotes.py:8:    python scripts/audit_rtd_option_quotes.py --db dados/app.db --json
scripts/audit_rtd_option_quotes.py:23:TABLE_NAME = "rtd_option_quotes"
scripts/audit_rtd_option_quotes.py:218:    print("Auditoria rtd_option_quotes")
scripts/audit_rtd_option_quotes.py:254:        description="Audita a tabela rtd_option_quotes em um banco SQLite."
scripts/build_rtd_symbols.py:81:def collect_from_rtd_option_quotes(cur):
scripts/build_rtd_symbols.py:82:    if not table_exists(cur, "rtd_option_quotes"):
scripts/build_rtd_symbols.py:87:        FROM rtd_option_quotes
scripts/build_rtd_symbols.py:129:            quote_symbols = collect_from_rtd_option_quotes(cur)
scripts/build_rtd_symbols.py:130:            sources.append(("rtd_option_quotes", quote_symbols))
scripts/create_rtd_option_quotes_sheet.py:27:RTD = 'RTD("btg_pro_rtd","","{topic}",$A{row})'
scripts/create_rtd_option_quotes_sheet.py:31:    return "=" + RTD.format(topic=topic, row=row)
scripts/create_rtd_option_quotes_sheet.py:40:        description="Cria/atualiza aba RTD_OPTION_QUOTES tabular em LISTA_RTD.xlsm."
scripts/create_rtd_option_quotes_sheet.py:42:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
scripts/create_rtd_option_quotes_sheet.py:48:    parser.add_argument("--sheet", default="RTD_OPTION_QUOTES")
scripts/dev/close_phase_5f_ui_pipeline.sh:37:    - Cotacoes RTD atualizadas: 4
scripts/dev/close_phase_5f_ui_pipeline.sh:52:    aab7e92 Integra importacao RTD CSV ao pipeline derived
scripts/dev/close_phase_5f_ui_pipeline.sh:53:    a64a464 Restaura e valida cadeia historica RTD de opcoes
scripts/dev/close_phase_5f_ui_pipeline.sh:81:    Compiling 'ATT/tests\\test_run_derived_pipeline_rtd_integration.py'...
scripts/dev/close_phase_5f_ui_pipeline.sh:90:    [PIPELINE] Importando cotacoes RTD para derived.db...
scripts/dev/close_phase_5f_ui_pipeline.sh:91:    Importacao RTD wide CSV
scripts/dev/close_phase_5f_ui_pipeline.sh:99:    Auditoria rtd_option_quotes
scripts/dev/close_phase_5f_ui_pipeline.sh:101:    Tabela: rtd_option_quotes
scripts/dev/close_phase_5f_ui_pipeline.sh:123:      Cotacoes RTD atualizadas: 4
scripts/dev/close_phase_5f_ui_pipeline.sh:135:      "rtd_import": {
scripts/dev/close_phase_5f_ui_pipeline.sh:144:      "rtd_quotes_updated": 4,
scripts/dev/close_phase_5f_ui_pipeline.sh:148:        "rtd_option_quotes": 4,
scripts/dev/close_phase_5f_ui_pipeline.sh:163:| Cotacoes RTD atualizadas exibidas no resumo | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:182:- cotacoes RTD atualizadas;
scripts/dev/close_phase_6_integrated_validation.sh:17:- ingestao RTD;
scripts/dev/close_phase_6_integrated_validation.sh:100:    - Cotacoes RTD atualizadas: 4
scripts/dev/close_phase_6_integrated_validation.sh:119:| Cotacoes RTD atualizadas exibidas no resumo | OK |
scripts/dev/close_phase_6_integrated_validation.sh:137:| Cotacoes RTD atualizadas | 4 |
scripts/dev/close_phase_6_integrated_validation.sh:151:- cotacoes RTD atualizadas;
scripts/dev/open_phase_6_integrated_validation.sh:19:- ingestao RTD;
scripts/dev/open_phase_6_integrated_validation.sh:34:- Importacao de cotacoes RTD
scripts/dev/open_phase_6_integrated_validation.sh:35:- Auditoria da tabela rtd_option_quotes
scripts/dev/open_phase_6_integrated_validation.sh:67:    - Cotacoes RTD atualizadas: 4
scripts/dev/open_phase_6_integrated_validation.sh:94:- Nenhuma regressao em RTD
scripts/dev/open_phase_6_integrated_validation.sh:103:- Importacao RTD retorna sem erros
scripts/dev/open_phase_6_integrated_validation.sh:104:- Auditoria de RTD retorna status ok
scripts/dev/open_phase_6_integrated_validation.sh:108:- Resumo operacional apresenta cotacoes RTD atualizadas
scripts/dev/open_phase_6_integrated_validation.sh:132:- rtd_option_quotes possui cotacoes atualizadas
scripts/dev/register_phase_7_delivery_package_matrix.sh:118:  echo "- Validar se LISTA_RTD.xlsm ainda e necessario ao fluxo real, pois ha muitas referencias textuais e ausencia no repositorio."
scripts/dev/register_phase_7_delivery_package_matrix.sh:120:  echo "- Confirmar se LISTA_RTD.xlsx e OPERACOES_E_OPCOES.xlsm devem permanecer no repositorio ou migrar para fixture controlada."
scripts/dev/register_phase_7_delivery_readiness_checklist.sh:92:  echo "- Decidir se LISTA_RTD.xlsx permanece no repositorio, entra no pacote interno ou deve ser substituido por fixture."
scripts/dev/register_phase_7_delivery_readiness_checklist.sh:94:  echo "- Decidir se LISTA_RTD.xlsm e pre-requisito externo, dependencia historica ou referencia obsoleta."
scripts/dev/register_phase_7_excel_packaging_guideline.sh:34:  echo "- Arquivo: LISTA_RTD.xlsx"
scripts/dev/register_phase_7_excel_packaging_guideline.sh:40:  echo "- Arquivo: LISTA_RTD.xlsm"
scripts/dev/register_phase_7_root_data_dependencies_review.sh:19:    git grep -n -I -E 'LISTA_RTD|OPERACOES_E_OPCOES|xlsx|xlsm|xls' -- . \
scripts/dev/register_phase_7_root_data_dependencies_review.sh:43:  echo "- LISTA_RTD.xlsx"
scripts/dev/register_phase_7_workbook_reference_gap_review.sh:18:  "LISTA_RTD.xlsx"
scripts/dev/register_phase_7_workbook_reference_gap_review.sh:19:  "LISTA_RTD.xlsm"
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:32:        | grep -Ei 'structure|estrutura|payoff|decision|decis|pipeline|rtd|repository|service|dialog|editor|manual|leg' \
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:72:    if any(term in low for term in ["structure", "estrutura", "leg", "payoff", "decision", "decis", "rtd", "quote"]):
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:83:    "rtd_option_quotes",
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:108:    if any(term in name for term in ["structure", "leg", "payoff", "decision", "rtd", "quote"]):
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:68:        "rtd_option_quotes",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:70:        "rtd_analise_robo_legs",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:82:        if any(t in low for t in ["structure", "leg", "pricing", "payoff", "decision", "rtd", "manual"]):
scripts/fase-3e-fix-facade-manual-sem-alias.sh:103:             usa MarketSnapshotSelector manual > rtd.
scripts/fase-3e-fix-facade-manual-sem-alias.sh:173:            #  2. Seleciona snapshot (manual > rtd)
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:112:        "rtd_option_quotes",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:263:- Excel apenas como ponte RTD.
scripts/fase-5-diagnostico-rtd.sh:4:OUT="docs/checkpoints/evidencias/fase-5-diagnostico-rtd.txt"
scripts/fase-5-diagnostico-rtd.sh:8:  echo "FASE 5 - DIAGNOSTICO RTD"
scripts/fase-5-diagnostico-rtd.sh:22:  echo "== Busca por RTD no projeto =="
scripts/fase-5-diagnostico-rtd.sh:24:    -E "RTD|rtd|rtd_option_quotes|option_quotes|quotes" . 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:34:    -E "connect_raw|connect_derived|sqlite|derived.db|raw.db|rtd_option_quotes" db repositories services scripts UI 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:37:  echo "== Arquivos candidatos RTD =="
scripts/fase-5-diagnostico-rtd.sh:39:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' \) \
scripts/fase-5-diagnostico-rtd.sh:62:        for target in ["rtd_option_quotes", "payoff_curve_points", "structure_decisions"]:
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:4:OUT="docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:8:  echo "FASE 5B - DIAGNOSTICO RTD CADEIA REAL E HISTORICO"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:22:  echo "== Arquivos rastreados relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:23:  git ls-files | grep -Ei "rtd|quote|market|snapshot" | sort
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:26:  echo "== Arquivos atuais em scripts relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:28:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:33:  echo "== Arquivos atuais em infra relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:35:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:40:  echo "== Arquivos atuais em repositories/services relacionados a RTD/quotes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:42:    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:47:  echo "== Historico Git de scripts RTD conhecidos =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:49:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:50:    scripts/import_rtd_links_to_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:51:    scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:52:    scripts/build_rtd_symbols.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:53:    scripts/run_rtd_refresh_full.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:54:    scripts/audit_rtd_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:55:    scripts/refresh_rtd_option_quotes_excel.ps1 \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:56:    infra/bootstrap_rtd_option_quotes_schema.py
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:64:  echo "== Alteracoes historicas por nome contendo RTD em scripts/infra =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:65:  git log --all --name-status -- scripts infra | grep -Ei "commit |rtd|quote|market" | head -500
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:68:  echo "== Conteudo atual dos scripts RTD existentes =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:70:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:71:    scripts/import_rtd_links_to_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:72:    scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:73:    scripts/build_rtd_symbols.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:74:    scripts/run_rtd_refresh_full.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:75:    scripts/audit_rtd_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:76:    infra/bootstrap_rtd_option_quotes_schema.py
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:90:  echo "== Testes vigentes relacionados ao pipeline/import/audit RTD =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:92:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:93:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:94:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:95:    ATT/tests/test_rtd_option_quotes_repository_contract.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:96:    ATT/tests/test_structure_leg_rtd_enrichment_service.py
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:110:  echo "== Schema e contagem rtd_option_quotes em app.db e derived.db =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:127:            "SELECT name FROM sqlite_master WHERE type='table' AND name='rtd_option_quotes'"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:129:        print(f"rtd_option_quotes existe: {bool(exists)}")
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:133:        count = con.execute("SELECT COUNT(*) AS c FROM rtd_option_quotes").fetchone()["c"]
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:137:        for col in con.execute("PRAGMA table_info(rtd_option_quotes)").fetchall():
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:144:            FROM rtd_option_quotes
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:158:  echo "== Arquivos de dados RTD atuais =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:159:  ls -la dados | grep -Ei "rtd|quote|lista" || true
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:162:  echo "== Primeiras linhas dados/RTD_LINKS.csv se existir =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:163:  if [ -f dados/RTD_LINKS.csv ]; then
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:166:p = Path("dados/RTD_LINKS.csv")
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:174:    echo "dados/RTD_LINKS.csv ausente"
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:178:  echo "== Busca por PowerShell/Excel/COM/RTD nos arquivos atuais =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:180:    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
scripts/fase-5c-restaurar-rtd-historico.sh:4:OUT="docs/checkpoints/evidencias/fase-5c-restauracao-rtd-historico.txt"
scripts/fase-5c-restaurar-rtd-historico.sh:8:  "infra/bootstrap_rtd_option_quotes_schema.py"
scripts/fase-5c-restaurar-rtd-historico.sh:9:  "scripts/audit_rtd_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:10:  "scripts/build_rtd_symbols.py"
scripts/fase-5c-restaurar-rtd-historico.sh:11:  "scripts/create_rtd_option_quotes_sheet.py"
scripts/fase-5c-restaurar-rtd-historico.sh:12:  "scripts/import_lista_rtd_excel_to_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:13:  "scripts/import_rtd_links_to_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:14:  "scripts/import_rtd_option_quotes_wide_csv.py"
scripts/fase-5c-restaurar-rtd-historico.sh:15:  "scripts/mapear_automacao_opcoes_rtd.py"
scripts/fase-5c-restaurar-rtd-historico.sh:16:  "scripts/refresh_rtd_option_quotes_excel.ps1"
scripts/fase-5c-restaurar-rtd-historico.sh:17:  "scripts/run_lista_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:18:  "scripts/run_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:19:  "scripts/run_rtd_refresh_full.py"
scripts/fase-5c-restaurar-rtd-historico.sh:20:  "scripts/seed_current_rtd_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:21:  "ATT/tests/test_audit_rtd_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:22:  "ATT/tests/test_import_rtd_links_to_option_quotes.py"
scripts/fase-5c-restaurar-rtd-historico.sh:23:  "ATT/tests/test_run_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:24:  "ATT/tests/test_rtd_option_quotes_repository_contract.py"
scripts/fase-5c-restaurar-rtd-historico.sh:29:  echo "FASE 5C - RESTAURACAO RTD HISTORICO"
scripts/fase-5c-restaurar-rtd-historico.sh:60:  echo "== Arquivos RTD restaurados =="
scripts/fase-5c-restaurar-rtd-historico.sh:70:    infra/bootstrap_rtd_option_quotes_schema.py \
scripts/fase-5c-restaurar-rtd-historico.sh:71:    scripts/audit_rtd_option_quotes.py \
scripts/fase-5c-restaurar-rtd-historico.sh:72:    scripts/build_rtd_symbols.py \
scripts/fase-5c-restaurar-rtd-historico.sh:73:    scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5c-restaurar-rtd-historico.sh:74:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5c-restaurar-rtd-historico.sh:75:    scripts/run_rtd_refresh_full.py
scripts/fase-5c-restaurar-rtd-historico.sh:86:  echo "== PowerShell RTD restaurado se existir =="
scripts/fase-5c-restaurar-rtd-historico.sh:87:  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
scripts/fase-5c-restaurar-rtd-historico.sh:88:    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase-5c-restaurar-rtd-historico.sh:94:  echo "== Py compile dos arquivos Python RTD restaurados =="
scripts/fase-5c-restaurar-rtd-historico.sh:110:    echo "Nenhum arquivo Python RTD restaurado para compilar"
scripts/fase-5c-restaurar-rtd-historico.sh:114:  echo "== Testes RTD restaurados disponíveis =="
scripts/fase-5c-restaurar-rtd-historico.sh:116:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5c-restaurar-rtd-historico.sh:117:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5c-restaurar-rtd-historico.sh:118:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5c-restaurar-rtd-historico.sh:119:    ATT/tests/test_rtd_option_quotes_repository_contract.py
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:4:OUT="docs/checkpoints/evidencias/fase-5d-validacao-rtd-restaurado-operacional.txt"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:8:  echo "FASE 5D - VALIDACAO OPERACIONAL RTD RESTAURADO"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:23:  if [ -f dados/RTD_LINKS.csv ]; then
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:24:    ls -l dados/RTD_LINKS.csv
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:27:    sed -n '1,10p' dados/RTD_LINKS.csv
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:29:    echo "ERRO: dados/RTD_LINKS.csv ausente"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:34:  if [ -f dados/rtd_symbols.txt ]; then
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:35:    ls -l dados/rtd_symbols.txt
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:37:    cat dados/rtd_symbols.txt
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:39:    echo "dados/rtd_symbols.txt ausente"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:44:  python scripts/audit_rtd_option_quotes.py --db dados/app.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:48:  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:52:  python scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:53:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:59:  python scripts/import_rtd_option_quotes_wide_csv.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:60:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:65:  echo "== Pipeline RTD restaurado - app.db =="
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:66:  python scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:67:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:72:  echo "== Pipeline RTD restaurado - derived.db =="
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:73:  python scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:74:    --csv dados/RTD_LINKS.csv \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:80:  python scripts/audit_rtd_option_quotes.py --db dados/app.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:84:  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:108:              AND name='rtd_option_quotes'
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:111:        print("rtd_option_quotes existe:", bool(exists))
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:122:            FROM rtd_option_quotes
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:140:            FROM rtd_option_quotes
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:152:  echo "== Testes RTD restaurados novamente =="
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:154:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:155:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:156:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:157:    ATT/tests/test_rtd_option_quotes_repository_contract.py
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:4:OUT="docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt"
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:8:  echo "FASE 5E - DIAGNOSTICO INTEGRACAO RTD NO DERIVED PIPELINE"
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:30:  echo "== Ocorrencias de rtd_quotes_updated =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:31:  grep -R "rtd_quotes_updated" -n . \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:50:  echo "== Ocorrencias de RTD na UI/controladores =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:51:  grep -R "RTD\\|rtd\\|Atualizar Dados\\|Executar Pipeline" -n \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:32:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:47:def _parse_rtd_pipeline_metrics(output: str) -> dict:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:48:    """Extrai métricas textuais emitidas pelo pipeline RTD restaurado."""
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:57:        match = _RTD_METRIC_RE.match(line)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:67:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:69:    if not rtd_result:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:72:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:75:def _run_rtd_option_quotes_import(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:77:    csv_path: str = "dados/RTD_LINKS.csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:81:    Executa a cadeia operacional RTD já restaurada contra o derived.db.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:84:    - Usa somente CSV local dados/RTD_LINKS.csv.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:85:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:86:    - Delega importação + auditoria para scripts/run_rtd_option_quotes_pipeline.py.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:89:    pipeline_script = repo_root / "scripts" / "run_rtd_option_quotes_pipeline.py"
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:98:            "message": f"Script RTD não encontrado: {pipeline_script}",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:110:            "message": f"CSV RTD não encontrado: {resolved_csv}",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:142:    metrics = _parse_rtd_pipeline_metrics(stdout)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:192:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:197:    - Inclui a quantidade de cotações RTD inseridas/atualizadas.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:199:    - Apenas lê contagens do banco depois que o pipeline RTD CSV já rodou.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:243:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:244:            "rtd_import": rtd_result,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:245:            "warnings": int((rtd_result or {}).get("warnings") or 0),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:246:            "errors": int((rtd_result or {}).get("errors") or 0),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:266:        "--skip-rtd",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:268:        help="Não importar dados/RTD_LINKS.csv para rtd_option_quotes no derived.db",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:271:        "--rtd-csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:272:        default="dados/RTD_LINKS.csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:273:        help="Caminho do CSV RTD usado pelo pipeline derivado",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:288:    rtd_result = None
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:289:    if args.skip_rtd:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:290:        print("\n[PIPELINE] Importação RTD pulada por --skip-rtd.")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:291:        rtd_result = {
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:302:        print("\n[PIPELINE] Importando cotações RTD para derived.db...")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:303:        rtd_result = _run_rtd_option_quotes_import(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:305:            csv_path=args.rtd_csv,
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:309:        if int(rtd_result.get("returncode") or 0) != 0:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:310:            print("[ERROR] PIPELINE FALHOU: importação/auditoria RTD falhou")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:311:            if rtd_result.get("message"):
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:312:                print(f"[ERROR] {rtd_result.get('message')}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:313:            summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:315:            return int(rtd_result.get("returncode") or 1)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:321:        summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:326:    summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:334:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:350:cat > ATT/tests/test_run_derived_pipeline_rtd_integration.py <<'PY'
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:371:def test_parse_rtd_pipeline_metrics_from_stdout():
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:375:Importação RTD wide CSV
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:384:    assert module._parse_rtd_pipeline_metrics(output) == {
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:392:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:395:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:396:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:397:    assert module._rtd_quotes_updated_count(None) == 0
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:400:def test_run_rtd_option_quotes_import_uses_csv_pipeline_without_excel_or_powershell(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:411:    (scripts_dir / "run_rtd_option_quotes_pipeline.py").write_text(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:412:        "# fake rtd csv pipeline\n",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:415:    (dados_dir / "RTD_LINKS.csv").write_text(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:439:    result = module._run_rtd_option_quotes_import(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:441:        csv_path="dados/RTD_LINKS.csv",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:454:    assert command[1].endswith("run_rtd_option_quotes_pipeline.py")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:456:    assert "dados/RTD_LINKS.csv" in command
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:462:    assert "refresh_rtd_option_quotes_excel" not in command_text
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:463:    assert "lista_rtd.xlsm" not in command_text
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:4:OUT="docs/checkpoints/evidencias/fase-5e-validacao-integracao-rtd-derived-pipeline.txt"
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:8:  echo "FASE 5E - VALIDACAO INTEGRACAO RTD NO DERIVED PIPELINE"
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:27:  sed -n '1,260p' ATT/tests/test_run_derived_pipeline_rtd_integration.py
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:35:  echo "== Testes focados RTD/pipeline =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:37:    ATT/tests/test_run_derived_pipeline_rtd_integration.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:38:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:39:    ATT/tests/test_audit_rtd_option_quotes.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:40:    ATT/tests/test_import_rtd_links_to_option_quotes.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:41:    ATT/tests/test_rtd_option_quotes_repository_contract.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:50:  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:53:  echo "== Estado SQLite rtd_option_quotes derived.db =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:66:        "SELECT name FROM sqlite_master WHERE type='table' AND name='rtd_option_quotes'"
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:68:    print("rtd_option_quotes existe:", bool(exists))
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:77:            FROM rtd_option_quotes
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:84:            FROM rtd_option_quotes
scripts/fase5_automacao_gitbash.sh:70:- quais cotações RTD foram atualizadas;
scripts/fase5_automacao_gitbash.sh:94:- nenhuma cotação RTD foi atualizada;
scripts/fase5_automacao_gitbash.sh:140:| Cotações RTD atualizadas | Quantidade de cotações atualizadas |
scripts/fase5_automacao_gitbash.sh:152:    scripts/run_rtd_option_quotes_pipeline.py
scripts/fase5_automacao_gitbash.sh:153:    scripts/run_rtd_refresh_full.py
scripts/fase5_automacao_gitbash.sh:154:    scripts/refresh_rtd_option_quotes_excel.ps1
scripts/fase5_automacao_gitbash.sh:155:    repositories/rtd_option_quotes_repository.py
scripts/fase5_automacao_gitbash.sh:157:    ATT/tests/test_run_rtd_option_quotes_pipeline.py
scripts/fase5_automacao_gitbash.sh:158:    ATT/tests/test_run_derived_pipeline_rtd_integration.py
scripts/fase5_automacao_gitbash.sh:159:    ATT/tests/test_rtd_option_quotes_repository_contract.py
scripts/fase5_automacao_gitbash.sh:160:    ATT/tests/test_structure_leg_rtd_enrichment_service.py
scripts/fase5_automacao_gitbash.sh:164:    scripts/refresh_rtd_symbol_to_option_quotes.py
scripts/fase5_automacao_gitbash.sh:176:| Contadores de RTD identificados ou criados | A validar |
scripts/fase5_automacao_gitbash.sh:392:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_automacao_gitbash.sh:402:  echo "- Confirmar se há contadores de RTD, payoff e decisões."
scripts/fase5_automacao_gitbash.sh:421:  "scripts/run_rtd_option_quotes_pipeline.py"
scripts/fase5_automacao_gitbash.sh:422:  "scripts/run_rtd_refresh_full.py"
scripts/fase5_automacao_gitbash.sh:497:  check_term "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_automacao_gitbash.sh:510:  write_occurrences "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_automacao_gitbash.sh:525:  echo "- cotações RTD atualizadas;"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:63:  run_grep "run_derived_pipeline|run_rtd_option_quotes_pipeline|run_rtd_refresh_full|payoff_curve_points|structure_decisions|RTD|rtd|payoff|decision|decisions"
scripts/fase5_buscar_fluxo_atualizar_dados.sh:73:  echo "- Confirmar se há contadores de RTD, payoff e decisões."
scripts/fase5_checar_resumo_pipeline.sh:12:  "scripts/run_rtd_option_quotes_pipeline.py"
scripts/fase5_checar_resumo_pipeline.sh:13:  "scripts/run_rtd_refresh_full.py"
scripts/fase5_checar_resumo_pipeline.sh:88:  check_term "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_checar_resumo_pipeline.sh:101:  write_occurrences "Cotações RTD" "RTD|rtd|quotes|option_quotes|cotacoes|cotações"
scripts/fase5_checar_resumo_pipeline.sh:116:  echo "- cotações RTD atualizadas;"
scripts/import_legacy_structure_legs.py:28:            "Importa pernas legadas manual/rtd para structure_legs "
scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
scripts/import_lista_rtd_excel_to_option_quotes.py:6:        -> aba RTD_OPTION_QUOTES ou RTD_PROBE_OPTIONS
scripts/import_lista_rtd_excel_to_option_quotes.py:7:        -> tabela rtd_option_quotes
scripts/import_lista_rtd_excel_to_option_quotes.py:10:    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db
scripts/import_lista_rtd_excel_to_option_quotes.py:11:    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db --dry-run
scripts/import_lista_rtd_excel_to_option_quotes.py:12:    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db --json
scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
scripts/import_lista_rtd_excel_to_option_quotes.py:28:DEFAULT_SHEETS = ["RTD_OPTION_QUOTES", "RTD_PROBE_OPTIONS", "RTD-BTG LISTA"]
scripts/import_lista_rtd_excel_to_option_quotes.py:220:    - aguarda RTD atualizar;
scripts/import_lista_rtd_excel_to_option_quotes.py:342:        "Nenhuma aba RTD encontrada. "
scripts/import_lista_rtd_excel_to_option_quotes.py:427:    columns = get_table_columns(conn, "rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:430:        raise RuntimeError("Tabela rtd_option_quotes não encontrada no banco.")
scripts/import_lista_rtd_excel_to_option_quotes.py:436:            "Tabela rtd_option_quotes está sem colunas obrigatórias: "
scripts/import_lista_rtd_excel_to_option_quotes.py:458:                "SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? LIMIT 1",
scripts/import_lista_rtd_excel_to_option_quotes.py:495:            "source": "lista_rtd_excel",
scripts/import_lista_rtd_excel_to_option_quotes.py:502:            UPDATE rtd_option_quotes
scripts/import_lista_rtd_excel_to_option_quotes.py:534:            INSERT INTO rtd_option_quotes (
scripts/import_lista_rtd_excel_to_option_quotes.py:588:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
scripts/import_lista_rtd_excel_to_option_quotes.py:600:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/import_lista_rtd_excel_to_option_quotes.py:607:            "Nome da aba. Se omitido, tenta RTD_OPTION_QUOTES "
scripts/import_lista_rtd_excel_to_option_quotes.py:608:            "e depois RTD_PROBE_OPTIONS."
scripts/import_lista_rtd_excel_to_option_quotes.py:694:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:704:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_rtd_links_to_option_quotes.py:3:Importa dados verticais de dados/RTD_LINKS.csv para rtd_option_quotes.
scripts/import_rtd_links_to_option_quotes.py:14:python scripts/import_rtd_links_to_option_quotes.py --csv dados/RTD_LINKS.csv --db dados/app.db
scripts/import_rtd_links_to_option_quotes.py:15:python scripts/import_rtd_links_to_option_quotes.py --csv dados/RTD_LINKS.csv --db dados/app.db --dry-run
scripts/import_rtd_links_to_option_quotes.py:212:        "source": "rtd_links",
scripts/import_rtd_links_to_option_quotes.py:307:        FROM rtd_option_quotes
scripts/import_rtd_links_to_option_quotes.py:323:        "ativo_base = COALESCE(excluded.ativo_base, rtd_option_quotes.ativo_base)",
scripts/import_rtd_links_to_option_quotes.py:324:        "call_put = COALESCE(excluded.call_put, rtd_option_quotes.call_put)",
scripts/import_rtd_links_to_option_quotes.py:325:        "strike = COALESCE(excluded.strike, rtd_option_quotes.strike)",
scripts/import_rtd_links_to_option_quotes.py:326:        "vencimento = COALESCE(excluded.vencimento, rtd_option_quotes.vencimento)",
scripts/import_rtd_links_to_option_quotes.py:327:        "ultimo_preco = COALESCE(excluded.ultimo_preco, rtd_option_quotes.ultimo_preco)",
scripts/import_rtd_links_to_option_quotes.py:328:        "ultima_quantidade = COALESCE(excluded.ultima_quantidade, rtd_option_quotes.ultima_quantidade)",
scripts/import_rtd_links_to_option_quotes.py:329:        "bid = COALESCE(excluded.bid, rtd_option_quotes.bid)",
scripts/import_rtd_links_to_option_quotes.py:330:        "ask = COALESCE(excluded.ask, rtd_option_quotes.ask)",
scripts/import_rtd_links_to_option_quotes.py:331:        "volume = COALESCE(excluded.volume, rtd_option_quotes.volume)",
scripts/import_rtd_links_to_option_quotes.py:332:        "iv = COALESCE(excluded.iv, rtd_option_quotes.iv)",
scripts/import_rtd_links_to_option_quotes.py:333:        "delta = COALESCE(excluded.delta, rtd_option_quotes.delta)",
scripts/import_rtd_links_to_option_quotes.py:334:        "gamma = COALESCE(excluded.gamma, rtd_option_quotes.gamma)",
scripts/import_rtd_links_to_option_quotes.py:335:        "theta = COALESCE(excluded.theta, rtd_option_quotes.theta)",
scripts/import_rtd_links_to_option_quotes.py:336:        "vega = COALESCE(excluded.vega, rtd_option_quotes.vega)",
scripts/import_rtd_links_to_option_quotes.py:343:        INSERT INTO rtd_option_quotes ({columns_sql})
scripts/import_rtd_links_to_option_quotes.py:386:        description="Importa dados/RTD_LINKS.csv para rtd_option_quotes"
scripts/import_rtd_links_to_option_quotes.py:391:        default="dados/RTD_LINKS.csv",
scripts/import_rtd_links_to_option_quotes.py:392:        help="Caminho do CSV RTD_LINKS.csv",
scripts/import_rtd_links_to_option_quotes.py:419:    print("Importação RTD_LINKS.csv -> rtd_option_quotes")
scripts/import_rtd_option_quotes_wide_csv.py:14:from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema
scripts/import_rtd_option_quotes_wide_csv.py:196:                "source": "BTG_RTD_EXCEL",
scripts/import_rtd_option_quotes_wide_csv.py:207:        CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo_opcao
scripts/import_rtd_option_quotes_wide_csv.py:208:        ON rtd_option_quotes(codigo_opcao)
scripts/import_rtd_option_quotes_wide_csv.py:226:    ensure_rtd_option_quotes_schema(db_path)
scripts/import_rtd_option_quotes_wide_csv.py:237:                "SELECT id, created_at FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
scripts/import_rtd_option_quotes_wide_csv.py:251:                    UPDATE rtd_option_quotes
scripts/import_rtd_option_quotes_wide_csv.py:299:                    INSERT INTO rtd_option_quotes (
scripts/import_rtd_option_quotes_wide_csv.py:369:        print("Importação RTD wide CSV")
scripts/mapear_automacao_opcoes_rtd.py:11:OUT_MD = ROOT / "docs" / "mapeamento_automacao_opcoes_rtd.md"
scripts/mapear_automacao_opcoes_rtd.py:12:OUT_JSON = ROOT / "docs" / "mapeamento_automacao_opcoes_rtd.json"
scripts/mapear_automacao_opcoes_rtd.py:58:    "rtd": ["rtd", "rtd_links", "option_quotes"],
scripts/mapear_automacao_opcoes_rtd.py:69:    "repositories/rtd_option_quotes_repository.py": "Prioritário para auditoria de persistência RTD.",
scripts/mapear_automacao_opcoes_rtd.py:75:    "dados/RTD_LINKS.csv": "Prioritário para auditoria do contrato RTD/Excel.",
scripts/mapear_automacao_opcoes_rtd.py:211:        "# Mapeamento automação opções RTD — ROTA_MESTRE_2 Fase 1",
scripts/mapear_automacao_opcoes_rtd.py:217:        "Mapeamento amplo de RTD, Excel, bridge, opções, persistência, serviços e UI.",
scripts/refresh_rtd_option_quotes_excel.ps1:2:    [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
scripts/refresh_rtd_option_quotes_excel.ps1:3:    [string]$SymbolsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\rtd_symbols.txt"),
scripts/refresh_rtd_option_quotes_excel.ps1:4:    [string]$CsvPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\RTD_LINKS.csv"),
scripts/refresh_rtd_option_quotes_excel.ps1:61:    $sheetName = "RTD_OPTION_QUOTES"
scripts/refresh_rtd_option_quotes_excel.ps1:125:            $formula = '=RTD("btg_pro_rtd";"";"' + $field + '";$A' + $row + ')'
scripts/refresh_rtd_option_quotes_excel.ps1:137:    Write-Host "Aba RTD_OPTION_QUOTES preenchida. Linhas:" $symbols.Count
scripts/refresh_rtd_option_quotes_excel.ps1:138:    Write-Host "Recalculando Excel/RTD..."
scripts/refresh_rtd_option_quotes_excel.ps1:150:    # Copia somente a aba RTD_OPTION_QUOTES para novo workbook e salva como CSV UTF-8.
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
scripts/run_derived_pipeline.py:24:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
scripts/run_derived_pipeline.py:39:def _parse_rtd_pipeline_metrics(output: str) -> dict:
scripts/run_derived_pipeline.py:40:    """Extrai métricas textuais emitidas pelo pipeline RTD restaurado."""
scripts/run_derived_pipeline.py:49:        match = _RTD_METRIC_RE.match(line)
scripts/run_derived_pipeline.py:59:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
scripts/run_derived_pipeline.py:61:    if not rtd_result:
scripts/run_derived_pipeline.py:64:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
scripts/run_derived_pipeline.py:67:def _run_rtd_option_quotes_import(
scripts/run_derived_pipeline.py:69:    csv_path: str = "dados/RTD_LINKS.csv",
scripts/run_derived_pipeline.py:73:    Executa a cadeia operacional RTD já restaurada contra o derived.db.
scripts/run_derived_pipeline.py:76:    - Usa somente CSV local dados/RTD_LINKS.csv.
scripts/run_derived_pipeline.py:77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
scripts/run_derived_pipeline.py:78:    - Delega importação + auditoria para scripts/run_rtd_option_quotes_pipeline.py.
scripts/run_derived_pipeline.py:81:    pipeline_script = repo_root / "scripts" / "run_rtd_option_quotes_pipeline.py"
scripts/run_derived_pipeline.py:90:            "message": f"Script RTD não encontrado: {pipeline_script}",
scripts/run_derived_pipeline.py:102:            "message": f"CSV RTD não encontrado: {resolved_csv}",
scripts/run_derived_pipeline.py:134:    metrics = _parse_rtd_pipeline_metrics(stdout)
scripts/run_derived_pipeline.py:184:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/run_derived_pipeline.py:189:    - Inclui a quantidade de cotações RTD inseridas/atualizadas.
scripts/run_derived_pipeline.py:191:    - Apenas lê contagens do banco depois que o pipeline RTD CSV já rodou.
scripts/run_derived_pipeline.py:235:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
scripts/run_derived_pipeline.py:236:            "rtd_import": rtd_result,
scripts/run_derived_pipeline.py:237:            "warnings": int((rtd_result or {}).get("warnings") or 0),
scripts/run_derived_pipeline.py:238:            "errors": int((rtd_result or {}).get("errors") or 0),
scripts/run_derived_pipeline.py:258:        "--skip-rtd",
scripts/run_derived_pipeline.py:260:        help="Não importar dados/RTD_LINKS.csv para rtd_option_quotes no derived.db",
scripts/run_derived_pipeline.py:263:        "--rtd-csv",
scripts/run_derived_pipeline.py:264:        default="dados/RTD_LINKS.csv",
scripts/run_derived_pipeline.py:265:        help="Caminho do CSV RTD usado pelo pipeline derivado",
scripts/run_derived_pipeline.py:280:    rtd_result = None
scripts/run_derived_pipeline.py:281:    if args.skip_rtd:
scripts/run_derived_pipeline.py:282:        print("\n[PIPELINE] Importação RTD pulada por --skip-rtd.")
scripts/run_derived_pipeline.py:283:        rtd_result = {
scripts/run_derived_pipeline.py:294:        print("\n[PIPELINE] Importando cotações RTD para derived.db...")
scripts/run_derived_pipeline.py:295:        rtd_result = _run_rtd_option_quotes_import(
scripts/run_derived_pipeline.py:297:            csv_path=args.rtd_csv,
scripts/run_derived_pipeline.py:301:        if int(rtd_result.get("returncode") or 0) != 0:
scripts/run_derived_pipeline.py:302:            print("[ERROR] PIPELINE FALHOU: importação/auditoria RTD falhou")
scripts/run_derived_pipeline.py:303:            if rtd_result.get("message"):
scripts/run_derived_pipeline.py:304:                print(f"[ERROR] {rtd_result.get('message')}")
scripts/run_derived_pipeline.py:305:            summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:307:            return int(rtd_result.get("returncode") or 1)
scripts/run_derived_pipeline.py:313:        summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:318:    summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:326:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
scripts/run_lista_rtd_option_quotes_pipeline.py:6:    1. scripts/import_lista_rtd_excel_to_option_quotes.py
scripts/run_lista_rtd_option_quotes_pipeline.py:7:    2. scripts/audit_rtd_option_quotes.py
scripts/run_lista_rtd_option_quotes_pipeline.py:10:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS
scripts/run_lista_rtd_option_quotes_pipeline.py:11:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS --json
scripts/run_lista_rtd_option_quotes_pipeline.py:12:    python scripts/run_lista_rtd_option_quotes_pipeline.py --dry-run --json
scripts/run_lista_rtd_option_quotes_pipeline.py:25:IMPORT_SCRIPT = Path("scripts/import_lista_rtd_excel_to_option_quotes.py")
scripts/run_lista_rtd_option_quotes_pipeline.py:26:AUDIT_SCRIPT = Path("scripts/audit_rtd_option_quotes.py")
scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:79:            "Aba RTD. Se omitida, o importador tenta RTD_OPTION_QUOTES "
scripts/run_lista_rtd_option_quotes_pipeline.py:80:            "e depois RTD_PROBE_OPTIONS."
scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_rtd_option_quotes_pipeline.py:3:Executa o pipeline operacional de cotações RTD de opções.
scripts/run_rtd_option_quotes_pipeline.py:7:    dados/RTD_LINKS.csv -> rtd_option_quotes -> auditoria
scripts/run_rtd_option_quotes_pipeline.py:11:    python scripts/run_rtd_option_quotes_pipeline.py
scripts/run_rtd_option_quotes_pipeline.py:12:    python scripts/run_rtd_option_quotes_pipeline.py --csv dados/RTD_LINKS.csv --db dados/app.db
scripts/run_rtd_option_quotes_pipeline.py:13:    python scripts/run_rtd_option_quotes_pipeline.py --dry-run
scripts/run_rtd_option_quotes_pipeline.py:14:    python scripts/run_rtd_option_quotes_pipeline.py --fail-on-warn
scripts/run_rtd_option_quotes_pipeline.py:28:IMPORT_SCRIPT = SCRIPTS_DIR / "import_rtd_option_quotes_wide_csv.py"
scripts/run_rtd_option_quotes_pipeline.py:29:AUDIT_SCRIPT = SCRIPTS_DIR / "audit_rtd_option_quotes.py"
scripts/run_rtd_option_quotes_pipeline.py:89:    csv_path: str = "dados/RTD_LINKS.csv",
scripts/run_rtd_option_quotes_pipeline.py:96:    print("Pipeline RTD option quotes")
scripts/run_rtd_option_quotes_pipeline.py:142:        description="Executa importação e auditoria de rtd_option_quotes."
scripts/run_rtd_option_quotes_pipeline.py:146:        default="dados/RTD_LINKS.csv",
scripts/run_rtd_option_quotes_pipeline.py:147:        help="Caminho do CSV RTD_LINKS.csv. Padrão: dados/RTD_LINKS.csv",
scripts/run_rtd_refresh_full.py:43:            FROM rtd_option_quotes
scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
scripts/run_rtd_refresh_full.py:80:    parser.add_argument("--symbols", default="dados/rtd_symbols.txt")
scripts/run_rtd_refresh_full.py:81:    parser.add_argument("--csv", default="dados/RTD_LINKS.csv")
scripts/run_rtd_refresh_full.py:82:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
scripts/run_rtd_refresh_full.py:99:    build_script = Path("scripts/build_rtd_symbols.py")
scripts/run_rtd_refresh_full.py:100:    import_script = Path("scripts/import_rtd_option_quotes_wide_csv.py")
scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
scripts/run_rtd_refresh_full.py:103:    print("=== RTD Refresh Full ===")
scripts/run_rtd_refresh_full.py:195:        print("- Cadastre uma estrutura pelo sistema ou rode sem --strict para usar fallback de rtd_option_quotes.")
scripts/run_rtd_refresh_full.py:205:        print("Pipeline interrompido: nenhum símbolo para consultar no RTD.")
scripts/run_rtd_refresh_full.py:241:            print("Pipeline interrompido no refresh Excel/RTD.")
scripts/run_rtd_refresh_full.py:245:        print("Refresh Excel/RTD pulado por --skip-excel.")
scripts/run_rtd_refresh_full.py:271:    print("OK: pipeline RTD finalizado.")
scripts/seed_current_rtd_option_quotes.py:3:Limpa e popula rtd_option_quotes com dados manuais atuais das estruturas
scripts/seed_current_rtd_option_quotes.py:8:    python scripts/seed_current_rtd_option_quotes.py
scripts/seed_current_rtd_option_quotes.py:9:    python scripts/seed_current_rtd_option_quotes.py --db dados/app.db
scripts/seed_current_rtd_option_quotes.py:13:- O script limpa somente a tabela rtd_option_quotes.
scripts/seed_current_rtd_option_quotes.py:136:        if not table_exists(connection, "rtd_option_quotes"):
scripts/seed_current_rtd_option_quotes.py:137:            raise RuntimeError("Tabela rtd_option_quotes não encontrada.")
scripts/seed_current_rtd_option_quotes.py:140:            "SELECT COUNT(*) FROM rtd_option_quotes"
scripts/seed_current_rtd_option_quotes.py:143:        connection.execute("DELETE FROM rtd_option_quotes")
scripts/seed_current_rtd_option_quotes.py:146:            INSERT INTO rtd_option_quotes (
scripts/seed_current_rtd_option_quotes.py:224:            "SELECT COUNT(*) FROM rtd_option_quotes"
scripts/seed_current_rtd_option_quotes.py:229:    print("Seed rtd_option_quotes concluído.")
scripts/seed_current_rtd_option_quotes.py:240:        description="Limpa e popula rtd_option_quotes com dados atuais de SMAL e PRIO."
scripts/verificar_andamento_rota.py:21:    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_6_RTD.md",
scripts/verificar_andamento_rota.py:353:        if "rtd_option_quotes" in table_names:
scripts/verificar_andamento_rota.py:354:            print_subsection("RTD option quotes")
scripts/verificar_andamento_rota.py:358:                FROM rtd_option_quotes
scripts/verificar_andamento_rota.py:361:            print(f"total_rtd_option_quotes={rows[0]['total']}")
Binary file scripts/__pycache__/audit_rtd_option_quotes.cpython-313.pyc matches
Binary file scripts/__pycache__/import_rtd_links_to_option_quotes.cpython-313.pyc matches
Binary file scripts/__pycache__/refresh_rtd_symbol_to_option_quotes.cpython-313.pyc matches
Binary file scripts/__pycache__/refresh_rtd_symbol_to_option_quotes_fallback.cpython-313.pyc matches
Binary file scripts/__pycache__/run_derived_pipeline.cpython-313.pyc matches
Binary file scripts/__pycache__/run_rtd_option_quotes_pipeline.cpython-313.pyc matches
services/calculation_orchestrator.py:97:        source=str(snapshot_row.get("source", "rtd")),
services/calculation_orchestrator.py:291:            source=str(market_snapshot_dict.get("source", "rtd")),
services/calculation_orchestrator.py:490:            "source":             snapshot.get("source", "rtd"),
services/canonical_input_service.py:8:  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
services/canonical_input_service.py:151:        legs pelo resultado do selector (manual > rtd).
services/canonical_input_service.py:188:    # Legs via selector (manual > rtd)
services/canonical_pricing_facade.py:91:            # Formatos comuns vindos de RTD/planilha:
services/legacy_structure_legs_reader.py:16:      - ler pernas legadas manual/rtd;
services/market_snapshot_selector.py:3:Política de precedência de snapshots: manual > rtd_option_quotes > rtd.
services/market_snapshot_selector.py:7:  - Caso contrário, se existir cotação em rtd_option_quotes para a leg RTD, usa rtd_option_quotes
services/market_snapshot_selector.py:8:  - Caso contrário, usa rtd_analise_robo_legs
services/market_snapshot_selector.py:19:RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
services/market_snapshot_selector.py:47:    Aplica a política manual > rtd_option_quotes > rtd para selecionar o snapshot canônico.
services/market_snapshot_selector.py:75:        rtd_legs = self._repo.get_rtd_legs(effective_ref)
services/market_snapshot_selector.py:77:        get_rtd_option_quote_legs = getattr(
services/market_snapshot_selector.py:79:            "get_rtd_option_quote_legs",
services/market_snapshot_selector.py:82:        if callable(get_rtd_option_quote_legs):
services/market_snapshot_selector.py:83:            rtd_option_quote_legs = get_rtd_option_quote_legs(effective_ref)
services/market_snapshot_selector.py:85:            rtd_option_quote_legs = []
services/market_snapshot_selector.py:95:        rtd_option_quote_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:96:        for leg in rtd_option_quote_legs:
services/market_snapshot_selector.py:97:            if leg.ativo and leg.ativo not in rtd_option_quote_by_ativo:
services/market_snapshot_selector.py:98:                rtd_option_quote_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:100:        rtd_by_ativo: dict[str, LegMarketSnapshot] = {}
services/market_snapshot_selector.py:101:        for leg in rtd_legs:
services/market_snapshot_selector.py:102:            if leg.ativo and leg.ativo not in rtd_by_ativo:
services/market_snapshot_selector.py:103:                rtd_by_ativo[leg.ativo] = leg
services/market_snapshot_selector.py:107:            | set(rtd_option_quote_by_ativo)
services/market_snapshot_selector.py:108:            | set(rtd_by_ativo)
services/market_snapshot_selector.py:117:                if ativo in rtd_option_quote_by_ativo or ativo in rtd_by_ativo:
services/market_snapshot_selector.py:119:            elif ativo in rtd_option_quote_by_ativo:
services/market_snapshot_selector.py:120:                legs_selected.append(rtd_option_quote_by_ativo[ativo])
services/market_snapshot_selector.py:122:                legs_selected.append(rtd_by_ativo[ativo])
services/market_snapshot_selector.py:126:        elif rtd_option_quote_legs:
services/market_snapshot_selector.py:127:            source = RTD_OPTION_QUOTES_SOURCE
services/market_snapshot_selector.py:129:            source = SnapshotSource.RTD
services/pricing_execution_app_service.py:6:  - execute_pricing() agora usa CanonicalPricingFacade (manual > rtd, caminho canônico)
services/robo_legs_service.py:23:      - obtém legs com regra manual > rtd
services/robo_legs_status_service.py:65:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(ref=ref)
services/robo_legs_status_service.py:69:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(aba)
services/robo_legs_status_service.py:74:        elif rtd_latest is not None:
services/robo_legs_status_service.py:75:            chosen_fonte = FonteType.RTD
services/robo_legs_status_service.py:76:            chosen_ts = rtd_latest
services/robo_legs_status_service.py:85:                rtd_latest_ts=None,
services/robo_legs_status_service.py:106:            rtd_latest_ts=rtd_latest,
services/structure_leg_rtd_enrichment_service.py:1:"""Service de enriquecimento de legs de estruturas via RTD.
services/structure_leg_rtd_enrichment_service.py:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:17:class StructureLegRtdEnrichmentService:
services/structure_leg_rtd_enrichment_service.py:18:    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
services/structure_leg_rtd_enrichment_service.py:20:    def __init__(self, rtd_option_quotes_repository: Any) -> None:
services/structure_leg_rtd_enrichment_service.py:21:        self._repo = rtd_option_quotes_repository
services/structure_leg_rtd_enrichment_service.py:31:        Campos enriquecidos via RTD:
services/structure_leg_rtd_enrichment_service.py:42:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py:123:        2. ultimo_preco vindo do RTD/cache;
services/structure_leg_rtd_enrichment_service.py:175:                raise ValueError(f"missing required RTD field: {field}")
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:1:"""Service de enriquecimento de legs de estruturas via RTD.
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:17:class StructureLegRtdEnrichmentService:
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:18:    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:20:    def __init__(self, rtd_option_quotes_repository: Any) -> None:
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:21:        self._repo = rtd_option_quotes_repository
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:31:        Campos enriquecidos via RTD:
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:42:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd:154:                raise ValueError(f"missing required RTD field: {field}")
Binary file services/__pycache__/calculation_orchestrator.cpython-313.pyc matches
Binary file services/__pycache__/canonical_input_service.cpython-313.pyc matches
Binary file services/__pycache__/legacy_structure_legs_reader.cpython-313.pyc matches
Binary file services/__pycache__/market_snapshot_selector.cpython-313.pyc matches
Binary file services/__pycache__/pricing_execution_app_service.cpython-313.pyc matches
Binary file services/__pycache__/robo_legs_service.cpython-313.pyc matches
Binary file services/__pycache__/robo_legs_status_service.cpython-313.pyc matches
Binary file services/__pycache__/structure_leg_rtd_enrichment_service.cpython-313.pyc matches
repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs), cotações RTD de opções
repositories/market_snapshot_repository.py:6:(rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
repositories/market_snapshot_repository.py:28:RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
repositories/market_snapshot_repository.py:32:_SQL_RTD_LEGS = """
repositories/market_snapshot_repository.py:54:    FROM rtd_analise_robo_legs
repositories/market_snapshot_repository.py:88:_SQL_RTD_SUMMARY = """
repositories/market_snapshot_repository.py:102:    FROM rtd_analise_robo
repositories/market_snapshot_repository.py:191:def _row_to_rtd_option_quote_leg(
repositories/market_snapshot_repository.py:196:    Converte uma cotação de rtd_option_quotes em LegMarketSnapshot mantendo
repositories/market_snapshot_repository.py:197:    os campos posicionais da leg RTD original.
repositories/market_snapshot_repository.py:199:    A tabela rtd_option_quotes é cache de cotação. Ela não define composição
repositories/market_snapshot_repository.py:201:    em rtd_analise_robo_legs.
repositories/market_snapshot_repository.py:242:        source=RTD_OPTION_QUOTES_SOURCE,
repositories/market_snapshot_repository.py:254:      get_rtd_legs(aba)                -> lista de LegMarketSnapshot source=RTD
repositories/market_snapshot_repository.py:255:      get_rtd_option_quote_legs(aba)   -> lista enriquecida source=rtd_option_quotes
repositories/market_snapshot_repository.py:257:      get_rtd_summary(aba)             -> dict com cabecalho RTD ou None
repositories/market_snapshot_repository.py:271:    # -- RTD ------------------------------------------------------------------
repositories/market_snapshot_repository.py:273:    def get_rtd_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:276:            rows = conn.execute(_SQL_RTD_LEGS, (aba,)).fetchall()
repositories/market_snapshot_repository.py:277:        return [_row_to_leg(r, SnapshotSource.RTD) for r in rows]
repositories/market_snapshot_repository.py:279:    def get_rtd_option_quote_legs(self, ref: StructureRef | str) -> list[LegMarketSnapshot]:
repositories/market_snapshot_repository.py:281:        Retorna legs RTD enriquecidas com rtd_option_quotes.
repositories/market_snapshot_repository.py:283:        A composição da estrutura vem de rtd_analise_robo_legs. Para cada ativo
repositories/market_snapshot_repository.py:284:        dessa composição, se houver cotação em rtd_option_quotes.codigo_opcao,
repositories/market_snapshot_repository.py:287:        base_legs = self.get_rtd_legs(ref)
repositories/market_snapshot_repository.py:321:            FROM rtd_option_quotes
repositories/market_snapshot_repository.py:330:            # Banco sem tabela rtd_option_quotes: mantém compatibilidade com
repositories/market_snapshot_repository.py:345:                enriched.append(_row_to_rtd_option_quote_leg(base_leg, quote_row))
repositories/market_snapshot_repository.py:349:    def get_rtd_summary(self, ref: StructureRef | str) -> Optional[dict]:
repositories/market_snapshot_repository.py:352:            row = conn.execute(_SQL_RTD_SUMMARY, (aba,)).fetchone()
repositories/market_snapshot_repository.py:370:        source: SnapshotSource = SnapshotSource.RTD,
repositories/market_snapshot_repository.py:374:        if source == SnapshotSource.RTD:
repositories/market_snapshot_repository.py:375:            legs = self.get_rtd_legs(ref)
repositories/market_snapshot_repository.py:376:            summary = self.get_rtd_summary(ref)
repositories/robo_legs_repository.py:36:      manual_analise_robo_legs > rtd_analise_robo_legs
repositories/robo_legs_repository.py:57:        - Se vazio, tenta RTD
repositories/robo_legs_repository.py:72:        rtd = self._query_legs(
repositories/robo_legs_repository.py:73:            table="rtd_analise_robo_legs",
repositories/robo_legs_repository.py:76:            fonte=FonteType.RTD,
repositories/robo_legs_repository.py:78:        return rtd
repositories/robo_legs_repository.py:101:        prefer: str = "manual_then_rtd",
repositories/robo_legs_repository.py:112:                    SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?
repositories/robo_legs_repository.py:128:                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "
repositories/robo_legs_repository.py:271:        prefer: str = "manual_then_rtd",
repositories/robo_legs_status_repository.py:47:        Retorna (manual_latest_ts, rtd_latest_ts) para a aba.
repositories/robo_legs_status_repository.py:57:                "SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",
repositories/robo_legs_status_repository.py:76:        Retorna (manual_latest_ts, rtd_latest_ts).
repositories/rtd_option_quotes_repository.py:1:# repositories/rtd_option_quotes_repository.py
repositories/rtd_option_quotes_repository.py:3:Repositorio para consulta de cotações de opções em rtd_option_quotes.
repositories/rtd_option_quotes_repository.py:19:class RtdOptionQuotesRepository:
repositories/rtd_option_quotes_repository.py:35:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:55:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:68:            FROM rtd_option_quotes
repositories/structure_events_repository.py:15:Tabelas legadas como rtd_encerramentos_manuais e rtd_rolls_detectados seguem
repositories/ui_data_table_candidates.py:8:legados de staging, como tabelas rtd_*.
repositories/ui_data_table_candidates.py:13:    "rtd_consolidacoes",
repositories/ui_data_table_candidates.py:14:    "rtd_consolidations",
repositories/ui_data_table_candidates.py:16:    "rtd_decisions",
repositories/ui_data_table_candidates.py:21:    "rtd_payoff_points",
repositories/ui_data_table_candidates.py:22:    "rtd_payoff_curva",
Binary file repositories/__pycache__/market_snapshot_repository.cpython-313.pyc matches
Binary file repositories/__pycache__/robo_legs_repository.cpython-313.pyc matches
Binary file repositories/__pycache__/robo_legs_status_repository.cpython-313.pyc matches
Binary file repositories/__pycache__/rtd_option_quotes_repository.cpython-313.pyc matches
Binary file repositories/__pycache__/structure_events_repository.cpython-313.pyc matches
Binary file repositories/__pycache__/ui_data_table_candidates.cpython-313.pyc matches
domain/calculation_request.py:28:VALID_SOURCES        = {"rtd", "manual", "ui"}
domain/calculation_request.py:178:    source             : 'rtd' | 'manual' | 'ui'
domain/calculation_request.py:219:    O orquestrador monta este objeto a partir do DB e do bridge/RTD,
domain/market_snapshot.py:19:    RTD    = "rtd"
domain/market_snapshot.py:50:    source          : SnapshotSource  = SnapshotSource.RTD
domain/market_snapshot.py:60:    Atributos do cabeçalho (todos opcionais -- podem vir de RTD ou manual):
domain/market_snapshot.py:72:    source             : SnapshotSource                 = SnapshotSource.RTD
domain/payoff_features.py:109:    timestamp + aba                rastreabilidade opcional (legado RTD).
Binary file domain/__pycache__/calculation_request.cpython-313.pyc matches
Binary file domain/__pycache__/market_snapshot.cpython-313.pyc matches
ATT/tests/test_audit_rtd_option_quotes.py:12:    / "audit_rtd_option_quotes.py"
ATT/tests/test_audit_rtd_option_quotes.py:18:        "audit_rtd_option_quotes_under_test",
ATT/tests/test_audit_rtd_option_quotes.py:33:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_audit_rtd_option_quotes.py:50:                source TEXT NOT NULL DEFAULT 'rtd_links',
ATT/tests/test_audit_rtd_option_quotes.py:75:            INSERT INTO rtd_option_quotes (
ATT/tests/test_audit_rtd_option_quotes.py:86:            VALUES (?, 'PETR4', 'CALL', 30.0, 1.0, 1.1, 'rtd_links', {updated_at_sql}, CURRENT_TIMESTAMP)
ATT/tests/test_audit_rtd_option_quotes.py:111:    assert "table not found: rtd_option_quotes" in result["errors"]
ATT/tests/test_audit_rtd_option_quotes.py:151:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_canonical_pricing_facade.py:13:        "source": "rtd",
ATT/tests/test_canonical_pricing_facade.py:30:def test_snapshot_result_to_payload_normalizes_common_rtd_number_formats(
ATT/tests/test_canonical_pricing_facade.py:72:                "source": "rtd_option_quotes",
ATT/tests/test_canonical_pricing_facade.py:93:        "snapshot_source": "rtd",
ATT/tests/test_canonical_pricing_facade.py:109:    assert leg["source"] == "rtd_option_quotes"
ATT/tests/test_import_rtd_links_to_option_quotes.py:11:SCRIPT_PATH = ROOT / "scripts" / "import_rtd_links_to_option_quotes.py"
ATT/tests/test_import_rtd_links_to_option_quotes.py:15:    "import_rtd_links_to_option_quotes",
ATT/tests/test_import_rtd_links_to_option_quotes.py:24:def create_rtd_option_quotes_schema(db_path: Path) -> None:
ATT/tests/test_import_rtd_links_to_option_quotes.py:30:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_import_rtd_links_to_option_quotes.py:53:                source TEXT NOT NULL DEFAULT 'rtd_links',
ATT/tests/test_import_rtd_links_to_option_quotes.py:68:def write_rtd_links_csv(path: Path, rows: list[list[str]]) -> None:
ATT/tests/test_import_rtd_links_to_option_quotes.py:103:            FROM rtd_option_quotes
ATT/tests/test_import_rtd_links_to_option_quotes.py:116:        return conn.execute("SELECT COUNT(*) FROM rtd_option_quotes").fetchone()[0]
ATT/tests/test_import_rtd_links_to_option_quotes.py:144:    csv_path = tmp_path / "RTD_LINKS.csv"
ATT/tests/test_import_rtd_links_to_option_quotes.py:146:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:176:    assert record["source"] == "rtd_links"
ATT/tests/test_import_rtd_links_to_option_quotes.py:183:    csv_path = tmp_path / "RTD_LINKS.csv"
ATT/tests/test_import_rtd_links_to_option_quotes.py:185:    create_rtd_option_quotes_schema(db_path)
ATT/tests/test_import_rtd_links_to_option_quotes.py:187:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:211:    csv_path = tmp_path / "RTD_LINKS.csv"
ATT/tests/test_import_rtd_links_to_option_quotes.py:213:    create_rtd_option_quotes_schema(db_path)
ATT/tests/test_import_rtd_links_to_option_quotes.py:215:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:235:    write_rtd_links_csv(
ATT/tests/test_import_rtd_links_to_option_quotes.py:264:    assert option["source"] == "rtd_links"
ATT/tests/test_legacy_structure_legs_importer_integration.py:65:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:128:def _insert_legacy_rtd_leg(db_path):
ATT/tests/test_legacy_structure_legs_importer_integration.py:132:        INSERT INTO rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_importer_integration.py:139:            190.0, 1000, 'rtdleg190', '2026-06-20', 0.55
ATT/tests/test_legacy_structure_legs_importer_integration.py:175:    # Insere RTD e MANUAL no mesmo timestamp.
ATT/tests/test_legacy_structure_legs_importer_integration.py:177:    _insert_legacy_rtd_leg(db_path)
ATT/tests/test_legacy_structure_legs_importer_integration.py:226:    # Garante que a leg antiga foi substituida e que RTD nao foi usado
ATT/tests/test_legacy_structure_legs_importer_integration.py:229:    assert imported_leg["symbol"] != "RTDLEG190"
ATT/tests/test_legacy_structure_legs_reader.py:142:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_legacy_structure_legs_reader.py:160:def test_read_by_structure_id_integrates_structure_alias_with_rtd_legs(tmp_path):
ATT/tests/test_legacy_structure_legs_reader.py:180:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:8:def _create_rtd_legs_table(conn):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:11:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:37:def _create_rtd_option_quotes_table(conn):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:40:        CREATE TABLE rtd_option_quotes (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:65:def _insert_base_rtd_leg(conn):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:68:        INSERT INTO rtd_analise_robo_legs (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:117:def test_get_rtd_option_quote_legs_enriches_base_rtd_leg_with_quote_cache(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:121:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:122:        _create_rtd_option_quotes_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:123:        _insert_base_rtd_leg(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:127:            INSERT INTO rtd_option_quotes (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:166:                "rtd_option_quotes",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:176:    legs = repo.get_rtd_option_quote_legs("BOVA11")
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:182:    # Identidade/composição vêm da leg estrutural RTD.
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:190:    # Cotação/greeks vêm do cache centralizado rtd_option_quotes.
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:191:    assert leg.source == "rtd_option_quotes"
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:207:def test_get_rtd_option_quote_legs_returns_empty_list_when_cache_table_is_missing(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:211:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:212:        _insert_base_rtd_leg(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:217:    assert repo.get_rtd_option_quote_legs("BOVA11") == []
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:220:def _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:240:        INSERT INTO rtd_option_quotes (
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:279:            "rtd_option_quotes",
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:287:def test_get_rtd_option_quote_legs_ignores_orphan_quote_without_structural_leg(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:291:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:292:        _create_rtd_option_quotes_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:294:        _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:308:    assert repo.get_rtd_option_quote_legs("BOVA11") == []
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:311:def test_get_rtd_option_quote_legs_uses_latest_quote_when_cache_has_duplicates(tmp_path):
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:315:        _create_rtd_legs_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:316:        _create_rtd_option_quotes_table(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:317:        _insert_base_rtd_leg(conn)
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:319:        _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:334:        _insert_rtd_option_quote(
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:353:    legs = repo.get_rtd_option_quote_legs("BOVA11")
ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py:359:    assert leg.source == "rtd_option_quotes"
ATT/tests/test_market_snapshot_selector.py:16:    def __init__(self, *, manual=None, rtd_option_quotes=None, rtd=None):
ATT/tests/test_market_snapshot_selector.py:18:        self.rtd_option_quotes = rtd_option_quotes or []
ATT/tests/test_market_snapshot_selector.py:19:        self.rtd = rtd or []
ATT/tests/test_market_snapshot_selector.py:24:    def get_rtd_option_quote_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:25:        return self.rtd_option_quotes
ATT/tests/test_market_snapshot_selector.py:27:    def get_rtd_legs(self, ref):
ATT/tests/test_market_snapshot_selector.py:28:        return self.rtd
ATT/tests/test_market_snapshot_selector.py:31:def test_selector_prioritizes_rtd_option_quotes_over_legacy_rtd_when_no_manual_exists():
ATT/tests/test_market_snapshot_selector.py:32:    legacy_rtd_leg = _leg("BOVAE195", "rtd", 1.10)
ATT/tests/test_market_snapshot_selector.py:33:    quote_leg = _leg("BOVAE195", "rtd_option_quotes", 1.23)
ATT/tests/test_market_snapshot_selector.py:37:            rtd=[legacy_rtd_leg],
ATT/tests/test_market_snapshot_selector.py:38:            rtd_option_quotes=[quote_leg],
ATT/tests/test_market_snapshot_selector.py:45:    assert result.source == "rtd_option_quotes"
ATT/tests/test_market_snapshot_selector.py:50:def test_selector_keeps_manual_leg_ahead_of_rtd_option_quotes():
ATT/tests/test_market_snapshot_selector.py:52:    quote_leg = _leg("BOVAE195", "rtd_option_quotes", 1.23)
ATT/tests/test_market_snapshot_selector.py:53:    legacy_rtd_leg = _leg("BOVAE195", "rtd", 1.10)
ATT/tests/test_market_snapshot_selector.py:58:            rtd_option_quotes=[quote_leg],
ATT/tests/test_market_snapshot_selector.py:59:            rtd=[legacy_rtd_leg],
ATT/tests/test_robo_legs_repository.py:25:        CREATE TABLE rtd_analise_robo_legs (
ATT/tests/test_robo_legs_repository.py:42:def test_get_legs_prefers_manual_over_rtd(tmp_path):
ATT/tests/test_robo_legs_repository.py:54:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:72:def test_get_legs_falls_back_to_rtd_when_manual_empty(tmp_path):
ATT/tests/test_robo_legs_repository.py:79:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:116:def test_list_timestamps_prefers_manual_then_rtd(tmp_path):
ATT/tests/test_robo_legs_repository.py:133:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_repository.py:158:        INSERT INTO rtd_analise_robo_legs
ATT/tests/test_robo_legs_status_repository.py:9:def test_latest_timestamps_returns_parsed_manual_and_rtd(tmp_path):
ATT/tests/test_robo_legs_status_repository.py:15:    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:26:        "INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
ATT/tests/test_robo_legs_status_repository.py:36:    manual_latest, rtd_latest = repo.latest_timestamps("TESTE")
ATT/tests/test_robo_legs_status_repository.py:39:    assert rtd_latest == datetime(2026, 5, 19, 10, 30, 0)
ATT/tests/test_robo_legs_status_repository.py:48:    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")
ATT/tests/test_robo_legs_status_repository.py:56:    manual_latest, rtd_latest = repo.latest_timestamps("INEXISTENTE")
ATT/tests/test_robo_legs_status_repository.py:59:    assert rtd_latest is None
ATT/tests/test_robo_legs_status_service.py:14:    def __init__(self, manual_latest=None, rtd_latest=None):
ATT/tests/test_robo_legs_status_service.py:16:        self._rtd_latest = rtd_latest
ATT/tests/test_robo_legs_status_service.py:21:        return self._manual_latest, self._rtd_latest
ATT/tests/test_robo_legs_status_service.py:31:        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:43:    assert result.rtd_latest_ts is None
ATT/tests/test_robo_legs_status_service.py:50:    rtd_latest = datetime(2026, 5, 19, 10, 1, 0)
ATT/tests/test_robo_legs_status_service.py:54:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=rtd_latest),
ATT/tests/test_robo_legs_status_service.py:63:    assert result.rtd_latest_ts == rtd_latest
ATT/tests/test_robo_legs_status_service.py:68:def test_status_uses_rtd_when_manual_missing():
ATT/tests/test_robo_legs_status_service.py:69:    rtd_latest = datetime(2026, 5, 19, 10, 0, 0)
ATT/tests/test_robo_legs_status_service.py:73:        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=rtd_latest),
ATT/tests/test_robo_legs_status_service.py:79:    assert result.chosen_fonte == FonteType.RTD
ATT/tests/test_robo_legs_status_service.py:80:    assert result.chosen_ts == rtd_latest
ATT/tests/test_robo_legs_status_service.py:82:    assert result.rtd_latest_ts == rtd_latest
ATT/tests/test_robo_legs_status_service.py:92:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:108:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_robo_legs_status_service.py:123:        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:31:class FakeRtdRoboLegsService:
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:46:                "source": "rtd_option_quotes",
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:51:def test_rtd_legacy_fallback_can_feed_pricing_payload_when_no_canonical_legs_exist():
ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py:63:        robo_legs_service=FakeRtdRoboLegsService(),
ATT/tests/test_rtd_option_quotes_repository_contract.py:6:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
ATT/tests/test_rtd_option_quotes_repository_contract.py:13:            CREATE TABLE rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:46:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:85:                "rtd_option_quotes",
ATT/tests/test_rtd_option_quotes_repository_contract.py:92:    repository = RtdOptionQuotesRepository(db_path=db_path)
ATT/tests/test_rtd_option_quotes_repository_contract.py:102:    assert quote["source"] == "rtd_option_quotes"
ATT/tests/test_rtd_option_quotes_repository_contract.py:110:    repository = RtdOptionQuotesRepository(db_path=db_path)
ATT/tests/test_rtd_option_quotes_repository_contract.py:122:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:142:                "rtd_option_quotes",
ATT/tests/test_rtd_option_quotes_repository_contract.py:148:    repository = RtdOptionQuotesRepository(db_path=db_path)
ATT/tests/test_rtd_option_quotes_repository_contract.py:158:    repository = RtdOptionQuotesRepository(db_path=db_path)
ATT/tests/test_rtd_option_quotes_repository_contract.py:177:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:188:            VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
ATT/tests/test_rtd_option_quotes_repository_contract.py:193:    repository = RtdOptionQuotesRepository(db_path=db_path)
ATT/tests/test_rtd_option_quotes_repository_contract.py:213:            INSERT INTO rtd_option_quotes (
ATT/tests/test_rtd_option_quotes_repository_contract.py:224:            VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
ATT/tests/test_rtd_option_quotes_repository_contract.py:229:    repository = RtdOptionQuotesRepository(db_path=db_path)
ATT/tests/test_run_derived_pipeline_rtd_integration.py:21:def test_parse_rtd_pipeline_metrics_from_stdout():
ATT/tests/test_run_derived_pipeline_rtd_integration.py:25:Importação RTD wide CSV
ATT/tests/test_run_derived_pipeline_rtd_integration.py:34:    assert module._parse_rtd_pipeline_metrics(output) == {
ATT/tests/test_run_derived_pipeline_rtd_integration.py:42:def test_rtd_quotes_updated_count_sums_inserted_and_updated():
ATT/tests/test_run_derived_pipeline_rtd_integration.py:45:    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
ATT/tests/test_run_derived_pipeline_rtd_integration.py:46:    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
ATT/tests/test_run_derived_pipeline_rtd_integration.py:47:    assert module._rtd_quotes_updated_count(None) == 0
ATT/tests/test_run_derived_pipeline_rtd_integration.py:50:def test_run_rtd_option_quotes_import_uses_csv_pipeline_without_excel_or_powershell(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:61:    (scripts_dir / "run_rtd_option_quotes_pipeline.py").write_text(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:62:        "# fake rtd csv pipeline\n",
ATT/tests/test_run_derived_pipeline_rtd_integration.py:65:    (dados_dir / "RTD_LINKS.csv").write_text(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:89:    result = module._run_rtd_option_quotes_import(
ATT/tests/test_run_derived_pipeline_rtd_integration.py:91:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_derived_pipeline_rtd_integration.py:104:    assert command[1].endswith("run_rtd_option_quotes_pipeline.py")
ATT/tests/test_run_derived_pipeline_rtd_integration.py:106:    assert "dados/RTD_LINKS.csv" in command
ATT/tests/test_run_derived_pipeline_rtd_integration.py:112:    assert "refresh_rtd_option_quotes_excel" not in command_text
ATT/tests/test_run_derived_pipeline_rtd_integration.py:113:    assert "lista_rtd.xlsm" not in command_text
ATT/tests/test_run_rtd_option_quotes_pipeline.py:11:    / "run_rtd_option_quotes_pipeline.py"
ATT/tests/test_run_rtd_option_quotes_pipeline.py:17:        "run_rtd_option_quotes_pipeline_under_test",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:30:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:35:    assert command[1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:37:    assert "dados/RTD_LINKS.csv" in command
ATT/tests/test_run_rtd_option_quotes_pipeline.py:47:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:64:    assert command[1].endswith("audit_rtd_option_quotes.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:98:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:104:    assert calls[0][1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:118:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:124:    assert calls[0][1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:125:    assert calls[1][1].endswith("audit_rtd_option_quotes.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:139:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_run_rtd_option_quotes_pipeline.py:146:    assert calls[0][1].endswith("import_rtd_option_quotes_wide_csv.py")
ATT/tests/test_run_rtd_option_quotes_pipeline.py:156:        if command[1].endswith("import_rtd_option_quotes_wide_csv.py"):
ATT/tests/test_run_rtd_option_quotes_pipeline.py:163:        csv_path="dados/RTD_LINKS.csv",
ATT/tests/test_structure_leg_rtd_enrichment_service.py:3:from services.structure_leg_rtd_enrichment_service import (
ATT/tests/test_structure_leg_rtd_enrichment_service.py:4:    StructureLegRtdEnrichmentService,
ATT/tests/test_structure_leg_rtd_enrichment_service.py:8:class FakeRtdOptionQuotesRepository:
ATT/tests/test_structure_leg_rtd_enrichment_service.py:18:def test_enrich_leg_from_symbol_uses_rtd_quote_and_returns_canonical_leg():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:19:    repo = FakeRtdOptionQuotesRepository(
ATT/tests/test_structure_leg_rtd_enrichment_service.py:30:    service = StructureLegRtdEnrichmentService(repo)
ATT/tests/test_structure_leg_rtd_enrichment_service.py:60:    repo = FakeRtdOptionQuotesRepository(
ATT/tests/test_structure_leg_rtd_enrichment_service.py:71:    service = StructureLegRtdEnrichmentService(repo)
ATT/tests/test_structure_leg_rtd_enrichment_service.py:95:    service = StructureLegRtdEnrichmentService(
ATT/tests/test_structure_leg_rtd_enrichment_service.py:96:        FakeRtdOptionQuotesRepository({})
ATT/tests/test_structure_leg_rtd_enrichment_service.py:108:def test_enrich_leg_raises_value_error_when_rtd_quote_is_not_found():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:109:    service = StructureLegRtdEnrichmentService(
ATT/tests/test_structure_leg_rtd_enrichment_service.py:110:        FakeRtdOptionQuotesRepository({})
ATT/tests/test_structure_leg_rtd_enrichment_service.py:123:def test_enrich_leg_raises_value_error_when_rtd_quote_has_missing_required_fields():
ATT/tests/test_structure_leg_rtd_enrichment_service.py:124:    service = StructureLegRtdEnrichmentService(
ATT/tests/test_structure_leg_rtd_enrichment_service.py:125:        FakeRtdOptionQuotesRepository(
ATT/tests/test_structure_leg_rtd_enrichment_service.py:137:    with pytest.raises(ValueError, match="missing required RTD field"):
Binary file ATT/tests/__pycache__/test_audit_rtd_option_quotes.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_canonical_pricing_facade.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_import_rtd_links_to_option_quotes.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_legacy_structure_legs_importer_integration.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_legacy_structure_legs_reader.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_market_snapshot_repository_rtd_option_quotes.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_market_snapshot_selector.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_robo_legs_repository.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_robo_legs_status_repository.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_robo_legs_status_service.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_rtd_legacy_canonical_pricing_input_guardrail.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_rtd_option_quotes_repository_contract.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_run_derived_pipeline_rtd_integration.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_run_rtd_option_quotes_pipeline.cpython-313-pytest-9.0.3.pyc matches
Binary file ATT/tests/__pycache__/test_structure_leg_rtd_enrichment_service.cpython-313-pytest-9.0.3.pyc matches

## Scripts RTD disponíveis

./.git/logs/refs/heads/fase-10a-rastreabilidade-preco-rtd
./.git/logs/refs/heads/fase-10b-rastreabilidade-preco-rtd-persistencia
./.git/logs/refs/heads/fase-10c-validacao-execucao-preco-rtd
./.git/logs/refs/heads/fase-10d-endurecimento-rastreabilidade-preco-rtd
./.git/logs/refs/heads/fase-10e-validacao-operacional-rastreabilidade-preco-rtd
./.git/logs/refs/heads/fase-10f-validacao-e2e-rtd-excel
./.git/logs/refs/heads/fase-10g-guardrails-operacionais-preco-rtd
./.git/logs/refs/heads/fase-11-testes-integrados-rtd
./.git/logs/refs/heads/fase-6-4-contrato-rtd-canonical-pricing
./.git/logs/refs/heads/fase-6-5-retomada-funcional-incremental-rtd
./.git/logs/refs/heads/fase-6-6-auditoria-metadados-rtd-canonical
./.git/logs/refs/heads/fase-6-7-consolidacao-diagnostico-rtd-canonical
./.git/logs/refs/heads/fase-6-8-guardrail-matriz-diagnostico-rtd
./.git/logs/refs/heads/fase-6-9-ajuste-rtd-canonical-pricing
./.git/logs/refs/remotes/origin/fase-10a-rastreabilidade-preco-rtd
./.git/logs/refs/remotes/origin/fase-10b-rastreabilidade-preco-rtd-persistencia
./.git/logs/refs/remotes/origin/fase-10c-validacao-execucao-preco-rtd
./.git/logs/refs/remotes/origin/fase-10d-endurecimento-rastreabilidade-preco-rtd
./.git/logs/refs/remotes/origin/fase-10e-validacao-operacional-rastreabilidade-preco-rtd
./.git/logs/refs/remotes/origin/fase-10f-validacao-e2e-rtd-excel
./.git/logs/refs/remotes/origin/fase-10g-guardrails-operacionais-preco-rtd
./.git/logs/refs/remotes/origin/fase-11-testes-integrados-rtd
./.git/logs/refs/remotes/origin/fase-6-4-contrato-rtd-canonical-pricing
./.git/logs/refs/remotes/origin/fase-6-5-retomada-funcional-incremental-rtd
./.git/logs/refs/remotes/origin/fase-6-6-auditoria-metadados-rtd-canonical
./.git/logs/refs/remotes/origin/fase-6-9-ajuste-rtd-canonical-pricing
./.git/refs/heads/fase-10a-rastreabilidade-preco-rtd
./.git/refs/heads/fase-10b-rastreabilidade-preco-rtd-persistencia
./.git/refs/heads/fase-10c-validacao-execucao-preco-rtd
./.git/refs/heads/fase-10d-endurecimento-rastreabilidade-preco-rtd
./.git/refs/heads/fase-10e-validacao-operacional-rastreabilidade-preco-rtd
./.git/refs/heads/fase-10f-validacao-e2e-rtd-excel
./.git/refs/heads/fase-10g-guardrails-operacionais-preco-rtd
./.git/refs/heads/fase-11-testes-integrados-rtd
./.git/refs/heads/fase-6-4-contrato-rtd-canonical-pricing
./.git/refs/heads/fase-6-5-retomada-funcional-incremental-rtd
./.git/refs/heads/fase-6-6-auditoria-metadados-rtd-canonical
./.git/refs/heads/fase-6-7-consolidacao-diagnostico-rtd-canonical
./.git/refs/heads/fase-6-8-guardrail-matriz-diagnostico-rtd
./.git/refs/heads/fase-6-9-ajuste-rtd-canonical-pricing
./.git/refs/remotes/origin/fase-10a-rastreabilidade-preco-rtd
./.git/refs/remotes/origin/fase-10b-rastreabilidade-preco-rtd-persistencia
./.git/refs/remotes/origin/fase-10c-validacao-execucao-preco-rtd
./.git/refs/remotes/origin/fase-10d-endurecimento-rastreabilidade-preco-rtd
./.git/refs/remotes/origin/fase-10e-validacao-operacional-rastreabilidade-preco-rtd
./.git/refs/remotes/origin/fase-10f-validacao-e2e-rtd-excel
./.git/refs/remotes/origin/fase-10g-guardrails-operacionais-preco-rtd
./.git/refs/remotes/origin/fase-11-testes-integrados-rtd
./.git/refs/remotes/origin/fase-6-4-contrato-rtd-canonical-pricing
./.git/refs/remotes/origin/fase-6-5-retomada-funcional-incremental-rtd
./.git/refs/remotes/origin/fase-6-6-auditoria-metadados-rtd-canonical
./.git/refs/remotes/origin/fase-6-9-ajuste-rtd-canonical-pricing
./.git/refs/tags/fase-6-9-rtd-canonical-pricing
./ATT/tests/test_audit_rtd_option_quotes.py
./ATT/tests/test_import_rtd_links_to_option_quotes.py
./ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py
./ATT/tests/test_rtd_legacy_canonical_pricing_input_guardrail.py
./ATT/tests/test_rtd_option_quotes_repository_contract.py
./ATT/tests/test_run_derived_pipeline_rtd_integration.py
./ATT/tests/test_run_rtd_option_quotes_pipeline.py
./ATT/tests/test_structure_leg_rtd_enrichment_service.py
./ATT/tests/__pycache__/test_audit_rtd_option_quotes.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_import_rtd_links_to_option_quotes.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_market_snapshot_repository_rtd_option_quotes.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_rtd_legacy_canonical_pricing_input_guardrail.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_rtd_option_quotes_repository_contract.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_run_derived_pipeline_rtd_integration.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_run_rtd_option_quotes_pipeline.cpython-313-pytest-9.0.3.pyc
./ATT/tests/__pycache__/test_structure_leg_rtd_enrichment_service.cpython-313-pytest-9.0.3.pyc
./backups/app_fase12_rtd_option_quotes_ok.db
./backups/app_fase12_rtd_option_quotes_ok.sql
./backups/LISTA_RTD_fase12_rtd_option_quotes_ok.xlsm
./dados/RTD_LINKS.csv
./dados/RTD_LINKS_probe.csv
./dados/rtd_symbols.txt
./dados/rtd_symbols_probe.txt
./docs/checkpoints/evidencias/diagnostico_fluxo_autopreenchimento_rtd.md
./docs/checkpoints/evidencias/diagnostico_rtd_autopreenchimento_focado.txt
./docs/checkpoints/evidencias/fase-1-mapa-rtd-codigo-atual.txt
./docs/checkpoints/evidencias/fase-1-mapa-rtd-runtime-codigo-atual.txt
./docs/checkpoints/evidencias/fase-1-trechos-rtd-runtime.txt
./docs/checkpoints/evidencias/fase-5-diagnostico-rtd.txt
./docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt
./docs/checkpoints/evidencias/fase-5c-restauracao-rtd-historico.txt
./docs/checkpoints/evidencias/fase-5d-validacao-rtd-restaurado-operacional.txt
./docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt
./docs/checkpoints/evidencias/fase-5e-validacao-integracao-rtd-derived-pipeline.txt
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
./docs/checkpoints/evidencias/grep_autopreenchimento_rtd.txt
./docs/checkpoints/evidencias/grep_rtd_autopreenchimento_focado.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_execute_pricing_rtd_integration_from_b492f16.py.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_db_path_from_bcb6ddb.py.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_canonical_pricing_facade_rtd_price_resolution_from_0c7e123.py.txt
./docs/checkpoints/evidencias/rtd_historico_collect_sanitizado/test_fase_11_rtd_integrated_flow_from_9009a40.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview
./docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_execute_pricing_rtd_integration.from-b492f16.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_db_path.from-bcb6ddb.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview/test_canonical_pricing_facade_rtd_price_resolution.from-0c7e123.py.txt
./docs/checkpoints/evidencias/rtd_historico_preview/test_fase_11_rtd_integrated_flow.from-9009a40.py.txt
./docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md
./docs/checkpoints/fase-6-8-guardrail-matriz-diagnostico-rtd.md
./docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md
./docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_6_RTD.md
./docs/decisoes/DECISAO_ATUALIZACAO_AUTOMATICA_RTD.md
./docs/evidencias/LEVANTAMENTO_ATUALIZACAO_AUTOMATICA_RTD.md
./docs/evidencias/trechos/TRECHOS_MAIN_WINDOW_ATUALIZACAO_RTD.md
./infra/bootstrap_rtd_option_quotes_schema.py
./infra/__pycache__/bootstrap_rtd_option_quotes_schema.cpython-313.pyc
./LISTA_RTD.xlsm
./repositories/rtd_option_quotes_repository.py
./repositories/__pycache__/rtd_option_quotes_repository.cpython-313.pyc
./scripts/audit_rtd_option_quotes.py
./scripts/build_rtd_symbols.py
./scripts/create_rtd_option_quotes_sheet.py
./scripts/fase-5-diagnostico-rtd.sh
./scripts/fase-5b-diagnostico-rtd-cadeia-real.sh
./scripts/fase-5c-restaurar-rtd-historico.sh
./scripts/fase-5d-validar-rtd-restaurado-operacional.sh
./scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh
./scripts/fase-5e-integrar-rtd-derived-pipeline.sh
./scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh
./scripts/import_lista_rtd_excel_to_option_quotes.py
./scripts/import_rtd_links_to_option_quotes.py
./scripts/import_rtd_option_quotes_wide_csv.py
./scripts/mapear_automacao_opcoes_rtd.py
./scripts/refresh_rtd_option_quotes_excel.ps1
./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
./scripts/run_lista_rtd_option_quotes_pipeline.py
./scripts/run_rtd_option_quotes_pipeline.py
./scripts/run_rtd_refresh_full.py
./scripts/seed_current_rtd_option_quotes.py
./scripts/__pycache__/audit_rtd_option_quotes.cpython-313.pyc
./scripts/__pycache__/import_rtd_links_to_option_quotes.cpython-313.pyc
./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes.cpython-313.pyc
./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes_fallback.cpython-313.pyc
./scripts/__pycache__/run_rtd_option_quotes_pipeline.cpython-313.pyc
./services/structure_leg_rtd_enrichment_service.py
./services/structure_leg_rtd_enrichment_service.py.bak_premium_from_rtd
./services/__pycache__/structure_leg_rtd_enrichment_service.cpython-313.pyc
./tools/revisao_funcional/diagnostico_fluxo_autopreenchimento_rtd.py
./tools/revisao_funcional/diagnostico_rtd_autopreenchimento_focado.py
./tools/revisao_funcional/diagnostico_rtd_option_quote.py

## Evidência recente observada na Fase 5

- Pipeline RTD option quotes executado.
- CSV usado: dados/RTD_LINKS.csv.
- Banco usado: dados/derived.db.
- input_rows: 4.
- inserted: 0.
- updated: 4.
- skipped: 0.
- rtd_option_quotes: 4 registros.
- Erros: 0.

## Estado inicial

A Fase 5 demonstrou que o pipeline chama a rotina RTD e persiste atualizações em rtd_option_quotes.
A Fase 6 deve confirmar se isso é suficiente para considerar o RTD operacional ou se há dependência externa ainda não coberta.
