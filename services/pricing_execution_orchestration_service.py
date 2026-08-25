import time
from typing import Any

from repositories.system_snapshots_repository import SystemSnapshotsRepository
from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)
from services.derived_payoff_persistence import DerivedPayoffPersistence
from services.pricing_execution_service import PricingExecutionService
from services.pricing_input_service import PricingInputService


class PricingExecutionOrchestrationService:
    def __init__(
        self,
        pricing_input_service: PricingInputService | None = None,
        pricing_execution_service: PricingExecutionService | None = None,
        pricing_execution_persistence_service: PricingExecutionPersistenceService | None = None,
    ):
        self.pricing_input_service = pricing_input_service or PricingInputService()
        self.pricing_execution_service = pricing_execution_service or PricingExecutionService(
            pricing_input_service=self.pricing_input_service,
        )
        self.pricing_execution_persistence_service = (
            pricing_execution_persistence_service
            or PricingExecutionPersistenceService(
                payoff_persistence_port=DerivedPayoffPersistence(),
                system_snapshots_repository=SystemSnapshotsRepository(),
            )
        )

    def execute_and_persist(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        started_at = time.perf_counter()

        try:
            result = self.pricing_execution_service.execute(
                structure_id=structure_id,
                reference_date=reference_date,
            )
            duration_ms = int((time.perf_counter() - started_at) * 1000)

            persisted = self.pricing_execution_persistence_service.persist_execution(
                pricing_payload=result["pricing_payload"],
                result=result,
                duration_ms=duration_ms,
                error_message=None,
            )

            return {
                "pricing_payload": result["pricing_payload"],
                "result": result,
                "persisted": persisted,
            }

        except Exception as exc:
            duration_ms = int((time.perf_counter() - started_at) * 1000)
            error_message = str(exc)

            result = {
                "pricing_payload": None,
                "result": {
                    "engine": "stub",
                    "status": "error",
                    "error_message": error_message,
                },
            }

            persisted = self.pricing_execution_persistence_service.persist_execution(
                pricing_payload=None,
                result=result,
                duration_ms=duration_ms,
                error_message=error_message,
            )

            return {
                "pricing_payload": None,
                "result": result,
                "persisted": persisted,
            }

# [FRENTE 43] INICIO - integracao envelope canonico fluxo pricing
def _frente_43_get_pricing_envelope_contract():
    """Retorna o modulo do contrato canonico de envelope de pricing.

    Esta funcao mantem a integracao local e controlada, sem alterar schema,
    persistencia ou fluxo operacional amplo.
    """

    from services import pricing_execution_envelope as pricing_execution_envelope_contract

    return pricing_execution_envelope_contract


def _frente_43_canonical_pricing_envelope(result, **metadata):
    """Normaliza retorno de pricing para o envelope canonico minimo.

    Contrato minimo esperado:
    - status
    - error_message
    - pricing_payload
    - engine_result
    - persisted
    - pricing_execution_id

    A funcao e intencionalmente conservadora: nao troca persistencia, nao troca
    schema e nao executa operacao operacional ampla.
    """

    _frente_43_get_pricing_envelope_contract()

    required_keys = {
        "status",
        "error_message",
        "pricing_payload",
        "engine_result",
        "persisted",
        "pricing_execution_id",
    }

    if isinstance(result, dict) and required_keys.issubset(set(result.keys())):
        envelope = dict(result)
        envelope.setdefault("metadata", {})
        if isinstance(envelope["metadata"], dict):
            envelope["metadata"].update(metadata)
        return envelope

    source = result if isinstance(result, dict) else {}

    status = (
        metadata.get("status")
        or source.get("status")
        or source.get("execution_status")
        or ("error" if source.get("error_message") or source.get("error") else "ok")
    )

    error_message = (
        metadata.get("error_message")
        or source.get("error_message")
        or source.get("error")
    )

    pricing_payload = (
        metadata.get("pricing_payload")
        or source.get("pricing_payload")
        or source.get("payload")
        or {}
    )

    engine_result = (
        metadata.get("engine_result")
        or source.get("engine_result")
        or source.get("result")
        or source.get("valuation")
        or {}
    )

    persisted = (
        metadata.get("persisted")
        or source.get("persisted")
        or {}
    )

    pricing_execution_id = (
        metadata.get("pricing_execution_id")
        or source.get("pricing_execution_id")
        or source.get("id")
    )

    return {
        "status": status,
        "error_message": error_message,
        "pricing_payload": pricing_payload,
        "engine_result": engine_result,
        "persisted": persisted,
        "pricing_execution_id": pricing_execution_id,
        "metadata": dict(metadata),
    }
# [FRENTE 43] FIM - integracao envelope canonico fluxo pricing

# [FRENTE 44] INICIO - propagacao controlada envelope retorno pricing
def _frente_44_is_pricing_envelope(value):
    """Confere o contrato minimo do envelope canonico de pricing."""

    if not isinstance(value, dict):
        return False

    required = {
        "status",
        "error_message",
        "pricing_payload",
        "engine_result",
        "persisted",
        "pricing_execution_id",
    }
    return required.issubset(set(value.keys()))


def _frente_44_propagate_pricing_envelope(result, **metadata):
    """Propaga retorno de pricing no envelope canonico de forma controlada.

    Esta frente nao troca persistencia, nao troca schema e nao altera fluxo
    operacional amplo. Ela apenas garante uma borda local para os services
    consumirem e retornarem o contrato minimo do envelope de pricing.
    """

    from services import pricing_execution_envelope as pricing_execution_envelope_contract

    source = result if isinstance(result, dict) else {}

    if _frente_44_is_pricing_envelope(source):
        envelope = dict(source)
    else:
        envelope = {}
        builder = None
        for name in (
            "ensure_pricing_execution_envelope",
            "canonical_pricing_envelope",
            "build_pricing_execution_envelope",
            "make_pricing_execution_envelope",
        ):
            candidate = getattr(pricing_execution_envelope_contract, name, None)
            if callable(candidate):
                builder = candidate
                break

        if builder is not None:
            try:
                built = builder(result, **metadata)
            except TypeError:
                try:
                    built = builder(result)
                except TypeError:
                    built = None
            if isinstance(built, dict):
                envelope = dict(built)

        if not envelope:
            status = source.get("status") or ("error" if source.get("error_message") else "ok")
            envelope = {
                "status": status,
                "error_message": source.get("error_message"),
                "pricing_payload": source.get("pricing_payload") or source.get("payload") or source,
                "engine_result": source.get("engine_result") or source.get("result") or source,
                "persisted": source.get("persisted") or {},
                "pricing_execution_id": source.get("pricing_execution_id") or source.get("id"),
            }

    defaults = {
        "status": "ok",
        "error_message": None,
        "pricing_payload": {},
        "engine_result": {},
        "persisted": {},
        "pricing_execution_id": None,
    }
    for key, value in defaults.items():
        envelope.setdefault(key, value)

    warnings_value = envelope.get("warnings")
    if warnings_value is None:
        warnings = []
    elif isinstance(warnings_value, list):
        warnings = list(warnings_value)
    elif isinstance(warnings_value, tuple):
        warnings = list(warnings_value)
    else:
        warnings = [str(warnings_value)]

    metadata_warnings = metadata.get("warnings")
    if isinstance(metadata_warnings, list):
        warnings.extend(str(item) for item in metadata_warnings)
    elif isinstance(metadata_warnings, tuple):
        warnings.extend(str(item) for item in metadata_warnings)
    elif metadata_warnings:
        warnings.append(str(metadata_warnings))

    envelope["warnings"] = warnings

    existing_metadata = envelope.get("metadata")
    if not isinstance(existing_metadata, dict):
        existing_metadata = {}

    merged_metadata = dict(existing_metadata)
    merged_metadata.update(metadata)
    envelope["metadata"] = merged_metadata

    return envelope


def _frente_44_extract_pricing_status(result):
    """Extrai status do envelope propagado com fallback seguro."""

    envelope = _frente_44_propagate_pricing_envelope(result)
    status = envelope.get("status")
    return status if status else "ok"
# [FRENTE 44] FIM - propagacao controlada envelope retorno pricing
