# Auditoria de retorno ao roteiro RTD/Excel

Data: 2026-07-10 10:12:52

## Objetivo

Conferir o estado do projeto após a frente de centralização COM operacional e retomar o roteiro do documento EXCEL_RTD_BTG_ONLINE REVISADO.

## Git status

Comando:

```bash
git status --short
```

Saída: sem ocorrências.

## Últimos commits

Comando:

```bash
git log --oneline -8
```

Saída:

```text
647360d refactor: conclui centralizacao COM operacional RTD Excel
3b9ef80 fix: restaura modelo de status RTD Excel
6869b73 fix: aplica centralizacao COM Excel RTD
0337f8d refactor: centraliza acesso COM Excel RTD
7ead120 chore: padroniza line endings do projeto
a2059bb refactor: centraliza schema RTD option quotes
244bb49 feat: adiciona status RTD Excel no menu ajuda
ec00d4e feat: expose Excel RTD status payload
```

## Busca COM direta

Comando:

```bash
git grep -n -E win32com|DispatchEx|GetActiveObject -- *.py
```

Saída:

```text
ATT/checks/check_api_routes.py:6:    import win32com.client
ATT/checks/check_api_routes.py:8:    win32com = None
ATT/checks/check_api_routes.py:35:        if win32com is None:
ATT/checks/check_api_routes.py:41:        excel = win32com.client.Dispatch("Excel.Application")
rtd_bridge/excel_rtd_option_quotes_bridge.py:4:- Usa DispatchEx para abrir uma instancia isolada do Excel.
rtd_bridge/excel_rtd_option_quotes_bridge.py:145:            import win32com.client
rtd_bridge/excel_rtd_option_quotes_bridge.py:149:            excel = win32com.client.DispatchEx("Excel.Application")
scripts/diagnose_excel_com.py:193:        import win32com.client
scripts/diagnose_excel_com.py:200:                    "message": f"win32com indisponivel: {exc}",
scripts/diagnose_excel_com.py:209:        excel = win32com.client.GetActiveObject("Excel.Application")
scripts/verify_rtd_excel_resume.py:35:    r"LISTA_RTD|RTD_OPTION_QUOTES|RTD-BTG|RTD|win32com|GetActiveObject|Dispatch|"
services/excel_rtd_com_access.py:18:def import_win32com_client() -> Any:
services/excel_rtd_com_access.py:20:        import win32com.client  # type: ignore[import-not-found]
services/excel_rtd_com_access.py:22:        raise ExcelComUnavailableError(f"win32com indisponivel: {exc}") from exc
services/excel_rtd_com_access.py:24:    return win32com.client
services/excel_rtd_com_access.py:28:    win32com_client = import_win32com_client()
services/excel_rtd_com_access.py:31:        return win32com_client.GetActiveObject(prog_id)
services/excel_rtd_workbook_probe.py:75:    Usa o nucleo central de acesso COM, baseado em GetActiveObject, para evitar abrir uma nova instancia
tools/audit_rtd_ui_flow.py:25:    "win32com",
tools/audit_rtd_ui_flow.py:302:        r"win32com",
```

## Busca bridge legado

Comando:

```bash
git grep -n -E RtdOptionQuotesBridge|excel_rtd_option_quotes_bridge|fetch_quotes -- *.py
```

Saída:

```text
ATT/tests/test_rtd_option_quotes_bridge.py:15:from rtd_bridge.excel_rtd_option_quotes_bridge import RtdOptionQuotesBridge
ATT/tests/test_rtd_option_quotes_bridge.py:79:        bridge = RtdOptionQuotesBridge(
ATT/tests/test_rtd_option_quotes_bridge.py:85:        result = bridge.fetch_quotes(args.codes)
rtd_bridge/excel_rtd_option_quotes_bridge.py:113:class RtdOptionQuotesBridge:
rtd_bridge/excel_rtd_option_quotes_bridge.py:132:    def fetch_quotes(self, option_codes: Sequence[str]) -> RtdOptionQuotesResult:
```

## Busca subprocess RTD/Excel

Comando:

```bash
git grep -n -E subprocess|Popen|run\( -- *.py
```

Saída:

```text
ATT/checks/check_cleanup_residuals.py:2:import subprocess
ATT/checks/check_cleanup_residuals.py:89:    result = subprocess.run(
ATT/checks/check_cleanup_residuals.py:93:        stdout=subprocess.PIPE,
ATT/checks/check_cleanup_residuals.py:94:        stderr=subprocess.PIPE,
ATT/checks/check_cleanup_residuals.py:108:    result = subprocess.run(
ATT/checks/check_cleanup_residuals.py:112:        stdout=subprocess.PIPE,
ATT/checks/check_cleanup_residuals.py:113:        stderr=subprocess.PIPE,
ATT/checks/run_all_checks.py:2:import subprocess
ATT/checks/run_all_checks.py:26:        result = subprocess.run([sys.executable, str(script_path)], cwd=str(CHECKS_DIR.parent))
ATT/tests/test_bd_unico_no_legacy_physical_db_creation.py:2:import subprocess
ATT/tests/test_bd_unico_no_legacy_physical_db_creation.py:71:    result = subprocess.run(
ATT/tests/test_bd_unico_no_legacy_physical_db_creation.py:117:    result = subprocess.run(
ATT/tests/test_excel_rtd_workbook_probe_contract.py:40:    result = probe.run()
ATT/tests/test_excel_rtd_workbook_probe_contract.py:60:    result = probe.run()
ATT/tests/test_excel_rtd_workbook_probe_contract.py:88:    result = probe.run()
ATT/tests/test_excel_rtd_workbook_probe_contract.py:132:    result = probe.run()
ATT/tests/test_excel_rtd_workbook_probe_contract.py:154:    result = probe.run()
ATT/tests/test_excel_rtd_workbook_probe_contract.py:177:    result = probe.run()
ATT/tests/test_pricing_engine_stub.py:22:    result = engine.run(pricing_payload)
ATT/tests/test_pricing_engine_stub.py:50:        engine.run({})
ATT/tests/test_pricing_engine_stub.py:67:        engine.run(pricing_payload)
ATT/tests/test_pricing_execution_service.py:24:    def run(self, pricing_payload):
ATT/tests/test_repository_generated_artifacts_guardrail.py:3:import subprocess
ATT/tests/test_repository_generated_artifacts_guardrail.py:21:    result = subprocess.run(
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:4:import subprocess
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:17:    Valida em um subprocess Python limpo, fora dos fakes de tkinter do conftest:
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:90:    completed = subprocess.run(
ATT/tests/test_ui_modern_moderndarkui_contract.py:2:import subprocess
ATT/tests/test_ui_modern_moderndarkui_contract.py:11:    return subprocess.run(
UI/components/details_panel.py:859:        """Chamado pelo MainWindow ao finalizar o subprocess do pipeline."""
UI/components/structure_editor_dialog.py:4:import subprocess
UI/components/structure_editor_dialog.py:438:            completed = subprocess.run(
UI/components/structure_editor_dialog.py:448:        except subprocess.TimeoutExpired:
UI/main_window.py:376:        import subprocess
UI/main_window.py:404:                res = subprocess.run(
UI/main_window.py:423:            except subprocess.TimeoutExpired:
UI/main_window.py:425:            except subprocess.CalledProcessError as e:
UI/main_window.py:459:            import subprocess
UI/main_window.py:462:            res = subprocess.run(
UI/main_window.py:478:        except subprocess.CalledProcessError as e:
UI/main_window.py:752:    def run(self):
UI/main_window.py:759:    app.run()
UI/modern/app.py:72:        result = module.run()
UI/modern/dark_window.py:272:    def run(self) -> None:
UI/modern/dark_window.py:278:    app.run()
db/migrations/add_structure_id_to_payoff_curve_points.py:80:def run(db_path: pathlib.Path):
db/migrations/add_structure_id_to_payoff_curve_points.py:129:    run(pathlib.Path(args.db))
scripts/23_smoke_pricing_execution_orchestration_error.py:8:    def run(self, pricing_payload):
scripts/check_rota_desenvolvimento.py:6:import subprocess
scripts/check_rota_desenvolvimento.py:66:def run(cmd: list[str], cwd: Path = ROOT, check: bool = False) -> str:
scripts/check_rota_desenvolvimento.py:67:    result = subprocess.run(
scripts/check_rota_desenvolvimento.py:71:        stdout=subprocess.PIPE,
scripts/check_rota_desenvolvimento.py:72:        stderr=subprocess.PIPE,
scripts/check_rota_desenvolvimento.py:101:    parents = run(["git", "show", "-s", "--format=%P", sha])
scripts/check_rota_desenvolvimento.py:106:    diff = run(["git", "diff", "--name-only", f"{first_parent}..{sha}"])
scripts/check_rota_desenvolvimento.py:133:        output = run([
scripts/check_rota_desenvolvimento.py:151:    output = run([
scripts/check_rota_desenvolvimento.py:203:    print(run(["git", "branch", "--show-current"]) or "(não identificado)")
scripts/check_rota_desenvolvimento.py:207:    status = run(["git", "status", "--short"])
scripts/check_rota_desenvolvimento.py:212:    print(run(["git", "log", "--oneline", "--decorate", "--date=short", "--format=%h %ad %d %s", "-20"]))
scripts/check_rota_desenvolvimento.py:264:    exists = run(["git", "cat-file", "-t", sha])
scripts/check_rota_desenvolvimento.py:270:    print(run(["git", "show", "-s", "--date=short", "--format=%h|%ad|%s|parents=%P", sha]))
scripts/check_rota_desenvolvimento.py:278:    files = run(["git", "diff", "--name-status", f"{sha}^..{sha}"])
scripts/probe_excel_rtd_workbook.py:59:    result = probe.run()
scripts/refresh_rtd_symbol_to_option_quotes.py:18:import subprocess
scripts/refresh_rtd_symbol_to_option_quotes.py:32:        completed = subprocess.run(
scripts/refresh_rtd_symbol_to_option_quotes.py:42:    except subprocess.TimeoutExpired as exc:
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:4:import subprocess
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:60:    cp = subprocess.run(
scripts/verify_rtd_excel_resume.py:9:import subprocess
scripts/verify_rtd_excel_resume.py:36:    r"Excel\.Application|subprocess|Popen|check_output|os\.system|Preencher|preencher|"
scripts/verify_rtd_excel_resume.py:83:        completed = subprocess.run(
services/excel_rtd_workbook_probe.py:184:    def run(self) -> ExcelRtdWorkbookProbeResult:
services/pricing_engine_stub.py:5:    def run(self, pricing_payload: dict[str, Any]) -> dict[str, Any]:
services/pricing_execution_service.py:31:        result = self.pricing_engine.run(pricing_payload)
```

## Busca status RTD Excel

Comando:

```bash
git grep -n -E excel_rtd|rtd|RTD|LISTA_RTD|connection_status -- services*.py
```

Saída:

```text
services/calculation_orchestrator.py:129:            source=str(market_snapshot_dict.get("source", "rtd")),
services/calculation_orchestrator.py:394:            "source": snapshot.get("source", "rtd"),
services/calculation_orchestrator.py:457:        "source": snapshot_row.get("source", "rtd"),
services/canonical_input_service.py:8:  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
services/canonical_input_service.py:151:        legs pelo resultado do selector (manual > rtd).
services/canonical_input_service.py:188:    # Legs via selector (manual > rtd)
services/canonical_pricing_facade.py:90:            # Formatos comuns vindos de RTD/planilha:
services/canonical_pricing_facade.py:363:            #  2. Seleciona snapshot (manual > rtd) 
services/excel_rtd_reader.py:13:from services.rtd_option_quotes_schema import (
services/excel_rtd_reader.py:20:from services.excel_rtd_com_access import (
services/excel_rtd_reader.py:160:    Escopo conservador: usado pelo leitor RTD Excel.
services/excel_rtd_reader.py:370:def read_excel_rtd_options(
services/excel_rtd_reader.py:457:def read_excel_rtd_options_as_dict(
services/excel_rtd_reader.py:462:        read_excel_rtd_options(
services/excel_rtd_workbook_probe.py:1:"""Probe controlado para diagnosticar o Excel RTD aberto.
services/excel_rtd_workbook_probe.py:8:- localizar LISTA_RTD.xlsm;
services/excel_rtd_workbook_probe.py:20:from services.rtd_option_quotes_schema import DEFAULT_WORKBOOK_NAME
services/excel_rtd_workbook_probe.py:21:from services.excel_rtd_com_access import get_active_excel_application
services/excel_rtd_workbook_probe.py:27:    """Erro controlado do probe Excel RTD."""
services/excel_rtd_workbook_probe.py:173:    """Servico de diagnostico do workbook RTD aberto."""
services/excel_rtd_workbook_probe.py:198:                message=f"erro inesperado no probe Excel RTD: {exc}",
services/excel_rtd_workbook_probe.py:222:                f"aba RTD solicitada nao encontrada: {requested_sheet}"
services/excel_rtd_workbook_probe.py:274:            message="workbook RTD localizado e amostra lida com sucesso",
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
services/robo_legs_service.py:23:      - obtém legs com regra manual > rtd
services/robo_legs_status_service.py:65:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(ref=ref)
services/robo_legs_status_service.py:69:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(aba)
services/robo_legs_status_service.py:74:        elif rtd_latest is not None:
services/robo_legs_status_service.py:75:            chosen_fonte = FonteType.RTD
services/robo_legs_status_service.py:76:            chosen_ts = rtd_latest
services/robo_legs_status_service.py:85:                rtd_latest_ts=None,
services/robo_legs_status_service.py:106:            rtd_latest_ts=rtd_latest,
services/rtd_option_quotes_schema.py:7:DEFAULT_WORKBOOK_NAME = "LISTA_RTD.xlsm"
services/rtd_option_quotes_schema.py:8:DEFAULT_SHEET_NAME = "RTD_OPTION_QUOTES"
services/rtd_option_quotes_schema.py:11:RTD_OPTION_QUOTES_MAP: Dict[str, Dict[str, Optional[str]]] = {
services/rtd_option_quotes_schema.py:14:        "rtd": None,
services/rtd_option_quotes_schema.py:18:        "role": "rtd",
services/rtd_option_quotes_schema.py:19:        "rtd": "QUOTE.UNDERLYING_SYMBOL",
services/rtd_option_quotes_schema.py:23:        "role": "rtd",
services/rtd_option_quotes_schema.py:24:        "rtd": "QUOTE.OPTION_TYPE",
services/rtd_option_quotes_schema.py:28:        "role": "rtd",
services/rtd_option_quotes_schema.py:29:        "rtd": "QUOTE.STRIKE_PRICE",
services/rtd_option_quotes_schema.py:33:        "role": "rtd",
services/rtd_option_quotes_schema.py:34:        "rtd": "QUOTE.MATURITYDATE",
services/rtd_option_quotes_schema.py:38:        "role": "rtd",
services/rtd_option_quotes_schema.py:39:        "rtd": "QUOTE.LAST_TRADE_PRICE",
services/rtd_option_quotes_schema.py:43:        "role": "rtd",
services/rtd_option_quotes_schema.py:44:        "rtd": "QUOTE.LAST_TRADE_QUANTITY",
services/rtd_option_quotes_schema.py:48:        "role": "rtd",
services/rtd_option_quotes_schema.py:49:        "rtd": "QUOTE.BID_PRICE",
services/rtd_option_quotes_schema.py:53:        "role": "rtd",
services/rtd_option_quotes_schema.py:54:        "rtd": "QUOTE.ASK_PRICE",
services/rtd_option_quotes_schema.py:58:        "role": "rtd",
services/rtd_option_quotes_schema.py:59:        "rtd": "QUOTE.VOLUME",
services/rtd_option_quotes_schema.py:63:        "role": "rtd",
services/rtd_option_quotes_schema.py:64:        "rtd": "QUOTE.IMPLIED_VOLATILITY",
services/rtd_option_quotes_schema.py:68:        "role": "rtd",
services/rtd_option_quotes_schema.py:69:        "rtd": "QUOTE.DELTA",
services/rtd_option_quotes_schema.py:73:        "role": "rtd",
services/rtd_option_quotes_schema.py:74:        "rtd": "QUOTE.GAMMA",
services/rtd_option_quotes_schema.py:78:        "role": "rtd",
services/rtd_option_quotes_schema.py:79:        "rtd": "QUOTE.THETA",
services/rtd_option_quotes_schema.py:83:        "role": "rtd",
services/rtd_option_quotes_schema.py:84:        "rtd": "QUOTE.VEGA",
services/rtd_option_quotes_schema.py:88:        "role": "rtd",
services/rtd_option_quotes_schema.py:89:        "rtd": "QUOTE.VWAP",
services/rtd_option_quotes_schema.py:95:REQUIRED_OPTION_HEADERS = list(RTD_OPTION_QUOTES_MAP.keys())
services/rtd_option_quotes_sync_service.py:7:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
services/rtd_option_quotes_sync_service.py:8:from services.excel_rtd_reader import (
services/rtd_option_quotes_sync_service.py:11:    read_excel_rtd_options_as_dict,
services/rtd_option_quotes_sync_service.py:31:def sync_rtd_option_quotes_records(
services/rtd_option_quotes_sync_service.py:35:    source: str = "excel_rtd_live",
services/rtd_option_quotes_sync_service.py:65:def sync_rtd_option_quotes_from_excel(
services/rtd_option_quotes_sync_service.py:70:    reader_fn: Callable[..., Mapping[str, Any]] = read_excel_rtd_options_as_dict,
services/rtd_option_quotes_sync_service.py:106:            error=read_result.get("error") or "excel_rtd_reader_returned_not_ok",
services/rtd_option_quotes_sync_service.py:109:    sync_result = sync_rtd_option_quotes_records(
services/rtd_option_quotes_sync_service.py:112:        source="excel_rtd_live",
services/structure_leg_rtd_enrichment_service.py:1:"""Service de enriquecimento de legs de estruturas via RTD.
services/structure_leg_rtd_enrichment_service.py:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:19:    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
services/structure_leg_rtd_enrichment_service.py:21:    def __init__(self, rtd_option_quotes_repository: Any) -> None:
services/structure_leg_rtd_enrichment_service.py:22:        self._repo = rtd_option_quotes_repository
services/structure_leg_rtd_enrichment_service.py:38:        Campos enriquecidos via RTD:
services/structure_leg_rtd_enrichment_service.py:49:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py:123:                raise ValueError(f"missing required RTD field: {field}")
services/terminal_vwap_payoff_app_service.py:6:- não acessa Excel, RTD real ou UI pesada diretamente.
services/terminal_vwap_payoff_app_service.py:25:    diretamente a Excel, RTD, Tkinter ou banco em testes unitários.
services/terminal_vwap_payoff_viewmodel_service.py:7:- não acessa RTD real;
```
