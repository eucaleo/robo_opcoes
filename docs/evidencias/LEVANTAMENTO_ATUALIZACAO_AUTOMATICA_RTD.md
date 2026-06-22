# Evidência - Pontos de atualização automática RTD

## Objetivo

Levantar somente pontos de código vivo relacionados a:

- refresh_data;
- eventos after do Tkinter;
- RTD;
- pipeline;
- payoff;
- cadastro de pernas;
- símbolos de opções.

## Observação

Este levantamento exclui documentação, cache, backups e o próprio arquivo de saída para evitar evidência poluída.


## Busca por refresh_data
UI/main_window.py:61:        self.refresh_data()
UI/main_window.py:131:        file_menu.add_command(label="Atualizar Dados", command=self.refresh_data)
UI/main_window.py:152:        self.root.bind("<F5>", lambda e: self.refresh_data())
UI/main_window.py:271:    def refresh_data(self):
UI/main_window.py:415:                self.root.after(0, self.refresh_data)
UI/main_window.py:539:            self.refresh_data()
UI/main_window.py:803:                        self.refresh_data()
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:25:  grep -n "Atualizar Dados\|Executar Pipeline\|def refresh_data\|def run_pipeline\|Pipeline executado\|status_bar.config" UI/main_window.py || true
scripts/fase-5-diagnostico-rtd.sh:29:    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:132:  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="

## Busca por after do Tkinter
UI/components/payoff_chart.py:131:            self.after(0, self.canvas.draw_idle)
UI/main_window.py:251:                self.root.after(
UI/main_window.py:261:                    self.root.after(
UI/main_window.py:415:                self.root.after(0, self.refresh_data)
UI/main_window.py:416:                self.root.after(
UI/main_window.py:421:                self.root.after(0, lambda: finish(False, "Timeout no recálculo"))
UI/main_window.py:427:                self.root.after(0, lambda: finish(False, "Falha no recálculo"))
UI/main_window.py:430:                self.root.after(0, lambda: finish(False, "Erro no recálculo"))
UI/main_window.py:664:            self.root.after(100, animate)
UI/main_window.py:780:                self.root.after(0, lambda: _set_status(text))
UI/main_window.py:808:                    self.root.after(0, _after_success)

## Busca por RTD
UI/main_window.py:475:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
UI/main_window.py:576:* Excel RTD  CSV Bridge
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
services/structure_leg_rtd_enrichment_service.py:19:    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
services/structure_leg_rtd_enrichment_service.py:21:    def __init__(self, rtd_option_quotes_repository: Any) -> None:
services/structure_leg_rtd_enrichment_service.py:22:        self._repo = rtd_option_quotes_repository
services/structure_leg_rtd_enrichment_service.py:38:        Campos enriquecidos via RTD:
services/structure_leg_rtd_enrichment_service.py:49:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py:123:                raise ValueError(f"missing required RTD field: {field}")
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
repositories/rtd_option_quotes_repository.py:12:    Leitura da tabela rtd_option_quotes.
repositories/rtd_option_quotes_repository.py:14:    Essa tabela é alimentada pelo CSV exportado da aba RTD_LINKS
repositories/rtd_option_quotes_repository.py:15:    e funciona como cache centralizado das cotações RTD de opções.
repositories/rtd_option_quotes_repository.py:48:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:80:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:112:            FROM rtd_option_quotes
repositories/structure_events_repository.py:15:Tabelas legadas como rtd_encerramentos_manuais e rtd_rolls_detectados seguem
repositories/ui_data_table_candidates.py:8:legados de staging, como tabelas rtd_*.
repositories/ui_data_table_candidates.py:13:    "rtd_consolidacoes",
repositories/ui_data_table_candidates.py:14:    "rtd_consolidations",
repositories/ui_data_table_candidates.py:16:    "rtd_decisions",
repositories/ui_data_table_candidates.py:21:    "rtd_payoff_points",
repositories/ui_data_table_candidates.py:22:    "rtd_payoff_curva",
domain/calculation_request.py:28:VALID_SOURCES        = {"rtd", "manual", "ui"}
domain/calculation_request.py:178:    source             : 'rtd' | 'manual' | 'ui'
domain/calculation_request.py:219:    O orquestrador monta este objeto a partir do DB e do bridge/RTD,
domain/market_snapshot.py:19:    RTD    = "rtd"
domain/market_snapshot.py:50:    source          : SnapshotSource  = SnapshotSource.RTD
domain/market_snapshot.py:60:    Atributos do cabeçalho (todos opcionais -- podem vir de RTD ou manual):
domain/market_snapshot.py:72:    source             : SnapshotSource                 = SnapshotSource.RTD
domain/payoff_features.py:109:    timestamp + aba                rastreabilidade opcional (legado RTD).
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

## Busca por pipeline
UI/components/details_panel.py:735:        """Chamado pelo MainWindow ao finalizar o subprocess do pipeline."""
UI/main_window.py:140:        tools_menu.add_command(label="Executar Pipeline", command=self.run_pipeline)
UI/main_window.py:397:                script_path = project_root / "scripts" / "run_derived_pipeline.py"
UI/main_window.py:399:                    script_path = project_root / "Scripts" / "run_derived_pipeline.py"
UI/main_window.py:435:    def _extract_pipeline_summary(self, stdout: str) -> Dict:
UI/main_window.py:436:        """Extrai o resumo JSON emitido por scripts/run_derived_pipeline.py."""
UI/main_window.py:450:    def _format_pipeline_value(self, value):
UI/main_window.py:456:    def _build_pipeline_feedback_message(self, stdout: str) -> str:
UI/main_window.py:457:        """Monta mensagem amigável para o usuário após executar pipeline."""
UI/main_window.py:458:        summary = self._extract_pipeline_summary(stdout)
UI/main_window.py:463:                "Resumo operacional não disponível no stdout do pipeline."
UI/main_window.py:470:            f"- Estruturas: {self._format_pipeline_value(summary.get('structures'))}",
UI/main_window.py:471:            f"- Decisões: {self._format_pipeline_value(summary.get('decisions'))}",
UI/main_window.py:472:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
UI/main_window.py:473:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
UI/main_window.py:474:            f"- Execuções de pricing: {self._format_pipeline_value(summary.get('pricing_executions'))}",
UI/main_window.py:475:            f"- Cotações RTD atualizadas: {self._format_pipeline_value(summary.get('rtd_quotes_updated'))}",
UI/main_window.py:476:            f"- Avisos: {self._format_pipeline_value(summary.get('warnings'))}",
UI/main_window.py:477:            f"- Erros: {self._format_pipeline_value(summary.get('errors'))}",
UI/main_window.py:481:    def _build_pipeline_status_message(self, stdout: str) -> str:
UI/main_window.py:482:        """Monta texto curto para status bar após pipeline."""
UI/main_window.py:483:        summary = self._extract_pipeline_summary(stdout)
UI/main_window.py:487:        decisions = self._format_pipeline_value(summary.get("decisions"))
UI/main_window.py:488:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
UI/main_window.py:489:        errors = self._format_pipeline_value(summary.get("errors"))
UI/main_window.py:497:    def run_pipeline(self):
UI/main_window.py:498:        """Executa o pipeline de derivados."""
UI/main_window.py:501:            "Executar pipeline de derivados?\nIsso pode demorar alguns segundos.",
UI/main_window.py:506:        self.status_bar.config(text="Executando pipeline...")
UI/main_window.py:510:            script_path = project_root / "scripts" / "run_derived_pipeline.py"
UI/main_window.py:512:                script_path = project_root / "Scripts" / "run_derived_pipeline.py"
UI/main_window.py:516:                    f"Não achei o script do pipeline em: {script_path}"
UI/main_window.py:535:            feedback = self._build_pipeline_feedback_message(res.stdout or "")
UI/main_window.py:536:            status_msg = self._build_pipeline_status_message(res.stdout or "")
UI/main_window.py:552:            messagebox.showerror("Erro", f"Erro ao executar pipeline: {e}")
UI/main_window.py:553:            self.status_bar.config(text="Erro ao executar pipeline")
services/calculation_orchestrator.py:4:# alteracao_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
services/calculation_orchestrator.py:6:#           run_full_pipeline_from_db
services/calculation_orchestrator.py:108:# Funcoes legadas de pipeline (alteracao_46/47 -- mantidas para
services/calculation_orchestrator.py:198:def run_full_pipeline(
services/calculation_orchestrator.py:205:    """alteracao_47: pipeline completo payoff + decision."""
services/calculation_orchestrator.py:338:    # run_payoff / run_decision / run_full_pipeline
services/calculation_orchestrator.py:386:    def run_full_pipeline(
services/calculation_orchestrator.py:498:    def run_full_pipeline_from_db(
services/calculation_orchestrator.py:512:        pipeline_result = self.run_full_pipeline(request)
services/calculation_orchestrator.py:516:            "payoff":       pipeline_result["payoff"],
services/calculation_orchestrator.py:517:            "decision":     pipeline_result["decision"],
services/canonical_input_service.py:61:            # com pipeline legado. Remover quando legado for desligado.
services/canonical_pricing_facade.py:323:    Orquestra o pipeline canônico ponta a ponta:
services/pricing_execution_persistence_service.py:5:from repositories.pricing_executions_repository import PricingExecutionsRepository
services/pricing_execution_persistence_service.py:15:        pricing_executions_repository: PricingExecutionsRepository | None = None,
services/pricing_execution_persistence_service.py:19:        self.pricing_executions_repository = (
services/pricing_execution_persistence_service.py:20:            pricing_executions_repository or PricingExecutionsRepository()
services/pricing_execution_persistence_service.py:46:        record = self.pricing_executions_repository.save_execution(
services/pricing_execution_query_service.py:4:from repositories.pricing_executions_repository import PricingExecutionsRepository
services/pricing_execution_query_service.py:10:        pricing_executions_repository: PricingExecutionsRepository | None = None,
services/pricing_execution_query_service.py:12:        self.pricing_executions_repository = (
services/pricing_execution_query_service.py:13:            pricing_executions_repository or PricingExecutionsRepository()
services/pricing_execution_query_service.py:44:        return self.pricing_executions_repository.list_executions()
services/pricing_execution_query_service.py:58:            executions = self.pricing_executions_repository.list_executions(
services/pricing_execution_query_service.py:68:            executions = self.pricing_executions_repository.list_executions()
services/pricing_execution_query_service.py:231:        execution = self.pricing_executions_repository.get_execution(execution_id)
repositories/pricing_executions_repository.py:58:                INSERT INTO pricing_executions (
repositories/pricing_executions_repository.py:103:                "SELECT * FROM pricing_executions WHERE id = ?",
repositories/pricing_executions_repository.py:146:                SELECT * FROM pricing_executions
repositories/pricing_executions_repository.py:185:                f"SELECT COUNT(*) FROM pricing_executions {where}",
repositories/pricing_executions_repository.py:208:                SELECT * FROM pricing_executions
scripts/check_rota_desenvolvimento.py:392:        "run_derived_pipeline.py",
scripts/dev/close_phase_5f_ui_pipeline.sh:9:# Fase 5F - Validacao da UI do resumo do pipeline
scripts/dev/close_phase_5f_ui_pipeline.sh:13:Validar que a interface executa o pipeline e exibe corretamente o resumo operacional ao usuario.
scripts/dev/close_phase_5f_ui_pipeline.sh:25:A interface exibiu mensagem de sucesso apos execucao do pipeline.
scripts/dev/close_phase_5f_ui_pipeline.sh:52:    aab7e92 Integra importacao RTD CSV ao pipeline derived
scripts/dev/close_phase_5f_ui_pipeline.sh:54:    711f088 fase 4: detalha feedback operacional do pipeline
scripts/dev/close_phase_5f_ui_pipeline.sh:81:    Compiling 'ATT/tests\\test_run_derived_pipeline_rtd_integration.py'...
scripts/dev/close_phase_5f_ui_pipeline.sh:86:## Evidencia do pipeline pela UI
scripts/dev/close_phase_5f_ui_pipeline.sh:88:A UI executou o pipeline e registrou no console:
scripts/dev/close_phase_5f_ui_pipeline.sh:134:      "pricing_executions": null,
scripts/dev/close_phase_5f_ui_pipeline.sh:178:Isso nao bloqueia a Fase 5F, pois o objetivo desta validacao era confirmar que a interface exibe corretamente o resumo operacional principal do pipeline, incluindo:
scripts/dev/close_phase_5f_ui_pipeline.sh:191:A UI confirma a execucao do pipeline, apresenta o resumo operacional esperado, reflete corretamente os dados persistidos no derived.db e mantem coerencia com a execucao em terminal.
scripts/dev/close_phase_6_integrated_validation.sh:19:- pipeline operacional;
scripts/dev/close_phase_6_integrated_validation.sh:40:| Fase 4 | Validada | Feedback operacional do pipeline |
scripts/dev/close_phase_6_integrated_validation.sh:41:| Fase 5F | Validada | UI do resumo operacional do pipeline |
scripts/dev/close_phase_6_integrated_validation.sh:147:- pipeline executando pela UI;
scripts/dev/open_phase_6_integrated_validation.sh:21:- pipeline operacional;
scripts/dev/open_phase_6_integrated_validation.sh:50:| Fase 4 | Validada | Feedback operacional do pipeline |
scripts/dev/open_phase_6_integrated_validation.sh:51:| Fase 5F | Validada | UI do resumo operacional do pipeline |
scripts/dev/open_phase_6_integrated_validation.sh:78:- Confirmar existencia dos scripts de pipeline
scripts/dev/open_phase_6_integrated_validation.sh:95:- Nenhuma regressao em pipeline
scripts/dev/open_phase_6_integrated_validation.sh:98:### 3. Validacao do pipeline
scripts/dev/open_phase_6_integrated_validation.sh:164:- o pipeline executar sem erros;
scripts/dev/open_phase_7_operational_consolidation.sh:28:- Confirmar fluxo operacional do pipeline.
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:32:        | grep -Ei 'structure|estrutura|payoff|decision|decis|pipeline|rtd|repository|service|dialog|editor|manual|leg' \
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:55:        "scripts/run_derived_pipeline.py"
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:65:        "pricing_executions",
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:116:        "pricing_executions",
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:186:    (app_db, ["pricing_executions", "structure_snapshots", "structure_leg_snapshots"]),
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:293:    (app_db, ["pricing_executions", "structure_snapshots", "structure_leg_snapshots"]),
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:303:    (app_db, "pricing_executions"),
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:107:        "pricing_executions",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:218:        "pricing_executions",
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:25:  grep -n "Atualizar Dados\|Executar Pipeline\|def refresh_data\|def run_pipeline\|Pipeline executado\|status_bar.config" UI/main_window.py || true
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:28:  echo "== scripts/run_derived_pipeline.py pontos principais =="
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:29:  grep -n "def main\|print\|run\|pipeline\|payoff\|decision\|summary\|count\|return" scripts/run_derived_pipeline.py || true
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:33:  grep -n "def run_full_pipeline\|def run_full_pipeline_from_db\|payoff\|decision\|return" services/calculation_orchestrator.py || true
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:48:  echo "== Trecho scripts/run_derived_pipeline.py 1-180 =="
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:49:  sed -n '1,180p' scripts/run_derived_pipeline.py
scripts/fase-5-diagnostico-rtd.sh:29:    -E "Atualizar Dados|refresh_data|run_pipeline|Executar Pipeline" UI scripts services db repositories domain . 2>/dev/null | head -300
scripts/fase-5-diagnostico-rtd.sh:132:  echo "== Trecho UI/main_window.py refresh_data e run_pipeline =="
scripts/fase-5-diagnostico-rtd.sh:136:  echo "== Trecho scripts/run_derived_pipeline.py =="
scripts/fase-5-diagnostico-rtd.sh:137:  sed -n '1,240p' scripts/run_derived_pipeline.py 2>/dev/null
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:49:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:70:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:90:  echo "== Testes vigentes relacionados ao pipeline/import/audit RTD =="
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:92:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5c-restaurar-rtd-historico.sh:17:  "scripts/run_lista_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:18:  "scripts/run_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:23:  "ATT/tests/test_run_rtd_option_quotes_pipeline.py"
scripts/fase-5c-restaurar-rtd-historico.sh:74:    scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5c-restaurar-rtd-historico.sh:118:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:66:  python scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:73:  python scripts/run_rtd_option_quotes_pipeline.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:156:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:22:  echo "== scripts/run_derived_pipeline.py =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:23:  if [ -f scripts/run_derived_pipeline.py ]; then
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:24:    sed -n '1,260p' scripts/run_derived_pipeline.py
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:26:    echo "ERRO: scripts/run_derived_pipeline.py nao encontrado"
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:40:  echo "== Ocorrencias de run_derived_pipeline =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:41:  grep -R "run_derived_pipeline" -n . \
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:61:  echo "== Testes relacionados a derived pipeline/orquestracao =="
scripts/fase-5e-diagnosticar-integracao-rtd-derived.sh:62:  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:7:path = Path("scripts/run_derived_pipeline.py")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:47:def _parse_rtd_pipeline_metrics(output: str) -> dict:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:48:    """Extrai métricas textuais emitidas pelo pipeline RTD restaurado."""
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:86:    - Delega importação + auditoria para scripts/run_rtd_option_quotes_pipeline.py.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:89:    pipeline_script = repo_root / "scripts" / "run_rtd_option_quotes_pipeline.py"
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:93:    if not pipeline_script.exists():
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:98:            "message": f"Script RTD não encontrado: {pipeline_script}",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:119:        str(pipeline_script),
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:142:    metrics = _parse_rtd_pipeline_metrics(stdout)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:192:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:199:    - Apenas lê contagens do banco depois que o pipeline RTD CSV já rodou.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:238:            "pricing_executions": _first_count(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:240:                "pricing_executions",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:259:    parser = argparse.ArgumentParser(description="Run derived pipeline")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:273:        help="Caminho do CSV RTD usado pelo pipeline derivado",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:313:            summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:321:        summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:326:    summary = _collect_pipeline_summary(rtd_result)
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:333:    print(f"  Execuções de pricing: {_display_summary_value(summary.get('pricing_executions'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:350:cat > ATT/tests/test_run_derived_pipeline_rtd_integration.py <<'PY'
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:357:SCRIPT_PATH = ROOT / "scripts" / "run_derived_pipeline.py"
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:362:        "run_derived_pipeline_under_test",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:371:def test_parse_rtd_pipeline_metrics_from_stdout():
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:384:    assert module._parse_rtd_pipeline_metrics(output) == {
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:400:def test_run_rtd_option_quotes_import_uses_csv_pipeline_without_excel_or_powershell(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:411:    (scripts_dir / "run_rtd_option_quotes_pipeline.py").write_text(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:412:        "# fake rtd csv pipeline\n",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:454:    assert command[1].endswith("run_rtd_option_quotes_pipeline.py")
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:4:OUT="docs/checkpoints/evidencias/fase-5e-validacao-integracao-rtd-derived-pipeline.txt"
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:22:  echo "== Diff scripts/run_derived_pipeline.py =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:23:  git diff -- scripts/run_derived_pipeline.py
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:27:  sed -n '1,260p' ATT/tests/test_run_derived_pipeline_rtd_integration.py
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:31:  python -m py_compile scripts/run_derived_pipeline.py
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:35:  echo "== Testes focados RTD/pipeline =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:37:    ATT/tests/test_run_derived_pipeline_rtd_integration.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:38:    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:45:  echo "== Execucao run_derived_pipeline.py --no-cleanup =="
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:46:  python scripts/run_derived_pipeline.py --no-cleanup
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:49:  echo "== Auditoria derived.db depois do pipeline derivado =="
scripts/run_derived_pipeline.py:39:def _parse_rtd_pipeline_metrics(output: str) -> dict:
scripts/run_derived_pipeline.py:40:    """Extrai métricas textuais emitidas pelo pipeline RTD restaurado."""
scripts/run_derived_pipeline.py:78:    - Delega importação + auditoria para scripts/run_rtd_option_quotes_pipeline.py.
scripts/run_derived_pipeline.py:81:    pipeline_script = repo_root / "scripts" / "run_rtd_option_quotes_pipeline.py"
scripts/run_derived_pipeline.py:85:    if not pipeline_script.exists():
scripts/run_derived_pipeline.py:90:            "message": f"Script RTD não encontrado: {pipeline_script}",
scripts/run_derived_pipeline.py:111:        str(pipeline_script),
scripts/run_derived_pipeline.py:134:    metrics = _parse_rtd_pipeline_metrics(stdout)
scripts/run_derived_pipeline.py:184:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
scripts/run_derived_pipeline.py:191:    - Apenas lê contagens do banco depois que o pipeline RTD CSV já rodou.
scripts/run_derived_pipeline.py:230:            "pricing_executions": _first_count(
scripts/run_derived_pipeline.py:232:                "pricing_executions",
scripts/run_derived_pipeline.py:251:    parser = argparse.ArgumentParser(description="Run derived pipeline")
scripts/run_derived_pipeline.py:265:        help="Caminho do CSV RTD usado pelo pipeline derivado",
scripts/run_derived_pipeline.py:305:            summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:313:        summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:318:    summary = _collect_pipeline_summary(rtd_result)
scripts/run_derived_pipeline.py:325:    print(f"  Execuções de pricing: {_display_summary_value(summary.get('pricing_executions'))}")
scripts/run_lista_rtd_option_quotes_pipeline.py:10:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS
scripts/run_lista_rtd_option_quotes_pipeline.py:11:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS --json
scripts/run_lista_rtd_option_quotes_pipeline.py:12:    python scripts/run_lista_rtd_option_quotes_pipeline.py --dry-run --json
scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
scripts/run_rtd_option_quotes_pipeline.py:3:Executa o pipeline operacional de cotações RTD de opções.
scripts/run_rtd_option_quotes_pipeline.py:11:    python scripts/run_rtd_option_quotes_pipeline.py
scripts/run_rtd_option_quotes_pipeline.py:12:    python scripts/run_rtd_option_quotes_pipeline.py --csv dados/RTD_LINKS.csv --db dados/app.db
scripts/run_rtd_option_quotes_pipeline.py:13:    python scripts/run_rtd_option_quotes_pipeline.py --dry-run
scripts/run_rtd_option_quotes_pipeline.py:14:    python scripts/run_rtd_option_quotes_pipeline.py --fail-on-warn
scripts/run_rtd_option_quotes_pipeline.py:88:def run_pipeline(
scripts/run_rtd_option_quotes_pipeline.py:173:        help="Faz o pipeline retornar falha quando a auditoria retornar warn.",
scripts/run_rtd_option_quotes_pipeline.py:182:    return run_pipeline(
scripts/run_rtd_refresh_full.py:271:    print("OK: pipeline RTD finalizado.")

## Busca por payoff
UI/components/details_panel.py:11:    def __init__(self, parent, on_recalculate=None, app_db_path=None):
UI/components/details_panel.py:13:        self._on_recalculate_cb = on_recalculate
UI/components/details_panel.py:33:            if hasattr(self, "btn_recalculate") and self.btn_recalculate:
UI/components/details_panel.py:34:                self.btn_recalculate.config(
UI/components/details_panel.py:411:            "payoff_curve_points",
UI/components/details_panel.py:625:        self.btn_recalculate = ttk.Button(
UI/components/details_panel.py:628:            command=self._on_recalculate_click,
UI/components/details_panel.py:630:        self.btn_recalculate.pack(side="left", padx=(0, 10))
UI/components/details_panel.py:920:    def _fetch_payoff_points_from_derived(self, structure_id):
UI/components/details_panel.py:922:        alteracao_36: filtra por structure_id (INTEGER) em payoff_curve_points.
UI/components/details_panel.py:934:                FROM payoff_curve_points
UI/components/details_panel.py:975:                "SELECT COUNT(*) AS n FROM payoff_curve_points WHERE structure_id = ?",
UI/components/details_panel.py:980:                "source_table": "derived.db:structure_decisions / payoff_curve_points",
UI/components/details_panel.py:1029:        pts = self._fetch_payoff_points_from_derived(structure_id)
UI/components/details_panel.py:1046:    def _on_recalculate_click(self):
UI/components/details_panel.py:1079:        if callable(getattr(self, "_on_recalculate_cb", None)):
UI/components/details_panel.py:1086:                self._on_recalculate_cb(structure_id)
UI/components/payoff_chart.py:1:# UI/components/payoff_chart.py
UI/components/payoff_chart.py:8:from UI.debug_utils import payoff_debug, payoff_info
UI/components/payoff_chart.py:170:        payoff_points: List[Dict],
UI/components/payoff_chart.py:178:        self._last_points = list(payoff_points) if payoff_points else []
UI/components/payoff_chart.py:182:            payoff_points, decision_data, overlay_curve=self._fixed_curve
UI/components/payoff_chart.py:187:        payoff_debug("FIX clicked -- id=", id(self))
UI/components/payoff_chart.py:216:        payoff_debug("CLEAR comparison -- id=", id(self))
UI/components/payoff_chart.py:258:        payoff_points: List[Dict],
UI/components/payoff_chart.py:268:        if not payoff_points:
UI/components/payoff_chart.py:269:            self.ax.set_title("Sem dados de payoff")
UI/components/payoff_chart.py:281:        for p in payoff_points:
UI/components/payoff_chart.py:290:            payoff_info("ERROR: não consegui extrair xs/ys de payoff_points.")
UI/components/payoff_chart.py:291:            self.ax.set_title("Sem dados de payoff")
UI/components/payoff_chart.py:297:        payoff_debug(
UI/components/payoff_chart.py:300:        payoff_debug(
UI/components/payoff_chart.py:453:            p, ["point_pl", "pl", "y", "pnl", "payoff", "profit_loss", "pl_value"]
UI/debug_utils.py:24:def payoff_debug(*args, **kwargs):
UI/debug_utils.py:25:    """Log de payoff chart apenas se debug ativo"""
UI/debug_utils.py:29:def payoff_info(*args, **kwargs):
UI/debug_utils.py:30:    """Log de payoff sempre"""
UI/main_window.py:5:Carrega dados de derived.db e app.db para exibir decisões e payoffs
UI/main_window.py:8:from UI.components.payoff_chart import PayoffChart
UI/main_window.py:40:        self._payoff_worker_id = 0
UI/main_window.py:46:        self._loading_payoff = False
UI/main_window.py:99:            on_recalculate=self.recalculate_structure,
UI/main_window.py:108:        self.payoff_chart = PayoffChart(chart_frame)
UI/main_window.py:109:        self.payoff_chart.pack(fill="both", expand=True, padx=5, pady=5)
UI/main_window.py:173:        alteracao_36: structure_id é suficiente para carregar payoff -- timestamp não é obrigatório.
UI/main_window.py:186:        # Carregar payoff em background -- apenas structure_id necessário
UI/main_window.py:191:            self._start_payoff_load(structure_id, timestamp, decision_data)
UI/main_window.py:193:            self.payoff_chart.clear()
UI/main_window.py:194:            self.status_bar.config(text="Dados insuficientes para payoff")
UI/main_window.py:196:    def _start_payoff_load(
UI/main_window.py:202:        """Inicia carregamento de payoff em thread separada.
UI/main_window.py:208:        self._payoff_worker_id += 1
UI/main_window.py:209:        current_worker_id = self._payoff_worker_id
UI/main_window.py:211:        if self._loading_payoff:
UI/main_window.py:212:            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
UI/main_window.py:214:            self.status_bar.config(text="Carregando payoff...")
UI/main_window.py:216:        self._loading_payoff = True
UI/main_window.py:220:                points, info_dict = self.data_model.get_payoff_curve_info(
UI/main_window.py:225:                        f"payoff structure_id={structure_id} ts_req={timestamp} "
UI/main_window.py:248:                if current_worker_id != self._payoff_worker_id:
UI/main_window.py:253:                    self._finish_payoff_load,
UI/main_window.py:260:                if current_worker_id == self._payoff_worker_id:
UI/main_window.py:263:                        self._handle_payoff_error,
UI/main_window.py:314:                        self._start_payoff_load(target_sid, target_ts, d)
UI/main_window.py:325:                    self.payoff_chart.clear()
UI/main_window.py:352:    def recalculate_structure(self, structure_id: str):
UI/main_window.py:355:        alteracao_36: recalculate_aba() removida; este é o único entry point.
UI/main_window.py:369:            self.payoff_chart.fix_current_curve()
UI/main_window.py:472:            f"- Pontos de payoff: {self._format_pipeline_value(summary.get('payoff_points'))}",
UI/main_window.py:473:            f"- Resumos de payoff: {self._format_pipeline_value(summary.get('payoff_summaries'))}",
UI/main_window.py:488:        payoff_points = self._format_pipeline_value(summary.get("payoff_points"))
UI/main_window.py:493:            f"pontos_payoff={payoff_points}; erros={errors}"
UI/main_window.py:573:Pipeline automático de payoff e decisões
UI/main_window.py:585:    # Handlers de payoff (thread  main thread)
UI/main_window.py:588:    def _finish_payoff_load(
UI/main_window.py:596:        if worker_id != self._payoff_worker_id:
UI/main_window.py:599:        self._loading_payoff = False
UI/main_window.py:604:                overlays = self.payoff_chart.update_chart(points, decision_data)
UI/main_window.py:622:                src = (info_dict or {}).get("source_table", "payoff_curve_points")
UI/main_window.py:629:                self.payoff_chart.clear()
UI/main_window.py:630:                self.status_bar.config(text="Sem dados de payoff para esta seleção")
UI/main_window.py:632:            self._handle_payoff_error(str(e), worker_id)
UI/main_window.py:634:    def _handle_payoff_error(self, error_msg: str, worker_id: int):
UI/main_window.py:635:        if worker_id != self._payoff_worker_id:
UI/main_window.py:637:        self._loading_payoff = False
UI/main_window.py:640:            self.payoff_chart.clear()
UI/main_window.py:643:        self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}")
UI/main_window.py:644:        print(f"[UI] Erro no payoff: {error_msg}")
UI/main_window.py:766:        Recalcula pricing/payoff/decisão após criação ou edição manual.
UI/main_window.py:785:        _post_status(f"Estrutura {sid} salva. Recalculando payoff...")
UI/main_window.py:801:                    _set_status(f"Estrutura {sid} salva e payoff recalculado.")
UI/models/ui_data.py:40:    "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
UI/models/ui_data.py:61:        self._payoff_table: Optional[str] = None
UI/models/ui_data.py:63:        self._payoff_cols: Dict[str, str] = {}
UI/models/ui_data.py:66:        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
UI/models/ui_data.py:67:        self._payoff_cache_max = 128
UI/models/ui_data.py:103:                self._payoff_table = t
UI/models/ui_data.py:124:    def _build_payoff_colmap(self):
UI/models/ui_data.py:125:        if not self._payoff_table:
UI/models/ui_data.py:126:            self._payoff_cols = {}
UI/models/ui_data.py:129:        cols = self._inspect_columns(self._payoff_table)
UI/models/ui_data.py:132:        if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:142:            print(f"[UI] Usando contrato canônico para {self._payoff_table}")
UI/models/ui_data.py:145:            print(f"[UI] Usando aliases flexíveis para {self._payoff_table}")
UI/models/ui_data.py:154:        self._payoff_cols = colmap
UI/models/ui_data.py:156:        if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols):
UI/models/ui_data.py:158:                f"Tabela {self._payoff_table} não apresenta colunas obrigatórias "
UI/models/ui_data.py:159:                f"para payoff (point_spot/point_pl ou spot/pl)."
UI/models/ui_data.py:163:        if "structure_id" not in self._payoff_cols:
UI/models/ui_data.py:165:                f"[UI] AVISO: {self._payoff_table} nao tem coluna structure_id. "
UI/models/ui_data.py:205:        self._build_payoff_colmap()
UI/models/ui_data.py:401:    def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:
UI/models/ui_data.py:410:        if hasattr(self, "_payoff_cache") and cache_key in self._payoff_cache:
UI/models/ui_data.py:411:            cached = self._payoff_cache[cache_key]
UI/models/ui_data.py:417:        if not self._payoff_table:
UI/models/ui_data.py:419:                "Tabela de payoff não encontrada. Esperadas: "
UI/models/ui_data.py:424:        p = self._payoff_cols
UI/models/ui_data.py:429:                f"Tabela {self._payoff_table} não possui colunas esperadas para payoff."
UI/models/ui_data.py:439:            FROM {self._payoff_table}
UI/models/ui_data.py:452:            FROM {self._payoff_table}
UI/models/ui_data.py:466:            FROM {self._payoff_table}
UI/models/ui_data.py:476:    def get_payoff_curve_info(
UI/models/ui_data.py:487:        if not self._payoff_table:
UI/models/ui_data.py:502:        p = self._payoff_cols
UI/models/ui_data.py:516:                "source_table": self._payoff_table,
UI/models/ui_data.py:524:            if self._payoff_table == "payoff_curve_points":
UI/models/ui_data.py:527:                if "meta_json" in self._inspect_columns("payoff_curve_points"):
UI/models/ui_data.py:532:                    f"FROM payoff_curve_points "
UI/models/ui_data.py:541:                        f"SELECT timestamp FROM payoff_curve_points "
UI/models/ui_data.py:562:                        f"Tabela {self._payoff_table} não possui colunas esperadas."
UI/models/ui_data.py:567:                    f"FROM {self._payoff_table} "
UI/models/ui_data.py:576:                        f"SELECT {p['timestamp']} AS ts FROM {self._payoff_table} "
UI/models/ui_data.py:639:        payoff_ok = bool(self._payoff_table)
UI/models/ui_data.py:642:        p = self._payoff_cols
UI/models/ui_data.py:653:            f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}\n"
UI/models/ui_data.py:659:        self._payoff_cache = {}
UI/models/ui_data.py:667:            return self._payoff_cache.get(key)
UI/models/ui_data.py:673:            self._payoff_cache[key] = value
UI/models/ui_data.py:674:            mx = getattr(self, "_payoff_cache_max", 0) or 0
UI/models/ui_data.py:675:            if mx > 0 and len(self._payoff_cache) > mx:
UI/models/ui_data.py:676:                self._payoff_cache.pop(next(iter(self._payoff_cache)))
services/calculation_orchestrator.py:3:# alteracao_46: _request_to_payoff_dict, run_payoff, run_decision
services/calculation_orchestrator.py:20:from domain.payoff import compute_payoff_from_canonical_input
services/calculation_orchestrator.py:111:def _request_to_payoff_dict(
services/calculation_orchestrator.py:149:def run_payoff(
services/calculation_orchestrator.py:156:    """Executa calculo de payoff a partir de um CalculationRequest."""
services/calculation_orchestrator.py:157:    canonical = _request_to_payoff_dict(request, extra_meta=extra_meta)
services/calculation_orchestrator.py:158:    return compute_payoff_from_canonical_input(
services/calculation_orchestrator.py:168:    payoff: Optional[dict] = None,
services/calculation_orchestrator.py:175:    if _pl_max is None and payoff:
services/calculation_orchestrator.py:176:        _pl_max = float(payoff.get("pl_max") or 0.0)
services/calculation_orchestrator.py:181:    if _pl_atual is None and payoff:
services/calculation_orchestrator.py:182:        _pl_atual = float(payoff.get("pl_atual") or payoff.get("pl_now") or 0.0)
services/calculation_orchestrator.py:195:    return compute_decision_from_contract(contract, payoff=payoff)
services/calculation_orchestrator.py:205:    """alteracao_47: pipeline completo payoff + decision."""
services/calculation_orchestrator.py:206:    payoff_result = run_payoff(
services/calculation_orchestrator.py:213:    decision_result = run_decision(request, payoff=payoff_result)
services/calculation_orchestrator.py:216:        "payoff":           payoff_result,
services/calculation_orchestrator.py:233:    - Executar payoff e decisao sem acessar raw DB diretamente
services/calculation_orchestrator.py:303:    def _request_to_payoff_dict(self, request: CalculationRequest) -> Dict[str, Any]:
services/calculation_orchestrator.py:304:        """Converte CalculationRequest para o dict de payoff."""
services/calculation_orchestrator.py:338:    # run_payoff / run_decision / run_full_pipeline
services/calculation_orchestrator.py:341:    def run_payoff(
services/calculation_orchestrator.py:348:        canonical = self._request_to_payoff_dict(request)
services/calculation_orchestrator.py:349:        return compute_payoff_from_canonical_input(
services/calculation_orchestrator.py:359:        payoff_result: Optional[Dict[str, Any]] = None,
services/calculation_orchestrator.py:361:        if payoff_result is None:
services/calculation_orchestrator.py:362:            payoff_result = self.run_payoff(request)
services/calculation_orchestrator.py:365:            payoff_result.get("pl_max") or payoff_result.get("max_profit") or 0.0
services/calculation_orchestrator.py:368:            payoff_result.get("pl_atual")
services/calculation_orchestrator.py:369:            or payoff_result.get("current_pl")
services/calculation_orchestrator.py:370:            or payoff_result.get("pl_now")
services/calculation_orchestrator.py:374:            payoff_result.get("dte_min")
services/calculation_orchestrator.py:384:        return compute_decision_from_contract(contract, payoff=payoff_result)
services/calculation_orchestrator.py:393:        """Executa run_payoff -> run_decision em sequencia."""
services/calculation_orchestrator.py:394:        payoff_result   = self.run_payoff(request, low_pct=low_pct, high_pct=high_pct, step_pct=step_pct)
services/calculation_orchestrator.py:395:        decision_result = self.run_decision(request, payoff_result=payoff_result)
services/calculation_orchestrator.py:398:            "payoff":           payoff_result,
services/calculation_orchestrator.py:506:        Retorna dict com chaves: structure_id, payoff, decision.
services/calculation_orchestrator.py:516:            "payoff":       pipeline_result["payoff"],
services/canonical_input_service.py:199:        consumidores downstream (pricing, greeks, payoff) tenham os dados.
services/canonical_pricing_facade.py:21:  C5: DerivedPayoffPersistence injetado como payoff_persistence_port
services/canonical_pricing_facade.py:34:from services.derived_payoff_persistence import DerivedPayoffPersistence
services/canonical_pricing_facade.py:272:            # campos canônicos esperados pelo fluxo pricing/payoff
services/canonical_pricing_facade.py:347:            payoff_persistence_port=DerivedPayoffPersistence(),
services/derived_payoff_persistence.py:1:# services/derived_payoff_persistence.py
services/derived_payoff_persistence.py:6:from domain.payoff import compute_payoff_from_canonical_input
services/derived_payoff_persistence.py:7:from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload
services/derived_payoff_persistence.py:18:      2. Calcular a curva de payoff via domain/payoff.py
services/derived_payoff_persistence.py:33:            logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
services/derived_payoff_persistence.py:40:                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
services/derived_payoff_persistence.py:45:        # Timestamp único para payoff + decisão.
services/derived_payoff_persistence.py:49:        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
services/derived_payoff_persistence.py:50:        if not payoff_saved:
services/derived_payoff_persistence.py:52:                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
services/derived_payoff_persistence.py:60:                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
services/derived_payoff_persistence.py:66:    #  payoff                                                          #
services/derived_payoff_persistence.py:69:    def _persist_payoff(
services/derived_payoff_persistence.py:77:            payoff_result = compute_payoff_from_canonical_input(canonical_input)
services/derived_payoff_persistence.py:79:            if not payoff_result.get("points"):
services/derived_payoff_persistence.py:81:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
services/derived_payoff_persistence.py:86:            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
services/derived_payoff_persistence.py:88:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
services/derived_payoff_persistence.py:89:                len(payoff_result["points"]),
services/derived_payoff_persistence.py:96:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
services/derived_payoff_persistence.py:166:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
services/derived_payoff_persistence.py:173:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
services/derived_payoff_persistence.py:186:        Normaliza aliases de direção para o contrato canônico de payoff.
services/derived_payoff_persistence.py:188:        domain/payoff.py exige leg["position_side"].
services/derived_payoff_persistence.py:221:    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
services/derived_payoff_persistence.py:224:        esperado por domain.compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:274:    def _normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:278:        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
services/derived_payoff_persistence.py:288:            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
services/derived_payoff_persistence.py:292:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
services/derived_payoff_persistence.py:307:        Monta o canonical_input esperado por compute_payoff_from_canonical_input().
services/derived_payoff_persistence.py:314:        # estrito de domain/payoff.py.
services/derived_payoff_persistence.py:316:            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
services/derived_payoff_persistence.py:331:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
services/derived_payoff_persistence.py:339:                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
services/derived_service.py:4:alteracao_30/alteracao_57c -- Servico de persistencia de dados derivados (payoff + decisoes).
services/derived_service.py:6:alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
services/derived_service.py:18:    cleanup_old_payoff_data,
services/derived_service.py:20:    insert_payoff_points,
services/derived_service.py:160:def save_payoff_curve(
services/derived_service.py:199:        return insert_payoff_points(
services/derived_service.py:210:def save_payoff_from_canonical_payload(
services/derived_service.py:211:    payoff: Dict[str, Any],
services/derived_service.py:219:        structure_id=payoff.get("structure_id"),
services/derived_service.py:220:        structure_name=payoff.get("structure_name"),
services/derived_service.py:221:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:224:    sid_from_payload = payoff.get("structure_id")
services/derived_service.py:232:        meta=payoff.get("meta"),
services/derived_service.py:234:        structure_name=payoff.get("structure_name"),
services/derived_service.py:235:        underlying_asset=payoff.get("underlying_asset"),
services/derived_service.py:236:        reference_date=payoff.get("reference_date"),
services/derived_service.py:237:        input_meta=payoff.get("input_meta"),
services/derived_service.py:242:        sig = inspect.signature(save_payoff_curve)
services/derived_service.py:254:        return save_payoff_curve(
services/derived_service.py:256:            points=payoff.get("points", []),
services/derived_service.py:257:            spot_ref=payoff.get("spot_ref"),
services/derived_service.py:263:    return save_payoff_curve(
services/derived_service.py:265:        points=payoff.get("points", []),
services/derived_service.py:266:        spot_ref=payoff.get("spot_ref"),
services/derived_service.py:371:        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
services/derived_service.py:373:        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
services/derived_service.py:380:def get_all_payoff_curves():
services/derived_service.py:385:            FROM payoff_curve_points
services/derived_service.py:400:def get_payoff_by_structure_id(structure_id: int):
services/derived_service.py:402:    alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff.
services/derived_service.py:403:    get_payoff_by_aba() removida da interface pública (alteracao_65).
services/derived_service.py:412:              FROM payoff_curve_points
services/derived_service.py:523:# get_payoff_by_aba() removida da interface pública.
services/derived_service.py:524:# get_payoff_by_structure_id() é o único ponto de entrada canônico.
services/derived_service.py:529:    alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id().
services/derived_service.py:530:    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
services/derived_service.py:533:    # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe.
services/derived_service.py:534:    # Chamadores legados devem migrar para get_payoff_by_structure_id().
services/derived_service.py:536:    def get_payoff_by_structure_id(self, structure_id: int):
services/derived_service.py:537:        """Retorna pontos de payoff para a estrutura informada."""
services/derived_service.py:538:        return get_payoff_by_structure_id(structure_id)
services/derived_service.py:540:    def save_payoff_curve(self, *args, **kwargs):
services/derived_service.py:541:        return save_payoff_curve(*args, **kwargs)
services/payoff_persistence_port.py:1:# services/payoff_persistence_port.py
services/payoff_persistence_port.py:7:    Contrato de persistência derivada (payoff + decisão).
services/pricing_execution_persistence_service.py:7:from services.payoff_persistence_port import PayoffPersistencePort
services/pricing_execution_persistence_service.py:16:        payoff_persistence_port: PayoffPersistencePort | None = None,
services/pricing_execution_persistence_service.py:22:        self._payoff_port = payoff_persistence_port
services/pricing_execution_persistence_service.py:67:        #  alteracao_21 -- persistência derivada (payoff + decisão)           #
services/pricing_execution_persistence_service.py:70:        if self._payoff_port is not None:
services/pricing_execution_persistence_service.py:72:                self._payoff_port.persist(
services/pricing_execution_persistence_service.py:78:                    "payoff_persistence_port.persist() falhou -- execução id=%s não afetada",
services/pricing_execution_persistence_service.py:124:                payoff_json=self._extract_result_field(inner, "payoff"),
services/structure_analysis_service.py:6:from domain.decision import compute_decision_from_payoff
services/structure_analysis_service.py:7:from domain.payoff import compute_payoff_from_canonical_input
services/structure_analysis_service.py:61:        # 6. Calcula payoff
services/structure_analysis_service.py:62:        payoff = compute_payoff_from_canonical_input(canonical_input)
services/structure_analysis_service.py:64:        # 7. Valida payoff -- se inválido, retorna HOLD com erro estruturado
services/structure_analysis_service.py:65:        if not payoff or not payoff.get("pl_max"):
services/structure_analysis_service.py:67:                "error": "payoff is required",
services/structure_analysis_service.py:69:                "reasons": ["invalid_payoff"],
services/structure_analysis_service.py:91:                "payoff":   payoff,
services/structure_analysis_service.py:96:        decision = compute_decision_from_payoff(
services/structure_analysis_service.py:97:            payoff=payoff,
services/structure_analysis_service.py:119:            "payoff":   payoff,
db/derived_repo.py:3:Repositório para operações com dados derivados (payoff e decisões).
db/derived_repo.py:4:Tabelas: payoff_curve_points, structure_decisions
db/derived_repo.py:6:Contrato canônico payoff: point_spot / point_pl (opção B).
db/derived_repo.py:20:  - fix: existing_payoff_cols -> existing_cols
db/derived_repo.py:74:# alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points
db/derived_repo.py:77:CREATE TABLE IF NOT EXISTS payoff_curve_points (
db/derived_repo.py:90:CREATE UNIQUE INDEX IF NOT EXISTS ux_payoff_snapshot
db/derived_repo.py:91:ON payoff_curve_points (timestamp, aba, point_spot)
db/derived_repo.py:96:CREATE INDEX IF NOT EXISTS ix_payoff_structure_id
db/derived_repo.py:97:ON payoff_curve_points (structure_id, timestamp)
db/derived_repo.py:138:        "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"
db/derived_repo.py:177:    # alteracao_36_A: migration incremental payoff_curve_points
db/derived_repo.py:178:    existing_cols = _table_columns(conn, "payoff_curve_points")
db/derived_repo.py:186:    # alteracao_36_B: index structure_id no payoff (após migration)
db/derived_repo.py:218:    alteracao_56: correções de bugs em _apply_schema e INSERTs do payoff.
db/derived_repo.py:329:    # Escrita -- payoff
db/derived_repo.py:332:    def write_payoff_snapshot_atomic(
db/derived_repo.py:354:                "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:359:                INSERT INTO payoff_curve_points
db/derived_repo.py:382:    def insert_payoff_points(
db/derived_repo.py:402:                INSERT OR REPLACE INTO payoff_curve_points
db/derived_repo.py:446:            # --- payoff ---
db/derived_repo.py:448:                "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:453:                INSERT INTO payoff_curve_points
db/derived_repo.py:488:    def get_payoff_points(
db/derived_repo.py:500:                    FROM payoff_curve_points
db/derived_repo.py:510:                    FROM payoff_curve_points
db/derived_repo.py:521:                    FROM payoff_curve_points
db/derived_repo.py:580:                LEFT JOIN payoff_curve_points p
db/derived_repo.py:588:                FROM payoff_curve_points p
db/derived_repo.py:607:    def cleanup_old_payoff_data(self, days_to_keep: int = 30) -> int:
db/derived_repo.py:611:                f"DELETE FROM payoff_curve_points "
db/derived_repo.py:676:def write_payoff_snapshot_atomic(
db/derived_repo.py:691:        "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
db/derived_repo.py:695:        INSERT INTO payoff_curve_points
db/derived_repo.py:764:        pc  = write_payoff_snapshot_atomic(conn, timestamp, aba, points, points_meta, structure_id=decision_dict.get("structure_id"))
db/derived_repo.py:769:def insert_payoff_points(
db/derived_repo.py:785:        INSERT OR REPLACE INTO payoff_curve_points
db/derived_repo.py:841:def get_payoff_points(
db/derived_repo.py:852:            FROM payoff_curve_points
db/derived_repo.py:859:            FROM payoff_curve_points
db/derived_repo.py:867:            FROM payoff_curve_points
db/derived_repo.py:881:        LEFT JOIN payoff_curve_points p ON (d.aba = p.aba AND d.timestamp = p.timestamp)
db/derived_repo.py:888:        FROM payoff_curve_points p
db/derived_repo.py:905:def cleanup_old_payoff_data(conn: sqlite3.Connection, days_to_keep: int = 30) -> int:
db/derived_repo.py:909:        DELETE FROM payoff_curve_points
db/migrations/add_structure_id_to_payoff_curve_points.py:1:# db/migrations/add_structure_id_to_payoff_curve_points.py
db/migrations/add_structure_id_to_payoff_curve_points.py:3:Migration: adiciona structure_id em payoff_curve_points
db/migrations/add_structure_id_to_payoff_curve_points.py:4:e payoff_curve_summary, com backfill via structure_decisions.
db/migrations/add_structure_id_to_payoff_curve_points.py:7:    python db/migrations/add_structure_id_to_payoff_curve_points.py
db/migrations/add_structure_id_to_payoff_curve_points.py:8:    python db/migrations/add_structure_id_to_payoff_curve_points.py --db dados/derived.db
db/migrations/add_structure_id_to_payoff_curve_points.py:18:    #  payoff_curve_points 
db/migrations/add_structure_id_to_payoff_curve_points.py:20:        "payoff_curve_points: verificar se structure_id já existe",
db/migrations/add_structure_id_to_payoff_curve_points.py:24:        "payoff_curve_points: ADD COLUMN structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:25:        "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER",
db/migrations/add_structure_id_to_payoff_curve_points.py:28:        "payoff_curve_points: BACKFILL structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:30:        UPDATE payoff_curve_points
db/migrations/add_structure_id_to_payoff_curve_points.py:34:            WHERE d.aba       = payoff_curve_points.aba
db/migrations/add_structure_id_to_payoff_curve_points.py:35:              AND d.timestamp = payoff_curve_points.timestamp
db/migrations/add_structure_id_to_payoff_curve_points.py:41:        "payoff_curve_points: CREATE INDEX sid+ts",
db/migrations/add_structure_id_to_payoff_curve_points.py:43:        CREATE INDEX IF NOT EXISTS idx_payoff_points_sid_ts
db/migrations/add_structure_id_to_payoff_curve_points.py:44:            ON payoff_curve_points (structure_id, timestamp)
db/migrations/add_structure_id_to_payoff_curve_points.py:47:    #  payoff_curve_summary 
db/migrations/add_structure_id_to_payoff_curve_points.py:49:        "payoff_curve_summary: ADD COLUMN structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:50:        "ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER",
db/migrations/add_structure_id_to_payoff_curve_points.py:53:        "payoff_curve_summary: BACKFILL structure_id",
db/migrations/add_structure_id_to_payoff_curve_points.py:55:        UPDATE payoff_curve_summary
db/migrations/add_structure_id_to_payoff_curve_points.py:59:            WHERE d.aba       = payoff_curve_summary.aba
db/migrations/add_structure_id_to_payoff_curve_points.py:60:              AND d.timestamp = payoff_curve_summary.timestamp
db/migrations/add_structure_id_to_payoff_curve_points.py:66:        "payoff_curve_summary: CREATE INDEX sid+ts",
db/migrations/add_structure_id_to_payoff_curve_points.py:68:        CREATE INDEX IF NOT EXISTS idx_payoff_summary_sid_ts
db/migrations/add_structure_id_to_payoff_curve_points.py:69:            ON payoff_curve_summary (structure_id, timestamp)
db/migrations/add_structure_id_to_payoff_curve_points.py:106:        for table in ("payoff_curve_points", "payoff_curve_summary"):
db/reader.py:15:    """Leitor para análise de pontos do payoff curve e decisões estruturais."""
db/reader.py:42:    def get_payoff_curve(self, ref: StructureRef, timestamp: Optional[str] = None) -> pd.DataFrame:
db/reader.py:44:        Retorna pontos do payoff curve como DataFrame.
db/reader.py:58:                    FROM payoff_curve_points
db/reader.py:67:                    FROM payoff_curve_points
db/reader.py:69:                        SELECT MAX(timestamp) FROM payoff_curve_points WHERE {ref.db_column()} = ?
db/schema.py:6:-- Curva de payoff (por ponto) usada no seu projeto
db/schema.py:7:CREATE TABLE IF NOT EXISTS payoff_curve_points (
db/schema.py:18:CREATE INDEX IF NOT EXISTS idx_payoff_timestamp_aba
db/schema.py:19:ON payoff_curve_points(timestamp, aba);
db/schema.py:21:CREATE INDEX IF NOT EXISTS idx_payoff_spot
db/schema.py:22:ON payoff_curve_points(point_spot);
db/schema.py:54:-- Compat: tabela esperada por código antigo/viewers (payoff_points)
db/schema.py:55:-- Vamos mapear para o mesmo conceito (pontos de payoff).
db/schema.py:56:CREATE TABLE IF NOT EXISTS payoff_points (
db/schema.py:59:    payoff_value REAL NOT NULL,
db/schema.py:64:CREATE INDEX IF NOT EXISTS idx_payoff_points_created_at
db/schema.py:65:ON payoff_points(created_at);
db/schema.py:67:CREATE INDEX IF NOT EXISTS idx_payoff_points_strategy
db/schema.py:68:ON payoff_points(strategy_type);
db/writer.py:13:    """Escritor para pontos do payoff curve e decisões estruturais."""
db/writer.py:27:    def save_payoff_points(self, 
db/writer.py:34:        Salva pontos do payoff curve.
db/writer.py:72:                INSERT INTO payoff_curve_points 
db/writer.py:138:    def get_payoff_history(self, ref: StructureRef, limit: int = 100) -> List[Dict]:
db/writer.py:139:        """Retorna histórico de payoff points para uma aba."""
db/writer.py:146:                FROM payoff_curve_points 
repositories/system_snapshots_repository.py:16:    "payoff_json",
repositories/system_snapshots_repository.py:90:        payoff_json: dict[str, Any] | list[Any] | None = None,
repositories/system_snapshots_repository.py:123:                    payoff_json,
repositories/system_snapshots_repository.py:140:                    _to_json(payoff_json),
repositories/ui_data_table_candidates.py:20:    "payoff_curve_points",
repositories/ui_data_table_candidates.py:21:    "rtd_payoff_points",
repositories/ui_data_table_candidates.py:22:    "rtd_payoff_curva",
repositories/ui_data_table_candidates.py:23:    "payoff_points",
domain/calculation_request.py:217:    Contrato canônico de entrada para qualquer cálculo de payoff/decisão.
domain/calculation_request.py:220:    e o domínio (payoff, decision) recebe SOMENTE este objeto -- sem
domain/decision.py:6:Funcoes canonicas: compute_decision_from_inputs, compute_decision_from_payoff,
domain/decision.py:32:def _interp_payoff(points: List[Tuple[float, float]], spot: float) -> float:
domain/decision.py:139:def compute_decision_from_payoff(
domain/decision.py:140:    payoff: Dict[str, Any],
domain/decision.py:147:    Decide a partir de um dict de payoff.
domain/decision.py:150:    if not payoff:
domain/decision.py:151:        why_dict = {"error": "payoff vazio ou invalido", "reason": "invalid_input"}
domain/decision.py:162:    pl_atual = payoff.get("pl_atual") or payoff.get("pl_now") or 0.0
domain/decision.py:163:    pl_max   = payoff.get("pl_max") or 0.0
domain/decision.py:166:    points = payoff.get("points") or []
domain/decision.py:167:    spot   = payoff.get("spot")
domain/decision.py:169:        pl_atual = _interp_payoff(points, float(spot))
domain/decision.py:195:    payoff: Optional[Dict[str, Any]] = None,
domain/decision.py:201:    if payoff:
domain/decision.py:202:        return compute_decision_from_payoff(payoff=payoff, dte_min=dte_min)
domain/payoff.py:27:def _compute_leg_payoff_at_expiration(leg: dict[str, Any], spot_at_expiration: float) -> float:
domain/payoff.py:43:    payoff_unit = intrinsic - premium_value
domain/payoff.py:46:        payoff_unit = -payoff_unit
domain/payoff.py:48:    return payoff_unit * quantity * multiplier
domain/payoff.py:51:def compute_payoff_curve_from_canonical_legs(
domain/payoff.py:90:            pl_total += _compute_leg_payoff_at_expiration(
domain/payoff.py:123:def compute_payoff_from_canonical_input(
domain/payoff.py:157:    result = compute_payoff_curve_from_canonical_legs(
domain/payoff_features.py:106:    Computa features da curva de payoff.
domain/payoff_features.py:146:    INSERT INTO payoff_curve_summary (
scripts/dev/close_phase_5f_ui_pipeline.sh:34:    - Pontos de payoff: 202
scripts/dev/close_phase_5f_ui_pipeline.sh:35:    - Resumos de payoff: n/d
scripts/dev/close_phase_5f_ui_pipeline.sh:55:    a1088b3 docs: add phase 3f payoff diagnostic evidence
scripts/dev/close_phase_5f_ui_pipeline.sh:56:    861c17f fix: normalize manual legs for derived payoff persistence
scripts/dev/close_phase_5f_ui_pipeline.sh:120:      Pontos de payoff: 202
scripts/dev/close_phase_5f_ui_pipeline.sh:121:      Resumos de payoff: n/d
scripts/dev/close_phase_5f_ui_pipeline.sh:132:      "payoff_points": 202,
scripts/dev/close_phase_5f_ui_pipeline.sh:133:      "payoff_summaries": null,
scripts/dev/close_phase_5f_ui_pipeline.sh:147:        "payoff_curve_points": 202,
scripts/dev/close_phase_5f_ui_pipeline.sh:162:| Pontos de payoff exibidos no resumo | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:166:| Curva de payoff visivel | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:169:| Contrato canonico de payoff_curve_points usado | OK |
scripts/dev/close_phase_5f_ui_pipeline.sh:176:Os campos Estruturas, Resumos de payoff e Execucoes de pricing permanecem como n/d.
scripts/dev/close_phase_5f_ui_pipeline.sh:181:- pontos de payoff;
scripts/dev/close_phase_6_integrated_validation.sh:21:- persistencia de payoff;
scripts/dev/close_phase_6_integrated_validation.sh:39:| Fase 3F | Validada | Diagnostico de payoff |
scripts/dev/close_phase_6_integrated_validation.sh:97:    - Pontos de payoff: 202
scripts/dev/close_phase_6_integrated_validation.sh:98:    - Resumos de payoff: n/d
scripts/dev/close_phase_6_integrated_validation.sh:117:| Pontos de payoff persistidos | OK |
scripts/dev/close_phase_6_integrated_validation.sh:118:| Curva de payoff visivel | OK |
scripts/dev/close_phase_6_integrated_validation.sh:134:| Pontos de payoff | 202 |
scripts/dev/close_phase_6_integrated_validation.sh:135:| Resumos de payoff | n/d |
scripts/dev/close_phase_6_integrated_validation.sh:143:Os campos Estruturas, Resumos de payoff e Execucoes de pricing permanecem como n/d.
scripts/dev/close_phase_6_integrated_validation.sh:149:- pontos de payoff persistidos;
scripts/dev/close_phase_6_integrated_validation.sh:150:- curva de payoff visivel;
scripts/dev/close_phase_6_integrated_validation.sh:163:O sistema confirma execucao operacional pela UI, persistencia em dados/derived.db, resumo operacional ao usuario, decisoes calculadas, curva de payoff disponivel e suite automatizada sem regressao.
scripts/dev/open_phase_6_integrated_validation.sh:23:- persistencia de payoff;
scripts/dev/open_phase_6_integrated_validation.sh:39:- Curvas de payoff
scripts/dev/open_phase_6_integrated_validation.sh:49:| Fase 3F | Validada | Diagnostico de payoff |
scripts/dev/open_phase_6_integrated_validation.sh:64:    - Pontos de payoff: 202
scripts/dev/open_phase_6_integrated_validation.sh:65:    - Resumos de payoff: n/d
scripts/dev/open_phase_6_integrated_validation.sh:93:- Nenhuma regressao em payoff
scripts/dev/open_phase_6_integrated_validation.sh:107:- Resumo operacional apresenta pontos de payoff
scripts/dev/open_phase_6_integrated_validation.sh:121:- Curva de payoff permanece visivel
scripts/dev/open_phase_6_integrated_validation.sh:130:- payoff_curve_points possui pontos persistidos
scripts/dev/open_phase_6_integrated_validation.sh:166:- as decisoes e a curva de payoff permanecerem visiveis;
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:5:OUT="$EVID_DIR/fase-3a-diagnostico-cadastro-payoff-decisoes.txt"
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:10:    echo "== Fase 3A - Diagnostico cadastro manual, payoff e decisoes =="
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:32:        | grep -Ei 'structure|estrutura|payoff|decision|decis|pipeline|rtd|repository|service|dialog|editor|manual|leg' \
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:39:    grep -RInE "structure_decisions|payoff_curve_points|manual|Manual|payoff|decision|decis|canonical|structure_id|Salvar|Aplicar Leg|must be numeric" . \
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:72:    if any(term in low for term in ["structure", "estrutura", "leg", "payoff", "decision", "decis", "rtd", "quote"]):
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:81:    "payoff_curve_points",
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:92:print("Schema resumido de estruturas, legs, payoff e decisoes:")
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:96:    if any(term in low for term in ["structure", "estrutura", "leg", "payoff", "decision", "decis"]):
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:113:terms = ("structure", "estrutura", "payoff", "decision", "decis", "manual", "leg")
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:127:    echo "6) Pytest focado em cadastro, structure, payoff, decision e leg"
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:129:    python -m pytest -q -k "manual or structure or payoff or decision or leg" || true
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:108:    if any(term in name for term in ["structure", "leg", "payoff", "decision", "rtd", "quote"]):
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:10:    echo "== Fase 3C - Diagnostico app.db, UI e fluxo pricing/payoff =="
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:66:        "payoff_curve_points",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:82:        if any(t in low for t in ["structure", "leg", "pricing", "payoff", "decision", "rtd", "manual"]):
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:28:    echo "3) Ocorrencias CanonicalPricingFacade e persistencia payoff/decision"
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:30:    grep -RInE "class CanonicalPricingFacade|def .*price|def .*pricing|def .*persist|save_payoff|save_decision|structure_decisions|payoff_curve_points|PricingExecution|Derived|derived" \
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:43:        services/derived_payoff_persistence.py \
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:44:        services/payoff_persistence_port.py \
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:119:        "payoff_curve_points",
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:187:    (derived_db, ["payoff_curve_points", "structure_decisions"]),
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:294:    (derived_db, ["payoff_curve_points", "structure_decisions"]),
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:305:    (derived_db, "payoff_curve_points"),
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-diagnostico-payoff-manual-canonico.txt"
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:26:  echo "== Busca por referencias a payoff_curve_points =="
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:27:  grep -RIn "payoff_curve_points" repositories services domain UI ATT scripts 2>/dev/null || true
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:34:  echo "== Busca por referencias a Payoff/payoff =="
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:35:  grep -RIn "payoff\|Payoff" repositories services domain UI ATT 2>/dev/null || true
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:110:        "payoff_curve_points",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:176:            "payoff",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:177:            "payoff_curve",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:178:            "payoff_points",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:201:  echo "== Inspecao pos-execucao de payoff e decisoes =="
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:216:        "payoff_curve_points",
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:275:## Fase 3F - Diagnostico payoff estrutura manual canonica
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:284:Identificar por que a estrutura manual canonica structure_id=2 ainda nao gera pontos em payoff_curve_points.
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:287:docs/checkpoints/evidencias/fase-3f-diagnostico-payoff-manual-canonico.txt
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt"
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:26:  echo "== Trechos essenciais domain/payoff.py =="
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:27:  grep -n "def validate_canonical_input\|def _compute_leg_payoff_at_expiration\|def compute_payoff_curve_from_canonical_legs\|def compute_payoff_from_canonical_input" domain/payoff.py || true
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:29:  sed -n '1,230p' domain/payoff.py
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:33:  grep -n "def insert_payoff_points\|def save_payoff_curve\|def save_payoff_from_canonical_payload\|def save_decision_from_canonical_payload" services/derived_service.py || true
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:40:  echo "== Execucao isolada corrigida: pricing_payload -> canonical_input -> compute_payoff =="
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:64:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:65:    from domain.payoff import compute_payoff_from_canonical_input, validate_canonical_input
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:94:    payoff = compute_payoff_from_canonical_input(canonical_input)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:97:    print("PAYOFF_TYPE:", type(payoff).__name__)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:98:    if isinstance(payoff, dict):
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:99:        print("PAYOFF_KEYS:", sorted(payoff.keys()))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:100:        print("PAYOFF_POINTS_LEN:", len(payoff.get("points") or []))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:102:        print(json.dumps(payoff.get("meta"), ensure_ascii=False, default=str, indent=2))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:104:        print(json.dumps((payoff.get("points") or [])[:10], ensure_ascii=False, default=str, indent=2))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:107:            "structure_id": payoff.get("structure_id"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:108:            "structure_name": payoff.get("structure_name"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:109:            "underlying_asset": payoff.get("underlying_asset"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:110:            "spot_ref": payoff.get("spot_ref"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:111:            "pl_min": payoff.get("pl_min"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:112:            "pl_max": payoff.get("pl_max"),
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:115:        print(repr(payoff))
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:146:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:152:    before_payoff = conn.execute(
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:153:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:162:    print("Antes payoff_curve_points structure_id=2:", before_payoff)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:185:    after_payoff = conn.execute(
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:186:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:194:    print("Depois payoff_curve_points structure_id=2:", after_payoff)
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:203:          from payoff_curve_points
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:243:## Fase 3F Fix1 - Diagnostico compute payoff V2
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:256:docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:259:Diagnostico V2 executado. Proxima etapa: patch corretivo no contrato de payoff, se necessario.
scripts/fase-3f-fix1-diagnostico-compute-payoff-v2.sh:263:echo "Diagnostico compute payoff V2 gerado em:"
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff.txt"
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:26:  echo "== Arquivo domain/payoff.py =="
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:27:  sed -n '1,420p' domain/payoff.py
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:34:  echo "== Execucao isolada: pricing_payload -> canonical_input -> compute_payoff =="
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:42:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:43:    from domain.payoff import compute_payoff_from_canonical_input
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:68:    payoff = compute_payoff_from_canonical_input(canonical_input)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:71:    print("PAYOFF_TYPE:", type(payoff).__name__)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:72:    if isinstance(payoff, dict):
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:73:        print("PAYOFF_KEYS:", sorted(payoff.keys()))
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:74:        for key, value in payoff.items():
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:84:        print(repr(payoff))
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:99:    from services.derived_payoff_persistence import DerivedPayoffPersistence
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:107:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:112:    print("Antes payoff_curve_points structure_id=2:", before)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:133:        "select count(*) from payoff_curve_points where structure_id=?",
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:142:    print("Depois payoff_curve_points structure_id=2:", after)
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:158:## Fase 3F Fix1 - Diagnostico compute payoff
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:168:compute_payoff_from_canonical_input() e DerivedPayoffPersistence.persist() para identificar
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:169:onde a geração/persistência do payoff falha.
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:172:docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff.txt
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:175:Diagnostico executado. Proxima etapa: patch corretivo no contrato de payoff.
scripts/fase-3f-fix1-diagnostico-compute-payoff.sh:179:echo "Diagnostico compute payoff gerado em:"
scripts/fase-3f-fix1-evidencia-final.sh:25:  echo "== Diff services/derived_payoff_persistence.py =="
scripts/fase-3f-fix1-evidencia-final.sh:26:  git diff -- services/derived_payoff_persistence.py
scripts/fase-3f-fix1-evidencia-final.sh:29:  echo "== Validação compute payoff V2 - resumo =="
scripts/fase-3f-fix1-evidencia-final.sh:30:  grep -n "VALIDATION_ERRORS\|PAYOFF_POINTS_LEN\|PAYOFF_META\|Antes payoff\|Depois payoff\|Traceback\|TypeError\|ValueError\|warning\|erro" -A20 -B10 \
scripts/fase-3f-fix1-evidencia-final.sh:31:    docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt || true
scripts/fase-3f-fix1-evidencia-final.sh:39:for table in ["payoff_curve_points", "structure_decisions"]:
scripts/fase-3f-fix1-evidencia-final.sh:49:      from payoff_curve_points
scripts/fase-3f-fix1-evidencia-final.sh:58:print("Amostra payoff:")
scripts/fase-3f-fix1-evidencia-final.sh:83:Normalização das legs em services/derived_payoff_persistence.py para preencher
scripts/fase-3f-fix1-evidencia-final.sh:84:position_side a partir de side antes de chamar domain.compute_payoff_from_canonical_input().
scripts/fase-3f-fix1-evidencia-final.sh:87:O payoff canônico validava structure.legs[n].position_side como obrigatório, enquanto
scripts/fase-3f-fix1-evidencia-final.sh:94:Patch aplicado e validado por diagnóstico de geração/persistência de payoff.
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:4:EVID="docs/checkpoints/evidencias/fase-3f-fix1-inspecao-contrato-payoff.txt"
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:26:  echo "== Schema payoff_curve_points em dados/derived.db =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:41:for table in ["payoff_curve_points", "structure_decisions"]:
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:81:  echo "== Busca arquivos de persistencia derivada/payoff =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:82:  find repositories services domain UI ATT -type f 2>/dev/null | grep -Ei "payoff|derived|decision|pricing" | sort
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:85:  echo "== Referencias diretas a payoff_curve_points =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:86:  grep -RIn "payoff_curve_points" repositories services domain UI ATT 2>/dev/null || true
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:97:  echo "== Testes atuais relacionados a pricing/payoff/canonical =="
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:98:  find ATT/tests -type f 2>/dev/null | grep -Ei "pricing|payoff|canonical|decision" | sort
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:109:## Fase 3F Fix1 - Inspecao contrato payoff
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:118:Inspecionar schema de payoff_curve_points, codigo da CanonicalPricingFacade e referencias existentes antes de implementar geracao de payoff canonico.
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:121:docs/checkpoints/evidencias/fase-3f-fix1-inspecao-contrato-payoff.txt
scripts/fase-3f-fix1-inspecao-contrato-payoff.sh:124:Inspecao executada. Proxima etapa: implementar geracao e persistencia de pontos de payoff para estrutura manual canonica.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:3:path = Path("services/derived_payoff_persistence.py")
scripts/fase-3f-fix1-patch-normaliza-position-side.py:13:        Normaliza aliases de direção para o contrato canônico de payoff.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:15:        domain/payoff.py exige leg["position_side"].
scripts/fase-3f-fix1-patch-normaliza-position-side.py:48:    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
scripts/fase-3f-fix1-patch-normaliza-position-side.py:51:        esperado por domain.compute_payoff_from_canonical_input().
scripts/fase-3f-fix1-patch-normaliza-position-side.py:101:    def _normalize_canonical_input_for_payoff(
scripts/fase-3f-fix1-patch-normaliza-position-side.py:105:        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:115:            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
scripts/fase-3f-fix1-patch-normaliza-position-side.py:119:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
scripts/fase-3f-fix1-patch-normaliza-position-side.py:144:        # estrito de domain/payoff.py.
scripts/fase-3f-fix1-patch-normaliza-position-side.py:146:            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
scripts/fase-3f-fix1-patch-normaliza-position-side.py:181:        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")
scripts/fase-3f-fix1-patch-normaliza-position-side.py:189:                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:29:  grep -n "def main\|print\|run\|pipeline\|payoff\|decision\|summary\|count\|return" scripts/run_derived_pipeline.py || true
scripts/fase-4-diagnostico-atualizar-dados-limpo.sh:33:  grep -n "def run_full_pipeline\|def run_full_pipeline_from_db\|payoff\|decision\|return" services/calculation_orchestrator.py || true
scripts/fase-5-diagnostico-rtd.sh:62:        for target in ["rtd_option_quotes", "payoff_curve_points", "structure_decisions"]:
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:157:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:226:            "payoff_points": _first_count(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:228:                "payoff_curve_points",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:229:                "payoff_points",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:230:                "derived_payoff_points",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:232:            "payoff_summaries": _first_count(
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:234:                "payoff_curve_summary",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:235:                "payoff_summaries",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:236:                "derived_payoff_summary",
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:331:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:332:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
scripts/mapear_automacao_opcoes_rtd.py:65:    "calculo": ["calculation", "pricing", "payoff", "metric", "metrics", "grega", "gregas"],
scripts/patch_derived_payoff_timestamp_consistency.sh:8:path = Path("services/derived_payoff_persistence.py")
scripts/patch_derived_payoff_timestamp_consistency.sh:11:    raise SystemExit("[ERROR] Arquivo não encontrado: services/derived_payoff_persistence.py")
scripts/patch_derived_payoff_timestamp_consistency.sh:38:# persist(): criar timestamp único e só gravar decisão se payoff gravou
scripts/patch_derived_payoff_timestamp_consistency.sh:43:        """        self._persist_payoff(pricing_payload, result)
scripts/patch_derived_payoff_timestamp_consistency.sh:46:        """        # Timestamp único para payoff + decisão.
scripts/patch_derived_payoff_timestamp_consistency.sh:50:        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
scripts/patch_derived_payoff_timestamp_consistency.sh:51:        if not payoff_saved:
scripts/patch_derived_payoff_timestamp_consistency.sh:53:                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:61:                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:70:# _persist_payoff signature: retorna bool e recebe snapshot_ts
scripts/patch_derived_payoff_timestamp_consistency.sh:75:        """    def _persist_payoff(
scripts/patch_derived_payoff_timestamp_consistency.sh:81:        """    def _persist_payoff(
scripts/patch_derived_payoff_timestamp_consistency.sh:88:        "_persist_payoff signature",
scripts/patch_derived_payoff_timestamp_consistency.sh:91:# payoff sem pontos deve retornar False
scripts/patch_derived_payoff_timestamp_consistency.sh:93:    """            if not payoff_result.get("points"):
scripts/patch_derived_payoff_timestamp_consistency.sh:95:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:100:    """            if not payoff_result.get("points"):
scripts/patch_derived_payoff_timestamp_consistency.sh:102:                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:110:# salvar payoff com timestamp único
scripts/patch_derived_payoff_timestamp_consistency.sh:112:    "            save_payoff_from_canonical_payload(payoff_result)\n",
scripts/patch_derived_payoff_timestamp_consistency.sh:113:    "            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)\n",
scripts/patch_derived_payoff_timestamp_consistency.sh:117:# payoff sucesso retorna True
scripts/patch_derived_payoff_timestamp_consistency.sh:118:if 'derived_payoff_persistence: %d pontos gravados -- structure_id=%s' in text and "return True\n\n        except Exception:" not in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:122:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:123:                len(payoff_result["points"]),
scripts/patch_derived_payoff_timestamp_consistency.sh:130:                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:131:                len(payoff_result["points"]),
scripts/patch_derived_payoff_timestamp_consistency.sh:138:        "_persist_payoff return True",
scripts/patch_derived_payoff_timestamp_consistency.sh:141:# payoff exception retorna False
scripts/patch_derived_payoff_timestamp_consistency.sh:142:if "erro ao gravar payoff" in text and "return False\n\n    # -------------------------------------------------------------- #\n    #  decisão" not in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:146:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:153:                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:160:        "_persist_payoff return False exception",
scripts/patch_derived_payoff_timestamp_consistency.sh:167:    # cuidado: já pode existir no payoff; testar assinatura específica da decisão
scripts/patch_derived_payoff_timestamp_consistency.sh:211:if 'derived_payoff_persistence: decisão gravada -- structure_id=%s' in text and "return True\n\n        except Exception:" in text:
scripts/patch_derived_payoff_timestamp_consistency.sh:212:    # Já existe return True em payoff; precisamos garantir decisão também.
scripts/patch_derived_payoff_timestamp_consistency.sh:216:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:224:                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:238:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:246:                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
scripts/patch_derived_payoff_timestamp_consistency.sh:263:    "save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)",
scripts/patch_derived_payoff_timestamp_consistency.sh:265:    "payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)",
scripts/patch_derived_payoff_timestamp_consistency.sh:280:    print("[OK] Patch aplicado em services/derived_payoff_persistence.py")
scripts/patch_derived_payoff_timestamp_consistency.sh:283:python -m py_compile services/derived_payoff_persistence.py
scripts/purge_derived_snapshots.py:12:    "payoff_curve_points",
scripts/purge_derived_snapshots.py:14:    "payoff_curve_summary",
scripts/repair_derived_db_consistency.py:21:        LEFT JOIN payoff_curve_points p
scripts/repair_derived_db_consistency.py:31:        FROM payoff_curve_points p
scripts/repair_derived_db_consistency.py:122:            FROM payoff_curve_points
scripts/repair_derived_db_consistency.py:223:                LEFT JOIN payoff_curve_points p
scripts/repair_derived_db_consistency.py:255:                FROM payoff_curve_points p
scripts/repair_derived_db_consistency.py:275:                        DELETE FROM payoff_curve_points
scripts/repair_derived_db_consistency.py:279:                            WHERE d.aba = payoff_curve_points.aba
scripts/repair_derived_db_consistency.py:280:                              AND d.timestamp = payoff_curve_points.timestamp
scripts/run_derived_pipeline.py:149:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
scripts/run_derived_pipeline.py:218:            "payoff_points": _first_count(
scripts/run_derived_pipeline.py:220:                "payoff_curve_points",
scripts/run_derived_pipeline.py:221:                "payoff_points",
scripts/run_derived_pipeline.py:222:                "derived_payoff_points",
scripts/run_derived_pipeline.py:224:            "payoff_summaries": _first_count(
scripts/run_derived_pipeline.py:226:                "payoff_curve_summary",
scripts/run_derived_pipeline.py:227:                "payoff_summaries",
scripts/run_derived_pipeline.py:228:                "derived_payoff_summary",
scripts/run_derived_pipeline.py:323:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
scripts/run_derived_pipeline.py:324:    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
scripts/validate_derived_db.py:65:        points_count = safe_count("payoff_curve_points")
scripts/validate_derived_db.py:71:            print("[WARN] Tabela payoff_curve_points nao acessivel (ou nao existe).")

## Busca por cadastro de pernas e símbolos
UI/components/structure_editor_dialog.py:29:    _add_leg_row()  alias publico de _cmd_add_leg (exigido por checks estaticos)
UI/components/structure_editor_dialog.py:146:        ttk.Button(leg_toolbar, text="+ Leg",    command=self._cmd_add_leg).pack(side="left", padx=2)
UI/components/structure_editor_dialog.py:155:        leg_cols   = ("order", "side", "type", "strike", "expiry", "qty", "premium", "mult", "symbol")
UI/components/structure_editor_dialog.py:198:        self._lf_symbol  = tk.StringVar()
UI/components/structure_editor_dialog.py:227:            ("Simbolo", self._lf_symbol),
UI/components/structure_editor_dialog.py:282:                leg.get("symbol") or "",
UI/components/structure_editor_dialog.py:311:        self._lf_symbol.set(str(leg.get("symbol") or ""))
UI/components/structure_editor_dialog.py:313:    def _cmd_add_leg(self):
UI/components/structure_editor_dialog.py:324:            "symbol":          None,
UI/components/structure_editor_dialog.py:334:    # _add_leg_row: alias publico exigido pelos checks estaticos do alteracao_69
UI/components/structure_editor_dialog.py:335:    # Delega para _cmd_add_leg mantendo compatibilidade total.
UI/components/structure_editor_dialog.py:337:    def _add_leg_row(self):
UI/components/structure_editor_dialog.py:339:        Alias publico de _cmd_add_leg().
UI/components/structure_editor_dialog.py:341:            hasattr(StructureEditorDialog, '_add_leg_row')
UI/components/structure_editor_dialog.py:343:        self._cmd_add_leg()
UI/components/structure_editor_dialog.py:385:            "symbol":          self._lf_symbol.get() or None,
UI/main_window.py:734:                    f"         Qtde   : {leg.get('quantity')}  Símbolo: {leg.get('symbol') or '--'}",
services/calculation_orchestrator.py:75:                symbol=row.get("symbol"),
services/calculation_orchestrator.py:124:            "symbol":          getattr(leg, "symbol",      None),
services/calculation_orchestrator.py:270:                    symbol=leg.get("symbol"),
services/calculation_orchestrator.py:313:                "symbol":          getattr(leg, "symbol",     None),
services/calculation_orchestrator.py:475:                    "symbol":          leg.get("symbol"),
services/canonical_pricing_facade.py:155:    symbol_candidates = {
services/canonical_pricing_facade.py:159:        "symbol",
services/canonical_pricing_facade.py:195:                symbol_cols = [
services/canonical_pricing_facade.py:197:                    for name in symbol_candidates
services/canonical_pricing_facade.py:207:                if not symbol_cols or not price_cols:
services/canonical_pricing_facade.py:210:                for symbol_col in symbol_cols:
services/canonical_pricing_facade.py:215:                            f"WHERE UPPER(CAST({_quote_ident(symbol_col)} AS TEXT)) = UPPER(?) "
services/canonical_pricing_facade.py:250:        raw_asset = _pick(d, "symbol", "asset", "ativo")
services/canonical_pricing_facade.py:273:            "symbol":          raw_asset,
services/derived_payoff_persistence.py:268:        if "symbol" not in data:
services/derived_payoff_persistence.py:269:            data["symbol"] = data.get("asset") or data.get("ativo")
services/legacy_robo_legs_fallback.py:229:            "symbol": self._clean_upper_text(
services/legacy_robo_legs_fallback.py:230:                data.get("ativo") or data.get("symbol") or data.get("ticker")
services/legacy_structure_legs_importer.py:1:# services/legacy_structure_legs_importer.py
services/legacy_structure_legs_importer.py:6:Importa pernas legadas ja normalizadas pelo LegacyStructureLegsReader
services/legacy_structure_legs_importer.py:7:para a tabela canonica structure_legs.
services/legacy_structure_legs_importer.py:41:    Orquestra a importacao das legs legadas para structure_legs.
services/legacy_structure_legs_importer.py:48:            Repositório canônico de structures/structure_legs.
services/legacy_structure_legs_reader.py:11:    Leitor canônico de pernas legadas para estruturas.
services/legacy_structure_legs_reader.py:16:      - ler pernas legadas manual/rtd;
services/legacy_structure_legs_reader.py:17:      - converter para payload compatível com structure_legs;
services/legacy_structure_legs_reader.py:18:      - NÃO gravar em structure_legs.
services/pricing_payload_adapter.py:43:                "symbol": _clean_upper_text(leg.get("symbol")),
services/robo_leg_mapper.py:70:        "symbol": _safe_upper_text(ativo),
services/structure_events_service.py:117:        symbol: str | None = None,
services/structure_events_service.py:139:            "symbol": self._normalize_optional_text(symbol),
services/structure_events_service.py:170:        symbol: str | None = None,
services/structure_events_service.py:181:            symbol=symbol,
services/structure_events_service.py:302:        - full_close zera a perna alvo ou a estrutura inteira.
services/structure_events_service.py:304:        - assignment, exercise e expiration zeram a perna alvo ou estrutura.
services/structure_events_service.py:436:        symbol = self._normalize_optional_text(event.get("symbol"))
services/structure_events_service.py:438:        if leg_id is None and symbol is None:
services/structure_events_service.py:453:            if symbol is not None:
services/structure_events_service.py:454:                leg_symbol = self._normalize_optional_text(leg.get("symbol"))
services/structure_events_service.py:455:                if leg_symbol == symbol:
services/structure_input_mapper.py:55:        "symbol": _clean_upper_text(leg.get("symbol")),
services/structure_leg_rtd_enrichment_service.py:4:- receber entrada minima baseada em simbolo/codigo da opcao;
services/structure_leg_rtd_enrichment_service.py:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:25:        """Retorna uma leg canonica enriquecida a partir do simbolo da opcao.
services/structure_leg_rtd_enrichment_service.py:28:        - symbol ou codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:45:        symbol = self._normalize_symbol(
services/structure_leg_rtd_enrichment_service.py:46:            leg_data.get("symbol") or leg_data.get("codigo_opcao")
services/structure_leg_rtd_enrichment_service.py:48:        if not symbol:
services/structure_leg_rtd_enrichment_service.py:49:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py:51:        quote = self._repo.get_by_codigo(symbol)
services/structure_leg_rtd_enrichment_service.py:53:            raise ValueError(f"option quote not found for symbol: {symbol}")
services/structure_leg_rtd_enrichment_service.py:67:            "symbol": symbol,
services/structure_leg_rtd_enrichment_service.py:87:    def _normalize_symbol(value: Any) -> str:
db/schema.py:80:    symbol         TEXT,
db/schema.py:87:    FOREIGN KEY (leg_id) REFERENCES structure_legs(id) ON DELETE SET NULL
db/schema_excel.py:22:  num_pernas INTEGER,
db/schema_excel.py:37:-- Snapshot por perna (ANALISE_ROBO_LEGS)
db/schema_excel.py:67:-- Histórico por perna (HIST_ROBO) (parece similar ao legs, mas sem alguns campos)
repositories/market_snapshot_repository.py:92:        num_pernas,
repositories/market_snapshot_repository.py:214:    ativo = _first_text(quote_row["codigo_opcao"], base_leg.ativo)
repositories/market_snapshot_repository.py:284:        dessa composição, se houver cotação em rtd_option_quotes.codigo_opcao,
repositories/market_snapshot_repository.py:302:                codigo_opcao,
repositories/market_snapshot_repository.py:322:            WHERE UPPER(codigo_opcao) IN ({placeholders})
repositories/market_snapshot_repository.py:336:            codigo = str(row["codigo_opcao"]).strip().upper()
repositories/market_snapshot_repository.py:393:            num_pernas=int(_f("num_pernas")) if _f("num_pernas") is not None else None,
repositories/rtd_option_quotes_repository.py:26:    def get_by_codigo(self, codigo_opcao: str) -> dict[str, Any] | None:
repositories/rtd_option_quotes_repository.py:29:                codigo_opcao,
repositories/rtd_option_quotes_repository.py:49:            WHERE codigo_opcao = ?
repositories/rtd_option_quotes_repository.py:54:            row = conn.execute(sql, (codigo_opcao,)).fetchone()
repositories/rtd_option_quotes_repository.py:61:                codigo_opcao,
repositories/rtd_option_quotes_repository.py:82:            ORDER BY vencimento, call_put, strike, codigo_opcao
repositories/rtd_option_quotes_repository.py:93:                codigo_opcao,
repositories/rtd_option_quotes_repository.py:113:            ORDER BY ativo_base, vencimento, call_put, strike, codigo_opcao
repositories/structures_repository.py:3:Repositório canônico de estruturas e suas pernas (legs).
repositories/structures_repository.py:98:    symbol          = leg.get("symbol")
repositories/structures_repository.py:146:    if symbol is not None:
repositories/structures_repository.py:147:        symbol = str(symbol).strip() or None
repositories/structures_repository.py:155:        "symbol":          symbol,
repositories/structures_repository.py:199:                id, structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:202:            FROM structure_legs
repositories/structures_repository.py:354:        de alguma perna falhe.
repositories/structures_repository.py:401:                    INSERT INTO structure_legs (
repositories/structures_repository.py:402:                        structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:411:                        leg["symbol"],
repositories/structures_repository.py:586:    def add_leg(self, structure_id: int, leg_data: dict[str, Any]) -> int:
repositories/structures_repository.py:596:                INSERT INTO structure_legs (
repositories/structures_repository.py:597:                    structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:604:                    leg["symbol"], leg["strike"], leg["expiration_date"],
repositories/structures_repository.py:643:                "DELETE FROM structure_legs WHERE structure_id=?",
repositories/structures_repository.py:650:                    INSERT INTO structure_legs (
repositories/structures_repository.py:651:                        structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:658:                        leg["symbol"], leg["strike"], leg["expiration_date"],
repositories/structures_repository.py:692:                "SELECT COUNT(*) AS n FROM structure_legs WHERE structure_id=?",
repositories/structure_events_repository.py:163:        "symbol": _normalize_optional_text(data.get("symbol")),
repositories/structure_events_repository.py:208:                symbol         TEXT,
repositories/structure_events_repository.py:215:                FOREIGN KEY (leg_id) REFERENCES structure_legs(id) ON DELETE SET NULL
repositories/structure_events_repository.py:290:            FROM structure_legs
repositories/structure_events_repository.py:330:                    symbol,
repositories/structure_events_repository.py:346:                    event["symbol"],
repositories/system_snapshots_repository.py:96:        """Cria um snapshot e suas pernas associadas.
repositories/system_snapshots_repository.py:178:                symbol,
repositories/system_snapshots_repository.py:197:                leg.get("symbol"),
repositories/system_snapshots_repository.py:210:        """Retorna um snapshot com suas pernas, ou None se não existir."""
domain/calculation_request.py:71:    Representa uma perna (leg) da estrutura, já normalizada.
domain/calculation_request.py:78:    symbol        : código da opção (ex.: BOVAE195) -- opcional
domain/calculation_request.py:89:    symbol:      Optional[str]   = None
domain/calculation_request.py:141:    legs              : pernas já normalizadas
domain/calculation_request.py:187:    option_quotes:       Optional[dict]  = None   # bid/ask por símbolo
domain/contracts.py:9:    symbol: str | None
domain/contracts.py:58:                symbol=leg.get("symbol"),
domain/contracts.py:106:                        "symbol": leg.symbol,
domain/market_snapshot.py:27:    """Representa uma perna (leg) de uma estrutura de opções."""
domain/market_snapshot.py:61:      aba, spot, num_pernas, dte_min, pl_realista_total,
domain/market_snapshot.py:76:    num_pernas         : Optional[int]   = None
domain/structure_metrics.py:330:        "num_pernas": len(computed_legs),
scripts/apply_fase9_atomic_create.py:30:Em caso de falha na gravação das legs, poderia sobrar estrutura persistida sem pernas.
scripts/apply_fase9_atomic_create.py:69:        de alguma perna falhe.
scripts/apply_fase9_atomic_create.py:116:                    INSERT INTO structure_legs (
scripts/apply_fase9_atomic_create.py:117:                        structure_id, position_side, option_type, symbol,
scripts/apply_fase9_atomic_create.py:126:                        leg["symbol"],
scripts/apply_fase9_update_tests_atomic_create.py:80:            "premium": None, "multiplier": 1, "symbol": None,
scripts/audit_rtd_option_quotes.py:26:    "codigo_opcao",
scripts/audit_rtd_option_quotes.py:125:        if "codigo_opcao" in column_set:
scripts/audit_rtd_option_quotes.py:132:                    WHERE codigo_opcao IS NULL
scripts/audit_rtd_option_quotes.py:133:                       OR TRIM(codigo_opcao) = ''
scripts/audit_rtd_option_quotes.py:143:                    SELECT COUNT(DISTINCT codigo_opcao)
scripts/audit_rtd_option_quotes.py:145:                    WHERE codigo_opcao IS NOT NULL
scripts/audit_rtd_option_quotes.py:146:                      AND TRIM(codigo_opcao) <> ''
scripts/audit_rtd_option_quotes.py:158:                        SELECT codigo_opcao
scripts/audit_rtd_option_quotes.py:160:                        WHERE codigo_opcao IS NOT NULL
scripts/audit_rtd_option_quotes.py:161:                          AND TRIM(codigo_opcao) <> ''
scripts/audit_rtd_option_quotes.py:162:                        GROUP BY codigo_opcao
scripts/audit_rtd_option_quotes.py:176:                    f"rows with missing codigo_opcao: {missing_codigo_count}"
scripts/audit_rtd_option_quotes.py:181:                    f"duplicated codigo_opcao groups: {duplicate_codigo_count}"
scripts/build_rtd_symbols.py:29:def collect_from_structure_legs(cur, include_inactive=False):
scripts/build_rtd_symbols.py:30:    if not table_exists(cur, "structure_legs"):
scripts/build_rtd_symbols.py:35:            SELECT DISTINCT TRIM(symbol)
scripts/build_rtd_symbols.py:36:            FROM structure_legs
scripts/build_rtd_symbols.py:37:            WHERE symbol IS NOT NULL
scripts/build_rtd_symbols.py:38:              AND TRIM(symbol) <> ''
scripts/build_rtd_symbols.py:42:            SELECT DISTINCT TRIM(l.symbol)
scripts/build_rtd_symbols.py:43:            FROM structure_legs l
scripts/build_rtd_symbols.py:46:            WHERE l.symbol IS NOT NULL
scripts/build_rtd_symbols.py:47:              AND TRIM(l.symbol) <> ''
scripts/build_rtd_symbols.py:72:        SELECT DISTINCT TRIM(symbol)
scripts/build_rtd_symbols.py:74:        WHERE symbol IS NOT NULL
scripts/build_rtd_symbols.py:75:          AND TRIM(symbol) <> ''
scripts/build_rtd_symbols.py:86:        SELECT DISTINCT TRIM(codigo_opcao)
scripts/build_rtd_symbols.py:88:        WHERE codigo_opcao IS NOT NULL
scripts/build_rtd_symbols.py:89:          AND TRIM(codigo_opcao) <> ''
scripts/build_rtd_symbols.py:95:def normalize_symbols(values):
scripts/build_rtd_symbols.py:96:    symbols = set()
scripts/build_rtd_symbols.py:107:        symbols.add(text)
scripts/build_rtd_symbols.py:109:    return sorted(symbols)
scripts/build_rtd_symbols.py:112:def load_symbols(db_path, include_inactive=False, include_snapshots=True, include_existing_quotes=True):
scripts/build_rtd_symbols.py:119:        leg_symbols = collect_from_structure_legs(cur, include_inactive=include_inactive)
scripts/build_rtd_symbols.py:120:        sources.append(("structure_legs", leg_symbols))
scripts/build_rtd_symbols.py:122:        snapshot_symbols = []
scripts/build_rtd_symbols.py:124:            snapshot_symbols = collect_from_structure_leg_snapshots(cur)
scripts/build_rtd_symbols.py:125:            sources.append(("structure_leg_snapshots", snapshot_symbols))
scripts/build_rtd_symbols.py:127:        quote_symbols = []
scripts/build_rtd_symbols.py:129:            quote_symbols = collect_from_rtd_option_quotes(cur)
scripts/build_rtd_symbols.py:130:            sources.append(("rtd_option_quotes", quote_symbols))
scripts/build_rtd_symbols.py:132:        all_symbols = []
scripts/build_rtd_symbols.py:134:            all_symbols.extend(values)
scripts/build_rtd_symbols.py:136:        return normalize_symbols(all_symbols), sources
scripts/build_rtd_symbols.py:152:    symbols, sources = load_symbols(
scripts/build_rtd_symbols.py:161:        print(f"- {name}: {len(normalize_symbols(values))}")
scripts/build_rtd_symbols.py:165:    if not symbols and not args.allow_empty:
scripts/build_rtd_symbols.py:167:        print("Nenhum símbolo encontrado.")
scripts/build_rtd_symbols.py:173:    out.write_text("\n".join(symbols) + ("\n" if symbols else ""), encoding="utf-8")
scripts/build_rtd_symbols.py:176:    print(f"Símbolos exportados: {len(symbols)}")
scripts/build_rtd_symbols.py:179:    for sym in symbols[:50]:
scripts/build_rtd_symbols.py:182:    if len(symbols) > 50:
scripts/build_rtd_symbols.py:183:        print(f"... mais {len(symbols) - 50}")
scripts/check_rota_desenvolvimento.py:368:                    LEFT JOIN structure_legs l ON l.structure_id = s.id
scripts/check_rota_desenvolvimento.py:377:                    print(f"  - structure_id={row[0]} | alias={row[1]} | structure_legs={row[2]}")
scripts/check_rota_desenvolvimento.py:381:            print(f"  Erro ao consultar structure_legs: {exc}")
scripts/check_rota_desenvolvimento.py:420:        "- Se structure_legs já estiver populada para 44-48, a pendência central da Fase 8 pode ter sido tratada.\n"
scripts/create_rtd_option_quotes_sheet.py:10:    "codigo_opcao",
scripts/fase-2b-quantity-tests-auto.sh:68:            "symbol": "TESTC100",
scripts/fase-3a-diagnostico-cadastro-payoff-decisoes.sh:79:    "structure_legs",
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:23:    echo "2) Localizacao de definicoes CREATE TABLE structures e structure_legs"
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:25:    grep -RInE "CREATE TABLE.*structures|CREATE TABLE.*structure_legs|CREATE TABLE IF NOT EXISTS.*structures|CREATE TABLE IF NOT EXISTS.*structure_legs" . \
scripts/fase-3b-diagnostico-schema-canonico-estruturas.sh:35:    grep -RInE "bootstrap_structures_schema|ensure.*structure|create.*structure|structure_legs" . \
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:60:        "structure_legs",
scripts/fase-3c-diagnostico-appdb-ui-pricing-flow.sh:99:            LEFT JOIN structure_legs l ON l.structure_id = s.id
scripts/fase-3d-diagnostico-facade-persistencia-derived.sh:115:        "structure_legs",
scripts/fase-3e-diagnostico-alias-null-facade-manual.sh:41:    LEFT JOIN structure_legs l ON l.structure_id = s.id
scripts/fase-3e-diagnostico-alias-null-facade-manual.sh:69:    JOIN structure_legs l ON l.structure_id = s.id
scripts/fase-3e-diagnostico-alias-null-facade-manual.sh:110:        JOIN structure_legs l ON l.structure_id = s.id
scripts/fase-3f-diagnostico-payoff-manual-canonico.sh:106:        "structure_legs",
scripts/fase-3f-fix1-patch-normaliza-position-side.py:95:        if "symbol" not in data:
scripts/fase-3f-fix1-patch-normaliza-position-side.py:96:            data["symbol"] = data.get("asset") or data.get("ativo")
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:52:    scripts/build_rtd_symbols.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:73:    scripts/build_rtd_symbols.py \
scripts/fase-5b-diagnostico-rtd-cadeia-real.sh:143:            SELECT codigo_opcao, ativo_base, call_put, strike, ultimo_preco, bid, ask, source, updated_at, created_at
scripts/fase-5c-restaurar-rtd-historico.sh:10:  "scripts/build_rtd_symbols.py"
scripts/fase-5c-restaurar-rtd-historico.sh:72:    scripts/build_rtd_symbols.py \
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:33:  echo "== Arquivo de símbolos atual =="
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:34:  if [ -f dados/rtd_symbols.txt ]; then
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:35:    ls -l dados/rtd_symbols.txt
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:37:    cat dados/rtd_symbols.txt
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:39:    echo "dados/rtd_symbols.txt ausente"
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:119:                COUNT(DISTINCT codigo_opcao) AS distintos,
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:130:                codigo_opcao,
scripts/fase-5d-validar-rtd-restaurado-operacional.sh:141:            ORDER BY codigo_opcao
scripts/fase-5e-integrar-rtd-derived-pipeline.sh:416:        "codigo_opcao;ativo_base\nPRIOG800;PRIO3\n",
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:74:                COUNT(DISTINCT codigo_opcao) AS distintos,
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:82:            SELECT codigo_opcao, ativo_base, call_put, strike, vencimento,
scripts/fase-5e-validar-integracao-rtd-derived-pipeline.sh:85:            ORDER BY codigo_opcao
scripts/import_legacy_structure_legs.py:19:from services.legacy_structure_legs_importer import (  # noqa: E402
scripts/import_legacy_structure_legs.py:22:from services.legacy_structure_legs_reader import LegacyStructureLegsReader  # noqa: E402
scripts/import_legacy_structure_legs.py:28:            "Importa pernas legadas manual/rtd para structure_legs "
scripts/import_legacy_structure_legs.py:55:        help="Apenas lê e exibe as pernas canônicas, sem gravar em structure_legs.",
scripts/import_lista_rtd_excel_to_option_quotes.py:31:    "codigo_opcao",
scripts/import_lista_rtd_excel_to_option_quotes.py:54:    "codigo_opcao": "codigo_opcao",
scripts/import_lista_rtd_excel_to_option_quotes.py:55:    "codigo": "codigo_opcao",
scripts/import_lista_rtd_excel_to_option_quotes.py:56:    "ticker": "codigo_opcao",
scripts/import_lista_rtd_excel_to_option_quotes.py:57:    "symbol": "codigo_opcao",
scripts/import_lista_rtd_excel_to_option_quotes.py:58:    "ativo": "codigo_opcao",
scripts/import_lista_rtd_excel_to_option_quotes.py:62:    "underlying_symbol": "ativo_base",
scripts/import_lista_rtd_excel_to_option_quotes.py:67:    "tipo_opcao": "option_type",
scripts/import_lista_rtd_excel_to_option_quotes.py:379:        codigo = clean_text(raw_row.get("codigo_opcao"))
scripts/import_lista_rtd_excel_to_option_quotes.py:384:        if codigo.lower() in {"codigo_opcao", "codigo", "ticker", "symbol"}:
scripts/import_lista_rtd_excel_to_option_quotes.py:391:            "codigo_opcao": codigo.upper(),
scripts/import_lista_rtd_excel_to_option_quotes.py:458:                "SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? LIMIT 1",
scripts/import_lista_rtd_excel_to_option_quotes.py:459:                (record["codigo_opcao"],),
scripts/import_lista_rtd_excel_to_option_quotes.py:470:        codigo = record["codigo_opcao"]
scripts/import_lista_rtd_excel_to_option_quotes.py:480:            "codigo_opcao": codigo,
scripts/import_lista_rtd_excel_to_option_quotes.py:520:             WHERE codigo_opcao = :codigo_opcao
scripts/import_lista_rtd_excel_to_option_quotes.py:535:                codigo_opcao,
scripts/import_lista_rtd_excel_to_option_quotes.py:556:                :codigo_opcao,
scripts/import_rtd_links_to_option_quotes.py:7:codigo_opcao,ativo_base,campo,valor,atualizado_em
scripts/import_rtd_links_to_option_quotes.py:32:    "codigo_opcao",
scripts/import_rtd_links_to_option_quotes.py:61:    "codigo_opcao",
scripts/import_rtd_links_to_option_quotes.py:195:def empty_record(codigo_opcao: str) -> dict[str, Any]:
scripts/import_rtd_links_to_option_quotes.py:197:        "codigo_opcao": codigo_opcao,
scripts/import_rtd_links_to_option_quotes.py:243:            codigo = str(cleaned.get("codigo_opcao") or "").strip().upper()
scripts/import_rtd_links_to_option_quotes.py:306:        SELECT codigo_opcao
scripts/import_rtd_links_to_option_quotes.py:308:        WHERE codigo_opcao IN ({placeholders})
scripts/import_rtd_links_to_option_quotes.py:345:        ON CONFLICT(codigo_opcao) DO UPDATE SET
scripts/import_rtd_links_to_option_quotes.py:368:        codes = [record["codigo_opcao"] for record in records]
scripts/import_rtd_option_quotes_wide_csv.py:33:    "codigo_opcao",
scripts/import_rtd_option_quotes_wide_csv.py:175:            codigo = clean_text(raw.get("codigo_opcao"))
scripts/import_rtd_option_quotes_wide_csv.py:181:                "codigo_opcao": codigo.upper(),
scripts/import_rtd_option_quotes_wide_csv.py:207:        CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo_opcao
scripts/import_rtd_option_quotes_wide_csv.py:208:        ON rtd_option_quotes(codigo_opcao)
scripts/import_rtd_option_quotes_wide_csv.py:234:            codigo = rec["codigo_opcao"]
scripts/import_rtd_option_quotes_wide_csv.py:237:                "SELECT id, created_at FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
scripts/import_rtd_option_quotes_wide_csv.py:300:                        codigo_opcao,
scripts/import_rtd_option_quotes_wide_csv.py:323:                        payload["codigo_opcao"],
scripts/mapear_automacao_opcoes_rtd.py:61:    "opcoes": ["opcao", "opção", "opcoes", "opções", "option", "strike", "vencimento"],
scripts/refresh_rtd_option_quotes_excel.ps1:3:    [string]$SymbolsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\rtd_symbols.txt"),
scripts/refresh_rtd_option_quotes_excel.ps1:33:    throw "Arquivo de símbolos não encontrado: $SymbolsPath"
scripts/refresh_rtd_option_quotes_excel.ps1:36:$symbols = Get-Content $SymbolsPath |
scripts/refresh_rtd_option_quotes_excel.ps1:41:if ($symbols.Count -eq 0) {
scripts/refresh_rtd_option_quotes_excel.ps1:42:    throw "Nenhum símbolo encontrado em: $SymbolsPath"
scripts/refresh_rtd_option_quotes_excel.ps1:45:Write-Host "Símbolos carregados:" $symbols.Count
scripts/refresh_rtd_option_quotes_excel.ps1:79:        "codigo_opcao",
scripts/refresh_rtd_option_quotes_excel.ps1:119:    foreach ($sym in $symbols) {
scripts/refresh_rtd_option_quotes_excel.ps1:132:    $lastRow = $symbols.Count + 1
scripts/refresh_rtd_option_quotes_excel.ps1:137:    Write-Host "Aba RTD_OPTION_QUOTES preenchida. Linhas:" $symbols.Count
scripts/run_rtd_refresh_full.py:59:def count_symbols_file(path):
scripts/run_rtd_refresh_full.py:65:    symbols = [
scripts/run_rtd_refresh_full.py:71:    return len(symbols), symbols
scripts/run_rtd_refresh_full.py:76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
scripts/run_rtd_refresh_full.py:80:    parser.add_argument("--symbols", default="dados/rtd_symbols.txt")
scripts/run_rtd_refresh_full.py:86:    parser.add_argument("--strict", action="store_true", help="Usa somente structure_legs como fonte de símbolos.")
scripts/run_rtd_refresh_full.py:88:    parser.add_argument("--allow-empty", action="store_true", help="Permite lista vazia de símbolos.")
scripts/run_rtd_refresh_full.py:95:    symbols_path = Path(args.symbols)
scripts/run_rtd_refresh_full.py:99:    build_script = Path("scripts/build_rtd_symbols.py")
scripts/run_rtd_refresh_full.py:106:    print(f"Symbols: {symbols_path}")
scripts/run_rtd_refresh_full.py:137:        str(symbols_path),
scripts/run_rtd_refresh_full.py:162:                str(symbols_path.resolve()),
scripts/run_rtd_refresh_full.py:191:        print("Pipeline interrompido na geração de símbolos.")
scripts/run_rtd_refresh_full.py:194:        print("- Em modo --strict, isso é esperado se não houver registros em structure_legs.")
scripts/run_rtd_refresh_full.py:198:    symbol_count, symbols = count_symbols_file(symbols_path)
scripts/run_rtd_refresh_full.py:201:    print(f"Símbolos no arquivo: {symbol_count}")
scripts/run_rtd_refresh_full.py:203:    if symbol_count == 0 and not args.allow_empty:
scripts/run_rtd_refresh_full.py:205:        print("Pipeline interrompido: nenhum símbolo para consultar no RTD.")
scripts/run_rtd_refresh_full.py:208:    if symbols:
scripts/run_rtd_refresh_full.py:209:        print("Primeiros símbolos:")
scripts/run_rtd_refresh_full.py:210:        for symbol in symbols[:20]:
scripts/run_rtd_refresh_full.py:211:            print(f"- {symbol}")
scripts/run_rtd_refresh_full.py:213:        if len(symbols) > 20:
scripts/run_rtd_refresh_full.py:214:            print(f"... mais {len(symbols) - 20}")
scripts/run_rtd_refresh_full.py:227:            str(symbols_path.resolve()),
scripts/seed_current_rtd_option_quotes.py:32:        "codigo_opcao": "SMALF129",
scripts/seed_current_rtd_option_quotes.py:42:        "codigo_opcao": "SMALF103",
scripts/seed_current_rtd_option_quotes.py:52:        "codigo_opcao": "SMALR127",
scripts/seed_current_rtd_option_quotes.py:62:        "codigo_opcao": "SMALR108",
scripts/seed_current_rtd_option_quotes.py:72:        "codigo_opcao": "PRIOG800",
scripts/seed_current_rtd_option_quotes.py:82:        "codigo_opcao": "PRIOH515",
scripts/seed_current_rtd_option_quotes.py:92:        "codigo_opcao": "PRIOT700",
scripts/seed_current_rtd_option_quotes.py:102:        "codigo_opcao": "PRIOS525",
scripts/seed_current_rtd_option_quotes.py:147:                codigo_opcao,
scripts/seed_current_rtd_option_quotes.py:168:                :codigo_opcao,
scripts/seed_current_rtd_option_quotes.py:200:                "codigo_opcao": quote["codigo_opcao"],
