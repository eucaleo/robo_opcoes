# Auditoria de fechamento da Fase 1 - RTD Excel BTG Online

Data: 2026-07-10 10:27:29

## Objetivo

Conferir se a Fase 1 do roteiro RTD Excel pode ser encerrada ou se ainda existem pendências operacionais.


## Critérios da Fase 1

- Manter LISTA_RTD.xlsm aberto.

- Detectar Excel aberto.

- Detectar workbook correto.

- Detectar aba RTD_OPTION_QUOTES.

- Validar cabeçalhos obrigatórios.

- Ler tabela viva RTD.

- Atualizar snapshot ou tabela RTD no banco.

- Exibir status RTD na UI.

- Eliminar subprocesso operacional para preencher leg.

## Git status inicial

Comando:

```bash
git status --short
```

Exit code: 0

Saída: sem ocorrências.

## Branch atual

Comando:

```bash
git branch --show-current
```

Exit code: 0

Saída:

```text
refactor/bd-unico-appdb
```

## Últimos commits

Comando:

```bash
git log --oneline -12
```

Exit code: 0

Saída:

```text
5af5813 docs: registra auditoria de retorno ao roteiro RTD Excel
647360d refactor: conclui centralizacao COM operacional RTD Excel
3b9ef80 fix: restaura modelo de status RTD Excel
6869b73 fix: aplica centralizacao COM Excel RTD
0337f8d refactor: centraliza acesso COM Excel RTD
7ead120 chore: padroniza line endings do projeto
a2059bb refactor: centraliza schema RTD option quotes
244bb49 feat: adiciona status RTD Excel no menu ajuda
ec00d4e feat: expose Excel RTD status payload
dbc0c83 feat: add Excel RTD connection status service
6e7a532 chore: guard against generated RTD artifacts
ff4318e refactor: move Excel RTD reader to RTD bridge
```

## Arquivos centrais RTD Excel

Comando:

```bash
git ls-files services/excel_rtd_com_access.py services/excel_rtd_workbook_probe.py services/excel_rtd_reader.py services/rtd_option_quotes_schema.py services/rtd_option_quotes_sync_service.py repositories/rtd_option_quotes_repository.py
```

Exit code: 0

Saída:

```text
repositories/rtd_option_quotes_repository.py
services/excel_rtd_com_access.py
services/excel_rtd_reader.py
services/excel_rtd_workbook_probe.py
services/rtd_option_quotes_schema.py
services/rtd_option_quotes_sync_service.py
```

## Validação de acesso COM centralizado

Comando:

```bash
git grep -n -E get_active_excel_application|import_win32com_client|ExcelComUnavailableError -- services/excel_rtd_com_access.py services/excel_rtd_workbook_probe.py services/excel_rtd_reader.py
```

Exit code: 0

Saída:

```text
services/excel_rtd_com_access.py:14:class ExcelComUnavailableError(ExcelComAccessError):
services/excel_rtd_com_access.py:18:def import_win32com_client() -> Any:
services/excel_rtd_com_access.py:22:        raise ExcelComUnavailableError(f"win32com indisponivel: {exc}") from exc
services/excel_rtd_com_access.py:27:def get_active_excel_application(prog_id: str = EXCEL_PROG_ID) -> Any:
services/excel_rtd_com_access.py:28:    win32com_client = import_win32com_client()
services/excel_rtd_reader.py:23:    get_active_excel_application,
services/excel_rtd_reader.py:285:        return get_active_excel_application()
services/excel_rtd_workbook_probe.py:21:from services.excel_rtd_com_access import get_active_excel_application
services/excel_rtd_workbook_probe.py:82:            self._excel = get_active_excel_application()
```

## Validação de workbook, aba e cabeçalhos

Comando:

```bash
git grep -n -E LISTA_RTD|RTD_OPTION_QUOTES|REQUIRED_OPTION_HEADERS|validate|required|header|cabec -- services/excel_rtd_workbook_probe.py services/excel_rtd_reader.py services/rtd_option_quotes_schema.py
```

Exit code: 0

Saída:

```text
services/excel_rtd_reader.py:16:    REQUIRED_OPTION_HEADERS,
services/excel_rtd_reader.py:17:    normalize_header,
services/excel_rtd_reader.py:72:    headers: List[str]
services/excel_rtd_reader.py:73:    missing_headers: List[str]
services/excel_rtd_reader.py:327:def build_header_index(raw_header_row: Sequence[Any]) -> Dict[str, int]:
services/excel_rtd_reader.py:328:    header_index = {}
services/excel_rtd_reader.py:330:    for index, value in enumerate(raw_header_row):
services/excel_rtd_reader.py:331:        header = normalize_header(value)
services/excel_rtd_reader.py:332:        if header and header not in header_index:
services/excel_rtd_reader.py:333:            header_index[header] = index
services/excel_rtd_reader.py:335:    return header_index
services/excel_rtd_reader.py:340:    header_index: Dict[str, int],
services/excel_rtd_reader.py:341:    headers: Sequence[str],
services/excel_rtd_reader.py:345:    for header in headers:
services/excel_rtd_reader.py:346:        index = header_index.get(header)
services/excel_rtd_reader.py:352:        record[header] = normalize_cell(header, raw_value)
services/excel_rtd_reader.py:373:    required_headers: Optional[Sequence[str]] = None,
services/excel_rtd_reader.py:375:    required = list(required_headers or REQUIRED_OPTION_HEADERS)
services/excel_rtd_reader.py:388:        header_index = build_header_index(rows[0])
services/excel_rtd_reader.py:389:        headers = list(header_index.keys())
services/excel_rtd_reader.py:390:        missing = [header for header in required if header not in header_index]
services/excel_rtd_reader.py:398:                headers=headers,
services/excel_rtd_reader.py:399:                missing_headers=missing,
services/excel_rtd_reader.py:403:                error="headers_obrigatorios_ausentes",
services/excel_rtd_reader.py:409:            record = normalize_record(row, header_index, required)
services/excel_rtd_reader.py:418:            headers=headers,
services/excel_rtd_reader.py:419:            missing_headers=[],
services/excel_rtd_reader.py:432:            headers=[],
services/excel_rtd_reader.py:433:            missing_headers=required,
services/excel_rtd_reader.py:447:        "headers": result.headers,
services/excel_rtd_reader.py:448:        "missing_headers": result.missing_headers,
services/excel_rtd_workbook_probe.py:8:- localizar LISTA_RTD.xlsm;
services/excel_rtd_workbook_probe.py:65:    headers: list[str] = field(default_factory=list)
services/excel_rtd_workbook_probe.py:134:                "headers": [],
services/excel_rtd_workbook_probe.py:148:        headers = [
services/excel_rtd_workbook_probe.py:155:            "headers": headers,
services/excel_rtd_workbook_probe.py:280:            headers=[str(h).strip() for h in sample.get("headers", [])],
services/rtd_option_quotes_schema.py:7:DEFAULT_WORKBOOK_NAME = "LISTA_RTD.xlsm"
services/rtd_option_quotes_schema.py:8:DEFAULT_SHEET_NAME = "RTD_OPTION_QUOTES"
services/rtd_option_quotes_schema.py:11:RTD_OPTION_QUOTES_MAP: Dict[str, Dict[str, Optional[str]]] = {
services/rtd_option_quotes_schema.py:95:REQUIRED_OPTION_HEADERS = list(RTD_OPTION_QUOTES_MAP.keys())
services/rtd_option_quotes_schema.py:98:def normalize_header(value: Any) -> str:
```

## Status RTD na UI e menu ajuda

Comando:

```bash
git grep -n -E RTD|Excel|Ajuda|Help|connection_status|status -- UI services ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py ATT/tests/test_excel_rtd_connection_status.py ATT/tests/test_excel_rtd_connection_status_presenter.py
```

Exit code: 0

Saída:

```text
ATT/tests/test_excel_rtd_connection_status.py:3:from rtd_bridge.excel_rtd_connection_status import (
ATT/tests/test_excel_rtd_connection_status.py:7:    check_excel_rtd_connection_status,
ATT/tests/test_excel_rtd_connection_status.py:81:class FakeExcel:
ATT/tests/test_excel_rtd_connection_status.py:86:def test_status_is_ready_when_excel_workbook_sheet_and_headers_are_valid() -> None:
ATT/tests/test_excel_rtd_connection_status.py:96:    excel = FakeExcel([workbook])
ATT/tests/test_excel_rtd_connection_status.py:98:    status = check_excel_rtd_connection_status(excel_app=excel)
ATT/tests/test_excel_rtd_connection_status.py:100:    assert status.is_ready is True
ATT/tests/test_excel_rtd_connection_status.py:101:    assert status.pywin32_available is True
ATT/tests/test_excel_rtd_connection_status.py:102:    assert status.excel_running is True
ATT/tests/test_excel_rtd_connection_status.py:103:    assert status.workbook_open is True
ATT/tests/test_excel_rtd_connection_status.py:104:    assert status.worksheet_available is True
ATT/tests/test_excel_rtd_connection_status.py:105:    assert status.required_headers_ok is True
ATT/tests/test_excel_rtd_connection_status.py:106:    assert status.missing_headers == ()
ATT/tests/test_excel_rtd_connection_status.py:107:    assert status.message == "RTD Excel pronto para leitura."
ATT/tests/test_excel_rtd_connection_status.py:110:def test_status_reports_missing_workbook() -> None:
ATT/tests/test_excel_rtd_connection_status.py:111:    excel = FakeExcel([])
ATT/tests/test_excel_rtd_connection_status.py:113:    status = check_excel_rtd_connection_status(excel_app=excel)
ATT/tests/test_excel_rtd_connection_status.py:115:    assert status.is_ready is False
ATT/tests/test_excel_rtd_connection_status.py:116:    assert status.pywin32_available is True
ATT/tests/test_excel_rtd_connection_status.py:117:    assert status.excel_running is True
ATT/tests/test_excel_rtd_connection_status.py:118:    assert status.workbook_open is False
ATT/tests/test_excel_rtd_connection_status.py:119:    assert status.worksheet_available is False
ATT/tests/test_excel_rtd_connection_status.py:120:    assert status.required_headers_ok is False
ATT/tests/test_excel_rtd_connection_status.py:121:    assert status.missing_headers == REQUIRED_OPTION_QUOTE_HEADERS
ATT/tests/test_excel_rtd_connection_status.py:122:    assert "Workbook obrigatório não está aberto" in status.message
ATT/tests/test_excel_rtd_connection_status.py:125:def test_status_reports_missing_worksheet() -> None:
ATT/tests/test_excel_rtd_connection_status.py:131:    excel = FakeExcel([workbook])
ATT/tests/test_excel_rtd_connection_status.py:133:    status = check_excel_rtd_connection_status(excel_app=excel)
ATT/tests/test_excel_rtd_connection_status.py:135:    assert status.is_ready is False
ATT/tests/test_excel_rtd_connection_status.py:136:    assert status.workbook_open is True
ATT/tests/test_excel_rtd_connection_status.py:137:    assert status.worksheet_available is False
ATT/tests/test_excel_rtd_connection_status.py:138:    assert status.required_headers_ok is False
ATT/tests/test_excel_rtd_connection_status.py:139:    assert status.missing_headers == REQUIRED_OPTION_QUOTE_HEADERS
ATT/tests/test_excel_rtd_connection_status.py:140:    assert "Aba obrigatória ausente" in status.message
ATT/tests/test_excel_rtd_connection_status.py:143:def test_status_reports_missing_required_header() -> None:
ATT/tests/test_excel_rtd_connection_status.py:155:    excel = FakeExcel([workbook])
ATT/tests/test_excel_rtd_connection_status.py:157:    status = check_excel_rtd_connection_status(excel_app=excel)
ATT/tests/test_excel_rtd_connection_status.py:159:    assert status.is_ready is False
ATT/tests/test_excel_rtd_connection_status.py:160:    assert status.workbook_open is True
ATT/tests/test_excel_rtd_connection_status.py:161:    assert status.worksheet_available is True
ATT/tests/test_excel_rtd_connection_status.py:162:    assert status.required_headers_ok is False
ATT/tests/test_excel_rtd_connection_status.py:163:    assert status.missing_headers == ("iv",)
ATT/tests/test_excel_rtd_connection_status.py:164:    assert status.message == (
ATT/tests/test_excel_rtd_connection_status.py:165:        "Cabeçalho obrigatório ausente na aba RTD_OPTION_QUOTES: iv"
ATT/tests/test_excel_rtd_connection_status.py:169:def test_status_accepts_headers_moved_to_different_columns() -> None:
ATT/tests/test_excel_rtd_connection_status.py:194:    excel = FakeExcel([workbook])
ATT/tests/test_excel_rtd_connection_status.py:196:    status = check_excel_rtd_connection_status(excel_app=excel)
ATT/tests/test_excel_rtd_connection_status.py:198:    assert status.is_ready is True
ATT/tests/test_excel_rtd_connection_status.py:199:    assert status.detected_headers == moved_headers
ATT/tests/test_excel_rtd_connection_status.py:200:    assert status.missing_headers == ()
ATT/tests/test_excel_rtd_connection_status_presenter.py:5:from rtd_bridge.excel_rtd_connection_status import (
ATT/tests/test_excel_rtd_connection_status_presenter.py:9:    ExcelRtdConnectionStatus,
ATT/tests/test_excel_rtd_connection_status_presenter.py:11:from rtd_bridge.excel_rtd_connection_status_presenter import (
ATT/tests/test_excel_rtd_connection_status_presenter.py:12:    build_excel_rtd_status_view_model,
ATT/tests/test_excel_rtd_connection_status_presenter.py:13:    get_excel_rtd_status_payload,
ATT/tests/test_excel_rtd_connection_status_presenter.py:14:    get_excel_rtd_status_view_model,
ATT/tests/test_excel_rtd_connection_status_presenter.py:21:def _ready_status() -> ExcelRtdConnectionStatus:
ATT/tests/test_excel_rtd_connection_status_presenter.py:22:    return ExcelRtdConnectionStatus(
ATT/tests/test_excel_rtd_connection_status_presenter.py:33:        message="RTD Excel pronto para leitura.",
ATT/tests/test_excel_rtd_connection_status_presenter.py:37:def test_build_view_model_for_ready_status() -> None:
ATT/tests/test_excel_rtd_connection_status_presenter.py:38:    view_model = build_excel_rtd_status_view_model(
ATT/tests/test_excel_rtd_connection_status_presenter.py:39:        status=_ready_status(),
ATT/tests/test_excel_rtd_connection_status_presenter.py:45:    assert view_model.title == "RTD Excel online"
ATT/tests/test_excel_rtd_connection_status_presenter.py:46:    assert view_model.message == "RTD Excel pronto para leitura."
ATT/tests/test_excel_rtd_connection_status_presenter.py:55:def test_payload_is_serializable_dict_for_ready_status() -> None:
ATT/tests/test_excel_rtd_connection_status_presenter.py:56:    view_model = build_excel_rtd_status_view_model(
ATT/tests/test_excel_rtd_connection_status_presenter.py:57:        status=_ready_status(),
ATT/tests/test_excel_rtd_connection_status_presenter.py:65:    assert payload["title"] == "RTD Excel online"
ATT/tests/test_excel_rtd_connection_status_presenter.py:78:def test_build_view_model_for_missing_workbook_status() -> None:
ATT/tests/test_excel_rtd_connection_status_presenter.py:79:    status = ExcelRtdConnectionStatus(
ATT/tests/test_excel_rtd_connection_status_presenter.py:91:    view_model = build_excel_rtd_status_view_model(
ATT/tests/test_excel_rtd_connection_status_presenter.py:92:        status=status,
ATT/tests/test_excel_rtd_connection_status_presenter.py:98:    assert view_model.title == "Workbook RTD não aberto"
ATT/tests/test_excel_rtd_connection_status_presenter.py:109:def test_build_view_model_for_missing_header_status() -> None:
ATT/tests/test_excel_rtd_connection_status_presenter.py:110:    status = ExcelRtdConnectionStatus(
ATT/tests/test_excel_rtd_connection_status_presenter.py:125:        message="Cabeçalho obrigatório ausente na aba RTD_OPTION_QUOTES: iv",
ATT/tests/test_excel_rtd_connection_status_presenter.py:128:    view_model = build_excel_rtd_status_view_model(
ATT/tests/test_excel_rtd_connection_status_presenter.py:129:        status=status,
ATT/tests/test_excel_rtd_connection_status_presenter.py:135:    assert view_model.title == "Cabeçalhos RTD inválidos"
ATT/tests/test_excel_rtd_connection_status_presenter.py:144:def test_get_view_model_uses_injected_status_checker() -> None:
ATT/tests/test_excel_rtd_connection_status_presenter.py:147:    def fake_status_checker(**kwargs):
ATT/tests/test_excel_rtd_connection_status_presenter.py:149:        return _ready_status()
ATT/tests/test_excel_rtd_connection_status_presenter.py:151:    view_model = get_excel_rtd_status_view_model(
ATT/tests/test_excel_rtd_connection_status_presenter.py:153:        status_checker=fake_status_checker,
ATT/tests/test_excel_rtd_connection_status_presenter.py:157:    assert view_model.title == "RTD Excel online"
ATT/tests/test_excel_rtd_connection_status_presenter.py:165:def test_get_payload_uses_injected_status_checker() -> None:
ATT/tests/test_excel_rtd_connection_status_presenter.py:166:    def fake_status_checker(**kwargs):
ATT/tests/test_excel_rtd_connection_status_presenter.py:167:        return _ready_status()
ATT/tests/test_excel_rtd_connection_status_presenter.py:169:    payload = get_excel_rtd_status_payload(
ATT/tests/test_excel_rtd_connection_status_presenter.py:171:        status_checker=fake_status_checker,
ATT/tests/test_excel_rtd_connection_status_presenter.py:176:    assert payload["title"] == "RTD Excel online"
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:13:def test_operational_dark_window_help_menu_and_live_excel_rtd_status() -> None:
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:21:    - construção real do menu Ajuda;
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:22:    - presença do item "Status RTD Excel";
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:23:    - payload real do RTD/Excel ativo;
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:26:    Este teste deve falhar se Excel/RTD/workbook/aba/cabeçalhos não estiverem
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:61:            if label == "Ajuda":
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:75:    payload = module.get_excel_rtd_status_payload()
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:76:    message = module._format_excel_rtd_status_message(payload)
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:118:    assert "Ajuda" in data["top_level_labels"]
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:119:    assert "Status RTD Excel" in data["help_labels"]
ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py:133:    assert payload["title"] == "RTD Excel online"
UI/components/decisions_dark_panel.py:50:        on_status: Optional[Callable[[str], None]] = None,
UI/components/decisions_dark_panel.py:57:        self.on_status = on_status
UI/components/decisions_dark_panel.py:65:        self._last_decision_status_text: Optional[str] = None
UI/components/decisions_dark_panel.py:66:        self._last_filter_status_text: Optional[str] = None
UI/components/decisions_dark_panel.py:73:    def _status(self, message: str) -> None:
UI/components/decisions_dark_panel.py:74:        if self.on_status:
UI/components/decisions_dark_panel.py:75:            self.on_status(message)
UI/components/decisions_dark_panel.py:308:        self._last_filter_status_text = None
UI/components/decisions_dark_panel.py:325:        self._select_decision(0, notify_status=False)
UI/components/decisions_dark_panel.py:328:            self._status(f"{len(self.decisions)} decisões carregadas no modo dark")
UI/components/decisions_dark_panel.py:331:        self._status_filter_result(
UI/components/decisions_dark_panel.py:338:        self._status_filter_result(
UI/components/decisions_dark_panel.py:345:        self._status("Nenhuma decisão encontrada no modo dark")
UI/components/decisions_dark_panel.py:355:        self._status(f"Erro ao carregar decisões: {exc}")
UI/components/decisions_dark_panel.py:556:            self._status(f"Erro ao carregar estruturas para filtro de decisões: {exc}")
UI/components/decisions_dark_panel.py:608:        status = self._structure_status_value(structure)
UI/components/decisions_dark_panel.py:610:        if status:
UI/components/decisions_dark_panel.py:611:            return not self._is_inactive_structure_status(status)
UI/components/decisions_dark_panel.py:613:        # Se nao houver campo de status, assume ativa para preservar compatibilidade.
UI/components/decisions_dark_panel.py:633:    def _structure_status_value(self, structure: Dict[str, Any]) -> str:
UI/components/decisions_dark_panel.py:634:        status = (
UI/components/decisions_dark_panel.py:635:            structure.get("status")
UI/components/decisions_dark_panel.py:641:        return str(status).strip().lower() if status else ""
UI/components/decisions_dark_panel.py:643:    def _is_inactive_structure_status(self, status: str) -> bool:
UI/components/decisions_dark_panel.py:664:        return status in inactive_values
UI/components/decisions_dark_panel.py:787:            self._status_filter_result(
UI/components/decisions_dark_panel.py:793:        self._status_filter_result("Nenhuma decisão de estrutura ativa encontrada no modo dark")
UI/components/decisions_dark_panel.py:825:        self._status_filter_result(f"Filtro inválido: {error_text}")
UI/components/decisions_dark_panel.py:843:            self._select_decision(0, notify_status=False)
UI/components/decisions_dark_panel.py:844:            self._status_filter_summary(active_decisions, announce_clear)
UI/components/decisions_dark_panel.py:859:    def _status_filter_summary(
UI/components/decisions_dark_panel.py:870:                self._status_filter_result(
UI/components/decisions_dark_panel.py:874:                self._status_filter_result(
UI/components/decisions_dark_panel.py:878:            self._status_filter_result(f"Filtros limpos: {active_label}")
UI/components/decisions_dark_panel.py:957:            self._status("Nenhuma decisão selecionada para carregar estrutura")
UI/components/decisions_dark_panel.py:961:            self._status("Seleção de decisão inválida")
UI/components/decisions_dark_panel.py:968:            self._status("Decisão selecionada não possui structure_id")
UI/components/decisions_dark_panel.py:972:            self._status("Carregamento de estrutura não está disponível")
UI/components/decisions_dark_panel.py:977:    def _select_decision(self, index: int, notify_status: bool = True) -> None:
UI/components/decisions_dark_panel.py:989:        if notify_status:
UI/components/decisions_dark_panel.py:990:            self._status_selected_decision(self._selected_decision_status_text(decision))
UI/components/decisions_dark_panel.py:1014:    def _selected_decision_status_text(self, decision: Dict[str, Any]) -> str:
UI/components/decisions_dark_panel.py:1028:        self._last_decision_status_text = None
UI/components/decisions_dark_panel.py:1030:    def _status_selected_decision(self, status_text: str) -> None:
UI/components/decisions_dark_panel.py:1031:        if status_text == getattr(self, "_last_decision_status_text", None):
UI/components/decisions_dark_panel.py:1033:        self._last_decision_status_text = status_text
UI/components/decisions_dark_panel.py:1034:        self._status(status_text)
UI/components/decisions_dark_panel.py:1036:    def _status_filter_result(self, status_text: str) -> None:
UI/components/decisions_dark_panel.py:1037:        if status_text == getattr(self, "_last_filter_status_text", None):
UI/components/decisions_dark_panel.py:1039:        self._last_filter_status_text = status_text
UI/components/decisions_dark_panel.py:1040:        self._status(status_text)
UI/components/decisions_dark_panel.py:1046:            self._status("Nenhuma decisão selecionada para copiar")
UI/components/decisions_dark_panel.py:1051:            self._status("Detalhe da decisão selecionada está vazio")
UI/components/decisions_dark_panel.py:1056:        self._status("Detalhe da decisão copiado para a área de transferência")
UI/components/decisions_dark_panel.py:1065:            self._status("Exportação CSV cancelada")
UI/components/decisions_dark_panel.py:1078:        self._status("Nenhuma decisão exibida para exportar")
UI/components/decisions_dark_panel.py:1126:        self._status(f"{total} decisões exportadas em CSV")
UI/components/decisions_dark_panel.py:1133:        self._status(f"Erro ao exportar CSV: {exc}")
UI/components/decisions_dark_panel.py:1230:    def _structure_status_label(self, structure_id: Any) -> str:
UI/components/decisions_dark_panel.py:1296:            "structure_status": self._structure_status_label(structure_id),
UI/components/decisions_dark_panel.py:1322:            f"Status da estrutura: {values['structure_status']}",
UI/components/details_panel.py:40:            if hasattr(self, "lbl_recalc_status") and self.lbl_recalc_status:
UI/components/details_panel.py:41:                self.lbl_recalc_status.config(text=msg, foreground=color)
UI/components/details_panel.py:631:            "operational_status_label",
UI/components/details_panel.py:728:        self.lbl_recalc_status = ttk.Label(
UI/components/details_panel.py:733:        self.lbl_recalc_status.pack(side="left")
UI/components/details_panel.py:811:        self.lbl_recalc_status.config(text="", foreground="gray")
UI/components/details_panel.py:852:            self.operational_status_label,
UI/components/details_panel.py:856:        self.lbl_recalc_status.config(text="", foreground="gray")
UI/components/details_panel.py:883:            "operational_status_label",
UI/components/details_panel.py:909:            "status": self._operational_status_text(effective_structure, state),
UI/components/details_panel.py:936:    def _operational_status_text(self, effective_structure: Dict[str, Any], state: Dict[str, Any]):
UI/components/details_panel.py:954:        self.operational_status_label.config(text=values["status"])
UI/components/details_panel.py:1004:    # Helpers internos
UI/components/details_panel.py:1205:            self.lbl_recalc_status.config(
UI/components/details_panel.py:1214:            self.lbl_recalc_status.config(
UI/components/details_panel.py:1246:            self.lbl_recalc_status.config(
UI/components/filters_panel.py:93:        self.status_label = ttk.Label(self, text="Filtros prontos", foreground="green")
UI/components/filters_panel.py:94:        self.status_label.pack(fill="x", pady=(5, 0))
UI/components/filters_panel.py:131:        self.status_label.config(
UI/components/filters_panel.py:148:        self.status_label.config(text="Filtros limpos", foreground="green")
UI/components/payoff_chart.py:18:# Helpers de formatação pt-BR
UI/components/structure_editor_dialog.py:26:    _f_status       tk.StringVar
UI/components/structure_editor_dialog.py:99:        self._f_status     = tk.StringVar(value="active")
UI/components/structure_editor_dialog.py:129:            ("Status",         self._f_status,     "combo", ["active", "archived"]),
UI/components/structure_editor_dialog.py:247:            text="[RTD] Preencher por Simbolo",
UI/components/structure_editor_dialog.py:280:        self._f_status.set(data.get("status", "active"))
UI/components/structure_editor_dialog.py:412:        """Atualiza uma opcao via RTD/Excel e grava o cache em dados/app.db."""
UI/components/structure_editor_dialog.py:423:            return False, f"Script RTD nao encontrado: {script_path}"
UI/components/structure_editor_dialog.py:449:            return False, f"Timeout ao atualizar RTD para {symbol}."
UI/components/structure_editor_dialog.py:456:            return False, f"Falha ao atualizar RTD para {symbol}: {detail}"
UI/components/structure_editor_dialog.py:461:            return False, f"RTD atualizou, mas retornou JSON invalido: {stdout[:500]}"
UI/components/structure_editor_dialog.py:463:        if data.get("status") != "ok":
UI/components/structure_editor_dialog.py:465:            return False, f"RTD retornou erro para {symbol}: {errors}"
UI/components/structure_editor_dialog.py:470:            return False, f"RTD executou, mas nao retornou cotacao para {symbol}."
UI/components/structure_editor_dialog.py:475:        """Cria/lazily retorna o service de preenchimento de leg via RTD."""
UI/components/structure_editor_dialog.py:504:                "Preencher via RTD",
UI/components/structure_editor_dialog.py:513:                "Preencher via RTD",
UI/components/structure_editor_dialog.py:514:                "Informe o campo 'Simbolo' antes de consultar o RTD.",
UI/components/structure_editor_dialog.py:533:                    "Preencher via RTD",
UI/components/structure_editor_dialog.py:542:                "Preencher via RTD",
UI/components/structure_editor_dialog.py:543:                f"Nao foi possivel preencher a leg pelo RTD:\n{exc}",
UI/components/structure_editor_dialog.py:621:            "status":           self._f_status.get(),
UI/components/structures_list_panel.py:4:Lista de estruturas com filtro de status, botoes CRUD e duplicar.
UI/components/structures_list_panel.py:19:    _status_var     tk.StringVar  ("active" | "all")
UI/components/structures_list_panel.py:35:_COLUMNS = ("id", "name", "underlying_asset", "alias", "status", "legs")
UI/components/structures_list_panel.py:41:    "status":           ("Status",    70,  "center"),
UI/components/structures_list_panel.py:76:        """Barra superior: filtro de status + busca por nome."""
UI/components/structures_list_panel.py:82:        self._status_var = tk.StringVar(value="active")
UI/components/structures_list_panel.py:83:        status_cb = ttk.Combobox(
UI/components/structures_list_panel.py:85:            textvariable=self._status_var,
UI/components/structures_list_panel.py:90:        status_cb.pack(side="left", padx=(2, 10))
UI/components/structures_list_panel.py:91:        status_cb.bind("<<ComboboxSelected>>", lambda _e: self.load())
UI/components/structures_list_panel.py:152:        self._status_label_var = tk.StringVar(value="")
UI/components/structures_list_panel.py:155:            textvariable=self._status_label_var,
UI/components/structures_list_panel.py:165:        """Recarrega do banco respeitando o filtro de status atual."""
UI/components/structures_list_panel.py:166:        include_archived = self._status_var.get() == "all"
UI/components/structures_list_panel.py:198:                    row["status"],
UI/components/structures_list_panel.py:201:                tags=(row["status"],),
UI/components/structures_list_panel.py:209:    # Helpers internos
UI/components/structures_list_panel.py:288:                "status":           "active",
UI/components/structures_list_panel.py:310:        alteracao_71: arquiva a estrutura selecionada com confirmacao e feedback de status.
UI/components/structures_list_panel.py:319:        if src and src.get("status") == "archived":
UI/components/structures_list_panel.py:334:            self._set_status(f"Estrutura '{name}' arquivada.")
UI/components/structures_list_panel.py:337:            self._set_status(f"Erro ao arquivar: {exc}")
UI/components/structures_list_panel.py:343:    # Feedback de status
UI/components/structures_list_panel.py:346:    def _set_status(self, msg: str) -> None:
UI/components/structures_list_panel.py:349:            self._status_label_var.set(msg)
UI/components/terminal_vwap_payoff_dark_panel.py:134:        on_status=None,
UI/components/terminal_vwap_payoff_dark_panel.py:139:        self.on_status = on_status or (lambda _msg: None)
UI/components/terminal_vwap_payoff_dark_panel.py:467:            self._safe_status(f"Erro ao carregar estruturas: {exc}")
UI/components/terminal_vwap_payoff_dark_panel.py:471:        self._safe_status(f"{len(self.structures)} estruturas carregadas")
UI/components/terminal_vwap_payoff_dark_panel.py:569:            status_col = _first_col(cols, ["status", "state", "situacao"])
UI/components/terminal_vwap_payoff_dark_panel.py:578:                f"{_q(status_col)} AS status" if status_col else "NULL AS status",
UI/components/terminal_vwap_payoff_dark_panel.py:590:                item["status"] = item.get("status") or "N/A"
UI/components/terminal_vwap_payoff_dark_panel.py:662:        status = structure.get("status")
UI/components/terminal_vwap_payoff_dark_panel.py:666:            text=f"ID {sid} | {asset}\n{name}\n{status}",
UI/components/terminal_vwap_payoff_dark_panel.py:696:        self.on_status(f"Estrutura carregada: ID {sid}")
UI/components/terminal_vwap_payoff_dark_panel.py:704:            if hasattr(self, 'on_status'):
UI/components/terminal_vwap_payoff_dark_panel.py:705:                self.on_status(f"Falha ao abrir painel de acoes: {exc}")
UI/components/terminal_vwap_payoff_dark_panel.py:1375:            self._safe_status("Exportacao PNG indisponivel")
UI/components/terminal_vwap_payoff_dark_panel.py:1386:            self._safe_status("Exportacao PNG cancelada")
UI/components/terminal_vwap_payoff_dark_panel.py:1391:            self._safe_status("Payoff exportado em PNG")
UI/components/terminal_vwap_payoff_dark_panel.py:1398:            self._safe_status("Erro ao exportar PNG")
UI/components/terminal_vwap_payoff_dark_panel.py:1406:    def _safe_status(self, message: str) -> None:
UI/components/terminal_vwap_payoff_dark_panel.py:1407:        if hasattr(self, "on_status"):
UI/components/terminal_vwap_payoff_dark_panel.py:1408:            self.on_status(message)
UI/components/terminal_vwap_payoff_dark_panel.py:1433:        self._safe_status(message)
UI/components/terminal_vwap_payoff_dark_panel.py:1469:        self._safe_status(msg)
UI/components/terminal_vwap_payoff_dark_panel.py:1680:        status = structure.get("status")
UI/components/terminal_vwap_payoff_dark_panel.py:1681:        return f"ID {sid}\n{name}\nAtivo: {asset}\nStatus: {status}"
UI/components/terminal_vwap_payoff_dark_panel.py:1790:        self._safe_status(f"Modo de ajuste aberto: ID {sid}")
UI/components/terminal_vwap_payoff_dark_panel.py:1854:                self._safe_status("Nova estrutura salva")
UI/components/terminal_vwap_payoff_dark_panel.py:1902:        self._safe_status(f"Estrutura ID {sid} atualizada")
UI/components/terminal_vwap_payoff_dark_panel.py:1937:            self._safe_status(f"Estrutura duplicada: ID {new_id}")
UI/components/terminal_vwap_payoff_dark_panel.py:1940:            self._safe_status(f"Erro ao duplicar estrutura: {exc}")
UI/components/terminal_vwap_payoff_dark_panel.py:1972:            "status": "active",
UI/components/terminal_vwap_payoff_dark_panel.py:2029:            self._safe_status(f"Payoff recalculado: ID {sid}")
UI/components/terminal_vwap_payoff_dark_panel.py:2032:            self._safe_status(f"Erro ao recalcular payoff: {exc}")
UI/components/terminal_vwap_payoff_dark_panel.py:2064:            self._safe_status(f"Erro ao arquivar estrutura: {exc}")
UI/components/terminal_vwap_payoff_dark_panel.py:2079:        status = str(structure.get("status") or "").strip().lower()
UI/components/terminal_vwap_payoff_dark_panel.py:2080:        return status in {
UI/components/terminal_vwap_payoff_dark_panel.py:2091:        self._safe_status(msg)
UI/components/terminal_vwap_payoff_dark_panel.py:2103:        self._safe_status("Arquivamento cancelado")
UI/components/terminal_vwap_payoff_dark_panel.py:2111:        self._safe_status(f"Estrutura arquivada: ID {sid}")
UI/components/terminal_vwap_payoff_dark_panel.py:2167:            self._safe_status(msg)
UI/components/terminal_vwap_payoff_dark_panel.py:2175:            self._safe_status("Encerramento cancelado")
UI/components/terminal_vwap_payoff_dark_panel.py:2187:            self._safe_status(f"Erro ao encerrar estrutura: {exc}")
UI/components/terminal_vwap_payoff_dark_panel.py:2198:        self._safe_status(msg)
UI/components/terminal_vwap_payoff_dark_panel.py:2216:            self._safe_status(f"Erro ao registrar decisao: {exc}")
UI/components/terminal_vwap_payoff_dark_panel.py:2221:        self._safe_status(msg)
UI/components/terminal_vwap_payoff_panel.py:166:        "status": _safe_text(structure.get("status")),
UI/components/terminal_vwap_payoff_panel.py:193:        on_status: Callable[[str], None] | None = None,
UI/components/terminal_vwap_payoff_panel.py:201:        self._on_status = on_status
UI/components/terminal_vwap_payoff_panel.py:225:        self._status_var = tk.StringVar(value="Terminal VWAP Payoff pronto")
UI/components/terminal_vwap_payoff_panel.py:228:            textvariable=self._status_var,
UI/components/terminal_vwap_payoff_panel.py:252:        columns = ("structure_id", "name", "underlying_asset", "status", "legs")
UI/components/terminal_vwap_payoff_panel.py:265:            "status": ("Status", 75, "center"),
UI/components/terminal_vwap_payoff_panel.py:320:                    ("status", "Status"),
UI/components/terminal_vwap_payoff_panel.py:448:            self._set_status(f"Erro ao listar estruturas: {exc}")
UI/components/terminal_vwap_payoff_panel.py:457:        self._set_status(f"{len(self._structures)} estruturas disponíveis no terminal")
UI/components/terminal_vwap_payoff_panel.py:462:            self._set_status("Selecione uma estrutura para carregar")
UI/components/terminal_vwap_payoff_panel.py:470:            self._set_status("Seleção inválida")
UI/components/terminal_vwap_payoff_panel.py:475:            self._set_status("Estrutura selecionada sem ID válido")
UI/components/terminal_vwap_payoff_panel.py:482:            self._set_status(f"Carregando estrutura {structure_id}...")
UI/components/terminal_vwap_payoff_panel.py:485:            self._set_status(f"Erro ao carregar estrutura {structure_id}: {exc}")
UI/components/terminal_vwap_payoff_panel.py:493:        self._set_status(f"Estrutura {structure_id} carregada no Terminal VWAP Payoff")
UI/components/terminal_vwap_payoff_panel.py:512:                    _safe_text(structure.get("status")),
UI/components/terminal_vwap_payoff_panel.py:575:    def _set_status(self, message: str) -> None:
UI/components/terminal_vwap_payoff_panel.py:576:        if hasattr(self, "_status_var"):
UI/components/terminal_vwap_payoff_panel.py:577:            self._status_var.set(message)
UI/components/terminal_vwap_payoff_panel.py:579:        if self._on_status is not None:
UI/components/terminal_vwap_payoff_panel.py:581:                self._on_status(message)
UI/main_window.py:118:        self.status_bar = ttk.Label(
UI/main_window.py:124:        self.status_bar.pack(side="bottom", fill="x")
UI/main_window.py:148:        # Menu Ajuda
UI/main_window.py:150:        menubar.add_cascade(label="Ajuda", menu=help_menu)
UI/main_window.py:164:        self.status_bar.config(text="Aplicando filtros...")
UI/main_window.py:169:            self.status_bar.config(text=f"{count} decisões encontradas")
UI/main_window.py:172:            self.status_bar.config(text="Erro nos filtros")
UI/main_window.py:197:            self.status_bar.config(text="Dados insuficientes para payoff")
UI/main_window.py:215:            self.status_bar.config(text="Carregando payoff... (cancelando anterior)")
UI/main_window.py:217:            self.status_bar.config(text="Carregando payoff...")
UI/main_window.py:278:        self.status_bar.config(text="Carregando dados...")
UI/main_window.py:332:            self.status_bar.config(
UI/main_window.py:338:            self.status_bar.config(text="Erro ao carregar dados")
UI/main_window.py:362:                self.status_bar.config(
UI/main_window.py:379:        self.status_bar.config(text=f"Recalculando {structure_id}...")
UI/main_window.py:384:                self.status_bar.config(text=msg)
UI/main_window.py:446:        self.status_bar.config(text="Executando pipeline...")
UI/main_window.py:486:            self.status_bar.config(text="Pipeline falhou")
UI/main_window.py:489:            self.status_bar.config(text="Erro ao executar pipeline")
UI/main_window.py:492:        """Verifica status dos bancos de dados."""
UI/main_window.py:494:            status = self.data_model.check_database_status()
UI/main_window.py:495:            messagebox.showinfo("Status dos Bancos", status)
UI/main_window.py:512:* Excel RTD  CSV Bridge
UI/main_window.py:563:                self.status_bar.config(text=msg)
UI/main_window.py:566:                self.status_bar.config(text="Sem dados de payoff para esta seleção")
UI/main_window.py:579:        self.status_bar.config(text=f"Erro ao carregar payoff: {error_msg}")
UI/main_window.py:596:            self.status_bar.config(text=f"{char} {base_text}")
UI/main_window.py:659:                f"Status     : {structure.get('status')}",
UI/main_window.py:690:                self.status_bar.config(text="Estrutura salva com sucesso.")
UI/main_window.py:729:                on_status=lambda msg: (
UI/main_window.py:730:                    self.status_bar.config(text=msg)
UI/main_window.py:731:                    if hasattr(self, "status_bar")
UI/models/ui_data.py:892:    def check_database_status(self) -> str:
UI/modern/dark_window.py:15:from rtd_bridge.excel_rtd_connection_status_presenter import get_excel_rtd_status_payload
UI/modern/dark_window.py:48:        self.status_var = tk.StringVar(value="Inicializando layout DARK...")
UI/modern/dark_window.py:63:        help_menu.add_command(label="Status RTD Excel", command=self._show_excel_rtd_status)
UI/modern/dark_window.py:68:        menu_bar.add_cascade(label="Ajuda", menu=help_menu)
UI/modern/dark_window.py:89:            on_status=self.set_status,
UI/modern/dark_window.py:96:            on_status=self.set_status,
UI/modern/dark_window.py:102:    def set_status(self, message: str) -> None:
UI/modern/dark_window.py:103:        self.status_var.set(message)
UI/modern/dark_window.py:119:                self.set_status("Dados recarregados")
UI/modern/dark_window.py:142:                    self.set_status(f"Erro ao recarregar estruturas para decisões: {exc}")
UI/modern/dark_window.py:150:            self.set_status(f"Erro ao obter estruturas para decisões: {exc}")
UI/modern/dark_window.py:168:                    self.set_status(
UI/modern/dark_window.py:195:                self.set_status(f"Estrutura {structure_id} não encontrada no Terminal VWAP")
UI/modern/dark_window.py:224:                self.set_status(f"Erro ao selecionar estrutura {structure_id}: {exc}")
UI/modern/dark_window.py:237:            self.set_status(f"Estrutura {structure_id} carregada a partir da decisão")
UI/modern/dark_window.py:240:            self.set_status(f"Erro ao carregar estrutura da decisão: {exc}")
UI/modern/dark_window.py:247:    def _show_excel_rtd_status(self) -> None:
UI/modern/dark_window.py:248:        """Exibe resumo operacional da conexão RTD/Excel."""
UI/modern/dark_window.py:249:        payload = get_excel_rtd_status_payload()
UI/modern/dark_window.py:250:        title = str(payload.get("title") or "Status RTD Excel")
UI/modern/dark_window.py:251:        message = _format_excel_rtd_status_message(payload)
UI/modern/dark_window.py:284:def _format_excel_rtd_status_message(payload: dict) -> str:
UI/modern/dark_window.py:285:    """Formata payload RTD/Excel para exibição amigável em messagebox."""
services/calculation_orchestrator.py:343:        if structure.get("status") == "archived":
services/canonical_pricing_facade.py:90:            # Formatos comuns vindos de RTD/planilha:
services/canonical_pricing_facade.py:394:                "status":          "ok",
services/canonical_pricing_facade.py:410:                    result={"engine": "stub", "status": "error", "error_message": error_message},
services/canonical_pricing_facade.py:418:                "status":          "error",
services/derived_payoff_persistence.py:37:        status = inner.get("status", "")
services/derived_payoff_persistence.py:38:        if status not in ("success", "ok", "completed"):
services/derived_payoff_persistence.py:40:                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
services/derived_payoff_persistence.py:41:                status,
services/derived_payoff_persistence.py:147:                    "execution_status": inner.get("status"),
services/derived_service.py:65:# Helpers internos
services/excel_rtd_com_access.py:7:EXCEL_PROG_ID = "Excel.Application"
services/excel_rtd_com_access.py:10:class ExcelComAccessError(RuntimeError):
services/excel_rtd_com_access.py:14:class ExcelComUnavailableError(ExcelComAccessError):
services/excel_rtd_com_access.py:22:        raise ExcelComUnavailableError(f"win32com indisponivel: {exc}") from exc
services/excel_rtd_com_access.py:33:        raise ExcelComAccessError(f"Excel ativo nao encontrado: {exc}") from exc
services/excel_rtd_reader.py:67:class ExcelRtdReadResult:
services/excel_rtd_reader.py:80:class ExcelRtdReaderError(RuntimeError):
services/excel_rtd_reader.py:160:    Escopo conservador: usado pelo leitor RTD Excel.
services/excel_rtd_reader.py:164:    - serial numerico Excel/COM -> DD-MM-YYYY
services/excel_rtd_reader.py:165:    - string numerica com serial Excel -> DD-MM-YYYY
services/excel_rtd_reader.py:178:        # Excel/COM usa base 1899-12-30.
services/excel_rtd_reader.py:287:        raise ExcelRtdReaderError(f"Nao foi possivel obter instancia ativa do Excel: {exc}") from exc
services/excel_rtd_reader.py:297:    raise ExcelRtdReaderError(
services/excel_rtd_reader.py:298:        f"Workbook '{workbook_name}' nao encontrado no Excel. "
services/excel_rtd_reader.py:310:    raise ExcelRtdReaderError(
services/excel_rtd_reader.py:374:) -> ExcelRtdReadResult:
services/excel_rtd_reader.py:386:            raise ExcelRtdReaderError("aba_sem_dados")
services/excel_rtd_reader.py:393:            return ExcelRtdReadResult(
services/excel_rtd_reader.py:413:        return ExcelRtdReadResult(
services/excel_rtd_reader.py:426:    except ExcelRtdReaderError as exc:
services/excel_rtd_reader.py:427:        return ExcelRtdReadResult(
services/excel_rtd_reader.py:441:def result_to_dict(result: ExcelRtdReadResult) -> Dict[str, Any]:
services/excel_rtd_workbook_probe.py:1:"""Probe controlado para diagnosticar o Excel RTD aberto.
services/excel_rtd_workbook_probe.py:3:Este modulo nao grava banco, nao altera UI e nao abre uma nova instancia do Excel.
services/excel_rtd_workbook_probe.py:4:A integracao real com COM fica isolada em Win32ExcelWorkbookAdapter.
services/excel_rtd_workbook_probe.py:7:- anexar ao Excel ja aberto;
services/excel_rtd_workbook_probe.py:8:- localizar LISTA_RTD.xlsm;
services/excel_rtd_workbook_probe.py:11:- retornar status estruturado e testavel.
services/excel_rtd_workbook_probe.py:26:class ExcelRtdProbeError(RuntimeError):
services/excel_rtd_workbook_probe.py:27:    """Erro controlado do probe Excel RTD."""
services/excel_rtd_workbook_probe.py:30:class ExcelWorkbookAdapter(Protocol):
services/excel_rtd_workbook_probe.py:31:    """Contrato minimo para permitir teste sem Excel real."""
services/excel_rtd_workbook_probe.py:34:        """Retorna workbooks abertos no Excel."""
services/excel_rtd_workbook_probe.py:48:class ExcelRtdWorkbookProbeConfig:
services/excel_rtd_workbook_probe.py:56:class ExcelRtdWorkbookProbeResult:
services/excel_rtd_workbook_probe.py:58:    status: str
services/excel_rtd_workbook_probe.py:72:class Win32ExcelWorkbookAdapter:
services/excel_rtd_workbook_probe.py:73:    """Adaptador COM para Excel ja aberto.
services/excel_rtd_workbook_probe.py:76:    escondida do Excel. Isso respeita a arquitetura da frente:
services/excel_rtd_workbook_probe.py:77:    corretora e Excel abertos antes do sistema.
services/excel_rtd_workbook_probe.py:84:            raise ExcelRtdProbeError(
services/excel_rtd_workbook_probe.py:85:                "Excel nao esta aberto ou nao esta acessivel via COM"
services/excel_rtd_workbook_probe.py:94:            raise ExcelRtdProbeError(f"falha ao listar workbooks: {exc}") from exc
services/excel_rtd_workbook_probe.py:169:        raise ExcelRtdProbeError(f"workbook nao encontrado pelo caminho: {workbook_full_name}")
services/excel_rtd_workbook_probe.py:172:class ExcelRtdWorkbookProbe:
services/excel_rtd_workbook_probe.py:173:    """Servico de diagnostico do workbook RTD aberto."""
services/excel_rtd_workbook_probe.py:178:        config: ExcelRtdWorkbookProbeConfig | None = None,
services/excel_rtd_workbook_probe.py:179:        adapter: ExcelWorkbookAdapter | None = None,
services/excel_rtd_workbook_probe.py:181:        self.config = config or ExcelRtdWorkbookProbeConfig()
services/excel_rtd_workbook_probe.py:184:    def run(self) -> ExcelRtdWorkbookProbeResult:
services/excel_rtd_workbook_probe.py:186:            adapter = self.adapter or Win32ExcelWorkbookAdapter()
services/excel_rtd_workbook_probe.py:188:        except ExcelRtdProbeError as exc:
services/excel_rtd_workbook_probe.py:189:            return ExcelRtdWorkbookProbeResult(
services/excel_rtd_workbook_probe.py:191:                status="excel_unavailable",
services/excel_rtd_workbook_probe.py:195:            return ExcelRtdWorkbookProbeResult(
services/excel_rtd_workbook_probe.py:197:                status="unexpected_error",
services/excel_rtd_workbook_probe.py:198:                message=f"erro inesperado no probe Excel RTD: {exc}",
services/excel_rtd_workbook_probe.py:209:            return ExcelRtdWorkbookProbeResult(
services/excel_rtd_workbook_probe.py:211:                status="workbook_not_found",
services/excel_rtd_workbook_probe.py:222:                f"aba RTD solicitada nao encontrada: {requested_sheet}"
services/excel_rtd_workbook_probe.py:227:            return ExcelRtdWorkbookProbeResult(
services/excel_rtd_workbook_probe.py:229:                status="sheet_not_found",
services/excel_rtd_workbook_probe.py:246:        except ExcelRtdProbeError as exc:
services/excel_rtd_workbook_probe.py:247:            return ExcelRtdWorkbookProbeResult(
services/excel_rtd_workbook_probe.py:249:                status="sheet_read_error",
services/excel_rtd_workbook_probe.py:259:            return ExcelRtdWorkbookProbeResult(
services/excel_rtd_workbook_probe.py:261:                status="sheet_read_error",
services/excel_rtd_workbook_probe.py:271:        return ExcelRtdWorkbookProbeResult(
services/excel_rtd_workbook_probe.py:273:            status="ok",
services/excel_rtd_workbook_probe.py:274:            message="workbook RTD localizado e amostra lida com sucesso",
services/excel_rtd_workbook_probe.py:317:    """Normaliza retorno COM do Excel para matriz de listas."""
services/legacy_robo_legs_fallback.py:138:        candidate_status_methods = [
services/legacy_robo_legs_fallback.py:139:            "status",
services/legacy_robo_legs_fallback.py:140:            "get_status",
services/legacy_robo_legs_fallback.py:143:        for method_name in candidate_status_methods:
services/legacy_robo_legs_fallback.py:147:                    status = method(aba=aba, requested_timestamp=reference_date)
services/legacy_robo_legs_fallback.py:150:                        status = method(aba, reference_date)
services/legacy_robo_legs_fallback.py:156:                chosen_ts = getattr(status, "chosen_ts", None)
services/legacy_robo_legs_fallback.py:160:                if isinstance(status, dict):
services/legacy_robo_legs_fallback.py:161:                    if status.get("chosen_ts") is not None:
services/legacy_robo_legs_fallback.py:162:                        return status.get("chosen_ts")
services/legacy_robo_legs_fallback.py:163:                    if status.get("timestamp") is not None:
services/legacy_robo_legs_fallback.py:164:                        return status.get("timestamp")
services/market_snapshot_selector.py:7:  - Caso contrário, se existir cotação em rtd_option_quotes para a leg RTD, usa rtd_option_quotes
services/market_snapshot_selector.py:19:RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
services/market_snapshot_selector.py:127:            source = RTD_OPTION_QUOTES_SOURCE
services/market_snapshot_selector.py:129:            source = SnapshotSource.RTD
services/pricing_engine_stub.py:18:            "status": "ok",
services/pricing_execution_app_service.py:67:        status = response.get("status")
services/pricing_execution_app_service.py:71:            status = inner_result.get("status", status)
services/pricing_execution_app_service.py:74:            status = execution_result.get("status", status)
services/pricing_execution_app_service.py:77:        if status == "error":
services/pricing_execution_app_service.py:96:        status: str | None = None,
services/pricing_execution_app_service.py:103:            status=status,
services/pricing_execution_app_service.py:112:        status: str | None = None,
services/pricing_execution_app_service.py:118:            status=status,
services/pricing_execution_app_service.py:129:        status: str | None = None,
services/pricing_execution_app_service.py:138:            status=status,
services/pricing_execution_orchestration_service.py:65:                    "status": "error",
services/pricing_execution_persistence_service.py:38:        execution_status = inner.get("status") if isinstance(inner, dict) else None
services/pricing_execution_persistence_service.py:49:            execution_status=execution_status,
services/pricing_execution_persistence_service.py:63:            execution_status=execution_status,
services/pricing_execution_persistence_service.py:98:        execution_status: str | None,
services/pricing_execution_persistence_service.py:106:        if execution_status != "ok":
services/pricing_execution_query_service.py:20:        status: str | None = None,
services/pricing_execution_query_service.py:29:        if status is not None and status not in {"ok", "error"}:
services/pricing_execution_query_service.py:30:            raise ValueError("status must be either 'ok' or 'error'")
services/pricing_execution_query_service.py:49:        status: str | None = None,
services/pricing_execution_query_service.py:61:                status=status,
services/pricing_execution_query_service.py:79:        status: str | None = None,
services/pricing_execution_query_service.py:86:            status=status,
services/pricing_execution_query_service.py:92:            status=status,
services/pricing_execution_query_service.py:114:                "execution_status": execution.get("execution_status"),
services/pricing_execution_query_service.py:141:            if status is not None and summary["execution_status"] != status:
services/pricing_execution_query_service.py:156:        status: str | None = None,
services/pricing_execution_query_service.py:165:            status=status,
services/pricing_execution_query_service.py:178:            status=status,
services/pricing_execution_query_service.py:204:        status: str | None = None,
services/pricing_execution_query_service.py:210:            status=status,
services/pricing_execution_query_service.py:217:            status=status,
services/robo_legs_status_service.py:5:patch_compat -- compatibilidade com status_repo.latest_timestamps(aba)
services/robo_legs_status_service.py:15:from dto.robo_legs_status_dto import DataFreshness, RoboLegsStatusDTO
services/robo_legs_status_service.py:17:from repositories.robo_legs_status_repository import (
services/robo_legs_status_service.py:34:        status_repo: Optional[RoboLegsStatusRepository] = None,
services/robo_legs_status_service.py:38:        self.status_repo = status_repo or RoboLegsStatusRepository(
services/robo_legs_status_service.py:43:    def status(
services/robo_legs_status_service.py:65:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(ref=ref)
services/robo_legs_status_service.py:69:            manual_latest, rtd_latest = self.status_repo.latest_timestamps(aba)
services/robo_legs_status_service.py:75:            chosen_fonte = FonteType.RTD
services/rtd_option_quotes_schema.py:7:DEFAULT_WORKBOOK_NAME = "LISTA_RTD.xlsm"
services/rtd_option_quotes_schema.py:8:DEFAULT_SHEET_NAME = "RTD_OPTION_QUOTES"
services/rtd_option_quotes_schema.py:11:RTD_OPTION_QUOTES_MAP: Dict[str, Dict[str, Optional[str]]] = {
services/rtd_option_quotes_schema.py:95:REQUIRED_OPTION_HEADERS = list(RTD_OPTION_QUOTES_MAP.keys())
services/structure_events_service.py:61:    def _validate_event_status(self, event_status: str) -> None:
services/structure_events_service.py:62:        if event_status not in self.ALLOWED_EVENT_STATUSES:
services/structure_events_service.py:64:            raise ValueError(f"event_status must be one of: {allowed}")
services/structure_events_service.py:114:        event_status: str = "registered",
services/structure_events_service.py:125:        self._validate_event_status(event_status)
services/structure_events_service.py:135:            "event_status": event_status,
services/structure_events_service.py:228:        event_status: str | None = None,
services/structure_events_service.py:238:        if event_status is not None:
services/structure_events_service.py:239:            self._validate_event_status(event_status)
services/structure_events_service.py:250:            event_status=event_status,
services/structure_events_service.py:341:            status = str(event.get("event_status", "registered")).strip().lower()
services/structure_events_service.py:343:            if status == "cancelled":
services/structure_events_service.py:428:        leg["operational_status"] = "closed" if quantity == 0 else "open"
services/structure_leg_rtd_enrichment_service.py:1:"""Service de enriquecimento de legs de estruturas via RTD.
services/structure_leg_rtd_enrichment_service.py:38:        Campos enriquecidos via RTD:
services/structure_leg_rtd_enrichment_service.py:49:            raise ValueError("symbol is required for RTD leg enrichment")
services/structure_leg_rtd_enrichment_service.py:123:                raise ValueError(f"missing required RTD field: {field}")
services/terminal_vwap_payoff_app_service.py:6:- não acessa Excel, RTD real ou UI pesada diretamente.
services/terminal_vwap_payoff_app_service.py:25:    diretamente a Excel, RTD, Tkinter ou banco em testes unitários.
services/terminal_vwap_payoff_viewmodel_service.py:6:- não acessa Excel;
services/terminal_vwap_payoff_viewmodel_service.py:7:- não acessa RTD real;
services/terminal_vwap_payoff_viewmodel_service.py:94:            "status": self._get(structure, "status", default=None),
services/terminal_vwap_payoff_viewmodel_service.py:188:            "status_vwap": "available" if vwap is not None else "unavailable",
```

## Persistência RTD option quotes

Comando:

```bash
git grep -n -E rtd_option_quotes|sync_rtd_option_quotes|upsert|insert|delete|SQLite|sqlite -- services repositories db ATT/tests/test_rtd_option_quotes_sync_service.py
```

Exit code: 0

Saída:

```text
ATT/tests/test_rtd_option_quotes_sync_service.py:1:import sqlite3
ATT/tests/test_rtd_option_quotes_sync_service.py:4:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
ATT/tests/test_rtd_option_quotes_sync_service.py:5:from services.rtd_option_quotes_sync_service import (
ATT/tests/test_rtd_option_quotes_sync_service.py:6:    sync_rtd_option_quotes_from_excel,
ATT/tests/test_rtd_option_quotes_sync_service.py:7:    sync_rtd_option_quotes_records,
ATT/tests/test_rtd_option_quotes_sync_service.py:11:def test_sync_records_upserts_one_snapshot_row_per_symbol(tmp_path: Path):
ATT/tests/test_rtd_option_quotes_sync_service.py:14:    first = sync_rtd_option_quotes_records(
ATT/tests/test_rtd_option_quotes_sync_service.py:41:    assert first.rows_upserted == 1
ATT/tests/test_rtd_option_quotes_sync_service.py:43:    second = sync_rtd_option_quotes_records(
ATT/tests/test_rtd_option_quotes_sync_service.py:70:    assert second.rows_upserted == 1
ATT/tests/test_rtd_option_quotes_sync_service.py:86:    with sqlite3.connect(str(db_path)) as conn:
ATT/tests/test_rtd_option_quotes_sync_service.py:90:            FROM rtd_option_quotes
ATT/tests/test_rtd_option_quotes_sync_service.py:124:    result = sync_rtd_option_quotes_from_excel(
ATT/tests/test_rtd_option_quotes_sync_service.py:131:    assert result.rows_upserted == 1
ATT/tests/test_rtd_option_quotes_sync_service.py:160:    result = sync_rtd_option_quotes_from_excel(
ATT/tests/test_rtd_option_quotes_sync_service.py:167:    assert result.rows_upserted == 0
db/config.py:4:import sqlite3
db/config.py:11:def connect_app() -> sqlite3.Connection:
db/config.py:13:    return sqlite3.connect(str(APP_DB_PATH))
db/derived_repo.py:26:import sqlite3
db/derived_repo.py:50:def get_app_db_connection() -> sqlite3.Connection:
db/derived_repo.py:71:def _table_columns(conn: sqlite3.Connection, table_name: str) -> List[str]:
db/derived_repo.py:176:def _apply_schema(conn: sqlite3.Connection) -> None:
db/derived_repo.py:189:            except sqlite3.OperationalError:
db/derived_repo.py:195:    except sqlite3.OperationalError:
db/derived_repo.py:210:def ensure_derived_tables(conn: sqlite3.Connection) -> None:
db/derived_repo.py:235:    def _connect(self) -> sqlite3.Connection:
db/derived_repo.py:236:        conn = sqlite3.connect(self._db_path)
db/derived_repo.py:237:        conn.row_factory = sqlite3.Row
db/derived_repo.py:307:            rowid = self._insert_decision(cur, ts, ab, decision_dict)
db/derived_repo.py:313:    def insert_structure_decision(
db/derived_repo.py:328:            rowid = self._insert_decision(cur, ts, ab, decision_dict, replace=True)
db/derived_repo.py:388:    def insert_payoff_points(
db/derived_repo.py:483:            decision_id = self._insert_decision(cur, ts, ab, decision_dict)
db/derived_repo.py:641:    def _insert_decision(
db/derived_repo.py:643:        cur: sqlite3.Cursor,
db/derived_repo.py:683:    conn: sqlite3.Connection,
db/derived_repo.py:723:    conn: sqlite3.Connection,
db/derived_repo.py:760:    conn: sqlite3.Connection,
db/derived_repo.py:775:def insert_payoff_points(
db/derived_repo.py:776:    conn: sqlite3.Connection,
db/derived_repo.py:813:def insert_structure_decision(
db/derived_repo.py:814:    conn: sqlite3.Connection,
db/derived_repo.py:848:    conn: sqlite3.Connection,
db/derived_repo.py:881:def validate_snapshot_consistency(conn: sqlite3.Connection) -> bool:
db/derived_repo.py:911:def cleanup_old_payoff_data(conn: sqlite3.Connection, days_to_keep: int = 30) -> int:
db/derived_repo.py:918:    deleted = cur.rowcount
db/derived_repo.py:920:    return deleted
db/derived_repo.py:923:def cleanup_old_decisions(conn: sqlite3.Connection, days_to_keep: int = 30) -> int:
db/derived_repo.py:930:    deleted = cur.rowcount
db/derived_repo.py:932:    return deleted
db/import_excel.py:4:from db.sqlite import connect
db/import_excel.py:77:    # mantém só colunas que existem no SQLite
db/init_db.py:2:from db.sqlite import connect
db/init_excel_schema.py:3:from db.sqlite import connect
db/migrations/add_structure_id_to_payoff_curve_points.py:11:import sqlite3
db/migrations/add_structure_id_to_payoff_curve_points.py:75:def col_exists(conn: sqlite3.Connection, table: str, col: str) -> bool:
db/migrations/add_structure_id_to_payoff_curve_points.py:85:    conn = sqlite3.connect(str(db_path))
db/reader.py:3:Reader para análise de dados consolidados do SQLite.
db/reader.py:6:import sqlite3
db/reader.py:22:        conn = sqlite3.connect(self.db_path)
db/reader.py:23:        conn.row_factory = sqlite3.Row
db/schema.py:113:    Espera receber uma conexão sqlite3 já aberta (padrão comum no restante do projeto).
db/sqlite.py:1:# db/sqlite.py
db/sqlite.py:2:import sqlite3
db/sqlite.py:9:    conn = sqlite3.connect(db_path)
db/sqlite.py:10:    conn.row_factory = sqlite3.Row
db/writer.py:3:Writer para persistência de dados consolidados no SQLite.
db/writer.py:6:import sqlite3
db/writer.py:24:        with sqlite3.connect(self.db_path) as conn:
db/writer.py:54:        with sqlite3.connect(self.db_path) as conn:
db/writer.py:125:        with sqlite3.connect(self.db_path) as conn:
db/writer.py:126:            conn.row_factory = sqlite3.Row
db/writer.py:141:        with sqlite3.connect(self.db_path) as conn:
db/writer.py:142:            conn.row_factory = sqlite3.Row
repositories/_aba_resolver_mixin.py:13:a conexão desejada (ex: sqlite3 in-memory).
repositories/_aba_resolver_mixin.py:41:        Implementação padrão usa sqlite_conn(self.config.app_db_path).
repositories/_aba_resolver_mixin.py:44:        from infra.sqlite_conn import sqlite_conn
repositories/_aba_resolver_mixin.py:45:        return sqlite_conn(self.config.app_db_path)
repositories/market_snapshot_repository.py:6:(rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
repositories/market_snapshot_repository.py:11:import sqlite3
repositories/market_snapshot_repository.py:28:RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
repositories/market_snapshot_repository.py:160:def _row_to_leg(row: sqlite3.Row, source: SnapshotSource) -> LegMarketSnapshot:
repositories/market_snapshot_repository.py:193:    quote_row: sqlite3.Row,
repositories/market_snapshot_repository.py:196:    Converte uma cotação de rtd_option_quotes em LegMarketSnapshot mantendo
repositories/market_snapshot_repository.py:199:    A tabela rtd_option_quotes é cache de cotação. Ela não define composição
repositories/market_snapshot_repository.py:255:      get_rtd_option_quote_legs(aba)   -> lista enriquecida source=rtd_option_quotes
repositories/market_snapshot_repository.py:266:    def _connect(self) -> sqlite3.Connection:
repositories/market_snapshot_repository.py:267:        conn = sqlite3.connect(str(self._db_path))
repositories/market_snapshot_repository.py:268:        conn.row_factory = sqlite3.Row
repositories/market_snapshot_repository.py:281:        Retorna legs RTD enriquecidas com rtd_option_quotes.
repositories/market_snapshot_repository.py:284:        dessa composição, se houver cotação em rtd_option_quotes.codigo_opcao,
repositories/market_snapshot_repository.py:321:            FROM rtd_option_quotes
repositories/market_snapshot_repository.py:329:        except sqlite3.OperationalError:
repositories/market_snapshot_repository.py:330:            # Banco sem tabela rtd_option_quotes: mantém compatibilidade com
repositories/market_snapshot_repository.py:334:        quote_by_codigo: dict[str, sqlite3.Row] = {}
repositories/pricing_executions_repository.py:2:import sqlite3
repositories/pricing_executions_repository.py:20:    def _connect(self) -> sqlite3.Connection:
repositories/pricing_executions_repository.py:21:        conn = sqlite3.connect(str(self._db_path))
repositories/pricing_executions_repository.py:22:        conn.row_factory = sqlite3.Row
repositories/pricing_executions_repository.py:228:        """Converte sqlite3.Row *ou* tupla para dict de forma segura."""
repositories/pricing_executions_repository.py:229:        if isinstance(row, sqlite3.Row):
repositories/robo_legs_repository.py:15:from infra.sqlite_conn import sqlite_conn
repositories/robo_legs_repository.py:94:        with sqlite_conn(self.config.app_db_path) as conn:
repositories/robo_legs_repository.py:106:        with sqlite_conn(self.config.app_db_path) as conn:
repositories/robo_legs_repository.py:149:        with sqlite_conn(self.config.app_db_path) as conn:
repositories/robo_legs_status_repository.py:13:from infra.sqlite_conn import sqlite_conn
repositories/robo_legs_status_repository.py:51:        with sqlite_conn(self.config.app_db_path) as conn:
repositories/rtd_option_quotes_repository.py:1:# repositories/rtd_option_quotes_repository.py
repositories/rtd_option_quotes_repository.py:8:import sqlite3
repositories/rtd_option_quotes_repository.py:12:from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema
repositories/rtd_option_quotes_repository.py:59:    - tabela rtd_option_quotes
repositories/rtd_option_quotes_repository.py:69:    def _connect(self) -> sqlite3.Connection:
repositories/rtd_option_quotes_repository.py:70:        conn = sqlite3.connect(str(self.db_path))
repositories/rtd_option_quotes_repository.py:71:        conn.row_factory = sqlite3.Row
repositories/rtd_option_quotes_repository.py:75:        ensure_rtd_option_quotes_schema(self.db_path)
repositories/rtd_option_quotes_repository.py:81:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:96:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:110:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:119:    def upsert_many(
repositories/rtd_option_quotes_repository.py:170:        insert_columns = [
repositories/rtd_option_quotes_repository.py:177:            UPDATE rtd_option_quotes
repositories/rtd_option_quotes_repository.py:183:        insert_sql = f"""
repositories/rtd_option_quotes_repository.py:184:            INSERT INTO rtd_option_quotes (
repositories/rtd_option_quotes_repository.py:185:                {", ".join(insert_columns)}
repositories/rtd_option_quotes_repository.py:188:                {", ".join("?" for _ in insert_columns)}
repositories/rtd_option_quotes_repository.py:200:                    insert_values = [row[column] for column in insert_columns]
repositories/rtd_option_quotes_repository.py:201:                    conn.execute(insert_sql, insert_values)
repositories/structure_events_repository.py:21:import sqlite3
repositories/structure_events_repository.py:178:    def _connect(self) -> sqlite3.Connection:
repositories/structure_events_repository.py:182:        conn = sqlite3.connect(str(db_path))
repositories/structure_events_repository.py:183:        conn.row_factory = sqlite3.Row
repositories/structure_events_repository.py:196:    def ensure_schema_on_connection(conn: sqlite3.Connection) -> None:
repositories/structure_events_repository.py:261:    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
repositories/structure_events_repository.py:270:    def _ensure_structure_exists(conn: sqlite3.Connection, structure_id: int) -> None:
repositories/structure_events_repository.py:280:        conn: sqlite3.Connection,
repositories/structures_repository.py:5:alteracao_11: conexões SQLite fechadas explicitamente via try/finally.
repositories/structures_repository.py:18:import sqlite3
repositories/structures_repository.py:178:    def _connect(self) -> sqlite3.Connection:
repositories/structures_repository.py:182:        conn = sqlite3.connect(str(db_path))
repositories/structures_repository.py:183:        conn.row_factory = sqlite3.Row
repositories/structures_repository.py:188:    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
repositories/structures_repository.py:194:        self, conn: sqlite3.Connection, structure_id: int
repositories/structures_repository.py:211:        self, conn: sqlite3.Connection, structure_id: int
repositories/structures_repository.py:224:    def ensure_audit_schema(self, conn: sqlite3.Connection) -> None:
repositories/structures_repository.py:266:        conn: sqlite3.Connection,
repositories/structures_repository.py:547:    # ARCHIVE (soft-delete)
repositories/system_snapshots_repository.py:4:import sqlite3
repositories/system_snapshots_repository.py:61:def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
repositories/system_snapshots_repository.py:72:    def _connect(self) -> sqlite3.Connection:
repositories/system_snapshots_repository.py:73:        conn = sqlite3.connect(self.db_path)
repositories/system_snapshots_repository.py:74:        conn.row_factory = sqlite3.Row
repositories/system_snapshots_repository.py:150:                self._insert_leg_snapshot(
repositories/system_snapshots_repository.py:160:    def _insert_leg_snapshot(
repositories/system_snapshots_repository.py:163:        conn: sqlite3.Connection,
repositories/system_snapshots_repository.py:279:    def _decode_snapshot_row(self, row: sqlite3.Row) -> dict[str, Any]:
repositories/system_snapshots_repository.py:287:    def _decode_leg_row(self, row: sqlite3.Row) -> dict[str, Any]:
services/canonical_pricing_facade.py:26:import sqlite3
services/canonical_pricing_facade.py:52:    with sqlite3.connect(str(db_path)) as conn:
services/canonical_pricing_facade.py:53:        conn.row_factory = sqlite3.Row
services/canonical_pricing_facade.py:181:        with sqlite3.connect(str(db_path)) as conn:
services/canonical_pricing_facade.py:183:                "SELECT name FROM sqlite_master WHERE type = 'table'"
services/derived_service.py:11:import sqlite3
services/derived_service.py:20:    insert_payoff_points,
services/derived_service.py:21:    insert_structure_decision,
services/derived_service.py:199:        return insert_payoff_points(
services/derived_service.py:296:        return insert_structure_decision(
services/derived_service.py:353:        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
services/derived_service.py:354:        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
services/derived_service.py:355:        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
services/derived_service.py:413:        conn.row_factory = sqlite3.Row
services/excel_rtd_reader.py:13:from services.rtd_option_quotes_schema import (
services/excel_rtd_workbook_probe.py:20:from services.rtd_option_quotes_schema import DEFAULT_WORKBOOK_NAME
services/market_snapshot_selector.py:3:Política de precedência de snapshots: manual > rtd_option_quotes > rtd.
services/market_snapshot_selector.py:7:  - Caso contrário, se existir cotação em rtd_option_quotes para a leg RTD, usa rtd_option_quotes
services/market_snapshot_selector.py:19:RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"
services/market_snapshot_selector.py:47:    Aplica a política manual > rtd_option_quotes > rtd para selecionar o snapshot canônico.
services/rtd_option_quotes_sync_service.py:7:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
services/rtd_option_quotes_sync_service.py:19:    rows_upserted: int
services/rtd_option_quotes_sync_service.py:31:def sync_rtd_option_quotes_records(
services/rtd_option_quotes_sync_service.py:41:        rows_upserted = repo.upsert_many(
services/rtd_option_quotes_sync_service.py:50:            rows_upserted=0,
services/rtd_option_quotes_sync_service.py:59:        rows_upserted=rows_upserted,
services/rtd_option_quotes_sync_service.py:65:def sync_rtd_option_quotes_from_excel(
services/rtd_option_quotes_sync_service.py:83:            rows_upserted=0,
services/rtd_option_quotes_sync_service.py:100:            rows_upserted=0,
services/rtd_option_quotes_sync_service.py:109:    sync_result = sync_rtd_option_quotes_records(
services/rtd_option_quotes_sync_service.py:119:        rows_upserted=sync_result.rows_upserted,
services/structure_leg_rtd_enrichment_service.py:5:- consultar rtd_option_quotes por codigo_opcao;
services/structure_leg_rtd_enrichment_service.py:19:    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""
services/structure_leg_rtd_enrichment_service.py:21:    def __init__(self, rtd_option_quotes_repository: Any) -> None:
services/structure_leg_rtd_enrichment_service.py:22:        self._repo = rtd_option_quotes_repository
```

## Subprocess operacional suspeito em UI

Comando:

```bash
git grep -n -E subprocess|Popen|refresh_rtd|rtd|RTD|Preencher|preencher -- UI/main_window.py UI/components/structure_editor_dialog.py scripts/refresh_rtd_symbol_to_option_quotes.py scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
```

Exit code: 0

Saída:

```text
UI/components/structure_editor_dialog.py:4:import subprocess
UI/components/structure_editor_dialog.py:43:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
UI/components/structure_editor_dialog.py:44:from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
UI/components/structure_editor_dialog.py:76:        _rtd_leg_enrichment_service=None,    # <-- injecao opcional para testes/UI
UI/components/structure_editor_dialog.py:91:        self._rtd_leg_enrichment_service = _rtd_leg_enrichment_service
UI/components/structure_editor_dialog.py:247:            text="[RTD] Preencher por Simbolo",
UI/components/structure_editor_dialog.py:248:            command=self._cmd_fill_leg_from_rtd,
UI/components/structure_editor_dialog.py:411:    def _refresh_rtd_symbol_on_demand(self, codigo_opcao: str) -> tuple[bool, str]:
UI/components/structure_editor_dialog.py:412:        """Atualiza uma opcao via RTD/Excel e grava o cache em dados/app.db."""
UI/components/structure_editor_dialog.py:419:        script_path = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
UI/components/structure_editor_dialog.py:423:            return False, f"Script RTD nao encontrado: {script_path}"
UI/components/structure_editor_dialog.py:438:            completed = subprocess.run(
UI/components/structure_editor_dialog.py:448:        except subprocess.TimeoutExpired:
UI/components/structure_editor_dialog.py:449:            return False, f"Timeout ao atualizar RTD para {symbol}."
UI/components/structure_editor_dialog.py:456:            return False, f"Falha ao atualizar RTD para {symbol}: {detail}"
UI/components/structure_editor_dialog.py:461:            return False, f"RTD atualizou, mas retornou JSON invalido: {stdout[:500]}"
UI/components/structure_editor_dialog.py:465:            return False, f"RTD retornou erro para {symbol}: {errors}"
UI/components/structure_editor_dialog.py:470:            return False, f"RTD executou, mas nao retornou cotacao para {symbol}."
UI/components/structure_editor_dialog.py:474:    def _get_rtd_leg_enrichment_service(self):
UI/components/structure_editor_dialog.py:475:        """Cria/lazily retorna o service de preenchimento de leg via RTD."""
UI/components/structure_editor_dialog.py:476:        if self._rtd_leg_enrichment_service is None:
UI/components/structure_editor_dialog.py:478:            rtd_db_path = project_root / "dados" / "app.db"
UI/components/structure_editor_dialog.py:479:            rtd_repo = RtdOptionQuotesRepository(rtd_db_path)
UI/components/structure_editor_dialog.py:480:            self._rtd_leg_enrichment_service = StructureLegRtdEnrichmentService(
UI/components/structure_editor_dialog.py:481:                rtd_repo
UI/components/structure_editor_dialog.py:483:        return self._rtd_leg_enrichment_service
UI/components/structure_editor_dialog.py:499:    def _cmd_fill_leg_from_rtd(self):
UI/components/structure_editor_dialog.py:500:        """Preenche a leg selecionada usando rtd_option_quotes.codigo_opcao."""
UI/components/structure_editor_dialog.py:504:                "Preencher via RTD",
UI/components/structure_editor_dialog.py:513:                "Preencher via RTD",
UI/components/structure_editor_dialog.py:514:                "Informe o campo 'Simbolo' antes de consultar o RTD.",
UI/components/structure_editor_dialog.py:529:            ok, message = self._refresh_rtd_symbol_on_demand(symbol)
UI/components/structure_editor_dialog.py:533:                    "Preencher via RTD",
UI/components/structure_editor_dialog.py:539:            enriched = self._get_rtd_leg_enrichment_service().enrich(leg_data)
UI/components/structure_editor_dialog.py:542:                "Preencher via RTD",
UI/components/structure_editor_dialog.py:543:                f"Nao foi possivel preencher a leg pelo RTD:\n{exc}",
UI/main_window.py:376:        import subprocess
UI/main_window.py:404:                res = subprocess.run(
UI/main_window.py:423:            except subprocess.TimeoutExpired:
UI/main_window.py:425:            except subprocess.CalledProcessError as e:
UI/main_window.py:459:            import subprocess
UI/main_window.py:462:            res = subprocess.run(
UI/main_window.py:478:        except subprocess.CalledProcessError as e:
UI/main_window.py:512:* Excel RTD  CSV Bridge
scripts/refresh_rtd_symbol_to_option_quotes.py:3:Atualiza uma opção avulsa via RTD Excel e importa para rtd_option_quotes.
scripts/refresh_rtd_symbol_to_option_quotes.py:6:    symbol -> arquivo temporário de símbolos -> refresh_rtd_option_quotes_excel.ps1
scripts/refresh_rtd_symbol_to_option_quotes.py:7:    -> CSV temporário -> import_rtd_option_quotes_wide_csv.py -> SQLite
scripts/refresh_rtd_symbol_to_option_quotes.py:10:    python scripts/refresh_rtd_symbol_to_option_quotes.py --symbol PETRS424 --db dados/app.db --visible --json
scripts/refresh_rtd_symbol_to_option_quotes.py:18:import subprocess
scripts/refresh_rtd_symbol_to_option_quotes.py:26:PS1_SCRIPT = PROJECT_ROOT / "scripts" / "refresh_rtd_option_quotes_excel.ps1"
scripts/refresh_rtd_symbol_to_option_quotes.py:27:IMPORT_SCRIPT = PROJECT_ROOT / "scripts" / "import_rtd_option_quotes_wide_csv.py"
scripts/refresh_rtd_symbol_to_option_quotes.py:32:        completed = subprocess.run(
scripts/refresh_rtd_symbol_to_option_quotes.py:42:    except subprocess.TimeoutExpired as exc:
scripts/refresh_rtd_symbol_to_option_quotes.py:87:            FROM rtd_option_quotes
scripts/refresh_rtd_symbol_to_option_quotes.py:103:        description="Atualiza uma opção avulsa via RTD Excel e importa para rtd_option_quotes."
scripts/refresh_rtd_symbol_to_option_quotes.py:120:        default="LISTA_RTD.xlsm",
scripts/refresh_rtd_symbol_to_option_quotes.py:121:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/refresh_rtd_symbol_to_option_quotes.py:128:        help="Timeout/espera do RTD. Padrão: 10.",
scripts/refresh_rtd_symbol_to_option_quotes.py:177:    symbols_path = tmp_dir / f"rtd_symbols_probe_{symbol}.txt"
scripts/refresh_rtd_symbol_to_option_quotes.py:178:    csv_path = tmp_dir / f"RTD_LINKS_probe_{symbol}.csv"
scripts/refresh_rtd_symbol_to_option_quotes.py:287:            print("Refresh RTD symbol -> rtd_option_quotes")
scripts/refresh_rtd_symbol_to_option_quotes.py:312:        print("Refresh RTD symbol -> rtd_option_quotes")
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:4:import subprocess
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:10:BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:60:    cp = subprocess.run(
```

## Bridge legado isolado

Comando:

```bash
git grep -n -E RtdOptionQuotesBridge|DispatchEx|fetch_quotes|excel_rtd_option_quotes_bridge -- rtd_bridge ATT/tests/test_rtd_option_quotes_bridge.py
```

Exit code: 0

Saída:

```text
ATT/tests/test_rtd_option_quotes_bridge.py:15:from rtd_bridge.excel_rtd_option_quotes_bridge import RtdOptionQuotesBridge
ATT/tests/test_rtd_option_quotes_bridge.py:79:        bridge = RtdOptionQuotesBridge(
ATT/tests/test_rtd_option_quotes_bridge.py:85:        result = bridge.fetch_quotes(args.codes)
rtd_bridge/excel_rtd_option_quotes_bridge.py:4:- Usa DispatchEx para abrir uma instancia isolada do Excel.
rtd_bridge/excel_rtd_option_quotes_bridge.py:113:class RtdOptionQuotesBridge:
rtd_bridge/excel_rtd_option_quotes_bridge.py:132:    def fetch_quotes(self, option_codes: Sequence[str]) -> RtdOptionQuotesResult:
rtd_bridge/excel_rtd_option_quotes_bridge.py:149:            excel = win32com.client.DispatchEx("Excel.Application")
```

## Testes focados da Fase 1

Comando:

```bash
python -m pytest ATT/tests/test_excel_rtd_connection_status.py ATT/tests/test_excel_rtd_connection_status_presenter.py ATT/tests/test_excel_rtd_reader.py ATT/tests/test_excel_rtd_workbook_probe_contract.py ATT/tests/test_rtd_option_quotes_sync_service.py ATT/tests/test_rtd_option_quotes_bridge.py ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py -q
```

Exit code: 0

Saída:

```text
......................                                                   [100%]
22 passed in 2.32s
```

## Parecer preliminar automático

Este relatório não encerra a fase automaticamente. Ele reúne evidências para decidir se a Fase 1 pode ser encerrada ou se ainda há subprocesso operacional/ponte legada a remover.

