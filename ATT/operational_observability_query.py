from __future__ import annotations

from datetime import date

from ATT.operational_observability_presentation import (
    OperationalObservabilityPresentation,
    build_operational_observability_presentation,
)
from ATT.operational_observability_service import (
    build_operational_observability_summary,
)


DEFAULT_OPERATIONAL_OBSERVABILITY_DATABASE_PATH = "dados/app.db"
DEFAULT_OPERATIONAL_OBSERVABILITY_RETENTION_DAYS = 365


def get_current_operational_observability_presentation(
    database_path: str = DEFAULT_OPERATIONAL_OBSERVABILITY_DATABASE_PATH,
    *,
    retention_days: int = DEFAULT_OPERATIONAL_OBSERVABILITY_RETENTION_DAYS,
    retention_today: str | None = None,
) -> OperationalObservabilityPresentation:
    today = retention_today or date.today().isoformat()

    summary = build_operational_observability_summary(
        database_path,
        retention_days=retention_days,
        retention_today=today,
    )

    return build_operational_observability_presentation(summary)


def get_current_operational_observability_text(
    database_path: str = DEFAULT_OPERATIONAL_OBSERVABILITY_DATABASE_PATH,
    *,
    retention_days: int = DEFAULT_OPERATIONAL_OBSERVABILITY_RETENTION_DAYS,
    retention_today: str | None = None,
) -> str:
    presentation = get_current_operational_observability_presentation(
        database_path,
        retention_days=retention_days,
        retention_today=retention_today,
    )

    return presentation.to_text()
