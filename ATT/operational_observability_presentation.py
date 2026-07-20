from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ATT.operational_observability_service import OperationalObservabilitySummary


HEALTH_LABELS = {
    "ok": "OK",
    "attention": "Atencao",
    "warning": "Aviso",
    "unknown": "Desconhecido",
}

RETENTION_LABELS = {
    "simulated": "Simulada",
    "not_requested": "Nao solicitada",
    "not_available": "Nao disponivel",
    "unavailable": "Indisponivel",
}


@dataclass(frozen=True)
class OperationalObservabilityPresentation:
    title: str
    general_state: str
    indicators: tuple[tuple[str, str], ...]
    critical_tables: tuple[tuple[str, str], ...]
    diagnostic_message: str
    read_only_notice: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "general_state": self.general_state,
            "indicators": list(self.indicators),
            "critical_tables": list(self.critical_tables),
            "diagnostic_message": self.diagnostic_message,
            "read_only_notice": self.read_only_notice,
        }

    def to_text(self) -> str:
        lines = [
            self.title,
            f"Estado geral: {self.general_state}",
            "",
            "Indicadores principais:",
        ]

        for label, value in self.indicators:
            lines.append(f"- {label}: {value}")

        lines.extend(
            [
                "",
                "Tabelas criticas:",
            ]
        )

        for label, value in self.critical_tables:
            lines.append(f"- {label}: {value}")

        lines.extend(
            [
                "",
                f"Mensagem: {self.diagnostic_message}",
                f"Aviso: {self.read_only_notice}",
            ]
        )

        return "\n".join(lines)


def build_operational_observability_presentation(
    summary: OperationalObservabilitySummary,
) -> OperationalObservabilityPresentation:
    general_state = _health_label(summary.health)

    indicators = (
        ("Banco local", summary.database_path),
        ("Banco encontrado", _yes_no(summary.database_exists)),
        ("Tabelas observadas", str(summary.table_count)),
        ("Registros observados", str(summary.total_record_count)),
        ("Retencao", _retention_label(summary.retention_status)),
        ("Candidatos de retencao", str(summary.retention_total_candidates)),
        ("Saude operacional", general_state),
    )

    critical_tables = tuple(
        (table_name, _present_absent(is_present))
        for table_name, is_present in sorted(summary.critical_tables_present.items())
    )

    return OperationalObservabilityPresentation(
        title="Observabilidade operacional",
        general_state=general_state,
        indicators=indicators,
        critical_tables=critical_tables,
        diagnostic_message=summary.message,
        read_only_notice=(
            "informacao somente leitura. Nenhuma acao operacional foi executada."
        ),
    )


def format_operational_observability_presentation(
    summary: OperationalObservabilitySummary,
) -> str:
    return build_operational_observability_presentation(summary).to_text()


def _health_label(value: str) -> str:
    return HEALTH_LABELS.get(value, value)


def _retention_label(value: str) -> str:
    return RETENTION_LABELS.get(value, value)


def _yes_no(value: bool) -> str:
    return "sim" if value else "nao"


def _present_absent(value: bool) -> str:
    return "presente" if value else "ausente"
