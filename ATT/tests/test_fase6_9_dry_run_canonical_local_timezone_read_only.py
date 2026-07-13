from pathlib import Path
import re


SCRIPT_PATH = Path("ATT/scripts/fase6_9_dry_run_limpeza_canonica_timezone_local_20260713.py")


def test_fase6_9_script_exists() -> None:
    assert SCRIPT_PATH.exists()


def test_fase6_9_script_uses_sqlite_read_only_mode() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "mode=ro" in text


def test_fase6_9_script_uses_canonical_local_timezone() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert 'LOCAL_TZ_NAME = "America/Sao_Paulo"' in text
    assert "ZoneInfo(LOCAL_TZ_NAME)" in text
    assert ".astimezone(LOCAL_TZ).replace(tzinfo=None)" in text


def test_fase6_9_script_reports_dry_run_eligibility() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "HistoryCandidate" in text
    assert "eligible" in text
    assert "COBERTO_POR_CANDLE_CANONICO_LOCAL" in text
    assert "Linhas elegiveis por cobertura canonica local" in text


def test_fase6_9_script_blocks_real_cleanup() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")
    assert "Aprovado para limpeza real: nao" in text
    assert "Registros removidos: 0" in text
    assert "Banco alterado: nao" in text


def test_fase6_9_script_does_not_execute_destructive_sql() -> None:
    text = SCRIPT_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        r"\.execute(?:many)?\s*\([^)]*\b"
        r"(DELETE|UPDATE|DROP|ALTER|VACUUM|TRUNCATE|INSERT|REPLACE)\b",
        re.IGNORECASE | re.DOTALL,
    )

    assert pattern.search(text) is None
