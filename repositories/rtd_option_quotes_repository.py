from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# repositories/rtd_option_quotes_repository.py


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

# INICIO FRENTE 62 RTD OPTION QUOTES EXCEL SYNC SQL BOUNDARY
# Código movido de services/rtd_option_quotes_excel_sync.py.
# Objetivo: concentrar sqlite3.connect, PRAGMA table_info e SQL direto em repository.
# Guardrail: não alterar schema, persistência ou contrato externo do service.

def _frente62_get_table_columns_impl(con, table_name):
    rows = con.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1] for row in rows}


def _frente62_update_or_insert_quotes_impl(db_path, quotes):
    if not quotes:
        return {
            "updated": 0,
            "inserted": 0,
            "total": 0,
        }

    updated = 0
    inserted = 0


    def _parse_excel_float(value):
        if value is None:
            return None

        if isinstance(value, (int, float)):
            try:
                return float(value)
            except Exception:
                return None

        s = str(value).strip()
        if not s:
            return None

        lowered = s.lower()
        if lowered in {"none", "null", "nan", "na", "n/a", "-", "--"}:
            return None

        s = s.replace("\xa0", "").replace(" ", "")

        # Formatos possíveis:
        # "1,05"       -> 1.05
        # "31.380,80"  -> 31380.80
        # "31380.80"   -> 31380.80
        # "1,234.56"   -> 1234.56
        try:
            if "," in s and "." in s:
                if s.rfind(",") > s.rfind("."):
                    s = s.replace(".", "").replace(",", ".")
                else:
                    s = s.replace(",", "")
            elif "," in s:
                s = s.replace(",", ".")

            return float(s)
        except Exception:
            return None


    def _parse_excel_date(value):
        if value is None:
            return None

        s = str(value).strip()
        if not s:
            return None

        # Já ISO.
        if len(s) >= 10 and s[4:5] == "-" and s[7:8] == "-":
            return s[:10]

        from datetime import datetime, timedelta

        for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(s[:10], fmt).date().isoformat()
            except Exception:
                pass

        serial = _parse_excel_float(value)
        if serial is not None and 20000 <= serial <= 60000:
            try:
                base = datetime(1899, 12, 30)
                return (base + timedelta(days=int(serial))).date().isoformat()
            except Exception:
                return None

        return None


    def _normalize_excel_quote_payload(quote):
        """
        Garante que as colunas operacionais reflitam o payload Excel/RTD atual.

        Motivo:
        em alguns fluxos o raw_json chegava novo, mas ultimo_preco/bid/ask/vwap
        permaneciam com valores antigos. A UI/payoff consome as colunas
        normalizadas, não o raw_json.
        """
        import json

        normalized = dict(quote or {})

        payload = None
        raw_json = normalized.get("raw_json")

        if isinstance(raw_json, dict):
            payload = raw_json
        elif isinstance(raw_json, str) and raw_json.strip():
            try:
                payload = json.loads(raw_json, strict=False)
            except Exception:
                payload = None

        source = payload if isinstance(payload, dict) else normalized

        codigo = source.get("codigo_opcao")
        if codigo is not None:
            normalized["codigo_opcao"] = str(codigo).strip().upper()

        ativo_base = source.get("ativo_base")
        if ativo_base is not None:
            normalized["ativo_base"] = str(ativo_base).strip().upper()

        call_put = source.get("call_put")
        if call_put is not None:
            normalized["call_put"] = str(call_put).strip().upper()

        vencimento = source.get("vencimento")
        parsed_vencimento = _parse_excel_date(vencimento)
        if parsed_vencimento is not None:
            normalized["vencimento"] = parsed_vencimento

        numeric_fields = (
            "strike",
            "ultimo_preco",
            "ultima_quantidade",
            "bid",
            "ask",
            "volume",
            "iv",
            "delta",
            "gamma",
            "theta",
            "vega",
            "vwap",
        )

        for field in numeric_fields:
            if field in source:
                parsed = _parse_excel_float(source.get(field))
                if parsed is not None:
                    normalized[field] = parsed

        return normalized



    def _force_operational_columns_from_raw_json(db_quote):
        """
        Hotfix: força as colunas operacionais a refletirem o raw_json atual.

        Caso observado:
        - raw_json chega novo do Excel/RTD;
        - ultimo_preco/bid/ask/vwap continuam antigos;
        - UI/payoff consomem as colunas normalizadas, não o raw_json.
        """
        import json
        from datetime import datetime, timedelta

        if not isinstance(db_quote, dict):
            return db_quote

        raw = db_quote.get("raw_json")
        if not raw:
            return db_quote

        try:
            payload = raw if isinstance(raw, dict) else json.loads(str(raw), strict=False)
        except Exception:
            return db_quote

        if not isinstance(payload, dict):
            return db_quote

        def parse_float(value):
            if value is None:
                return None

            if isinstance(value, (int, float)):
                try:
                    return float(value)
                except Exception:
                    return None

            s = str(value).strip()
            if not s:
                return None

            if s.lower() in {"none", "null", "nan", "na", "n/a", "-", "--"}:
                return None

            s = s.replace("\xa0", "").replace(" ", "")

            try:
                if "," in s and "." in s:
                    # BR: 31.380,80
                    if s.rfind(",") > s.rfind("."):
                        s = s.replace(".", "").replace(",", ".")
                    # US: 31,380.80
                    else:
                        s = s.replace(",", "")
                elif "," in s:
                    s = s.replace(",", ".")

                return float(s)
            except Exception:
                return None

        def parse_date(value):
            if value is None:
                return None

            s = str(value).strip()
            if not s:
                return None

            if len(s) >= 10 and s[4:5] == "-" and s[7:8] == "-":
                return s[:10]

            for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
                try:
                    return datetime.strptime(s[:10], fmt).date().isoformat()
                except Exception:
                    pass

            serial = parse_float(value)
            if serial is not None and 20000 <= serial <= 60000:
                try:
                    return (datetime(1899, 12, 30) + timedelta(days=int(serial))).date().isoformat()
                except Exception:
                    return None

            return None

        text_fields = {
            "codigo_opcao": lambda x: str(x).strip().upper(),
            "ativo_base": lambda x: str(x).strip().upper(),
            "call_put": lambda x: str(x).strip().upper(),
        }

        for field, converter in text_fields.items():
            if field in payload and payload.get(field) is not None:
                db_quote[field] = converter(payload.get(field))

        vencimento = parse_date(payload.get("vencimento"))
        if vencimento is not None:
            db_quote["vencimento"] = vencimento

        numeric_fields = (
            "strike",
            "ultimo_preco",
            "ultima_quantidade",
            "bid",
            "ask",
            "volume",
            "iv",
            "delta",
            "gamma",
            "theta",
            "vega",
            "vwap",
        )

        for field in numeric_fields:
            if field in payload:
                parsed = parse_float(payload.get(field))
                if parsed is not None:
                    db_quote[field] = parsed

        return db_quote



    def _reconcile_operational_columns_from_raw_json_sql(con, db_quote, columns):
        """
        Reconciliação final e explícita:
        força no SQLite as colunas normalizadas a partir do raw_json atual.
        """
        import json
        from datetime import datetime, timedelta

        if not isinstance(db_quote, dict):
            return False

        codigo_opcao = db_quote.get("codigo_opcao")

        if not codigo_opcao:
            return False

        raw = db_quote.get("raw_json")

        # Fallback importante:
        # em alguns fluxos, db_quote não carrega raw_json,
        # mas o UPDATE anterior já persistiu/tem o raw_json no SQLite.
        if not raw:
            try:
                row = con.execute(
                    """
                    SELECT raw_json
                    FROM rtd_option_quotes
                    WHERE codigo_opcao = ?
                    """,
                    (codigo_opcao,),
                ).fetchone()

                if row:
                    raw = row[0]
            except Exception:
                raw = None

        if not raw:
            return False

        try:
            payload = raw if isinstance(raw, dict) else json.loads(str(raw), strict=False)
        except Exception:
            return False

        if not isinstance(payload, dict):
            return False

        def parse_float(value):
            if value is None:
                return None

            if isinstance(value, (int, float)):
                try:
                    return float(value)
                except Exception:
                    return None

            s = str(value).strip()
            if not s:
                return None

            if s.lower() in {"none", "null", "nan", "na", "n/a", "-", "--"}:
                return None

            s = s.replace("\xa0", "").replace(" ", "")

            try:
                if "," in s and "." in s:
                    # BR: 31.380,80
                    if s.rfind(",") > s.rfind("."):
                        s = s.replace(".", "").replace(",", ".")
                    # US: 31,380.80
                    else:
                        s = s.replace(",", "")
                elif "," in s:
                    s = s.replace(",", ".")

                return float(s)
            except Exception:
                return None

        def parse_date(value):
            if value is None:
                return None

            s = str(value).strip()
            if not s:
                return None

            if len(s) >= 10 and s[4:5] == "-" and s[7:8] == "-":
                return s[:10]

            for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
                try:
                    return datetime.strptime(s[:10], fmt).date().isoformat()
                except Exception:
                    pass

            serial = parse_float(value)
            if serial is not None and 20000 <= serial <= 60000:
                try:
                    return (datetime(1899, 12, 30) + timedelta(days=int(serial))).date().isoformat()
                except Exception:
                    return None

            return None

        values = {}

        text_fields = {
            "ativo_base": lambda x: str(x).strip().upper(),
            "call_put": lambda x: str(x).strip().upper(),
        }

        for field, converter in text_fields.items():
            if field in columns and field in payload and payload.get(field) is not None:
                values[field] = converter(payload.get(field))

        if "vencimento" in columns:
            vencimento = parse_date(payload.get("vencimento"))
            if vencimento is not None:
                values["vencimento"] = vencimento

        numeric_fields = (
            "strike",
            "ultimo_preco",
            "ultima_quantidade",
            "bid",
            "ask",
            "volume",
            "iv",
            "delta",
            "gamma",
            "theta",
            "vega",
            "vwap",
        )

        for field in numeric_fields:
            if field in columns and field in payload:
                parsed = parse_float(payload.get(field))
                if parsed is not None:
                    values[field] = parsed

        if not values:
            return False

        set_clause = ", ".join([f"{field} = ?" for field in values.keys()])
        params = list(values.values()) + [codigo_opcao]

        con.execute(
            f"""
            UPDATE rtd_option_quotes
            SET {set_clause}
            WHERE codigo_opcao = ?
            """,
            params,
        )

        return True


    with sqlite3.connect(db_path) as con:
        columns = get_table_columns(con, "rtd_option_quotes")

        for quote in quotes:
            quote = _normalize_excel_quote_payload(quote)

            db_quote = {
                key: value
                for key, value in quote.items()
                if key in columns
            }

            db_quote = _force_operational_columns_from_raw_json(db_quote)
            db_quote = {
                key: value
                for key, value in db_quote.items()
                if key in columns
            }

            codigo_opcao = db_quote.get("codigo_opcao")

            if not codigo_opcao:
                continue

            update_columns = [
                key
                for key in db_quote.keys()
                if key not in {"id", "codigo_opcao", "created_at"}
            ]

            if update_columns:
                set_clause = ", ".join([f"{col} = ?" for col in update_columns])
                params = [db_quote[col] for col in update_columns]
                params.append(codigo_opcao)

                cursor = con.execute(
                    f"""
                    UPDATE rtd_option_quotes
                    SET {set_clause}
                    WHERE codigo_opcao = ?
                    """,
                    params,
                )

                if cursor.rowcount > 0:
                    _reconcile_operational_columns_from_raw_json_sql(con, db_quote, columns)
                    updated += 1
                    continue

            insert_columns = [
                key
                for key in db_quote.keys()
                if key not in {"id"}
            ]

            placeholders = ", ".join(["?"] * len(insert_columns))
            column_clause = ", ".join(insert_columns)
            params = [db_quote[col] for col in insert_columns]

            con.execute(
                f"""
                INSERT INTO rtd_option_quotes ({column_clause})
                VALUES ({placeholders})
                """,
                params,
            )

            inserted += 1

        con.commit()

    return {
        "updated": updated,
        "inserted": inserted,
        "total": updated + inserted,
    }

# FIM FRENTE 62 RTD OPTION QUOTES EXCEL SYNC SQL BOUNDARY
