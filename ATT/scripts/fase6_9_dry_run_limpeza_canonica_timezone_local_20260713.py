from __future__ import annotations

import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_9_dry_run_limpeza_canonica_timezone_local_20260713.md")

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
class HistoryCandidate:
    row_id: int
    symbol: str
    captured_raw: str
    source_tz_label: str
    captured_local: datetime | None
    expected_bucket_local: datetime | None
    eligible: bool
    reason: str


@dataclass(frozen=True)
class CandleRow:
    symbol: str
    interval_minutes: int
    bucket_raw: str
    bucket_local: datetime | None


@dataclass(frozen=True)
class Result:
    history_count: int
    candles_count: int
    interval_minutes: int | None
    candidates: list[HistoryCandidate]
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
    sign = "+" if total_seconds >= 0 else "-"
    abs_seconds = abs(total_seconds)
    hours = abs_seconds // 3600
    minutes = (abs_seconds % 3600) // 60

    return f"aware_UTC{sign}{hours:02d}:{minutes:02d}"


def parse_datetime_to_local_naive(value: object) -> datetime | None:
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


def load_history_raw(conn: sqlite3.Connection) -> list[tuple[int, str, str]]:
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
        (
            int(row[0]),
            "" if row[1] is None else str(row[1]),
            "" if row[2] is None else str(row[2]),
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
            symbol="" if row[0] is None else str(row[0]),
            interval_minutes=int(row[1]),
            bucket_raw="" if row[2] is None else str(row[2]),
            bucket_local=parse_datetime_to_local_naive(row[2]),
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


def build_candidates(
    history_raw: list[tuple[int, str, str]],
    candle_rows: list[CandleRow],
    interval_minutes: int | None,
) -> list[HistoryCandidate]:
    if interval_minutes is None:
        return [
            HistoryCandidate(
                row_id=row_id,
                symbol=symbol,
                captured_raw=captured_raw,
                source_tz_label=source_timezone_label(captured_raw),
                captured_local=parse_datetime_to_local_naive(captured_raw),
                expected_bucket_local=None,
                eligible=False,
                reason="SEM_INTERVALO_CANDLE_PRIMARIO",
            )
            for row_id, symbol, captured_raw in history_raw
        ]

    candle_keys = {
        (row.symbol, row.bucket_local)
        for row in candle_rows
        if row.interval_minutes == interval_minutes and row.bucket_local is not None
    }

    candidates: list[HistoryCandidate] = []

    for row_id, symbol, captured_raw in history_raw:
        captured_local = parse_datetime_to_local_naive(captured_raw)
        tz_label = source_timezone_label(captured_raw)

        if not symbol:
            candidates.append(
                HistoryCandidate(
                    row_id=row_id,
                    symbol=symbol,
                    captured_raw=captured_raw,
                    source_tz_label=tz_label,
                    captured_local=captured_local,
                    expected_bucket_local=None,
                    eligible=False,
                    reason="SIMBOLO_INVALIDO",
                )
            )
            continue

        if captured_local is None:
            candidates.append(
                HistoryCandidate(
                    row_id=row_id,
                    symbol=symbol,
                    captured_raw=captured_raw,
                    source_tz_label=tz_label,
                    captured_local=None,
                    expected_bucket_local=None,
                    eligible=False,
                    reason="CAPTURED_AT_INVALIDO",
                )
            )
            continue

        expected_bucket = floor_datetime_to_interval(captured_local, interval_minutes)
        covered = (symbol, expected_bucket) in candle_keys

        candidates.append(
            HistoryCandidate(
                row_id=row_id,
                symbol=symbol,
                captured_raw=captured_raw,
                source_tz_label=tz_label,
                captured_local=captured_local,
                expected_bucket_local=expected_bucket,
                eligible=covered,
                reason="COBERTO_POR_CANDLE_CANONICO_LOCAL" if covered else "SEM_CANDLE_CANONICO_LOCAL",
            )
        )

    return candidates


def evaluate(conn: sqlite3.Connection) -> Result:
    validate_required_columns(conn)

    history_raw = load_history_raw(conn)
    candle_rows = load_candle_rows(conn)
    interval_minutes = choose_primary_interval(candle_rows)
    candidates = build_candidates(history_raw, candle_rows, interval_minutes)

    return Result(
        history_count=len(history_raw),
        candles_count=len(candle_rows),
        interval_minutes=interval_minutes,
        candidates=candidates,
        invalid_history_timestamps=sum(
            1 for _, _, captured_raw in history_raw
            if parse_datetime_to_local_naive(captured_raw) is None
        ),
        invalid_candle_timestamps=sum(
            1 for row in candle_rows
            if row.bucket_local is None
        ),
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


def render_samples(candidates: list[HistoryCandidate], limit: int = 100) -> list[str]:
    lines: list[str] = []

    lines.append("## Amostras do dry-run")
    lines.append("")

    if not candidates:
        lines.append("Nenhuma linha avaliada.")
        lines.append("")
        return lines

    lines.append("| ID | Simbolo | Captured raw | Origem timezone | Captured local | Bucket local esperado | Elegivel | Motivo |")
    lines.append("|---:|---|---|---|---|---|---|---|")

    for row in candidates[:limit]:
        lines.append(
            "| "
            + f"{row.row_id} | "
            + f"`{row.symbol}` | "
            + f"`{row.captured_raw}` | "
            + f"`{row.source_tz_label}` | "
            + f"`{format_datetime(row.captured_local)}` | "
            + f"`{format_datetime(row.expected_bucket_local)}` | "
            + f"{'sim' if row.eligible else 'nao'} | "
            + f"`{row.reason}` |"
        )

    lines.append("")
    return lines


def decide_status(result: Result) -> str:
    total = len(result.candidates)
    eligible = sum(1 for row in result.candidates if row.eligible)
    blocked = total - eligible

    if total == 0:
        return "NAO_CONCLUSIVO: nenhuma linha avaliada."

    if eligible == total and result.invalid_history_timestamps == 0 and result.invalid_candle_timestamps == 0:
        return "DRY_RUN_CANONICO_VALIDADO: todas as linhas do historico bruto estao cobertas por candles pela regra local; limpeza real segue bloqueada."

    if eligible > 0 and blocked > 0:
        return "DRY_RUN_CANONICO_PARCIAL: parte das linhas esta coberta, mas ha bloqueios; limpeza real segue bloqueada."

    return "DRY_RUN_CANONICO_BLOQUEADO: nenhuma linha elegivel; limpeza real segue bloqueada."


def render_report(result: Result, now: datetime) -> str:
    total = len(result.candidates)
    eligible = sum(1 for row in result.candidates if row.eligible)
    blocked = total - eligible
    eligible_percent = 0.0 if total == 0 else round((eligible / total) * 100.0, 4)

    reason_counter = Counter(row.reason for row in result.candidates)
    tz_counter = Counter(row.source_tz_label for row in result.candidates)
    eligibility_counter = Counter("elegivel" if row.eligible else "bloqueado" for row in result.candidates)

    candidate_ids = [str(row.row_id) for row in result.candidates if row.eligible]
    blocked_ids = [str(row.row_id) for row in result.candidates if not row.eligible]

    lines: list[str] = []

    lines.append("# Fase 6.9 - Dry-run de limpeza com timezone local canonico")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Dry-run operacional, nao destrutivo e somente leitura.")
    lines.append("")
    lines.append("Esta fase simula quais linhas do historico bruto seriam elegiveis para limpeza por ja possuirem candle correspondente pela regra canonica local.")
    lines.append("")
    lines.append("## Regra canonica usada")
    lines.append("")
    lines.append("```text")
    lines.append("Timezone local operacional: America/Sao_Paulo")
    lines.append("history.captured_at com timezone -> converter para America/Sao_Paulo")
    lines.append("history.captured_at sem timezone -> assumir America/Sao_Paulo")
    lines.append("candles.bucket_start -> tratar como horario local operacional")
    lines.append("elegibilidade = existe candle com mesmo simbolo e mesmo bucket local")
    lines.append("```")
    lines.append("")
    lines.append("## Banco")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH.as_posix()}`")
    lines.append(f"- Existe: {'sim' if DB_PATH.exists() else 'nao'}")
    if DB_PATH.exists():
        lines.append(f"- Tamanho em bytes: {DB_PATH.stat().st_size}")
    lines.append("")
    lines.append("## Volumetria do dry-run")
    lines.append("")
    lines.append(f"- Linhas no historico bruto: {result.history_count}")
    lines.append(f"- Linhas em candles: {result.candles_count}")
    lines.append(f"- Intervalo primario avaliado: {result.interval_minutes if result.interval_minutes is not None else 'nenhum'} minutos")
    lines.append(f"- Linhas elegiveis por cobertura canonica local: {eligible}/{total}")
    lines.append(f"- Linhas bloqueadas: {blocked}")
    lines.append(f"- Percentual elegivel: {eligible_percent:.4f}")
    lines.append(f"- Datas invalidas no historico: {result.invalid_history_timestamps}")
    lines.append(f"- Datas invalidas nos candles: {result.invalid_candle_timestamps}")
    lines.append("")
    lines.extend(render_counter_table("Distribuicao por elegibilidade", eligibility_counter))
    lines.extend(render_counter_table("Distribuicao por motivo", reason_counter))
    lines.extend(render_counter_table("Distribuicao por origem de timezone em captured_at", tz_counter))
    lines.append("## IDs simulados")
    lines.append("")
    lines.append(f"- IDs elegiveis simulados: `{', '.join(candidate_ids) if candidate_ids else ''}`")
    lines.append(f"- IDs bloqueados: `{', '.join(blocked_ids) if blocked_ids else ''}`")
    lines.append("")
    lines.extend(render_samples(result.candidates))
    lines.append("## Resultado")
    lines.append("")
    lines.append(f"- Status: {decide_status(result)}")
    lines.append(f"- Linhas elegiveis por cobertura canonica local: {eligible}/{total}")
    lines.append(f"- Linhas bloqueadas: {blocked}")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.9 e apenas dry-run.")
    lines.append("")
    lines.append("Mesmo com cobertura completa, nenhuma remocao real fica autorizada por esta fase.")
    lines.append("")
    lines.append("A proxima fase podera criar o plano operacional de execucao controlada, com backup obrigatorio e comando separado de confirmacao.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate(conn)

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    total = len(result.candidates)
    eligible = sum(1 for row in result.candidates if row.eligible)
    blocked = total - eligible

    print("Dry-run canonico de limpeza concluido sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Timezone local operacional: {LOCAL_TZ_NAME}")
    print(f"Intervalo primario avaliado: {result.interval_minutes if result.interval_minutes is not None else 'nenhum'} minutos")
    print(f"Linhas elegiveis por cobertura canonica local: {eligible}/{total}")
    print(f"Linhas bloqueadas: {blocked}")
    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
