"""Servico de relatorio final auditavel da Fase 7R.7.

Este modulo gera uma estrutura de relatorio diagnostica, auditavel,
deterministica e somente leitura a partir da trilha consolidada da Fase 7R.6.

Nao executa ordens.
Nao acessa Excel real.
Nao conecta broker.
Nao chama APIs externas.
Nao persiste dados.
"""

from copy import deepcopy


ALLOWED_SOURCE_STATUSES = {
    "consolidado",
    "consolidado_com_alertas",
    "nao_consolidado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

ALLOWED_REPORT_STATUSES = {
    "gerado",
    "gerado_com_alertas",
    "nao_gerado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

REQUIRED_SECTIONS = (
    "identificacao",
    "origem_da_trilha",
    "resumo_executivo_diagnostico",
    "status_consolidado",
    "componentes_da_cadeia",
    "validacao_cruzada",
    "explicacao_operacional",
    "decisao_simulada",
    "alerta_simulado",
    "inconsistencias",
    "warnings",
    "limitacoes",
    "checks_executados",
    "guardrails",
    "conclusao_auditavel",
)

REQUIRED_LIMITATIONS = (
    "dados simulados",
    "ausencia de Excel real",
    "ausencia de banco real",
    "ausencia de execucao operacional",
    "ausencia de broker",
    "ausencia de validacao em tempo real",
    "uso apenas diagnostico e auditavel",
    "relatorio somente leitura",
    "dependencia da qualidade da trilha consolidada",
    "ausencia de recomendacao executavel",
    "ausencia de envio automatico para sistemas externos",
)

READ_ONLY_VALUES = {
    "somente_leitura",
    "somente leitura",
    "read_only",
    "readonly",
}

BLOCKED_GUARDRAIL_VALUES = {
    "violado",
    "bloqueado",
    "bloqueado_por_guardrail",
    "blocked",
    "guardrail_violado",
}

SUSPICIOUS_FIELD_FRAGMENTS = (
    "action",
    "acao",
    "command",
    "comando",
    "order",
    "ordem",
    "execution",
    "execucao",
    "broker",
    "automation",
    "automacao",
    "trigger",
    "routing",
    "roteamento",
    "api",
    "external",
    "externo",
)

SAFE_CONTEXT_FRAGMENTS = (
    "limitation",
    "limitations",
    "limitacao",
    "limitacoes",
    "warning",
    "warnings",
    "audit_note",
    "nota",
    "disclaimer",
    "status",
    "summary",
    "resumo",
    "conclusion",
    "conclusao",
)

EXECUTABLE_TERMS = (
    "executar",
    "execucao real",
    "enviar ordem",
    "ordem de compra",
    "ordem de venda",
    "comprar",
    "vender",
    "acionar broker",
    "broker",
    "automatizar",
    "trigger operacional",
    "rotear ordem",
    "api externa",
    "sistema externo",
)

NEGATING_TERMS = (
    "nao",
    "não",
    "sem",
    "ausencia",
    "ausência",
    "somente leitura",
    "somente_leitura",
    "diagnostico",
    "diagnóstico",
    "simulado",
    "simulada",
    "nao executavel",
    "não executável",
)


def generate_final_audit_report(consolidated_trail, metadata=None):
    """Gera relatorio final auditavel a partir da trilha consolidada.

    Args:
        consolidated_trail: dicionario da consolidacao 7R.6.
        metadata: dicionario opcional com dados simbolicos de auditoria.

    Returns:
        dict: relatorio final auditavel somente leitura.
    """
    metadata = metadata if isinstance(metadata, dict) else {}

    inconsistencies = []
    warnings = []
    checks_performed = [
        "validacao_entrada",
        "validacao_guardrails",
        "validacao_status_origem",
        "validacao_rastreabilidade",
        "propagacao_inconsistencias",
        "propagacao_warnings",
        "propagacao_limitacoes",
        "geracao_secoes_obrigatorias",
        "declaracao_modo_somente_leitura",
    ]

    if not isinstance(consolidated_trail, dict):
        if consolidated_trail is None:
            inconsistencies.append("trilha consolidada ausente")
        else:
            inconsistencies.append("trilha consolidada invalida")

        report_id = metadata.get("report_id") or "report_sem_trilha_consolidada"

        return _build_report(
            report_status="nao_gerado",
            is_report_generated=False,
            report_id=report_id,
            event_id=None,
            alert_type=None,
            source_consolidated_status=None,
            source_chain_consistency_status=None,
            consolidated_trail={},
            inconsistencies=inconsistencies,
            warnings=warnings,
            limitations=list(REQUIRED_LIMITATIONS),
            checks_performed=checks_performed,
            guardrail_status="preservado",
            final_audit_conclusion="Relatorio nao gerado por ausencia ou invalidade da trilha consolidada.",
        )

    source = deepcopy(consolidated_trail)

    source_inconsistencies = _as_list(source.get("inconsistencies"))
    source_warnings = _as_list(source.get("warnings"))
    source_limitations = _as_list(source.get("limitations"))
    source_checks = _as_list(source.get("checks_performed"))

    inconsistencies.extend(source_inconsistencies)
    warnings.extend(source_warnings)

    if not source_limitations:
        inconsistencies.append("limitacoes ausentes na trilha consolidada")

    if not source_checks:
        inconsistencies.append("checks executados ausentes na trilha consolidada")

    checks_performed = _unique_list(checks_performed + source_checks)

    event_id = source.get("event_id")
    alert_type = source.get("alert_type")
    source_status = source.get("consolidated_status")
    source_chain_status = source.get("chain_consistency_status")
    source_operational_status = source.get("operational_status")
    source_guardrail_status = source.get("guardrail_status")

    if not event_id:
        inconsistencies.append("event_id ausente")

    if not alert_type:
        inconsistencies.append("alert_type ausente")

    if not source_status:
        inconsistencies.append("status consolidado ausente")
    elif source_status not in ALLOWED_SOURCE_STATUSES:
        inconsistencies.append("status consolidado nao permitido")

    if not source_operational_status:
        inconsistencies.append("operational_status ausente")
    elif _normalize(source_operational_status) not in READ_ONLY_VALUES:
        inconsistencies.append("operational_status diferente de somente leitura")

    if not source_guardrail_status:
        inconsistencies.append("guardrail_status ausente")

    report_id = metadata.get("report_id")
    if not report_id:
        report_id = _make_report_id(event_id, alert_type)
        warnings.append("report_id gerado automaticamente")

    if not metadata.get("timestamp") and not metadata.get("marcador_temporal"):
        warnings.append("marcador temporal simbolico ausente")

    if not metadata.get("reviewer") and not metadata.get("responsavel"):
        warnings.append("responsavel simbolico pela revisao ausente")

    guardrail_violations = _detect_guardrail_violations(source)
    guardrail_violations.extend(_detect_guardrail_violations(metadata))

    if source_status == "bloqueado_por_guardrail":
        guardrail_violations.append("trilha de origem bloqueada por guardrail")

    if _normalize(source_guardrail_status) in BLOCKED_GUARDRAIL_VALUES:
        guardrail_violations.append("guardrail_status de origem indica bloqueio")

    if _normalize(source_operational_status) not in READ_ONLY_VALUES:
        guardrail_violations.append("status operacional de origem nao e somente leitura")

    if guardrail_violations:
        inconsistencies.extend(_unique_list(guardrail_violations))
        report_status = "bloqueado_por_guardrail"
        is_report_generated = False
        guardrail_status = "bloqueado_por_guardrail"
        conclusion = "Relatorio bloqueado por guardrail operacional. Nenhuma execucao real autorizada."
    elif source_status not in ALLOWED_SOURCE_STATUSES:
        report_status = "nao_gerado"
        is_report_generated = False
        guardrail_status = "preservado"
        conclusion = "Relatorio nao gerado por status consolidado de origem nao permitido."
    elif source_status == "inconclusivo":
        report_status = "inconclusivo"
        is_report_generated = False
        guardrail_status = "preservado"
        conclusion = "Relatorio inconclusivo por trilha consolidada inconclusiva."
    elif source_status == "nao_consolidado":
        report_status = "gerado_com_alertas"
        is_report_generated = True
        guardrail_status = "preservado"
        conclusion = "Relatorio gerado com alertas para trilha nao consolidada."
    elif source_status == "consolidado_com_alertas" or inconsistencies or warnings:
        report_status = "gerado_com_alertas"
        is_report_generated = True
        guardrail_status = "preservado"
        conclusion = "Relatorio final auditavel gerado com alertas preservados."
    else:
        report_status = "gerado"
        is_report_generated = True
        guardrail_status = "preservado"
        conclusion = "Relatorio final auditavel gerado em modo diagnostico e somente leitura."

    limitations = _unique_list(source_limitations + list(REQUIRED_LIMITATIONS))

    return _build_report(
        report_status=report_status,
        is_report_generated=is_report_generated,
        report_id=report_id,
        event_id=event_id,
        alert_type=alert_type,
        source_consolidated_status=source_status,
        source_chain_consistency_status=source_chain_status,
        consolidated_trail=source,
        inconsistencies=_unique_list(inconsistencies),
        warnings=_unique_list(warnings),
        limitations=limitations,
        checks_performed=checks_performed,
        guardrail_status=guardrail_status,
        final_audit_conclusion=conclusion,
    )


def _build_report(
    report_status,
    is_report_generated,
    report_id,
    event_id,
    alert_type,
    source_consolidated_status,
    source_chain_consistency_status,
    consolidated_trail,
    inconsistencies,
    warnings,
    limitations,
    checks_performed,
    guardrail_status,
    final_audit_conclusion,
):
    report = {
        "report_status": report_status,
        "is_report_generated": is_report_generated,
        "report_id": report_id,
        "event_id": event_id,
        "alert_type": alert_type,
        "source_consolidated_status": source_consolidated_status,
        "source_chain_consistency_status": source_chain_consistency_status,
        "executive_summary": _make_executive_summary(
            report_status,
            event_id,
            alert_type,
            source_consolidated_status,
        ),
        "audit_sections": {},
        "inconsistencies": _unique_list(inconsistencies),
        "warnings": _unique_list(warnings),
        "limitations": _unique_list(limitations),
        "checks_performed": _unique_list(checks_performed),
        "guardrail_status": guardrail_status,
        "operational_status": "somente_leitura",
        "final_audit_conclusion": final_audit_conclusion,
        "audit_note": (
            "Relatorio diagnostico, auditavel, somente leitura e sem autorizacao "
            "para execucao operacional real."
        ),
    }

    report["audit_sections"] = _make_sections(report, consolidated_trail)

    missing_sections = [
        section for section in REQUIRED_SECTIONS
        if section not in report["audit_sections"]
    ]
    if missing_sections:
        report["inconsistencies"].append(
            "secoes obrigatorias ausentes: " + ", ".join(missing_sections)
        )
        report["inconsistencies"] = _unique_list(report["inconsistencies"])

    if report_status not in ALLOWED_REPORT_STATUSES:
        report["inconsistencies"].append("status do relatorio nao permitido")
        report["report_status"] = "nao_gerado"
        report["is_report_generated"] = False

    return report


def _make_sections(report, consolidated_trail):
    source = consolidated_trail if isinstance(consolidated_trail, dict) else {}

    return {
        "identificacao": {
            "report_id": report["report_id"],
            "event_id": report["event_id"],
            "alert_type": report["alert_type"],
        },
        "origem_da_trilha": {
            "source_consolidated_status": report["source_consolidated_status"],
            "source_chain_consistency_status": report["source_chain_consistency_status"],
        },
        "resumo_executivo_diagnostico": {
            "executive_summary": report["executive_summary"],
        },
        "status_consolidado": {
            "consolidated_status": source.get("consolidated_status"),
            "is_consolidated": source.get("is_consolidated"),
        },
        "componentes_da_cadeia": {
            "chain_components": source.get("chain_components", {}),
        },
        "validacao_cruzada": {
            "validation_status": source.get("validation_status"),
        },
        "explicacao_operacional": {
            "explanation_status": source.get("explanation_status"),
        },
        "decisao_simulada": {
            "decision_status": source.get("decision_status"),
        },
        "alerta_simulado": {
            "alert_status": source.get("alert_status"),
        },
        "inconsistencias": {
            "items": report["inconsistencies"],
        },
        "warnings": {
            "items": report["warnings"],
        },
        "limitacoes": {
            "items": report["limitations"],
        },
        "checks_executados": {
            "items": report["checks_performed"],
        },
        "guardrails": {
            "guardrail_status": report["guardrail_status"],
            "operational_status": report["operational_status"],
        },
        "conclusao_auditavel": {
            "final_audit_conclusion": report["final_audit_conclusion"],
            "audit_note": report["audit_note"],
        },
    }


def _make_report_id(event_id, alert_type):
    safe_event = str(event_id or "sem_evento").strip().replace(" ", "_")
    safe_alert = str(alert_type or "sem_alerta").strip().replace(" ", "_")
    return "report_" + safe_event + "_" + safe_alert


def _make_executive_summary(report_status, event_id, alert_type, source_status):
    return (
        "Relatorio final auditavel com status "
        + str(report_status)
        + " para evento "
        + str(event_id)
        + " e alerta "
        + str(alert_type)
        + ". Status consolidado de origem: "
        + str(source_status)
        + ". Saida somente leitura e nao executavel."
    )


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return deepcopy(value)
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _unique_list(values):
    result = []
    seen = set()

    for value in values:
        key = repr(value)
        if key not in seen:
            seen.add(key)
            result.append(value)

    return result


def _normalize(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def _detect_guardrail_violations(payload):
    violations = []
    _scan_for_guardrail_violations(payload, path="", violations=violations)
    return _unique_list(violations)


def _scan_for_guardrail_violations(value, path, violations):
    if isinstance(value, dict):
        for key, inner_value in value.items():
            key_text = str(key).lower()
            next_path = key_text if not path else path + "." + key_text

            if _is_safe_context(key_text):
                continue

            if _is_suspicious_field(key_text):
                joined = key_text + " " + _stringify(inner_value)
                if _contains_executable_intent(joined):
                    violations.append(
                        "tentativa de converter relatorio em execucao operacional em " + next_path
                    )

            _scan_for_guardrail_violations(inner_value, next_path, violations)

    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_for_guardrail_violations(item, path + "[" + str(index) + "]", violations)


def _is_safe_context(key_text):
    return any(fragment in key_text for fragment in SAFE_CONTEXT_FRAGMENTS)


def _is_suspicious_field(key_text):
    return any(fragment in key_text for fragment in SUSPICIOUS_FIELD_FRAGMENTS)


def _contains_executable_intent(text):
    normalized = _normalize(text)

    if any(term in normalized for term in NEGATING_TERMS):
        return False

    return any(term in normalized for term in EXECUTABLE_TERMS)


def _stringify(value):
    if isinstance(value, dict):
        return " ".join(str(item) for pair in value.items() for item in pair)
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


__all__ = ["generate_final_audit_report"]
