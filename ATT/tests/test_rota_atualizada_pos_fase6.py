from pathlib import Path


ROUTE_DOC = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/ROTA_ATUALIZADA_POS_FASE6_20260713.md")
MAIN_AUDIT = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_RTD_EXCEL_BTG_ONLINE.md")


def test_rota_atualizada_existe() -> None:
    assert ROUTE_DOC.exists()


def test_rota_registra_fase6_encerrada() -> None:
    text = ROUTE_DOC.read_text(encoding="utf-8")

    assert "FASE 6: ENCERRADA TECNICAMENTE" in text
    assert "FASE 7: PROXIMA FASE PERMITIDA" in text
    assert "ef39bab Encerra frente retencao limpeza Fase 6.15 RTD Excel" in text
    assert "feature/rtd-excel-online-fase6-retencao-limpeza" in text


def test_rota_preserva_restricao_de_ordens_reais() -> None:
    text = ROUTE_DOC.read_text(encoding="utf-8")

    assert "A execucao automatica de ordens reais permanece fora do escopo." in text
    assert "envio automatico de ordens reais" in text
    assert "robo executor" in text
    assert "roteamento automatico para broker" in text


def test_rota_registra_evidencias_fase6() -> None:
    text = ROUTE_DOC.read_text(encoding="utf-8")

    assert "Historico final limpo: sim" in text
    assert "IDs elegiveis remanescentes: 0" in text
    assert "Total de candles preservados: 110" in text
    assert "Integridade SQLite final: ok" in text
    assert "Performance validada: sim" in text
    assert "Ausencia de regressao: sim" in text
    assert "Rollback documentado: sim" in text
    assert "Pronto para revisao ou merge: sim" in text


def test_auditoria_principal_registra_atualizacao() -> None:
    text = MAIN_AUDIT.read_text(encoding="utf-8")

    assert "INICIO_ROTA_ATUALIZADA_POS_FASE6_20260713" in text
    assert "FIM_ROTA_ATUALIZADA_POS_FASE6_20260713" in text
    assert "Fase 6: encerrada tecnicamente" in text
    assert "Fase 7: proxima fase permitida" in text
