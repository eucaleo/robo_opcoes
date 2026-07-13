"""Probe controlado do Excel RTD BTG Online.

Este módulo faz apenas diagnóstico de conexão com Excel/Workbook/Aba.
Ele não abre Excel, não grava banco, não dispara subprocessos e não inicia coleta.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import os
import re
import unicodedata
from typing import Any, Callable, Iterable


DEFAULT_WORKBOOK_NAME = "LISTA_RTD.xlsm"
DEFAULT_WORKSHEET_NAME = "RTD_OPTION_QUOTES"

DEFAULT_REQUIRED_HEADERS = (
    "ticker",
    "bid",
    "ask",
)

HEADER_ALIASES = {
    "ticker": (
        "ticker",
        "ativo",
        "codigo",
        "codigo_ativo",
        "codigo_opcao",
        "opcao",
        "codigo_da_opcao",
        "symbol",
        "underlying",
    ),
    "bid": (
        "bid",
        "compra",
        "preco_compra",
        "best_bid",
    ),
    "ask": (
        "ask",
        "venda",
        "preco_venda",
        "best_ask",
    ),
}


class ExcelProbeDependencyError(RuntimeError):
    """Dependência COM/pywin32 indisponível."""


class ExcelNotRunningError(RuntimeError):
    """Excel não está aberto ou não está registrado no COM ativo."""


@dataclass(frozen=True)
class ExcelRtdProbeResult:
    ok: bool = False
    excel_running: bool = False
    workbook_found: bool = False
    worksheet_found: bool = False
    workbook_name: str | None = None
    workbook_path: str | None = None
    worksheet_name: str | None = None
    headers: dict[str, int] = field(default_factory=dict)
    raw_headers: dict[str, int] = field(default_factory=dict)
    required_headers: list[str] = field(default_factory=list)
    missing_headers: list[str] = field(default_factory=list)
    message: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExcelRtdProbeService:
    """Serviço de diagnóstico do Excel RTD.

    A dependência de Excel pode ser injetada nos testes via get_active_excel.
    Em produção, usa get_active_excel_application("Excel.Application").
    """

    def __init__(
        self,
        get_active_excel: Callable[[], Any] | None = None,
    ) -> None:
        self._get_active_excel = get_active_excel or _default_get_active_excel

    def probe(
        self,
        workbook_name: str = DEFAULT_WORKBOOK_NAME,
        worksheet_name: str = DEFAULT_WORKSHEET_NAME,
        required_headers: Iterable[str] = DEFAULT_REQUIRED_HEADERS,
    ) -> ExcelRtdProbeResult:
        required_headers_list = list(required_headers)

        try:
            excel = self._get_active_excel()
        except ExcelNotRunningError as exc:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Excel não está aberto ou não foi encontrado via COM ativo.",
                error=str(exc),
            )
        except ExcelProbeDependencyError as exc:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Dependência de automação Excel indisponível.",
                error=str(exc),
            )
        except Exception as exc:  # pragma: no cover - defesa contra COM instável
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Falha inesperada ao acessar Excel via COM.",
                error=str(exc),
            )

        if excel is None:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Excel não retornou instância ativa.",
            )

        workbook = _find_workbook(excel, workbook_name)

        if workbook is None:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=True,
                workbook_found=False,
                required_headers=required_headers_list,
                message=f"Workbook '{workbook_name}' não encontrado no Excel ativo.",
            )

        found_workbook_name = _safe_str(getattr(workbook, "Name", None))
        found_workbook_path = _safe_str(getattr(workbook, "FullName", None))

        worksheet = _find_worksheet(workbook, worksheet_name)

        if worksheet is None:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=True,
                workbook_found=True,
                worksheet_found=False,
                workbook_name=found_workbook_name,
                workbook_path=found_workbook_path,
                required_headers=required_headers_list,
                message=(
                    f"Workbook '{workbook_name}' encontrado, "
                    f"mas aba '{worksheet_name}' não localizada."
                ),
            )

        headers, raw_headers = _read_header_row(worksheet)
        missing_headers = _missing_required_headers(headers, required_headers_list)

        ok = len(missing_headers) == 0

        return ExcelRtdProbeResult(
            ok=ok,
            excel_running=True,
            workbook_found=True,
            worksheet_found=True,
            workbook_name=found_workbook_name,
            workbook_path=found_workbook_path,
            worksheet_name=_safe_str(getattr(worksheet, "Name", None)),
            headers=headers,
            raw_headers=raw_headers,
            required_headers=required_headers_list,
            missing_headers=missing_headers,
            message=(
                "Probe Excel RTD validado com sucesso."
                if ok
                else "Probe Excel RTD encontrou cabeçalhos obrigatórios ausentes."
            ),
        )


def _default_get_active_excel() -> Any:
    try:
        from services.excel_rtd_com_access import get_active_excel_application, import_win32com_client
        import_win32com_client()
    except ModuleNotFoundError as exc:
        raise ExcelProbeDependencyError(
            "Módulo win32com.client não disponível. Instale pywin32 no ambiente Windows."
        ) from exc

    try:
        return get_active_excel_application("Excel.Application")
    except Exception as exc:
        raise ExcelNotRunningError(
            "Excel.Application não encontrado via GetActiveObject."
        ) from exc


def _find_workbook(excel: Any, workbook_name: str) -> Any | None:
    expected = workbook_name.casefold()

    for workbook in _iter_com_collection(getattr(excel, "Workbooks", [])):
        name = _safe_str(getattr(workbook, "Name", None)).casefold()
        full_name = _safe_str(getattr(workbook, "FullName", None))
        basename = os.path.basename(full_name).casefold() if full_name else ""

        if name == expected or basename == expected:
            return workbook

    return None


def _find_worksheet(workbook: Any, worksheet_name: str) -> Any | None:
    expected = worksheet_name.casefold()

    for worksheet in _iter_com_collection(getattr(workbook, "Worksheets", [])):
        name = _safe_str(getattr(worksheet, "Name", None)).casefold()

        if name == expected:
            return worksheet

    return None


def _read_header_row(worksheet: Any) -> tuple[dict[str, int], dict[str, int]]:
    headers: dict[str, int] = {}
    raw_headers: dict[str, int] = {}

    max_columns = _used_range_columns_count(worksheet)

    for col in range(1, max_columns + 1):
        value = _cell_value(worksheet, 1, col)

        if value is None:
            continue

        raw = str(value).strip()

        if not raw:
            continue

        normalized = normalize_header(raw)

        if not normalized:
            continue

        headers.setdefault(normalized, col)
        raw_headers.setdefault(raw, col)

    return headers, raw_headers


def _used_range_columns_count(worksheet: Any) -> int:
    used_range = getattr(worksheet, "UsedRange", None)

    if used_range is None:
        return 256

    columns = getattr(used_range, "Columns", None)

    if columns is None:
        return 256

    count = getattr(columns, "Count", None)

    try:
        parsed = int(count)
    except (TypeError, ValueError):
        return 256

    if parsed <= 0:
        return 256

    return min(parsed, 1024)


def _cell_value(worksheet: Any, row: int, col: int) -> Any:
    cell_accessor = getattr(worksheet, "Cells", None)

    if cell_accessor is None:
        return None

    try:
        cell = cell_accessor(row, col)
    except TypeError:
        return None

    return getattr(cell, "Value", None)


def _missing_required_headers(
    normalized_headers: dict[str, int],
    required_headers: Iterable[str],
) -> list[str]:
    missing: list[str] = []

    for required in required_headers:
        aliases = _aliases_for(required)

        if not any(alias in normalized_headers for alias in aliases):
            missing.append(required)

    return missing


def _aliases_for(header: str) -> tuple[str, ...]:
    normalized = normalize_header(header)
    aliases = {normalized}

    for alias in HEADER_ALIASES.get(normalized, ()):
        alias_normalized = normalize_header(alias)

        if alias_normalized:
            aliases.add(alias_normalized)

    return tuple(sorted(aliases))


def normalize_header(value: Any) -> str:
    if value is None:
        return ""

    text = str(value).strip().casefold()

    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")

    return text


def _iter_com_collection(collection: Any) -> Iterable[Any]:
    count = getattr(collection, "Count", None)
    item = getattr(collection, "Item", None)

    if count is not None and item is not None:
        try:
            parsed_count = int(count)
        except (TypeError, ValueError):
            parsed_count = 0

        if parsed_count > 0:
            for index in range(1, parsed_count + 1):
                yield item(index)

            return

    try:
        yield from collection
    except TypeError:
        return


def _safe_str(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()

    return text or None
