"""
Servico de sumario executivo final da cadeia auditavel - Fase 7R.9.

Modulo deterministico, em memoria, somente leitura e nao executavel.
Nao realiza integracoes reais, nao envia ordens e nao produz recomendacao executavel.
"""

ALLOWED_CLOSURE_STATUSES = {
    "encerrado",
    "encerrado_com_alertas",
    "nao_encerrado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

ALLOWED_SUMMARY_STATUSES = {
    "gerado",
    "gerado_com_alertas",
    "nao_gerado",
    "bloqueado_por_guardrail",
    "inconclusivo",
}

REQUIRED_CLOSURE_FIELDS = [
    "closure_id",
    "report_id",
    "event_id",
    "alert_type",
    "closure_status",
    "is_chain_closed",
    "operational_status",
    "guardrail_status",
    "chain_components",
    "closure_sections",
    "inconsistencies",
    "warnings",
    "limitations",
    "checks_performed",
    "final_chain_conclusion",
    "audit_note",
]

MANDATORY_SUMMARY_SECTIONS = [
    "identificacao",
    "origem_do_encerramento",
    "resumo_executivo_final",
    "panorama_da_cadeia",
    "componentes_da_cadeia",
    "status_do_encerramento",
    "rastreabilidade_final",
    "inconsistencias_herdadas",
    "warnings_herdados",
    "limitacoes_herdadas",
    "checks_herdados",
    "riscos_residuais",
    "guardrails",
    "conclusao_executiva_final",
]

MANDATORY_FINAL_LIMITATIONS = [
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
    "sumario somente leitura",
    "dependencia da qualidade do encerramento auditavel",
    "dependencia da qualidade do relatorio final auditavel",
    "dependencia da qualidade da trilha consolidada anterior",
    "ausencia de recomendacao executavel",
    "ausencia de decisao executavel",
    "ausencia de garantia operacional real",
]

MANDATORY_FINAL_RISKS = [
    "dependencia da qualidade do encerramento auditavel de origem",
    "dependencia da qualidade do relatorio final auditavel anterior",
    "dependencia da qualidade da trilha consolidada anterior",
    "entradas malformadas podem gerar sumario nao gerado ou inconclusivo",
    "warnings herdados nao representam emergencia operacional real",
    "inconsistencias herdadas devem continuar sendo revisadas por humano",
    "ausencia de dados obrigatorios reduz a completude auditavel",
    "saida permanece diagnostica e nao executavel",
    "validacao nao substitui auditoria humana",
    "sumario executivo nao representa recomendacao financeira personalizada",
    "sumario executivo nao representa autorizacao operacional",
]

SUMMARY_CHECKS = [
    "validacao de presenca do encerramento auditavel",
    "validacao de tipo do encerramento auditavel",
    "validacao de closure_id",
    "validacao de report_id",
    "validacao de event_id",
    "validacao de alert_type",
    "validacao de closure_status",
    "validacao de is_chain_closed",
    "validacao de operational_status",
    "validacao de guardrail_status",
    "validacao de chain_components",
    "validacao de closure_sections",
    "validacao de propagacao de inconsistencias",
    "validacao de propagacao de warnings",
    "validacao de propagacao de limitacoes",
    "validacao de checks anteriores",
    "validacao de riscos residuais",
    "validacao de secoes obrigatorias",
    "validacao de ausencia de execucao operacional",
    "validacao de ausencia de integracoes reais",
]

OPERATIONAL_CONTEXT_KEYS = (
    "acao",
    "action",
    "comando",
    "command",
    "ordem",
    "order",
    "broker",
    "api",
    "trigger",
    "automacao",
    "automation",
    "execucao",
    "execution",
    "executar",
    "execute",
    "roteamento",
    "routing",
    "contexto_externo",
    "external_context",
    "envio",
    "send",
)

EXPLICIT_OPERATIONAL_PHRASES = (
    "executar ordem",
    "execute order",
    "enviar ordem",
    "send order",
    "ordem real",
    "real order",
    "ordem operacional",
    "operational order",
    "conectar broker",
    "connect broker",
    "acionar broker",
    "broker real",
    "chamar api externa",
    "external api",
    "disparar trigger",
    "trigger operacional",
    "executar automacao",
    "run automation",
    "roteamento operacional",
    "comprar ativo",
    "vender ativo",
    "buy asset",
    "sell asset",
)

DISCLAIMER_MARKERS = (
    "ausencia de",
    "sem ",
    "nao ",
    "not ",
    "never ",
    "somente leitura",
    "nao executavel",
    "sem autorizacao",
)


def build_final_executive_summary(auditable_closure, metadata=None):
    """
    Gera sumario executivo final da cadeia auditavel a partir do encerramento 7R.8.

    A funcao retorna apenas estrutura em memoria.
    """
    metadata = metadata if isinstance(metadata, dict) else {}

    base = _extract_base(auditable_closure)
    inherited_inconsistencies = _as_list(base.get("inconsistencies"))
    inherited_warnings = _as_list(base.get("warnings"))
    inherited_limitations = _as_list(base.get("limitations"))
    inherited_checks = _as_list(base.get("checks_performed"))

    validation_errors = _validate_closure(auditable_closure)
    operational_violation = _has_operational_violation(auditable_closure) or _has_operational_violation(metadata)
    source_guardrail_status = base.get("guardrail_status")
    source_closure_status = base.get("closure_status")

    if _guardrail_is_blocked(source_guardrail_status) or source_closure_status == "bloqueado_por_guardrail":
        operational_violation = True

    if not isinstance(auditable_closure, dict):
        summary_status = "nao_gerado"
    elif operational_violation:
        summary_status = "bloqueado_por_guardrail"
    elif validation_errors:
        summary_status = "nao_gerado"
    elif source_closure_status not in ALLOWED_CLOSURE_STATUSES:
        summary_status = "nao_gerado"
    elif source_closure_status == "inconclusivo":
        summary_status = "inconclusivo"
    elif source_closure_status == "nao_encerrado":
        summary_status = "inconclusivo"
    elif base.get("is_chain_closed") is not True:
        summary_status = "inconclusivo"
    elif source_closure_status == "encerrado_com_alertas":
        summary_status = "gerado_com_alertas"
    elif inherited_inconsistencies or inherited_warnings or inherited_limitations:
        summary_status = "gerado_com_alertas"
    else:
        summary_status = "gerado"

    summary_id = _resolve_summary_id(base, metadata, summary_status)
    final_limitations = _merge_unique(inherited_limitations, MANDATORY_FINAL_LIMITATIONS)
    final_risks = list(MANDATORY_FINAL_RISKS)
    all_checks = _merge_unique(inherited_checks, SUMMARY_CHECKS)

    summary = {
        "summary_status": summary_status,
        "is_summary_generated": summary_status in {"gerado", "gerado_com_alertas"},
        "summary_id": summary_id,
        "closure_id": base.get("closure_id"),
        "report_id": base.get("report_id"),
        "event_id": base.get("event_id"),
        "alert_type": base.get("alert_type"),
        "source_closure_status": source_closure_status,
        "source_is_chain_closed": base.get("is_chain_closed"),
        "source_operational_status": base.get("operational_status"),
        "source_guardrail_status": source_guardrail_status,
        "source_chain_consistency_status": base.get("source_chain_consistency_status"),
        "executive_summary": _build_executive_summary_text(summary_status, base, validation_errors),
        "chain_overview": _build_chain_overview(base),
        "chain_components": _as_list(base.get("chain_components")),
        "summary_sections": {},
        "inherited_inconsistencies": inherited_inconsistencies,
        "inherited_warnings": inherited_warnings,
        "inherited_limitations": inherited_limitations,
        "inherited_checks": inherited_checks,
        "checks_performed": all_checks,
        "final_limitations": final_limitations,
        "final_risks": final_risks,
        "guardrail_status": "violado" if operational_violation else "preservado",
        "operational_status": "somente_leitura_sem_execucao_real",
        "final_executive_conclusion": _build_final_conclusion(summary_status),
        "audit_note": (
            "Sumario executivo final diagnostico, auditavel, somente leitura e sem "
            "autorizacao para execucao operacional real."
        ),
        "validation_errors": validation_errors,
    }

    summary["summary_sections"] = _build_sections(summary)
    return summary


def _extract_base(value):
    if isinstance(value, dict):
        return value
    return {}


def _validate_closure(value):
    errors = []
    if value is None:
        return ["encerramento auditavel ausente"]
    if not isinstance(value, dict):
        return ["encerramento auditavel invalido"]

    for field in REQUIRED_CLOSURE_FIELDS:
        if field not in value:
            errors.append(f"campo obrigatorio ausente: {field}")

    identity_fields = [
        "closure_id",
        "report_id",
        "event_id",
        "alert_type",
        "closure_status",
        "operational_status",
        "guardrail_status",
        "final_chain_conclusion",
        "audit_note",
    ]
    for field in identity_fields:
        if field in value and value.get(field) in (None, ""):
            errors.append(f"campo obrigatorio vazio: {field}")

    if "closure_status" in value and value.get("closure_status") not in ALLOWED_CLOSURE_STATUSES:
        errors.append("closure_status nao permitido")

    if "is_chain_closed" in value and not isinstance(value.get("is_chain_closed"), bool):
        errors.append("is_chain_closed invalido")

    list_fields = ["chain_components", "inconsistencies", "warnings", "limitations", "checks_performed"]
    for field in list_fields:
        if field in value and not isinstance(value.get(field), list):
            errors.append(f"{field} deve ser lista")

    if "closure_sections" in value and not isinstance(value.get("closure_sections"), dict):
        errors.append("closure_sections deve ser dicionario")

    return errors


def _guardrail_is_blocked(status):
    normalized = _normalize(status)
    blocked_statuses = {
        "violado",
        "bloqueado",
        "bloqueado_por_guardrail",
        "guardrail_violado",
        "falha_guardrail",
    }
    return normalized in blocked_statuses


def _has_operational_violation(value, current_key=""):
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = _normalize(key)
            if _is_operational_context_key(key_text) and _context_value_is_violation(key_text, item):
                return True
            if _has_operational_violation(item, key_text):
                return True
        return False

    if isinstance(value, (list, tuple, set)):
        return any(_has_operational_violation(item, current_key) for item in value)

    if isinstance(value, str):
        if _looks_like_disclaimer(value):
            return False
        if _is_operational_context_key(current_key):
            return _is_explicit_operational_command(value)
        return _is_explicit_operational_command(value)

    return False


def _is_operational_context_key(key_text):
    return any(marker in key_text for marker in OPERATIONAL_CONTEXT_KEYS)


def _context_value_is_violation(key_text, value):
    if value in (None, "", False):
        return False

    flattened = _flatten_text(value)
    normalized = _normalize(flattened)

    if normalized in {"none", "nenhum", "nenhuma", "n/a", "na", "somente leitura"}:
        return False

    if _looks_like_disclaimer(flattened):
        return False

    strong_contexts = (
        "broker",
        "api",
        "trigger",
        "automacao",
        "automation",
        "roteamento",
        "routing",
        "contexto_externo",
        "external_context",
    )
    if any(marker in key_text for marker in strong_contexts):
        return True

    return _is_explicit_operational_command(flattened)


def _is_explicit_operational_command(text):
    normalized = _normalize(text)
    if _looks_like_disclaimer(text):
        return False
    return any(phrase in normalized for phrase in EXPLICIT_OPERATIONAL_PHRASES)


def _looks_like_disclaimer(text):
    normalized = _normalize(text)
    if not normalized:
        return False

    operational_terms = (
        "execucao",
        "executavel",
        "ordem",
        "broker",
        "api",
        "trigger",
        "automacao",
        "roteamento",
        "chamada externa",
        "envio automatico",
    )

    has_disclaimer = any(marker in normalized for marker in DISCLAIMER_MARKERS)
    has_operational_term = any(term in normalized for term in operational_terms)
    return has_disclaimer and has_operational_term


def _flatten_text(value):
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            parts.append(str(key))
            parts.append(_flatten_text(item))
        return " ".join(parts)
    if isinstance(value, (list, tuple, set)):
        return " ".join(_flatten_text(item) for item in value)
    return "" if value is None else str(value)


def _normalize(value):
    return str(value).strip().lower()


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, (tuple, set)):
        return list(value)
    return [value]


def _merge_unique(*lists):
    result = []
    seen = set()
    for items in lists:
        for item in _as_list(items):
            marker = str(item)
            if marker not in seen:
                seen.add(marker)
                result.append(item)
    return result


def _resolve_summary_id(base, metadata, summary_status):
    if isinstance(metadata, dict) and metadata.get("summary_id"):
        return str(metadata["summary_id"])

    closure_id = base.get("closure_id")
    if closure_id:
        return "summary-" + _safe_identifier(closure_id)

    return "summary-" + _safe_identifier(summary_status)


def _safe_identifier(value):
    text = str(value).strip().lower()
    safe_chars = []
    for char in text:
        if char.isalnum():
            safe_chars.append(char)
        elif char in {"-", "_"}:
            safe_chars.append(char)
        else:
            safe_chars.append("-")
    return "".join(safe_chars).strip("-") or "indefinido"


def _build_executive_summary_text(summary_status, base, validation_errors):
    if summary_status == "gerado":
        return "Sumario executivo final gerado para cadeia auditavel encerrada e sem alertas herdados relevantes."
    if summary_status == "gerado_com_alertas":
        return "Sumario executivo final gerado com preservacao de alertas, limitacoes ou inconsistencias herdadas."
    if summary_status == "bloqueado_por_guardrail":
        return "Sumario executivo final bloqueado por guardrail operacional."
    if summary_status == "inconclusivo":
        return "Sumario executivo final inconclusivo por status de encerramento ou informacao insuficiente."
    if validation_errors:
        return "Sumario executivo final nao gerado por falha de validacao estrutural."
    return "Sumario executivo final nao gerado."


def _build_chain_overview(base):
    components = _as_list(base.get("chain_components"))
    return {
        "closure_id": base.get("closure_id"),
        "component_count": len(components),
        "components": components,
        "closure_status": base.get("closure_status"),
        "is_chain_closed": base.get("is_chain_closed"),
        "operational_status": base.get("operational_status"),
        "guardrail_status": base.get("guardrail_status"),
    }


def _build_final_conclusion(summary_status):
    conclusions = {
        "gerado": (
            "Cadeia auditavel sumarizada de forma final, somente leitura, "
            "sem autorizacao operacional real."
        ),
        "gerado_com_alertas": (
            "Cadeia auditavel sumarizada com alertas herdados preservados, "
            "sem autorizacao operacional real."
        ),
        "nao_gerado": (
            "Sumario executivo final nao gerado por ausencia ou invalidade estrutural "
            "do encerramento auditavel."
        ),
        "bloqueado_por_guardrail": (
            "Sumario executivo final bloqueado por guardrail e sem qualquer autorizacao "
            "para execucao operacional real."
        ),
        "inconclusivo": (
            "Sumario executivo final inconclusivo e limitado a diagnostico somente leitura."
        ),
    }
    return conclusions.get(summary_status, "Status de sumario nao reconhecido.")


def _build_sections(summary):
    return {
        "identificacao": {
            "summary_id": summary["summary_id"],
            "closure_id": summary["closure_id"],
            "report_id": summary["report_id"],
            "event_id": summary["event_id"],
            "alert_type": summary["alert_type"],
        },
        "origem_do_encerramento": {
            "source_closure_status": summary["source_closure_status"],
            "source_is_chain_closed": summary["source_is_chain_closed"],
            "source_operational_status": summary["source_operational_status"],
            "source_guardrail_status": summary["source_guardrail_status"],
        },
        "resumo_executivo_final": summary["executive_summary"],
        "panorama_da_cadeia": summary["chain_overview"],
        "componentes_da_cadeia": summary["chain_components"],
        "status_do_encerramento": summary["source_closure_status"],
        "rastreabilidade_final": {
            "summary_id": summary["summary_id"],
            "closure_id": summary["closure_id"],
            "report_id": summary["report_id"],
            "event_id": summary["event_id"],
            "alert_type": summary["alert_type"],
        },
        "inconsistencias_herdadas": summary["inherited_inconsistencies"],
        "warnings_herdados": summary["inherited_warnings"],
        "limitacoes_herdadas": summary["inherited_limitations"],
        "checks_herdados": summary["inherited_checks"],
        "riscos_residuais": summary["final_risks"],
        "guardrails": {
            "guardrail_status": summary["guardrail_status"],
            "operational_status": summary["operational_status"],
            "nota": "Somente leitura e sem execucao operacional real.",
        },
        "conclusao_executiva_final": summary["final_executive_conclusion"],
    }
