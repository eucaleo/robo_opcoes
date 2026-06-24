"""Service de enriquecimento de legs de estruturas via RTD.

Objetivo:
- receber entrada minima baseada em simbolo/codigo da opcao;
- consultar rtd_option_quotes por codigo_opcao;
- devolver payload canonico de leg para o repository de structures;
- validar divergencia entre tipo informado e tipo detectado.
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

        Campos enriquecidos via RTD:
        - underlying_asset;
        - option_type;
        - strike;
        - expiration_date.
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

        detected_option_type = self._normalize_option_type(quote.get("call_put"))

        informed_option_type_raw = leg_data.get("option_type")
        if informed_option_type_raw not in (None, ""):
            informed_option_type = self._normalize_option_type(informed_option_type_raw)
            if informed_option_type != detected_option_type:
                raise ValueError(
                    "option_type divergente do símbolo informado: "
                    f"informado={informed_option_type}, "
                    f"detectado={detected_option_type}, "
                    f"symbol={symbol}"
                )

        return {
            "symbol": symbol,
            "position_side": normalize_position_side(leg_data.get("position_side")),
            "option_type": detected_option_type,
            "strike": self._to_float(quote.get("strike"), "strike"),
            "expiration_date": str(quote.get("vencimento")).strip(),
            "quantity": self._to_float(leg_data.get("quantity", 1), "quantity"),
            "premium": self._resolve_premium(leg_data, quote),
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

    @classmethod
    def _normalize_option_type(cls, value: Any) -> str:
        text = cls._normalize_required_text(value, "option_type")
        mapping = {
            "C": "CALL",
            "CALL": "CALL",
            "COMPRA": "CALL",
            "P": "PUT",
            "PUT": "PUT",
            "VENDA": "PUT",
        }
        normalized = mapping.get(text)
        if normalized is None:
            raise ValueError(f"invalid option_type/call_put: {value!r}")
        return normalized

    @classmethod
    def _resolve_premium(cls, leg_data: dict[str, Any], quote: dict[str, Any]) -> float:
        """Resolve o prêmio da leg.

        Prioridade:
        1. premium informado manualmente na leg;
        2. ultimo_preco vindo do RTD/cache;
        3. zero, para preservar compatibilidade quando não houver preço.
        """
        premium = leg_data.get("premium")

        if premium is not None and str(premium).strip() != "":
            return cls._to_float(premium, "premium")

        quote_premium = quote.get("ultimo_preco")

        if quote_premium is not None and str(quote_premium).strip() != "":
            return cls._to_float(quote_premium, "ultimo_preco")

        return 0.0

    @staticmethod
    def _to_float(value: Any, field_name: str) -> float:
        if value is None or str(value).strip() == "":
            raise ValueError(f"{field_name} is required")

        text = str(value).strip()
        if "," in text and "." in text:
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", ".")

        try:
            return float(text)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be numeric") from exc

    @classmethod
    def _to_optional_float(cls, value: Any, field_name: str) -> float | None:
        if value is None or str(value).strip() == "":
            return None
        return cls._to_float(value, field_name)

    @classmethod
    def _to_int(cls, value: Any, field_name: str) -> int:
        number = cls._to_float(value, field_name)
        if int(number) != number:
            raise ValueError(f"{field_name} must be integer")
        return int(number)

    @staticmethod
    def _ensure_required_quote_fields(
        quote: dict[str, Any],
        required: tuple[str, ...],
    ) -> None:
        for field in required:
            value = quote.get(field)
            if value is None or str(value).strip() == "":
                raise ValueError(f"missing required RTD field: {field}")
