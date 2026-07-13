from pathlib import Path
import json
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_10_plano_execucao_controlada_backup_20260713.py")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_plano_execucao_controlada_backup_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_manifesto_ids_elegiveis_20260713.json")


def test_fase6_10_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_10_script_uses_read_only_mode() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text


def test_fase6_10_script_uses_canonical_timezone() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert 'LOCAL_TZ_NAME = "America/Sao_Paulo"' in text
    assert "ZoneInfo(LOCAL_TZ_NAME)" in text
    assert ".astimezone(LOCAL_TZ).replace(tzinfo=None)" in text


def test_fase6_10_script_requires_backup_and_blocks_cleanup() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "Backup obrigatorio antes da limpeza real: sim" in text
    assert "Aprovado para limpeza real: nao" in text
    assert "Registros removidos: 0" in text
    assert "Banco alterado: nao" in text


def test_fase6_10_manifest_is_valid_json_when_present() -> None:
    if MANIFEST_PATH.exists():
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        assert data["phase"] == "6.10"
        assert data["summary"]["real_cleanup_approved"] is False
        assert data["summary"]["backup_required_before_cleanup"] is True
        assert data["rule"]["timezone"] == "America/Sao_Paulo"


def test_fase6_10_report_mentions_manifest_when_present() -> None:
    if REPORT_PATH.exists():
        text = REPORT_PATH.read_text(encoding="utf-8")
        assert "Manifesto" in text
        assert "fase6_10_manifesto_ids_elegiveis_20260713.json" in text


def test_fase6_10_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None
