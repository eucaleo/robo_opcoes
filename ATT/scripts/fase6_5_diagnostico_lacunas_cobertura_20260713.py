from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_5_diagnostico_lacunas_cobertura_20260713.md")

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
    captured_raw: str
    captured_at: datetime | None


@dataclass(frozen=True)
class CandleRow:
    symbol: str
    interval_minutes: int
    bucket_raw: str
    bucket_start: datetime | None


@dataclass(frozen=True)
class MissingSample:
    row_id: int
    symbol: str
    captured_raw: str
    expected_bucket: str
    nearest_bucket: str
    nearest_delta_minutes: str


@dataclass(frozen=True)
class IntervalDiagnostic:
    interval_minutes: int
    history_rows: int
    exact_covered_rows: int
    exact_uncovered_rows: int
    exact_coverage_percent: float
    symbol_only_covered_rows: int
    date_symbol_covered_rows: int
    nearest_within_interval_rows: int
    distinct_expected_pairs: int
    distinct_candle_pairs: int
    missing_expected_pairs: int
    extra_candle_pairs: int
    invalid_history_timestamps: int
    invalid_candle_timestamps: int
    distinct_history_symbols: int
    distinct_candle_symbols: int
    history_bucket_values: list[str]
    candle_bucket_values: list[str]
    missing_samples: list[MissingSample]


@dataclass(frozen=True)
class DiagnosticResult:
    history_count: int
    candles_count: int
    intervals: list[int]
    diagnostics: list[IntervalDiagnostic]
    best_interval: IntervalDiagnostic | None


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


def format_datetime(value: datetime | None) -> str:
    if value is None:
        return ""

    return value.isoformat(sep=" ", timespec="seconds")


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

    return [
        HistoryRow(
            row_id=int(row[0]),
            symbol=str(row[1]),
            captured_raw=str(row[2]),
            captured_at=parse_datetime(row[2]),
        )
        for row in rows
    ]


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

    return [
        CandleRow(
            symbol=str(row[0]),
            interval_minutes=int(row[1]),
            bucket_raw=str(row[2]),
            bucket_start=parse_datetime(row[2]),
        )
        for row in rows
    ]


def nearest_bucket(
    symbol: str,
    expected_bucket: datetime,
    candle_buckets_by_symbol: dict[str, list[datetime]],
) -> tuple[datetime | None, float | None]:
    candidates = candle_buckets_by_symbol.get(symbol, [])

    if not candidates:
        return None, None

    nearest = min(candidates, key=lambda item: abs((item - expected_bucket).total_seconds()))
    delta_minutes = abs((nearest - expected_bucket).total_seconds()) / 60.0

    return nearest, delta_minutes


def diagnose_interval(
    history_rows: list[HistoryRow],
    candle_rows: list[CandleRow],
    interval_minutes: int,
) -> IntervalDiagnostic:
    interval_candles = [item for item in candle_rows if item.interval_minutes == interval_minutes]

    candle_keys = {
        (item.symbol, item.bucket_start)
        for item in interval_candles
        if item.bucket_start is not None
    }

    candle_symbols = {item.symbol for item in interval_candles}

    candle_dates_by_symbol = {
        (item.symbol, item.bucket_start.date())
        for item in interval_candles
        if item.bucket_start is not None
    }

    candle_buckets_by_symbol: dict[str, list[datetime]] = {}

    for item in interval_candles:
        if item.bucket_start is not None:
            candle_buckets_by_symbol.setdefault(item.symbol, []).append(item.bucket_start)

    expected_pairs: set[tuple[str, datetime]] = set()
    exact_covered_ids: set[int] = set()
    symbol_only_ids: set[int] = set()
    date_symbol_ids: set[int] = set()
    nearest_within_interval_ids: set[int] = set()
    missing_samples: list[MissingSample] = []

    invalid_history_timestamps = 0

    for item in history_rows:
        if item.symbol in candle_symbols:
            symbol_only_ids.add(item.row_id)

        if item.captured_at is None:
            invalid_history_timestamps += 1
            continue

        expected_bucket = floor_datetime_to_interval(item.captured_at, interval_minutes)
        expected_key = (item.symbol, expected_bucket)
        expected_pairs.add(expected_key)

        if (item.symbol, item.captured_at.date()) in candle_dates_by_symbol:
            date_symbol_ids.add(item.row_id)

        nearest, delta_minutes = nearest_bucket(
            item.symbol,
            expected_bucket,
            candle_buckets_by_symbol,
        )

        if delta_minutes is not None and delta_minutes <= interval_minutes:
            nearest_within_interval_ids.add(item.row_id)

        if expected_key in candle_keys:
            exact_covered_ids.add(item.row_id)
        elif len(missing_samples) < 25:
            missing_samples.append(
                MissingSample(
                    row_id=item.row_id,
                    symbol=item.symbol,
                    captured_raw=item.captured_raw,
                    expected_bucket=format_datetime(expected_bucket),
                    nearest_bucket=format_datetime(nearest),
                    nearest_delta_minutes="" if delta_minutes is None else f"{delta_minutes:.4f}",
                )
            )

    exact_covered_rows = len(exact_covered_ids)
    history_count = len(history_rows)
    exact_uncovered_rows = history_count - exact_covered_rows
    exact_coverage_percent = 0.0 if history_count == 0 else round((exact_covered_rows / history_count) * 100.0, 4)

    missing_expected_pairs = len(expected_pairs - candle_keys)
    extra_candle_pairs = len(candle_keys - expected_pairs)

    history_bucket_values = sorted({
        format_datetime(bucket)
        for _, bucket in expected_pairs
    })

    candle_bucket_values = sorted({
        format_datetime(item.bucket_start)
        for item in interval_candles
        if item.bucket_start is not None
    })

    invalid_candle_timestamps = sum(1 for item in interval_candles if item.bucket_start is None)

    return IntervalDiagnostic(
        interval_minutes=interval_minutes,
        history_rows=history_count,
        exact_covered_rows=exact_covered_rows,
        exact_uncovered_rows=exact_uncovered_rows,
        exact_coverage_percent=exact_coverage_percent,
        symbol_only_covered_rows=len(symbol_only_ids),
        date_symbol_covered_rows=len(date_symbol_ids),
        nearest_within_interval_rows=len(nearest_within_interval_ids),
        distinct_expected_pairs=len(expected_pairs),
        distinct_candle_pairs=len(candle_keys),
        missing_expected_pairs=missing_expected_pairs,
        extra_candle_pairs=extra_candle_pairs,
        invalid_history_timestamps=invalid_history_timestamps,
        invalid_candle_timestamps=invalid_candle_timestamps,
        distinct_history_symbols=len({item.symbol for item in history_rows}),
        distinct_candle_symbols=len(candle_symbols),
        history_bucket_values=history_bucket_values,
        candle_bucket_values=candle_bucket_values,
        missing_samples=missing_samples,
    )


def choose_best_interval(diagnostics: list[IntervalDiagnostic]) -> IntervalDiagnostic | None:
    if not diagnostics:
        return None

    return sorted(
        diagnostics,
        key=lambda item: (
            item.exact_covered_rows,
            item.exact_coverage_percent,
            item.nearest_within_interval_rows,
            item.symbol_only_covered_rows,
            -item.exact_uncovered_rows,
        ),
        reverse=True,
    )[0]


def evaluate(conn: sqlite3.Connection) -> DiagnosticResult:
    validate_required_columns(conn)

    history_rows = load_history_rows(conn)
    candle_rows = load_candle_rows(conn)

    intervals = sorted({
        item.interval_minutes
        for item in candle_rows
        if item.interval_minutes > 0
    })

    diagnostics = [
        diagnose_interval(history_rows, candle_rows, interval)
        for interval in intervals
    ]

    return DiagnosticResult(
        history_count=len(history_rows),
        candles_count=len(candle_rows),
        intervals=intervals,
        diagnostics=diagnostics,
        best_interval=choose_best_interval(diagnostics),
    )


def render_summary_table(diagnostics: list[IntervalDiagnostic]) -> list[str]:
    lines: list[str] = []

    if not diagnostics:
        lines.append("Nenhum intervalo encontrado.")
        lines.append("")
        return lines

    lines.append("| Intervalo min | Historico | Cobertura exata | Nao cobertos | Cobertura pct | Cobertura por simbolo | Cobertura por data e simbolo | Proximos dentro do intervalo | Pares esperados | Pares candles | Pares esperados ausentes | Pares candles extras |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

    for item in diagnostics:
        lines.append(
            "| "
            + f"{item.interval_minutes} | "
            + f"{item.history_rows} | "
            + f"{item.exact_covered_rows} | "
            + f"{item.exact_uncovered_rows} | "
            + f"{item.exact_coverage_percent:.4f} | "
            + f"{item.symbol_only_covered_rows} | "
            + f"{item.date_symbol_covered_rows} | "
            + f"{item.nearest_within_interval_rows} | "
            + f"{item.distinct_expected_pairs} | "
            + f"{item.distinct_candle_pairs} | "
            + f"{item.missing_expected_pairs} | "
            + f"{item.extra_candle_pairs} |"
        )

    lines.append("")
    return lines


def render_bucket_values(title: str, values: list[str], limit: int = 30) -> list[str]:
    lines: list[str] = []

    lines.append(f"### {title}")
    lines.append("")

    if not values:
        lines.append("Nenhum valor.")
        lines.append("")
        return lines

    shown = values[:limit]

    for value in shown:
        lines.append(f"- `{value}`")

    if len(values) > limit:
        lines.append(f"- ... total de valores: {len(values)}")

    lines.append("")
    return lines


def render_missing_samples(samples: list[MissingSample]) -> list[str]:
    lines: list[str] = []

    if not samples:
        lines.append("Nenhuma amostra de lacuna encontrada.")
        lines.append("")
        return lines

    lines.append("| ID historico | Simbolo | Captured raw | Bucket esperado | Bucket candle mais proximo | Delta min |")
    lines.append("|---:|---|---|---|---|---:|")

    for item in samples:
        lines.append(
            "| "
            + f"{item.row_id} | "
            + f"`{item.symbol}` | "
            + f"`{item.captured_raw}` | "
            + f"`{item.expected_bucket}` | "
            + f"`{item.nearest_bucket}` | "
            + f"{item.nearest_delta_minutes} |"
        )

    lines.append("")
    return lines


def render_interval_details(diagnostics: list[IntervalDiagnostic]) -> list[str]:
    lines: list[str] = []

    for item in diagnostics:
        lines.append(f"## Detalhe do intervalo de {item.interval_minutes} minutos")
        lines.append("")
        lines.append(f"- Simbolos distintos no historico: {item.distinct_history_symbols}")
        lines.append(f"- Simbolos distintos nos candles do intervalo: {item.distinct_candle_symbols}")
        lines.append(f"- Datas invalidas no historico: {item.invalid_history_timestamps}")
        lines.append(f"- Datas invalidas nos candles: {item.invalid_candle_timestamps}")
        lines.append("")
        lines.extend(render_bucket_values("Buckets esperados a partir do historico", item.history_bucket_values))
        lines.extend(render_bucket_values("Buckets existentes nos candles", item.candle_bucket_values))
        lines.append("### Amostras de lacunas")
        lines.append("")
        lines.extend(render_missing_samples(item.missing_samples))

    return lines


def decide_status(result: DiagnosticResult) -> str:
    best = result.best_interval

    if best is None:
        return "NAO_CONCLUSIVO: nenhum intervalo foi encontrado para diagnostico."

    if best.exact_uncovered_rows == 0 and best.invalid_history_timestamps == 0:
        return "REGRA_CANDIDATA_VALIDADA: cobertura exata completa encontrada; limpeza real segue bloqueada."

    if best.symbol_only_covered_rows == best.history_rows and best.exact_uncovered_rows > 0:
        return "LACUNA_TEMPORAL_IDENTIFICADA: simbolos parecem cobertos, mas buckets temporais nao fecham."

    if best.date_symbol_covered_rows == best.history_rows and best.exact_uncovered_rows > 0:
        return "LACUNA_DE_BUCKET_IDENTIFICADA: datas e simbolos parecem cobertos, mas bucket exato nao fecha."

    return "NAO_CONCLUSIVO: lacunas permanecem sem causa unica determinada."


def render_report(result: DiagnosticResult, now: datetime) -> str:
    lines: list[str] = []

    lines.append("# Fase 6.5 - Diagnostico das lacunas de cobertura")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_5_DIAGNOSTICO_LACUNAS_COBERTURA_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Diagnostico operacional nao destrutivo e somente leitura.")
    lines.append("")
    lines.append("Esta fase investiga por que a regra explicita da Fase 6.4 cobriu apenas parte do historico bruto.")
    lines.append("")
    lines.append("## Regra base")
    lines.append("")
    lines.append("- Historico chave: `rtd_option_quotes_intraday_history.codigo_opcao`")
    lines.append("- Candles chave: `rtd_option_quotes_intraday_candles.symbol`")
    lines.append("- Historico tempo: `rtd_option_quotes_intraday_history.captured_at`")
    lines.append("- Candles bucket: `rtd_option_quotes_intraday_candles.bucket_start`")
    lines.append("- Candles intervalo: `rtd_option_quotes_intraday_candles.interval_minutes`")
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
    lines.append("## Resumo do diagnostico")
    lines.append("")
    lines.extend(render_summary_table(result.diagnostics))
    lines.append("## Melhor intervalo diagnostico")
    lines.append("")

    if result.best_interval is None:
        lines.append("- Nenhum intervalo candidato.")
    else:
        lines.append(f"- Intervalo: {result.best_interval.interval_minutes} minutos")
        lines.append(f"- Cobertura exata: {result.best_interval.exact_covered_rows}/{result.best_interval.history_rows}")
        lines.append(f"- Nao cobertos: {result.best_interval.exact_uncovered_rows}")
        lines.append(f"- Cobertura percentual: {result.best_interval.exact_coverage_percent:.4f}")
        lines.append(f"- Cobertura por simbolo: {result.best_interval.symbol_only_covered_rows}/{result.best_interval.history_rows}")
        lines.append(f"- Cobertura por data e simbolo: {result.best_interval.date_symbol_covered_rows}/{result.best_interval.history_rows}")
        lines.append(f"- Proximos dentro do intervalo: {result.best_interval.nearest_within_interval_rows}/{result.best_interval.history_rows}")

    lines.append("")
    lines.extend(render_interval_details(result.diagnostics))
    lines.append("## Resultado")
    lines.append("")
    lines.append(f"- Status: {decide_status(result)}")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.5 apenas diagnostica lacunas de cobertura.")
    lines.append("")
    lines.append("A limpeza real permanece bloqueada ate regra posterior explicitamente aprovada.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_5_DIAGNOSTICO_LACUNAS_COBERTURA_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate(conn)

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    print("Diagnostico de lacunas concluido sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")

    if result.best_interval is None:
        print("Melhor intervalo diagnostico: nenhum")
    else:
        print(f"Melhor intervalo diagnostico: {result.best_interval.interval_minutes} minutos")
        print(f"Cobertura exata: {result.best_interval.exact_covered_rows}/{result.best_interval.history_rows}")
        print(f"Cobertura por simbolo: {result.best_interval.symbol_only_covered_rows}/{result.best_interval.history_rows}")
        print(f"Nao cobertos: {result.best_interval.exact_uncovered_rows}")

    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
