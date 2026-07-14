from __future__ import annotations

from datetime import datetime, timezone

from rtd_bridge.excel_rtd_connection_status import (
    DEFAULT_WORKBOOK_NAME,
    DEFAULT_WORKSHEET_NAME,
    REQUIRED_OPTION_QUOTE_HEADERS,
    ExcelRtdConnectionStatus,
)
from rtd_bridge.excel_rtd_connection_status_presenter import (
    build_excel_rtd_status_view_model,
    get_excel_rtd_status_payload,
    get_excel_rtd_status_view_model,
)


FIXED_CHECKED_AT = datetime(2026, 7, 10, 8, 30, 0, tzinfo=timezone.utc)


def _ready_status() -> ExcelRtdConnectionStatus:
    return ExcelRtdConnectionStatus(
        pywin32_available=True,
        excel_running=True,
        workbook_open=True,
        worksheet_available=True,
        required_headers_ok=True,
        workbook_name=DEFAULT_WORKBOOK_NAME,
        worksheet_name=DEFAULT_WORKSHEET_NAME,
        workbook_full_name=f"C:/tmp/{DEFAULT_WORKBOOK_NAME}",
        detected_headers=REQUIRED_OPTION_QUOTE_HEADERS,
        missing_headers=(),
        message="RTD Excel pronto para leitura.",
    )


def test_build_view_model_for_ready_status() -> None:
    view_model = build_excel_rtd_status_view_model(
        status=_ready_status(),
        checked_at=FIXED_CHECKED_AT,
    )

    assert view_model.ready is True
    assert view_model.severity == "ok"
    assert view_model.title == "RTD Excel online"
    assert view_model.message == "RTD Excel pronto para leitura."
    assert view_model.checked_at == FIXED_CHECKED_AT.isoformat()
    assert view_model.workbook_name == DEFAULT_WORKBOOK_NAME
    assert view_model.worksheet_name == DEFAULT_WORKSHEET_NAME
    assert view_model.missing_headers == ()
    assert len(view_model.checks) == 5
    assert all(check.ok for check in view_model.checks)


def test_payload_is_serializable_dict_for_ready_status() -> None:
    view_model = build_excel_rtd_status_view_model(
        status=_ready_status(),
        checked_at=FIXED_CHECKED_AT,
    )

    payload = view_model.to_dict()

    assert payload["ready"] is True
    assert payload["severity"] == "ok"
    assert payload["title"] == "RTD Excel online"
    assert payload["checked_at"] == FIXED_CHECKED_AT.isoformat()
    assert payload["detected_headers"] == list(REQUIRED_OPTION_QUOTE_HEADERS)
    assert payload["missing_headers"] == []
    assert len(payload["checks"]) == 5
    assert payload["checks"][0] == {
        "key": "pywin32_available",
        "label": "pywin32 disponível",
        "ok": True,
        "detail": "OK",
    }


def test_build_view_model_for_missing_workbook_status() -> None:
    status = ExcelRtdConnectionStatus(
        pywin32_available=True,
        excel_running=True,
        workbook_open=False,
        worksheet_available=False,
        required_headers_ok=False,
        workbook_name=DEFAULT_WORKBOOK_NAME,
        worksheet_name=DEFAULT_WORKSHEET_NAME,
        missing_headers=REQUIRED_OPTION_QUOTE_HEADERS,
        message=f"Workbook obrigatório não está aberto: {DEFAULT_WORKBOOK_NAME}",
    )

    view_model = build_excel_rtd_status_view_model(
        status=status,
        checked_at=FIXED_CHECKED_AT,
    )

    assert view_model.ready is False
    assert view_model.severity == "warning"
    assert view_model.title == "Workbook RTD não aberto"

    checks_by_key = {check.key: check for check in view_model.checks}

    assert checks_by_key["pywin32_available"].ok is True
    assert checks_by_key["excel_running"].ok is True
    assert checks_by_key["workbook_open"].ok is False
    assert checks_by_key["worksheet_available"].ok is False
    assert checks_by_key["required_headers_ok"].ok is False


def test_build_view_model_for_missing_header_status() -> None:
    status = ExcelRtdConnectionStatus(
        pywin32_available=True,
        excel_running=True,
        workbook_open=True,
        worksheet_available=True,
        required_headers_ok=False,
        workbook_name=DEFAULT_WORKBOOK_NAME,
        worksheet_name=DEFAULT_WORKSHEET_NAME,
        workbook_full_name=f"C:/tmp/{DEFAULT_WORKBOOK_NAME}",
        detected_headers=tuple(
            header
            for header in REQUIRED_OPTION_QUOTE_HEADERS
            if header != "iv"
        ),
        missing_headers=("iv",),
        message="Cabeçalho obrigatório ausente na aba RTD_OPTION_QUOTES: iv",
    )

    view_model = build_excel_rtd_status_view_model(
        status=status,
        checked_at=FIXED_CHECKED_AT,
    )

    assert view_model.ready is False
    assert view_model.severity == "error"
    assert view_model.title == "Cabeçalhos RTD inválidos"
    assert view_model.missing_headers == ("iv",)

    checks_by_key = {check.key: check for check in view_model.checks}

    assert checks_by_key["required_headers_ok"].ok is False
    assert checks_by_key["required_headers_ok"].detail == "Ausentes: iv"


def test_get_view_model_uses_injected_status_checker() -> None:
    calls = []

    def fake_status_checker(**kwargs):
        calls.append(kwargs)
        return _ready_status()

    view_model = get_excel_rtd_status_view_model(
        checked_at=FIXED_CHECKED_AT,
        status_checker=fake_status_checker,
    )

    assert view_model.ready is True
    assert view_model.title == "RTD Excel online"
    assert len(calls) == 1
    assert calls[0]["workbook_name"] == DEFAULT_WORKBOOK_NAME
    assert calls[0]["worksheet_name"] == DEFAULT_WORKSHEET_NAME
    assert calls[0]["required_headers"] == REQUIRED_OPTION_QUOTE_HEADERS
    assert calls[0]["excel_app"] is None


def test_get_payload_uses_injected_status_checker() -> None:
    def fake_status_checker(**kwargs):
        return _ready_status()

    payload = get_excel_rtd_status_payload(
        checked_at=FIXED_CHECKED_AT,
        status_checker=fake_status_checker,
    )

    assert payload["ready"] is True
    assert payload["severity"] == "ok"
    assert payload["title"] == "RTD Excel online"
    assert payload["workbook_name"] == DEFAULT_WORKBOOK_NAME
    assert payload["worksheet_name"] == DEFAULT_WORKSHEET_NAME
