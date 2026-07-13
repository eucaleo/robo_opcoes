from __future__ import annotations

import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_7_diagnostico_coortes_temporais_cobertura_20260713.md")

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

HISTORY_ID_COLUMN = "id"
HISTORY_KEY_COLUMN = "codigo_opcao"
HISTORY_TIME_COLUMN = "captured_at"

CANDLES_KEY_COLUMN = "symbol"
CANDLES_TIME_COLUMN = "bucket_start"
CANDLES_INTERVAL_COLUMN = "interval_minutes"

OFFSETS_TO_TEST = list(range(-12, 13))


@dataclass(frozen=True)
class HistoryRow:
    row_id: int
    symbol: str
    captured_raw: str
    captured_at: datetime | None
    has_explicit_timezone: bool


@dataclass(frozen=True)
class CandleRow:
    symbol: str
    interval_minutes: int
    bucket_raw: str
    bucket_start: datetime | None


@dataclass(frozen=True)
class RowClassification:
    row_id: int
    symbol: str
    captured_raw: str
    has_explicit_timezone: bool
    interval_minutes: int
    matching_offsets: tuple[int, ...]
    chosen_offset: int | None
    chosen_bucket: str
    status: str


@dataclass(frozen=True)
class Result:
    history_count: int
    candles_count: int
    interval_minutes: int | None
    classifications: list[RowClassification]


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {db_path}")

    absolute_path = db_path.resolve().as_posix()
    uri = f"file:{absolute_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def has_explicit_timezone_marker(value: object) -> bool:
    if value is None:
        return False

    text = str(value).strip()

    if not text:
        return False

    if text.endswith("Z"):
        return True

    if len(text) >= 6 and (text[-6] in ["+", "-"]) and text[-3] == ":":
        return True

    return False


def parse_datetime_as_wall_clock(value: object) -> datetime | None:
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

    result: list[HistoryRow] = []

    for row in rows:
        captured_raw = "" if row[2] is None else str(row[2])

        result.append(
            HistoryRow(
                row_id=int(row[0]),
                symbol=str(row[1]),
                captured_raw=captured_raw,
                captured_at=parse_datetime_as_wall_clock(row[2]),
                has_explicit_timezone=has_explicit_timezone_marker(row[2]),
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

    return [
        CandleRow(
            symbol=str(row[0]),
            interval_minutes=int(row[1]),
            bucket_raw=str(row[2]),
            bucket_start=parse_datetime_as_wall_clock(row[2]),
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


def classify_rows(
    history_rows: list[HistoryRow],
    candle_rows: list[CandleRow],
    interval_minutes: int | None,
) -> list[RowClassification]:
    if interval_minutes is None:
        return []

    candle_keys = {
        (row.symbol, row.bucket_start)
        for row in candle_rows
        if row.interval_minutes == interval_minutes and row.bucket_start is not None
    }

    classifications: list[RowClassification] = []

    for row in history_rows:
        if row.captured_at is None:
            classifications.append(
                RowClassification(
                    row_id=row.row_id,
                    symbol=row.symbol,
                    captured_raw=row.captured_raw,
                    has_explicit_timezone=row.has_explicit_timezone,
                    interval_minutes=interval_minutes,
                    matching_offsets=tuple(),
                    chosen_offset=None,
                    chosen_bucket="",
                    status="DATA_INVALIDA",
                )
            )
            continue

        matches: list[int] = []
        bucket_by_offset: dict[int, datetime] = {}

        for offset in OFFSETS_TO_TEST:
            adjusted = row.captured_at + timedelta(hours=offset)
            expected_bucket = floor_datetime_to_interval(adjusted, interval_minutes)
            bucket_by_offset[offset] = expected_bucket

            if (row.symbol, expected_bucket) in candle_keys:
                matches.append(offset)

        chosen_offset: int | None = None

        if matches:
            chosen_offset = sorted(matches, key=lambda value: (abs(value), value))[0]
            status = "COBERTO"
            chosen_bucket = format_datetime(bucket_by_offset[chosen_offset])
        else:
            status = "NAO_COBERTO"
            chosen_bucket = ""

        classifications.append(
            RowClassification(
                row_id=row.row_id,
                symbol=row.symbol,
                captured_raw=row.captured_raw,
                has_explicit_timezone=row.has_explicit_timezone,
                interval_minutes=interval_minutes,
                matching_offsets=tuple(matches),
                chosen_offset=chosen_offset,
                chosen_bucket=chosen_bucket,
                status=status,
            )
        )

    return classifications


def evaluate(conn: sqlite3.Connection) -> Result:
    validate_required_columns(conn)

    history_rows = load_history_rows(conn)
    candle_rows = load_candle_rows(conn)
    interval_minutes = choose_primary_interval(candle_rows)
    classifications = classify_rows(history_rows, candle_rows, interval_minutes)

    return Result(
        history_count=len(history_rows),
        candles_count=len(candle_rows),
        interval_minutes=interval_minutes,
        classifications=classifications,
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

    for key, count in sorted(counter.items(), key=lambda item: (str(item[0]))):
        lines.append(f"| `{key}` | {count} |")

    lines.append("")
    return lines


def render_classification_samples(classifications: list[RowClassification], limit: int = 80) -> list[str]:
    lines: list[str] = []

    lines.append("## Amostras classificadas")
    lines.append("")

    if not classifications:
        lines.append("Nenhuma classificacao disponivel.")
        lines.append("")
        return lines

    lines.append("| ID | Simbolo | Captured raw | Tem timezone explicito | Offsets que cobrem | Offset escolhido | Bucket escolhido | Status |")
    lines.append("|---:|---|---|---|---|---:|---|---|")

    for row in classifications[:limit]:
        offsets = ", ".join(str(item) for item in row.matching_offsets) if row.matching_offsets else ""
        chosen = "" if row.chosen_offset is None else str(row.chosen_offset)

        lines.append(
            "| "
            + f"{row.row_id} | "
            + f"`{row.symbol}` | "
            + f"`{row.captured_raw}` | "
            + f"{'sim' if row.has_explicit_timezone else 'nao'} | "
            + f"`{offsets}` | "
            + f"{chosen} | "
            + f"`{row.chosen_bucket}` | "
            + f"{row.status} |"
        )

    lines.append("")
    return lines


def decide_status(result: Result) -> str:
    classifications = result.classifications

    if not classifications:
        return "NAO_CONCLUSIVO: nenhuma classificacao disponivel."

    covered = [row for row in classifications if row.status == "COBERTO"]
    uncovered = [row for row in classifications if row.status != "COBERTO"]

    offsets = Counter(row.chosen_offset for row in covered)
    non_null_offsets = [key for key in offsets if key is not None]

    if len(covered) == len(classifications) and len(non_null_offsets) > 1:
        return "COORTES_TEMPORAIS_MULTIPLAS_CONFIRMADAS: todas as linhas possuem cobertura com offsets distintos; limpeza real segue bloqueada."

    if len(covered) == len(classifications) and len(non_null_offsets) == 1:
        return "COORTE_TEMPORAL_UNICA_CONFIRMADA: todas as linhas possuem cobertura com um unico offset; limpeza real segue bloqueada."

    if covered and uncovered:
        return "COORTES_TEMPORAIS_PARCIAIS: ha linhas cobertas por offset e linhas ainda sem cobertura; limpeza real segue bloqueada."

    return "NAO_CONCLUSIVO: nenhuma linha foi coberta por offset."


def render_report(result: Result, now: datetime) -> str:
    classifications = result.classifications

    status_counter = Counter(row.status for row in classifications)
    offset_counter = Counter(
        row.chosen_offset
        for row in classifications
        if row.chosen_offset is not None
    )
    tz_counter = Counter(
        "com timezone explicito" if row.has_explicit_timezone else "sem timezone explicito"
        for row in classifications
    )
    offset_by_tz_counter = Counter(
        (
            "com timezone explicito" if row.has_explicit_timezone else "sem timezone explicito",
            row.chosen_offset,
        )
        for row in classifications
        if row.chosen_offset is not None
    )

    covered_count = status_counter.get("COBERTO", 0)
    uncovered_count = len(classifications) - covered_count
    coverage_percent = 0.0 if not classifications else round((covered_count / len(classifications)) * 100.0, 4)

    lines: list[str] = []

    lines.append("# Fase 6.7 - Diagnostico de coortes temporais de cobertura")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Diagnostico operacional nao destrutivo e somente leitura.")
    lines.append("")
    lines.append("Esta fase classifica cada linha do historico pelo offset horario que permite encontrar candle correspondente.")
    lines.append("")
    lines.append("## Objetivo")
    lines.append("")
    lines.append("Verificar se existem coortes temporais distintas, por exemplo:")
    lines.append("")
    lines.append("- linhas que exigem offset `-3h`;")
    lines.append("- linhas que exigem offset `0h`;")
    lines.append("- linhas com timezone explicito em `captured_at`;")
    lines.append("- linhas sem timezone explicito em `captured_at`.")
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
    lines.append(f"- Linhas cobertas por algum offset: {covered_count}/{len(classifications)}")
    lines.append(f"- Linhas nao cobertas por nenhum offset: {uncovered_count}")
    lines.append(f"- Cobertura por coortes: {coverage_percent:.4f}")
    lines.append("")
    lines.extend(render_counter_table("Distribuicao por status", status_counter))
    lines.extend(render_counter_table("Distribuicao por offset escolhido", offset_counter))
    lines.extend(render_counter_table("Distribuicao por presenca de timezone explicito", tz_counter))
    lines.append("## Distribuicao por timezone explicito e offset")
    lines.append("")

    if offset_by_tz_counter:
        lines.append("| Timezone explicito | Offset escolhido | Quantidade |")
        lines.append("|---|---:|---:|")

        for key, count in sorted(offset_by_tz_counter.items(), key=lambda item: (str(item[0][0]), item[0][1])):
            tz_label, offset = key
            lines.append(f"| `{tz_label}` | {offset} | {count} |")

        lines.append("")
    else:
        lines.append("Nenhum offset escolhido.")
        lines.append("")

    lines.extend(render_classification_samples(classifications))
    lines.append("## Resultado")
    lines.append("")
    lines.append(f"- Status: {decide_status(result)}")
    lines.append(f"- Linhas cobertas por algum offset: {covered_count}/{len(classifications)}")
    lines.append(f"- Linhas nao cobertas por nenhum offset: {uncovered_count}")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.7 apenas diagnostica coortes temporais.")
    lines.append("")
    lines.append("Nenhuma regra destrutiva e nenhuma limpeza real ficam autorizadas por esta fase.")
    lines.append("")
    lines.append("Uma fase posterior podera propor regra normalizada de cobertura por coorte, ainda em modo dry-run.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate(conn)

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    classifications = result.classifications
    covered_count = sum(1 for row in classifications if row.status == "COBERTO")
    uncovered_count = len(classifications) - covered_count
    offset_counter = Counter(
        row.chosen_offset
        for row in classifications
        if row.chosen_offset is not None
    )

    print("Diagnostico de coortes temporais concluido sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Intervalo primario avaliado: {result.interval_minutes if result.interval_minutes is not None else 'nenhum'} minutos")
    print(f"Linhas cobertas por algum offset: {covered_count}/{len(classifications)}")
    print(f"Linhas nao cobertas por nenhum offset: {uncovered_count}")
    print("Distribuicao por offset escolhido:")

    for offset, count in sorted(offset_counter.items(), key=lambda item: item[0]):
        print(f"  offset {offset}: {count}")

    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
