from pathlib import Path
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_3_mapeamento_schema_cobertura_20260713.py")


def test_fase6_3_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_3_script_uses_sqlite_read_only_mode() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text


def test_fase6_3_script_targets_expected_tables() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "rtd_option_quotes_intraday_history" in text
    assert "rtd_option_quotes_intraday_candles" in text


def test_fase6_3_script_blocks_real_cleanup() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "Aprovado para limpeza real: nao" in text
    assert "Registros removidos: 0" in text
    assert "Banco alterado: nao" in text


def test_fase6_3_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None
