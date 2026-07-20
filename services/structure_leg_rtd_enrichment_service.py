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


    def enrich_legs(
        self,
        legs: list[dict[str, Any]],
        *,
        strict: bool = False,
        apply_live_price: bool = True,
        price_policy: str = "last_mid",
    ) -> list[dict[str, Any]]:
        """Enriquece uma lista de legs com dados de rtd_option_quotes.

        Este método é tolerante por padrão:
        - se uma leg não tiver símbolo, preserva a leg original;
        - se não encontrar cotação, preserva a leg original;
        - se houver erro de conversão/campo, preserva a leg original.

        Use strict=True apenas em fluxos de validação/cadastro.
        """

        enriched_legs: list[dict[str, Any]] = []

        for raw_leg in legs or []:
            if not isinstance(raw_leg, dict):
                enriched_legs.append(raw_leg)
                continue

            leg = dict(raw_leg)

            try:
                leg = self.enrich_live_market_fields(
                    leg,
                    apply_live_price=apply_live_price,
                    price_policy=price_policy,
                )
            except Exception:
                if strict:
                    raise

            enriched_legs.append(leg)

        return enriched_legs

    def enrich_live_market_fields(
        self,
        leg_data: dict[str, Any],
        *,
        apply_live_price: bool = True,
        price_policy: str = "last_mid",
    ) -> dict[str, Any]:
        """Enriquece uma leg existente com campos de mercado vindos do RTD.

        Diferente de enrich(), este método preserva a leg original e apenas
        complementa/atualiza campos úteis para payoff e UI.

        Política de preço padrão:
        - ultimo_preco;
        - mid bid/ask;
        - bid;
        - ask;
        - vwap.
        """

        leg = dict(leg_data or {})
        symbol = self._normalize_symbol(
            leg.get("symbol") or leg.get("codigo_opcao") or leg.get("asset")
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

        leg["symbol"] = symbol
        leg["codigo_opcao"] = quote.get("codigo_opcao") or symbol
        leg["option_type"] = self._normalize_required_text(
            quote.get("call_put"),
            "call_put",
        )
        leg["call_put"] = leg["option_type"]
        leg["strike"] = self._to_float(quote.get("strike"), "strike")
        leg["expiration_date"] = str(quote.get("vencimento")).strip()
        leg["vencimento"] = leg["expiration_date"]
        leg["underlying_asset"] = self._normalize_required_text(
            quote.get("ativo_base"),
            "ativo_base",
        )

        for field in (
            "ultimo_preco",
            "bid",
            "ask",
            "vwap",
            "volume",
            "iv",
            "delta",
            "gamma",
            "theta",
            "vega",
        ):
            leg[field] = self._to_optional_float(quote.get(field))

        leg["updated_at"] = quote.get("updated_at")
        leg["source"] = "rtd_option_quotes"

        if apply_live_price:
            price, price_source = self._quote_policy_price(
                quote,
                side=leg.get("position_side") or leg.get("side") or leg.get("cv"),
                policy=price_policy,
            )

            if price is not None:
                if "entry_premium" not in leg:
                    leg["entry_premium"] = self._to_optional_float(
                        leg.get("premium")
                        or leg.get("premio")
                        or leg.get("prêmio")
                        or leg.get("valor_executado")
                    )

                leg["premium"] = price
                leg["current_price"] = price
                leg["price_source"] = price_source
                leg["_rtd_live_price_applied"] = True

        return leg

    @classmethod
    def _quote_policy_price(
        cls,
        quote: dict[str, Any],
        *,
        side: Any = None,
        policy: str = "last_mid",
    ) -> tuple[float | None, str | None]:
        last = cls._to_optional_float(quote.get("ultimo_preco"))
        bid = cls._to_optional_float(quote.get("bid"))
        ask = cls._to_optional_float(quote.get("ask"))
        vwap = cls._to_optional_float(quote.get("vwap"))

        mid = None
        if bid is not None and ask is not None:
            mid = (bid + ask) / 2.0

        normalized_policy = str(policy or "last_mid").strip().lower()
        side_norm = str(side or "").strip().upper()

        if normalized_policy == "side_exit":
            if side_norm in {"SHORT", "SELL", "VENDIDO", "VENDER", "V"}:
                candidates = (
                    (ask, "rtd_option_quotes.ask"),
                    (last, "rtd_option_quotes.ultimo_preco"),
                    (mid, "rtd_option_quotes.mid_bid_ask"),
                    (bid, "rtd_option_quotes.bid"),
                    (vwap, "rtd_option_quotes.vwap"),
                )
            else:
                candidates = (
                    (bid, "rtd_option_quotes.bid"),
                    (last, "rtd_option_quotes.ultimo_preco"),
                    (mid, "rtd_option_quotes.mid_bid_ask"),
                    (ask, "rtd_option_quotes.ask"),
                    (vwap, "rtd_option_quotes.vwap"),
                )
        else:
            candidates = (
                (last, "rtd_option_quotes.ultimo_preco"),
                (mid, "rtd_option_quotes.mid_bid_ask"),
                (bid, "rtd_option_quotes.bid"),
                (ask, "rtd_option_quotes.ask"),
                (vwap, "rtd_option_quotes.vwap"),
            )

        for value, source in candidates:
            if value is not None:
                return value, source

        return None, None

    @staticmethod
    def _to_optional_float(value: Any) -> float | None:
        if value is None:
            return None

        try:
            if isinstance(value, str):
                text = value.strip()
                if not text:
                    return None
                if "," in text:
                    text = text.replace(".", "").replace(",", ".")
                value = text

            converted = float(value)
        except (TypeError, ValueError):
            return None

        return converted if converted > 0 else None


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
