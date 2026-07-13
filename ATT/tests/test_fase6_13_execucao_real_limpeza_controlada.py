from pathlib import Path
import json


SCRIPT_PATH = Path("ATT/scripts/fase6_13_execucao_real_limpeza_controlada_20260713.py")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_13_execucao_real_limpeza_controlada_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_13_execucao_real_limpeza_controlada_20260713.json")


def test_fase6_13_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_13_requires_explicit_confirmation() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "CONFIRM_REAL_CLEANUP_FASE6_13" in text
    assert 'CONFIRM_VALUE = "SIM"' in text
    assert "Confirmacao explicita ausente" in text


def test_fase6_13_uses_phase_6_12_manifest() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "fase6_12_prepara_execucao_real_rollback_20260713.json" in text
    assert 'manifest.get("phase") != "6.12"' in text
    assert "next_phase_requires_explicit_confirmation" in text


def test_fase6_13_validates_backup_and_integrity() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "sha256_file" in text
    assert "PRAGMA integrity_check" in text
    assert "backup_reference" in text
    assert "rollback_reference" in text
    assert "create_local_safety_backup" in text


def test_fase6_13_delete_is_limited_to_target_ids() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "DELETE FROM {TARGET_TABLE} WHERE {TARGET_ID_COLUMN} IN ({placeholders})" in text
    assert "EXPECTED_ELIGIBLE_COUNT = 60" in text
    assert "EXPECTED_BLOCKED_COUNT = 0" in text
    assert "removed != EXPECTED_ELIGIBLE_COUNT" in text


def test_fase6_13_uses_transaction() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "BEGIN IMMEDIATE" in text
    assert "conn.commit()" in text
    assert "conn.rollback()" in text


def test_fase6_13_preserves_candles() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "rtd_option_quotes_intraday_candles" in text
    assert "Candles foram alterados" in text
    assert '"candles_preserved": True' in text


def test_fase6_13_manifest_is_valid_when_present() -> None:
    if not MANIFEST_PATH.exists():
        return

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert data["phase"] == "6.13"
    assert data["confirmation"]["confirmed"] is True
    assert data["database"]["database_modified"] is True
    assert data["rollback_reference"]["rollback_available"] is True

    cleanup = data["cleanup_execution"]

    assert cleanup["target_table"] == "rtd_option_quotes_intraday_history"
    assert cleanup["eligible_count_before"] == 60
    assert cleanup["eligible_count_after"] == 0
    assert cleanup["blocked_count"] == 0
    assert cleanup["records_removed"] == 60
    assert cleanup["table_total_after"] == cleanup["expected_table_total_after"]

    candles = data["candles_preservation"]
    assert candles["rows_before"] == candles["rows_after"]
    assert candles["modified"] is False

    decision = data["decision"]
    assert decision["real_cleanup_executed"] is True
    assert decision["real_cleanup_approved"] is True
    assert decision["records_removed"] == 60
    assert decision["database_modified"] is True
    assert decision["rollback_documented"] is True
    assert decision["candles_preserved"] is True

    if decision.get("regularization_only") is True:
        assert decision["new_delete_executed_during_regularization"] is False
        assert cleanup["regularization_executed_delete"] is False


def test_fase6_13_report_mentions_real_cleanup_when_present() -> None:
    if not REPORT_PATH.exists():
        return

    text = REPORT_PATH.read_text(encoding="utf-8")

    assert "LIMPEZA_REAL_CONTROLADA_EXECUTADA" in text
    assert "Limpeza real executada: sim" in text
    assert "Limpeza real aprovada: sim" in text
    assert "Registros removidos: 60" in text
    assert "Banco alterado: sim" in text
    assert "Rollback documentado: sim" in text
    assert "Candles preservados: sim" in text
    assert "Fase 6.13 encerrada tecnicamente: sim" in text


def test_fase6_13_has_no_unbounded_delete() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    delete_lines = [
        line.strip()
        for line in text.splitlines()
        if "DELETE FROM" in line.upper()
    ]

    assert delete_lines

    for line in delete_lines:
        upper = line.upper()
        assert "WHERE" in upper
        assert " IN " in upper or " IN(" in upper
