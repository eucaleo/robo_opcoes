from pathlib import Path
import json
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_11_backup_fisico_controlado_20260713.py")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_11_backup_fisico_controlado_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_11_backup_fisico_controlado_20260713.json")


def test_fase6_11_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_11_script_uses_phase_6_10_manifest() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "fase6_10_manifesto_ids_elegiveis_20260713.json" in text
    assert "expected_eligible != 60" in text
    assert "expected_blocked != 0" in text


def test_fase6_11_script_uses_read_only_sqlite_integrity_check() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text
    assert "PRAGMA integrity_check" in text


def test_fase6_11_script_copies_backup_and_does_not_version_db() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "shutil.copy2" in text
    assert '"versioned_in_git": False' in text
    assert "backups_local/" in text


def test_fase6_11_script_blocks_cleanup() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert '"cleanup_executed": False' in text
    assert '"records_removed": 0' in text
    assert '"database_modified": False' in text
    assert '"approved_for_real_cleanup": False' in text


def test_fase6_11_manifest_is_valid_when_present() -> None:
    if MANIFEST_PATH.exists():
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        assert data["phase"] == "6.11"
        assert data["backup_database"]["versioned_in_git"] is False
        assert data["decision"]["backup_created"] is True
        assert data["decision"]["backup_validated"] is True
        assert data["decision"]["approved_for_real_cleanup"] is False
        assert data["rule"]["records_removed"] == 0
        assert data["rule"]["database_modified"] is False


def test_fase6_11_report_mentions_backup_when_present() -> None:
    if REPORT_PATH.exists():
        text = REPORT_PATH.read_text(encoding="utf-8")
        assert "BACKUP_FISICO_CONTROLADO_CRIADO_E_VALIDADO" in text
        assert "Backup versionado no Git: nao" in text
        assert "Banco original alterado: nao" in text
        assert "Limpeza real aprovada: nao" in text


def test_fase6_11_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None
