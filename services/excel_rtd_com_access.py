from __future__ import annotations

from pathlib import Path
from typing import Any


EXCEL_PROG_ID = "Excel.Application"


class ExcelComAccessError(RuntimeError):
    pass


class ExcelComUnavailableError(ExcelComAccessError):
    pass


def import_win32com_client() -> Any:
    try:
        import win32com.client  # type: ignore[import-not-found]
    except Exception as exc:
        raise ExcelComUnavailableError(f"win32com indisponivel: {exc}") from exc

    return win32com.client


def get_active_excel_application(prog_id: str = EXCEL_PROG_ID) -> Any:
    win32com_client = import_win32com_client()

    try:
        return win32com_client.GetActiveObject(prog_id)
    except Exception as exc:
        raise ExcelComAccessError(f"Excel ativo nao encontrado: {exc}") from exc


def safe_getattr(obj: Any, name: str, default: Any = None) -> Any:
    try:
        return getattr(obj, name)
    except Exception:
        return default


def safe_str(value: Any) -> str:
    try:
        return "" if value is None else str(value)
    except Exception:
        return ""


def normalize_com_name(value: Any) -> str:
    return safe_str(value).strip().casefold()


def get_com_item(collection: Any, index: int) -> Any:
    item_getter = safe_getattr(collection, "Item")

    if callable(item_getter):
        try:
            return item_getter(index)
        except Exception:
            pass

    try:
        return collection(index)
    except Exception:
        pass

    try:
        return collection[index - 1]
    except Exception:
        return None


def iter_com_collection(collection: Any) -> list[Any]:
    if collection is None:
        return []

    count = safe_getattr(collection, "Count")

    if count is not None:
        try:
            total = int(count)
        except Exception:
            total = 0

        if total > 0:
            items: list[Any] = []
            for index in range(1, total + 1):
                item = get_com_item(collection, index)
                if item is not None:
                    items.append(item)
            return items

    try:
        return list(collection)
    except Exception:
        return []


def find_open_workbook(excel_app: Any, workbook_name: str) -> Any:
    expected = normalize_com_name(Path(workbook_name).name)
    workbooks = safe_getattr(excel_app, "Workbooks")

    for workbook in iter_com_collection(workbooks):
        candidates = [
            safe_getattr(workbook, "Name"),
            Path(safe_str(safe_getattr(workbook, "FullName"))).name,
        ]

        if any(normalize_com_name(candidate) == expected for candidate in candidates):
            return workbook

    return None


def list_workbook_names(excel_app: Any) -> list[str]:
    workbooks = safe_getattr(excel_app, "Workbooks")
    return [
        safe_str(safe_getattr(workbook, "Name")).strip()
        for workbook in iter_com_collection(workbooks)
        if safe_str(safe_getattr(workbook, "Name")).strip()
    ]


def find_worksheet(workbook: Any, sheet_name: str) -> Any:
    expected = normalize_com_name(sheet_name)

    for collection_name in ("Worksheets", "Sheets"):
        sheets = safe_getattr(workbook, collection_name)

        for sheet in iter_com_collection(sheets):
            if normalize_com_name(safe_getattr(sheet, "Name")) == expected:
                return sheet

    for collection_name in ("Worksheets", "Sheets"):
        sheets = safe_getattr(workbook, collection_name)

        try:
            return sheets(sheet_name)
        except Exception:
            pass

        item_getter = safe_getattr(sheets, "Item")
        if callable(item_getter):
            try:
                return item_getter(sheet_name)
            except Exception:
                pass

    return None


def list_worksheet_names(workbook: Any) -> list[str]:
    worksheets = safe_getattr(workbook, "Worksheets") or safe_getattr(workbook, "Sheets")
    return [
        safe_str(safe_getattr(sheet, "Name")).strip()
        for sheet in iter_com_collection(worksheets)
        if safe_str(safe_getattr(sheet, "Name")).strip()
    ]
