from ATT.audit_trail_consolidation_service import (
    CONSOLIDATION_OUTPUT_FIELDS,
    consolidate_audit_trail,
)


def _alert(**overrides):
    data = {
        "event_id": "evt-001",
        "alert_type": "variacao_preco",
        "asset": "SIMULADO3",
        "status": "simulado",
    }
    data.update(overrides)
    return data


def _decision(**overrides):
    data = {
        "event_id": "evt-001",
        "alert_type": "variacao_preco",
        "decision_status": "observacao",
        "classification": "monitorar",
    }
    data.update(overrides)
    return data


def _explanation(**overrides):
    data = {
        "event_id": "evt-001",
        "alert_type": "variacao_preco",
        "classification": "monitorar",
        "severity": "media",
        "confidence": "media",
        "limitations": [
            "dados simulados",
            "ausencia de Excel real",
            "ausencia de banco real",
            "ausencia de execucao operacional",
            "ausencia de broker",
            "ausencia de validacao em tempo real",
            "uso apenas diagnostico e auditavel",
        ],
        "audit_note": "Explicacao somente leitura e nao executavel.",
        "operational_status": "somente_leitura",
    }
    data.update(overrides)
    return data


def _cross_validation(**overrides):
    data = {
        "validation_status": "valido",
        "is_valid": True,
        "checked_event_id": "evt-001",
        "checked_alert_type": "variacao_preco",
        "inconsistencies": [],
        "warnings": [],
        "checks_performed": ["estrutura", "event_id", "alert_type"],
        "operational_status": "somente_leitura",
        "audit_note": "Validacao cruzada somente leitura.",
    }
    data.update(overrides)
    return data


def test_consolidate_audit_trail_accepts_valid_case():
    result = consolidate_audit_trail(
        _alert(),
        _decision(),
        _explanation(),
        _cross_validation(),
    )

    assert tuple(result.keys()) == CONSOLIDATION_OUTPUT_FIELDS
    assert result["consolidated_status"] == "consolidado"
    assert result["is_consolidated"] is True
    assert result["event_id"] == "evt-001"
    assert result["alert_type"] == "variacao_preco"
    assert result["guardrail_status"] == "preservado"
    assert result["operational_status"] == "somente_leitura"
    assert result["inconsistencies"] == []


def test_consolidate_audit_trail_accepts_valid_case_with_warnings():
    result = consolidate_audit_trail(
        _alert(),
        _decision(),
        _explanation(warnings=["metadados incompletos"]),
        _cross_validation(warnings=["fonte simulada incompleta"]),
    )

    assert result["consolidated_status"] == "consolidado_com_alertas"
    assert result["is_consolidated"] is True
    assert len(result["warnings"]) == 2


def test_consolidate_audit_trail_rejects_missing_component():
    result = consolidate_audit_trail(
        _alert(),
        {},
        _explanation(),
        _cross_validation(),
    )

    assert result["consolidated_status"] == "nao_consolidado"
    assert result["is_consolidated"] is False
    assert result["chain_components"]["decision"] == "ausente"
    assert any("decision" in item for item in result["inconsistencies"])


def test_consolidate_audit_trail_rejects_event_id_divergence():
    result = consolidate_audit_trail(
        _alert(event_id="evt-alerta"),
        _decision(),
        _explanation(),
        _cross_validation(),
    )

    assert result["consolidated_status"] == "nao_consolidado"
    assert any("event_id divergente" in item for item in result["inconsistencies"])


def test_consolidate_audit_trail_rejects_alert_type_divergence():
    result = consolidate_audit_trail(
        _alert(alert_type="tipo_a"),
        _decision(alert_type="tipo_b"),
        _explanation(),
        _cross_validation(),
    )

    assert result["consolidated_status"] == "nao_consolidado"
    assert any("alert_type divergente" in item for item in result["inconsistencies"])


def test_consolidate_audit_trail_rejects_invalid_cross_validation():
    result = consolidate_audit_trail(
        _alert(),
        _decision(),
        _explanation(),
        _cross_validation(validation_status="invalido"),
    )

    assert result["consolidated_status"] == "nao_consolidado"
    assert result["validation_status"] == "invalido"
    assert result["chain_components"]["cross_validation"] == "invalido"


def test_consolidate_audit_trail_blocks_guardrail_action():
    result = consolidate_audit_trail(
        _alert(requested_action="executar ordem no broker"),
        _decision(),
        _explanation(),
        _cross_validation(),
    )

    assert result["consolidated_status"] == "bloqueado_por_guardrail"
    assert result["is_consolidated"] is False
    assert result["guardrail_status"] == "bloqueado"


def test_consolidate_audit_trail_marks_inconclusive_case():
    result = consolidate_audit_trail(
        _alert(),
        _decision(classification="inconclusivo"),
        _explanation(classification="inconclusivo"),
        _cross_validation(validation_status="inconclusivo"),
    )

    assert result["consolidated_status"] == "inconclusivo"
    assert result["is_consolidated"] is False
    assert result["chain_consistency_status"] == "inconclusivo"


def test_consolidate_audit_trail_propagates_inconsistencies():
    result = consolidate_audit_trail(
        _alert(),
        _decision(),
        _explanation(),
        _cross_validation(inconsistencies=["regra incompleta"]),
    )

    assert result["consolidated_status"] == "nao_consolidado"
    assert any("regra incompleta" in item for item in result["inconsistencies"])


def test_consolidate_audit_trail_rejects_invalid_input():
    result = consolidate_audit_trail(
        "alerta invalido",
        _decision(),
        _explanation(),
        _cross_validation(),
    )

    assert result["consolidated_status"] == "nao_consolidado"
    assert result["is_consolidated"] is False
    assert result["chain_consistency_status"] == "inconsistente"
