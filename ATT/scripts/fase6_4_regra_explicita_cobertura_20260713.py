from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_4_regra_explicita_cobertura_20260713.md")

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

HISTORY_KEY_COLUMN = "codigo_opcao"
HISTORY_TIME_COLUMN = "captured_at"

CANDLES_KEY_COLUMN = "symbol"
CANDLES_TIME_COLUMN = "bucket_start"
CANDLES_INTERVAL_COLUMN = "interval_minutes"


@dataclass(frozen=True)
class HistoryRow:
    row_id: int
    symbol: str
    captured_at_raw: str
    captured_at: datetime | None


@dataclass(frozen=True)
class CandleRow:
    symbol: str
    interval_minutes: int
    bucket_start_raw: str
    bucket_start: datetime | None


@dataclass(frozen=True)
class IntervalCoverage:
    interval_minutes: int
    history_rows: int
    covered_rows: int
    uncovered_rows: int
    coverage_percent: float
    distinct_history_symbols: int
    distinct_covered_symbols: int
    distinct_uncovered_symbols: int
    invalid_history_timestamps: int
    invalid_candle_timestamps: int


@dataclass(frozen=True)
class EvaluationResult:
    history_count: int
    candles_count: int
    intervals: list[int]
    interval_results: list[IntervalCoverage]
    best_interval: IntervalCoverage | None
    real_cleanup_approved: bool


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {db_path}")

    absolute_path = db_path.resolve().as_posix()
    uri = f"file:{absolute_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def parse_datetime(value: object) -> datetime | None:
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    candidates = [
        text,
        text.replace("Z", "+00:00"),
        text.replace("T", " "),
        text.replace("T", " ").replace("Z", "+00:00"),
    ]

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    ]

    for candidate in candidates:
        try:
            parsed = datetime.fromisoformat(candidate)
            return parsed.replace(tzinfo=None)
        except ValueError:
            pass

    normalized = text.replace("T", " ").replace("Z", "")

    for fmt in formats:
        try:
            parsed = datetime.strptime(normalized, fmt)
            return parsed.replace(tzinfo=None)
        except ValueError:
            pass

    return None


def floor_datetime_to_interval(value: datetime, interval_minutes: int) -> datetime:
    floored_minute = (value.minute // interval_minutes) * interval_minutes
    return value.replace(minute=floored_minute, second=0, microsecond=0)


def table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({quote_identifier(table_name)})").fetchall()
    return {str(row[1]) for row in rows}


def validate_required_columns(conn: sqlite3.Connection) -> None:
    history_columns = table_columns(conn, HISTORY_TABLE)
    candles_columns = table_columns(conn, CANDLES_TABLE)

    required_history = {HISTORY_KEY_COLUMN, HISTORY_TIME_COLUMN}
    required_candles = {CANDLES_KEY_COLUMN, CANDLES_TIME_COLUMN, CANDLES_INTERVAL_COLUMN}

    missing_history = sorted(required_history - history_columns)
    missing_candles = sorted(required_candles - candles_columns)

    if missing_history:
        raise RuntimeError(f"Colunas ausentes no historico: {missing_history}")

    if missing_candles:
        raise RuntimeError(f"Colunas ausentes nos candles: {missing_candles}")


def load_history_rows(conn: sqlite3.Connection) -> list[HistoryRow]:
    rows = conn.execute(
        f"""
        SELECT
            {quote_identifier("id")},
            {quote_identifier(HISTORY_KEY_COLUMN)},
            {quote_identifier(HISTORY_TIME_COLUMN)}
        FROM {quote_identifier(HISTORY_TABLE)}
        ORDER BY {quote_identifier("id")}
        """
    ).fetchall()

    result: list[HistoryRow] = []

    for row_id, symbol, captured_at in rows:
        result.append(
            HistoryRow(
                row_id=int(row_id),
                symbol=str(symbol),
                captured_at_raw=str(captured_at),
                captured_at=parse_datetime(captured_at),
            )
        )

    return result


def load_candle_rows(conn: sqlite3.Connection) -> list[CandleRow]:
    rows = conn.execute(
        f"""
        SELECT
            {quote_identifier(CANDLES_KEY_COLUMN)},
            {quote_identifier(CANDLES_INTERVAL_COLUMN)},
            {quote_identifier(CANDLES_TIME_COLUMN)}
        FROM {quote_identifier(CANDLES_TABLE)}
        ORDER BY
            {quote_identifier(CANDLES_INTERVAL_COLUMN)},
            {quote_identifier(CANDLES_KEY_COLUMN)},
            {quote_identifier(CANDLES_TIME_COLUMN)}
        """
    ).fetchall()

    result: list[CandleRow] = []

    for symbol, interval_minutes, bucket_start in rows:
        result.append(
            CandleRow(
                symbol=str(symbol),
                interval_minutes=int(interval_minutes),
                bucket_start_raw=str(bucket_start),
                bucket_start=parse_datetime(bucket_start),
            )
        )

    return result


def available_intervals(candles: Iterable[CandleRow]) -> list[int]:
    return sorted({item.interval_minutes for item in candles if item.interval_minutes > 0})


def evaluate_interval(
    history_rows: list[HistoryRow],
    candle_rows: list[CandleRow],
    interval_minutes: int,
) -> IntervalCoverage:
    candle_keys = {
        (item.symbol, item.bucket_start)
        for item in candle_rows
        if item.interval_minutes == interval_minutes and item.bucket_start is not None
    }

    invalid_history_timestamps = sum(1 for item in history_rows if item.captured_at is None)
    invalid_candle_timestamps = sum(
        1
        for item in candle_rows
        if item.interval_minutes == interval_minutes and item.bucket_start is None
    )

    covered_row_ids: set[int] = set()
    uncovered_symbols: set[str] = set()
    covered_symbols: set[str] = set()

    for item in history_rows:
        if item.captured_at is None:
            uncovered_symbols.add(item.symbol)
            continue

        expected_bucket = floor_datetime_to_interval(item.captured_at, interval_minutes)
        expected_key = (item.symbol, expected_bucket)

        if expected_key in candle_keys:
            covered_row_ids.add(item.row_id)
            covered_symbols.add(item.symbol)
        else:
            uncovered_symbols.add(item.symbol)

    history_count = len(history_rows)
    covered_count = len(covered_row_ids)
    uncovered_count = history_count - covered_count
    coverage_percent = 0.0 if history_count == 0 else round((covered_count / history_count) * 100.0, 4)

    return IntervalCoverage(
        interval_minutes=interval_minutes,
        history_rows=history_count,
        covered_rows=covered_count,
        uncovered_rows=uncovered_count,
        coverage_percent=coverage_percent,
        distinct_history_symbols=len({item.symbol for item in history_rows}),
        distinct_covered_symbols=len(covered_symbols),
        distinct_uncovered_symbols=len(uncovered_symbols),
        invalid_history_timestamps=invalid_history_timestamps,
        invalid_candle_timestamps=invalid_candle_timestamps,
    )


def choose_best_interval(results: list[IntervalCoverage]) -> IntervalCoverage | None:
    if not results:
        return None

    return sorted(
        results,
        key=lambda item: (
            item.covered_rows,
            item.coverage_percent,
            -item.uncovered_rows,
            -item.invalid_history_timestamps,
            -item.invalid_candle_timestamps,
        ),
        reverse=True,
    )[0]


def evaluate(conn: sqlite3.Connection) -> EvaluationResult:
    validate_required_columns(conn)

    history_rows = load_history_rows(conn)
    candle_rows = load_candle_rows(conn)
    intervals = available_intervals(candle_rows)

    interval_results = [
        evaluate_interval(history_rows, candle_rows, interval)
        for interval in intervals
    ]

    best_interval = choose_best_interval(interval_results)

    return EvaluationResult(
        history_count=len(history_rows),
        candles_count=len(candle_rows),
        intervals=intervals,
        interval_results=interval_results,
        best_interval=best_interval,
        real_cleanup_approved=False,
    )


def render_interval_table(results: list[IntervalCoverage]) -> list[str]:
    lines: list[str] = []

    if not results:
        lines.append("Nenhum intervalo de candle foi encontrado.")
        lines.append("")
        return lines

    lines.append("| Intervalo min | Historico | Cobertos | Nao cobertos | Cobertura pct | Simbolos historico | Simbolos cobertos | Simbolos nao cobertos | Datas invalidas historico | Datas invalidas candles |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

    for item in results:
        lines.append(
            "| "
            + f"{item.interval_minutes} | "
            + f"{item.history_rows} | "
            + f"{item.covered_rows} | "
            + f"{item.uncovered_rows} | "
            + f"{item.coverage_percent:.4f} | "
            + f"{item.distinct_history_symbols} | "
            + f"{item.distinct_covered_symbols} | "
            + f"{item.distinct_uncovered_symbols} | "
            + f"{item.invalid_history_timestamps} | "
            + f"{item.invalid_candle_timestamps} |"
        )

    lines.append("")
    return lines


def render_report(result: EvaluationResult, now: datetime) -> str:
    lines: list[str] = []

    lines.append("# Fase 6.4 - Regra explicita de cobertura")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Validacao operacional nao destrutiva e somente leitura.")
    lines.append("")
    lines.append("Esta fase transforma o mapeamento da Fase 6.3 em uma regra explicita de cobertura.")
    lines.append("")
    lines.append("## Regra explicita avaliada")
    lines.append("")
    lines.append("- Chave do historico: `rtd_option_quotes_intraday_history.codigo_opcao`")
    lines.append("- Chave dos candles: `rtd_option_quotes_intraday_candles.symbol`")
    lines.append("- Tempo do historico: `rtd_option_quotes_intraday_history.captured_at`")
    lines.append("- Bucket dos candles: `rtd_option_quotes_intraday_candles.bucket_start`")
    lines.append("- Intervalo dos candles: `rtd_option_quotes_intraday_candles.interval_minutes`")
    lines.append("")
    lines.append("Uma linha do historico e considerada coberta quando existe candle com:")
    lines.append("")
    lines.append("```text")
    lines.append("candles.symbol = history.codigo_opcao")
    lines.append("candles.interval_minutes = intervalo avaliado")
    lines.append("candles.bucket_start = floor(history.captured_at, intervalo avaliado)")
    lines.append("```")
    lines.append("")
    lines.append("## Banco")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH.as_posix()}`")
    lines.append(f"- Existe: {'sim' if DB_PATH.exists() else 'nao'}")
    if DB_PATH.exists():
        lines.append(f"- Tamanho em bytes: {DB_PATH.stat().st_size}")
    lines.append("")
    lines.append("## Volumetria")
    lines.append("")
    lines.append(f"- Linhas no historico bruto: {result.history_count}")
    lines.append(f"- Linhas em candles: {result.candles_count}")
    lines.append(f"- Intervalos encontrados: {', '.join(str(item) for item in result.intervals) if result.intervals else 'nenhum'}")
    lines.append("")
    lines.append("## Cobertura por intervalo")
    lines.append("")
    lines.extend(render_interval_table(result.interval_results))
    lines.append("## Melhor intervalo candidato")
    lines.append("")

    if result.best_interval is None:
        lines.append("- Nenhum intervalo candidato identificado.")
    else:
        lines.append(f"- Intervalo: {result.best_interval.interval_minutes} minutos")
        lines.append(f"- Linhas cobertas: {result.best_interval.covered_rows}")
        lines.append(f"- Linhas nao cobertas: {result.best_interval.uncovered_rows}")
        lines.append(f"- Cobertura percentual: {result.best_interval.coverage_percent:.4f}")

    lines.append("")
    lines.append("## Resultado")
    lines.append("")

    if result.best_interval is None:
        status = "NAO_CONCLUSIVO: nenhum intervalo de candle foi encontrado."
    elif result.best_interval.uncovered_rows == 0 and result.best_interval.invalid_history_timestamps == 0:
        status = "REGRA_CANDIDATA_VALIDADA: cobertura completa encontrada para o melhor intervalo; limpeza real segue bloqueada."
    else:
        status = "NAO_CONCLUSIVO: regra candidata ainda apresenta linhas nao cobertas ou datas invalidas."

    lines.append(f"- Status: {status}")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.4 define e avalia uma regra explicita de cobertura, mas nao autoriza limpeza real.")
    lines.append("")
    lines.append("Qualquer remocao futura permanece bloqueada ate fase posterior com aprovacao explicita.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate(conn)

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    print("Regra explicita de cobertura avaliada sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")

    if result.best_interval is None:
        print("Melhor intervalo candidato: nenhum")
    else:
        print(f"Melhor intervalo candidato: {result.best_interval.interval_minutes} minutos")
        print(f"Cobertura: {result.best_interval.covered_rows}/{result.best_interval.history_rows}")
        print(f"Nao cobertos: {result.best_interval.uncovered_rows}")

    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
