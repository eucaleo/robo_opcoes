# repositories/rtd_option_quotes_repository.py

from __future__ import annotations

import datetime as dt
import json
import math
import sqlite3
from pathlib import Path
from typing import Any, Iterable

from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema


READ_COLUMNS = [
    "codigo_opcao",
    "ativo_base",
    "call_put",
    "strike",
    "vencimento",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "vwap",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "source",
    "raw_json",
    "updated_at",
    "created_at",
]

NUMERIC_COLUMNS = {
    "strike",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "vwap",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
}


class RtdOptionQuotesRepository:
    """
    Snapshot centralizado de cotacoes RTD de opcoes.

    Papel:
    - tabela rtd_option_quotes
    - banco dados/app.db
    - uma linha logica por codigo_opcao
    - atualizacao por sobrescrita
    - sem historico intraday nesta fase
    """

    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def ensure_schema(self) -> None:
        ensure_rtd_option_quotes_schema(self.db_path)

    def get_by_codigo(self, codigo_opcao: str) -> dict[str, Any] | None:
        sql = f"""
            SELECT
                {", ".join(READ_COLUMNS)}
            FROM rtd_option_quotes
            WHERE UPPER(TRIM(codigo_opcao)) = UPPER(TRIM(?))
            ORDER BY updated_at DESC, id DESC
            LIMIT 1
        """

        with self._connect() as conn:
            row = conn.execute(sql, (codigo_opcao,)).fetchone()

        return dict(row) if row else None

    def list_by_ativo_base(self, ativo_base: str) -> list[dict[str, Any]]:
        sql = f"""
            SELECT
                {", ".join(READ_COLUMNS)}
            FROM rtd_option_quotes
            WHERE UPPER(TRIM(ativo_base)) = UPPER(TRIM(?))
            ORDER BY vencimento, call_put, strike, codigo_opcao
        """

        with self._connect() as conn:
            rows = conn.execute(sql, (ativo_base,)).fetchall()

        return [dict(row) for row in rows]

    def list_all(self) -> list[dict[str, Any]]:
        sql = f"""
            SELECT
                {", ".join(READ_COLUMNS)}
            FROM rtd_option_quotes
            ORDER BY ativo_base, vencimento, call_put, strike, codigo_opcao
        """

        with self._connect() as conn:
            rows = conn.execute(sql).fetchall()

        return [dict(row) for row in rows]

    def upsert_many(
        self,
        records: Iterable[dict[str, Any]],
        *,
        source: str = "excel_rtd_live",
        read_at: str | None = None,
    ) -> int:
        """
        Atualiza o snapshot por codigo_opcao.

        Nao grava historico. Nao duplica simbolos. Preserva created_at quando
        a linha ja existe e altera updated_at a cada sincronizacao valida.
        """
        self.ensure_schema()

        timestamp = _clean_text(read_at) or _utc_now_iso()

        prepared_rows = []
        for record in records:
            prepared = _prepare_record(
                record,
                source=source,
                timestamp=timestamp,
            )
            if prepared is not None:
                prepared_rows.append(prepared)

        if not prepared_rows:
            return 0

        update_columns = [
            "ativo_base",
            "call_put",
            "strike",
            "vencimento",
            "ultimo_preco",
            "ultima_quantidade",
            "bid",
            "ask",
            "volume",
            "vwap",
            "iv",
            "delta",
            "gamma",
            "theta",
            "vega",
            "source",
            "raw_json",
            "updated_at",
        ]

        insert_columns = [
            "codigo_opcao",
            *update_columns,
            "created_at",
        ]

        update_sql = f"""
            UPDATE rtd_option_quotes
            SET
                {", ".join(f"{column} = ?" for column in update_columns)}
            WHERE UPPER(TRIM(codigo_opcao)) = UPPER(TRIM(?))
        """

        insert_sql = f"""
            INSERT INTO rtd_option_quotes (
                {", ".join(insert_columns)}
            )
            VALUES (
                {", ".join("?" for _ in insert_columns)}
            )
        """

        with self._connect() as conn:
            for row in prepared_rows:
                update_values = [row[column] for column in update_columns]
                update_values.append(row["codigo_opcao"])

                cursor = conn.execute(update_sql, update_values)

                if cursor.rowcount == 0:
                    insert_values = [row[column] for column in insert_columns]
                    conn.execute(insert_sql, insert_values)

            conn.commit()

        return len(prepared_rows)


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    lowered = text.lower()
    if lowered in {
        "none",
        "null",
        "nan",
        "#n/a",
        "#n/d",
        "#value!",
        "#valor!",
    }:
        return None

    return text


def _clean_symbol(value: Any) -> str | None:
    text = _clean_text(value)
    if text is None:
        return None
    return text.upper()


def _to_float(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return float(value)

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return float(value)

    text = _clean_text(value)
    if text is None:
        return None

    text = text.replace("\u00a0", "")
    text = text.replace("R$", "")
    text = text.replace("%", "")
    text = text.strip()

    if "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        number = float(text)
    except ValueError:
        return None

    if math.isnan(number) or math.isinf(number):
        return None

    return number


def _prepare_record(
    record: dict[str, Any],
    *,
    source: str,
    timestamp: str,
) -> dict[str, Any] | None:
    codigo_opcao = _clean_symbol(record.get("codigo_opcao"))

    if not codigo_opcao:
        return None

    row: dict[str, Any] = {
        "codigo_opcao": codigo_opcao,
        "ativo_base": _clean_symbol(record.get("ativo_base")),
        "call_put": _clean_text(record.get("call_put")),
        "strike": None,
        "vencimento": _clean_text(record.get("vencimento")),
        "ultimo_preco": None,
        "ultima_quantidade": None,
        "bid": None,
        "ask": None,
        "volume": None,
        "vwap": None,
        "iv": None,
        "delta": None,
        "gamma": None,
        "theta": None,
        "vega": None,
        "source": _clean_text(source) or "excel_rtd_live",
        "raw_json": json.dumps(
            record,
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        ),
        "updated_at": timestamp,
        "created_at": timestamp,
    }

    for column in NUMERIC_COLUMNS:
        row[column] = _to_float(record.get(column))

    return row
