from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_plano_execucao_controlada_backup_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_manifesto_ids_elegiveis_20260713.json")

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
class Candidate:
    row_id: int
    symbol: str
    captured_raw: str
    captured_local: datetime | None
    expected_bucket_local: datetime | None
    eligible: bool
    reason: str


@dataclass(frozen=True)
class CandleRow:
    symbol: str
    interval_minutes: int
    bucket_local: datetime | None


@dataclass(frozen=True)
class Result:
    history_count: int
    candles_count: int
    interval_minutes: int | None
    candidates: list[Candidate]
    db_sha256: str
    db_size_bytes: int


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {db_path}")

    absolute_path = db_path.resolve().as_posix()
    uri = f"file:{absolute_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()

    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def normalize_iso_text(value: object) -> str:
    if value is None:
        return ""

    return str(value).strip().replace("Z", "+00:00")


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
            bucket_local=parse_datetime_to_local_naive(row[2]),
        )
        for row in rows
    ]


def choose_primary_interval(candle_rows: list[CandleRow]) -> int | None:
    counter = Counter(row.interval_minutes for row in candle_rows if row.interval_minutes > 0)

    if not counter:
        return None

    return sorted(counter.items(), key=lambda item: (item[1], -item[0]), reverse=True)[0][0]


def build_candidates(
    history_raw: list[tuple[int, str, str]],
    candle_rows: list[CandleRow],
    interval_minutes: int | None,
) -> list[Candidate]:
    if interval_minutes is None:
        return [
            Candidate(
                row_id=row_id,
                symbol=symbol,
                captured_raw=captured_raw,
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

    candidates: list[Candidate] = []

    for row_id, symbol, captured_raw in history_raw:
        captured_local = parse_datetime_to_local_naive(captured_raw)

        if not symbol:
            reason = "SIMBOLO_INVALIDO"
            expected_bucket = None
            eligible = False
        elif captured_local is None:
            reason = "CAPTURED_AT_INVALIDO"
            expected_bucket = None
            eligible = False
        else:
            expected_bucket = floor_datetime_to_interval(captured_local, interval_minutes)
            eligible = (symbol, expected_bucket) in candle_keys
            reason = "ELEGIVEL_BACKUP_OBRIGATORIO" if eligible else "BLOQUEADO_SEM_CANDLE_CANONICO_LOCAL"

        candidates.append(
            Candidate(
                row_id=row_id,
                symbol=symbol,
                captured_raw=captured_raw,
                captured_local=captured_local,
                expected_bucket_local=expected_bucket,
                eligible=eligible,
                reason=reason,
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
        db_sha256=sha256_file(DB_PATH),
        db_size_bytes=DB_PATH.stat().st_size,
    )


def build_manifest(result: Result, now: datetime) -> dict:
    eligible_candidates = [row for row in result.candidates if row.eligible]
    blocked_candidates = [row for row in result.candidates if not row.eligible]

    return {
        "phase": "6.10",
        "generated_at_utc": now.replace(microsecond=0).isoformat(),
        "database": {
            "path": DB_PATH.as_posix(),
            "sha256": result.db_sha256,
            "size_bytes": result.db_size_bytes,
        },
        "rule": {
            "timezone": LOCAL_TZ_NAME,
            "captured_at_aware": "converter_para_America_Sao_Paulo",
            "captured_at_naive": "assumir_America_Sao_Paulo",
            "bucket_start": "horario_local_operacional",
            "matching": "codigo_opcao_symbol_e_bucket_local",
        },
        "summary": {
            "history_count": result.history_count,
            "candles_count": result.candles_count,
            "interval_minutes": result.interval_minutes,
            "eligible_count": len(eligible_candidates),
            "blocked_count": len(blocked_candidates),
            "real_cleanup_approved": False,
            "backup_required_before_cleanup": True,
        },
        "eligible_ids": [row.row_id for row in eligible_candidates],
        "blocked_ids": [row.row_id for row in blocked_candidates],
        "eligible_rows": [
            {
                "id": row.row_id,
                "symbol": row.symbol,
                "captured_raw": row.captured_raw,
                "captured_local": format_datetime(row.captured_local),
                "expected_bucket_local": format_datetime(row.expected_bucket_local),
                "reason": row.reason,
            }
            for row in eligible_candidates
        ],
    }


def render_report(result: Result, now: datetime) -> str:
    total = len(result.candidates)
    eligible = sum(1 for row in result.candidates if row.eligible)
    blocked = total - eligible
    percent = 0.0 if total == 0 else round((eligible / total) * 100.0, 4)

    reason_counter = Counter(row.reason for row in result.candidates)

    eligible_ids = [str(row.row_id) for row in result.candidates if row.eligible]
    blocked_ids = [str(row.row_id) for row in result.candidates if not row.eligible]

    lines: list[str] = []

    lines.append("# Fase 6.10 - Plano de execucao controlada com backup")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_10_PLANO_EXECUCAO_CONTROLADA_BACKUP_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Plano operacional nao destrutivo, somente leitura, sem remocao de registros.")
    lines.append("")
    lines.append("## Banco de referencia")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH.as_posix()}`")
    lines.append(f"- Tamanho em bytes: {result.db_size_bytes}")
    lines.append(f"- SHA256: `{result.db_sha256}`")
    lines.append("")
    lines.append("## Regra canonica consolidada")
    lines.append("")
    lines.append("```text")
    lines.append("Timezone local operacional: America/Sao_Paulo")
    lines.append("captured_at com timezone -> converter para America/Sao_Paulo")
    lines.append("captured_at sem timezone -> assumir America/Sao_Paulo")
    lines.append("bucket_start -> horario local operacional")
    lines.append("elegibilidade -> mesmo simbolo e mesmo bucket local")
    lines.append("```")
    lines.append("")
    lines.append("## Volumetria planejada")
    lines.append("")
    lines.append(f"- Linhas no historico bruto: {result.history_count}")
    lines.append(f"- Linhas em candles: {result.candles_count}")
    lines.append(f"- Intervalo primario avaliado: {result.interval_minutes if result.interval_minutes is not None else 'nenhum'} minutos")
    lines.append(f"- IDs elegiveis no plano: {eligible}/{total}")
    lines.append(f"- IDs bloqueados no plano: {blocked}")
    lines.append(f"- Percentual elegivel: {percent:.4f}")
    lines.append("")
    lines.append("## Distribuicao por motivo")
    lines.append("")
    lines.append("| Motivo | Quantidade |")
    lines.append("|---|---:|")
    for key, count in sorted(reason_counter.items(), key=lambda item: str(item[0])):
        lines.append(f"| `{key}` | {count} |")
    lines.append("")
    lines.append("## Manifesto")
    lines.append("")
    lines.append(f"- Arquivo: `{MANIFEST_PATH.as_posix()}`")
    lines.append(f"- IDs elegiveis: `{', '.join(eligible_ids) if eligible_ids else ''}`")
    lines.append(f"- IDs bloqueados: `{', '.join(blocked_ids) if blocked_ids else ''}`")
    lines.append("")
    lines.append("## Plano obrigatorio antes de qualquer limpeza real")
    lines.append("")
    lines.append("1. Confirmar branch correta.")
    lines.append("2. Confirmar working tree limpo.")
    lines.append("3. Parar qualquer processo que escreva no banco.")
    lines.append("4. Criar backup fisico do arquivo `dados/app.db`.")
    lines.append("5. Calcular SHA256 do backup.")
    lines.append("6. Comparar SHA256 do banco original com o registrado neste plano.")
    lines.append("7. Executar validacao read-only imediatamente antes da limpeza.")
    lines.append("8. Executar limpeza real somente em fase posterior explicitamente aprovada.")
    lines.append("9. Validar contagens apos a limpeza.")
    lines.append("10. Manter backup ate fechamento da auditoria.")
    lines.append("")
    lines.append("## Resultado")
    lines.append("")
    lines.append("- Status: PLANO_CONTROLADO_GERADO_COM_BACKUP_OBRIGATORIO")
    lines.append(f"- IDs elegiveis no plano: {eligible}/{total}")
    lines.append(f"- IDs bloqueados no plano: {blocked}")
    lines.append("- Backup obrigatorio antes da limpeza real: sim")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("Esta fase nao executa limpeza real.")
    lines.append("")
    lines.append("A limpeza real permanece bloqueada ate uma fase posterior com confirmacao explicita.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_10_PLANO_EXECUCAO_CONTROLADA_BACKUP_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate(conn)

    manifest = build_manifest(result, now)

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    total = len(result.candidates)
    eligible = sum(1 for row in result.candidates if row.eligible)
    blocked = total - eligible

    print("Plano controlado de execucao gerado sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Manifesto gerado em: {MANIFEST_PATH.as_posix()}")
    print(f"SHA256 do banco: {result.db_sha256}")
    print(f"Timezone local operacional: {LOCAL_TZ_NAME}")
    print(f"IDs elegiveis no plano: {eligible}/{total}")
    print(f"IDs bloqueados no plano: {blocked}")
    print("Backup obrigatorio antes da limpeza real: sim")
    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
