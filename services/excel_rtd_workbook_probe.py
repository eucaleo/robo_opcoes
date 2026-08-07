"""Probe controlado para diagnosticar o Excel RTD aberto.

Este modulo nao grava banco, nao altera UI e nao abre uma nova instancia do Excel.
A integracao real com COM fica isolada em Win32ExcelWorkbookAdapter.

Objetivo da Fase 1:
- anexar ao Excel ja aberto;
- localizar LISTA_RTD.xlsm;
- listar abas;
- ler uma pequena amostra da planilha;
- retornar status estruturado e testavel.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from services.rtd_option_quotes_schema import DEFAULT_WORKBOOK_NAME
from services.excel_rtd_com_access import get_excel_application_for_workbook




class ExcelRtdProbeError(RuntimeError):
    """Erro controlado do probe Excel RTD."""


class ExcelWorkbookAdapter(Protocol):
    """Contrato minimo para permitir teste sem Excel real."""

    def list_workbooks(self) -> list[dict[str, Any]]:
        """Retorna workbooks abertos no Excel."""

    def read_sheet_sample(
        self,
        *,
        workbook_full_name: str,
        sheet_name: str,
        max_rows: int,
        max_cols: int,
    ) -> dict[str, Any]:
        """Le pequena amostra de uma aba."""


@dataclass(frozen=True)
class ExcelRtdWorkbookProbeConfig:
    workbook_name: str = DEFAULT_WORKBOOK_NAME
    preferred_sheet: str | None = None
    max_rows: int = 8
    max_cols: int = 40


@dataclass(frozen=True)
class ExcelRtdWorkbookProbeResult:
    ok: bool
    status: str
    message: str
    workbook_name: str | None = None
    workbook_full_name: str | None = None
    sheets: list[str] = field(default_factory=list)
    selected_sheet: str | None = None
    requested_sheet: str | None = None
    headers: list[str] = field(default_factory=list)
    sample_rows: list[list[Any]] = field(default_factory=list)
    row_count: int | None = None
    col_count: int | None = None
    workbooks_seen: list[str] = field(default_factory=list)


class Win32ExcelWorkbookAdapter:
    """Adaptador COM para Excel ja aberto.

    Usa o nucleo central de acesso COM, baseado em GetActiveObject, para evitar abrir uma nova instancia
    escondida do Excel. Isso respeita a arquitetura da frente:
    corretora e Excel abertos antes do sistema.
    """

    def __init__(self) -> None:
        try:
            self._excel = get_excel_application_for_workbook(DEFAULT_WORKBOOK_NAME)
        except Exception as exc:  # pragma: no cover
            raise ExcelRtdProbeError(
                "Excel nao esta aberto ou nao esta acessivel via COM"
            ) from exc

    def list_workbooks(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []

        try:
            count = int(self._excel.Workbooks.Count)
        except Exception as exc:  # pragma: no cover
            raise ExcelRtdProbeError(f"falha ao listar workbooks: {exc}") from exc

        for idx in range(1, count + 1):
            wb = self._excel.Workbooks.Item(idx)
            sheets: list[str] = []

            try:
                sheet_count = int(wb.Worksheets.Count)
                for sheet_idx in range(1, sheet_count + 1):
                    sheets.append(str(wb.Worksheets.Item(sheet_idx).Name))
            except Exception:
                sheets = []

            items.append(
                {
                    "name": str(wb.Name),
                    "full_name": str(wb.FullName),
                    "sheets": sheets,
                }
            )

        return items

    def read_sheet_sample(
        self,
        *,
        workbook_full_name: str,
        sheet_name: str,
        max_rows: int,
        max_cols: int,
    ) -> dict[str, Any]:
        wb = self._find_workbook_by_full_name(workbook_full_name)
        ws = wb.Worksheets(sheet_name)

        used = ws.UsedRange
        row_count = int(used.Rows.Count)
        col_count = int(used.Columns.Count)

        if row_count <= 0 or col_count <= 0:
            return {
                "headers": [],
                "rows": [],
                "row_count": row_count,
                "col_count": col_count,
            }

        first_row = int(used.Row)
        first_col = int(used.Column)
        last_row = first_row + min(max_rows, row_count) - 1
        last_col = first_col + min(max_cols, col_count) - 1

        rng = ws.Range(ws.Cells(first_row, first_col), ws.Cells(last_row, last_col))
        matrix = _normalize_excel_value_matrix(rng.Value)

        headers = [
            str(value).strip() if value is not None else ""
            for value in (matrix[0] if matrix else [])
        ]
        rows = matrix[1:] if len(matrix) > 1 else []

        return {
            "headers": headers,
            "rows": rows,
            "row_count": row_count,
            "col_count": col_count,
        }

    def _find_workbook_by_full_name(self, workbook_full_name: str) -> Any:
        target = str(workbook_full_name).casefold()

        for idx in range(1, int(self._excel.Workbooks.Count) + 1):
            wb = self._excel.Workbooks.Item(idx)
            if str(wb.FullName).casefold() == target:
                return wb

        raise ExcelRtdProbeError(f"workbook nao encontrado pelo caminho: {workbook_full_name}")


class ExcelRtdWorkbookProbe:
    """Servico de diagnostico do workbook RTD aberto."""

    def __init__(
        self,
        *,
        config: ExcelRtdWorkbookProbeConfig | None = None,
        adapter: ExcelWorkbookAdapter | None = None,
    ) -> None:
        self.config = config or ExcelRtdWorkbookProbeConfig()
        self.adapter = adapter

    def run(self) -> ExcelRtdWorkbookProbeResult:
        try:
            adapter = self.adapter or Win32ExcelWorkbookAdapter()
            workbooks = adapter.list_workbooks()
        except ExcelRtdProbeError as exc:
            return ExcelRtdWorkbookProbeResult(
                ok=False,
                status="excel_unavailable",
                message=str(exc),
            )
        except Exception as exc:
            return ExcelRtdWorkbookProbeResult(
                ok=False,
                status="unexpected_error",
                message=f"erro inesperado no probe Excel RTD: {exc}",
            )

        workbooks_seen = [
            str(item.get("name") or item.get("full_name") or "")
            for item in workbooks
        ]

        selected = self._find_workbook(workbooks)

        if selected is None:
            return ExcelRtdWorkbookProbeResult(
                ok=False,
                status="workbook_not_found",
                message=f"workbook alvo nao encontrado: {self.config.workbook_name}",
                workbooks_seen=workbooks_seen,
            )

        sheets = [str(sheet) for sheet in selected.get("sheets", [])]
        selected_sheet = self._choose_sheet(sheets)

        if not selected_sheet:
            requested_sheet = self.config.preferred_sheet
            message = (
                f"aba RTD solicitada nao encontrada: {requested_sheet}"
                if requested_sheet
                else "nenhuma aba disponivel para leitura"
            )

            return ExcelRtdWorkbookProbeResult(
                ok=False,
                status="sheet_not_found",
                message=message,
                workbook_name=str(selected.get("name") or ""),
                workbook_full_name=str(selected.get("full_name") or ""),
                sheets=sheets,
                selected_sheet=None,
                requested_sheet=requested_sheet,
                workbooks_seen=workbooks_seen,
            )

        try:
            sample = adapter.read_sheet_sample(
                workbook_full_name=str(selected.get("full_name") or ""),
                sheet_name=selected_sheet,
                max_rows=self.config.max_rows,
                max_cols=self.config.max_cols,
            )
        except ExcelRtdProbeError as exc:
            return ExcelRtdWorkbookProbeResult(
                ok=False,
                status="sheet_read_error",
                message=str(exc),
                workbook_name=str(selected.get("name") or ""),
                workbook_full_name=str(selected.get("full_name") or ""),
                sheets=sheets,
                selected_sheet=selected_sheet,
                requested_sheet=self.config.preferred_sheet,
                workbooks_seen=workbooks_seen,
            )
        except Exception as exc:
            return ExcelRtdWorkbookProbeResult(
                ok=False,
                status="sheet_read_error",
                message=f"falha ao ler amostra da aba: {exc}",
                workbook_name=str(selected.get("name") or ""),
                workbook_full_name=str(selected.get("full_name") or ""),
                sheets=sheets,
                selected_sheet=selected_sheet,
                requested_sheet=self.config.preferred_sheet,
                workbooks_seen=workbooks_seen,
            )

        return ExcelRtdWorkbookProbeResult(
            ok=True,
            status="ok",
            message="workbook RTD localizado e amostra lida com sucesso",
            workbook_name=str(selected.get("name") or ""),
            workbook_full_name=str(selected.get("full_name") or ""),
            sheets=sheets,
            selected_sheet=selected_sheet,
            requested_sheet=self.config.preferred_sheet,
            headers=[str(h).strip() for h in sample.get("headers", [])],
            sample_rows=sample.get("rows", []),
            row_count=sample.get("row_count"),
            col_count=sample.get("col_count"),
            workbooks_seen=workbooks_seen,
        )

    def _find_workbook(self, workbooks: list[dict[str, Any]]) -> dict[str, Any] | None:
        target_name = Path(self.config.workbook_name).name.casefold()

        for item in workbooks:
            name = str(item.get("name") or "").casefold()
            full_name = str(item.get("full_name") or "")
            full_basename = Path(full_name).name.casefold()

            if name == target_name or full_basename == target_name:
                return item

        return None

    def _choose_sheet(self, sheets: list[str]) -> str | None:
        if not sheets:
            return None

        preferred = self.config.preferred_sheet

        if preferred:
            for sheet in sheets:
                if sheet.casefold() == preferred.casefold():
                    return sheet

            return None

        return sheets[0]


def _normalize_excel_value_matrix(value: Any) -> list[list[Any]]:
    """Normaliza retorno COM do Excel para matriz de listas."""

    if value is None:
        return []

    if not isinstance(value, tuple):
        return [[value]]

    if value and not isinstance(value[0], tuple):
        return [list(value)]

    return [list(row) for row in value]

# --- INICIO FRENTE 24 EXCEL RTD WORKBOOK PROBE SCHEMA PUBLIC API ---
# Frente 24 guardrail: Sem troca de persistência.
# Frente 24 guardrail: Sem troca de fluxo operacional amplo.
# Frente 24 guardrail: option_type canônico somente CALL/PUT por extenso; C/V são compra/venda legado.
# Adoção local e incremental do contrato canônico de RTD Option Quotes.
#
# Esta ponte mantém compatibilidade com constantes locais legadas, mas passa a
# preferir as APIs públicas de services.rtd_option_quotes_schema.py quando
# disponíveis. Não altera persistência, bridge, importadores ou fluxo operacional
# amplo.

def _frente24_get_rtd_option_quotes_schema():
    try:
        from services import rtd_option_quotes_schema as _schema
    except Exception:
        return None
    return _schema


def _frente24_call_schema_public_api(api_name, fallback=None):
    schema = _frente24_get_rtd_option_quotes_schema()
    if schema is None:
        return fallback

    api = getattr(schema, api_name, None)
    if not callable(api):
        return fallback

    try:
        value = api()
    except Exception:
        return fallback

    return fallback if value is None else value


def rtd_workbook_probe_option_quotes_workbook_name(fallback=None):
    return _frente24_call_schema_public_api(
        "rtd_option_quotes_workbook_name",
        fallback,
    )


def rtd_workbook_probe_option_quotes_sheet_name(fallback=None):
    return _frente24_call_schema_public_api(
        "rtd_option_quotes_sheet_name",
        fallback,
    )


def rtd_workbook_probe_option_quotes_headers(fallback=None):
    value = _frente24_call_schema_public_api(
        "rtd_option_quotes_headers",
        fallback or (),
    )
    return tuple(value or ())


def rtd_workbook_probe_option_quotes_required_headers(fallback=None):
    value = _frente24_call_schema_public_api(
        "rtd_option_quotes_required_headers",
        fallback or (),
    )
    return tuple(value or ())


def rtd_workbook_probe_normalize_option_quotes_header(header):
    schema = _frente24_get_rtd_option_quotes_schema()
    if schema is not None:
        for api_name in (
            "normalize_rtd_option_quotes_header",
            "normalize_header",
            "normalize_header_name",
        ):
            api = getattr(schema, api_name, None)
            if callable(api):
                try:
                    return api(header)
                except Exception:
                    break

    if header is None:
        return ""
    return str(header).strip().lower()


def _frente24_apply_rtd_option_quotes_schema_defaults():
    workbook_name = rtd_workbook_probe_option_quotes_workbook_name()
    sheet_name = rtd_workbook_probe_option_quotes_sheet_name()
    headers = rtd_workbook_probe_option_quotes_headers()
    required_headers = rtd_workbook_probe_option_quotes_required_headers()

    if workbook_name:
        for name in (
            "DEFAULT_WORKBOOK_NAME",
            "WORKBOOK_NAME",
            "RTD_WORKBOOK_NAME",
            "RTD_OPTION_QUOTES_WORKBOOK_NAME",
            "OPTION_QUOTES_WORKBOOK_NAME",
        ):
            if name in globals():
                globals()[name] = workbook_name

    if sheet_name:
        for name in (
            "DEFAULT_SHEET_NAME",
            "SHEET_NAME",
            "RTD_SHEET_NAME",
            "RTD_OPTION_QUOTES_SHEET_NAME",
            "OPTION_QUOTES_SHEET_NAME",
        ):
            if name in globals():
                globals()[name] = sheet_name

    if headers:
        for name in (
            "HEADERS",
            "RTD_HEADERS",
            "OPTION_QUOTES_HEADERS",
            "RTD_OPTION_QUOTES_HEADERS",
            "EXPECTED_HEADERS",
        ):
            if name in globals():
                globals()[name] = headers

    if required_headers:
        for name in (
            "REQUIRED_HEADERS",
            "RTD_REQUIRED_HEADERS",
            "OPTION_QUOTES_REQUIRED_HEADERS",
            "RTD_OPTION_QUOTES_REQUIRED_HEADERS",
            "MIN_REQUIRED_HEADERS",
        ):
            if name in globals():
                globals()[name] = required_headers


_frente24_apply_rtd_option_quotes_schema_defaults()
# --- FIM FRENTE 24 EXCEL RTD WORKBOOK PROBE SCHEMA PUBLIC API ---
