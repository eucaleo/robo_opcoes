"""Audit trail consolidation service for Phase 7R.6.

This module consolidates simulated alerts, simulated decisions, operational
explanations and cross validation results into a single read-only audit trail.

It does not access Excel, COM, real databases, brokers, network resources or
external files. It does not execute operational orders.
"""

from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


CONSOLIDATION_OUTPUT_FIELDS: Tuple[str, ...] = (
    "consolidated_status",
    "is_consolidated",
    "event_id",
    "alert_type",
    "chain_components",
    "chain_consistency_status",
    "validation_status",
    "explanation_status",
    "decision_status",
    "alert_status",
    "inconsistencies",
    "warnings",
    "checks_performed",
    "limitations",
    "guardrail_status",
    "operational_status",
    "audit_summary",
    "audit_note",
)

ALLOWED_CONSOLIDATED_STATUSES = {
    "consolidado",
    "consolidado_com_alertas",
    "nao_consolidado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

ALLOWED_VALIDATION_STATUSES = {
    "valido",
    "valido_com_alertas",
    "invalido",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

READ_ONLY_OPERATIONAL_STATUS = "somente_leitura"


def consolidate_audit_trail(
    alert: Mapping[str, Any],
    decision: Mapping[str, Any],
    explanation: Mapping[str, Any],
    cross_validation: Mapping[str, Any],
    metadata: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Consolidate an audit trail in read-only diagnostic mode."""

    inconsistencies: List[str] = []
    warnings: List[str] = []
    checks_performed: List[str] = []

    metadata = metadata or {}

    payloads = (alert, decision, explanation, cross_validation, metadata)

    if not all(isinstance(payload, Mapping) for payload in payloads):
        return _build_result(
            status="nao_consolidado",
            is_consolidated=False,
            event_id=None,
            alert_type=None,
            chain_components={
                "alert": "invalido",
                "decision": "invalido",
                "explanation": "invalido",
                "cross_validation": "invalido",
            },
            chain_consistency_status="inconsistente",
            validation_status="ausente",
            explanation_status="invalido",
            decision_status="invalido",
            alert_status="invalido",
            inconsistencies=["Entradas invalidas: todos os componentes devem ser mapeamentos."],
            warnings=[],
            checks_performed=["validacao_tipo_entrada"],
            limitations=_default_limitations(),
            guardrail_status="preservado",
            audit_summary="Trilha nao consolidada por entrada invalida.",
            audit_note=_default_audit_note("nao_consolidado"),
        )

    checks_performed.append("validacao_tipo_entrada")

    if _detect_guardrail(alert, decision, explanation, cross_validation, metadata):
        return _build_result(
            status="bloqueado_por_guardrail",
            is_consolidated=False,
            event_id=_first_present(_candidate_event_ids(alert, decision, explanation, cross_validation)),
            alert_type=_first_present(_candidate_alert_types(alert, decision, explanation, cross_validation)),
            chain_components=_component_map(alert, decision, explanation, cross_validation),
            chain_consistency_status="inconsistente",
            validation_status=_as_text(cross_validation.get("validation_status"), "ausente"),
            explanation_status=_component_status(explanation, ("event_id", "alert_type")),
            decision_status=_component_status(decision, ("event_id", "alert_type")),
            alert_status=_component_status(alert, ("event_id", "alert_type")),
            inconsistencies=["Guardrail operacional acionado por indicio de execucao real em campo de acao ou comando."],
            warnings=[],
            checks_performed=checks_performed + ["guardrail_operacional"],
            limitations=_collect_limitations(explanation, cross_validation),
            guardrail_status="bloqueado",
            audit_summary="Consolidacao bloqueada por guardrail operacional.",
            audit_note=_default_audit_note("bloqueado_por_guardrail"),
        )

    checks_performed.append("guardrail_operacional")

    chain_components = _component_map(alert, decision, explanation, cross_validation)
    checks_performed.append("verificacao_componentes_cadeia")

    for component_name, component_status in chain_components.items():
        if component_status == "ausente":
            inconsistencies.append(f"Componente obrigatorio ausente: {component_name}.")
        elif component_status == "invalido":
            inconsistencies.append(f"Componente obrigatorio invalido: {component_name}.")

    event_id, event_id_inconsistencies = _resolve_consensus(
        "event_id",
        _candidate_event_ids(alert, decision, explanation, cross_validation),
    )
    alert_type, alert_type_inconsistencies = _resolve_consensus(
        "alert_type",
        _candidate_alert_types(alert, decision, explanation, cross_validation),
    )

    inconsistencies.extend(event_id_inconsistencies)
    inconsistencies.extend(alert_type_inconsistencies)
    checks_performed.append("validacao_consistencia_event_id")
    checks_performed.append("validacao_consistencia_alert_type")

    validation_status = _as_text(cross_validation.get("validation_status"), "ausente")
    if validation_status == "ausente":
        inconsistencies.append("Status de validacao cruzada ausente.")
    elif validation_status not in ALLOWED_VALIDATION_STATUSES:
        inconsistencies.append("Status de validacao cruzada nao permitido.")
    elif validation_status == "invalido":
        inconsistencies.append("Validacao cruzada invalida propagada para consolidacao.")
    elif validation_status == "bloqueado_por_guardrail":
        inconsistencies.append("Validacao cruzada bloqueada por guardrail propagada para consolidacao.")

    checks_performed.append("validacao_status_validacao_cruzada")

    propagated_inconsistencies = _as_list(cross_validation.get("inconsistencies"))
    if propagated_inconsistencies:
        inconsistencies.extend(
            f"Inconsistencia propagada da validacao cruzada: {item}"
            for item in propagated_inconsistencies
        )

    propagated_warnings = _as_list(cross_validation.get("warnings"))
    if propagated_warnings:
        warnings.extend(
            f"Warning propagado da validacao cruzada: {item}"
            for item in propagated_warnings
        )

    explanation_warnings = _as_list(explanation.get("warnings"))
    if explanation_warnings:
        warnings.extend(
            f"Warning propagado da explicacao: {item}"
            for item in explanation_warnings
        )

    checks_performed.append("propagacao_inconsistencias_warnings")

    limitations = _collect_limitations(explanation, cross_validation)
    if not limitations:
        inconsistencies.append("Limitacoes obrigatorias ausentes.")

    checks_performed.append("validacao_limitacoes")

    if not explanation.get("audit_note"):
        inconsistencies.append("Audit note da explicacao ausente.")

    if not cross_validation.get("audit_note"):
        warnings.append("Audit note da validacao cruzada ausente.")

    checks_performed.append("validacao_notas_auditoria")

    explanation_status = _explanation_status(explanation)
    decision_status = _component_status(decision, ("event_id", "alert_type"))
    alert_status = _component_status(alert, ("event_id", "alert_type"))

    if _is_inconclusive(explanation, cross_validation):
        warnings.append("Trilha contem classificacao ou validacao inconclusiva.")

    if validation_status == "bloqueado_por_guardrail":
        consolidated_status = "bloqueado_por_guardrail"
        chain_consistency_status = "inconsistente"
    elif inconsistencies:
        consolidated_status = "nao_consolidado"
        chain_consistency_status = "inconsistente"
    elif _is_inconclusive(explanation, cross_validation):
        consolidated_status = "inconclusivo"
        chain_consistency_status = "inconclusivo"
    elif warnings:
        consolidated_status = "consolidado_com_alertas"
        chain_consistency_status = "consistente"
    else:
        consolidated_status = "consolidado"
        chain_consistency_status = "consistente"

    checks_performed.append("atribuicao_status_consolidado")

    return _build_result(
        status=consolidated_status,
        is_consolidated=consolidated_status in {"consolidado", "consolidado_com_alertas"},
        event_id=event_id,
        alert_type=alert_type,
        chain_components=chain_components,
        chain_consistency_status=chain_consistency_status,
        validation_status=validation_status,
        explanation_status=explanation_status,
        decision_status=decision_status,
        alert_status=alert_status,
        inconsistencies=inconsistencies,
        warnings=warnings,
        checks_performed=checks_performed,
        limitations=limitations or _default_limitations(),
        guardrail_status="preservado",
        audit_summary=_audit_summary(consolidated_status, inconsistencies, warnings),
        audit_note=_default_audit_note(consolidated_status),
    )


def _build_result(
    *,
    status: str,
    is_consolidated: bool,
    event_id: Optional[str],
    alert_type: Optional[str],
    chain_components: Mapping[str, str],
    chain_consistency_status: str,
    validation_status: str,
    explanation_status: str,
    decision_status: str,
    alert_status: str,
    inconsistencies: Sequence[str],
    warnings: Sequence[str],
    checks_performed: Sequence[str],
    limitations: Sequence[str],
    guardrail_status: str,
    audit_summary: str,
    audit_note: str,
) -> Dict[str, Any]:
    result = {
        "consolidated_status": status,
        "is_consolidated": is_consolidated,
        "event_id": event_id,
        "alert_type": alert_type,
        "chain_components": dict(chain_components),
        "chain_consistency_status": chain_consistency_status,
        "validation_status": validation_status,
        "explanation_status": explanation_status,
        "decision_status": decision_status,
        "alert_status": alert_status,
        "inconsistencies": list(inconsistencies),
        "warnings": list(warnings),
        "checks_performed": list(checks_performed),
        "limitations": list(limitations),
        "guardrail_status": guardrail_status,
        "operational_status": READ_ONLY_OPERATIONAL_STATUS,
        "audit_summary": audit_summary,
        "audit_note": audit_note,
    }

    return {field: result[field] for field in CONSOLIDATION_OUTPUT_FIELDS}


def _component_map(
    alert: Mapping[str, Any],
    decision: Mapping[str, Any],
    explanation: Mapping[str, Any],
    cross_validation: Mapping[str, Any],
) -> Dict[str, str]:
    return {
        "alert": _component_status(alert, ("event_id", "alert_type")),
        "decision": _component_status(decision, ("event_id", "alert_type")),
        "explanation": _component_status(explanation, ("event_id", "alert_type")),
        "cross_validation": _cross_validation_component_status(cross_validation),
    }


def _component_status(component: Mapping[str, Any], required_fields: Iterable[str]) -> str:
    if not component:
        return "ausente"

    missing = [field for field in required_fields if not component.get(field)]
    if missing:
        return "invalido"

    if _as_text(component.get("classification"), "") == "inconclusivo":
        return "inconclusivo"

    return "presente"


def _cross_validation_component_status(component: Mapping[str, Any]) -> str:
    if not component:
        return "ausente"

    validation_status = _as_text(component.get("validation_status"), "")
    if not validation_status:
        return "invalido"

    if validation_status not in ALLOWED_VALIDATION_STATUSES:
        return "invalido"

    if validation_status == "inconclusivo":
        return "inconclusivo"

    if validation_status in {"invalido", "bloqueado_por_guardrail"}:
        return "invalido"

    return "presente"


def _explanation_status(explanation: Mapping[str, Any]) -> str:
    if not explanation:
        return "ausente"

    if not explanation.get("event_id") or not explanation.get("alert_type"):
        return "invalido"

    if _as_text(explanation.get("classification"), "") == "inconclusivo":
        return "inconclusivo"

    return "presente"


def _candidate_event_ids(
    alert: Mapping[str, Any],
    decision: Mapping[str, Any],
    explanation: Mapping[str, Any],
    cross_validation: Mapping[str, Any],
) -> List[Tuple[str, Optional[str]]]:
    return [
        ("alert", _optional_text(alert.get("event_id"))),
        ("decision", _optional_text(decision.get("event_id"))),
        ("explanation", _optional_text(explanation.get("event_id"))),
        ("cross_validation", _optional_text(cross_validation.get("checked_event_id") or cross_validation.get("event_id"))),
    ]


def _candidate_alert_types(
    alert: Mapping[str, Any],
    decision: Mapping[str, Any],
    explanation: Mapping[str, Any],
    cross_validation: Mapping[str, Any],
) -> List[Tuple[str, Optional[str]]]:
    return [
        ("alert", _optional_text(alert.get("alert_type"))),
        ("decision", _optional_text(decision.get("alert_type"))),
        ("explanation", _optional_text(explanation.get("alert_type"))),
        ("cross_validation", _optional_text(cross_validation.get("checked_alert_type") or cross_validation.get("alert_type"))),
    ]


def _resolve_consensus(name: str, candidates: Sequence[Tuple[str, Optional[str]]]) -> Tuple[Optional[str], List[str]]:
    present = [(source, value) for source, value in candidates if value]

    if not present:
        return None, [f"{name} ausente em todos os componentes."]

    unique_values = {value for _, value in present}
    if len(unique_values) > 1:
        detail = ", ".join(f"{source}={value}" for source, value in present)
        return present[0][1], [f"{name} divergente entre componentes: {detail}."]

    return present[0][1], []


def _first_present(candidates: Sequence[Tuple[str, Optional[str]]]) -> Optional[str]:
    for _, value in candidates:
        if value:
            return value
    return None


def _collect_limitations(
    explanation: Mapping[str, Any],
    cross_validation: Mapping[str, Any],
) -> List[str]:
    limitations: List[str] = []

    for item in _as_list(explanation.get("limitations")):
        if item not in limitations:
            limitations.append(item)

    for item in _as_list(cross_validation.get("limitations")):
        if item not in limitations:
            limitations.append(item)

    return limitations


def _default_limitations() -> List[str]:
    return [
        "dados simulados",
        "ausencia de Excel real",
        "ausencia de banco real",
        "ausencia de execucao operacional",
        "ausencia de broker",
        "ausencia de validacao em tempo real",
        "uso apenas diagnostico e auditavel",
        "consolidacao somente leitura",
        "dependencia da qualidade das entradas fornecidas",
    ]


def _detect_guardrail(*payloads: Mapping[str, Any]) -> bool:
    return any(_scan_guardrail_intent(payload) for payload in payloads)


def _scan_guardrail_intent(value: Any, key_context: str = "") -> bool:
    if isinstance(value, Mapping):
        return any(_scan_guardrail_intent(item, str(key).lower()) for key, item in value.items())

    if isinstance(value, (list, tuple, set)):
        return any(_scan_guardrail_intent(item, key_context) for item in value)

    if not isinstance(value, str):
        return False

    if not _is_intent_context(key_context):
        return False

    return _contains_forbidden_operational_intent(value)


def _is_intent_context(key_context: str) -> bool:
    markers = (
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
    return any(marker in key_context.lower() for marker in markers)


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


def _is_inconclusive(
    explanation: Mapping[str, Any],
    cross_validation: Mapping[str, Any],
) -> bool:
    return (
        _as_text(explanation.get("classification"), "") == "inconclusivo"
        or _as_text(cross_validation.get("validation_status"), "") == "inconclusivo"
    )


def _audit_summary(status: str, inconsistencies: Sequence[str], warnings: Sequence[str]) -> str:
    return (
        f"Status consolidado: {status}. "
        f"Inconsistencias: {len(inconsistencies)}. "
        f"Warnings: {len(warnings)}. "
        "Resultado somente leitura e nao executavel."
    )


def _default_audit_note(status: str) -> str:
    return (
        f"Consolidacao auditavel encerrada com status {status}. "
        "A saida e diagnostica, somente leitura e sem autorizacao para execucao real."
    )


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []

    if isinstance(value, str):
        return [value] if value else []

    if isinstance(value, Iterable):
        return [str(item) for item in value if item is not None and str(item)]

    return [str(value)]


def _as_text(value: Any, default: str) -> str:
    if value is None:
        return default

    text = str(value)
    return text if text else default


def _optional_text(value: Any) -> Optional[str]:
    if value is None:
        return None

    text = str(value)
    return text if text else None
