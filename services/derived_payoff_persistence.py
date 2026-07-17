# services/derived_payoff_persistence.py
import logging
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
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
      3. Persistir pontos no app.db via derived_service
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

        structure_id = self._extract_structure_id(pricing_payload)
        if structure_id is None:
            logger.warning(
                "derived_payoff_persistence: structure_id ausente; persistência bloqueada."
            )
            return

        if not self._is_active_structure(structure_id):
            logger.warning(
                "derived_payoff_persistence: estrutura inativa/arquivada; "
                "payoff e decisão não serão gravados -- structure_id=%s",
                structure_id,
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

            structure_payload = pricing_payload.get("structure") if isinstance(pricing_payload, dict) else {}
            if not isinstance(structure_payload, dict):
                structure_payload = {}

            market_payload = pricing_payload.get("market") if isinstance(pricing_payload, dict) else {}
            if not isinstance(market_payload, dict):
                market_payload = {}

            structure_id = (
                pricing_payload.get("structure_id")
                or structure_payload.get("structure_id")
                or structure_payload.get("id")
            )
            structure_name = (
                pricing_payload.get("structure_name")
                or structure_payload.get("structure_name")
                or structure_payload.get("name")
            )
            underlying_asset = (
                pricing_payload.get("underlying_asset")
                or structure_payload.get("underlying_asset")
                or structure_payload.get("underlying")
                or market_payload.get("underlying_asset")
                or market_payload.get("underlying")
            )

            decision_dict = {
                "decision":      "HOLD",
                "level":         0,
                "pl_atual":      pl_atual,
                "pl_max":        pl_max,
                "pl_pct_of_max": pl_pct_of_max,
                "dte_min":       dte_min,
                "spot_ref":      spot_ref,
                "structure_id":    structure_id,
                "structure_name":  structure_name,
                "underlying_asset": underlying_asset,
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

            if isinstance(decision_dict, dict) and decision_dict.get("structure_id") is None:
                decision_dict["structure_id"] = structure_id

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
    def _extract_structure_id(pricing_payload: dict[str, Any]) -> int | None:
        structure_payload = pricing_payload.get("structure") if isinstance(pricing_payload, dict) else {}
        if not isinstance(structure_payload, dict):
            structure_payload = {}

        raw = (
            pricing_payload.get("structure_id")
            or structure_payload.get("structure_id")
            or structure_payload.get("id")
        )

        try:
            sid = int(raw)
        except (TypeError, ValueError):
            return None

        return sid if sid > 0 else None

    @staticmethod
    def _default_db_path() -> Path:
        env_path = os.getenv("APP_DB_PATH")
        if env_path:
            return Path(env_path)

        # services/derived_payoff_persistence.py -> raiz do projeto -> dados/app.db
        return Path(__file__).resolve().parents[1] / "dados" / "app.db"

    @classmethod
    def _is_active_structure(cls, structure_id: int) -> bool:
        """
        Barreira de segurança na camada de persistência.

        Retorna True somente quando structures.status == 'active'.
        Qualquer ausência, erro ou status diferente bloqueia gravação.
        """
        db_path = cls._default_db_path()

        try:
            if not db_path.exists():
                logger.warning(
                    "derived_payoff_persistence: app.db não encontrado para validar structure_id=%s -- db_path=%s",
                    structure_id,
                    db_path,
                )
                return False

            with sqlite3.connect(str(db_path)) as conn:
                conn.row_factory = sqlite3.Row

                row = conn.execute(
                    """
                    SELECT status
                      FROM structures
                     WHERE id = ?
                     LIMIT 1
                    """,
                    (int(structure_id),),
                ).fetchone()

            if not row:
                logger.warning(
                    "derived_payoff_persistence: structure_id=%s não encontrada; persistência bloqueada.",
                    structure_id,
                )
                return False

            status = str(row["status"] or "").strip().lower()
            return status == "active"

        except Exception:
            logger.exception(
                "derived_payoff_persistence: falha ao validar status da estrutura -- structure_id=%s",
                structure_id,
            )
            return False

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

        Importante:
          O domínio valida structure.legs[*].position_side.
          Algumas etapas anteriores entregam legs com side.
          Por isso, aqui normalizamos side -> position_side antes de calcular payoff.
        """
        _ = result

        def normalize_leg_for_canonical(leg: dict[str, Any]) -> dict[str, Any]:
            normalized = dict(leg or {})

            if not normalized.get("position_side") and normalized.get("side"):
                side_value = str(normalized.get("side") or "").strip().upper()

                if side_value in {"LONG", "BUY", "C", "COMPRA"}:
                    normalized["position_side"] = "LONG"
                elif side_value in {"SHORT", "SELL", "V", "VENDA"}:
                    normalized["position_side"] = "SHORT"
                else:
                    normalized["position_side"] = side_value

            if normalized.get("option_type"):
                normalized["option_type"] = str(
                    normalized.get("option_type")
                ).strip().upper()

            if normalized.get("instrument_type"):
                normalized["instrument_type"] = str(
                    normalized.get("instrument_type")
                ).strip().upper()

            return normalized

        def normalize_legs(legs: Any) -> list[dict[str, Any]]:
            return [
                normalize_leg_for_canonical(leg)
                for leg in (legs or [])
                if isinstance(leg, dict)
            ]

        # Formato A -- já canônico
        if "structure" in pricing_payload and "market" in pricing_payload:
            canonical_input = dict(pricing_payload)
            structure = dict(canonical_input.get("structure") or {})
            structure["legs"] = normalize_legs(structure.get("legs"))
            canonical_input["structure"] = structure
            return canonical_input

        # Formato B -- flat  montar canônico
        structure_id   = pricing_payload.get("structure_id")
        structure_name = pricing_payload.get("structure_name")
        underlying     = pricing_payload.get("underlying_asset")
        spot_price     = pricing_payload.get("spot_price") or 0.0
        reference_date = pricing_payload.get("reference_date")
        legs           = normalize_legs(pricing_payload.get("legs"))

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
