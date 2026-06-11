# services/pricing_execution_persistence_service.py
import logging
from typing import Any

from repositories.pricing_executions_repository import PricingExecutionsRepository
from services.payoff_persistence_port import PayoffPersistencePort

logger = logging.getLogger(__name__)


class PricingExecutionPersistenceService:
    def __init__(
        self,
        pricing_executions_repository: PricingExecutionsRepository | None = None,
        payoff_persistence_port: PayoffPersistencePort | None = None,
    ):
        self.pricing_executions_repository = (
            pricing_executions_repository or PricingExecutionsRepository()
        )
        self._payoff_port = payoff_persistence_port

    def persist_execution(
        self,
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
        duration_ms: int | None = None,
        error_message: str | None = None,
    ) -> dict[str, Any]:
        # result pode chegar como wrapper {"result": {...}} ou já desempacotado
        inner = result.get("result", result) if isinstance(result, dict) else result
        metrics   = inner.get("metrics",   {}) if isinstance(inner, dict) else {}
        valuation = inner.get("valuation", {}) if isinstance(inner, dict) else {}

        execution_engine        = inner.get("engine")        if isinstance(inner, dict) else None
        execution_status        = inner.get("status")        if isinstance(inner, dict) else None
        persisted_error_message = error_message or (inner.get("error_message") if isinstance(inner, dict) else None)
        number_of_legs          = metrics.get("number_of_legs")
        total_quantity          = metrics.get("total_quantity")
        theoretical_value       = valuation.get("theoretical_value")

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

        # ------------------------------------------------------------------ #
        #  alteracao_21 -- persistência derivada (payoff + decisão)                #
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

        return {
            "record": record,
        }
