from pathlib import Path
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_6_validacao_offset_temporal_cobertura_20260713.py")


def test_fase6_6_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_6_script_uses_sqlite_read_only_mode() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text


def test_fase6_6_script_uses_expected_columns() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert 'HISTORY_KEY_COLUMN = "codigo_opcao"' in text
    assert 'CANDLES_KEY_COLUMN = "symbol"' in text
    assert 'HISTORY_TIME_COLUMN = "captured_at"' in text
    assert 'CANDLES_TIME_COLUMN = "bucket_start"' in text
    assert 'CANDLES_INTERVAL_COLUMN = "interval_minutes"' in text


def test_fase6_6_script_tests_temporal_offsets() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "OFFSET_HOURS_TO_TEST" in text
    assert "timedelta(hours=offset_hours)" in text
    assert "captured_ajustado" in text
    assert "OFFSET_TEMPORAL_CANDIDATO_VALIDADO" in text


def test_fase6_6_script_blocks_real_cleanup() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "Aprovado para limpeza real: nao" in text
    assert "Registros removidos: 0" in text
    assert "Banco alterado: nao" in text


def test_fase6_6_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None
