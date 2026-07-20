"""Operational decision explanation service.

Pure read-only module for Phase 7R.4.

This module does not access Excel, COM, databases, brokers, files, networks,
or any real operational execution path.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


ALLOWED_CLASSIFICATIONS = {
    "informativo",
    "atencao",
    "risco_simulado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

ALLOWED_SEVERITIES = {
    "baixa",
    "media",
    "alta",
    "critica_simulada",
}

ALLOWED_CONFIDENCE_LEVELS = {
    "baixa",
    "media",
    "alta",
}

REQUIRED_INPUT_FIELDS = (
    "event_id",
    "alert_type",
)

RECOMMENDED_INPUT_FIELDS = (
    "asset",
    "timestamp",
    "observed_values",
    "thresholds",
    "candidate_rules",
    "source",
)

CONTRACT_OUTPUT_FIELDS = (
    "event_id",
    "alert_type",
    "classification",
    "severity",
    "confidence",
    "reasons",
    "data_used",
    "rules_applied",
    "limitations",
    "operational_status",
    "audit_note",
)

DEFAULT_LIMITATIONS = (
    "dados simulados",
    "ausencia de Excel real",
    "ausencia de banco real",
    "ausencia de execucao operacional",
    "ausencia de broker",
    "ausencia de validacao em tempo real",
    "uso apenas diagnostico e auditavel",
)

OPERATIONAL_STATUS = "SOMENTE_LEITURA_SEM_EXECUCAO_REAL"

AUDIT_NOTE = (
    "Decisao explicavel gerada em modo somente leitura. "
    "Nao representa ordem operacional real, recomendacao executavel, "
    "acionamento de broker ou automacao de compra ou venda."
)


def explain_operational_decision(event: Mapping[str, Any]) -> dict[str, Any]:
    """Build an explainable operational decision from simulated input.

    The function is deterministic and read-only. It only transforms the input
    mapping into an auditable explanation payload aligned with Phase 7R.4.
    """

    if not isinstance(event, Mapping):
        raise TypeError("event must be a mapping")

    missing_required = _missing_fields(event, REQUIRED_INPUT_FIELDS)
    missing_recommended = _missing_fields(event, RECOMMENDED_INPUT_FIELDS)
    guardrail_triggered = _detect_guardrail(event)

    rules_applied = _normalize_rules(
        event.get("candidate_rules")
        or event.get("rules_applied")
        or event.get("rules")
    )

    classification = _resolve_classification(
        event=event,
        guardrail_triggered=guardrail_triggered,
        missing_required=missing_required,
    )

    severity = _resolve_severity(event=event, classification=classification)
    confidence = _resolve_confidence(
        classification=classification,
        missing_required=missing_required,
        missing_recommended=missing_recommended,
        rules_applied=rules_applied,
        guardrail_triggered=guardrail_triggered,
    )

    data_used = _build_data_used(event)
    limitations = _build_limitations(event)

    reasons = _build_reasons(
        classification=classification,
        severity=severity,
        confidence=confidence,
        missing_required=missing_required,
        missing_recommended=missing_recommended,
        rules_applied=rules_applied,
        guardrail_triggered=guardrail_triggered,
    )

    explanation = {
        "event_id": event.get("event_id"),
        "alert_type": event.get("alert_type"),
        "classification": classification,
        "severity": severity,
        "confidence": confidence,
        "reasons": reasons,
        "data_used": data_used,
        "rules_applied": rules_applied,
        "limitations": limitations,
        "operational_status": OPERATIONAL_STATUS,
        "audit_note": AUDIT_NOTE,
    }

    return {field: explanation[field] for field in CONTRACT_OUTPUT_FIELDS}


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _missing_fields(event: Mapping[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [field for field in fields if _is_empty(event.get(field))]


def _resolve_classification(
    *,
    event: Mapping[str, Any],
    guardrail_triggered: bool,
    missing_required: list[str],
) -> str:
    if guardrail_triggered:
        return "bloqueado_por_guardrail"

    if missing_required:
        return "inconclusivo"

    supplied = event.get("classification") or event.get("prior_classification")

    if supplied in ALLOWED_CLASSIFICATIONS:
        return str(supplied)

    if supplied:
        return "inconclusivo"

    return "inconclusivo"


def _resolve_severity(*, event: Mapping[str, Any], classification: str) -> str:
    supplied = event.get("severity")

    if supplied in ALLOWED_SEVERITIES:
        return str(supplied)

    if classification == "bloqueado_por_guardrail":
        return "critica_simulada"

    if classification == "risco_simulado":
        return "alta"

    if classification == "atencao":
        return "media"

    return "baixa"


def _resolve_confidence(
    *,
    classification: str,
    missing_required: list[str],
    missing_recommended: list[str],
    rules_applied: list[dict[str, Any]],
    guardrail_triggered: bool,
) -> str:
    if missing_required:
        return "baixa"

    if guardrail_triggered:
        return "alta"

    if classification == "inconclusivo":
        return "baixa"

    if not rules_applied:
        return "media"

    if len(missing_recommended) >= 4:
        return "baixa"

    if missing_recommended:
        return "media"

    return "alta"


def _normalize_rules(value: Any) -> list[dict[str, Any]]:
    if _is_empty(value):
        return []

    if isinstance(value, Mapping):
        items = [value]
    elif isinstance(value, (list, tuple)):
        items = list(value)
    else:
        items = [value]

    normalized: list[dict[str, Any]] = []

    for index, item in enumerate(items, start=1):
        if isinstance(item, Mapping):
            name = (
                item.get("name")
                or item.get("id")
                or item.get("rule_id")
                or f"regra_{index}"
            )
            description = (
                item.get("description")
                or item.get("descricao")
                or "Regra sem descricao detalhada."
            )
            condition = (
                item.get("condition")
                or item.get("condicao")
                or "Condicao nao informada."
            )
            result = item.get("result", item.get("resultado", "nao_informado"))
            impact = item.get("impact", item.get("impacto", "nao_informado"))
        else:
            name = str(item)
            description = "Regra informada em formato textual."
            condition = "Condicao nao informada."
            result = "nao_informado"
            impact = "nao_informado"

        normalized.append(
            {
                "name": str(name),
                "description": str(description),
                "condition": str(condition),
                "result": _stringify_result(result),
                "impact": str(impact),
            }
        )

    return normalized


def _stringify_result(value: Any) -> str:
    if value is True:
        return "verdadeiro"

    if value is False:
        return "falso"

    return str(value)


def _build_data_used(event: Mapping[str, Any]) -> dict[str, Any]:
    fields = (
        "event_id",
        "alert_type",
        "asset",
        "timestamp",
        "observed_values",
        "thresholds",
        "classification",
        "prior_classification",
        "severity",
        "source",
    )

    data: dict[str, Any] = {}

    for field in fields:
        value = event.get(field)
        data[field] = "ausente" if _is_empty(value) else value

    return data


def _build_limitations(event: Mapping[str, Any]) -> list[str]:
    limitations = list(DEFAULT_LIMITATIONS)

    extra = event.get("limitations")

    if isinstance(extra, str) and extra:
        limitations.append(extra)
    elif isinstance(extra, (list, tuple)):
        limitations.extend(str(item) for item in extra if not _is_empty(item))

    return list(dict.fromkeys(limitations))


def _build_reasons(
    *,
    classification: str,
    severity: str,
    confidence: str,
    missing_required: list[str],
    missing_recommended: list[str],
    rules_applied: list[dict[str, Any]],
    guardrail_triggered: bool,
) -> list[str]:
    reasons: list[str] = []

    if guardrail_triggered:
        reasons.append(
            "Guardrail acionado: entrada indica tentativa ou pedido de execucao operacional real."
        )

    for field in missing_required:
        reasons.append(f"Dado obrigatorio ausente: {field}.")

    for field in missing_recommended:
        reasons.append(f"Dado recomendado ausente: {field}.")

    reasons.append(f"Classificacao definida como {classification}.")
    reasons.append(f"Severidade definida como {severity}.")
    reasons.append(f"Confianca definida como {confidence}.")

    if rules_applied:
        for rule in rules_applied:
            reasons.append(
                "Regra aplicada: "
                f"{rule['name']} com resultado {rule['result']} "
                f"e impacto {rule['impact']}."
            )
    else:
        reasons.append("Nenhuma regra candidata foi informada para a explicacao.")

    reasons.append(
        "Saida mantida em modo somente leitura, sem ordem, broker, Excel real, COM ou banco real."
    )

    return reasons


def _detect_guardrail(event: Mapping[str, Any]) -> bool:
    boolean_flags = (
        "guardrail_violation",
        "blocked_by_guardrail",
        "forbidden_operation_requested",
    )

    if any(bool(event.get(flag)) for flag in boolean_flags):
        return True

    text_fields = (
        "requested_action",
        "action",
        "operation",
        "instruction",
        "operational_request",
    )

    combined_text = " ".join(
        str(event.get(field, "")).lower() for field in text_fields
    )

    forbidden_fragments = (
        "executar ordem",
        "enviar ordem",
        "acionar broker",
        "ordem real",
        "compra real",
        "venda real",
        "excel real",
        "usar com",
        "banco real",
        "loop tempo real",
        "trigger operacional",
    )

    return any(fragment in combined_text for fragment in forbidden_fragments)
