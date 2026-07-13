from ATT.operational_decision_explanation_service import (
    CONTRACT_OUTPUT_FIELDS,
    OPERATIONAL_STATUS,
    explain_operational_decision,
)


def test_explain_operational_decision_returns_contract_fields_for_complete_event():
    event = {
        "event_id": "evt-001",
        "alert_type": "threshold_variation",
        "asset": "SIMULADO",
        "timestamp": "2026-07-10T20:30:00-03:00",
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

    explanation = explain_operational_decision(event)

    assert tuple(explanation.keys()) == CONTRACT_OUTPUT_FIELDS
    assert explanation["event_id"] == "evt-001"
    assert explanation["alert_type"] == "threshold_variation"
    assert explanation["classification"] == "atencao"
    assert explanation["severity"] == "media"
    assert explanation["confidence"] == "alta"
    assert explanation["operational_status"] == OPERATIONAL_STATUS
    assert "observed_values" in explanation["data_used"]
    assert explanation["rules_applied"][0]["name"] == "variacao_acima_limite"
    assert "Nao representa ordem operacional real" in explanation["audit_note"]


def test_explain_operational_decision_marks_missing_required_data_as_inconclusive():
    event = {
        "alert_type": "threshold_variation",
        "classification": "atencao",
    }

    explanation = explain_operational_decision(event)

    assert explanation["classification"] == "inconclusivo"
    assert explanation["confidence"] == "baixa"
    assert explanation["data_used"]["event_id"] == "ausente"
    assert any("event_id" in reason for reason in explanation["reasons"])
    assert explanation["operational_status"] == OPERATIONAL_STATUS


def test_explain_operational_decision_blocks_guardrail_request():
    event = {
        "event_id": "evt-guard-001",
        "alert_type": "operational_request",
        "classification": "atencao",
        "requested_action": "executar ordem no broker",
        "candidate_rules": [
            {
                "name": "bloqueio_execucao_real",
                "condition": "requested_action contains executar ordem",
                "result": True,
                "impact": "bloqueia_saida_operacional",
            }
        ],
    }

    explanation = explain_operational_decision(event)

    assert explanation["classification"] == "bloqueado_por_guardrail"
    assert explanation["severity"] == "critica_simulada"
    assert explanation["confidence"] == "alta"
    assert any("Guardrail acionado" in reason for reason in explanation["reasons"])
    assert explanation["operational_status"] == OPERATIONAL_STATUS


def test_explain_operational_decision_normalizes_textual_rules():
    event = {
        "event_id": "evt-002",
        "alert_type": "simple_check",
        "asset": "SIMULADO",
        "timestamp": "2026-07-10T20:31:00-03:00",
        "observed_values": {"value": 1},
        "thresholds": {"limit": 2},
        "classification": "informativo",
        "source": "simulado",
        "candidate_rules": ["regra_textual_simples"],
    }

    explanation = explain_operational_decision(event)

    assert explanation["classification"] == "informativo"
    assert explanation["rules_applied"][0]["name"] == "regra_textual_simples"
    assert explanation["rules_applied"][0]["result"] == "nao_informado"
    assert explanation["operational_status"] == OPERATIONAL_STATUS


def test_explain_operational_decision_rejects_non_mapping_input():
    try:
        explain_operational_decision(["nao", "e", "mapping"])
    except TypeError as exc:
        assert "event must be a mapping" in str(exc)
    else:
        raise AssertionError("TypeError was not raised")
