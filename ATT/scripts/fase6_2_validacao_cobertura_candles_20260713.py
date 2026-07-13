from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_2_validacao_cobertura_candles_20260713.md")

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

KEY_CANDIDATES = [
    "ticker",
    "symbol",
    "option_symbol",
    "asset",
    "code",
    "contract",
    "instrument",
    "underlying",
]

TIME_CANDIDATES = [
    "captured_at",
    "timestamp",
    "created_at",
    "updated_at",
    "candle_start",
    "candle_end",
    "start_at",
    "end_at",
    "bucket_start",
    "bucket_end",
]


@dataclass(frozen=True)
class TableProfile:
    table_name: str
    exists: bool
    row_count: int
    columns: list[str]
    key_column: str | None
    time_column: str | None
    min_time: str | None
    max_time: str | None
    distinct_keys: int | None


@dataclass(frozen=True)
class CoverageResult:
    history_profile: TableProfile
    candles_profile: TableProfile
    comparable_by_key: bool
    history_keys_without_candles: int | None
    candles_keys_without_history: int | None
    coverage_status: str
    real_cleanup_approved: bool


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco não encontrado: {db_path}")

    absolute_path = db_path.resolve().as_posix()
    uri = f"file:{absolute_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type IN ('table', 'view')
          AND name = ?
        LIMIT 1
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({quote_identifier(table_name)})").fetchall()
    return [str(row[1]) for row in rows]


def count_rows(conn: sqlite3.Connection, table_name: str) -> int:
    row = conn.execute(
        f"SELECT COUNT(*) FROM {quote_identifier(table_name)}"
    ).fetchone()
    return int(row[0] or 0)


def choose_column(columns: list[str], candidates: list[str]) -> str | None:
    normalized = {column.lower(): column for column in columns}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    return None


def min_max_time(
    conn: sqlite3.Connection,
    table_name: str,
    time_column: str | None,
) -> tuple[str | None, str | None]:
    if not time_column:
        return None, None

    row = conn.execute(
        f"""
        SELECT
            MIN({quote_identifier(time_column)}),
            MAX({quote_identifier(time_column)})
        FROM {quote_identifier(table_name)}
        WHERE {quote_identifier(time_column)} IS NOT NULL
        """
    ).fetchone()

    return (
        None if row[0] is None else str(row[0]),
        None if row[1] is None else str(row[1]),
    )


def count_distinct_keys(
    conn: sqlite3.Connection,
    table_name: str,
    key_column: str | None,
) -> int | None:
    if not key_column:
        return None

    row = conn.execute(
        f"""
        SELECT COUNT(DISTINCT {quote_identifier(key_column)})
        FROM {quote_identifier(table_name)}
        WHERE {quote_identifier(key_column)} IS NOT NULL
        """
    ).fetchone()

    return int(row[0] or 0)


def profile_table(conn: sqlite3.Connection, table_name: str) -> TableProfile:
    if not table_exists(conn, table_name):
        return TableProfile(
            table_name=table_name,
            exists=False,
            row_count=0,
            columns=[],
            key_column=None,
            time_column=None,
            min_time=None,
            max_time=None,
            distinct_keys=None,
        )

    columns = table_columns(conn, table_name)
    key_column = choose_column(columns, KEY_CANDIDATES)
    time_column = choose_column(columns, TIME_CANDIDATES)
    row_count = count_rows(conn, table_name)
    min_time, max_time = min_max_time(conn, table_name, time_column)
    distinct_keys = count_distinct_keys(conn, table_name, key_column)

    return TableProfile(
        table_name=table_name,
        exists=True,
        row_count=row_count,
        columns=columns,
        key_column=key_column,
        time_column=time_column,
        min_time=min_time,
        max_time=max_time,
        distinct_keys=distinct_keys,
    )


def count_keys_left_without_right(
    conn: sqlite3.Connection,
    left_table: str,
    left_key: str,
    right_table: str,
    right_key: str,
) -> int:
    row = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM (
            SELECT DISTINCT {quote_identifier(left_key)} AS item_key
            FROM {quote_identifier(left_table)}
            WHERE {quote_identifier(left_key)} IS NOT NULL

            EXCEPT

            SELECT DISTINCT {quote_identifier(right_key)} AS item_key
            FROM {quote_identifier(right_table)}
            WHERE {quote_identifier(right_key)} IS NOT NULL
        )
        """
    ).fetchone()

    return int(row[0] or 0)


def evaluate_coverage(conn: sqlite3.Connection) -> CoverageResult:
    history_profile = profile_table(conn, HISTORY_TABLE)
    candles_profile = profile_table(conn, CANDLES_TABLE)

    comparable_by_key = bool(
        history_profile.exists
        and candles_profile.exists
        and history_profile.key_column
        and candles_profile.key_column
    )

    history_keys_without_candles: int | None = None
    candles_keys_without_history: int | None = None

    if comparable_by_key:
        history_keys_without_candles = count_keys_left_without_right(
            conn,
            HISTORY_TABLE,
            history_profile.key_column or "",
            CANDLES_TABLE,
            candles_profile.key_column or "",
        )
        candles_keys_without_history = count_keys_left_without_right(
            conn,
            CANDLES_TABLE,
            candles_profile.key_column or "",
            HISTORY_TABLE,
            history_profile.key_column or "",
        )

    if not history_profile.exists:
        coverage_status = "BLOQUEADO: tabela de histórico intraday bruto ausente."
    elif not candles_profile.exists:
        coverage_status = "BLOQUEADO: tabela de candles consolidados ausente."
    elif history_profile.row_count > 0 and candles_profile.row_count == 0:
        coverage_status = "BLOQUEADO: há histórico bruto, mas não há candles consolidados."
    elif not history_profile.time_column:
        coverage_status = "NAO_CONCLUSIVO: histórico bruto sem coluna temporal detectada."
    elif not candles_profile.time_column:
        coverage_status = "NAO_CONCLUSIVO: candles sem coluna temporal detectada."
    elif not comparable_by_key:
        coverage_status = "NAO_CONCLUSIVO: não foi possível comparar chaves entre histórico e candles."
    elif history_keys_without_candles and history_keys_without_candles > 0:
        coverage_status = "NAO_CONCLUSIVO: existem chaves no histórico sem candles correspondentes."
    else:
        coverage_status = "INFORMATIVO: cobertura por chave não indicou lacunas evidentes; limpeza real segue bloqueada."

    return CoverageResult(
        history_profile=history_profile,
        candles_profile=candles_profile,
        comparable_by_key=comparable_by_key,
        history_keys_without_candles=history_keys_without_candles,
        candles_keys_without_history=candles_keys_without_history,
        coverage_status=coverage_status,
        real_cleanup_approved=False,
    )


def render_profile(profile: TableProfile) -> list[str]:
    lines: list[str] = []
    lines.append(f"### `{profile.table_name}`")
    lines.append("")
    lines.append(f"- Existe: {'sim' if profile.exists else 'não'}")
    lines.append(f"- Linhas: {profile.row_count}")
    lines.append(f"- Coluna de chave detectada: `{profile.key_column}`" if profile.key_column else "- Coluna de chave detectada: não detectada")
    lines.append(f"- Coluna temporal detectada: `{profile.time_column}`" if profile.time_column else "- Coluna temporal detectada: não detectada")
    lines.append(f"- Menor data/hora: `{profile.min_time}`" if profile.min_time else "- Menor data/hora: não disponível")
    lines.append(f"- Maior data/hora: `{profile.max_time}`" if profile.max_time else "- Maior data/hora: não disponível")
    if profile.distinct_keys is None:
        lines.append("- Chaves distintas: não disponível")
    else:
        lines.append(f"- Chaves distintas: {profile.distinct_keys}")
    lines.append("")
    lines.append("Colunas detectadas:")
    lines.append("")
    if profile.columns:
        for column in profile.columns:
            lines.append(f"- `{column}`")
    else:
        lines.append("- nenhuma")
    lines.append("")
    return lines


def render_report(result: CoverageResult, now: datetime) -> str:
    lines: list[str] = []
    lines.append("# Fase 6.2 - Validação de cobertura dos candles")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713")
    lines.append("")
    lines.append(f"Data de geração: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Validação operacional não destrutiva e somente leitura.")
    lines.append("")
    lines.append("A finalidade é avaliar se há evidência mínima de cobertura entre histórico intraday bruto e candles consolidados.")
    lines.append("")
    lines.append("## Banco")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH}`")
    lines.append(f"- Existe: {'sim' if DB_PATH.exists() else 'não'}")
    if DB_PATH.exists():
        lines.append(f"- Tamanho em bytes: {DB_PATH.stat().st_size}")
    lines.append("")
    lines.append("## Perfis avaliados")
    lines.append("")
    lines.extend(render_profile(result.history_profile))
    lines.extend(render_profile(result.candles_profile))
    lines.append("## Comparação")
    lines.append("")
    lines.append(f"- Comparável por chave: {'sim' if result.comparable_by_key else 'não'}")
    lines.append(
        "- Chaves no histórico sem candles correspondentes: "
        + ("não disponível" if result.history_keys_without_candles is None else str(result.history_keys_without_candles))
    )
    lines.append(
        "- Chaves em candles sem histórico correspondente: "
        + ("não disponível" if result.candles_keys_without_history is None else str(result.candles_keys_without_history))
    )
    lines.append("")
    lines.append("## Resultado")
    lines.append("")
    lines.append(f"- Status de cobertura: {result.coverage_status}")
    lines.append("- Aprovado para limpeza real: não")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: não")
    lines.append("")
    lines.append("## Decisão")
    lines.append("")
    lines.append("A Fase 6.2 apenas valida cobertura e preserva bloqueio de limpeza real.")
    lines.append("")
    lines.append("Qualquer remoção futura deve exigir aprovação explícita em fase posterior.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        result = evaluate_coverage(conn)

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    print("Validação de cobertura concluída sem alterações no banco.")
    print(f"Relatório gerado em: {REPORT_PATH}")
    print(f"Status: {result.coverage_status}")
    print("Aprovado para limpeza real: não")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
