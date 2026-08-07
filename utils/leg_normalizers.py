
# ---------------------------------------------------------------------------
# Frente 19C — adocao controlada dos normalizadores financeiros compartilhados
# ---------------------------------------------------------------------------
# Estes imports documentam e estabilizam o contrato de normalizacao financeira
# sem trocar o fluxo operacional amplo nesta etapa.
#
# Campos de risco/gregas devem preservar negativos e zero:
#   parse_optional_risk_float / parse_optional_greek_float
#
# Campos financeiros que exigem positividade continuam protegidos:
#   parse_optional_positive_float
#
# Campos em que zero e valido, mas negativo nao:
#   parse_optional_non_negative_float
try:
    from utils.financial_number_normalizers import (
        parse_optional_greek_float,
        parse_optional_non_negative_float,
        parse_optional_positive_float,
        parse_optional_risk_float,
        parse_optional_variation_float,
    )
except Exception:  # pragma: no cover - fallback defensivo para import parcial
    parse_optional_greek_float = None
    parse_optional_non_negative_float = None
    parse_optional_positive_float = None
    parse_optional_risk_float = None
    parse_optional_variation_float = None

from domain.refs.structure_ref import StructureRef
from datetime import datetime, timedelta
from typing import Union, Optional
import pandas as pd

from dto.robo_leg_dto import RoboLegDTO, CallPutType, CVType, FonteType


class LegNormalizer:

    @staticmethod
    def normalize_call_put(value: Union[str, int, None]) -> CallPutType:
        """
        Frente 13:
        option_type/call_put canonico aceita apenas CALL ou PUT por extenso.

        C/P nao sao aceitos aqui, pois C/V pertencem ao contrato de
        compra/venda da posicao.
        """
        if value is None:
            raise ValueError("call_put não pode ser None")

        value_str = str(value).strip().upper()

        if value_str == 'CALL':
            return CallPutType.CALL

        if value_str == 'PUT':
            return CallPutType.PUT

        raise ValueError(
            f"Valor call_put não reconhecido: {value}. "
            "Use CALL ou PUT por extenso."
        )

    @staticmethod
    def normalize_cv(value: Union[str, int, None]) -> CVType:
        """Normaliza C/V para enum padrão"""
        if value is None:
            raise ValueError("cv não pode ser None")

        value_str = str(value).upper().strip()

        compra_mappings = ['C', 'COMPRA', 'BUY', '1', 'LONG']
        venda_mappings = ['V', 'VENDA', 'SELL', '0', 'SHORT']

        if value_str in compra_mappings:
            return CVType.C
        elif value_str in venda_mappings:
            return CVType.V
        else:
            raise ValueError(f"Valor cv não reconhecido: {value}")

    @staticmethod
    def _excel_serial_to_datetime(serial: float) -> datetime:
        """
        Converte serial date do Excel para datetime.
        Base prática compatível com pandas/openpyxl:
        1899-12-30 + N dias
        """
        return datetime(1899, 12, 30) + timedelta(days=serial)

    @staticmethod
    def _try_parse_excel_serial(value) -> Optional[datetime]:
        """
        Tenta interpretar value como serial do Excel.
        Aceita:
        - int / float
        - strings numéricas, inclusive com vírgula decimal
        """
        if value is None:
            return None

        if isinstance(value, (int, float)):
            serial = float(value)
            return LegNormalizer._excel_serial_to_datetime(serial)

        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return None

            # evita tratar timestamps clássicos como número
            if "/" in raw or "-" in raw or ":" in raw:
                return None

            raw_num = raw.replace(",", ".")
            try:
                serial = float(raw_num)
                return LegNormalizer._excel_serial_to_datetime(serial)
            except ValueError:
                return None

        return None

    @staticmethod
    def parse_timestamp(value: Union[str, int, float, datetime, pd.Timestamp, None]) -> datetime:
        """Parser robusto para timestamp, incluindo serial Excel."""
        if value is None:
            raise ValueError("timestamp não pode ser None")

        if isinstance(value, datetime):
            return value

        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()

        # tenta serial Excel cedo, antes do pandas genérico
        excel_dt = LegNormalizer._try_parse_excel_serial(value)
        if excel_dt is not None:
            return excel_dt

        if isinstance(value, str):
            raw = value.strip()

            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%d',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y',
                '%Y%m%d_%H%M%S',
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(raw, fmt)
                except ValueError:
                    continue

            try:
                return pd.to_datetime(raw).to_pydatetime()
            except Exception:
                raise ValueError(f"Formato de timestamp não reconhecido: {value}")

        raise ValueError(f"Tipo de timestamp não suportado: {type(value)}")

    @staticmethod
    def parse_vencimento(value: Union[str, int, float, datetime, pd.Timestamp, None]) -> datetime:
        """Parser para vencimento (similar ao timestamp)"""
        return LegNormalizer.parse_timestamp(value)

    @staticmethod
    def normalize_fonte(value: Union[str, FonteType, None]) -> FonteType:
        """Normaliza fonte de dados"""
        if value is None:
            return FonteType.RTD

        if isinstance(value, FonteType):
            return value

        value_str = str(value).lower().strip()

        if value_str in ['manual', 'man', 'm']:
            return FonteType.MANUAL
        elif value_str in ['rtd', 'real_time', 'rt', 'auto']:
            return FonteType.RTD
        else:
            return FonteType.RTD

    @classmethod
    def from_dict(cls, data: dict, fonte: Optional[FonteType] = None) -> RoboLegDTO:
        """Cria DTO a partir de dicionário com normalização automática"""

        normalized_data = {
            'aba': str(data.get('aba', '')).strip(),
            'timestamp': cls.parse_timestamp(data.get('timestamp')),
            'cv': cls.normalize_cv(data.get('cv')),
            'call_put': cls.normalize_call_put(data.get('call_put')),
            'strike': float(data.get('strike', 0)),
            'quant': int(data.get('quant', 0)),
            'ativo': str(data.get('ativo', '')).strip().upper(),
            'vencimento': cls.parse_vencimento(data.get('vencimento')),
            'fonte': fonte or cls.normalize_fonte(data.get('fonte'))
        }

        optional_fields = ['id', 'preco', 'delta', 'gamma', 'theta', 'vega', 'created_at', 'updated_at']
        for field in optional_fields:
            if field in data and data[field] is not None:
                if field in ['created_at', 'updated_at']:
                    normalized_data[field] = cls.parse_timestamp(data[field])
                else:
                    normalized_data[field] = data[field]

        return RoboLegDTO(**normalized_data)

    @classmethod
    def from_dataframe_row(cls, row: pd.Series, fonte: Optional[FonteType] = None) -> RoboLegDTO:
        """Cria DTO a partir de linha do DataFrame"""
        return cls.from_dict(row.to_dict(), fonte)


def normalize_call_put(value):
    return LegNormalizer.normalize_call_put(value)


def normalize_cv(value):
    return LegNormalizer.normalize_cv(value)


def parse_timestamp(value):
    return LegNormalizer.parse_timestamp(value)


def parse_vencimento(value):
    return LegNormalizer.parse_vencimento(value)


def normalize_fonte(value):
    return LegNormalizer.normalize_fonte(value)

# Frente 13 - normalizacao explicita C/V versus CALL/PUT

class LegNormalizationError(ValueError):
    """Erro explicito para contratos invalidos de leg."""


def _normalize_token(value):
    if value is None:
        return ""
    return str(value).strip().upper()


def normalize_position_side(value):
    """
    Normaliza o lado operacional da posicao.

    Contrato:
      C, COMPRA, COMPRADO, LONG  -> COMPRADO
      V, VENDA, VENDIDO, SHORT   -> VENDIDO
    """
    token = _normalize_token(value)

    if token in {"C", "COMPRA", "COMPRADO", "LONG"}:
        return "COMPRADO"

    if token in {"V", "VENDA", "VENDIDO", "SHORT"}:
        return "VENDIDO"

    raise LegNormalizationError(
        f"position_side invalido: {value!r}. "
        "Use C/COMPRA/COMPRADO/LONG ou V/VENDA/VENDIDO/SHORT."
    )


def normalize_pricing_side(value):
    """
    Normaliza o lado tecnico usado pelo pricing.

    Contrato:
      C, COMPRA, COMPRADO, LONG  -> LONG
      V, VENDA, VENDIDO, SHORT   -> SHORT
    """
    position_side = normalize_position_side(value)

    if position_side == "COMPRADO":
        return "LONG"

    if position_side == "VENDIDO":
        return "SHORT"

    raise LegNormalizationError(f"pricing_side invalido: {value!r}")


def normalize_option_type(value):
    """
    Normaliza o tipo da opcao.

    Contrato canonico:
      CALL -> CALL
      PUT  -> PUT

    Importante:
      C e P nao sao aceitos como option_type canonico.
      C/V pertencem ao contrato de compra/venda, nao ao tipo da opcao.
      Valor desconhecido deve gerar erro explicito.
    """
    token = _normalize_token(value)

    if token in {"CALL", "PUT"}:
        return token

    if token in {"C", "P"}:
        raise LegNormalizationError(
            f"option_type invalido: {value!r}. "
            "Use CALL ou PUT por extenso. C/V sao reservados para compra/venda."
        )

    raise LegNormalizationError(
        f"option_type invalido: {value!r}. Use CALL ou PUT."
    )

# Frente 14 - contrato canonico de multiplier de opcoes
DEFAULT_OPTION_MULTIPLIER = 100.0


def normalize_option_multiplier(value=None, default=DEFAULT_OPTION_MULTIPLIER) -> float:
    """
    Normaliza o multiplicador contratual de opcoes.

    Contrato Frente 14:
      - Se ausente, vazio ou None: usa DEFAULT_OPTION_MULTIPLIER = 100.0
      - Se informado: deve ser numero positivo
      - Valor invalido ou menor/igual a zero gera erro explicito

    Observacao:
      O multiplier nao deve ser usado para corrigir quantidade.
      Ele representa o fator contratual aplicado ao payoff/preco da opcao.
    """
    if value is None:
        return float(default)

    text = str(value).strip()

    if not text:
        return float(default)

    text = text.replace(",", ".")

    try:
        result = float(text)
    except (TypeError, ValueError) as exc:
        raise LegNormalizationError(
            f"multiplier invalido: {value!r}. Use numero positivo."
        ) from exc

    if result <= 0:
        raise LegNormalizationError(
            f"multiplier invalido: {value!r}. Use numero positivo."
        )

    return result
