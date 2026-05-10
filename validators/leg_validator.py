from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from dto.robo_leg_dto import RoboLegDTO
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
        self.required_fields = ['aba', 'timestamp', 'cv', 'call_put', 'strike', 'quant', 'ativo', 'vencimento']
    
    def validate_dataframe(self, df: pd.DataFrame) -> ValidationReport:
        """Valida um DataFrame completo de pernas"""
        errors = []
        warnings = []
        valid_count = 0
        
        for idx, row in df.iterrows():
            row_errors = self._validate_row(row, idx)
            
            # Separa erros de warnings
            row_errors_only = [e for e in row_errors if e.severity == "ERROR"]
            row_warnings_only = [e for e in row_errors if e.severity == "WARNING"]
            
            errors.extend(row_errors_only)
            warnings.extend(row_warnings_only)
            
            # Conta como válida se não tem erros críticos
            if len(row_errors_only) == 0:
                valid_count += 1
        
        return ValidationReport(
            total_rows=len(df),
            valid_rows=valid_count,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_row(self, row: pd.Series, row_index: int) -> List[ValidationError]:
        """Valida uma linha individual"""
        errors = []
        
        # 1. Campos obrigatórios presentes
        for field in self.required_fields:
            if field not in row or pd.isna(row[field]) or row[field] is None:
                errors.append(ValidationError(
                    row_index=row_index,
                    field=field,
                    value=row.get(field),
                    error_message=f"Campo obrigatório '{field}' está ausente ou nulo",
                    severity="ERROR"
                ))
        
        # Se faltam campos críticos, não adianta continuar
        if any(e.field in ['timestamp', 'aba'] for e in errors if e.severity == "ERROR"):
            return errors
        
        # 2. Validação de timestamp obrigatório
        try:
            timestamp = LegNormalizer.parse_timestamp(row.get('timestamp'))
            
            # Warning se timestamp é muito antigo ou futuro
            now = datetime.now()
            if timestamp < datetime(2020, 1, 1):
                errors.append(ValidationError(
                    row_index=row_index,
                    field='timestamp',
                    value=row.get('timestamp'),
                    error_message="Timestamp anterior a 2020",
                    severity="WARNING"
                ))
            elif timestamp > now:
                errors.append(ValidationError(
                    row_index=row_index,
                    field='timestamp',
                    value=row.get('timestamp'),
                    error_message="Timestamp no futuro",
                    severity="WARNING"
                ))
                
        except Exception as e:
            errors.append(ValidationError(
                row_index=row_index,
                field='timestamp',
                value=row.get('timestamp'),
                error_message=f"Timestamp inválido: {str(e)}",
                severity="ERROR"
            ))
        
        # 3. Validação de tipos e formatos
        self._validate_numeric_fields(row, row_index, errors)
        self._validate_enum_fields(row, row_index, errors)
        self._validate_business_rules(row, row_index, errors)
        
        return errors
    
    def _validate_numeric_fields(self, row: pd.Series, row_index: int, errors: List[ValidationError]):
        """Valida campos numéricos"""
        
        # Strike
        try:
            strike = float(row.get('strike', 0))
            if strike <= 0:
                errors.append(ValidationError(
                    row_index=row_index,
                    field='strike',
                    value=row.get('strike'),
                    error_message="Strike deve ser positivo",
                    severity="ERROR"
                ))
        except (ValueError, TypeError):
            errors.append(ValidationError(
                row_index=row_index,
                field='strike',
                value=row.get('strike'),
                error_message="Strike deve ser um número",
                severity="ERROR"
            ))
        
        # Quantidade
        try:
            quant = int(row.get('quant', 0))
            if quant <= 0:
                errors.append(ValidationError(
                    row_index=row_index,
                    field='quant',
                    value=row.get('quant'),
                    error_message="Quantidade deve ser positiva",
                    severity="ERROR"
                ))
        except (ValueError, TypeError):
            errors.append(ValidationError(
                row_index=row_index,
                field='quant',
                value=row.get('quant'),
                error_message="Quantidade deve ser um número inteiro",
                severity="ERROR"
            ))
    
    def _validate_enum_fields(self, row: pd.Series, row_index: int, errors: List[ValidationError]):
        """Valida campos que devem seguir enums"""
        
        # CV
        try:
            LegNormalizer.normalize_cv(row.get('cv'))
        except Exception as e:
            errors.append(ValidationError(
                row_index=row_index,
                field='cv',
                value=row.get('cv'),
                error_message=f"Valor cv inválido: {str(e)}",
                severity="ERROR"
            ))
        
        # Call/Put
        try:
            LegNormalizer.normalize_call_put(row.get('call_put'))
        except Exception as e:
            errors.append(ValidationError(
                row_index=row_index,
                field='call_put',
                value=row.get('call_put'),
                error_message=f"Valor call_put inválido: {str(e)}",
                severity="ERROR"
            ))
    
    def _validate_business_rules(self, row: pd.Series, row_index: int, errors: List[ValidationError]):
        """Valida regras de negócio"""
        
        # Vencimento deve ser posterior ao timestamp
        try:
            timestamp = LegNormalizer.parse_timestamp(row.get('timestamp'))
            vencimento = LegNormalizer.parse_vencimento(row.get('vencimento'))
            
            if vencimento <= timestamp:
                errors.append(ValidationError(
                    row_index=row_index,
                    field='vencimento',
                    value=row.get('vencimento'),
                    error_message="Vencimento deve ser posterior ao timestamp",
                    severity="ERROR"
                ))
                
        except Exception:
            # Erro já capturado nas validações de timestamp
            pass
        
        # Ativo não pode estar vazio
        ativo = str(row.get('ativo', '')).strip()
        if not ativo:
            errors.append(ValidationError(
                row_index=row_index,
                field='ativo',
                value=row.get('ativo'),
                error_message="Ativo não pode estar vazio",
                severity="ERROR"
            ))
        
        # Aba não pode estar vazia
        aba = str(row.get('aba', '')).strip()
        if not aba:
            errors.append(ValidationError(
                row_index=row_index,
                field='aba',
                value=row.get('aba'),
                error_message="Aba não pode estar vazia",
                severity="ERROR"
            ))

    def validate_and_report(self, df: pd.DataFrame, print_details: bool = True) -> ValidationReport:
        """Valida e imprime relatório detalhado"""
        report = self.validate_dataframe(df)
        
        if print_details:
            print(report.summary())
            
            if report.errors:
                print("\n=== ERROS ENCONTRADOS ===")
                for error in report.errors[:10]:  # Limita a 10 primeiros
                    print(f"Linha {error.row_index}: {error.field} = '{error.value}' - {error.error_message}")
                
                if len(report.errors) > 10:
                    print(f"... e mais {len(report.errors) - 10} erros")
            
            if report.warnings:
                print("\n=== WARNINGS ===")
                for warning in report.warnings[:5]:  # Limita a 5 primeiros
                    print(f"Linha {warning.row_index}: {warning.field} = '{warning.value}' - {warning.error_message}")
        
        return report
