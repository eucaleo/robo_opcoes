# services/derived_payoff_persistence.py
import logging
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

        self._persist_payoff(pricing_payload, result)
        self._persist_decision(pricing_payload, result)

    # -------------------------------------------------------------- #
    #  payoff                                                          #
    # -------------------------------------------------------------- #

    def _persist_payoff(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        try:
            canonical_input = self._build_canonical_input(pricing_payload, result)
            payoff_result = compute_payoff_from_canonical_input(canonical_input)

            if not payoff_result.get("points"):
                logger.warning(
                    "derived_payoff_persistence: payoff sem pontos para structure_id=%s",
                    pricing_payload.get("structure_id"),
                )
                return

            save_payoff_from_canonical_payload(payoff_result)
            logger.info(
                "derived_payoff_persistence: %d pontos gravados -- structure_id=%s",
                len(payoff_result["points"]),
                pricing_payload.get("structure_id"),
            )

        except Exception:
            logger.exception(
                "derived_payoff_persistence: erro ao gravar payoff -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )

    # -------------------------------------------------------------- #
    #  decisão                                                         #
    # -------------------------------------------------------------- #

    def _persist_decision(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
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
            )
            logger.info(
                "derived_payoff_persistence: decisão gravada -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )

        except Exception:
            logger.exception(
                "derived_payoff_persistence: erro ao gravar decisão -- structure_id=%s",
                pricing_payload.get("structure_id"),
            )

    # -------------------------------------------------------------- #
    #  helpers                                                         #
    # -------------------------------------------------------------- #

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
        # Formato A -- já canônico
        if "structure" in pricing_payload and "market" in pricing_payload:
            return pricing_payload

        # Formato B -- flat  montar canônico
        structure_id   = pricing_payload.get("structure_id")
        structure_name = pricing_payload.get("structure_name")
        underlying     = pricing_payload.get("underlying_asset")
        spot_price     = pricing_payload.get("spot_price") or 0.0
        reference_date = pricing_payload.get("reference_date")
        legs           = pricing_payload.get("legs") or []

        return {
            "structure": {
                "structure_id":    structure_id,
                "name":            structure_name,
                "underlying_asset": underlying,
                "legs":            legs,
            },
            "market": {
                "spot_price":       spot_price,
                "underlying_asset": underlying,
                "reference_date":   reference_date,
            },
            "meta": {
                "source": "pricing_execution_persistence",
            },
        }
