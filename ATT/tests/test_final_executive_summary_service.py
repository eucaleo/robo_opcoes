import inspect
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import final_executive_summary_service as service
from final_executive_summary_service import build_final_executive_summary


def valid_closure(**overrides):
    base = {
        "closure_status": "encerrado",
        "is_chain_closed": True,
        "closure_id": "closure-7r8-001",
        "report_id": "report-7r7-001",
        "event_id": "event-001",
        "alert_type": "simulado",
        "source_report_status": "gerado",
        "source_operational_status": "somente_leitura_sem_execucao_real",
        "source_guardrail_status": "preservado",
        "source_chain_consistency_status": "consistente",
        "closure_summary": "Encerramento auditavel concluido.",
        "chain_components": [
            "alerta_simulado",
            "decisao_simulada",
            "explicacao_operacional",
            "validacao_cruzada",
            "trilha_consolidada",
            "relatorio_final_auditavel",
        ],
        "closure_sections": {
            "identificacao": {},
            "origem_do_relatorio": {},
            "resumo_do_encerramento": {},
            "componentes_da_cadeia": {},
            "status_do_relatorio_final": {},
            "rastreabilidade": {},
            "inconsistencias": {},
            "warnings": {},
            "limitacoes": {},
            "checks_executados": {},
            "guardrails": {},
            "conclusao_final_auditavel": {},
        },
        "inconsistencies": [],
        "warnings": [],
        "limitations": [],
        "checks_performed": ["check herdado"],
        "guardrail_status": "preservado",
        "operational_status": "somente_leitura_sem_execucao_real",
        "final_chain_conclusion": "Cadeia encerrada sem execucao real.",
        "audit_note": "Somente leitura.",
    }
    base.update(overrides)
    return base


def test_sumario_gerado_para_encerramento_valido():
    result = build_final_executive_summary(valid_closure())

    assert result["summary_status"] == "gerado"
    assert result["is_summary_generated"] is True
    assert result["closure_id"] == "closure-7r8-001"
    assert result["operational_status"] == "somente_leitura_sem_execucao_real"


def test_sumario_gerado_com_alertas():
    result = build_final_executive_summary(
        valid_closure(
            closure_status="encerrado_com_alertas",
            warnings=["warning herdado"],
        )
    )

    assert result["summary_status"] == "gerado_com_alertas"
    assert result["is_summary_generated"] is True
    assert "warning herdado" in result["inherited_warnings"]


def test_sumario_nao_gerado_por_encerramento_ausente():
    result = build_final_executive_summary(None)

    assert result["summary_status"] == "nao_gerado"
    assert result["is_summary_generated"] is False


def test_sumario_nao_gerado_por_encerramento_invalido():
    result = build_final_executive_summary(["invalido"])

    assert result["summary_status"] == "nao_gerado"
    assert result["is_summary_generated"] is False


def test_sumario_nao_gerado_por_status_nao_permitido():
    result = build_final_executive_summary(valid_closure(closure_status="executar"))

    assert result["summary_status"] == "nao_gerado"
    assert result["is_summary_generated"] is False


def test_sumario_bloqueado_por_guardrail_de_origem():
    result = build_final_executive_summary(
        valid_closure(
            closure_status="bloqueado_por_guardrail",
            guardrail_status="violado",
        )
    )

    assert result["summary_status"] == "bloqueado_por_guardrail"
    assert result["guardrail_status"] == "violado"


def test_sumario_bloqueado_por_comando_operacional_em_metadados():
    result = build_final_executive_summary(
        valid_closure(),
        metadata={"comando": "executar ordem real no broker"},
    )

    assert result["summary_status"] == "bloqueado_por_guardrail"
    assert result["is_summary_generated"] is False


def test_sumario_inconclusivo():
    result = build_final_executive_summary(
        valid_closure(
            closure_status="inconclusivo",
            is_chain_closed=False,
        )
    )

    assert result["summary_status"] == "inconclusivo"
    assert result["is_summary_generated"] is False


def test_propagacao_de_inconsistencias_herdadas():
    result = build_final_executive_summary(
        valid_closure(inconsistencies=["inconsistencia herdada"])
    )

    assert result["summary_status"] == "gerado_com_alertas"
    assert "inconsistencia herdada" in result["inherited_inconsistencies"]


def test_propagacao_de_warnings_herdados():
    result = build_final_executive_summary(
        valid_closure(warnings=["warning herdado"])
    )

    assert result["summary_status"] == "gerado_com_alertas"
    assert "warning herdado" in result["inherited_warnings"]


def test_propagacao_de_limitacoes_herdadas():
    result = build_final_executive_summary(
        valid_closure(limitations=["limitacao herdada"])
    )

    assert result["summary_status"] == "gerado_com_alertas"
    assert "limitacao herdada" in result["inherited_limitations"]
    assert "limitacao herdada" in result["final_limitations"]


def test_propagacao_de_checks_herdados():
    result = build_final_executive_summary(
        valid_closure(checks_performed=["check anterior"])
    )

    assert "check anterior" in result["inherited_checks"]
    assert "check anterior" in result["checks_performed"]
    assert "validacao de ausencia de integracoes reais" in result["checks_performed"]


def test_preserva_identificadores():
    result = build_final_executive_summary(
        valid_closure(
            closure_id="closure-x",
            report_id="report-y",
            event_id="event-z",
            alert_type="alerta-teste",
        )
    )

    assert result["closure_id"] == "closure-x"
    assert result["report_id"] == "report-y"
    assert result["event_id"] == "event-z"
    assert result["alert_type"] == "alerta-teste"


def test_secoes_obrigatorias_presentes():
    result = build_final_executive_summary(valid_closure())

    for section in service.MANDATORY_SUMMARY_SECTIONS:
        assert section in result["summary_sections"]


def test_riscos_residuais_obrigatorios_presentes():
    result = build_final_executive_summary(valid_closure())

    for risk in service.MANDATORY_FINAL_RISKS:
        assert risk in result["final_risks"]


def test_saida_nao_executavel():
    result = build_final_executive_summary(valid_closure())

    assert result["operational_status"] == "somente_leitura_sem_execucao_real"
    assert "sem autorizacao" in result["final_executive_conclusion"]


def test_ausencia_de_integracoes_reais_no_codigo_do_servico():
    source = inspect.getsource(service)
    forbidden = [
        "win32com",
        "xlwings",
        "pythoncom",
        "sqlite3",
        "requests",
        "subprocess",
        "socket",
        "open(",
    ]

    for token in forbidden:
        assert token not in source
