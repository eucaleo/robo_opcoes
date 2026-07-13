from pathlib import Path
import json
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_12_prepara_execucao_real_rollback_20260713.py")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_12_prepara_execucao_real_rollback_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_12_prepara_execucao_real_rollback_20260713.json")


def test_fase6_12_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_12_script_references_required_previous_phases() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "fase6_10_manifesto_ids_elegiveis_20260713.json" in text
    assert "fase6_11_backup_fisico_controlado_20260713.json" in text
    assert "fase6_10_plano_execucao_controlada_backup_20260713.md" in text


def test_fase6_12_script_is_read_only_for_database() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text
    assert "PRAGMA integrity_check" in text
    assert "database_modified" in text
    assert '"database_modified": False' in text


def test_fase6_12_script_validates_backup_and_rollback() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "backup_validated" in text
    assert "rollback_plan" in text
    assert "restaurar_arquivo_db_a_partir_do_backup_fisico_validado" in text
    assert "requires_sha256_validation_after_restore" in text
    assert "requires_sqlite_integrity_check_after_restore" in text


def test_fase6_12_script_keeps_real_cleanup_blocked() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert '"real_cleanup_executed": False' in text
    assert '"real_cleanup_approved": False' in text
    assert '"records_removed": 0' in text
    assert '"next_phase_requires_explicit_confirmation": True' in text


def test_fase6_12_script_validates_eligible_ids() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "TARGET_TABLE = \"rtd_option_quotes_intraday_history\"" in text
    assert "eligible_present" in text
    assert "phase_6_10_eligible_count != 60" in text
    assert "phase_6_10_blocked_count != 0" in text


def test_fase6_12_manifest_is_valid_when_present() -> None:
    if MANIFEST_PATH.exists():
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        assert data["phase"] == "6.12"
        assert data["decision"]["preflight_ready"] is True
        assert data["decision"]["real_cleanup_executed"] is False
        assert data["decision"]["real_cleanup_approved"] is False
        assert data["decision"]["records_removed"] == 0
        assert data["decision"]["database_modified"] is False
        assert data["decision"]["next_phase_requires_explicit_confirmation"] is True
        assert data["backup_reference"]["validated"] is True
        assert data["backup_reference"]["versioned_in_git"] is False
        assert data["cleanup_candidate"]["eligible_count"] == 60
        assert data["cleanup_candidate"]["blocked_count"] == 0
        assert data["candles_preservation"]["planned_to_modify"] is False


def test_fase6_12_report_mentions_no_cleanup_when_present() -> None:
    if REPORT_PATH.exists():
        text = REPORT_PATH.read_text(encoding="utf-8")
        assert "PRE_FLIGHT_EXECUCAO_REAL_COM_ROLLBACK_PRONTO" in text
        assert "Pre-flight pronto: sim" in text
        assert "Rollback documentado: sim" in text
        assert "Limpeza real executada: nao" in text
        assert "Limpeza real aprovada: nao" in text
        assert "Registros removidos: 0" in text
        assert "Banco alterado: nao" in text
        assert "Proxima fase exige confirmacao explicita: sim" in text


def test_fase6_12_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None
