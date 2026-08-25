
# [FRENTE 34] BEGIN rtd bridge option quotes parser bridge contract
# Ponte contratual local para os parsers canonicos de normalizacao.
#
# Objetivo:
# - declarar que este bridge RTD de option quotes deve convergir, em frentes futuras,
#   para os contratos publicos de utils.number_parser e utils.date_parser;
# - reduzir duplicacao futura de parsing numerico e parsing de datas nos fluxos RTD;
# - preservar integralmente o comportamento operacional atual nesta frente.
#
# Contratos canonicos referenciados:
# - utils.number_parser.parse_float_br
# - utils.number_parser.parse_optional_float
# - utils.number_parser.parse_positive_float
# - utils.number_parser.parse_percent
# - utils.date_parser.parse_excel_date_to_iso
# - utils.date_parser.parse_datetime_to_iso
#
# Regras preservadas nesta frente:
# - sem troca de persistencia;
# - sem troca de schema;
# - sem alteracao operacional do bridge RTD;
# - sem alteracao operacional do sync RTD;
# - option_type canonico somente CALL/PUT por extenso;
# - C/V permanecem apenas como compra/venda legado.
# [FRENTE 34] END rtd bridge option quotes parser bridge contract

"""Bridge legado/manual para criar instancia isolada do Excel e consultar RTD.

Atencao:
- Usa DispatchEx para abrir uma instancia isolada do Excel.
- Abre e fecha o workbook informado.
- Nao deve ser usado pelo fluxo operacional principal da UI/status/sync.
- O fluxo principal deve usar services.excel_rtd_com_access e services.excel_rtd_reader.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from typing import Any, Dict, List, Optional, Sequence

from services.rtd_option_quotes_schema import (
    DEFAULT_SHEET_NAME,
    REQUIRED_OPTION_HEADERS,
    RTD_OPTION_QUOTES_MAP,
    normalize_header,
)

RTD_OPTION_QUOTES_SHEET = DEFAULT_SHEET_NAME
REQUIRED_RTD_OPTION_HEADERS = REQUIRED_OPTION_HEADERS


XL_TO_LEFT = -4159
XL_UP = -4162
class RtdBridgeError(Exception):
    pass


class MissingHeaderError(RtdBridgeError):
    pass


@dataclass
class RtdOptionQuotesResult:
    rows: List[Dict[str, Any]]
    headers_map: Dict[str, int]
    elapsed_seconds: float
def column_letter(column_number: int) -> str:
    if column_number <= 0:
        raise ValueError("Número de coluna inválido.")

    result = ""

    while column_number:
        column_number, remainder = divmod(column_number - 1, 26)
        result = chr(65 + remainder) + result

    return result


def excel_serial_to_date(value: float) -> date:
    base = datetime(1899, 12, 30)
    converted = base + timedelta(days=float(value))
    return converted.date()


def convert_value(field_name: str, value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, str):
        cleaned = value.strip()

        if cleaned == "":
            return None

        return cleaned

    if field_name == "vencimento":
        if hasattr(value, "date"):
            try:
                return value.date().isoformat()
            except Exception:
                return str(value)

        if isinstance(value, (int, float)):
            try:
                return excel_serial_to_date(value).isoformat()
            except Exception:
                return value

    if field_name in {"ultima_quantidade", "volume"}:
        if isinstance(value, (int, float)):
            return int(value)

    if field_name in {
        "strike",
        "ultimo_preco",
        "bid",
        "ask",
        "iv",
        "delta",
        "gamma",
        "theta",
        "vega",
        "vwap",
    }:
        if isinstance(value, (int, float)):
            return float(value)

    return value


def build_rtd_formula(rtd_function: str, input_column_letter: str, row_number: int) -> str:
    return '=RTD("btg_pro_rtd";"";"' + rtd_function + '";$' + input_column_letter + str(row_number) + ")"


class RtdOptionQuotesBridge:
    def __init__(
        self,
        workbook_path: str,
        sheet_name: str = RTD_OPTION_QUOTES_SHEET,
        visible: bool = False,
        display_alerts: bool = False,
        start_row: int = 2,
        rtd_wait_seconds: float = 2.0,
        rtd_timeout_seconds: float = 20.0,
    ) -> None:
        self.workbook_path = workbook_path
        self.sheet_name = sheet_name
        self.visible = visible
        self.display_alerts = display_alerts
        self.start_row = start_row
        self.rtd_wait_seconds = rtd_wait_seconds
        self.rtd_timeout_seconds = rtd_timeout_seconds

    def fetch_quotes(self, option_codes: Sequence[str]) -> RtdOptionQuotesResult:
        clean_codes = self._normalize_option_codes(option_codes)

        if not clean_codes:
            return RtdOptionQuotesResult(rows=[], headers_map={}, elapsed_seconds=0.0)

        started_at = time.time()

        excel = None
        workbook = None

        try:
            import pythoncom
            import win32com.client

            pythoncom.CoInitialize()

            excel = win32com.client.DispatchEx("Excel.Application")
            excel.Visible = self.visible
            excel.DisplayAlerts = self.display_alerts
            excel.EnableEvents = True

            workbook = excel.Workbooks.Open(self.workbook_path)
            sheet = workbook.Worksheets(self.sheet_name)

            headers_map = self.read_headers_map(sheet)
            self.validate_required_headers(headers_map)

            self.clear_request_area(
                sheet=sheet,
                headers_map=headers_map,
                request_rows=len(clean_codes),
            )

            self.inject_option_codes(
                sheet=sheet,
                headers_map=headers_map,
                option_codes=clean_codes,
            )

            self.apply_rtd_formulas(
                sheet=sheet,
                headers_map=headers_map,
                row_count=len(clean_codes),
            )

            self.wait_rtd_refresh(
                excel=excel,
                sheet=sheet,
                headers_map=headers_map,
                row_count=len(clean_codes),
            )

            rows = self.read_option_quote_rows(
                sheet=sheet,
                headers_map=headers_map,
                row_count=len(clean_codes),
            )

            elapsed = time.time() - started_at

            return RtdOptionQuotesResult(
                rows=rows,
                headers_map=headers_map,
                elapsed_seconds=elapsed,
            )

        finally:
            if workbook is not None:
                workbook.Close(SaveChanges=False)

            if excel is not None:
                excel.DisplayAlerts = False
                excel.Quit()

            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

    def read_headers_map(self, sheet: Any, header_row: int = 1) -> Dict[str, int]:
        last_column = sheet.Cells(header_row, sheet.Columns.Count).End(XL_TO_LEFT).Column
        headers_map: Dict[str, int] = {}

        for column in range(1, last_column + 1):
            raw_value = sheet.Cells(header_row, column).Value
            header = normalize_header(raw_value)

            if not header:
                continue

            if header in headers_map:
                raise RtdBridgeError(
                    "Cabeçalho duplicado na aba "
                    + self.sheet_name
                    + ": "
                    + header
                )

            headers_map[header] = column

        return headers_map

    def validate_required_headers(self, headers_map: Dict[str, int]) -> None:
        missing = [
            header
            for header in REQUIRED_RTD_OPTION_HEADERS
            if header not in headers_map
        ]

        if missing:
            raise MissingHeaderError(
                "Cabeçalho obrigatório ausente na aba "
                + self.sheet_name
                + ": "
                + ", ".join(missing)
            )

    def clear_request_area(
        self,
        sheet: Any,
        headers_map: Dict[str, int],
        request_rows: int,
        extra_rows: int = 20,
    ) -> None:
        input_column = headers_map["codigo_opcao"]

        last_used_row = sheet.Cells(sheet.Rows.Count, input_column).End(XL_UP).Row

        if last_used_row < self.start_row:
            last_used_row = self.start_row

        end_row = max(
            last_used_row,
            self.start_row + request_rows + extra_rows - 1,
        )

        for column in headers_map.values():
            sheet.Range(
                sheet.Cells(self.start_row, column),
                sheet.Cells(end_row, column),
            ).ClearContents()

    def inject_option_codes(
        self,
        sheet: Any,
        headers_map: Dict[str, int],
        option_codes: Sequence[str],
    ) -> None:
        input_column = headers_map["codigo_opcao"]

        for index, option_code in enumerate(option_codes):
            row_number = self.start_row + index
            sheet.Cells(row_number, input_column).Value = option_code

    def apply_rtd_formulas(
        self,
        sheet: Any,
        headers_map: Dict[str, int],
        row_count: int,
    ) -> None:
        input_column = headers_map["codigo_opcao"]
        input_column_letter = column_letter(input_column)

        for index in range(row_count):
            row_number = self.start_row + index

            for field_name, config in RTD_OPTION_QUOTES_MAP.items():
                if config["role"] != "rtd":
                    continue

                rtd_function = config["rtd"]

                if not rtd_function:
                    continue

                output_column = headers_map[field_name]
                formula = build_rtd_formula(
                    rtd_function=rtd_function,
                    input_column_letter=input_column_letter,
                    row_number=row_number,
                )

                sheet.Cells(row_number, output_column).FormulaLocal = formula

    def wait_rtd_refresh(
        self,
        excel: Any,
        sheet: Any,
        headers_map: Dict[str, int],
        row_count: int,
    ) -> None:
        time.sleep(self.rtd_wait_seconds)

        deadline = time.time() + self.rtd_timeout_seconds

        while time.time() < deadline:
            try:
                excel.CalculateUntilAsyncQueriesDone()
            except Exception:
                pass

            if self._has_basic_rtd_values(
                sheet=sheet,
                headers_map=headers_map,
                row_count=row_count,
            ):
                return

            time.sleep(0.5)

    def read_option_quote_rows(
        self,
        sheet: Any,
        headers_map: Dict[str, int],
        row_count: int,
    ) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []

        for index in range(row_count):
            row_number = self.start_row + index
            row_data: Dict[str, Any] = {}

            for field_name in REQUIRED_RTD_OPTION_HEADERS:
                column = headers_map[field_name]
                raw_value = sheet.Cells(row_number, column).Value
                row_data[field_name] = convert_value(field_name, raw_value)

            rows.append(row_data)

        return rows

    def _has_basic_rtd_values(
        self,
        sheet: Any,
        headers_map: Dict[str, int],
        row_count: int,
    ) -> bool:
        field_name = "ativo_base"

        if field_name not in headers_map:
            return False

        column = headers_map[field_name]

        for index in range(row_count):
            row_number = self.start_row + index
            value = sheet.Cells(row_number, column).Value

            if value is None:
                return False

            if isinstance(value, str) and value.strip() == "":
                return False

        return True

    def _normalize_option_codes(self, option_codes: Sequence[str]) -> List[str]:
        result: List[str] = []

        for option_code in option_codes:
            if option_code is None:
                continue

            cleaned = str(option_code).strip().upper()

            if cleaned:
                result.append(cleaned)

        return result


# --- INICIO FRENTE 23 RTD BRIDGE SCHEMA PUBLIC API ---
#
# Ponte incremental para o contrato público de RTD Option Quotes.
#
# Esta frente mantém o bridge operacional existente, mas cria um ponto local e
# pequeno para preferir as APIs públicas de services/rtd_option_quotes_schema.py
# quando disponíveis. Não há troca de persistência, não há substituição ampla
# do fluxo operacional e não há execução de git.
#
def _frente_23_schema_api(*names):
    try:
        from services import rtd_option_quotes_schema as schema
    except Exception:
        return None

    for name in names:
        api = getattr(schema, name, None)
        if callable(api):
            return api

    return None


def _frente_23_rtd_option_quotes_headers():
    api = _frente_23_schema_api("rtd_option_quotes_headers")
    if api is not None:
        return list(api())

    value = globals().get("RTD_OPTION_QUOTES_HEADERS")
    if value is None:
        value = globals().get("HEADERS")
    if value is None:
        return []

    return list(value)


def _frente_23_rtd_option_quotes_required_headers():
    api = _frente_23_schema_api("rtd_option_quotes_required_headers")
    if api is not None:
        return list(api())

    value = globals().get("RTD_OPTION_QUOTES_REQUIRED_HEADERS")
    if value is None:
        value = globals().get("REQUIRED_HEADERS")
    if value is None:
        return []

    return list(value)


def _frente_23_rtd_option_quotes_workbook_name():
    api = _frente_23_schema_api("rtd_option_quotes_workbook_name")
    if api is not None:
        return str(api())

    value = globals().get("DEFAULT_WORKBOOK_NAME")
    if value is None:
        value = globals().get("WORKBOOK_NAME")
    if value is None:
        return ""

    return str(value)


def _frente_23_rtd_option_quotes_sheet_name():
    api = _frente_23_schema_api("rtd_option_quotes_sheet_name")
    if api is not None:
        return str(api())

    value = globals().get("DEFAULT_SHEET_NAME")
    if value is None:
        value = globals().get("SHEET_NAME")
    if value is None:
        return ""

    return str(value)


def _frente_23_normalize_rtd_option_quotes_header(value):
    api = _frente_23_schema_api(
        "normalize_rtd_option_quotes_header",
        "normalize_header",
        "rtd_option_quotes_normalize_header",
    )
    if api is not None:
        return api(value)

    text = "" if value is None else str(value)
    return text.strip().lower().replace(" ", "_").replace("-", "_")


# --- FIM FRENTE 23 RTD BRIDGE SCHEMA PUBLIC API ---
