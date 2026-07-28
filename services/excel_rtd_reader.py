#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import datetime as dt
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from services.rtd_option_quotes_schema import (
    DEFAULT_SHEET_NAME,
    DEFAULT_WORKBOOK_NAME,
    REQUIRED_OPTION_HEADERS,
    normalize_header,
)

from services.excel_rtd_com_access import (
    find_open_workbook as _find_open_workbook,
    find_worksheet as _find_worksheet,
    get_excel_application_for_workbook,
    iter_com_collection as _iter_com_collection,
    list_workbook_names as _list_workbook_names,
    list_worksheet_names as _list_worksheet_names,
)
NUMERIC_FIELDS = {
    "strike",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "vwap",
}

STRING_FIELDS = {
    "codigo_opcao",
    "ativo_base",
    "call_put",
}

EMPTY_VALUES = {
    "",
    "-",
    "--",
    "nan",
    "none",
    "null",
    "#n/a",
    "#n/d",
    "#value!",
    "#valor!",
    "#ref!",
    "#name?",
    "#nome?",
}


@dataclass(frozen=True)
class ExcelRtdReadResult:
    ok: bool
    workbook_name: str
    workbook_path: str
    sheet_name: str
    headers: List[str]
    missing_headers: List[str]
    row_count: int
    records: List[Dict[str, Any]]
    read_at: str
    error: Optional[str] = None


class ExcelRtdReaderError(RuntimeError):
    pass
def normalize_symbol(value: Any) -> Optional[str]:
    if value is None:
        return None

    text = str(value).strip().upper()

    if not text:
        return None

    if text.lower() in EMPTY_VALUES:
        return None

    return text


def normalize_text(value: Any) -> Optional[str]:
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    if text.lower() in EMPTY_VALUES:
        return None

    return text


def normalize_number(value: Any) -> Optional[float]:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return float(value)

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return float(value)

    text = str(value).strip()

    if not text:
        return None

    if text.lower() in EMPTY_VALUES:
        return None

    text = text.replace("\u00a0", "")
    text = text.replace("R$", "")
    text = text.replace("%", "")
    text = text.strip()

    if "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        number = float(text)
    except ValueError:
        return None

    if math.isnan(number) or math.isinf(number):
        return None

    return number


def normalize_date(value: Any) -> Optional[str]:
    """Normaliza datas para o padrao brasileiro DD-MM-YYYY.

    Escopo conservador: usado pelo leitor RTD Excel.

    Regras:
    - datetime/date Python -> DD-MM-YYYY
    - serial numerico Excel/COM -> DD-MM-YYYY
    - string numerica com serial Excel -> DD-MM-YYYY
    - ISO YYYY-MM-DD -> DD-MM-YYYY
    - BR DD-MM-YYYY ou DD/MM/YYYY -> DD-MM-YYYY
    - US MM-DD-YYYY ou MM/DD/YYYY -> DD-MM-YYYY quando nao conflitar
    - texto nao reconhecido -> retorna texto original
    """
    import datetime as _dt
    import re as _re

    def _format_date(date_value: _dt.date) -> str:
        return date_value.strftime("%d-%m-%Y")

    def _from_excel_serial(serial_value: float) -> Optional[str]:
        # Excel/COM usa base 1899-12-30.
        # A fracao representa horario; para vencimento, usamos apenas a data.
        if not (20000 <= serial_value <= 80000):
            return None

        excel_epoch = _dt.datetime(1899, 12, 30)
        date_value = (excel_epoch + _dt.timedelta(days=float(serial_value))).date()
        return _format_date(date_value)

    if value is None:
        return None

    if isinstance(value, _dt.datetime):
        return _format_date(value.date())

    if isinstance(value, _dt.date):
        return _format_date(value)

    if isinstance(value, bool):
        return str(value)

    if isinstance(value, (int, float)):
        converted = _from_excel_serial(float(value))
        if converted is not None:
            return converted
        return str(value)

    raw = str(value).strip()
    if not raw:
        return None

    lowered = raw.lower()
    if lowered in {"none", "null", "nan", "nat"}:
        return None

    numeric_candidate = raw.replace(",", ".")
    if _re.fullmatch(r"\d+(?:\.\d+)?", numeric_candidate):
        converted = _from_excel_serial(float(numeric_candidate))
        if converted is not None:
            return converted

    # Data compacta, ex.: 20260821 ou 21082026.
    if _re.fullmatch(r"\d{8}", raw):
        for fmt in ("%Y%m%d", "%d%m%Y"):
            try:
                return _format_date(_dt.datetime.strptime(raw, fmt).date())
            except ValueError:
                pass

    # Remove horario em strings ISO ou similares.
    date_part = raw.replace("T", " ").split(" ")[0].strip()

    # Ordem proposital:
    # 1. ISO
    # 2. Brasil
    # 3. EUA apenas quando a data BR nao for parseavel, ex.: 08/21/2026
    formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d.%m.%Y",
        "%m-%d-%Y",
        "%m/%d/%Y",
    )

    for fmt in formats:
        try:
            return _format_date(_dt.datetime.strptime(date_part, fmt).date())
        except ValueError:
            pass

    return raw


def normalize_cell(field_name: str, value: Any) -> Any:
    if field_name in NUMERIC_FIELDS:
        return normalize_number(value)

    if field_name == "vencimento":
        return normalize_date(value)

    if field_name == "codigo_opcao":
        return normalize_symbol(value)

    if field_name in STRING_FIELDS:
        text = normalize_text(value)
        return text.upper() if text is not None else None

    return normalize_text(value)


def iter_rows_from_range(values: Any) -> Iterable[Sequence[Any]]:
    if values is None:
        return []

    if not isinstance(values, tuple):
        return [(values,)]

    if values and not isinstance(values[0], tuple):
        return [values]

    return values


def get_excel_application(workbook_name: str = DEFAULT_WORKBOOK_NAME) -> Any:
    try:
        return get_excel_application_for_workbook(workbook_name)
    except Exception as exc:
        raise ExcelRtdReaderError(f"Nao foi possivel obter instancia ativa do Excel: {exc}") from exc


def find_workbook(excel: Any, workbook_name: str = DEFAULT_WORKBOOK_NAME) -> Any:
    workbook = _find_open_workbook(excel, workbook_name)

    if workbook is not None:
        return workbook

    available = _list_workbook_names(excel)
    raise ExcelRtdReaderError(
        f"Workbook '{workbook_name}' nao encontrado no Excel. "
        f"Workbooks disponiveis: {available}"
    )


def find_sheet(workbook: Any, sheet_name: str = DEFAULT_SHEET_NAME) -> Any:
    sheet = _find_worksheet(workbook, sheet_name)

    if sheet is not None:
        return sheet

    available = _list_worksheet_names(workbook)
    raise ExcelRtdReaderError(
        f"Worksheet '{sheet_name}' nao encontrada no workbook. "
        f"Worksheets disponiveis: {available}"
    )


def get_used_range_values(sheet: Any) -> List[List[Any]]:
    used_range = sheet.UsedRange
    values = used_range.Value

    rows = []
    for row in iter_rows_from_range(values):
        rows.append(list(row))

    return rows


def build_header_index(raw_header_row: Sequence[Any]) -> Dict[str, int]:
    header_index = {}

    for index, value in enumerate(raw_header_row):
        header = normalize_header(value)
        if header and header not in header_index:
            header_index[header] = index

    return header_index


def normalize_record(
    row: Sequence[Any],
    header_index: Dict[str, int],
    headers: Sequence[str],
) -> Dict[str, Any]:
    record = {}

    for header in headers:
        index = header_index.get(header)
        raw_value = None

        if index is not None and index < len(row):
            raw_value = row[index]

        record[header] = normalize_cell(header, raw_value)

    return record


def is_meaningful_record(record: Dict[str, Any]) -> bool:
    symbol = record.get("codigo_opcao")
    if not symbol:
        return False

    has_market_value = any(
        record.get(field) is not None
        for field in ("ultimo_preco", "bid", "ask", "volume", "vwap")
    )

    return bool(has_market_value)


def read_excel_rtd_options(
    workbook_name: str = DEFAULT_WORKBOOK_NAME,
    sheet_name: str = DEFAULT_SHEET_NAME,
    required_headers: Optional[Sequence[str]] = None,
) -> ExcelRtdReadResult:
    required = list(required_headers or REQUIRED_OPTION_HEADERS)
    read_at = dt.datetime.now().isoformat(timespec="seconds")

    try:
        excel = get_excel_application(workbook_name)
        workbook = find_workbook(excel, workbook_name)
        sheet = find_sheet(workbook, sheet_name)

        rows = get_used_range_values(sheet)

        if not rows:
            raise ExcelRtdReaderError("aba_sem_dados")

        header_index = build_header_index(rows[0])
        headers = list(header_index.keys())
        missing = [header for header in required if header not in header_index]

        if missing:
            return ExcelRtdReadResult(
                ok=False,
                workbook_name=str(workbook.Name),
                workbook_path=str(getattr(workbook, "FullName", "")),
                sheet_name=str(sheet.Name),
                headers=headers,
                missing_headers=missing,
                row_count=len(rows),
                records=[],
                read_at=read_at,
                error="headers_obrigatorios_ausentes",
            )

        records = []

        for row in rows[1:]:
            record = normalize_record(row, header_index, required)
            if is_meaningful_record(record):
                records.append(record)

        return ExcelRtdReadResult(
            ok=True,
            workbook_name=str(workbook.Name),
            workbook_path=str(getattr(workbook, "FullName", "")),
            sheet_name=str(sheet.Name),
            headers=headers,
            missing_headers=[],
            row_count=len(rows),
            records=records,
            read_at=read_at,
            error=None,
        )

    except ExcelRtdReaderError as exc:
        return ExcelRtdReadResult(
            ok=False,
            workbook_name=workbook_name,
            workbook_path="",
            sheet_name=sheet_name,
            headers=[],
            missing_headers=required,
            row_count=0,
            records=[],
            read_at=read_at,
            error=str(exc),
        )


def result_to_dict(result: ExcelRtdReadResult) -> Dict[str, Any]:
    return {
        "ok": result.ok,
        "workbook_name": result.workbook_name,
        "workbook_path": result.workbook_path,
        "sheet_name": result.sheet_name,
        "headers": result.headers,
        "missing_headers": result.missing_headers,
        "row_count": result.row_count,
        "record_count": len(result.records),
        "records": result.records,
        "read_at": result.read_at,
        "error": result.error,
    }


def read_excel_rtd_options_as_dict(
    workbook_name: str = DEFAULT_WORKBOOK_NAME,
    sheet_name: str = DEFAULT_SHEET_NAME,
) -> Dict[str, Any]:
    return result_to_dict(
        read_excel_rtd_options(
            workbook_name=workbook_name,
            sheet_name=sheet_name,
        )
    )
