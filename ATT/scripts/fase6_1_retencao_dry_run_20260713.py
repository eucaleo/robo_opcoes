from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


DB_PATH = Path("dados/app.db")
REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_1_retencao_dry_run_20260713.md")

TARGET_TABLES = [
    "rtd_option_quotes",
    "rtd_option_quotes_intraday_history",
    "rtd_option_quotes_intraday_candles",
    "rtd_underlying_quotes",
    "structure_snapshots",
    "system_snapshots",
]

TIMESTAMP_CANDIDATES = [
    "captured_at",
    "timestamp",
    "created_at",
    "updated_at",
    "candle_start",
    "candle_end",
    "snapshot_at",
    "as_of",
]


@dataclass(frozen=True)
class TableDryRunResult:
    table_name: str
    exists: bool
    row_count: int | None
    timestamp_column: str | None
    cutoff_iso: str | None
    eligible_rows: int | None
    retention_rule: str
    destructive_action: str


def connect_read_only(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco não encontrado: {db_path}")

    absolute_path = db_path.resolve().as_posix()
    uri = f"file:{absolute_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


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
    rows = conn.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    return [str(row[1]) for row in rows]


def count_rows(conn: sqlite3.Connection, table_name: str) -> int:
    row = conn.execute(f'SELECT COUNT(*) FROM "{table_name}"').fetchone()
    return int(row[0] or 0)


def choose_timestamp_column(columns: Iterable[str]) -> str | None:
    lowered = {column.lower(): column for column in columns}
    for candidate in TIMESTAMP_CANDIDATES:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    return None


def count_eligible_rows(
    conn: sqlite3.Connection,
    table_name: str,
    timestamp_column: str,
    cutoff_iso: str,
) -> int:
    row = conn.execute(
        f'''
        SELECT COUNT(*)
        FROM "{table_name}"
        WHERE "{timestamp_column}" IS NOT NULL
          AND "{timestamp_column}" < ?
        ''',
        (cutoff_iso,),
    ).fetchone()
    return int(row[0] or 0)


def retention_rule_for(table_name: str) -> tuple[int | None, str]:
    if table_name == "rtd_option_quotes":
        return None, "snapshot operacional atual: preservar integralmente"
    if table_name == "rtd_option_quotes_intraday_candles":
        return None, "candles consolidados: preservar integralmente nesta etapa"
    if table_name == "rtd_option_quotes_intraday_history":
        return 30, "histórico intraday bruto: candidato futuro apenas após validação de cobertura por candles"
    if table_name == "rtd_underlying_quotes":
        return 30, "cotações de ativo base: candidato futuro somente via política explícita"
    if table_name == "structure_snapshots":
        return 90, "snapshots estruturais: candidato futuro com retenção mínima de auditoria"
    if table_name == "system_snapshots":
        return 90, "snapshots sistêmicos: candidato futuro com retenção mínima de auditoria"
    return None, "sem política definida: preservar"


def simulate_table(conn: sqlite3.Connection, table_name: str, now: datetime) -> TableDryRunResult:
    if not table_exists(conn, table_name):
        return TableDryRunResult(
            table_name=table_name,
            exists=False,
            row_count=None,
            timestamp_column=None,
            cutoff_iso=None,
            eligible_rows=None,
            retention_rule="tabela ausente",
            destructive_action="nenhuma",
        )

    columns = table_columns(conn, table_name)
    row_count = count_rows(conn, table_name)
    retention_days, rule = retention_rule_for(table_name)

    if retention_days is None:
        return TableDryRunResult(
            table_name=table_name,
            exists=True,
            row_count=row_count,
            timestamp_column=None,
            cutoff_iso=None,
            eligible_rows=0,
            retention_rule=rule,
            destructive_action="nenhuma",
        )

    timestamp_column = choose_timestamp_column(columns)

    if timestamp_column is None:
        return TableDryRunResult(
            table_name=table_name,
            exists=True,
            row_count=row_count,
            timestamp_column=None,
            cutoff_iso=None,
            eligible_rows=0,
            retention_rule=f"{rule}; sem coluna temporal detectada, preservar",
            destructive_action="nenhuma",
        )

    cutoff = now - timedelta(days=retention_days)
    cutoff_iso = cutoff.replace(microsecond=0).isoformat()
    eligible_rows = count_eligible_rows(conn, table_name, timestamp_column, cutoff_iso)

    return TableDryRunResult(
        table_name=table_name,
        exists=True,
        row_count=row_count,
        timestamp_column=timestamp_column,
        cutoff_iso=cutoff_iso,
        eligible_rows=eligible_rows,
        retention_rule=f"{rule}; janela simulada: {retention_days} dias",
        destructive_action="nenhuma",
    )


def render_report(results: list[TableDryRunResult], db_path: Path, now: datetime) -> str:
    total_eligible = sum(result.eligible_rows or 0 for result in results)

    lines: list[str] = []
    lines.append("# Fase 6.1 - Dry-run de retenção, limpeza e consolidação")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_1_RETENCAO_DRY_RUN_20260713")
    lines.append("")
    lines.append(f"Data de geração: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Simulação operacional não destrutiva.")
    lines.append("")
    lines.append("Este dry-run abre o banco SQLite em modo somente leitura.")
    lines.append("")
    lines.append("## Banco")
    lines.append("")
    lines.append(f"- Caminho: `{db_path}`")
    lines.append(f"- Existe: {'sim' if db_path.exists() else 'não'}")
    if db_path.exists():
        lines.append(f"- Tamanho em bytes: {db_path.stat().st_size}")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.append("- Nenhum `DELETE` foi executado.")
    lines.append("- Nenhum `UPDATE` foi executado.")
    lines.append("- Nenhum `INSERT` foi executado.")
    lines.append("- Nenhum `DROP` foi executado.")
    lines.append("- Nenhum `ALTER` foi executado.")
    lines.append("- Nenhum `VACUUM` foi executado.")
    lines.append("- Nenhuma compactação foi executada.")
    lines.append("- Nenhum dado foi removido.")
    lines.append("")
    lines.append("## Resultado por tabela")
    lines.append("")
    lines.append("| Tabela | Existe | Linhas | Coluna temporal | Corte simulado | Elegíveis simulados | Regra | Ação destrutiva |")
    lines.append("|---|---:|---:|---|---|---:|---|---|")

    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    result.table_name,
                    "sim" if result.exists else "não",
                    "" if result.row_count is None else str(result.row_count),
                    result.timestamp_column or "",
                    result.cutoff_iso or "",
                    "" if result.eligible_rows is None else str(result.eligible_rows),
                    result.retention_rule,
                    result.destructive_action,
                ]
            )
            + " |"
        )

    lines.append("")
    lines.append("## Total simulado")
    lines.append("")
    lines.append(f"- Linhas potencialmente elegíveis em simulação: {total_eligible}")
    lines.append("- Linhas efetivamente removidas: 0")
    lines.append("")
    lines.append("## Decisão")
    lines.append("")
    lines.append("A Fase 6.1 define contrato e simulação.")
    lines.append("")
    lines.append("A execução destrutiva permanece bloqueada até aprovação explícita em fase posterior.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_1_RETENCAO_DRY_RUN_20260713")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with connect_read_only(DB_PATH) as conn:
        results = [simulate_table(conn, table_name, now) for table_name in TARGET_TABLES]

    report = render_report(results, DB_PATH, now)
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(f"Dry-run concluído sem ações destrutivas.")
    print(f"Relatório gerado em: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
