from ATT.final_audit_report_service import generate_final_audit_report


def make_valid_trail():
    return {
        "consolidated_status": "consolidado",
        "is_consolidated": True,
        "event_id": "EVT-7R7-001",
        "alert_type": "alerta_simulado",
        "chain_components": {
            "alert": "presente",
            "decision": "presente",
            "explanation": "presente",
            "cross_validation": "presente",
        },
        "chain_consistency_status": "consistente",
        "validation_status": "valido",
        "explanation_status": "valido",
        "decision_status": "valido",
        "alert_status": "valido",
        "inconsistencies": [],
        "warnings": [],
        "checks_performed": ["check_origem_7R6"],
        "limitations": ["dados simulados"],
        "guardrail_status": "preservado",
        "operational_status": "somente_leitura",
        "audit_summary": "Trilha consolidada em modo diagnostico.",
        "audit_note": "Sem autorizacao para execucao real.",
    }


def test_relatorio_gerado_para_trilha_consolidada():
    report = generate_final_audit_report(
        make_valid_trail(),
        metadata={
            "report_id": "RPT-001",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    assert report["report_status"] == "gerado"
    assert report["is_report_generated"] is True
    assert report["report_id"] == "RPT-001"
    assert report["event_id"] == "EVT-7R7-001"
    assert report["alert_type"] == "alerta_simulado"
    assert report["operational_status"] == "somente_leitura"
    assert report["guardrail_status"] == "preservado"


def test_relatorio_gerado_com_alertas_quando_origem_tem_warning():
    trail = make_valid_trail()
    trail["warnings"] = ["warning herdado da consolidacao"]

    report = generate_final_audit_report(
        trail,
        metadata={
            "report_id": "RPT-002",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    assert report["report_status"] == "gerado_com_alertas"
    assert "warning herdado da consolidacao" in report["warnings"]


def test_relatorio_nao_gerado_por_trilha_ausente():
    report = generate_final_audit_report(None)

    assert report["report_status"] == "nao_gerado"
    assert report["is_report_generated"] is False
    assert "trilha consolidada ausente" in report["inconsistencies"]


def test_relatorio_nao_gerado_por_trilha_invalida():
    report = generate_final_audit_report(["entrada", "invalida"])

    assert report["report_status"] == "nao_gerado"
    assert report["is_report_generated"] is False
    assert "trilha consolidada invalida" in report["inconsistencies"]


def test_relatorio_nao_gerado_por_status_consolidado_nao_permitido():
    trail = make_valid_trail()
    trail["consolidated_status"] = "status_desconhecido"

    report = generate_final_audit_report(
        trail,
        metadata={
            "report_id": "RPT-003",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    assert report["report_status"] == "nao_gerado"
    assert report["is_report_generated"] is False
    assert "status consolidado nao permitido" in report["inconsistencies"]


def test_relatorio_bloqueado_por_guardrail_em_pedido_explicito_de_execucao():
    trail = make_valid_trail()

    report = generate_final_audit_report(
        trail,
        metadata={
            "report_id": "RPT-004",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
            "execution_request": "enviar ordem de compra",
        },
    )

    assert report["report_status"] == "bloqueado_por_guardrail"
    assert report["is_report_generated"] is False
    assert report["guardrail_status"] == "bloqueado_por_guardrail"
    assert any("execucao operacional" in item for item in report["inconsistencies"])


def test_relatorio_inconclusivo_quando_origem_inconclusiva():
    trail = make_valid_trail()
    trail["consolidated_status"] = "inconclusivo"

    report = generate_final_audit_report(
        trail,
        metadata={
            "report_id": "RPT-005",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    assert report["report_status"] == "inconclusivo"
    assert report["is_report_generated"] is False


def test_propagacao_de_inconsistencias():
    trail = make_valid_trail()
    trail["inconsistencies"] = ["inconsistencia herdada"]

    report = generate_final_audit_report(
        trail,
        metadata={
            "report_id": "RPT-006",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    assert report["report_status"] == "gerado_com_alertas"
    assert "inconsistencia herdada" in report["inconsistencies"]


def test_propagacao_de_warnings():
    trail = make_valid_trail()
    trail["warnings"] = ["warning herdado"]

    report = generate_final_audit_report(
        trail,
        metadata={
            "report_id": "RPT-007",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    assert "warning herdado" in report["warnings"]


def test_propagacao_de_limitacoes_e_limitacoes_obrigatorias():
    trail = make_valid_trail()
    trail["limitations"] = ["limitacao herdada"]

    report = generate_final_audit_report(
        trail,
        metadata={
            "report_id": "RPT-008",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    assert "limitacao herdada" in report["limitations"]
    assert "ausencia de Excel real" in report["limitations"]
    assert "ausencia de broker" in report["limitations"]
    assert "relatorio somente leitura" in report["limitations"]


def test_secoes_obrigatorias_presentes_e_saida_nao_executavel():
    report = generate_final_audit_report(
        make_valid_trail(),
        metadata={
            "report_id": "RPT-009",
            "timestamp": "simulado",
            "reviewer": "auditoria simbolica",
        },
    )

    expected_sections = {
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
    }

    assert expected_sections.issubset(set(report["audit_sections"].keys()))
    assert "sem autorizacao para execucao operacional real" in report["audit_note"]
    assert report["operational_status"] == "somente_leitura"
