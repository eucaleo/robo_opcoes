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


def resolve_workbook_path(
    workbook_name: str,
    workbook_path: str | Path | None = None,
) -> Path:
    if workbook_path is not None:
        path = Path(workbook_path)
    else:
        path = Path(workbook_name)

    if path.is_absolute():
        return path

    project_root = Path(__file__).resolve().parents[1]
    candidates = [
        Path.cwd() / path,
        project_root / path,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


def open_workbook(excel_app: Any, workbook_path: str | Path) -> Any:
    path = Path(workbook_path)

    if not path.exists():
        raise ExcelComAccessError(f"Workbook nao encontrado no disco: {path}")

    workbooks = safe_getattr(excel_app, "Workbooks")
    open_method = safe_getattr(workbooks, "Open")

    if not callable(open_method):
        raise ExcelComAccessError("Excel.Workbooks.Open indisponivel via COM")

    try:
        return open_method(str(path))
    except Exception as exc:
        raise ExcelComAccessError(
            f"Falha ao abrir workbook via Excel COM: {path}: {exc}"
        ) from exc


def get_or_open_workbook(
    excel_app: Any,
    workbook_name: str,
    workbook_path: str | Path | None = None,
) -> Any:
    workbook = find_open_workbook(excel_app, workbook_name)

    if workbook is not None:
        return workbook

    path = resolve_workbook_path(workbook_name, workbook_path)
    opened = open_workbook(excel_app, path)

    workbook = find_open_workbook(excel_app, workbook_name)

    if workbook is not None:
        return workbook

    if opened is not None:
        return opened

    raise ExcelComAccessError(
        f"Workbook aberto, mas nao localizado no Excel: {workbook_name}"
    )


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


def get_excel_application_with_workbook(workbook_name: str) -> Any:
    """Varre o ROT (Running Object Table) e retorna a instancia do Excel
    que possui o workbook alvo aberto.

    Resolve o problema de multiplas instancias do Excel abertas
    simultaneamente, onde GetActiveObject() pode retornar uma instancia
    diferente daquela que contem o workbook desejado.
    """
    import pythoncom

    target = normalize_com_name(Path(workbook_name).name)
    context = pythoncom.CreateBindCtx(0)
    rot = pythoncom.GetRunningObjectTable()

    last_error: Exception | None = None

    for moniker in rot:
        try:
            display_name = moniker.GetDisplayName(context, None)
        except Exception as exc:
            last_error = exc
            continue

        if target not in normalize_com_name(display_name):
            continue

        try:
            workbook = rot.GetObject(moniker)
            application = safe_getattr(workbook, "Application")

            if application is not None:
                return application
        except Exception as exc:
            last_error = exc
            continue

    detail = f" ultimo erro: {last_error}" if last_error else ""
    raise ExcelComAccessError(
        f"Nenhuma instancia do Excel com '{workbook_name}' aberto foi "
        f"encontrada no ROT.{detail}"
    )


def get_excel_application_for_workbook(
    workbook_name: str,
    fallback_to_active: bool = True,
) -> Any:
    """Tenta localizar a instancia correta do Excel pelo workbook alvo.

    Se nao encontrar via ROT e fallback_to_active=True, cai para
    GetActiveObject() como ultimo recurso (comportamento legado).
    """
    try:
        return get_excel_application_with_workbook(workbook_name)
    except ExcelComAccessError:
        if not fallback_to_active:
            raise
        return get_active_excel_application()
