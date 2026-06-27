from typing import Any

from domain.payoff import compute_payoff_curve_from_canonical_legs
from domain.position_side import to_pricing_engine_side


class PayoffPricingEngine:
    """
    Motor financeiro baseado na curva de payoff canônica, com separação entre:

    - payoff no vencimento;
    - payoff no spot atual do ativo-base;
    - PL atual por marcação a mercado das opções, quando o payload trouxer
      preço atual de opção vindo de RTD/cache/mercado.

    Observação importante:
    - premium/entry_price representa preço de entrada da perna;
    - current_price/current_option_price/ultimo_preco/etc. representa preço
      atual da opção para MTM;
    - esses conceitos não devem ser misturados.
    """

    engine_name = "payoff_pricing_engine"

    def run(self, pricing_payload: dict[str, Any]) -> dict[str, Any]:
        if not pricing_payload:
            raise ValueError("pricing_payload is required")

        legs = pricing_payload.get("legs") or []
        if not legs:
            raise ValueError("pricing_payload.legs is required")

        spot_price = float(pricing_payload.get("spot_price") or 0.0)
        if spot_price <= 0:
            raise ValueError("pricing_payload.spot_price is required")

        if self._is_static_market_snapshot(pricing_payload):
            raise ValueError(
                "pricing_payload.spot_price veio de static_fallback; "
                "informe um snapshot real/atual antes de calcular PL atual"
            )

        normalized_legs = [self._normalize_leg(leg) for leg in legs]

        total_quantity = sum(
            int(float(leg.get("quantity") or 0))
            for leg in normalized_legs
        )
        number_of_legs = len(normalized_legs)

        payoff = compute_payoff_curve_from_canonical_legs(
            legs=normalized_legs,
            spot_ref=spot_price,
            low_pct=0.5,
            high_pct=1.5,
            step_pct=0.01,
        )

        pl_max = payoff.get("pl_max")
        pl_min = payoff.get("pl_min")

        payoff_at_spot = self._compute_pl_at_spot(
            legs=normalized_legs,
            spot_price=spot_price,
        )

        mtm_result = self._compute_mark_to_market(normalized_legs)
        pl_atual_mtm = mtm_result["pl_atual_mtm"]
        mtm_complete = mtm_result["complete"]

        if mtm_complete:
            pl_atual = pl_atual_mtm
            theoretical_value = pl_atual_mtm
            pl_atual_source = "mark_to_market"
            method = "expiration_payoff_grid_with_mark_to_market"
        else:
            pl_atual = payoff_at_spot
            theoretical_value = payoff_at_spot
            pl_atual_source = "expiration_payoff_at_spot"
            method = "expiration_payoff_grid"

        premium_paid = self._compute_net_premium_paid(normalized_legs)

        warnings = []
        if not mtm_complete:
            warnings.append(
                "MTM incompleto: uma ou mais pernas não possuem preço atual "
                "de opção no payload. pl_atual foi mantido como payoff no spot."
            )

        return {
            "engine": self.engine_name,
            "status": "ok",
            "structure_id": pricing_payload.get("structure_id"),
            "underlying_asset": pricing_payload.get("underlying_asset"),
            "reference_date": pricing_payload.get("reference_date"),
            "metrics": {
                "number_of_legs": number_of_legs,
                "total_quantity": total_quantity,
                "spot_price": spot_price,
                "interest_rate": float(pricing_payload.get("interest_rate") or 0.0),
                "volatility": float(pricing_payload.get("volatility") or 0.0),
                "payoff_points": len(payoff.get("points") or []),
                "pl_max": pl_max,
                "pl_min": pl_min,
                "pl_atual": pl_atual,
                "pl_atual_mtm": pl_atual_mtm,
                "payoff_at_spot": payoff_at_spot,
                "mtm_complete": mtm_complete,
                "mtm_legs_priced": mtm_result["priced_count"],
                "mtm_legs_missing_price": mtm_result["missing_count"],
            },
            "valuation": {
                "theoretical_value": theoretical_value,
                "premium_paid": premium_paid,
                "max_profit": pl_max,
                "max_loss": pl_min,
                "pl_max": pl_max,
                "pl_min": pl_min,
                "pl_atual": pl_atual,
                "pl_atual_mtm": pl_atual_mtm,
                "payoff_at_spot": payoff_at_spot,
                "pl_atual_source": pl_atual_source,
                "mtm_complete": mtm_complete,
                "mtm_legs_priced": mtm_result["priced_count"],
                "mtm_legs_missing_price": mtm_result["missing_count"],
                "leg_valuations": mtm_result["legs"],
                "method": method,
                "warnings": warnings,
            },
            "payoff": payoff,
        }

    @staticmethod
    def _is_static_market_snapshot(pricing_payload: dict[str, Any]) -> bool:
        meta = pricing_payload.get("meta") or {}
        input_meta = pricing_payload.get("input_meta") or {}

        source = str(
            pricing_payload.get("market_snapshot_source")
            or pricing_payload.get("snapshot_source")
            or meta.get("market_snapshot_source")
            or meta.get("snapshot_source")
            or input_meta.get("market_snapshot_source")
            or input_meta.get("snapshot_source")
            or ""
        ).strip().lower()

        explicit_static_flag = any(
            bool(value)
            for value in [
                pricing_payload.get("is_static_fallback"),
                pricing_payload.get("market_is_static_fallback"),
                meta.get("is_static_fallback"),
                meta.get("market_is_static_fallback"),
                input_meta.get("is_static_fallback"),
                input_meta.get("market_is_static_fallback"),
            ]
        )

        return explicit_static_flag or source == "static_fallback"

    @staticmethod
    def _normalize_leg(leg: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(leg)

        side = (
            normalized.get("position_side")
            or normalized.get("side")
            or normalized.get("direction")
        )
        normalized["position_side"] = to_pricing_engine_side(side)

        normalized["option_type"] = str(
            normalized.get("option_type")
            or normalized.get("type")
            or normalized.get("kind")
            or ""
        ).strip().upper()

        normalized["strike"] = float(normalized.get("strike") or 0.0)
        normalized["quantity"] = float(normalized.get("quantity") or 0.0)
        normalized["multiplier"] = float(normalized.get("multiplier") or 1.0)

        premium = (
            normalized.get("premium")
            if normalized.get("premium") is not None
            else normalized.get("entry_price")
        )
        if premium is None:
            premium = normalized.get("entry_premium")
        if premium is None:
            premium = normalized.get("valor_executado")
        if premium is None:
            premium = normalized.get("price")
        if premium is None:
            premium = normalized.get("last_price")
        if premium is None:
            premium = 0.0

        normalized["premium"] = float(premium)

        current_price, current_price_source = PayoffPricingEngine._resolve_current_option_price(
            normalized
        )
        normalized["current_option_price"] = current_price
        normalized["current_option_price_source"] = current_price_source

        return normalized

    @staticmethod
    def _to_float_or_none(value: Any) -> float | None:
        if value is None:
            return None

        if isinstance(value, bool):
            return None

        text = str(value).strip()
        if not text:
            return None

        invalid_values = {
            "NONE",
            "NULL",
            "N/A",
            "NA",
            "#N/A",
            "#VALUE!",
            "#REF!",
            "#NAME?",
        }
        if text.upper() in invalid_values:
            return None

        text = (
            text.replace("R$", "")
            .replace("%", "")
            .replace("\u00a0", " ")
            .strip()
        )
        text = text.replace(" ", "")

        if "," in text and "." in text:
            text = text.replace(".", "").replace(",", ".")
        elif "," in text:
            text = text.replace(",", ".")

        try:
            return float(text)
        except ValueError:
            return None

    @classmethod
    def _resolve_current_option_price(cls, leg: dict[str, Any]) -> tuple[float | None, str | None]:
        """
        Resolve preço atual da opção para MTM.

        Ordem proposital:
        1. campos explicitamente atuais;
        2. campos efetivos vindos da fachada RTD;
        3. ultimo_preco/last_price;
        4. mid/bid/ask.

        Não usa premium nem entry_price, pois esses são preço de entrada.
        """

        direct_candidates = [
            ("current_option_price", "current_option_price"),
            ("current_price", "current_price"),
            ("market_price", "market_price"),
            ("option_market_price", "option_market_price"),
            ("rtd_option_price", "rtd_option_price"),
            ("effective_option_price", "effective_option_price"),
            ("ultimo_preco", "ultimo_preco"),
            ("last_price", "last_price"),
            ("last", "last"),
            ("mid", "mid"),
        ]

        explicit_source = (
            leg.get("current_option_price_source")
            or leg.get("current_price_source")
            or leg.get("market_price_source")
            or leg.get("option_market_price_source")
            or leg.get("rtd_option_price_source")
            or leg.get("effective_option_price_source")
            or leg.get("option_price_source")
            or leg.get("price_source")
            or leg.get("source")
        )

        for key, default_source in direct_candidates:
            value = cls._to_float_or_none(leg.get(key))
            if value is not None and value >= 0:
                return round(float(value), 6), str(explicit_source or default_source)

        bid = cls._to_float_or_none(leg.get("bid"))
        ask = cls._to_float_or_none(leg.get("ask"))

        if bid is not None and ask is not None and bid >= 0 and ask >= 0:
            return round((bid + ask) / 2.0, 6), str(explicit_source or "mid_bid_ask")

        if bid is not None and bid >= 0:
            return round(float(bid), 6), str(explicit_source or "bid")

        if ask is not None and ask >= 0:
            return round(float(ask), 6), str(explicit_source or "ask")

        return None, None

    @staticmethod
    def _is_short_leg(leg: dict[str, Any]) -> bool:
        side = str(leg.get("position_side") or "").strip().upper()
        return side in {"SHORT", "SELL", "SOLD", "VENDIDA", "VENDIDO"}

    @staticmethod
    def _intrinsic_value(option_type: str, strike: float, spot: float) -> float:
        if option_type == "CALL":
            return max(spot - strike, 0.0)
        if option_type == "PUT":
            return max(strike - spot, 0.0)
        return 0.0

    def _compute_pl_at_spot(
        self,
        legs: list[dict[str, Any]],
        spot_price: float,
    ) -> float:
        """
        Calcula payoff no vencimento avaliado no spot atual do ativo-base.

        Este método não é MTM da opção.
        Ele usa valor intrínseco no vencimento menos prêmio de entrada.
        """
        total = 0.0

        for leg in legs:
            intrinsic = self._intrinsic_value(
                option_type=str(leg.get("option_type") or "").upper(),
                strike=float(leg.get("strike") or 0.0),
                spot=spot_price,
            )

            premium = float(leg.get("premium") or 0.0)
            quantity = float(leg.get("quantity") or 0.0)
            multiplier = float(leg.get("multiplier") or 1.0)

            unit_pl = intrinsic - premium

            if self._is_short_leg(leg):
                unit_pl = -unit_pl

            total += unit_pl * quantity * multiplier

        return round(float(total), 6)

    def _compute_mark_to_market(self, legs: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Calcula PL atual por marcação a mercado das opções.

        Compra:
            PL = preço atual - preço de entrada

        Venda:
            PL = preço de entrada - preço atual

        Ambos multiplicados por quantidade e multiplicador.
        """
        total = 0.0
        leg_valuations = []
        priced_count = 0
        missing_count = 0

        for index, leg in enumerate(legs):
            symbol = (
                leg.get("symbol")
                or leg.get("codigo_opcao")
                or leg.get("ticker")
                or leg.get("option_symbol")
            )

            entry_price = float(leg.get("premium") or 0.0)
            current_price = leg.get("current_option_price")
            current_price_source = leg.get("current_option_price_source")

            quantity = float(leg.get("quantity") or 0.0)
            multiplier = float(leg.get("multiplier") or 1.0)
            side = str(leg.get("position_side") or "").strip().upper()

            if current_price is None:
                missing_count += 1
                leg_valuations.append(
                    {
                        "index": index,
                        "symbol": symbol,
                        "position_side": side,
                        "entry_price": entry_price,
                        "current_price": None,
                        "current_price_source": None,
                        "quantity": quantity,
                        "multiplier": multiplier,
                        "pl_mtm": None,
                        "status": "missing_current_option_price",
                    }
                )
                continue

            current_price = float(current_price)
            side_sign = -1.0 if self._is_short_leg(leg) else 1.0

            unit_pl = side_sign * (current_price - entry_price)
            pl_mtm = unit_pl * quantity * multiplier

            total += pl_mtm
            priced_count += 1

            leg_valuations.append(
                {
                    "index": index,
                    "symbol": symbol,
                    "option_type": leg.get("option_type"),
                    "position_side": side,
                    "entry_price": round(float(entry_price), 6),
                    "current_price": round(float(current_price), 6),
                    "current_price_source": current_price_source,
                    "quantity": quantity,
                    "multiplier": multiplier,
                    "unit_pl_mtm": round(float(unit_pl), 6),
                    "pl_mtm": round(float(pl_mtm), 6),
                    "status": "ok",
                }
            )

        complete = bool(legs) and missing_count == 0

        return {
            "pl_atual_mtm": round(float(total), 6) if priced_count else None,
            "legs": leg_valuations,
            "priced_count": priced_count,
            "missing_count": missing_count,
            "complete": complete,
        }

    @staticmethod
    def _compute_net_premium_paid(legs: list[dict[str, Any]]) -> float:
        total = 0.0

        for leg in legs:
            premium = float(leg.get("premium") or 0.0)
            quantity = float(leg.get("quantity") or 0.0)
            multiplier = float(leg.get("multiplier") or 1.0)

            amount = premium * quantity * multiplier

            if PayoffPricingEngine._is_short_leg(leg):
                amount = -amount

            total += amount

        return round(float(total), 6)
