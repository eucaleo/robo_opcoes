from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
from services.excel_rtd_reader import (
    DEFAULT_SHEET_NAME,
    DEFAULT_WORKBOOK_NAME,
    read_excel_rtd_options_as_dict,
)


@dataclass(frozen=True)
class RtdOptionQuotesSyncResult:
    ok: bool
    rows_read: int
    rows_upserted: int
    db_path: str
    workbook_name: str | None = None
    workbook_path: str | None = None
    sheet_name: str | None = None
    read_at: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def sync_rtd_option_quotes_records(
    records: list[dict[str, Any]],
    *,
    db_path: str | Path = "dados/app.db",
    source: str = "excel_rtd_live",
    read_at: str | None = None,
) -> RtdOptionQuotesSyncResult:
    repo = RtdOptionQuotesRepository(db_path=db_path)

    try:
        rows_upserted = repo.upsert_many(
            records,
            source=source,
            read_at=read_at,
        )
    except Exception as exc:
        return RtdOptionQuotesSyncResult(
            ok=False,
            rows_read=len(records),
            rows_upserted=0,
            db_path=str(db_path),
            read_at=read_at,
            error=repr(exc),
        )

    return RtdOptionQuotesSyncResult(
        ok=True,
        rows_read=len(records),
        rows_upserted=rows_upserted,
        db_path=str(db_path),
        read_at=read_at,
    )


def sync_rtd_option_quotes_from_existing_excel(
    *,
    db_path: str | Path = "dados/app.db",
    workbook_name: str = DEFAULT_WORKBOOK_NAME,
    sheet_name: str = DEFAULT_SHEET_NAME,
    reader_fn: Callable[..., Mapping[str, Any]] = read_excel_rtd_options_as_dict,
) -> RtdOptionQuotesSyncResult:
    try:
        read_result = dict(
            reader_fn(
                workbook_name=workbook_name,
                sheet_name=sheet_name,
            )
        )
    except Exception as exc:
        return RtdOptionQuotesSyncResult(
            ok=False,
            rows_read=0,
            rows_upserted=0,
            db_path=str(db_path),
            workbook_name=workbook_name,
            sheet_name=sheet_name,
            error=repr(exc),
        )

    records = list(read_result.get("records") or [])
    read_at = read_result.get("read_at")
    workbook_path = read_result.get("workbook_path")
    actual_workbook_name = read_result.get("workbook_name") or workbook_name
    actual_sheet_name = read_result.get("sheet_name") or sheet_name

    if not read_result.get("ok"):
        return RtdOptionQuotesSyncResult(
            ok=False,
            rows_read=len(records),
            rows_upserted=0,
            db_path=str(db_path),
            workbook_name=actual_workbook_name,
            workbook_path=workbook_path,
            sheet_name=actual_sheet_name,
            read_at=read_at,
            error=read_result.get("error") or "excel_rtd_reader_returned_not_ok",
        )

    sync_result = sync_rtd_option_quotes_records(
        records,
        db_path=db_path,
        source="excel_rtd_live",
        read_at=read_at,
    )

    return RtdOptionQuotesSyncResult(
        ok=sync_result.ok,
        rows_read=sync_result.rows_read,
        rows_upserted=sync_result.rows_upserted,
        db_path=str(db_path),
        workbook_name=actual_workbook_name,
        workbook_path=workbook_path,
        sheet_name=actual_sheet_name,
        read_at=read_at,
        error=sync_result.error,
    )

# <!-- INICIO FRENTE 35 RTD OPTION QUOTES SYNC SERVICE PARSER BRIDGE CONTRACT -->
# Frente 35:
# Ponte contratual local para parsers canonicos no sync service de RTD Option Quotes.
#
# Objetivo:
# - registrar dependencia preferencial de utils.number_parser e utils.date_parser;
# - preservar rtd_option_quotes_sync_service.py como orquestrador de sync via repository;
# - nao alterar persistencia;
# - nao alterar schema;
# - nao alterar fluxo operacional do sync RTD nesta frente;
# - manter option_type canonico somente CALL/PUT por extenso;
# - manter C/V como compra/venda legado.
try:
    from utils.number_parser import (
        parse_float_br as _frente35_parse_float_br,
        parse_optional_float as _frente35_parse_optional_float,
        parse_positive_float as _frente35_parse_positive_float,
        parse_percent as _frente35_parse_percent,
    )
except Exception:  # pragma: no cover - fallback contratual defensivo
    _frente35_parse_float_br = None
    _frente35_parse_optional_float = None
    _frente35_parse_positive_float = None
    _frente35_parse_percent = None

try:
    from utils.date_parser import (
        parse_excel_date_to_iso as _frente35_parse_excel_date_to_iso,
        parse_datetime_to_iso as _frente35_parse_datetime_to_iso,
    )
except Exception:  # pragma: no cover - fallback contratual defensivo
    _frente35_parse_excel_date_to_iso = None
    _frente35_parse_datetime_to_iso = None


def _frente35_number_parser_contract():
    """Retorna os parsers numericos canonicos conhecidos pelo sync service.

    Esta ponte e declarativa e incremental. Ela nao troca persistencia, nao
    altera schema e nao muda o fluxo operacional existente do sync RTD.
    """
    return {
        "parse_float_br": _frente35_parse_float_br,
        "parse_optional_float": _frente35_parse_optional_float,
        "parse_positive_float": _frente35_parse_positive_float,
        "parse_percent": _frente35_parse_percent,
    }


def _frente35_date_parser_contract():
    """Retorna os parsers canonicos de data conhecidos pelo sync service."""
    return {
        "parse_excel_date_to_iso": _frente35_parse_excel_date_to_iso,
        "parse_datetime_to_iso": _frente35_parse_datetime_to_iso,
    }


def _frente35_rtd_option_quotes_sync_service_parser_bridge_contract():
    """Contrato local da Frente 35 para parsers canonicos no sync service.

    Regras preservadas:
    - sem troca de persistencia;
    - sem troca de schema;
    - sem alteracao operacional do sync RTD;
    - option_type canonico somente CALL/PUT por extenso;
    - C/V sao compra/venda legado.
    """
    return {
        "number_parser": _frente35_number_parser_contract(),
        "date_parser": _frente35_date_parser_contract(),
        "persistence_changed": False,
        "schema_changed": False,
        "operational_sync_changed": False,
        "canonical_option_type": ("CALL", "PUT"),
        "legacy_buy_sell": ("C", "V"),
    }
# <!-- FIM FRENTE 35 RTD OPTION QUOTES SYNC SERVICE PARSER BRIDGE CONTRACT -->
