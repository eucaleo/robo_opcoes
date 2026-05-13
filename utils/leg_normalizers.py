from datetime import datetime, timedelta
from typing import Union, Optional
import pandas as pd

from dto.robo_leg_dto import RoboLegDTO, CallPutType, CVType, FonteType


class LegNormalizer:

    @staticmethod
    def normalize_call_put(value: Union[str, int, None]) -> CallPutType:
        """Normaliza call/put para enum padrão"""
        if value is None:
            raise ValueError("call_put não pode ser None")

        value_str = str(value).upper().strip()

        call_mappings = ['CALL', 'C', '1', 'COMPRA_CALL', 'BUY_CALL']
        put_mappings = ['PUT', 'P', '0', 'COMPRA_PUT', 'BUY_PUT']

        if value_str in call_mappings:
            return CallPutType.CALL
        elif value_str in put_mappings:
            return CallPutType.PUT
        else:
            raise ValueError(f"Valor call_put não reconhecido: {value}")

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
