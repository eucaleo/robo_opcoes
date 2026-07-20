from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class ValidationErrorItem:
    code: str
    field: str
    aba: str


class ValidationReport:
    def __init__(self, errors: List[ValidationErrorItem] | None = None):
        self.errors = errors or []

    def is_ok(self) -> bool:
        return len(self.errors) == 0


def validate_legs(legs: list[Any]) -> ValidationReport:
    errors: list[ValidationErrorItem] = []

    for leg in legs:
        aba = getattr(leg, "aba", "") or ""

        cv = getattr(leg, "cv", None)
        if cv not in ("C", "V"):
            errors.append(
                ValidationErrorItem(
                    code="invalid_cv",
                    field="cv",
                    aba=aba,
                )
            )

        call_put = getattr(leg, "call_put", None)
        if call_put not in ("CALL", "PUT"):
            errors.append(
                ValidationErrorItem(
                    code="invalid_call_put",
                    field="call_put",
                    aba=aba,
                )
            )

        quant = getattr(leg, "quant", None)
        if not isinstance(quant, int) or quant <= 0:
            errors.append(
                ValidationErrorItem(
                    code="invalid_quant",
                    field="quant",
                    aba=aba,
                )
            )

        strike = getattr(leg, "strike", None)
        if strike is None:
            errors.append(
                ValidationErrorItem(
                    code="missing_strike",
                    field="strike",
                    aba=aba,
                )
            )

        ativo = getattr(leg, "ativo", None)
        if not ativo:
            errors.append(
                ValidationErrorItem(
                    code="missing_ativo",
                    field="ativo",
                    aba=aba,
                )
            )

    return ValidationReport(errors)
