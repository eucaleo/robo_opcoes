"""Operational cross validation service.

Pure read-only module for Phase 7R.5.

This module validates consistency between a simulated alert, a simulated decision
and an explainable operational explanation.

It does not access Excel, COM, databases, brokers, files, networks,
or any real operational execution path.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ATT.operational_decision_explanation_service import (
    ALLOWED_CLASSIFICATIONS,
    ALLOWED_CONFIDENCE_LEVELS,
    ALLOWED_SEVERITIES,
    CONTRACT_OUTPUT_FIELDS as EXPLANATION_CONTRACT_OUTPUT_FIELDS,
    OPERATIONAL_STATUS,
)


VALIDATION_OUTPUT_FIELDS = (
    "validation_status",
    "is_valid",
    "checked_event_id",
    "checked_alert_type",
    "inconsistencies",
    "warnings",
    "checks_performed",
    "data_traceability_status",
    "rule_traceability_status",
    "limitation_status",
    "operational_status",
    "audit_note",
)

ALLOWED_VALIDATION_STATUSES = {
    "valido",
    "valido_com_alertas",
    "invalido",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

EXPECTED_LIMITATIONS = (
    "dados simulados",
    "ausencia de Excel real",
    "ausencia de banco real",
    "ausencia de execucao operacional",
    "ausencia de broker",
    "ausencia de validacao em tempo real",
    "uso apenas diagnostico e auditavel",
)

RECOMMENDED_DATA_TRACE_FIELDS = (
    "asset",
    "timestamp",
    "observed_values",
    "thresholds",
    "source",
)

REQUIRED_RULE_FIELDS = (
    "name",
    "description",
    "condition",
    "result",
    "impact",
)

AUDIT_NOTE = (
    "Validacao cruzada gerada em modo somente leitura. "
    "Nao representa ordem operacional real, recomendacao executavel, "
    "acionamento de broker ou automacao de compra ou venda."
)


def validate_operational_cross_explanation(
    alert: Mapping[str, Any],
    decision: Mapping[str, Any],
    explanation: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate consistency between alert, decision and explanation.

    The function is deterministic and read-only. It only inspects dictionaries
    already supplied by the caller and returns an auditable validation result.
    """

    _ensure_mapping(alert, "alert")
    _ensure_mapping(decision, "decision")
    _ensure_mapping(explanation, "explanation")

    inconsistencies: list[str] = []
    warnings: list[str] = []
    checks_performed: list[str] = []

    checked_event_id = _first_non_empty(
        explanation.get("event_id"),
        decision.get("event_id"),
        alert.get("event_id"),
    )
    checked_alert_type = _first_non_empty(
        explanation.get("alert_type"),
        decision.get("alert_type"),
        alert.get("alert_type"),
    )

    checks_performed.append("estrutura_minima_da_explicacao")
    _check_explanation_contract(explanation, inconsistencies)

    checks_performed.append("consistencia_event_id")
    _check_field_consistency(
        field="event_id",
        alert=alert,
        decision=decision,
        explanation=explanation,
        inconsistencies=inconsistencies,
    )

    checks_performed.append("consistencia_alert_type")
    _check_field_consistency(
        field="alert_type",
        alert=alert,
        decision=decision,
        explanation=explanation,
        inconsistencies=inconsistencies,
    )

    checks_performed.append("classificacao_permitida")
    _check_allowed_value(
        field="classification",
        value=explanation.get("classification"),
        allowed=ALLOWED_CLASSIFICATIONS,
        inconsistencies=inconsistencies,
    )

    checks_performed.append("severidade_permitida")
    _check_allowed_value(
        field="severity",
        value=explanation.get("severity"),
        allowed=ALLOWED_SEVERITIES,
        inconsistencies=inconsistencies,
    )

    checks_performed.append("confianca_permitida")
    _check_allowed_value(
        field="confidence",
        value=explanation.get("confidence"),
        allowed=ALLOWED_CONFIDENCE_LEVELS,
        inconsistencies=inconsistencies,
    )

    checks_performed.append("motivos_objetivos")
    _check_reasons(explanation, inconsistencies, warnings)

    checks_performed.append("rastreabilidade_de_dados")
    data_traceability_status = _check_data_traceability(
        explanation=explanation,
        inconsistencies=inconsistencies,
        warnings=warnings,
    )

    checks_performed.append("rastreabilidade_de_regras")
    rule_traceability_status = _check_rule_traceability(
        explanation=explanation,
        inconsistencies=inconsistencies,
        warnings=warnings,
    )

    checks_performed.append("limitacoes_obrigatorias")
    limitation_status = _check_limitations(
        explanation=explanation,
        inconsistencies=inconsistencies,
        warnings=warnings,
    )

    checks_performed.append("status_operacional_somente_leitura")
    _check_operational_status(explanation, inconsistencies)

    checks_performed.append("guardrails_operacionais")
    guardrail_triggered = _detect_guardrail(alert, decision, explanation)
    if guardrail_triggered:
        inconsistencies.append(
            "Guardrail acionado: foi detectado texto ou campo associado a execucao operacional real."
        )

    checks_performed.append("warnings_diagnosticos")
    _collect_diagnostic_warnings(explanation, warnings)

    validation_status = _resolve_validation_status(
        explanation=explanation,
        inconsistencies=inconsistencies,
        warnings=warnings,
        guardrail_triggered=guardrail_triggered,
    )

    result = {
        "validation_status": validation_status,
        "is_valid": validation_status in {"valido", "valido_com_alertas"},
        "checked_event_id": checked_event_id,
        "checked_alert_type": checked_alert_type,
        "inconsistencies": _dedupe(inconsistencies),
        "warnings": _dedupe(warnings),
        "checks_performed": checks_performed,
        "data_traceability_status": data_traceability_status,
        "rule_traceability_status": rule_traceability_status,
        "limitation_status": limitation_status,
        "operational_status": OPERATIONAL_STATUS,
        "audit_note": AUDIT_NOTE,
    }

    return {field: result[field] for field in VALIDATION_OUTPUT_FIELDS}


def _ensure_mapping(value: Any, name: str) -> None:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _is_absent_marker(value: Any) -> bool:
    return _is_empty(value) or value == "ausente"


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if not _is_empty(value):
            return value
    return None


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _check_explanation_contract(
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
) -> None:
    for field in EXPLANATION_CONTRACT_OUTPUT_FIELDS:
        if field not in explanation:
            inconsistencies.append(f"Campo obrigatorio ausente na explicacao: {field}.")


def _check_field_consistency(
    *,
    field: str,
    alert: Mapping[str, Any],
    decision: Mapping[str, Any],
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
) -> None:
    values = {
        "alert": alert.get(field),
        "decision": decision.get(field),
        "explanation": explanation.get(field),
    }

    absent_sources = [source for source, value in values.items() if _is_empty(value)]
    for source in absent_sources:
        inconsistencies.append(f"{field} ausente em {source}.")

    present_values = {source: value for source, value in values.items() if not _is_empty(value)}
    unique_values = set(present_values.values())

    if len(unique_values) > 1:
        inconsistencies.append(
            f"{field} divergente entre alerta, decisao e explicacao."
        )


def _check_allowed_value(
    *,
    field: str,
    value: Any,
    allowed: set[str],
    inconsistencies: list[str],
) -> None:
    if _is_empty(value):
        inconsistencies.append(f"{field} ausente.")
        return

    if value not in allowed:
        inconsistencies.append(f"{field} nao permitido: {value}.")


def _check_reasons(
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
    warnings: list[str],
) -> None:
    reasons = explanation.get("reasons")

    if not isinstance(reasons, list) or not reasons:
        inconsistencies.append("Motivos ausentes ou invalidos.")
        return

    for index, reason in enumerate(reasons, start=1):
        if not isinstance(reason, str) or not reason.strip():
            inconsistencies.append(f"Motivo invalido na posicao {index}.")
        elif len(reason.strip()) < 15:
            warnings.append(f"Motivo potencialmente generico na posicao {index}.")


def _check_data_traceability(
    *,
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
    warnings: list[str],
) -> str:
    data_used = explanation.get("data_used")

    if not isinstance(data_used, Mapping) or not data_used:
        inconsistencies.append("Dados usados ausentes ou invalidos.")
        return "invalido"

    for field in ("event_id", "alert_type"):
        if _is_absent_marker(data_used.get(field)):
            inconsistencies.append(f"Dado usado obrigatorio ausente: {field}.")

    for field in RECOMMENDED_DATA_TRACE_FIELDS:
        if _is_absent_marker(data_used.get(field)):
            warnings.append(f"Dado recomendado ausente na rastreabilidade: {field}.")

    if any(item.startswith("Dado usado obrigatorio ausente") for item in inconsistencies):
        return "invalido"

    if any(item.startswith("Dado recomendado ausente na rastreabilidade") for item in warnings):
        return "com_alertas"

    return "ok"


def _check_rule_traceability(
    *,
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
    warnings: list[str],
) -> str:
    rules = explanation.get("rules_applied")

    if not isinstance(rules, list) or not rules:
        inconsistencies.append("Regras aplicadas ausentes ou invalidas.")
        return "invalido"

    invalid = False

    for rule_index, rule in enumerate(rules, start=1):
        if not isinstance(rule, Mapping):
            inconsistencies.append(f"Regra aplicada invalida na posicao {rule_index}.")
            invalid = True
            continue

        for field in REQUIRED_RULE_FIELDS:
            value = rule.get(field)
            if _is_empty(value):
                inconsistencies.append(
                    f"Regra aplicada incompleta na posicao {rule_index}: {field} ausente."
                )
                invalid = True

        if rule.get("condition") == "Condicao nao informada.":
            inconsistencies.append(
                f"Regra aplicada incompleta na posicao {rule_index}: condicao nao informada."
            )
            invalid = True

        if rule.get("result") == "nao_informado":
            inconsistencies.append(
                f"Regra aplicada incompleta na posicao {rule_index}: resultado nao informado."
            )
            invalid = True

        if rule.get("impact") == "nao_informado":
            warnings.append(
                f"Regra aplicada com impacto pouco detalhado na posicao {rule_index}."
            )

    if invalid:
        return "invalido"

    if any("Regra aplicada com impacto pouco detalhado" in item for item in warnings):
        return "com_alertas"

    return "ok"


def _check_limitations(
    *,
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
    warnings: list[str],
) -> str:
    limitations = explanation.get("limitations")

    if not isinstance(limitations, list) or not limitations:
        inconsistencies.append("Limitacoes ausentes ou invalidas.")
        return "invalido"

    normalized = {str(item).lower() for item in limitations}

    missing = [
        limitation
        for limitation in EXPECTED_LIMITATIONS
        if limitation.lower() not in normalized
    ]

    for limitation in missing:
        warnings.append(f"Limitacao esperada nao declarada: {limitation}.")

    if not limitations:
        return "invalido"

    if missing:
        return "com_alertas"

    return "ok"


def _check_operational_status(
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
) -> None:
    status = explanation.get("operational_status")

    if _is_empty(status):
        inconsistencies.append("operational_status ausente.")
        return

    if status != OPERATIONAL_STATUS:
        inconsistencies.append(
            "operational_status nao declara modo somente leitura esperado."
        )

    audit_note = explanation.get("audit_note")
    if _is_empty(audit_note):
        inconsistencies.append("audit_note ausente.")


def _collect_diagnostic_warnings(
    explanation: Mapping[str, Any],
    warnings: list[str],
) -> None:
    if explanation.get("confidence") == "baixa":
        warnings.append("Confianca baixa na explicacao.")

    if explanation.get("classification") == "inconclusivo":
        warnings.append("Classificacao inconclusiva.")

    if explanation.get("severity") == "critica_simulada":
        warnings.append("Severidade critica_simulada exige revisao diagnostica.")


def _resolve_validation_status(
    *,
    explanation: Mapping[str, Any],
    inconsistencies: list[str],
    warnings: list[str],
    guardrail_triggered: bool,
) -> str:
    if guardrail_triggered:
        return "bloqueado_por_guardrail"

    if inconsistencies:
        return "invalido"

    if explanation.get("classification") == "inconclusivo":
        return "inconclusivo"

    if warnings:
        return "valido_com_alertas"

    return "valido"


def _detect_guardrail(*payloads: Mapping[str, Any]) -> bool:
    """Detect explicit operational execution intent.

    Safety disclaimers and limitations are not treated as violations.
    The guardrail is triggered only when an intent-bearing field asks for
    real execution, broker activation, automation, trigger or similar action.
    """

    return any(_scan_guardrail_intent(payload) for payload in payloads)


def _scan_guardrail_intent(value: Any, key_context: str = "") -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            next_context = str(key).lower()
            if _scan_guardrail_intent(item, next_context):
                return True
        return False

    if isinstance(value, (list, tuple, set)):
        return any(_scan_guardrail_intent(item, key_context) for item in value)

    if not isinstance(value, str):
        return False

    if not _is_intent_context(key_context):
        return False

    return _contains_forbidden_operational_intent(value)


def _is_intent_context(key_context: str) -> bool:
    key = key_context.lower()

    intent_markers = (
        "requested_action",
        "action",
        "acao",
        "order",
        "ordem",
        "broker",
        "execution",
        "execucao",
        "execute",
        "executar",
        "trigger",
        "automation",
        "automacao",
        "command",
        "comando",
    )

    return any(marker in key for marker in intent_markers)


def _contains_forbidden_operational_intent(value: str) -> bool:
    text = value.lower()

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
        "recomendacao executavel",
        "automacao de compra",
        "automacao de venda",
    )

    return any(fragment in text for fragment in forbidden_fragments)
