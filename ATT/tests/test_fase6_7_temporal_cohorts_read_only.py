from pathlib import Path
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_7_diagnostico_coortes_temporais_cobertura_20260713.py")


def test_fase6_7_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_7_script_uses_sqlite_read_only_mode() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text


def test_fase6_7_script_classifies_offsets_per_row() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "RowClassification" in text
    assert "matching_offsets" in text
    assert "chosen_offset" in text
    assert "COORTES_TEMPORAIS_MULTIPLAS_CONFIRMADAS" in text


def test_fase6_7_script_detects_explicit_timezone() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "has_explicit_timezone_marker" in text
    assert "has_explicit_timezone" in text
    assert "com timezone explicito" in text


def test_fase6_7_script_blocks_real_cleanup() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "Aprovado para limpeza real: nao" in text
    assert "Registros removidos: 0" in text
    assert "Banco alterado: nao" in text


def test_fase6_7_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None
