import inspect

from ATT.auditable_chain_closure_service import close_auditable_chain


def _valid_report(**overrides):
    report = {
        "report_status": "gerado",
        "is_report_generated": True,
        "report_id": "report-001",
        "event_id": "event-001",
        "alert_type": "simulated_alert",
        "source_consolidated_status": "consolidado",
        "source_chain_consistency_status": "consistente",
        "executive_summary": "Relatorio final auditavel simulado.",
        "audit_sections": {
            "identificacao": {},
            "origem_da_trilha": {},
            "resumo_executivo_diagnostico": {},
            "status_consolidado": {},
            "componentes_da_cadeia": {},
            "validacao_cruzada": {},
            "explicacao_operacional": {},
            "decisao_simulada": {},
            "alerta_simulado": {},
            "inconsistencias": {},
            "warnings": {},
            "limitacoes": {},
            "checks_executados": {},
            "guardrails": {},
            "conclusao_auditavel": {},
        },
        "inconsistencies": [],
        "warnings": [],
        "limitations": [],
        "checks_performed": ["check anterior"],
        "guardrail_status": "PRESERVADO",
        "operational_status": "SEM AUTORIZACAO PARA EXECUCAO REAL",
        "final_audit_conclusion": "Relatorio gerado sem execucao real.",
        "audit_note": "Somente leitura.",
    }
    report.update(overrides)
    return report


def test_encerramento_gerado_para_relatorio_valido():
    result = close_auditable_chain(_valid_report())

    assert result["closure_status"] == "encerrado"
    assert result["is_chain_closed"] is True
    assert result["report_id"] == "report-001"
    assert result["event_id"] == "event-001"
    assert result["alert_type"] == "simulated_alert"
    assert result["operational_status"] == "SEM AUTORIZACAO PARA EXECUCAO REAL"


def test_encerramento_gerado_com_alertas():
    result = close_auditable_chain(
        _valid_report(warnings=["warning herdado"])
    )

    assert result["closure_status"] == "encerrado_com_alertas"
    assert result["is_chain_closed"] is True
    assert "warning herdado" in result["warnings"]


def test_encerramento_nao_gerado_por_relatorio_ausente():
    result = close_auditable_chain(None)

    assert result["closure_status"] == "nao_encerrado"
    assert result["is_chain_closed"] is False
    assert result["report_id"] is None


def test_encerramento_nao_gerado_por_relatorio_invalido():
    result = close_auditable_chain(["relatorio invalido"])

    assert result["closure_status"] == "nao_encerrado"
    assert result["is_chain_closed"] is False
    assert result["inconsistencies"]


def test_encerramento_nao_gerado_por_status_nao_permitido():
    result = close_auditable_chain(
        _valid_report(report_status="status_nao_permitido")
    )

    assert result["closure_status"] == "nao_encerrado"
    assert result["is_chain_closed"] is False
    assert any("report_status nao permitido" in item for item in result["inconsistencies"])


def test_encerramento_bloqueado_por_guardrail_de_origem():
    result = close_auditable_chain(
        _valid_report(report_status="bloqueado_por_guardrail")
    )

    assert result["closure_status"] == "bloqueado_por_guardrail"
    assert result["is_chain_closed"] is False
    assert result["guardrail_status"] == "BLOQUEADO"


def test_encerramento_bloqueado_por_comando_operacional_em_metadados():
    result = close_auditable_chain(
        _valid_report(),
        metadata={"command": "enviar ordem real para broker"},
    )

    assert result["closure_status"] == "bloqueado_por_guardrail"
    assert result["is_chain_closed"] is False
    assert result["guardrail_status"] == "BLOQUEADO"


def test_encerramento_inconclusivo():
    result = close_auditable_chain(
        _valid_report(report_status="inconclusivo")
    )

    assert result["closure_status"] == "inconclusivo"
    assert result["is_chain_closed"] is False


def test_propaga_inconsistencias():
    result = close_auditable_chain(
        _valid_report(inconsistencies=["inconsistencia herdada"])
    )

    assert "inconsistencia herdada" in result["inconsistencies"]
    assert result["closure_status"] == "encerrado_com_alertas"


def test_propaga_warnings():
    result = close_auditable_chain(
        _valid_report(warnings=["warning herdado"])
    )

    assert "warning herdado" in result["warnings"]


def test_propaga_limitacoes():
    result = close_auditable_chain(
        _valid_report(limitations=["limitacao herdada"])
    )

    assert "limitacao herdada" in result["limitations"]
    assert "ausencia de broker real" in result["limitations"]


def test_propaga_checks_executados():
    result = close_auditable_chain(
        _valid_report(checks_performed=["check herdado"])
    )

    assert "check herdado" in result["checks_performed"]
    assert "validacao de ausencia de execucao operacional" in result["checks_performed"]


def test_secoes_obrigatorias():
    result = close_auditable_chain(_valid_report())

    required_sections = {
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
    }

    assert required_sections.issubset(set(result["closure_sections"].keys()))


def test_saida_nao_executavel():
    result = close_auditable_chain(_valid_report())

    assert result["operational_status"] == "SEM AUTORIZACAO PARA EXECUCAO REAL"
    assert "sem autorizacao" in result["audit_note"].lower()
    assert "recomendacao executavel" in result["audit_note"].lower()


def test_ausencia_de_integracoes_reais_no_codigo():
    import ATT.auditable_chain_closure_service as module

    source = inspect.getsource(module)
    forbidden_tokens = [
        "win32com",
        "xlwings",
        "pythoncom",
        "sqlite3",
        "requests",
        "subprocess",
        "socket",
        "open(",
    ]

    for token in forbidden_tokens:
        assert token not in source
