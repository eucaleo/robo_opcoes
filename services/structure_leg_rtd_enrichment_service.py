"""Service de enriquecimento de legs de estruturas via RTD.

Objetivo da Fase 9:
- receber entrada minima baseada em simbolo/codigo da opcao;
- consultar rtd_option_quotes por codigo_opcao;
- devolver payload canonico de leg para o repository de structures.

Este service nao persiste dados e nao contem regra de UI.
"""

from __future__ import annotations

from typing import Any

from domain.position_side import normalize_position_side


class StructureLegRtdEnrichmentService:
    """Enriquece uma leg de estrutura usando dados de rtd_option_quotes."""

    def __init__(self, rtd_option_quotes_repository: Any) -> None:
        self._repo = rtd_option_quotes_repository

    def enrich(self, leg_data: dict[str, Any]) -> dict[str, Any]:
        """Retorna uma leg canonica enriquecida a partir do simbolo da opcao.

        Entrada minima esperada:
        - symbol ou codigo_opcao;
        - position_side;
        - quantity.

        Campos opcionais preservados/normalizados:
        - premium;
        - multiplier;
        - leg_order;
        - notes.

        Campos enriquecidos via RTD:
        - option_type;
        - strike;
        - expiration_date;
        - underlying_asset.
        """

        symbol = self._normalize_symbol(
            leg_data.get("symbol") or leg_data.get("codigo_opcao")
        )
        if not symbol:
            raise ValueError("symbol is required for RTD leg enrichment")

        quote = self._repo.get_by_codigo(symbol)
        if quote is None:
            raise ValueError(f"option quote not found for symbol: {symbol}")

        self._ensure_required_quote_fields(
            quote,
            required=("ativo_base", "call_put", "strike", "vencimento"),
        )

        position_side = normalize_position_side(leg_data.get("position_side"))
        option_type = self._normalize_required_text(
            quote.get("call_put"),
            "call_put",
        )

        return {
            "symbol": symbol,
            "position_side": position_side,
            "option_type": option_type,
            "strike": self._to_float(quote.get("strike"), "strike"),
            "expiration_date": str(quote.get("vencimento")).strip(),
            "quantity": self._to_float(leg_data.get("quantity"), "quantity"),
            "premium": self._to_float(leg_data.get("premium", 0.0), "premium"),
            "multiplier": self._to_float(
                leg_data.get("multiplier", 100.0),
                "multiplier",
            ),
            "leg_order": self._to_int(leg_data.get("leg_order", 0), "leg_order"),
            "notes": leg_data.get("notes"),
            "underlying_asset": self._normalize_required_text(
                quote.get("ativo_base"),
                "ativo_base",
            ),
        }

    @staticmethod
    def _normalize_symbol(value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip().upper()

    @staticmethod
    def _normalize_required_text(value: Any, field_name: str) -> str:
        if value is None:
            raise ValueError(f"{field_name} is required")
        normalized = str(value).strip().upper()
        if not normalized:
            raise ValueError(f"{field_name} is required")
        return normalized

    @staticmethod
    def _to_float(value: Any, field_name: str) -> float:
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be numeric") from exc

    @staticmethod
    def _to_int(value: Any, field_name: str) -> int:
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be integer") from exc

    @staticmethod
    def _ensure_required_quote_fields(
        quote: dict[str, Any],
        required: tuple[str, ...],
    ) -> None:
        for field in required:
            value = quote.get(field)
            if value is None or str(value).strip() == "":
                raise ValueError(f"missing required RTD field: {field}")
