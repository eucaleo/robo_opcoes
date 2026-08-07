# services/pricing_execution_app_service.py
"""
execute_pricing() delegado para PricingExecutionOrchestrationService.

Alterações:
  - execute_pricing() agora usa PricingExecutionOrchestrationService no app.db consolidado
  - CanonicalPricingFacade removido do caminho de execução para evitar dependência legada
  - Todos os métodos de query (list, get, paginate, latest) inalterados
  - Validações _validate_structure_id / _validate_reference_date mantidas
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService
from services.pricing_execution_query_service import PricingExecutionQueryService

_DEFAULT_DB = Path("dados/app.db")


class PricingExecutionAppService:
    def __init__(
        self,
        canonical_pricing_facade: Any | None = None,
        pricing_execution_orchestration_service: PricingExecutionOrchestrationService | None = None,
        pricing_execution_query_service: PricingExecutionQueryService | None = None,
        db_path: Path | str = _DEFAULT_DB,
    ):
        # canonical_pricing_facade e db_path mantidos na assinatura por compatibilidade
        # com callers antigos, mas o fluxo atual usa app.db consolidado via orchestration.
        _ = (canonical_pricing_facade, db_path)

        self._orchestration = (
            pricing_execution_orchestration_service
            or PricingExecutionOrchestrationService()
        )
        self.pricing_execution_query_service = (
            pricing_execution_query_service or PricingExecutionQueryService()
        )

    # ------------------------------------------------------------------
    # Execução
    # ------------------------------------------------------------------

    def execute_pricing(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        self._validate_structure_id(structure_id)
        self._validate_reference_date(reference_date)

        response = self._orchestration.execute_and_persist(
            structure_id=structure_id,
            reference_date=reference_date,
        )

        # propaga erros como ValueError para manter contrato com callers existentes
        execution_result = response.get("result")
        inner_result = (
            execution_result.get("result")
            if isinstance(execution_result, dict)
            else None
        )

        status = response.get("status")
        error_message = response.get("error_message")

        if isinstance(inner_result, dict):
            status = inner_result.get("status", status)
            error_message = inner_result.get("error_message", error_message)
        elif isinstance(execution_result, dict):
            status = execution_result.get("status", status)
            error_message = execution_result.get("error_message", error_message)

        if status == "error":
            raise ValueError(error_message or "pricing execution failed")

        persisted = response.get("persisted")
        if isinstance(persisted, dict):
            record = persisted.get("record")
            if isinstance(record, dict):
                return record

        return response

    # ------------------------------------------------------------------
    # Queries -- inalteradas
    # ------------------------------------------------------------------

    def list_execution_summaries(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
        descending: bool = True,
    ) -> list[dict[str, Any]]:
        return self.pricing_execution_query_service.list_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            descending=descending,
        )

    def get_latest_execution_summary(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        return self.pricing_execution_query_service.get_latest_execution_summary(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

    def get_execution(self, execution_id: int) -> dict[str, Any]:
        return self.pricing_execution_query_service.get_execution(execution_id)

    def paginate_execution_summaries(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
        descending: bool = True,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, Any]:
        return self.pricing_execution_query_service.paginate_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            descending=descending,
            page=page,
            page_size=page_size,
        )

    # ------------------------------------------------------------------
    # Validações
    # ------------------------------------------------------------------

    def _validate_structure_id(self, structure_id: int) -> None:
        if structure_id <= 0:
            raise ValueError("structure_id must be greater than zero")

    def _validate_reference_date(self, reference_date: str | None) -> None:
        if reference_date is None:
            return

        try:
            parsed = datetime.strptime(reference_date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("reference_date must be in YYYY-MM-DD format") from exc

        if parsed.strftime("%Y-%m-%d") != reference_date:
            raise ValueError("reference_date must be in YYYY-MM-DD format")

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
