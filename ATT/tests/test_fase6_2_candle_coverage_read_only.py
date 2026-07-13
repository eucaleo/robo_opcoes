from pathlib import Path
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_2_validacao_cobertura_candles_20260713.py")


def test_fase6_2_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_2_script_uses_sqlite_read_only_mode() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text


def test_fase6_2_script_targets_history_and_candles_tables() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "rtd_option_quotes_intraday_history" in text
    assert "rtd_option_quotes_intraday_candles" in text


def test_fase6_2_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None


def test_fase6_2_report_keeps_cleanup_blocked() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "Aprovado para limpeza real: não" in text
    assert "real_cleanup_approved=False" in text
