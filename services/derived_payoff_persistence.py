# services/derived_payoff_persistence.py
import logging
from datetime import datetime, timezone
from typing import Any

from domain.payoff import compute_payoff_from_canonical_input
from services.derived_service import save_payoff_from_canonical_payload, save_decision_from_canonical_payload

logger = logging.getLogger(__name__)


class DerivedPayoffPersistence:
    """
    Implementação concreta de PayoffPersistencePort.

    Responsabilidades:
      1. Montar o canonical_input a partir do pricing_payload
      2. Calcular a curva de payoff via domain/payoff.py
      3. Persistir pontos no derived.db via derived_service
      4. Persistir decisão básica derivada do resultado do engine
    """

    # -------------------------------------------------------------- #
    #  PayoffPersistencePort.persist()                                 #
    # -------------------------------------------------------------- #

    def persist(
        self,
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
    ) -> None:
        if not pricing_payload:
            logger.debug("derived_payoff_persistence: pricing_payload vazio, skip.")
            return

        inner = result.get("result", result) if isinstance(result, dict) else{}
        status = inner.get("status", "")
        if status not in ("success", "ok", "completed"):
            logger.debug(
                "derived_payoff_persistence: status=%r não elegível para payoff, skip.",
                status,
            )
            return

        # Timestamp único para payoff + decisão.
        # Evita snapshots inconsistentes por diferença de milissegundos entre gravações.
        snapshot_ts = datetime.now(timezone.utc).isoformat()

        payoff_saved = self._persist_payoff(pricing_payload, result, snapshot_ts)
        if not payoff_saved:
            logger.warning(
                "derived_payoff_persistence: decisão não gravada porque payoff não foi salvo -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return

        decision_saved = self._persist_decision(pricing_payload, result, snapshot_ts)
        if not decision_saved:
            logger.error(
                "derived_payoff_persistence: payoff salvo, mas decisão falhou -- structure_id=%s timestamp=%s",
                pricing_payload.get("structure_id"),
                snapshot_ts,
            )

    # -------------------------------------------------------------- #
    #  payoff                                                          #
    # -------------------------------------------------------------- #

    def _persist_payoff(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
        snapshot_ts: str,
    ) -> bool:
        try:
            canonical_input = self._build_canonical_input(pricing_payload, result)
            payoff_result = compute_payoff_from_canonical_input(canonical_input)

            if not payoff_result.get("points"):
                logger.warning(
                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
                    pricing_payload.get("structure_id"),
                )
                return False

            save_payoff_from_canonical_payload(payoff_result, timestamp=snapshot_ts)
            logger.info(
                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
                len(payoff_result["points"]),
                pricing_payload.get("structure_id"),
            )
            return True

        except Exception:
            logger.exception(
                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return False

    # -------------------------------------------------------------- #
    #  decisão                                                         #
    # -------------------------------------------------------------- #

    def _persist_decision(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
        snapshot_ts: str,
    ) -> bool:
        try:
            if not isinstance(result, dict):
                inner = {}
            else:
                inner = result.get("result") or result

            valuation = inner.get("valuation") or {}
            metrics   = inner.get("metrics")   or {}

            theoretical_value = valuation.get("theoretical_value")
            pl_max            = valuation.get("pl_max")
            pl_atual          = valuation.get("pl_atual") or theoretical_value
            dte_min           = metrics.get("dte_min")
            spot_ref          = pricing_payload.get("spot_price")
            
            if spot_ref is None:
                spot_ref = (pricing_payload.get("market") or {}).get("spot_price")

            pl_pct_of_max = None
            if pl_max and pl_atual is not None:
                try:
                    pl_pct_of_max = round(float(pl_atual) / float(pl_max), 6)
                except (ZeroDivisionError, TypeError, ValueError):
                    pass

            decision_dict = {
                "decision":      "HOLD",
                "level":         0,
                "pl_atual":      pl_atual,
                "pl_max":        pl_max,
                "pl_pct_of_max": pl_pct_of_max,
                "dte_min":       dte_min,
                "spot_ref":      spot_ref,
                "why": {
                    "source":           "pricing_engine",
                    "engine":           inner.get("engine"),
                    "execution_status": inner.get("status"),
                    "theoretical_value": theoretical_value,
                },
                "meta": {
                    "structure_id":    pricing_payload.get("structure_id"),
                    "structure_name":  pricing_payload.get("structure_name"),
                    "underlying_asset": pricing_payload.get("underlying_asset"),
                    "reference_date":  pricing_payload.get("reference_date"),
                },
            }

            save_decision_from_canonical_payload(
                decision=decision_dict,
                structure_id=pricing_payload.get("structure_id"),
                structure_name=pricing_payload.get("structure_name"),
                underlying_asset=pricing_payload.get("underlying_asset"),
                timestamp=snapshot_ts,
            )
            logger.info(
                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return True

        except Exception:
            logger.exception(
                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )
            return False

    # -------------------------------------------------------------- #
    #  helpers                                                         #
    # -------------------------------------------------------------- #


    @staticmethod
    def _normalize_position_side(value: Any, quantity: Any = None) -> str | None:
        """
        Normaliza aliases de direção para o contrato canônico de payoff.

        domain/payoff.py exige leg["position_side"].
        Payloads vindos da UI/manual podem vir com leg["side"].
        """
        raw = "" if value is None else str(value).strip().upper()

        aliases = {
            "BUY": "LONG",
            "BOUGHT": "LONG",
            "COMPRA": "LONG",
            "COMPRADO": "LONG",
            "LONG": "LONG",
            "SELL": "SHORT",
            "SOLD": "SHORT",
            "VENDA": "SHORT",
            "VENDIDO": "SHORT",
            "SHORT": "SHORT",
        }

        if raw in aliases:
            return aliases[raw]

        try:
            q = float(quantity)
            if q < 0:
                return "SHORT"
            if q > 0:
                return "LONG"
        except (TypeError, ValueError):
            pass

        return None

    @staticmethod
    def _normalize_leg_for_payoff(leg: Any) -> dict[str, Any]:
        """
        Adapta uma leg recebida de fontes legadas/manuais para o contrato
        esperado por domain.compute_payoff_from_canonical_input().

        Correção principal da Fase 3F Fix1:
          side -> position_side

        Também mantém aliases úteis sem remover os campos originais.
        """
        data = dict(leg) if isinstance(leg, dict) else dict(vars(leg))

        quantity = data.get("quantity", data.get("quant"))
        position_side = data.get("position_side") or data.get("side")

        normalized_side = DerivedPayoffPersistence._normalize_position_side(
            position_side,
            quantity,
        )

        if normalized_side:
            data["position_side"] = normalized_side
            data.setdefault("side", normalized_side)

        if quantity is not None:
            try:
                # No contrato canônico, a direção fica em position_side.
                # A quantidade deve ser magnitude positiva.
                data["quantity"] = abs(float(quantity))
            except (TypeError, ValueError):
                data["quantity"] = quantity

        option_type = data.get("option_type")
        if option_type is not None:
            data["option_type"] = str(option_type).strip().upper()

        instrument_type = data.get("instrument_type")
        if instrument_type is not None:
            data["instrument_type"] = str(instrument_type).strip().upper()

        # Aliases defensivos para eventuais payloads de outras origens.
        if "premium" not in data and "price" in data:
            data["premium"] = data.get("price")

        if "price" not in data and "premium" in data:
            data["price"] = data.get("premium")

        if "symbol" not in data:
            data["symbol"] = data.get("asset") or data.get("ativo")

        return data

    @staticmethod
    def _normalize_canonical_input_for_payoff(
        canonical_input: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Retorna uma cópia rasa do canonical_input com legs normalizadas para payoff.
        """
        normalized = dict(canonical_input)

        structure = dict(normalized.get("structure") or {})
        market = dict(normalized.get("market") or {})
        meta = dict(normalized.get("meta") or {})

        legs = structure.get("legs") or []
        structure["legs"] = [
            DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
            for leg in legs
        ]

        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")

        normalized["structure"] = structure
        normalized["market"] = market
        normalized["meta"] = meta

        return normalized


    @staticmethod
    def _build_canonical_input(
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Monta o canonical_input esperado por compute_payoff_from_canonical_input().

        Suporta dois formatos de pricing_payload:
          A) já canônico: { structure: { legs, ... }, market: { spot_price, ... } }
          B) flat:        { legs: [...], spot_price: ..., structure_id: ..., ... }
        """
        # Formato A -- já canônico, mas ainda assim normalizado para o contrato
        # estrito de domain/payoff.py.
        if "structure" in pricing_payload and "market" in pricing_payload:
            return DerivedPayoffPersistence._normalize_canonical_input_for_payoff(
                pricing_payload
            )

        # Formato B -- flat  montar canônico
        structure_id   = pricing_payload.get("structure_id")
        structure_name = pricing_payload.get("structure_name")
        underlying     = pricing_payload.get("underlying_asset")
        spot_price     = pricing_payload.get("spot_price") or 0.0
        reference_date = pricing_payload.get("reference_date")
        legs           = pricing_payload.get("legs") or []

        payload_meta = pricing_payload.get("meta")
        meta = dict(payload_meta) if isinstance(payload_meta, dict) else {}
        meta.setdefault("source", "pricing_execution_persistence")
        meta.setdefault("payoff_leg_normalization", "fase_3f_fix1_position_side_from_side")

        canonical_input = {
            "structure": {
                "structure_id":    structure_id,
                "name":            structure_name,
                "underlying_asset": underlying,
                "legs": [
                    DerivedPayoffPersistence._normalize_leg_for_payoff(leg)
                    for leg in legs
                ],
            },
            "market": {
                "spot_price":       spot_price,
                "underlying_asset": underlying,
                "reference_date":   reference_date,
            },
            "meta": meta,
        }

        return canonical_input
