from ATT.operational_observability_presentation import (
    build_operational_observability_presentation,
    format_operational_observability_presentation,
)
from ATT.operational_observability_service import OperationalObservabilitySummary


def test_build_presentation_uses_stable_main_indicators():
    summary = _summary()

    presentation = build_operational_observability_presentation(summary)

    assert presentation.title == "Observabilidade operacional"
    assert presentation.general_state == "OK"
    assert presentation.indicators == (
        ("Banco local", "dados/app.db"),
        ("Banco encontrado", "sim"),
        ("Tabelas observadas", "11"),
        ("Registros observados", "1245"),
        ("Retencao", "Simulada"),
        ("Candidatos de retencao", "0"),
        ("Saude operacional", "OK"),
    )
    assert presentation.diagnostic_message == "Banco observado com saude ok."
    assert "somente leitura" in presentation.read_only_notice


def test_format_presentation_contains_read_only_notice_and_no_action_claim():
    summary = _summary()

    text = format_operational_observability_presentation(summary)

    assert "Observabilidade operacional" in text
    assert "Estado geral: OK" in text
    assert "- Banco local: dados/app.db" in text
    assert "- Retencao: Simulada" in text
    assert "- Candidatos de retencao: 0" in text
    assert "Aviso: informacao somente leitura" in text
    assert "Nenhuma acao operacional foi executada" in text


def test_presentation_orders_critical_tables_by_name():
    summary = _summary(
        critical_tables_present={
            "structures": True,
            "payoff_curve_points": False,
            "pricing_executions": True,
        }
    )

    presentation = build_operational_observability_presentation(summary)

    assert presentation.critical_tables == (
        ("payoff_curve_points", "ausente"),
        ("pricing_executions", "presente"),
        ("structures", "presente"),
    )


def test_presentation_labels_warning_and_missing_database():
    summary = _summary(
        database_exists=False,
        table_count=0,
        total_record_count=0,
        retention_status="not_available",
        health="warning",
        message="Banco local nao encontrado.",
        critical_tables_present={"structures": False},
    )

    text = format_operational_observability_presentation(summary)

    assert "Estado geral: Aviso" in text
    assert "- Banco encontrado: nao" in text
    assert "- Retencao: Nao disponivel" in text
    assert "- structures: ausente" in text
    assert "Banco local nao encontrado." in text


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
            "structures": True,
            "pricing_executions": True,
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
