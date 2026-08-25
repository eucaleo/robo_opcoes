# services/pricing_execution_persistence_service.py
import logging
from typing import Any

from repositories.pricing_executions_repository import PricingExecutionsRepository
from repositories.system_snapshots_repository import SystemSnapshotsRepository
from services.payoff_persistence_port import PayoffPersistencePort

logger = logging.getLogger(__name__)


class PricingExecutionPersistenceService:
    def __init__(
        self,
        pricing_executions_repository: PricingExecutionsRepository | None = None,
        payoff_persistence_port: PayoffPersistencePort | None = None,
        system_snapshots_repository: SystemSnapshotsRepository | None = None,
    ):
        self.pricing_executions_repository = (
            pricing_executions_repository or PricingExecutionsRepository()
        )
        self._payoff_port = payoff_persistence_port
        self._system_snapshots_repository = system_snapshots_repository

    def persist_execution(
        self,
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
        duration_ms: int | None = None,
        error_message: str | None = None,
    ) -> dict[str, Any]:
        # result pode chegar como wrapper {"result": {...}} ou já desempacotado
        inner = result.get("result", result) if isinstance(result, dict) else result
        metrics = inner.get("metrics", {}) if isinstance(inner, dict) else {}
        valuation = inner.get("valuation", {}) if isinstance(inner, dict) else {}

        execution_engine = inner.get("engine") if isinstance(inner, dict) else None
        execution_status = inner.get("status") if isinstance(inner, dict) else None
        persisted_error_message = error_message or (
            inner.get("error_message") if isinstance(inner, dict) else None
        )
        number_of_legs = metrics.get("number_of_legs")
        total_quantity = metrics.get("total_quantity")
        theoretical_value = valuation.get("theoretical_value")

        record = self.pricing_executions_repository.save_execution(
            pricing_payload=pricing_payload,
            result=result,
            execution_status=execution_status,
            execution_engine=execution_engine,
            error_message=persisted_error_message,
            duration_ms=duration_ms,
            number_of_legs=number_of_legs,
            total_quantity=total_quantity,
            theoretical_value=theoretical_value,
        )

        snapshot_id = self._create_system_snapshot_if_applicable(
            record=record,
            pricing_payload=pricing_payload,
            result=result,
            inner=inner,
            execution_status=execution_status,
        )

        # ------------------------------------------------------------------ #
        #  alteracao_21 -- persistência derivada (payoff + decisão)           #
        #  Fire-and-forget: falha aqui nunca derruba a execução principal.    #
        # ------------------------------------------------------------------ #
        if self._payoff_port is not None:
            try:
                self._payoff_port.persist(
                    pricing_payload=pricing_payload,
                    result=result,
                )
            except Exception:
                logger.exception(
                    "payoff_persistence_port.persist() falhou -- execução id=%s não afetada",
                    record.get("id"),
                )

        response = {
            "record": record,
        }

        if snapshot_id is not None:
            response["snapshot_id"] = snapshot_id

        return response

    def _create_system_snapshot_if_applicable(
        self,
        *,
        record: dict[str, Any],
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
        inner: Any,
        execution_status: str | None,
    ) -> int | None:
        if self._system_snapshots_repository is None:
            return None

        if not pricing_payload:
            return None

        if execution_status != "ok":
            return None

        structure_id = pricing_payload.get("structure_id") or record.get("structure_id")
        if not structure_id:
            return None

        try:
            return self._system_snapshots_repository.create_snapshot(
                structure_id=int(structure_id),
                pricing_execution_id=record.get("id"),
                underlying_asset=pricing_payload.get("underlying_asset"),
                reference_date=pricing_payload.get("reference_date"),
                snapshot_source="system_pricing_execution",
                structure_json=self._build_structure_json(pricing_payload),
                legs=pricing_payload.get("legs") or [],
                market_json=self._build_market_json(pricing_payload),
                metrics_json=self._extract_result_field(inner, "metrics"),
                payoff_json=self._extract_result_field(inner, "payoff"),
                decision_json=self._extract_result_field(inner, "decision"),
                alerts_json=self._extract_result_field(inner, "alerts"),
                operation_state_json={
                    "pricing_execution": record,
                    "pricing_payload": pricing_payload,
                    "result": result,
                },
            )
        except Exception:
            logger.exception(
                "system_snapshots_repository.create_snapshot() falhou -- execução id=%s não afetada",
                record.get("id"),
            )
            return None

    @staticmethod
    def _build_structure_json(pricing_payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "structure_id": pricing_payload.get("structure_id"),
            "structure_name": pricing_payload.get("structure_name"),
            "underlying_asset": pricing_payload.get("underlying_asset"),
            "reference_date": pricing_payload.get("reference_date"),
            "meta": pricing_payload.get("meta"),
        }

    @staticmethod
    def _build_market_json(pricing_payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "spot_price": pricing_payload.get("spot_price"),
            "interest_rate": pricing_payload.get("interest_rate"),
            "volatility": pricing_payload.get("volatility"),
        }

    @staticmethod
    def _extract_result_field(inner: Any, field: str) -> Any:
        if not isinstance(inner, dict):
            return None

        value = inner.get(field)
        return value if value not in ({}, [], None) else None
