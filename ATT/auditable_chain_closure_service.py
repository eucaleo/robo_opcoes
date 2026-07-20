from __future__ import annotations

from typing import Any, Dict, List, Optional


ALLOWED_REPORT_STATUSES = {
    "gerado",
    "gerado_com_alertas",
    "nao_gerado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

CLOSURE_STATUSES = {
    "encerrado",
    "encerrado_com_alertas",
    "nao_encerrado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

FINAL_OPERATIONAL_STATUS = "SEM AUTORIZACAO PARA EXECUCAO REAL"
FINAL_GUARDRAIL_STATUS = "PRESERVADO"
BLOCKED_GUARDRAIL_STATUS = "BLOQUEADO"

REQUIRED_REPORT_FIELDS = (
    "report_id",
    "event_id",
    "alert_type",
    "report_status",
    "operational_status",
    "guardrail_status",
)

REQUIRED_CLOSURE_SECTIONS = (
    "identificacao",
    "origem_do_relatorio",
    "resumo_do_encerramento",
    "componentes_da_cadeia",
    "status_do_relatorio_final",
    "rastreabilidade",
    "inconsistencias",
    "warnings",
    "limitacoes",
    "checks_executados",
    "guardrails",
    "conclusao_final_auditavel",
)

DEFAULT_LIMITATIONS = (
    "dados simulados",
    "estruturas controladas",
    "ausencia de Excel real",
    "ausencia de banco real",
    "ausencia de broker real",
    "ausencia de execucao operacional",
    "ausencia de chamada externa",
    "ausencia de envio automatico",
    "ausencia de validacao em tempo real",
    "uso apenas diagnostico e auditavel",
    "encerramento somente leitura",
    "dependencia da qualidade do relatorio final auditavel",
    "dependencia da qualidade da trilha consolidada anterior",
    "ausencia de recomendacao executavel",
)

CLOSURE_CHECKS = (
    "validacao de presenca do relatorio final auditavel",
    "validacao de tipo do relatorio final auditavel",
    "validacao de report_id",
    "validacao de event_id",
    "validacao de alert_type",
    "validacao de report_status",
    "validacao de operational_status",
    "validacao de guardrail_status",
    "validacao de propagacao de inconsistencias",
    "validacao de propagacao de warnings",
    "validacao de propagacao de limitacoes",
    "validacao de checks anteriores",
    "validacao de secoes obrigatorias",
    "validacao de ausencia de execucao operacional",
    "validacao de ausencia de integracoes reais",
)

ACTION_CONTEXT_KEYS = {
    "acao",
    "action",
    "comando",
    "command",
    "ordem",
    "order",
    "execucao",
    "execution",
    "executar",
    "execute",
    "broker",
    "automacao",
    "automation",
    "trigger",
    "api",
    "contexto_externo",
    "external_context",
    "roteamento",
    "routing",
}

BLOCKED_VALUE_TERMS = (
    "enviar",
    "executar",
    "acionar",
    "ordem",
    "order",
    "broker",
    "comprar",
    "vender",
    "buy",
    "sell",
    "api",
    "extern",
    "automacao",
    "automation",
    "trigger",
    "rotear",
    "routing",
)


def close_auditable_chain(
    final_audit_report: Optional[Dict[str, Any]],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    metadata = metadata if isinstance(metadata, dict) else {}

    checks = list(CLOSURE_CHECKS)

    if not isinstance(final_audit_report, dict):
        return _build_closure(
            closure_status="nao_encerrado",
            is_chain_closed=False,
            report={},
            metadata=metadata,
            inconsistencies=["relatorio final auditavel ausente ou invalido"],
            warnings=[],
            limitations=list(DEFAULT_LIMITATIONS),
            checks=checks,
            guardrail_status=FINAL_GUARDRAIL_STATUS,
            conclusion="Cadeia auditavel nao encerrada por ausencia ou invalidade do relatorio final auditavel.",
        )

    source_inconsistencies = _as_list(final_audit_report.get("inconsistencies"))
    source_warnings = _as_list(final_audit_report.get("warnings"))
    source_limitations = _merge_unique(
        _as_list(final_audit_report.get("limitations")),
        list(DEFAULT_LIMITATIONS),
    )
    source_checks = _as_list(final_audit_report.get("checks_performed"))
    checks = _merge_unique(source_checks, checks)

    guardrail_violations = _detect_guardrail_violations(final_audit_report, metadata)
    if guardrail_violations:
        return _build_closure(
            closure_status="bloqueado_por_guardrail",
            is_chain_closed=False,
            report=final_audit_report,
            metadata=metadata,
            inconsistencies=_merge_unique(source_inconsistencies, guardrail_violations),
            warnings=source_warnings,
            limitations=source_limitations,
            checks=checks,
            guardrail_status=BLOCKED_GUARDRAIL_STATUS,
            conclusion="Encerramento bloqueado por preservacao de guardrails operacionais.",
        )

    missing_fields = [
        field for field in REQUIRED_REPORT_FIELDS
        if _is_blank(final_audit_report.get(field))
    ]

    report_status = final_audit_report.get("report_status")
    if report_status not in ALLOWED_REPORT_STATUSES:
        return _build_closure(
            closure_status="nao_encerrado",
            is_chain_closed=False,
            report=final_audit_report,
            metadata=metadata,
            inconsistencies=_merge_unique(
                source_inconsistencies,
                [f"report_status nao permitido: {report_status}"],
            ),
            warnings=source_warnings,
            limitations=source_limitations,
            checks=checks,
            guardrail_status=FINAL_GUARDRAIL_STATUS,
            conclusion="Cadeia auditavel nao encerrada por status de relatorio nao permitido.",
        )

    if missing_fields:
        return _build_closure(
            closure_status="nao_encerrado",
            is_chain_closed=False,
            report=final_audit_report,
            metadata=metadata,
            inconsistencies=_merge_unique(
                source_inconsistencies,
                [f"campo obrigatorio ausente: {field}" for field in missing_fields],
            ),
            warnings=source_warnings,
            limitations=source_limitations,
            checks=checks,
            guardrail_status=FINAL_GUARDRAIL_STATUS,
            conclusion="Cadeia auditavel nao encerrada por ausencia de dados obrigatorios.",
        )

    if report_status == "bloqueado_por_guardrail":
        return _build_closure(
            closure_status="bloqueado_por_guardrail",
            is_chain_closed=False,
            report=final_audit_report,
            metadata=metadata,
            inconsistencies=source_inconsistencies,
            warnings=source_warnings,
            limitations=source_limitations,
            checks=checks,
            guardrail_status=BLOCKED_GUARDRAIL_STATUS,
            conclusion="Encerramento bloqueado por status de guardrail herdado do relatorio final auditavel.",
        )

    if report_status == "nao_gerado":
        return _build_closure(
            closure_status="nao_encerrado",
            is_chain_closed=False,
            report=final_audit_report,
            metadata=metadata,
            inconsistencies=source_inconsistencies,
            warnings=source_warnings,
            limitations=source_limitations,
            checks=checks,
            guardrail_status=FINAL_GUARDRAIL_STATUS,
            conclusion="Cadeia auditavel nao encerrada porque o relatorio final auditavel nao foi gerado.",
        )

    if report_status == "inconclusivo" or _is_inconclusive_source(final_audit_report):
        return _build_closure(
            closure_status="inconclusivo",
            is_chain_closed=False,
            report=final_audit_report,
            metadata=metadata,
            inconsistencies=source_inconsistencies,
            warnings=source_warnings,
            limitations=source_limitations,
            checks=checks,
            guardrail_status=FINAL_GUARDRAIL_STATUS,
            conclusion="Encerramento inconclusivo por informacao insuficiente ou status de origem inconclusivo.",
        )

    has_alerts = bool(source_inconsistencies or source_warnings or _has_relevant_limitations(final_audit_report))

    closure_status = "encerrado_com_alertas" if has_alerts else "encerrado"
    conclusion = (
        "Cadeia auditavel encerrada com alertas preservados para revisao humana."
        if has_alerts
        else "Cadeia auditavel encerrada formalmente em modo diagnostico, auditavel e somente leitura."
    )

    return _build_closure(
        closure_status=closure_status,
        is_chain_closed=True,
        report=final_audit_report,
        metadata=metadata,
        inconsistencies=source_inconsistencies,
        warnings=source_warnings,
        limitations=source_limitations,
        checks=checks,
        guardrail_status=FINAL_GUARDRAIL_STATUS,
        conclusion=conclusion,
    )


def _build_closure(
    closure_status: str,
    is_chain_closed: bool,
    report: Dict[str, Any],
    metadata: Dict[str, Any],
    inconsistencies: List[Any],
    warnings: List[Any],
    limitations: List[Any],
    checks: List[Any],
    guardrail_status: str,
    conclusion: str,
) -> Dict[str, Any]:
    report_id = report.get("report_id")
    event_id = report.get("event_id")
    alert_type = report.get("alert_type")
    closure_id = metadata.get("closure_id") or _make_closure_id(report_id, event_id)

    source_report_status = report.get("report_status")
    source_operational_status = report.get("operational_status")
    source_guardrail_status = report.get("guardrail_status")
    source_chain_consistency_status = report.get("source_chain_consistency_status")

    chain_components = _build_chain_components(report)

    closure_sections = {
        "identificacao": {
            "closure_id": closure_id,
            "report_id": report_id,
            "event_id": event_id,
            "alert_type": alert_type,
        },
        "origem_do_relatorio": {
            "source_report_status": source_report_status,
            "source_operational_status": source_operational_status,
            "source_guardrail_status": source_guardrail_status,
            "source_chain_consistency_status": source_chain_consistency_status,
        },
        "resumo_do_encerramento": {
            "closure_status": closure_status,
            "is_chain_closed": is_chain_closed,
            "summary": conclusion,
        },
        "componentes_da_cadeia": chain_components,
        "status_do_relatorio_final": {
            "report_status": source_report_status,
        },
        "rastreabilidade": {
            "closure_id": closure_id,
            "report_id": report_id,
            "event_id": event_id,
            "alert_type": alert_type,
        },
        "inconsistencias": list(inconsistencies),
        "warnings": list(warnings),
        "limitacoes": list(limitations),
        "checks_executados": list(checks),
        "guardrails": {
            "guardrail_status": guardrail_status,
            "modo": "somente leitura",
            "execucao_real": "nao autorizada",
        },
        "conclusao_final_auditavel": {
            "final_chain_conclusion": conclusion,
        },
    }

    return {
        "closure_status": closure_status,
        "is_chain_closed": is_chain_closed,
        "closure_id": closure_id,
        "report_id": report_id,
        "event_id": event_id,
        "alert_type": alert_type,
        "source_report_status": source_report_status,
        "source_operational_status": source_operational_status,
        "source_guardrail_status": source_guardrail_status,
        "source_chain_consistency_status": source_chain_consistency_status,
        "closure_summary": conclusion,
        "chain_components": chain_components,
        "closure_sections": closure_sections,
        "inconsistencies": list(inconsistencies),
        "warnings": list(warnings),
        "limitations": list(limitations),
        "checks_performed": list(checks),
        "guardrail_status": guardrail_status,
        "operational_status": FINAL_OPERATIONAL_STATUS,
        "final_chain_conclusion": conclusion,
        "audit_note": (
            "Encerramento auditavel gerado apenas em memoria, sem autorizacao "
            "para execucao real, sem integracoes reais e sem recomendacao executavel."
        ),
    }


def _build_chain_components(report: Dict[str, Any]) -> Dict[str, Any]:
    audit_sections = report.get("audit_sections")
    if isinstance(audit_sections, dict):
        return {
            "alerta_simulado": "alerta_simulado" in audit_sections,
            "decisao_simulada": "decisao_simulada" in audit_sections,
            "explicacao_operacional": "explicacao_operacional" in audit_sections,
            "validacao_cruzada": "validacao_cruzada" in audit_sections,
            "trilha_consolidada": "origem_da_trilha" in audit_sections or "status_consolidado" in audit_sections,
            "relatorio_final_auditavel": True,
        }

    return {
        "alerta_simulado": None,
        "decisao_simulada": None,
        "explicacao_operacional": None,
        "validacao_cruzada": None,
        "trilha_consolidada": None,
        "relatorio_final_auditavel": bool(report),
    }


def _detect_guardrail_violations(report: Dict[str, Any], metadata: Dict[str, Any]) -> List[str]:
    violations: List[str] = []

    guardrail_status = str(report.get("guardrail_status", "")).lower()
    if guardrail_status in {"violado", "bloqueado", "bloqueado_por_guardrail"}:
        violations.append("guardrail_status de origem indica violacao ou bloqueio")

    if _has_operational_action_context(report):
        violations.append("relatorio contem contexto de acao operacional real")

    if _has_operational_action_context(metadata):
        violations.append("metadados contem contexto de acao operacional real")

    return violations


def _has_operational_action_context(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized_key = str(key).strip().lower()
            if normalized_key in ACTION_CONTEXT_KEYS and _is_blocked_action_value(item):
                return True
            if _has_operational_action_context(item):
                return True

    if isinstance(value, list):
        return any(_has_operational_action_context(item) for item in value)

    return False


def _is_blocked_action_value(value: Any) -> bool:
    if value is None or value is False:
        return False

    if value is True:
        return True

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, dict) or isinstance(value, list):
        return _has_operational_action_context(value)

    text = str(value).strip().lower()
    if not text:
        return False

    safe_markers = (
        "nao autorizado",
        "sem autorizacao",
        "ausencia",
        "somente leitura",
        "nao executavel",
        "sem execucao",
    )
    if any(marker in text for marker in safe_markers):
        return False

    return any(term in text for term in BLOCKED_VALUE_TERMS)


def _is_inconclusive_source(report: Dict[str, Any]) -> bool:
    chain_status = str(report.get("source_chain_consistency_status", "")).lower()
    if chain_status == "inconclusivo":
        return True

    operational_status = str(report.get("operational_status", "")).lower()
    if not operational_status:
        return True

    return False


def _has_relevant_limitations(report: Dict[str, Any]) -> bool:
    original_limitations = _as_list(report.get("limitations"))
    return bool(original_limitations)


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _merge_unique(*items: List[Any]) -> List[Any]:
    merged: List[Any] = []
    seen = set()

    for group in items:
        for item in group:
            marker = repr(item)
            if marker not in seen:
                seen.add(marker)
                merged.append(item)

    return merged


def _is_blank(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _make_closure_id(report_id: Any, event_id: Any) -> str:
    if report_id:
        return f"closure-{report_id}"
    if event_id:
        return f"closure-event-{event_id}"
    return "closure-unidentified"
