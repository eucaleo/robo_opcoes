from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from rtd_bridge.excel_rtd_connection_status import (
    DEFAULT_WORKBOOK_NAME,
    DEFAULT_WORKSHEET_NAME,
    REQUIRED_OPTION_QUOTE_HEADERS,
    ExcelRtdConnectionStatus,
    check_excel_rtd_connection_status,
)


@dataclass(frozen=True)
class ExcelRtdStatusCheckViewModel:
    key: str
    label: str
    ok: bool
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "ok": self.ok,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class ExcelRtdStatusViewModel:
    ready: bool
    severity: str
    title: str
    message: str
    checked_at: str
    workbook_name: str
    worksheet_name: str
    workbook_full_name: str | None
    detected_headers: tuple[str, ...]
    missing_headers: tuple[str, ...]
    checks: tuple[ExcelRtdStatusCheckViewModel, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "severity": self.severity,
            "title": self.title,
            "message": self.message,
            "checked_at": self.checked_at,
            "workbook_name": self.workbook_name,
            "worksheet_name": self.worksheet_name,
            "workbook_full_name": self.workbook_full_name,
            "detected_headers": list(self.detected_headers),
            "missing_headers": list(self.missing_headers),
            "checks": [check.to_dict() for check in self.checks],
        }


ExcelRtdStatusChecker = Callable[..., ExcelRtdConnectionStatus]


def get_excel_rtd_status_view_model(
    workbook_name: str = DEFAULT_WORKBOOK_NAME,
    worksheet_name: str = DEFAULT_WORKSHEET_NAME,
    required_headers: tuple[str, ...] = REQUIRED_OPTION_QUOTE_HEADERS,
    excel_app: Any | None = None,
    checked_at: datetime | None = None,
    status_checker: ExcelRtdStatusChecker = check_excel_rtd_connection_status,
) -> ExcelRtdStatusViewModel:
    status = status_checker(
        workbook_name=workbook_name,
        worksheet_name=worksheet_name,
        required_headers=required_headers,
        excel_app=excel_app,
    )

    return build_excel_rtd_status_view_model(
        status=status,
        checked_at=checked_at,
    )


def get_excel_rtd_status_payload(
    workbook_name: str = DEFAULT_WORKBOOK_NAME,
    worksheet_name: str = DEFAULT_WORKSHEET_NAME,
    required_headers: tuple[str, ...] = REQUIRED_OPTION_QUOTE_HEADERS,
    excel_app: Any | None = None,
    checked_at: datetime | None = None,
    status_checker: ExcelRtdStatusChecker = check_excel_rtd_connection_status,
) -> dict[str, Any]:
    view_model = get_excel_rtd_status_view_model(
        workbook_name=workbook_name,
        worksheet_name=worksheet_name,
        required_headers=required_headers,
        excel_app=excel_app,
        checked_at=checked_at,
        status_checker=status_checker,
    )

    return view_model.to_dict()


def build_excel_rtd_status_view_model(
    status: ExcelRtdConnectionStatus,
    checked_at: datetime | None = None,
) -> ExcelRtdStatusViewModel:
    effective_checked_at = checked_at or datetime.now(timezone.utc)

    return ExcelRtdStatusViewModel(
        ready=status.is_ready,
        severity=_resolve_severity(status),
        title=_resolve_title(status),
        message=status.message,
        checked_at=effective_checked_at.isoformat(),
        workbook_name=status.workbook_name,
        worksheet_name=status.worksheet_name,
        workbook_full_name=status.workbook_full_name,
        detected_headers=status.detected_headers,
        missing_headers=status.missing_headers,
        checks=_build_checks(status),
    )


def _resolve_severity(status: ExcelRtdConnectionStatus) -> str:
    if status.is_ready:
        return "ok"

    if not status.pywin32_available:
        return "error"

    if not status.excel_running:
        return "error"

    if not status.workbook_open:
        return "warning"

    if not status.worksheet_available:
        return "warning"

    if not status.required_headers_ok:
        return "error"

    return "warning"


def _resolve_title(status: ExcelRtdConnectionStatus) -> str:
    if status.is_ready:
        return "RTD Excel online"

    if not status.pywin32_available:
        return "pywin32 indisponível"

    if not status.excel_running:
        return "Excel não encontrado"

    if not status.workbook_open:
        return "Workbook RTD não aberto"

    if not status.worksheet_available:
        return "Aba RTD indisponível"

    if not status.required_headers_ok:
        return "Cabeçalhos RTD inválidos"

    return "RTD Excel indisponível"


def _build_checks(
    status: ExcelRtdConnectionStatus,
) -> tuple[ExcelRtdStatusCheckViewModel, ...]:
    return (
        ExcelRtdStatusCheckViewModel(
            key="pywin32_available",
            label="pywin32 disponível",
            ok=status.pywin32_available,
            detail=_bool_detail(status.pywin32_available),
        ),
        ExcelRtdStatusCheckViewModel(
            key="excel_running",
            label="Excel aberto",
            ok=status.excel_running,
            detail=_bool_detail(status.excel_running),
        ),
        ExcelRtdStatusCheckViewModel(
            key="workbook_open",
            label=f"Workbook aberto: {status.workbook_name}",
            ok=status.workbook_open,
            detail=_workbook_detail(status),
        ),
        ExcelRtdStatusCheckViewModel(
            key="worksheet_available",
            label=f"Aba disponível: {status.worksheet_name}",
            ok=status.worksheet_available,
            detail=_bool_detail(status.worksheet_available),
        ),
        ExcelRtdStatusCheckViewModel(
            key="required_headers_ok",
            label="Cabeçalhos obrigatórios",
            ok=status.required_headers_ok,
            detail=_headers_detail(status),
        ),
    )


def _bool_detail(ok: bool) -> str:
    if ok:
        return "OK"

    return "Falhou"


def _workbook_detail(status: ExcelRtdConnectionStatus) -> str:
    if not status.workbook_open:
        return "Falhou"

    if status.workbook_full_name:
        return status.workbook_full_name

    return "OK"


def _headers_detail(status: ExcelRtdConnectionStatus) -> str:
    if status.required_headers_ok:
        return (
            f"{len(status.detected_headers)} cabeçalhos detectados; "
            f"{len(REQUIRED_OPTION_QUOTE_HEADERS)} obrigatórios validados"
        )

    if status.missing_headers:
        return "Ausentes: " + ", ".join(status.missing_headers)

    return "Falhou"
