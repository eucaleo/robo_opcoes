from typing import List, Any
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

from dto.robo_leg_dto import RoboLegDTO, CVType, CallPutType, FonteType
from utils.leg_normalizers import LegNormalizer


@dataclass
class ValidationError:
    row_index: int
    field: str
    value: Any
    error_message: str
    severity: str = "ERROR"  # ERROR, WARNING, INFO


@dataclass
class ValidationReport:
    total_rows: int
    valid_rows: int
    errors: List[ValidationError]
    warnings: List[ValidationError]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def is_ok(self) -> bool:
        return self.is_valid

    @property
    def error_rate(self) -> float:
        return len(self.errors) / self.total_rows if self.total_rows > 0 else 0

    def summary(self) -> str:
        return f"""
Relatório de Validação:
- Total de linhas: {self.total_rows}
- Linhas válidas: {self.valid_rows}
- Erros: {len(self.errors)}
- Warnings: {len(self.warnings)}
- Taxa de erro: {self.error_rate:.2%}
"""


class LegValidator:
    def __init__(self):
        self.required_fields = ["aba", "timestamp", "cv", "call_put", "strike", "quant", "ativo", "vencimento"]

    def validate_dataframe(self, df: pd.DataFrame) -> ValidationReport:
        """Valida um DataFrame completo de pernas"""
        errors: List[ValidationError] = []
        warnings: List[ValidationError] = []
        valid_count = 0

        for idx, row in df.iterrows():
            row_errors = self._validate_row(row, idx)

            row_errors_only = [e for e in row_errors if e.severity == "ERROR"]
            row_warnings_only = [e for e in row_errors if e.severity == "WARNING"]

            errors.extend(row_errors_only)
            warnings.extend(row_warnings_only)

            if len(row_errors_only) == 0:
                valid_count += 1

        return ValidationReport(
            total_rows=len(df),
            valid_rows=valid_count,
            errors=errors,
            warnings=warnings,
        )

    def _validate_row(self, row: pd.Series, row_index: int) -> List[ValidationError]:
        """Valida uma linha individual"""
        errors: List[ValidationError] = []

        for field in self.required_fields:
            if field not in row or pd.isna(row[field]) or row[field] is None:
                errors.append(
                    ValidationError(
                        row_index=row_index,
                        field=field,
                        value=row.get(field),
                        error_message=f"Campo obrigatório '{field}' está ausente ou nulo",
                        severity="ERROR",
                    )
                )

        if any(e.field in ["timestamp", "aba", "vencimento"] for e in errors if e.severity == "ERROR"):
            return errors

        try:
            timestamp = LegNormalizer.parse_timestamp(row.get("timestamp"))

            now = datetime.now()
            if timestamp < datetime(2020, 1, 1):
                errors.append(
                    ValidationError(
                        row_index=row_index,
                        field="timestamp",
                        value=row.get("timestamp"),
                        error_message="Timestamp anterior a 2020",
                        severity="WARNING",
                    )
                )
            elif timestamp > now:
                errors.append(
                    ValidationError(
                        row_index=row_index,
                        field="timestamp",
                        value=row.get("timestamp"),
                        error_message="Timestamp no futuro",
                        severity="WARNING",
                    )
                )

        except Exception as e:
            errors.append(
                ValidationError(
                    row_index=row_index,
                    field="timestamp",
                    value=row.get("timestamp"),
                    error_message=f"Timestamp inválido: {str(e)}",
                    severity="ERROR",
                )
            )

        self._validate_numeric_fields(row, row_index, errors)
        self._validate_enum_fields(row, row_index, errors)
        self._validate_business_rules(row, row_index, errors)

        return errors

    def _validate_numeric_fields(self, row: pd.Series, row_index: int, errors: List[ValidationError]):
        """Valida campos numéricos"""
        try:
            strike = float(row.get("strike", 0))
            if strike <= 0:
                errors.append(
                    ValidationError(
                        row_index=row_index,
                        field="strike",
                        value=row.get("strike"),
                        error_message="Strike deve ser positivo",
                        severity="ERROR",
                    )
                )
        except (ValueError, TypeError):
            errors.append(
                ValidationError(
                    row_index=row_index,
                    field="strike",
                    value=row.get("strike"),
                    error_message="Strike deve ser um número",
                    severity="ERROR",
                )
            )

        try:
            quant = int(row.get("quant", 0))
            if quant <= 0:
                errors.append(
                    ValidationError(
                        row_index=row_index,
                        field="quant",
                        value=row.get("quant"),
                        error_message="Quantidade deve ser positiva",
                        severity="ERROR",
                    )
                )
        except (ValueError, TypeError):
            errors.append(
                ValidationError(
                    row_index=row_index,
                    field="quant",
                    value=row.get("quant"),
                    error_message="Quantidade deve ser um número inteiro",
                    severity="ERROR",
                )
            )

    def _validate_enum_fields(self, row: pd.Series, row_index: int, errors: List[ValidationError]):
        """Valida campos que devem seguir enums"""
        try:
            LegNormalizer.normalize_cv(row.get("cv"))
        except Exception as e:
            errors.append(
                ValidationError(
                    row_index=row_index,
                    field="cv",
                    value=row.get("cv"),
                    error_message=f"Valor cv inválido: {str(e)}",
                    severity="ERROR",
                )
            )

        try:
            LegNormalizer.normalize_call_put(row.get("call_put"))
        except Exception as e:
            errors.append(
                ValidationError(
                    row_index=row_index,
                    field="call_put",
                    value=row.get("call_put"),
                    error_message=f"Valor call_put inválido: {str(e)}",
                    severity="ERROR",
                )
            )

    def _validate_business_rules(self, row: pd.Series, row_index: int, errors: List[ValidationError]):
        """Valida regras de negócio"""
        try:
            timestamp = LegNormalizer.parse_timestamp(row.get("timestamp"))
            vencimento = LegNormalizer.parse_vencimento(row.get("vencimento"))

            if vencimento <= timestamp:
                errors.append(
                    ValidationError(
                        row_index=row_index,
                        field="vencimento",
                        value=row.get("vencimento"),
                        error_message="Vencimento deve ser posterior ao timestamp",
                        severity="ERROR",
                    )
                )

        except Exception:
            pass

        ativo = str(row.get("ativo", "")).strip()
        if not ativo:
            errors.append(
                ValidationError(
                    row_index=row_index,
                    field="ativo",
                    value=row.get("ativo"),
                    error_message="Ativo não pode estar vazio",
                    severity="ERROR",
                )
            )

        aba = str(row.get("aba", "")).strip()
        if not aba:
            errors.append(
                ValidationError(
                    row_index=row_index,
                    field="aba",
                    value=row.get("aba"),
                    error_message="Aba não pode estar vazia",
                    severity="ERROR",
                )
            )

    def validate_and_report(self, df: pd.DataFrame, print_details: bool = True) -> ValidationReport:
        """Valida e imprime relatório detalhado"""
        report = self.validate_dataframe(df)

        if print_details:
            print(report.summary())

            if report.errors:
                print("\n=== ERROS ENCONTRADOS ===")
                for error in report.errors[:10]:
                    print(f"Linha {error.row_index}: {error.field} = '{error.value}' - {error.error_message}")

                if len(report.errors) > 10:
                    print(f"... e mais {len(report.errors) - 10} erros")

            if report.warnings:
                print("\n=== WARNINGS ===")
                for warning in report.warnings[:5]:
                    print(f"Linha {warning.row_index}: {warning.field} = '{warning.value}' - {warning.error_message}")

        return report


def validate_legs(legs: List[RoboLegDTO]) -> ValidationReport:
    """
    Valida lista de RoboLegDTO já normalizados.
    Mantém o mesmo contrato de ValidationReport usado no validador tabular.
    """
    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

    for idx, leg in enumerate(legs):
        if not str(leg.aba).strip():
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="aba",
                    value=leg.aba,
                    error_message="Aba não pode estar vazia",
                    severity="ERROR",
                )
            )

        if leg.timestamp < datetime(2020, 1, 1):
            warnings.append(
                ValidationError(
                    row_index=idx,
                    field="timestamp",
                    value=leg.timestamp,
                    error_message="Timestamp anterior a 2020",
                    severity="WARNING",
                )
            )

        if not isinstance(leg.cv, CVType):
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="cv",
                    value=leg.cv,
                    error_message="CV inválido",
                    severity="ERROR",
                )
            )

        if not isinstance(leg.call_put, CallPutType):
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="call_put",
                    value=leg.call_put,
                    error_message="Call/Put inválido",
                    severity="ERROR",
                )
            )

        if not isinstance(leg.fonte, FonteType):
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="fonte",
                    value=leg.fonte,
                    error_message="Fonte inválida",
                    severity="ERROR",
                )
            )

        if leg.quant <= 0:
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="quant",
                    value=leg.quant,
                    error_message="Quantidade deve ser positiva",
                    severity="ERROR",
                )
            )

        if leg.strike <= 0:
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="strike",
                    value=leg.strike,
                    error_message="Strike deve ser positivo",
                    severity="ERROR",
                )
            )

        if not str(leg.ativo).strip():
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="ativo",
                    value=leg.ativo,
                    error_message="Ativo não pode estar vazio",
                    severity="ERROR",
                )
            )

        if leg.vencimento is None:
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="vencimento",
                    value=leg.vencimento,
                    error_message="Vencimento não pode ser nulo",
                    severity="ERROR",
                )
            )
        elif leg.vencimento <= leg.timestamp:
            errors.append(
                ValidationError(
                    row_index=idx,
                    field="vencimento",
                    value=leg.vencimento,
                    error_message="Vencimento deve ser posterior ao timestamp",
                    severity="ERROR",
                )
            )

    valid_rows = len(legs) - len({e.row_index for e in errors})

    return ValidationReport(
        total_rows=len(legs),
        valid_rows=max(valid_rows, 0),
        errors=errors,
        warnings=warnings,
    )
