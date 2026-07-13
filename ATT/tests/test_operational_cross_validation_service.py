from ATT.operational_cross_validation_service import (
    OPERATIONAL_STATUS,
    VALIDATION_OUTPUT_FIELDS,
    validate_operational_cross_explanation,
)
from ATT.operational_decision_explanation_service import explain_operational_decision


def _base_event(**overrides):
    event = {
        "event_id": "evt-7r5-001",
        "alert_type": "threshold_variation",
        "asset": "SIMULADO",
        "timestamp": "2026-07-10T20:40:00-03:00",
        "observed_values": {"price": 10.5, "reference": 10.0},
        "thresholds": {"variation_limit": 0.03},
        "classification": "atencao",
        "severity": "media",
        "source": "simulado",
        "candidate_rules": [
            {
                "name": "variacao_acima_limite",
                "description": "Compara variacao observada com limite simulado.",
                "condition": "variation > variation_limit",
                "result": True,
                "impact": "eleva_para_atencao",
            }
        ],
    }
    event.update(overrides)
    return event


def _alert_and_decision(event):
    alert = {
        "event_id": event["event_id"],
        "alert_type": event["alert_type"],
        "classification": event.get("classification"),
    }
    decision = {
        "event_id": event["event_id"],
        "alert_type": event["alert_type"],
        "classification": event.get("classification"),
    }
    return alert, decision


def test_validate_operational_cross_explanation_accepts_valid_case():
    event = _base_event()
    alert, decision = _alert_and_decision(event)
    explanation = explain_operational_decision(event)

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert tuple(result.keys()) == VALIDATION_OUTPUT_FIELDS
    assert result["validation_status"] == "valido"
    assert result["is_valid"] is True
    assert result["checked_event_id"] == "evt-7r5-001"
    assert result["checked_alert_type"] == "threshold_variation"
    assert result["inconsistencies"] == []
    assert result["operational_status"] == OPERATIONAL_STATUS


def test_validate_operational_cross_explanation_accepts_valid_case_with_warnings():
    event = _base_event(asset=None, source=None)
    alert, decision = _alert_and_decision(event)
    explanation = explain_operational_decision(event)

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert result["validation_status"] == "valido_com_alertas"
    assert result["is_valid"] is True
    assert result["inconsistencies"] == []
    assert any("Dado recomendado ausente" in item for item in result["warnings"])


def test_validate_operational_cross_explanation_rejects_event_id_divergence():
    event = _base_event()
    alert, decision = _alert_and_decision(event)
    alert["event_id"] = "evt-divergente"
    explanation = explain_operational_decision(event)

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert result["validation_status"] == "invalido"
    assert result["is_valid"] is False
    assert any("event_id divergente" in item for item in result["inconsistencies"])


def test_validate_operational_cross_explanation_rejects_invalid_classification():
    event = _base_event()
    alert, decision = _alert_and_decision(event)
    explanation = explain_operational_decision(event)
    explanation["classification"] = "execucao_real"

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert result["validation_status"] == "invalido"
    assert result["is_valid"] is False
    assert any("classification nao permitido" in item for item in result["inconsistencies"])


def test_validate_operational_cross_explanation_rejects_incomplete_rule():
    event = _base_event()
    alert, decision = _alert_and_decision(event)
    explanation = explain_operational_decision(event)
    explanation["rules_applied"][0]["condition"] = "Condicao nao informada."
    explanation["rules_applied"][0]["result"] = "nao_informado"

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert result["validation_status"] == "invalido"
    assert result["rule_traceability_status"] == "invalido"
    assert any("Regra aplicada incompleta" in item for item in result["inconsistencies"])


def test_validate_operational_cross_explanation_rejects_missing_limitations():
    event = _base_event()
    alert, decision = _alert_and_decision(event)
    explanation = explain_operational_decision(event)
    explanation["limitations"] = []

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert result["validation_status"] == "invalido"
    assert result["limitation_status"] == "invalido"
    assert any("Limitacoes ausentes" in item for item in result["inconsistencies"])


def test_validate_operational_cross_explanation_blocks_guardrail_request():
    event = _base_event()
    alert, decision = _alert_and_decision(event)
    decision["requested_action"] = "executar ordem no broker"
    explanation = explain_operational_decision(event)

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert result["validation_status"] == "bloqueado_por_guardrail"
    assert result["is_valid"] is False
    assert any("Guardrail acionado" in item for item in result["inconsistencies"])


def test_validate_operational_cross_explanation_marks_inconclusive_case():
    event = _base_event(classification="inconclusivo")
    alert, decision = _alert_and_decision(event)
    explanation = explain_operational_decision(event)

    result = validate_operational_cross_explanation(alert, decision, explanation)

    assert result["validation_status"] == "inconclusivo"
    assert result["is_valid"] is False
    assert any("Classificacao inconclusiva" in item for item in result["warnings"])


def test_validate_operational_cross_explanation_rejects_non_mapping_inputs():
    event = _base_event()
    alert, decision = _alert_and_decision(event)
    explanation = explain_operational_decision(event)

    try:
        validate_operational_cross_explanation([], decision, explanation)
    except TypeError as exc:
        assert "alert must be a mapping" in str(exc)
    else:
        raise AssertionError("TypeError was not raised")
