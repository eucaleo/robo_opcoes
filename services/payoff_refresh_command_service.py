from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from services.pricing_execution_app_service import PricingExecutionAppService

from repositories.payoff_refresh_command_service_sql_boundary import (
    _PayoffRefreshCommandService__latest_snapshot_id as _boundary__PayoffRefreshCommandService__latest_snapshot_id,
    _PayoffRefreshCommandService__decision_exists as _boundary__PayoffRefreshCommandService__decision_exists,
    _PayoffRefreshCommandService__latest_payoff_summary as _boundary__PayoffRefreshCommandService__latest_payoff_summary,
    _PayoffRefreshCommandService__connect as _boundary__PayoffRefreshCommandService__connect,
    _PayoffRefreshCommandService__ensure_active_structure as _boundary__PayoffRefreshCommandService__ensure_active_structure,
)


class PayoffRefreshCommandService:
    """
    Serviço oficial para refresh operacional de payoff.

    Regra arquitetural:
    - UI não calcula payoff.
    - UI chama este serviço.
    - Este serviço chama PricingExecutionAppService.
    - A persistência derivada deve acontecer no wiring oficial.
    - Após a execução, este serviço valida se houve payoff persistido.
    """

    def __init__(
        self,
        pricing_app_service: PricingExecutionAppService | None = None,
        db_path: str | Path | None = None,
    ) -> None:
        self.pricing_app_service = pricing_app_service or PricingExecutionAppService()
        self.db_path = Path(db_path or "dados/app.db")

    def refresh_payoff_for_structure(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        structure_id = self._validate_structure_id(structure_id)

        before_ts = self._latest_payoff_timestamp(structure_id)

        try:
            pricing_result = self._execute_pricing(structure_id, reference_date)
        except Exception as exc:
            return {
                "status": "error",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": None,
                "snapshot_id": None,
                "payoff_points_count": 0,
                "latest_payoff_timestamp": before_ts,
                "decision_found": False,
                "message": f"Erro ao executar pricing: {exc}",
            }

        pricing_status = self._extract_status(pricing_result)
        pricing_execution_id = self._extract_pricing_execution_id(pricing_result)

        if pricing_status in {"error", "failed", "fail"}:
            return {
                "status": "error",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": pricing_execution_id,
                "snapshot_id": None,
                "payoff_points_count": 0,
                "latest_payoff_timestamp": before_ts,
                "decision_found": False,
                "message": "Pricing retornou erro. Payoff não será considerado atualizado.",
                "pricing_result": pricing_result,
            }

        payoff_summary = self._latest_payoff_summary(structure_id)
        after_ts = payoff_summary.get("latest_payoff_timestamp")
        points_count = int(payoff_summary.get("payoff_points_count") or 0)

        decision_found = self._decision_exists(structure_id, after_ts)
        snapshot_id = self._latest_snapshot_id(structure_id)

        if points_count <= 0:
            return {
                "status": "error",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": pricing_execution_id,
                "snapshot_id": snapshot_id,
                "payoff_points_count": 0,
                "latest_payoff_timestamp": after_ts,
                "decision_found": decision_found,
                "message": (
                    "Pricing executado, mas nenhum payoff persistido foi encontrado. "
                    "Verifique o wiring de DerivedPayoffPersistence."
                ),
                "pricing_result": pricing_result,
            }

        if before_ts == after_ts:
            return {
                "status": "warning",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": pricing_execution_id,
                "snapshot_id": snapshot_id,
                "payoff_points_count": points_count,
                "latest_payoff_timestamp": after_ts,
                "decision_found": decision_found,
                "message": (
                    "Pricing executado, mas o timestamp do payoff não mudou. "
                    "Pode haver persistência antiga, deduplicação ou falha silenciosa."
                ),
                "pricing_result": pricing_result,
            }

        return {
            "status": "ok",
            "structure_id": structure_id,
            "reference_date": reference_date,
            "pricing_execution_id": pricing_execution_id,
            "snapshot_id": snapshot_id,
            "payoff_points_count": points_count,
            "latest_payoff_timestamp": after_ts,
            "decision_found": decision_found,
            "message": "Payoff atualizado com sucesso.",
            "pricing_result": pricing_result,
        }

    def _execute_pricing(
        self,
        structure_id: int,
        reference_date: str | None,
    ) -> Any:
        method = self.pricing_app_service.execute_pricing
        signature = inspect.signature(method)

        kwargs: dict[str, Any] = {"structure_id": structure_id}

        if reference_date is not None and "reference_date" in signature.parameters:
            kwargs["reference_date"] = reference_date

        return method(**kwargs)

    def _validate_structure_id(self, structure_id: int) -> int:
        try:
            value = int(structure_id)
        except Exception as exc:
            raise ValueError("structure_id inválido") from exc

        if value <= 0:
            raise ValueError("structure_id deve ser maior que zero")

        self._ensure_active_structure(value)

        return value

    def _ensure_active_structure(*args, **kwargs):
        return _boundary__PayoffRefreshCommandService__ensure_active_structure(*args, **kwargs)

    def _connect(*args, **kwargs):
        return _boundary__PayoffRefreshCommandService__connect(*args, **kwargs)

    def _latest_payoff_timestamp(self, structure_id: int) -> str | None:
        return self._latest_payoff_summary(structure_id).get("latest_payoff_timestamp")

    def _latest_payoff_summary(*args, **kwargs):
        return _boundary__PayoffRefreshCommandService__latest_payoff_summary(*args, **kwargs)

    def _decision_exists(*args, **kwargs):
        return _boundary__PayoffRefreshCommandService__decision_exists(*args, **kwargs)

    def _latest_snapshot_id(*args, **kwargs):
        return _boundary__PayoffRefreshCommandService__latest_snapshot_id(*args, **kwargs)

    def _extract_status(self, result: Any) -> str | None:
        if isinstance(result, dict):
            value = result.get("status")
            return str(value).lower() if value is not None else None

        value = getattr(result, "status", None)
        return str(value).lower() if value is not None else None

    def _extract_pricing_execution_id(self, result: Any) -> int | None:
        keys = [
            "pricing_execution_id",
            "execution_id",
            "id",
        ]

        if isinstance(result, dict):
            for key in keys:
                value = result.get(key)
                if value is not None:
                    try:
                        return int(value)
                    except Exception:
                        return None

        for key in keys:
            value = getattr(result, key, None)
            if value is not None:
                try:
                    return int(value)
                except Exception:
                    return None

        return None
