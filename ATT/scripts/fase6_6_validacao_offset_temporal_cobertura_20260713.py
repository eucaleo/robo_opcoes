from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_6_validacao_offset_temporal_cobertura_20260713.md")

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

HISTORY_KEY_COLUMN = "codigo_opcao"
HISTORY_TIME_COLUMN = "captured_at"

CANDLES_KEY_COLUMN = "symbol"
CANDLES_TIME_COLUMN = "bucket_start"
CANDLES_INTERVAL_COLUMN = "interval_minutes"

OFFSET_HOURS_TO_TEST = list(range(-12, 13))


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
class OffsetEvaluation:
    interval_minutes: int
    offset_hours: int
    history_rows: int
    covered_rows: int
    uncovered_rows: int
    coverage_percent: float
    distinct_expected_pairs: int
    distinct_candle_pairs: int
    missing_expected_pairs: int
    extra_candle_pairs: int
    invalid_history_timestamps: int
    invalid_candle_timestamps: int


@dataclass(frozen=True)
class MissingSample:
    row_id: int
    symbol: str
    captured_raw: str
    offset_hours: int
    adjusted_captured_at: str
    expected_bucket: str


@dataclass(frozen=True)
class Result:
    history_count: int
    candles_count: int
    intervals: list[int]
    evaluations: list[OffsetEvaluation]
    best: OffsetEvaluation | None
    missing_samples: list[MissingSample]


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


def evaluate_offset(
    history_rows: list[HistoryRow],
    candle_rows: list[CandleRow],
    interval_minutes: int,
    offset_hours: int,
) -> OffsetEvaluation:
    interval_candles = [
        item
        for item in candle_rows
        if item.interval_minutes == interval_minutes
    ]

    candle_keys = {
        (item.symbol, item.bucket_start)
        for item in interval_candles
        if item.bucket_start is not None
    }

    expected_keys: set[tuple[str, datetime]] = set()
    covered_row_ids: set[int] = set()

    invalid_history_timestamps = 0

    for item in history_rows:
        if item.captured_at is None:
            invalid_history_timestamps += 1
            continue

        adjusted_time = item.captured_at + timedelta(hours=offset_hours)
        expected_bucket = floor_datetime_to_interval(adjusted_time, interval_minutes)
        expected_key = (item.symbol, expected_bucket)
        expected_keys.add(expected_key)

        if expected_key in candle_keys:
            covered_row_ids.add(item.row_id)

    history_count = len(history_rows)
    covered_rows = len(covered_row_ids)
    uncovered_rows = history_count - covered_rows
    coverage_percent = 0.0 if history_count == 0 else round((covered_rows / history_count) * 100.0, 4)

    invalid_candle_timestamps = sum(1 for item in interval_candles if item.bucket_start is None)

    return OffsetEvaluation(
        interval_minutes=interval_minutes,
        offset_hours=offset_hours,
        history_rows=history_count,
        covered_rows=covered_rows,
        uncovered_rows=uncovered_rows,
        coverage_percent=coverage_percent,
        distinct_expected_pairs=len(expected_keys),
        distinct_candle_pairs=len(candle_keys),
        missing_expected_pairs=len(expected_keys - candle_keys),
        extra_candle_pairs=len(candle_keys - expected_keys),
        invalid_history_timestamps=invalid_history_timestamps,
        invalid_candle_timestamps=invalid_candle_timestamps,
    )


def choose_best(evaluations: list[OffsetEvaluation]) -> OffsetEvaluation | None:
    if not evaluations:
        return None

    return sorted(
        evaluations,
        key=lambda item: (
            item.covered_rows,
            item.coverage_percent,
            -item.uncovered_rows,
            -abs(item.offset_hours),
            -item.missing_expected_pairs,
        ),
        reverse=True,
    )[0]


def build_missing_samples(
    history_rows: list[HistoryRow],
    candle_rows: list[CandleRow],
    best: OffsetEvaluation | None,
    limit: int = 25,
) -> list[MissingSample]:
    if best is None:
        return []

    candle_keys = {
        (item.symbol, item.bucket_start)
        for item in candle_rows
        if item.interval_minutes == best.interval_minutes and item.bucket_start is not None
    }

    samples: list[MissingSample] = []

    for item in history_rows:
        if item.captured_at is None:
            continue

        adjusted_time = item.captured_at + timedelta(hours=best.offset_hours)
        expected_bucket = floor_datetime_to_interval(adjusted_time, best.interval_minutes)

        if (item.symbol, expected_bucket) not in candle_keys:
            samples.append(
                MissingSample(
                    row_id=item.row_id,
                    symbol=item.symbol,
                    captured_raw=item.captured_raw,
                    offset_hours=best.offset_hours,
                    adjusted_captured_at=format_datetime(adjusted_time),
                    expected_bucket=format_datetime(expected_bucket),
                )
            )

        if len(samples) >= limit:
            break

    return samples


def evaluate(conn: sqlite3.Connection) -> Result:
    validate_required_columns(conn)

    history_rows = load_history_rows(conn)
    candle_rows = load_candle_rows(conn)

    intervals = sorted({
        item.interval_minutes
        for item in candle_rows
        if item.interval_minutes > 0
    })

    evaluations = [
        evaluate_offset(history_rows, candle_rows, interval, offset)
        for interval in intervals
        for offset in OFFSET_HOURS_TO_TEST
    ]

    best = choose_best(evaluations)

    return Result(
        history_count=len(history_rows),
        candles_count=len(candle_rows),
        intervals=intervals,
        evaluations=evaluations,
        best=best,
        missing_samples=build_missing_samples(history_rows, candle_rows, best),
    )


def render_top_evaluations(evaluations: list[OffsetEvaluation], limit: int = 20) -> list[str]:
    lines: list[str] = []

    if not evaluations:
        lines.append("Nenhuma avaliacao realizada.")
        lines.append("")
        return lines

    ordered = sorted(
        evaluations,
        key=lambda item: (
            item.covered_rows,
            item.coverage_percent,
            -item.uncovered_rows,
            -abs(item.offset_hours),
        ),
        reverse=True,
    )[:limit]

    lines.append("| Rank | Intervalo min | Offset horas aplicado ao historico | Cobertos | Nao cobertos | Cobertura pct | Pares esperados | Pares candles | Pares esperados ausentes | Pares candles extras |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

    for rank, item in enumerate(ordered, start=1):
        lines.append(
            "| "
            + f"{rank} | "
            + f"{item.interval_minutes} | "
            + f"{item.offset_hours} | "
            + f"{item.covered_rows} | "
            + f"{item.uncovered_rows} | "
            + f"{item.coverage_percent:.4f} | "
            + f"{item.distinct_expected_pairs} | "
            + f"{item.distinct_candle_pairs} | "
            + f"{item.missing_expected_pairs} | "
            + f"{item.extra_candle_pairs} |"
        )

    lines.append("")
    return lines


def render_missing_samples(samples: list[MissingSample]) -> list[str]:
    lines: list[str] = []

    if not samples:
        lines.append("Nenhuma lacuna encontrada para o melhor offset.")
        lines.append("")
        return lines

    lines.append("| ID historico | Simbolo | Captured raw | Offset horas | Captured ajustado | Bucket esperado |")
    lines.append("|---:|---|---|---:|---|---|")

    for item in samples:
        lines.append(
            "| "
            + f"{item.row_id} | "
            + f"`{item.symbol}` | "
            + f"`{item.captured_raw}` | "
            + f"{item.offset_hours} | "
            + f"`{item.adjusted_captured_at}` | "
            + f"`{item.expected_bucket}` |"
        )

    lines.append("")
    return lines


def decide_status(result: Result) -> str:
    best = result.best

    if best is None:
        return "NAO_CONCLUSIVO: nenhum intervalo ou offset foi avaliado."

    if best.uncovered_rows == 0 and best.invalid_history_timestamps == 0 and best.invalid_candle_timestamps == 0:
        return "OFFSET_TEMPORAL_CANDIDATO_VALIDADO: cobertura completa encontrada apos ajuste temporal; limpeza real segue bloqueada."

    if best.covered_rows > 0:
        return "OFFSET_TEMPORAL_CANDIDATO_PARCIAL: ajuste temporal melhora cobertura, mas ainda restam lacunas."

    return "NAO_CONCLUSIVO: nenhum offset temporal melhorou a cobertura."


def render_report(result: Result, now: datetime) -> str:
    lines: list[str] = []

    lines.append("# Fase 6.6 - Validacao de offset temporal de cobertura")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Validacao operacional nao destrutiva e somente leitura.")
    lines.append("")
    lines.append("Esta fase testa offsets horarios aplicados ao timestamp do historico bruto antes do calculo do bucket esperado.")
    lines.append("")
    lines.append("## Hipotese validada")
    lines.append("")
    lines.append("A Fase 6.5 mostrou cobertura completa por simbolo e por data, mas baixa cobertura exata de bucket.")
    lines.append("")
    lines.append("A divergencia observada sugere diferenca de fuso horario entre `captured_at` e `bucket_start`.")
    lines.append("")
    lines.append("## Regra avaliada")
    lines.append("")
    lines.append("```text")
    lines.append("captured_ajustado = history.captured_at + offset_horas")
    lines.append("bucket_esperado = floor(captured_ajustado, candles.interval_minutes)")
    lines.append("candles.symbol = history.codigo_opcao")
    lines.append("candles.bucket_start = bucket_esperado")
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
    lines.append(f"- Offsets testados em horas: {min(OFFSET_HOURS_TO_TEST)} ate {max(OFFSET_HOURS_TO_TEST)}")
    lines.append("")
    lines.append("## Ranking de offsets")
    lines.append("")
    lines.extend(render_top_evaluations(result.evaluations))
    lines.append("## Melhor offset candidato")
    lines.append("")

    if result.best is None:
        lines.append("- Nenhum offset candidato.")
    else:
        lines.append(f"- Intervalo: {result.best.interval_minutes} minutos")
        lines.append(f"- Offset aplicado ao historico: {result.best.offset_hours} horas")
        lines.append(f"- Linhas cobertas: {result.best.covered_rows}/{result.best.history_rows}")
        lines.append(f"- Linhas nao cobertas: {result.best.uncovered_rows}")
        lines.append(f"- Cobertura percentual: {result.best.coverage_percent:.4f}")
        lines.append(f"- Pares esperados ausentes: {result.best.missing_expected_pairs}")
        lines.append(f"- Pares candles extras: {result.best.extra_candle_pairs}")
        lines.append(f"- Datas invalidas no historico: {result.best.invalid_history_timestamps}")
        lines.append(f"- Datas invalidas nos candles: {result.best.invalid_candle_timestamps}")

    lines.append("")
    lines.append("## Amostras de lacunas apos melhor offset")
    lines.append("")
    lines.extend(render_missing_samples(result.missing_samples))
    lines.append("## Resultado")
    lines.append("")
    lines.append(f"- Status: {decide_status(result)}")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.6 apenas valida a hipotese de offset temporal.")
    lines.append("")
    lines.append("Mesmo com cobertura completa, a limpeza real permanece bloqueada ate fase posterior explicitamente aprovada.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate(conn)

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    print("Validacao de offset temporal concluida sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")

    if result.best is None:
        print("Melhor offset candidato: nenhum")
    else:
        print(f"Melhor intervalo candidato: {result.best.interval_minutes} minutos")
        print(f"Melhor offset candidato: {result.best.offset_hours} horas")
        print(f"Cobertura: {result.best.covered_rows}/{result.best.history_rows}")
        print(f"Nao cobertos: {result.best.uncovered_rows}")

    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
