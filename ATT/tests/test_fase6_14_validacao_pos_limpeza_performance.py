from pathlib import Path
import json


SCRIPT_PATH = Path("ATT/scripts/fase6_14_validacao_pos_limpeza_performance_20260713.py")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_14_validacao_pos_limpeza_performance_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_14_validacao_pos_limpeza_performance_20260713.json")


def test_fase6_14_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_14_script_is_read_only_for_database() -> None:
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


def test_fase6_14_manifest_is_valid() -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert data["phase"] == "6.14"
    assert data["database"]["open_mode"] == "read_only"
    assert data["database"]["database_modified"] is False
    assert data["database"]["sha256_unchanged"] is True
    assert str(data["database"]["sqlite_integrity"]).lower() == "ok"

    validation = data["post_cleanup_validation"]
    assert validation["history_total"] == 0
    assert validation["expected_history_total"] == 0
    assert validation["eligible_ids_checked"] == 60
    assert validation["eligible_ids_remaining"] == 0
    assert validation["candles_total"] == 110
    assert validation["expected_candles_total"] == 110

    regression = data["regression_checks"]
    assert regression["integrity_ok"] is True
    assert regression["history_clean"] is True
    assert regression["eligible_ids_absent"] is True
    assert regression["candles_preserved"] is True
    assert regression["database_hash_unchanged"] is True
    assert regression["no_write_operation_performed"] is True

    decision = data["decision"]
    assert decision["phase_6_14_status"] == "APROVADA"
    assert decision["post_cleanup_validated"] is True
    assert decision["performance_validated"] is True
    assert decision["regression_absent"] is True
    assert decision["database_modified"] is False


def test_fase6_14_performance_is_within_threshold() -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    perf = data["performance"]

    assert perf["performance_ok"] is True
    assert perf["max_elapsed_ms"] <= perf["threshold_ms"]

    for value in perf["measurements_ms"].values():
        assert value >= 0
        assert value <= perf["threshold_ms"]


def test_fase6_14_report_mentions_success() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8")

    assert "FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_APROVADA" in text
    assert "Pos-limpeza validado: sim" in text
    assert "Performance validada: sim" in text
    assert "Ausencia de regressao: sim" in text
    assert "Banco modificado: nao" in text
    assert "Integridade final: ok" in text
    assert "Fase 6.14 encerrada tecnicamente: sim" in text
    assert "FIM_FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_20260713" in text
