from pathlib import Path
import json


SCRIPT_PATH = Path("ATT/scripts/fase6_15_encerramento_frente_consolidacao_final_20260713.py")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_15_encerramento_frente_consolidacao_final_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_15_encerramento_frente_consolidacao_final_20260713.json")


def test_fase6_15_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_15_script_opens_database_read_only() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text
    assert "connect_readonly" in text
    assert "DELETE FROM" not in text.upper()
    assert "UPDATE " not in text.upper()
    assert "INSERT INTO" not in text.upper()
    assert "DROP TABLE" not in text.upper()
    assert "ALTER TABLE" not in text.upper()
    assert "VACUUM" not in text.upper()
    assert "WAL_CHECKPOINT" not in text.upper()


def test_fase6_15_manifest_is_valid() -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert data["phase"] == "6.15"
    assert data["database"]["open_mode"] == "read_only"
    assert data["database"]["database_modified"] is False
    assert data["database"]["sha256_unchanged"] is True
    assert str(data["database"]["sqlite_integrity"]).lower() == "ok"
    assert data["database"]["history_total"] == 0
    assert data["database"]["eligible_ids_remaining"] == 0
    assert data["database"]["candles_total"] == 110

    assert data["phase_6_13_summary"]["real_cleanup_executed"] is True
    assert data["phase_6_13_summary"]["records_removed"] == 60
    assert data["phase_6_13_summary"]["eligible_count_after"] == 0
    assert data["phase_6_13_summary"]["rollback_available"] is True
    assert data["phase_6_13_summary"]["candles_preserved"] is True

    assert data["phase_6_14_summary"]["status"] == "APROVADA"
    assert data["phase_6_14_summary"]["post_cleanup_validated"] is True
    assert data["phase_6_14_summary"]["performance_validated"] is True
    assert data["phase_6_14_summary"]["regression_absent"] is True
    assert data["phase_6_14_summary"]["database_modified"] is False

    decision = data["decision"]
    assert decision["phase_6_15_status"] == "APROVADA"
    assert decision["front_status"] == "ENCERRADA_TECNICAMENTE"
    assert decision["cleanup_front_completed"] is True
    assert decision["ready_for_review_or_merge"] is True
    assert decision["database_modified"] is False


def test_fase6_15_all_consolidated_validations_are_ok() -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    validations = data["consolidated_validations"]

    assert validations
    assert all(validations.values())


def test_fase6_15_report_mentions_final_closure() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8")

    assert "FASE6_15_ENCERRAMENTO_FRENTE_CONSOLIDACAO_FINAL_APROVADA" in text
    assert "Frente encerrada tecnicamente: sim" in text
    assert "Limpeza real consolidada: sim" in text
    assert "Pos-limpeza validado: sim" in text
    assert "Performance validada: sim" in text
    assert "Ausencia de regressao: sim" in text
    assert "Rollback documentado: sim" in text
    assert "Banco modificado nesta fase: nao" in text
    assert "Integridade final: ok" in text
    assert "Historico final limpo: sim" in text
    assert "Candles finais preservados: sim" in text
    assert "Pronto para revisao ou merge: sim" in text
    assert "Fase 6.15 encerrada tecnicamente: sim" in text
    assert "FIM_FASE6_15_ENCERRAMENTO_FRENTE_CONSOLIDACAO_FINAL_20260713" in text
