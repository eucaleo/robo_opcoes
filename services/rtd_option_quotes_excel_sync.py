import argparse
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

from services.rtd_option_quotes_excel_populator import (
    get_db_path,
    get_workbook_path,
    get_sheet_name,
    load_option_codes_from_db,
    get_excel_application,
    get_excel_pid,
    open_workbook_readonly,
    get_or_create_sheet,
    populate_sheet,
    calculate_excel,
    close_without_saving,
)


HEADERS = [
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
    "vwap",
]

NUMERIC_FIELDS = {
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
}


def normalize_empty(value):
    if value is None:
        return None

    if isinstance(value, str):
        text = value.strip()

        if not text:
            return None

        if text.startswith("#"):
            return None

        return text

    return value


def normalize_number(value):
    value = normalize_empty(value)

    if value is None:
        return None

    try:
        return float(value)
    except Exception:
        return None


def normalize_symbol(value):
    value = normalize_empty(value)

    if value is None:
        return None

    return str(value).strip().upper()


def normalize_call_put(value):
    value = normalize_empty(value)

    if value is None:
        return None

    text = str(value).strip().upper()

    if text in {"CALL", "C"}:
        return "CALL"

    if text in {"PUT", "P"}:
        return "PUT"

    return text


def excel_serial_to_date(value):
    try:
        serial = float(value)
    except Exception:
        return None

    # Excel/COM date base.
    dt = datetime(1899, 12, 30) + timedelta(days=serial)

    return dt.date().isoformat()


def normalize_date(value):
    value = normalize_empty(value)

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return excel_serial_to_date(value)

    text = str(value).strip()

    if not text:
        return None

    known_formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
    ]

    for fmt in known_formats:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except Exception:
            pass

    return text


def read_quote_rows(sheet, expected_rows):
    range_values = sheet.Range(f"A1:P{expected_rows}").Value

    if not range_values:
        return []

    rows = list(range_values)

    # Remove cabeçalho.
    data_rows = rows[1:]

    quotes = []

    for row in data_rows:
        if not row:
            continue

        raw = dict(zip(HEADERS, row))
        codigo_opcao = normalize_symbol(raw.get("codigo_opcao"))

        if not codigo_opcao:
            continue

        quote = {
            "codigo_opcao": codigo_opcao,
            "ativo_base": normalize_symbol(raw.get("ativo_base")),
            "call_put": normalize_call_put(raw.get("call_put")),
            "vencimento": normalize_date(raw.get("vencimento")),
        }

        for field in NUMERIC_FIELDS:
            quote[field] = normalize_number(raw.get(field))

        quote["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        quotes.append(quote)

    return quotes


def get_table_columns(con, table_name):
    rows = con.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1] for row in rows}


def update_or_insert_quotes(db_path, quotes):
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


def sync_rtd_option_quotes_from_excel(
    db_path=None,
    workbook_path=None,
    sheet_name=None,
    include_archived=False,
    wait_seconds=10,
    visible=False,
    isolated=True,
    close_on_finish=True,
    dry_run=False,
    print_rows=True,
):
    db_path = Path(db_path or get_db_path()).resolve()
    workbook_path = Path(workbook_path or get_workbook_path()).resolve()
    sheet_name = sheet_name or get_sheet_name()

    codes = load_option_codes_from_db(
        db_path=db_path,
        include_archived=include_archived,
    )

    excel = None
    workbook = None

    print("=" * 80)
    print("RTD Option Quotes Excel Sync - EXCEL TEMPORÁRIO / NO SAVE")
    print("=" * 80)
    print(f"Banco: {db_path}")
    print(f"Workbook: {workbook_path}")
    print(f"Aba: {sheet_name}")
    print(f"Modo isolado: {isolated}")
    print(f"Visível: {visible}")
    print(f"Fechar no final: {close_on_finish}")
    print(f"NUNCA SALVAR EXCEL: True")
    print(f"Dry-run SQLite: {dry_run}")
    print(f"Códigos: {len(codes)}")
    print(codes)
    print("=" * 80)

    try:
        excel = get_excel_application(
            isolated=isolated,
            visible=visible,
        )

        print(f"Excel PID: {get_excel_pid(excel)}")

        workbook, opened_by_script = open_workbook_readonly(
            excel=excel,
            workbook_path=workbook_path,
        )

        print(f"Workbook aberto: {workbook.FullName}")
        print(f"Workbook aberto pelo script: {opened_by_script}")
        print(f"ReadOnly: {bool(workbook.ReadOnly)}")

        sheet = get_or_create_sheet(workbook, sheet_name)

        populate_sheet(sheet, codes)

        calculate_excel(excel)

        if wait_seconds and wait_seconds > 0:
            print(f"Aguardando {wait_seconds}s para atualização RTD...")
            time.sleep(wait_seconds)

        calculate_excel(excel)

        expected_rows = len(codes) + 1
        quotes = read_quote_rows(sheet, expected_rows)

        print("=" * 80)
        print(f"Quotes lidos do Excel: {len(quotes)}")
        print("=" * 80)

        if print_rows:
            for quote in quotes:
                print(quote)

        if dry_run:
            result = {
                "updated": 0,
                "inserted": 0,
                "total": 0,
            }

            print("=" * 80)
            print("DRY-RUN ativo. SQLite não foi alterado.")
            print("=" * 80)

        else:
            result = update_or_insert_quotes(db_path, quotes)

            print("=" * 80)
            print("SQLite atualizado.")
            print(f"Atualizados: {result['updated']}")
            print(f"Inseridos: {result['inserted']}")
            print(f"Total: {result['total']}")
            print("=" * 80)

        print("Excel não foi salvo.")

        return {
            "codes": codes,
            "quotes": quotes,
            "db_result": result,
        }

    finally:
        if close_on_finish:
            print("Fechando workbook/Excel sem salvar...")
            close_without_saving(
                workbook=workbook,
                excel=excel,
                close_workbook=True,
                quit_excel=isolated,
            )
            print("Fechamento solicitado.")


def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza cotações RTD de opções: Excel invisível/read-only -> SQLite, sem salvar Excel."
    )

    parser.add_argument(
        "--db",
        default=str(get_db_path()),
        help="Caminho do banco SQLite.",
    )

    parser.add_argument(
        "--workbook",
        default=str(get_workbook_path()),
        help="Caminho do LISTA_RTD.xlsm.",
    )

    parser.add_argument(
        "--sheet",
        default=get_sheet_name(),
        help="Nome da aba RTD_OPTION_QUOTES.",
    )

    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Inclui opções de estruturas archived.",
    )

    parser.add_argument(
        "--wait",
        type=int,
        default=10,
        help="Segundos aguardando o RTD atualizar.",
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Mostra o Excel para debug. Por padrão roda invisível.",
    )

    parser.add_argument(
        "--attach",
        action="store_true",
        help="Usa Excel existente. Por padrão cria instância isolada.",
    )

    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Não fecha o Excel no final.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Lê RTD, mas não grava no SQLite.",
    )

    parser.add_argument(
        "--no-print-rows",
        action="store_true",
        help="Não imprime os quotes normalizados.",
    )

    args = parser.parse_args()

    sync_rtd_option_quotes_from_excel(
        db_path=Path(args.db),
        workbook_path=Path(args.workbook),
        sheet_name=args.sheet,
        include_archived=args.include_archived,
        wait_seconds=args.wait,
        visible=args.visible,
        isolated=not args.attach,
        close_on_finish=not args.keep_open,
        dry_run=args.dry_run,
        print_rows=not args.no_print_rows,
    )


if __name__ == "__main__":
    main()
