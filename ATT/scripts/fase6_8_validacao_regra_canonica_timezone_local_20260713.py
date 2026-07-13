from __future__ import annotations

import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_8_validacao_regra_canonica_timezone_local_20260713.md")

LOCAL_TZ_NAME = "America/Sao_Paulo"
LOCAL_TZ = ZoneInfo(LOCAL_TZ_NAME)

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

HISTORY_ID_COLUMN = "id"
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
    captured_local: datetime | None
    source_tz_label: str


@dataclass(frozen=True)
class CandleRow:
    symbol: str
    interval_minutes: int
    bucket_raw: str
    bucket_local: datetime | None


@dataclass(frozen=True)
class CoverageRow:
    row_id: int
    symbol: str
    captured_raw: str
    source_tz_label: str
    captured_local: str
    expected_bucket_local: str
    covered: bool


@dataclass(frozen=True)
class Result:
    history_count: int
    candles_count: int
    interval_minutes: int | None
    coverage_rows: list[CoverageRow]
    invalid_history_timestamps: int
    invalid_candle_timestamps: int


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {db_path}")

    absolute_path = db_path.resolve().as_posix()
    uri = f"file:{absolute_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def normalize_iso_text(value: object) -> str:
    if value is None:
        return ""

    return str(value).strip().replace("Z", "+00:00")


def source_timezone_label(value: object) -> str:
    text = normalize_iso_text(value)

    if not text:
        return "vazio"

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return "invalido"

    if parsed.tzinfo is None:
        return "naive_assumido_local"

    offset = parsed.utcoffset()

    if offset is None:
        return "tzinfo_sem_offset"

    total_seconds = int(offset.total_seconds())
    hours = total_seconds // 3600
    minutes = abs(total_seconds % 3600) // 60

    return f"aware_UTC{hours:+03d}:{minutes:02d}"


def parse_captured_at_to_local_naive(value: object) -> datetime | None:
    text = normalize_iso_text(value)

    if not text:
        return None

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=None)

    return parsed.astimezone(LOCAL_TZ).replace(tzinfo=None)


def parse_bucket_start_as_local_naive(value: object) -> datetime | None:
    text = normalize_iso_text(value)

    if not text:
        return None

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=None)

    return parsed.astimezone(LOCAL_TZ).replace(tzinfo=None)


def floor_datetime_to_interval(value: datetime, interval_minutes: int) -> datetime:
    floored_minute = (value.minute // interval_minutes) * interval_minutes
    return value.replace(minute=floored_minute, second=0, microsecond=0)


def format_datetime(value: datetime | None) -> str:
    if value is None:
        return ""

    return value.isoformat(sep=" ", timespec="seconds")


def table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({quote_identifier(table_name)})").fetchall()
    return {str(row[1]) for row in rows}


def validate_required_columns(conn: sqlite3.Connection) -> None:
    history_columns = table_columns(conn, HISTORY_TABLE)
    candles_columns = table_columns(conn, CANDLES_TABLE)

    required_history = {HISTORY_ID_COLUMN, HISTORY_KEY_COLUMN, HISTORY_TIME_COLUMN}
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
            {quote_identifier(HISTORY_ID_COLUMN)},
            {quote_identifier(HISTORY_KEY_COLUMN)},
            {quote_identifier(HISTORY_TIME_COLUMN)}
        FROM {quote_identifier(HISTORY_TABLE)}
        ORDER BY {quote_identifier(HISTORY_ID_COLUMN)}
        """
    ).fetchall()

    return [
        HistoryRow(
            row_id=int(row[0]),
            symbol=str(row[1]),
            captured_raw="" if row[2] is None else str(row[2]),
            captured_local=parse_captured_at_to_local_naive(row[2]),
            source_tz_label=source_timezone_label(row[2]),
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
            bucket_raw="" if row[2] is None else str(row[2]),
            bucket_local=parse_bucket_start_as_local_naive(row[2]),
        )
        for row in rows
    ]


def choose_primary_interval(candle_rows: list[CandleRow]) -> int | None:
    counter = Counter(
        row.interval_minutes
        for row in candle_rows
        if row.interval_minutes > 0
    )

    if not counter:
        return None

    return sorted(counter.items(), key=lambda item: (item[1], -item[0]), reverse=True)[0][0]


def evaluate_coverage(
    history_rows: list[HistoryRow],
    candle_rows: list[CandleRow],
    interval_minutes: int | None,
) -> list[CoverageRow]:
    if interval_minutes is None:
        return []

    candle_keys = {
        (row.symbol, row.bucket_local)
        for row in candle_rows
        if row.interval_minutes == interval_minutes and row.bucket_local is not None
    }

    coverage_rows: list[CoverageRow] = []

    for row in history_rows:
        if row.captured_local is None:
            coverage_rows.append(
                CoverageRow(
                    row_id=row.row_id,
                    symbol=row.symbol,
                    captured_raw=row.captured_raw,
                    source_tz_label=row.source_tz_label,
                    captured_local="",
                    expected_bucket_local="",
                    covered=False,
                )
            )
            continue

        expected_bucket = floor_datetime_to_interval(row.captured_local, interval_minutes)
        covered = (row.symbol, expected_bucket) in candle_keys

        coverage_rows.append(
            CoverageRow(
                row_id=row.row_id,
                symbol=row.symbol,
                captured_raw=row.captured_raw,
                source_tz_label=row.source_tz_label,
                captured_local=format_datetime(row.captured_local),
                expected_bucket_local=format_datetime(expected_bucket),
                covered=covered,
            )
        )

    return coverage_rows


def evaluate(conn: sqlite3.Connection) -> Result:
    validate_required_columns(conn)

    history_rows = load_history_rows(conn)
    candle_rows = load_candle_rows(conn)
    interval_minutes = choose_primary_interval(candle_rows)
    coverage_rows = evaluate_coverage(history_rows, candle_rows, interval_minutes)

    return Result(
        history_count=len(history_rows),
        candles_count=len(candle_rows),
        interval_minutes=interval_minutes,
        coverage_rows=coverage_rows,
        invalid_history_timestamps=sum(1 for row in history_rows if row.captured_local is None),
        invalid_candle_timestamps=sum(1 for row in candle_rows if row.bucket_local is None),
    )


def render_counter_table(title: str, counter: Counter) -> list[str]:
    lines: list[str] = []

    lines.append(f"## {title}")
    lines.append("")

    if not counter:
        lines.append("Nenhum dado.")
        lines.append("")
        return lines

    lines.append("| Valor | Quantidade |")
    lines.append("|---|---:|")

    for key, count in sorted(counter.items(), key=lambda item: str(item[0])):
        lines.append(f"| `{key}` | {count} |")

    lines.append("")
    return lines


def render_samples(rows: list[CoverageRow], limit: int = 80) -> list[str]:
    lines: list[str] = []

    lines.append("## Amostras da cobertura canonica local")
    lines.append("")

    if not rows:
        lines.append("Nenhuma linha avaliada.")
        lines.append("")
        return lines

    lines.append("| ID | Simbolo | Captured raw | Origem timezone | Captured local | Bucket local esperado | Coberto |")
    lines.append("|---:|---|---|---|---|---|---|")

    for row in rows[:limit]:
        lines.append(
            "| "
            + f"{row.row_id} | "
            + f"`{row.symbol}` | "
            + f"`{row.captured_raw}` | "
            + f"`{row.source_tz_label}` | "
            + f"`{row.captured_local}` | "
            + f"`{row.expected_bucket_local}` | "
            + f"{'sim' if row.covered else 'nao'} |"
        )

    lines.append("")
    return lines


def decide_status(result: Result) -> str:
    total = len(result.coverage_rows)
    covered = sum(1 for row in result.coverage_rows if row.covered)

    if total == 0:
        return "NAO_CONCLUSIVO: nenhuma linha avaliada."

    if covered == total and result.invalid_history_timestamps == 0 and result.invalid_candle_timestamps == 0:
        return "REGRA_CANONICA_LOCAL_VALIDADA: cobertura completa usando normalizacao para America/Sao_Paulo; limpeza real segue bloqueada."

    if covered > 0:
        return "REGRA_CANONICA_LOCAL_PARCIAL: houve cobertura parcial; limpeza real segue bloqueada."

    return "NAO_CONCLUSIVO: regra canonica local nao encontrou cobertura."


def render_report(result: Result, now: datetime) -> str:
    total = len(result.coverage_rows)
    covered = sum(1 for row in result.coverage_rows if row.covered)
    uncovered = total - covered
    coverage_percent = 0.0 if total == 0 else round((covered / total) * 100.0, 4)

    source_tz_counter = Counter(row.source_tz_label for row in result.coverage_rows)
    covered_counter = Counter("coberto" if row.covered else "nao_coberto" for row in result.coverage_rows)

    lines: list[str] = []

    lines.append("# Fase 6.8 - Validacao da regra canonica de timezone local")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_8_VALIDACAO_REGRA_CANONICA_TIMEZONE_LOCAL_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Validacao operacional nao destrutiva e somente leitura.")
    lines.append("")
    lines.append("## Regra canonica validada")
    lines.append("")
    lines.append("```text")
    lines.append("Timezone local operacional: America/Sao_Paulo")
    lines.append("Se history.captured_at tem timezone: converter para America/Sao_Paulo.")
    lines.append("Se history.captured_at nao tem timezone: assumir que ja esta em America/Sao_Paulo.")
    lines.append("Tratar candles.bucket_start como horario local operacional.")
    lines.append("bucket_esperado = floor(captured_at_local, candles.interval_minutes)")
    lines.append("cobertura = candles.symbol = history.codigo_opcao AND candles.bucket_start_local = bucket_esperado")
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
    lines.append(f"- Intervalo primario avaliado: {result.interval_minutes if result.interval_minutes is not None else 'nenhum'} minutos")
    lines.append(f"- Cobertura canonica local: {covered}/{total}")
    lines.append(f"- Linhas nao cobertas: {uncovered}")
    lines.append(f"- Cobertura percentual: {coverage_percent:.4f}")
    lines.append(f"- Datas invalidas no historico: {result.invalid_history_timestamps}")
    lines.append(f"- Datas invalidas nos candles: {result.invalid_candle_timestamps}")
    lines.append("")
    lines.extend(render_counter_table("Distribuicao por origem de timezone em captured_at", source_tz_counter))
    lines.extend(render_counter_table("Distribuicao por cobertura", covered_counter))
    lines.extend(render_samples(result.coverage_rows))
    lines.append("## Resultado")
    lines.append("")
    lines.append(f"- Status: {decide_status(result)}")
    lines.append(f"- Cobertura canonica local: {covered}/{total}")
    lines.append(f"- Linhas nao cobertas: {uncovered}")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.8 valida a regra canonica de timezone local, mas nao autoriza limpeza real.")
    lines.append("")
    lines.append("A proxima fase podera atualizar o contrato de dry-run para usar esta normalizacao antes de qualquer execucao destrutiva.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_8_VALIDACAO_REGRA_CANONICA_TIMEZONE_LOCAL_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate(conn)

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    total = len(result.coverage_rows)
    covered = sum(1 for row in result.coverage_rows if row.covered)
    uncovered = total - covered

    print("Validacao da regra canonica de timezone local concluida sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Timezone local operacional: {LOCAL_TZ_NAME}")
    print(f"Intervalo primario avaliado: {result.interval_minutes if result.interval_minutes is not None else 'nenhum'} minutos")
    print(f"Cobertura canonica local: {covered}/{total}")
    print(f"Linhas nao cobertas: {uncovered}")
    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
