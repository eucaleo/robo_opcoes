"""
Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.

Fluxo esperado:
    LISTA_RTD.xlsm aberto no Excel
        -> aba RTD_OPTION_QUOTES ou RTD_PROBE_OPTIONS
        -> tabela rtd_option_quotes

Uso:
    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db
    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db --dry-run
    python scripts/import_lista_rtd_excel_to_option_quotes.py --db dados/app.db --json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
DEFAULT_SHEETS = ["RTD_OPTION_QUOTES", "RTD_PROBE_OPTIONS", "RTD-BTG LISTA"]

REQUIRED_DB_COLUMNS = [
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


HEADER_ALIASES = {
    "codigo_opcao": "codigo_opcao",
    "codigo": "codigo_opcao",
    "ticker": "codigo_opcao",
    "symbol": "codigo_opcao",
    "ativo": "codigo_opcao",

    "ativo_base": "ativo_base",
    "underlying": "ativo_base",
    "underlying_symbol": "ativo_base",
    "base": "ativo_base",

    "option_type": "option_type",
    "tipo": "option_type",
    "tipo_opcao": "option_type",
    "call_put": "call_put",

    "strike": "strike",
    "strike_price": "strike",

    "maturity": "vencimento",
    "maturitydate": "vencimento",
    "vencimento": "vencimento",
    "data_vencimento": "vencimento",

    "ultimo_preco": "ultimo_preco",
    "last": "ultimo_preco",
    "last_price": "ultimo_preco",
    "last_trade_price": "ultimo_preco",

    "ultima_quantidade": "ultima_quantidade",
    "last_qty": "ultima_quantidade",
    "last_quantity": "ultima_quantidade",
    "last_trade_quantity": "ultima_quantidade",

    "bid": "bid",
    "bid_price": "bid",

    "ask": "ask",
    "ask_price": "ask",

    "volume": "volume",

    "iv": "iv",
    "implied_volatility": "iv",
    "volatilidade_implicita": "iv",

    "delta": "delta",
    "gamma": "gamma",
    "theta": "theta",
    "vega": "vega",

    "status": "status",
}


def normalize_header(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower()
    text = text.replace(" ", "_")
    text = text.replace("-", "_")
    text = text.replace(".", "_")
    text = text.replace("/", "_")
    text = text.replace("%", "pct")

    while "__" in text:
        text = text.replace("__", "_")

    return HEADER_ALIASES.get(text, text)


def excel_serial_to_date(value: Any) -> str | None:
    if value is None or value == "":
        return None

    if isinstance(value, dt.datetime):
        return value.date().isoformat()

    if isinstance(value, dt.date):
        return value.isoformat()

    try:
        number = float(value)
    except Exception:
        text = str(value).strip()
        if not text:
            return None

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return dt.datetime.strptime(text, fmt).date().isoformat()
            except ValueError:
                pass

        return text

    if number <= 0:
        return None

    base = dt.datetime(1899, 12, 30)
    converted = base + dt.timedelta(days=number)
    return converted.date().isoformat()


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None

    if isinstance(value, bool):
        return float(value)

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    text = text.replace("\u00a0", "")
    text = text.replace("R$", "")
    text = text.replace("%", "")
    text = text.strip()

    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    else:
        text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def normalize_call_put(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip().upper()

    if not text:
        return None

    if text in {"C", "CALL", "COMPRA"}:
        return "CALL"

    if text in {"P", "PUT", "VENDA"}:
        return "PUT"

    return text


def clean_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text if text else None


def connect_excel(workbook_path: Path, visible: bool, wait_seconds: int):
    """
    Abre uma instância isolada do Excel apenas para esta importação.

    Regra operacional:
    - não reaproveita Excel já aberto;
    - abre o workbook;
    - aguarda RTD atualizar;
    - registra cleanup para fechar workbook e encerrar Excel ao sair do processo.

    Observação:
    - excel_found retorna False por desenho, pois não buscamos instância ativa.
    """
    import atexit

    try:
        import pythoncom
        import win32com.client
    except ImportError as exc:
        raise RuntimeError(
            "Dependência ausente: pywin32. Instale com: pip install pywin32"
        ) from exc

    workbook = None
    excel = None
    cleaned = False

    try:
        try:
            pythoncom.CoInitialize()
        except Exception:
            pass

        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = visible
        excel.DisplayAlerts = False
        excel.AskToUpdateLinks = False

        def cleanup_excel():
            nonlocal cleaned, workbook, excel

            if cleaned:
                return

            cleaned = True

            try:
                if workbook is not None:
                    workbook.Close(SaveChanges=False)
            except Exception:
                pass

            try:
                if excel is not None:
                    excel.Quit()
            except Exception:
                pass

            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

        atexit.register(cleanup_excel)

        if not workbook_path.exists():
            raise FileNotFoundError(f"Workbook não encontrado: {workbook_path}")

        workbook = excel.Workbooks.Open(
            str(workbook_path),
            UpdateLinks=3,
            ReadOnly=True,
            IgnoreReadOnlyRecommended=True,
        )

        if wait_seconds > 0:
            time.sleep(wait_seconds)

        try:
            excel.Calculate()
        except Exception:
            pass

        try:
            excel.CalculateUntilAsyncQueriesDone()
        except Exception:
            pass

        excel_found = False
        return excel, workbook, excel_found

    except Exception:
        try:
            if workbook is not None:
                workbook.Close(SaveChanges=False)
        except Exception:
            pass

        try:
            if excel is not None:
                excel.Quit()
        except Exception:
            pass

        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

        raise


def find_sheet(workbook: Any, preferred_sheet: str | None) -> Any:
    candidates = [preferred_sheet] if preferred_sheet else DEFAULT_SHEETS

    for sheet_name in candidates:
        if not sheet_name:
            continue

        try:
            return workbook.Worksheets(sheet_name)
        except Exception:
            pass

    available = []
    for ws in workbook.Worksheets:
        available.append(ws.Name)

    raise RuntimeError(
        "Nenhuma aba RTD encontrada. "
        f"Tentadas: {candidates}. "
        f"Disponíveis: {available}"
    )


def read_sheet_records(worksheet: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    used = worksheet.UsedRange
    row_count = int(used.Rows.Count)
    col_count = int(used.Columns.Count)

    if row_count < 2 or col_count < 2:
        return [], {
            "sheet": worksheet.Name,
            "rows_used": row_count,
            "cols_used": col_count,
            "headers": [],
        }

    headers: list[str] = []

    for col in range(1, col_count + 1):
        raw = worksheet.Cells(1, col).Value
        headers.append(normalize_header(raw))

    records: list[dict[str, Any]] = []

    for row in range(2, row_count + 1):
        raw_row: dict[str, Any] = {}

        for col, header in enumerate(headers, start=1):
            if not header:
                continue

            value = worksheet.Cells(row, col).Value
            raw_row[header] = value

        codigo = clean_text(raw_row.get("codigo_opcao"))

        if not codigo:
            continue

        if codigo.lower() in {"codigo_opcao", "codigo", "ticker", "symbol"}:
            continue

        option_type = raw_row.get("option_type")
        call_put = raw_row.get("call_put") or option_type

        normalized = {
            "codigo_opcao": codigo.upper(),
            "ativo_base": clean_text(raw_row.get("ativo_base")),
            "call_put": normalize_call_put(call_put),
            "strike": to_float(raw_row.get("strike")),
            "vencimento": excel_serial_to_date(raw_row.get("vencimento")),
            "ultimo_preco": to_float(raw_row.get("ultimo_preco")),
            "ultima_quantidade": to_float(raw_row.get("ultima_quantidade")),
            "bid": to_float(raw_row.get("bid")),
            "ask": to_float(raw_row.get("ask")),
            "volume": to_float(raw_row.get("volume")),
            "iv": to_float(raw_row.get("iv")),
            "delta": to_float(raw_row.get("delta")),
            "gamma": to_float(raw_row.get("gamma")),
            "theta": to_float(raw_row.get("theta")),
            "vega": to_float(raw_row.get("vega")),
            "raw_input": raw_row,
        }

        records.append(normalized)

    metadata = {
        "sheet": worksheet.Name,
        "rows_used": row_count,
        "cols_used": col_count,
        "headers": headers,
    }

    return records, metadata


def get_table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row[1] for row in rows}


def validate_database(conn: sqlite3.Connection) -> None:
    columns = get_table_columns(conn, "rtd_option_quotes")

    if not columns:
        raise RuntimeError("Tabela rtd_option_quotes não encontrada no banco.")

    missing = [col for col in REQUIRED_DB_COLUMNS if col not in columns]

    if missing:
        raise RuntimeError(
            "Tabela rtd_option_quotes está sem colunas obrigatórias: "
            + ", ".join(missing)
        )


def upsert_records(
    conn: sqlite3.Connection,
    records: list[dict[str, Any]],
    dry_run: bool,
) -> dict[str, int]:
    now = dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")

    stats = {
        "read": len(records),
        "inserted": 0,
        "updated": 0,
        "skipped": 0,
    }

    if dry_run:
        for record in records:
            existing = conn.execute(
                "SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? LIMIT 1",
                (record["codigo_opcao"],),
            ).fetchone()

            if existing:
                stats["updated"] += 1
            else:
                stats["inserted"] += 1

        return stats

    for record in records:
        codigo = record["codigo_opcao"]

        raw_json = json.dumps(
            record.get("raw_input", {}),
            ensure_ascii=False,
            default=str,
            sort_keys=True,
        )

        params_update = {
            "codigo_opcao": codigo,
            "ativo_base": record.get("ativo_base"),
            "call_put": record.get("call_put"),
            "strike": record.get("strike"),
            "vencimento": record.get("vencimento"),
            "ultimo_preco": record.get("ultimo_preco"),
            "ultima_quantidade": record.get("ultima_quantidade"),
            "bid": record.get("bid"),
            "ask": record.get("ask"),
            "volume": record.get("volume"),
            "iv": record.get("iv"),
            "delta": record.get("delta"),
            "gamma": record.get("gamma"),
            "theta": record.get("theta"),
            "vega": record.get("vega"),
            "source": "lista_rtd_excel",
            "raw_json": raw_json,
            "updated_at": now,
        }

        cursor = conn.execute(
            """
            UPDATE rtd_option_quotes
               SET ativo_base = :ativo_base,
                   call_put = :call_put,
                   strike = :strike,
                   vencimento = :vencimento,
                   ultimo_preco = :ultimo_preco,
                   ultima_quantidade = :ultima_quantidade,
                   bid = :bid,
                   ask = :ask,
                   volume = :volume,
                   iv = :iv,
                   delta = :delta,
                   gamma = :gamma,
                   theta = :theta,
                   vega = :vega,
                   source = :source,
                   raw_json = :raw_json,
                   updated_at = :updated_at
             WHERE codigo_opcao = :codigo_opcao
            """,
            params_update,
        )

        if cursor.rowcount > 0:
            stats["updated"] += 1
            continue

        params_insert = dict(params_update)
        params_insert["created_at"] = now

        conn.execute(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            )
            VALUES (
                :codigo_opcao,
                :ativo_base,
                :call_put,
                :strike,
                :vencimento,
                :ultimo_preco,
                :ultima_quantidade,
                :bid,
                :ask,
                :volume,
                :iv,
                :delta,
                :gamma,
                :theta,
                :vega,
                :source,
                :raw_json,
                :updated_at,
                :created_at
            )
            """,
            params_insert,
        )

        stats["inserted"] += 1

    conn.commit()
    return stats


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
    )

    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do SQLite. Padrão: dados/app.db",
    )

    parser.add_argument(
        "--workbook",
        default=DEFAULT_WORKBOOK,
        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
    )

    parser.add_argument(
        "--sheet",
        default=None,
        help=(
            "Nome da aba. Se omitido, tenta RTD_OPTION_QUOTES "
            "e depois RTD_PROBE_OPTIONS."
        ),
    )

    parser.add_argument(
        "--wait-seconds",
        type=int,
        default=5,
        help="Tempo de espera após abrir o workbook. Padrão: 5",
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Deixa o Excel visível.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Lê e valida, mas não grava no banco.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime resultado em JSON.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    db_path = Path(args.db)
    workbook_path = Path(args.workbook).resolve()

    result: dict[str, Any] = {
        "status": "ok",
        "db": str(db_path),
        "workbook": str(workbook_path),
        "sheet": args.sheet,
        "dry_run": bool(args.dry_run),
        "errors": [],
        "stats": {},
        "metadata": {},
        "sample": [],
    }

    try:
        excel, workbook, excel_found = connect_excel(
            workbook_path=workbook_path,
            visible=bool(args.visible),
            wait_seconds=int(args.wait_seconds),
        )

        worksheet = find_sheet(workbook, args.sheet)

        try:
            excel.Calculate()
        except Exception:
            pass

        records, metadata = read_sheet_records(worksheet)

        result["sheet"] = worksheet.Name
        result["excel_found"] = excel_found
        result["metadata"] = metadata
        result["sample"] = records[:3]

        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            validate_database(conn)
            stats = upsert_records(conn, records, dry_run=bool(args.dry_run))

        result["stats"] = stats

    except Exception as exc:
        result["status"] = "error"
        result["errors"].append(f"{type(exc).__name__}: {exc}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        else:
            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
            print("Status: error")
            for error in result["errors"]:
                print("-", error)

        return 1

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
        print(f"Workbook: {result['workbook']}")
        print(f"Aba: {result['sheet']}")
        print(f"DB: {result['db']}")
        print(f"Dry-run: {'sim' if args.dry_run else 'não'}")
        print("Status: ok")
        print()
        print("Métricas:")
        for key, value in result["stats"].items():
            print(f"- {key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
