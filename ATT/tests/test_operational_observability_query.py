import inspect

import ATT.operational_observability_query as query
from ATT.operational_observability_query import (
    DEFAULT_OPERATIONAL_OBSERVABILITY_DATABASE_PATH,
    DEFAULT_OPERATIONAL_OBSERVABILITY_RETENTION_DAYS,
    get_current_operational_observability_presentation,
    get_current_operational_observability_text,
)
from ATT.operational_observability_service import OperationalObservabilitySummary


def test_query_builds_current_presentation_from_service_summary(monkeypatch):
    calls = []

    def fake_build_summary(database_path, *, retention_days, retention_today):
        calls.append(
            {
                "database_path": database_path,
                "retention_days": retention_days,
                "retention_today": retention_today,
            }
        )
        return _summary(database_path=database_path)

    monkeypatch.setattr(
        query,
        "build_operational_observability_summary",
        fake_build_summary,
    )

    presentation = get_current_operational_observability_presentation(
        "dados/app.db",
        retention_days=365,
        retention_today="2026-07-10",
    )

    assert calls == [
        {
            "database_path": "dados/app.db",
            "retention_days": 365,
            "retention_today": "2026-07-10",
        }
    ]
    assert presentation.title == "Observabilidade operacional"
    assert presentation.general_state == "OK"
    assert ("Banco local", "dados/app.db") in presentation.indicators
    assert ("Retencao", "Simulada") in presentation.indicators


def test_query_text_preserves_read_only_notice_and_no_action_message(monkeypatch):
    def fake_build_summary(database_path, *, retention_days, retention_today):
        return _summary(database_path=database_path)

    monkeypatch.setattr(
        query,
        "build_operational_observability_summary",
        fake_build_summary,
    )

    text = get_current_operational_observability_text(
        "dados/app.db",
        retention_days=365,
        retention_today="2026-07-10",
    )

    assert "Observabilidade operacional" in text
    assert "- Banco local: dados/app.db" in text
    assert "- Retencao: Simulada" in text
    assert "Aviso: informacao somente leitura" in text
    assert "Nenhuma acao operacional foi executada" in text


def test_query_uses_safe_defaults(monkeypatch):
    calls = []

    def fake_build_summary(database_path, *, retention_days, retention_today):
        calls.append((database_path, retention_days, retention_today))
        return _summary(database_path=database_path)

    monkeypatch.setattr(
        query,
        "build_operational_observability_summary",
        fake_build_summary,
    )

    presentation = get_current_operational_observability_presentation(
        retention_today="2026-07-10"
    )

    assert calls == [
        (
            DEFAULT_OPERATIONAL_OBSERVABILITY_DATABASE_PATH,
            DEFAULT_OPERATIONAL_OBSERVABILITY_RETENTION_DAYS,
            "2026-07-10",
        )
    ]
    assert presentation.general_state == "OK"


def test_query_module_does_not_reference_ui_excel_com_or_subprocess():
    source = inspect.getsource(query).lower()

    forbidden_terms = (
        "tkinter",
        "pyqt",
        "pyside",
        "win32com",
        "comtypes",
        "subprocess",
        "popen",
        "excel",
    )

    for term in forbidden_terms:
        assert term not in source


def _summary(
    *,
    database_path="dados/app.db",
    database_exists=True,
    table_count=11,
    total_record_count=1245,
    critical_tables_present=None,
    retention_status="simulated",
    retention_total_candidates=0,
    health="ok",
    message="Banco observado com saude ok.",
):
    if critical_tables_present is None:
        critical_tables_present = {
            "payoff_curve_points": True,
            "pricing_executions": True,
            "structure_leg_snapshots": True,
            "structure_legs": True,
            "structure_snapshots": True,
            "structures": True,
        }

    return OperationalObservabilitySummary(
        database_path=database_path,
        database_exists=database_exists,
        table_count=table_count,
        total_record_count=total_record_count,
        critical_tables_present=critical_tables_present,
        retention_status=retention_status,
        retention_total_candidates=retention_total_candidates,
        health=health,
        message=message,
    )
