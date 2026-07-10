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


def sync_rtd_option_quotes_from_excel(
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
