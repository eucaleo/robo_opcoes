from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_WORKBOOK_NAME = "LISTA_RTD.xlsm"
DEFAULT_WORKSHEET_NAME = "RTD_OPTION_QUOTES"

REQUIRED_OPTION_QUOTE_HEADERS: tuple[str, ...] = (
    "codigo_opcao",
    "ativo_base",
    "call_put",
    "strike",
    "vencimento",
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
)


@dataclass(frozen=True)
class ExcelRtdConnectionStatus:
    pywin32_available: bool
    excel_running: bool
    workbook_open: bool
    worksheet_available: bool
    required_headers_ok: bool
    workbook_name: str
    worksheet_name: str
    workbook_full_name: str | None = None
    detected_headers: tuple[str, ...] = ()
    missing_headers: tuple[str, ...] = ()
    message: str = ""

    @property
    def is_ready(self) -> bool:
        return (
            self.pywin32_available
            and self.excel_running
            and self.workbook_open
            and self.worksheet_available
            and self.required_headers_ok
        )


def check_excel_rtd_connection_status(
    workbook_name: str = DEFAULT_WORKBOOK_NAME,
    worksheet_name: str = DEFAULT_WORKSHEET_NAME,
    required_headers: tuple[str, ...] = REQUIRED_OPTION_QUOTE_HEADERS,
    excel_app: Any | None = None,
) -> ExcelRtdConnectionStatus:
    if excel_app is None:
        try:
            import win32com.client  # type: ignore[import-not-found]
        except Exception as exc:
            return ExcelRtdConnectionStatus(
                pywin32_available=False,
                excel_running=False,
                workbook_open=False,
                worksheet_available=False,
                required_headers_ok=False,
                workbook_name=workbook_name,
                worksheet_name=worksheet_name,
                missing_headers=required_headers,
                message=f"pywin32 indisponível: {exc}",
            )

        try:
            excel_app = win32com.client.GetActiveObject("Excel.Application")
        except Exception as exc:
            return ExcelRtdConnectionStatus(
                pywin32_available=True,
                excel_running=False,
                workbook_open=False,
                worksheet_available=False,
                required_headers_ok=False,
                workbook_name=workbook_name,
                worksheet_name=worksheet_name,
                missing_headers=required_headers,
                message=f"Excel não está aberto ou não foi encontrado via COM: {exc}",
            )

    workbook = _find_open_workbook(excel_app, workbook_name)

    if workbook is None:
        return ExcelRtdConnectionStatus(
            pywin32_available=True,
            excel_running=True,
            workbook_open=False,
            worksheet_available=False,
            required_headers_ok=False,
            workbook_name=workbook_name,
            worksheet_name=worksheet_name,
            missing_headers=required_headers,
            message=f"Workbook obrigatório não está aberto: {workbook_name}",
        )

    workbook_full_name = _safe_str(_safe_getattr(workbook, "FullName"))
    worksheet = _find_worksheet(workbook, worksheet_name)

    if worksheet is None:
        return ExcelRtdConnectionStatus(
            pywin32_available=True,
            excel_running=True,
            workbook_open=True,
            worksheet_available=False,
            required_headers_ok=False,
            workbook_name=workbook_name,
            worksheet_name=worksheet_name,
            workbook_full_name=workbook_full_name,
            missing_headers=required_headers,
            message=f"Aba obrigatória ausente no workbook {workbook_name}: {worksheet_name}",
        )

    detected_headers = _read_header_row(worksheet)
    detected_set = set(detected_headers)
    missing_headers = tuple(
        header for header in required_headers if header not in detected_set
    )

    if missing_headers:
        return ExcelRtdConnectionStatus(
            pywin32_available=True,
            excel_running=True,
            workbook_open=True,
            worksheet_available=True,
            required_headers_ok=False,
            workbook_name=workbook_name,
            worksheet_name=worksheet_name,
            workbook_full_name=workbook_full_name,
            detected_headers=detected_headers,
            missing_headers=missing_headers,
            message=(
                "Cabeçalho obrigatório ausente na aba "
                f"{worksheet_name}: {missing_headers[0]}"
            ),
        )

    return ExcelRtdConnectionStatus(
        pywin32_available=True,
        excel_running=True,
        workbook_open=True,
        worksheet_available=True,
        required_headers_ok=True,
        workbook_name=workbook_name,
        worksheet_name=worksheet_name,
        workbook_full_name=workbook_full_name,
        detected_headers=detected_headers,
        missing_headers=(),
        message="RTD Excel pronto para leitura.",
    )


def _find_open_workbook(excel_app: Any, workbook_name: str) -> Any | None:
    expected = _normalize_workbook_name(workbook_name)

    for workbook in _iter_com_collection(_safe_getattr(excel_app, "Workbooks")):
        current_name = _normalize_workbook_name(_safe_getattr(workbook, "Name"))
        current_full_name = _normalize_workbook_name(
            Path(_safe_str(_safe_getattr(workbook, "FullName"))).name
        )

        if expected in {current_name, current_full_name}:
            return workbook

    return None


def _find_worksheet(workbook: Any, worksheet_name: str) -> Any | None:
    worksheets = _safe_getattr(workbook, "Worksheets")

    try:
        return worksheets.Item(worksheet_name)
    except Exception:
        pass

    expected = _normalize_header(worksheet_name)

    for worksheet in _iter_com_collection(worksheets):
        current = _normalize_header(_safe_getattr(worksheet, "Name"))

        if current == expected:
            return worksheet

    return None


def _read_header_row(worksheet: Any) -> tuple[str, ...]:
    max_columns = _detect_used_columns(worksheet)

    headers: list[str] = []

    for column in range(1, max_columns + 1):
        value = _safe_get_cell_value(worksheet, 1, column)
        normalized = _normalize_header(value)

        if normalized:
            headers.append(normalized)

    return tuple(headers)


def _detect_used_columns(worksheet: Any) -> int:
    try:
        count = worksheet.UsedRange.Columns.Count
        count_as_int = int(count)

        if count_as_int > 0:
            return min(count_as_int, 512)
    except Exception:
        pass

    return 128


def _safe_get_cell_value(worksheet: Any, row: int, column: int) -> Any:
    try:
        return worksheet.Cells(row, column).Value
    except Exception:
        return None


def _iter_com_collection(collection: Any) -> list[Any]:
    if collection is None:
        return []

    try:
        count = int(collection.Count)
    except Exception:
        try:
            return list(collection)
        except Exception:
            return []

    items: list[Any] = []

    for index in range(1, count + 1):
        try:
            items.append(collection.Item(index))
        except Exception:
            continue

    return items


def _normalize_workbook_name(value: Any) -> str:
    return _safe_str(value).strip().casefold()


def _normalize_header(value: Any) -> str:
    return _safe_str(value).strip().casefold()


def _safe_getattr(obj: Any, name: str) -> Any:
    try:
        return getattr(obj, name)
    except Exception:
        return None


def _safe_str(value: Any) -> str:
    if value is None:
        return ""

    return str(value)
