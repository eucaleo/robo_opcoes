from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def safe_get(label: str, getter):
    try:
        return {
            "ok": True,
            "label": label,
            "value": getter(),
            "error": None,
        }
    except Exception as exc:
        return {
            "ok": False,
            "label": label,
            "value": None,
            "error": str(exc),
        }


def normalize_scalar(value: Any) -> Any:
    try:
        if value is None:
            return None

        if isinstance(value, (str, int, float, bool)):
            return value

        return str(value)
    except Exception:
        return None


def inspect_excel_application(excel: Any) -> dict[str, Any]:
    result: dict[str, Any] = {
        "application": {},
        "workbooks": [],
    }

    app_checks = [
        safe_get("Name", lambda: normalize_scalar(excel.Name)),
        safe_get("Version", lambda: normalize_scalar(excel.Version)),
        safe_get("Visible", lambda: normalize_scalar(excel.Visible)),
        safe_get("Hwnd", lambda: normalize_scalar(excel.Hwnd)),
        safe_get("Workbooks.Count", lambda: int(excel.Workbooks.Count)),
    ]

    for item in app_checks:
        result["application"][item["label"]] = {
            "ok": item["ok"],
            "value": item["value"],
            "error": item["error"],
        }

    count_item = next(
        item for item in app_checks if item["label"] == "Workbooks.Count"
    )

    if not count_item["ok"]:
        return result

    workbook_count = int(count_item["value"] or 0)

    for workbook_index in range(1, workbook_count + 1):
        workbook_info: dict[str, Any] = {
            "index": workbook_index,
            "name": None,
            "full_name": None,
            "path": None,
            "read_only": None,
            "sheets": [],
            "errors": [],
        }

        try:
            workbook = excel.Workbooks.Item(workbook_index)
        except Exception as exc:
            workbook_info["errors"].append(
                f"falha ao acessar workbook {workbook_index}: {exc}"
            )
            result["workbooks"].append(workbook_info)
            continue

        for field_name, getter in [
            ("name", lambda workbook=workbook: normalize_scalar(workbook.Name)),
            ("full_name", lambda workbook=workbook: normalize_scalar(workbook.FullName)),
            ("path", lambda workbook=workbook: normalize_scalar(workbook.Path)),
            ("read_only", lambda workbook=workbook: normalize_scalar(workbook.ReadOnly)),
        ]:
            item = safe_get(field_name, getter)
            if item["ok"]:
                workbook_info[field_name] = item["value"]
            else:
                workbook_info["errors"].append(
                    f"falha ao ler {field_name}: {item['error']}"
                )

        try:
            sheet_count = int(workbook.Worksheets.Count)
            for sheet_index in range(1, sheet_count + 1):
                try:
                    sheet = workbook.Worksheets.Item(sheet_index)
                    workbook_info["sheets"].append(
                        {
                            "index": sheet_index,
                            "name": normalize_scalar(sheet.Name),
                        }
                    )
                except Exception as exc:
                    workbook_info["errors"].append(
                        f"falha ao ler aba {sheet_index}: {exc}"
                    )
        except Exception as exc:
            workbook_info["errors"].append(f"falha ao contar abas: {exc}")

        result["workbooks"].append(workbook_info)

    return result


def build_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    expected_sheets = {
        "RTD-BTG",
        "LISTA",
        "RTD_OPTION_QUOTES",
    }

    workbooks = payload.get("workbooks", [])
    workbook_count = len(workbooks)

    matching_by_sheet = []

    for workbook in workbooks:
        sheet_names = {
            str(sheet.get("name") or "")
            for sheet in workbook.get("sheets", [])
        }

        found = sorted(expected_sheets.intersection(sheet_names))

        if found:
            matching_by_sheet.append(
                {
                    "name": workbook.get("name"),
                    "full_name": workbook.get("full_name"),
                    "found_expected_sheets": found,
                }
            )

    return {
        "workbook_count_seen": workbook_count,
        "expected_sheets": sorted(expected_sheets),
        "matching_workbooks_by_sheet": matching_by_sheet,
        "probable_issue": infer_probable_issue(payload, workbook_count, matching_by_sheet),
    }


def infer_probable_issue(
    payload: dict[str, Any],
    workbook_count: int,
    matching_by_sheet: list[dict[str, Any]],
) -> str:
    app = payload.get("application", {})
    count_info = app.get("Workbooks.Count", {})

    if not count_info.get("ok"):
        return "Excel acessivel parcialmente, mas Workbooks.Count falhou."

    if workbook_count == 0:
        return (
            "Python anexou em uma instancia do Excel sem workbooks. "
            "Possivel causa: existe outra instancia do Excel com a planilha RTD aberta."
        )

    if matching_by_sheet:
        return (
            "Workbook RTD encontrado por nome de aba. "
            "O nome real do arquivo provavelmente nao e LISTA_RTD.xlsm."
        )

    return (
        "Excel e workbooks foram vistos, mas nenhum workbook possui as abas esperadas."
    )


def main() -> int:
    try:
        import win32com.client
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "pywin32_unavailable",
                    "message": f"win32com indisponivel: {exc}",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "excel_unavailable",
                    "message": f"Excel nao esta aberto ou nao esta acessivel via COM: {exc}",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    payload = inspect_excel_application(excel)
    payload["analysis"] = build_analysis(payload)
    payload["ok"] = True
    payload["status"] = "ok"

    print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
