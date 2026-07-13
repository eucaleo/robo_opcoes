from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_3_mapeamento_schema_cobertura_20260713.md")

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

KEY_HINTS = [
    "ticker",
    "symbol",
    "option_symbol",
    "asset",
    "code",
    "contract",
    "instrument",
    "underlying",
    "ativo",
    "opcao",
    "option",
]

TIME_HINTS = [
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
    "time",
    "date",
    "datetime",
]


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    column_type: str
    not_null: bool
    primary_key_position: int
    non_null_rows: int
    distinct_values: int | None
    is_key_candidate: bool
    is_time_candidate: bool


@dataclass(frozen=True)
class TableSchemaProfile:
    table_name: str
    exists: bool
    row_count: int
    columns: list[ColumnProfile]


@dataclass(frozen=True)
class CandidatePair:
    history_column: str
    candles_column: str
    score: int
    reason: str
    history_distinct: int | None
    candles_distinct: int | None
    history_without_candles: int | None
    candles_without_history: int | None


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {db_path}")

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


def count_rows(conn: sqlite3.Connection, table_name: str) -> int:
    row = conn.execute(
        f"SELECT COUNT(*) FROM {quote_identifier(table_name)}"
    ).fetchone()
    return int(row[0] or 0)


def count_non_null(conn: sqlite3.Connection, table_name: str, column_name: str) -> int:
    row = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM {quote_identifier(table_name)}
        WHERE {quote_identifier(column_name)} IS NOT NULL
        """
    ).fetchone()
    return int(row[0] or 0)


def count_distinct(conn: sqlite3.Connection, table_name: str, column_name: str) -> int | None:
    row = conn.execute(
        f"""
        SELECT COUNT(DISTINCT {quote_identifier(column_name)})
        FROM {quote_identifier(table_name)}
        WHERE {quote_identifier(column_name)} IS NOT NULL
        """
    ).fetchone()
    return int(row[0] or 0)


def has_hint(column_name: str, hints: list[str]) -> bool:
    normalized = column_name.lower()
    return any(hint.lower() in normalized for hint in hints)


def profile_table(conn: sqlite3.Connection, table_name: str) -> TableSchemaProfile:
    if not table_exists(conn, table_name):
        return TableSchemaProfile(
            table_name=table_name,
            exists=False,
            row_count=0,
            columns=[],
        )

    row_count = count_rows(conn, table_name)
    info_rows = conn.execute(
        f"PRAGMA table_info({quote_identifier(table_name)})"
    ).fetchall()

    columns: list[ColumnProfile] = []

    for row in info_rows:
        name = str(row[1])
        column_type = str(row[2] or "")
        not_null = bool(row[3])
        primary_key_position = int(row[5] or 0)
        non_null_rows = count_non_null(conn, table_name, name)
        distinct_values = count_distinct(conn, table_name, name)

        columns.append(
            ColumnProfile(
                name=name,
                column_type=column_type,
                not_null=not_null,
                primary_key_position=primary_key_position,
                non_null_rows=non_null_rows,
                distinct_values=distinct_values,
                is_key_candidate=has_hint(name, KEY_HINTS),
                is_time_candidate=has_hint(name, TIME_HINTS),
            )
        )

    return TableSchemaProfile(
        table_name=table_name,
        exists=True,
        row_count=row_count,
        columns=columns,
    )


def count_left_without_right(
    conn: sqlite3.Connection,
    left_table: str,
    left_column: str,
    right_table: str,
    right_column: str,
) -> int:
    row = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM (
            SELECT DISTINCT CAST({quote_identifier(left_column)} AS TEXT) AS item_key
            FROM {quote_identifier(left_table)}
            WHERE {quote_identifier(left_column)} IS NOT NULL

            EXCEPT

            SELECT DISTINCT CAST({quote_identifier(right_column)} AS TEXT) AS item_key
            FROM {quote_identifier(right_table)}
            WHERE {quote_identifier(right_column)} IS NOT NULL
        )
        """
    ).fetchone()
    return int(row[0] or 0)


def pair_score(history_column: ColumnProfile, candles_column: ColumnProfile) -> tuple[int, str]:
    score = 0
    reasons: list[str] = []

    if history_column.name.lower() == candles_column.name.lower():
        score += 100
        reasons.append("mesmo nome de coluna")

    if history_column.is_key_candidate and candles_column.is_key_candidate:
        score += 40
        reasons.append("ambas parecem colunas de chave")

    if history_column.is_time_candidate and candles_column.is_time_candidate:
        score += 35
        reasons.append("ambas parecem colunas temporais")

    if history_column.column_type.lower() == candles_column.column_type.lower():
        score += 10
        reasons.append("mesmo tipo declarado")

    if history_column.distinct_values and candles_column.distinct_values:
        smaller = min(history_column.distinct_values, candles_column.distinct_values)
        larger = max(history_column.distinct_values, candles_column.distinct_values)
        if larger > 0 and smaller / larger >= 0.5:
            score += 10
            reasons.append("cardinalidade relativamente proxima")

    return score, "; ".join(reasons) if reasons else "baixo sinal de equivalencia"


def build_candidate_pairs(
    conn: sqlite3.Connection,
    history_profile: TableSchemaProfile,
    candles_profile: TableSchemaProfile,
) -> list[CandidatePair]:
    if not history_profile.exists or not candles_profile.exists:
        return []

    pairs: list[CandidatePair] = []

    for history_column in history_profile.columns:
        for candles_column in candles_profile.columns:
            score, reason = pair_score(history_column, candles_column)

            if score < 40:
                continue

            history_without_candles = count_left_without_right(
                conn,
                HISTORY_TABLE,
                history_column.name,
                CANDLES_TABLE,
                candles_column.name,
            )
            candles_without_history = count_left_without_right(
                conn,
                CANDLES_TABLE,
                candles_column.name,
                HISTORY_TABLE,
                history_column.name,
            )

            pairs.append(
                CandidatePair(
                    history_column=history_column.name,
                    candles_column=candles_column.name,
                    score=score,
                    reason=reason,
                    history_distinct=history_column.distinct_values,
                    candles_distinct=candles_column.distinct_values,
                    history_without_candles=history_without_candles,
                    candles_without_history=candles_without_history,
                )
            )

    return sorted(pairs, key=lambda item: item.score, reverse=True)


def render_table_profile(profile: TableSchemaProfile) -> list[str]:
    lines: list[str] = []

    lines.append(f"## Tabela `{profile.table_name}`")
    lines.append("")
    lines.append(f"- Existe: {'sim' if profile.exists else 'nao'}")
    lines.append(f"- Linhas: {profile.row_count}")
    lines.append("")

    if not profile.exists:
        return lines

    lines.append("| Coluna | Tipo | Not null | PK | Nao nulos | Distintos | Chave candidata | Temporal candidata |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")

    for column in profile.columns:
        distinct_text = "" if column.distinct_values is None else str(column.distinct_values)
        lines.append(
            "| "
            + f"`{column.name}` | "
            + f"`{column.column_type}` | "
            + f"{'sim' if column.not_null else 'nao'} | "
            + f"{column.primary_key_position} | "
            + f"{column.non_null_rows} | "
            + f"{distinct_text} | "
            + f"{'sim' if column.is_key_candidate else 'nao'} | "
            + f"{'sim' if column.is_time_candidate else 'nao'} |"
        )

    lines.append("")
    return lines


def render_candidate_pairs(pairs: list[CandidatePair]) -> list[str]:
    lines: list[str] = []

    lines.append("## Pares candidatos para comparacao")
    lines.append("")

    if not pairs:
        lines.append("Nenhum par candidato suficiente foi identificado automaticamente.")
        lines.append("")
        return lines

    lines.append("| Historico | Candles | Score | Motivo | Distintos historico | Distintos candles | Historico sem candles | Candles sem historico |")
    lines.append("|---|---|---:|---|---:|---:|---:|---:|")

    for pair in pairs:
        lines.append(
            "| "
            + f"`{pair.history_column}` | "
            + f"`{pair.candles_column}` | "
            + f"{pair.score} | "
            + f"{pair.reason} | "
            + f"{'' if pair.history_distinct is None else pair.history_distinct} | "
            + f"{'' if pair.candles_distinct is None else pair.candles_distinct} | "
            + f"{'' if pair.history_without_candles is None else pair.history_without_candles} | "
            + f"{'' if pair.candles_without_history is None else pair.candles_without_history} |"
        )

    lines.append("")
    return lines


def coverage_decision(pairs: list[CandidatePair]) -> str:
    if not pairs:
        return "NAO_CONCLUSIVO: nao ha par de colunas candidato suficiente para validar cobertura."

    best = pairs[0]

    if best.history_without_candles == 0:
        return (
            "MAPEAMENTO_CANDIDATO: melhor par nao indicou historico sem candles, "
            "mas a limpeza real permanece bloqueada."
        )

    return (
        "NAO_CONCLUSIVO: melhor par ainda indica historico sem candles correspondentes "
        "ou requer validacao humana."
    )


def render_report(
    history_profile: TableSchemaProfile,
    candles_profile: TableSchemaProfile,
    pairs: list[CandidatePair],
    now: datetime,
) -> str:
    decision = coverage_decision(pairs)

    lines: list[str] = []

    lines.append("# Fase 6.3 - Mapeamento de schema para cobertura de candles")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Mapeamento operacional nao destrutivo e somente leitura.")
    lines.append("")
    lines.append("A finalidade e identificar pares de colunas candidatos para tornar a validacao de cobertura mais objetiva.")
    lines.append("")
    lines.append("## Banco")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH.as_posix()}`")
    lines.append(f"- Existe: {'sim' if DB_PATH.exists() else 'nao'}")
    if DB_PATH.exists():
        lines.append(f"- Tamanho em bytes: {DB_PATH.stat().st_size}")
    lines.append("")
    lines.extend(render_table_profile(history_profile))
    lines.extend(render_table_profile(candles_profile))
    lines.extend(render_candidate_pairs(pairs))
    lines.append("## Resultado")
    lines.append("")
    lines.append(f"- Status: {decision}")
    lines.append("- Aprovado para limpeza real: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.3 apenas mapeia schema e candidatos de comparacao.")
    lines.append("")
    lines.append("A execucao de limpeza real permanece bloqueada ate aprovacao explicita em fase posterior.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        history_profile = profile_table(conn, HISTORY_TABLE)
        candles_profile = profile_table(conn, CANDLES_TABLE)
        pairs = build_candidate_pairs(conn, history_profile, candles_profile)

    REPORT_PATH.write_text(
        render_report(history_profile, candles_profile, pairs, now),
        encoding="utf-8",
    )

    print("Mapeamento de schema concluido sem alteracoes no banco.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Pares candidatos encontrados: {len(pairs)}")
    print("Aprovado para limpeza real: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
