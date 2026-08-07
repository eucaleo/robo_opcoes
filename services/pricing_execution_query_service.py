from datetime import datetime
from typing import Any

from repositories.pricing_executions_repository import PricingExecutionsRepository


class PricingExecutionQueryService:
    def __init__(
        self,
        pricing_executions_repository: PricingExecutionsRepository | None = None,
    ):
        self.pricing_executions_repository = (
            pricing_executions_repository or PricingExecutionsRepository()
        )

    def _validate_summary_filters(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> None:
        if structure_id is not None and structure_id <= 0:
            raise ValueError("structure_id must be greater than zero")

        if underlying_asset is not None and not underlying_asset.strip():
            raise ValueError("underlying_asset must not be empty")

        if status is not None and status not in {"ok", "error"}:
            raise ValueError("status must be either 'ok' or 'error'")

        if reference_date is not None:
            if not reference_date.strip():
                raise ValueError("reference_date must not be empty")

            try:
                datetime.strptime(reference_date, "%Y-%m-%d")
            except ValueError as exc:
                raise ValueError(
                    "reference_date must be in YYYY-MM-DD format"
                ) from exc

    def list_executions(self) -> list[dict[str, Any]]:
        return self.pricing_executions_repository.list_executions()

    def _load_executions_for_summary(
        self,
        structure_id: int | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Compatibilidade:
        - repositório real pode aceitar page/page_size/filtros;
        - fakes antigos dos testes aceitam list_executions() sem kwargs.
        """
        try:
            executions = self.pricing_executions_repository.list_executions(
                page=1,
                page_size=10_000,
                status=status,
                structure_id=structure_id,
                reference_date=reference_date,
            )
        except TypeError as exc:
            if "unexpected keyword argument" not in str(exc):
                raise
            executions = self.pricing_executions_repository.list_executions()

        if isinstance(executions, dict):
            executions = executions.get("items", [])

        return list(executions or [])

    def list_execution_summaries(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
        descending: bool = True,
    ) -> list[dict[str, Any]]:
        self._validate_summary_filters(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

        executions = self._load_executions_for_summary(
            structure_id=structure_id,
            status=status,
            reference_date=reference_date,
        )

        summaries = []
        for execution in executions:
            persisted_number_of_legs = execution.get("number_of_legs")
            persisted_total_quantity = execution.get("total_quantity")
            persisted_theoretical_value = execution.get("theoretical_value")

            nested_result = execution.get("result", {}) or {}
            engine_result = nested_result.get("result", nested_result)
            metrics = engine_result.get("metrics", {}) or {}
            valuation = engine_result.get("valuation", {}) or {}

            summary = {
                "id": execution["id"],
                "created_at": execution["created_at"],
                "structure_id": execution["structure_id"],
                "underlying_asset": execution["underlying_asset"],
                "reference_date": execution["reference_date"],
                "execution_engine": execution.get("execution_engine"),
                "execution_status": execution.get("execution_status"),
                "duration_ms": execution.get("duration_ms"),
                "error_message": execution.get("error_message"),
                "number_of_legs": (
                    persisted_number_of_legs
                    if persisted_number_of_legs is not None
                    else metrics.get("number_of_legs")
                ),
                "total_quantity": (
                    persisted_total_quantity
                    if persisted_total_quantity is not None
                    else metrics.get("total_quantity")
                ),
                "theoretical_value": (
                    persisted_theoretical_value
                    if persisted_theoretical_value is not None
                    else valuation.get("theoretical_value")
                ),
            }

            if structure_id is not None and summary["structure_id"] != structure_id:
                continue

            if underlying_asset is not None:
                if str(summary["underlying_asset"]).upper() != underlying_asset.upper():
                    continue

            if status is not None and summary["execution_status"] != status:
                continue

            if reference_date is not None and summary["reference_date"] != reference_date:
                continue

            summaries.append(summary)

        summaries.sort(key=lambda item: item["id"], reverse=descending)
        return summaries

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
        self._validate_summary_filters(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

        if page <= 0:
            raise ValueError("page must be greater than zero")

        if page_size <= 0:
            raise ValueError("page_size must be greater than zero")

        summaries = self.list_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            descending=descending,
        )

        total_items = len(summaries)
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        start = (page - 1) * page_size
        end = start + page_size
        items = summaries[start:end]

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_latest_execution_summary(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        self._validate_summary_filters(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

        summaries = self.list_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            descending=True,
        )

        if not summaries:
            raise ValueError("no pricing execution summaries found")

        return summaries[0]

    def get_execution(self, execution_id: int) -> dict[str, Any]:
        if execution_id <= 0:
            raise ValueError("execution_id must be greater than zero")

        execution = self.pricing_executions_repository.get_execution(execution_id)

        if execution is None:
            raise ValueError(f"pricing execution {execution_id} not found")

        return execution

    def get_execution_details(self, execution_id: int) -> dict[str, Any]:
        return self.get_execution(execution_id)

# [FRENTE 45] INICIO - estabilizacao envelope query retorno pricing
def _frente_45_get_pricing_envelope_contract():
    """Retorna o modulo do contrato canonico de envelope de pricing."""

    from services import pricing_execution_envelope as pricing_execution_envelope_contract

    return pricing_execution_envelope_contract


def _frente_45_has_minimum_pricing_envelope(value):
    """Confere o contrato minimo do envelope canonico de pricing."""

    required = {
        "status",
        "error_message",
        "pricing_payload",
        "engine_result",
        "persisted",
        "pricing_execution_id",
    }
    return isinstance(value, dict) and required.issubset(set(value.keys()))


def _frente_45_metadata(**metadata):
    """Monta metadata local da Frente 45 sem alterar persistencia ou schema."""

    current = dict(metadata)
    current.setdefault("frente", 45)
    current.setdefault("fase", "Fase 4 - Pricing e payoff")
    current.setdefault("query_return", True)
    current.setdefault("persistence_change", False)
    current.setdefault("schema_change", False)
    current.setdefault("operational_change", False)
    return current


def _frente_45_merge_metadata(envelope, metadata):
    """Acrescenta metadata ao envelope sem remover campos existentes."""

    result = dict(envelope)
    current = result.get("metadata")
    if not isinstance(current, dict):
        current = {}
    merged = dict(current)
    for key, value in metadata.items():
        merged.setdefault(key, value)
    result["metadata"] = merged
    return result


def _frente_45_extract_pricing_execution_id(result, metadata):
    """Extrai pricing_execution_id de retorno de query sem impor schema novo."""

    if isinstance(result, dict):
        for key in ("pricing_execution_id", "execution_id", "id"):
            value = result.get(key)
            if value is not None:
                return value
    return metadata.get("pricing_execution_id")


def _frente_45_stabilize_query_pricing_return(result, **metadata):
    """Estabiliza retorno de consulta de pricing no envelope canonico minimo.

    Esta funcao e intencionalmente conservadora:
    - nao altera banco;
    - nao cria schema;
    - nao troca repository;
    - nao muda fluxo operacional amplo;
    - apenas normaliza o formato de retorno para consumidores de query.
    """

    current_metadata = _frente_45_metadata(**metadata)

    if _frente_45_has_minimum_pricing_envelope(result):
        return _frente_45_merge_metadata(result, current_metadata)

    contract = _frente_45_get_pricing_envelope_contract()
    builders = (
        "normalize_pricing_envelope",
        "canonical_pricing_envelope",
        "build_pricing_envelope",
        "create_pricing_envelope",
    )

    for builder_name in builders:
        builder = getattr(contract, builder_name, None)
        if builder is None:
            continue
        attempts = (
            lambda: builder(result, **current_metadata),
            lambda: builder(result),
            lambda: builder(
                pricing_payload=(result.get("pricing_payload") if isinstance(result, dict) else None),
                engine_result=(result.get("result") if isinstance(result, dict) else result),
                persisted={"record": result},
                pricing_execution_id=_frente_45_extract_pricing_execution_id(result, current_metadata),
                metadata=current_metadata,
            ),
        )
        for attempt in attempts:
            try:
                candidate = attempt()
            except TypeError:
                continue
            if _frente_45_has_minimum_pricing_envelope(candidate):
                return _frente_45_merge_metadata(candidate, current_metadata)

    pricing_execution_id = _frente_45_extract_pricing_execution_id(result, current_metadata)

    if isinstance(result, dict):
        pricing_payload = result.get("pricing_payload")
        engine_result = result.get("engine_result", result.get("result", result))
        persisted = result.get("persisted")
        if not isinstance(persisted, dict):
            persisted = {"record": result}
        status = result.get("status", "ok")
        error_message = result.get("error_message")
    else:
        pricing_payload = None
        engine_result = result
        persisted = {"record": None}
        status = "ok"
        error_message = None

    envelope = {
        "status": status,
        "error_message": error_message,
        "pricing_payload": pricing_payload,
        "engine_result": engine_result,
        "persisted": persisted,
        "pricing_execution_id": pricing_execution_id,
        "metadata": current_metadata,
    }
    return envelope
# [FRENTE 45] FIM - estabilizacao envelope query retorno pricing
