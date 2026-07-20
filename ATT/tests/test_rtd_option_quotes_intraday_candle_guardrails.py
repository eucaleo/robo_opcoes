from pathlib import Path


def test_guardrails_fase4():
    files = [
        Path("repositories/rtd_option_quotes_intraday_candle_repository.py"),
        Path("services/rtd_option_quotes_intraday_candle_service.py"),
        Path("scripts/rtd_option_quotes_intraday_build_candles.py"),
        Path("ATT/tests/test_rtd_option_quotes_intraday_candle_repository.py"),
        Path("ATT/tests/test_rtd_option_quotes_intraday_candle_service.py"),
        Path("ATT/tests/test_rtd_option_quotes_intraday_build_candles_command.py"),
        Path("ATT/tests/test_rtd_option_quotes_intraday_candle_guardrails.py"),
        # Documento histórico removido junto com artefatos obsoletos da frente RTD.
    ]

    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in files
    )
    lowered = text.lower()

    forbidden = [
        chr(96),
        "while " + "true",
        "sub" + "process",
        "po" + "pen",
        "win32" + "com",
        "xl" + "wings",
        "." + "work" + "books",
        "." + "sheets",
    ]

    result = {
        f"item_{index}": item not in lowered and item not in text
        for index, item in enumerate(forbidden)
    }

    assert all(result.values()), f"Guardrails falharam: {result}"
