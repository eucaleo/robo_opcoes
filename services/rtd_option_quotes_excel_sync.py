from __future__ import annotations

# --- INICIO FRENTE 32 RTD OPTION QUOTES EXCEL SYNC PARSER BRIDGE CONTRACT ---
# Frente 32: ponte local de contrato para parsers canonicos no sync Excel RTD.
#
# Objetivo: deixar rtd_option_quotes_excel_sync.py preparado para reconhecer
# utils.number_parser e utils.date_parser como contratos canonicos de
# normalizacao, mantendo a operacao atual intacta nesta frente.
#
# Esta frente nao troca persistencia.
# Esta frente nao altera o caminho operacional do sync RTD.
# Esta frente apenas registra a ponte contratual para migracao incremental.
from repositories.rtd_option_quotes_repository import (
    _frente62_get_table_columns_impl,
    _frente62_update_or_insert_quotes_impl,
)
try:
    from utils.number_parser import (
        parse_float_br as _frente32_parse_float_br,
        parse_optional_float as _frente32_parse_optional_float,
        parse_positive_float as _frente32_parse_positive_float,
        parse_percent as _frente32_parse_percent,
    )
    from utils.date_parser import (
        parse_datetime_to_iso as _frente32_parse_datetime_to_iso,
        parse_excel_date_to_iso as _frente32_parse_excel_date_to_iso,
    )
except Exception:
    _frente32_parse_float_br = None
    _frente32_parse_optional_float = None
    _frente32_parse_positive_float = None
    _frente32_parse_percent = None
    _frente32_parse_datetime_to_iso = None
    _frente32_parse_excel_date_to_iso = None


FRENTE32_CANONICAL_NUMBER_PARSERS = (
    _frente32_parse_float_br,
    _frente32_parse_optional_float,
    _frente32_parse_positive_float,
    _frente32_parse_percent,
)

FRENTE32_CANONICAL_DATE_PARSERS = (
    _frente32_parse_datetime_to_iso,
    _frente32_parse_excel_date_to_iso,
)
# --- FIM FRENTE 32 RTD OPTION QUOTES EXCEL SYNC PARSER BRIDGE CONTRACT ---

# --- INICIO FRENTE 28 RTD OPTION QUOTES EXCEL SYNC REPOSITORY BRIDGE CONTRACT ---
# Frente 28: ponte local de contrato para o sync Excel RTD de opcoes.
#
# Objetivo: deixar rtd_option_quotes_excel_sync.py preparado para reconhecer
# RtdOptionQuotesRepository como caminho oficial de persistencia futura de
# rtd_option_quotes, mantendo a operacao atual intacta nesta frente.
#
# Esta frente nao troca persistencia.
# Esta frente nao troca o fluxo operacional amplo.
# Regra preservada: option_type canonico somente CALL/PUT por extenso;
# C/V sao compra/venda legado.

try:
    from repositories.rtd_option_quotes_repository import (
        RtdOptionQuotesRepository as _frente28_RtdOptionQuotesRepository,
    )
except Exception:
    _frente28_RtdOptionQuotesRepository = None

try:
    from services import rtd_option_quotes_schema as _frente28_rtd_option_quotes_schema
except Exception:
    _frente28_rtd_option_quotes_schema = None


def _frente28_get_rtd_option_quotes_repository_class():
    return _frente28_RtdOptionQuotesRepository


def _frente28_get_rtd_option_quotes_schema():
    return _frente28_rtd_option_quotes_schema


def _frente28_build_rtd_option_quotes_repository(db_path=None):
    repo_cls = _frente28_get_rtd_option_quotes_repository_class()
    if repo_cls is None:
        return None

    if db_path is not None:
        try:
            return repo_cls(db_path=db_path)
        except TypeError:
            pass
        except Exception:
            return None

        try:
            return repo_cls(db_path)
        except TypeError:
            pass
        except Exception:
            return None

    try:
        return repo_cls()
    except Exception:
        return None


def _frente28_repository_bridge_contract_note():
    return (
        "rtd_option_quotes_excel_sync deve convergir para "
        "RtdOptionQuotesRepository.upsert_many como caminho oficial; "
        "esta frente cria apenas a ponte contratual local, sem troca de "
        "persistencia e sem troca operacional ampla."
    )

# --- FIM FRENTE 28 RTD OPTION QUOTES EXCEL SYNC REPOSITORY BRIDGE CONTRACT ---

import argparse
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
    """Delegado para repository pela Frente 62; mantém assinatura pública/local."""
    return _frente62_get_table_columns_impl(con, table_name)


def update_or_insert_quotes(db_path, quotes):
    """Delegado para repository pela Frente 62; mantém assinatura pública/local."""
    return _frente62_update_or_insert_quotes_impl(db_path, quotes)


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


# --- Frente 22C: RTD Option Quotes schema public API bridge ---
#
# Adoção incremental e local do contrato público de RTD Option Quotes.
# Esta ponte não troca fluxo operacional, não altera persistência e não
# muda contrato financeiro. O contrato canônico de option_type permanece
# fora deste ponto: CALL/PUT por extenso; C/V pertencem ao legado de
# compra/venda.

try:
    from services import rtd_option_quotes_schema as _frente_22c_rtd_option_quotes_schema
except Exception:  # pragma: no cover - fallback defensivo para ambientes parciais
    _frente_22c_rtd_option_quotes_schema = None


def _frente_22c_schema_api(*names):
    schema = globals().get("_frente_22c_rtd_option_quotes_schema")
    if schema is None:
        return None

    for name in names:
        api = getattr(schema, name, None)
        if callable(api):
            return api

    return None


def _frente_22c_schema_value(*names, default=None):
    api = _frente_22c_schema_api(*names)
    if callable(api):
        try:
            return api()
        except Exception:
            return default

    schema = globals().get("_frente_22c_rtd_option_quotes_schema")
    if schema is not None:
        for name in names:
            if hasattr(schema, name):
                return getattr(schema, name)

    return default


def _frente_22c_schema_headers(default=None):
    value = _frente_22c_schema_value(
        "rtd_option_quotes_headers",
        "RTD_OPTION_QUOTES_HEADERS",
        "HEADERS",
        default=default,
    )
    if value is None:
        return default

    try:
        return list(value)
    except TypeError:
        return default


def _frente_22c_schema_required_headers(default=None):
    value = _frente_22c_schema_value(
        "rtd_option_quotes_required_headers",
        "RTD_OPTION_QUOTES_REQUIRED_HEADERS",
        "REQUIRED_HEADERS",
        default=default,
    )
    if value is None:
        return default

    try:
        return list(value)
    except TypeError:
        return default


def _frente_22c_schema_workbook_name(default=None):
    value = _frente_22c_schema_value(
        "rtd_option_quotes_workbook_name",
        "RTD_OPTION_QUOTES_WORKBOOK_NAME",
        "DEFAULT_WORKBOOK_NAME",
        default=default,
    )
    return default if value in (None, "") else value


def _frente_22c_schema_sheet_name(default=None):
    value = _frente_22c_schema_value(
        "rtd_option_quotes_sheet_name",
        "RTD_OPTION_QUOTES_SHEET_NAME",
        "DEFAULT_SHEET_NAME",
        default=default,
    )
    return default if value in (None, "") else value


_FRENTE_22C_PREVIOUS_NORMALIZE_HEADER = globals().get("normalize_header")


def _frente_22c_normalize_header(value):
    api = _frente_22c_schema_api(
        "normalize_rtd_option_quotes_header",
        "rtd_option_quotes_normalize_header",
        "normalize_header",
    )
    if callable(api):
        return api(value)

    previous = globals().get("_FRENTE_22C_PREVIOUS_NORMALIZE_HEADER")
    if callable(previous):
        return previous(value)

    if value is None:
        return ""

    text = str(value).strip().lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^a-z0-9_]+", "", text)
    return text


def _frente_22c_apply_schema_contract():
    workbook = _frente_22c_schema_workbook_name(
        globals().get("DEFAULT_WORKBOOK_NAME")
        or globals().get("WORKBOOK_NAME")
        or globals().get("EXCEL_WORKBOOK_NAME")
        or globals().get("DEFAULT_EXCEL_WORKBOOK_NAME")
    )
    sheet = _frente_22c_schema_sheet_name(
        globals().get("DEFAULT_SHEET_NAME")
        or globals().get("SHEET_NAME")
        or globals().get("EXCEL_SHEET_NAME")
        or globals().get("DEFAULT_EXCEL_SHEET_NAME")
    )
    headers = _frente_22c_schema_headers(
        globals().get("HEADERS")
        or globals().get("RTD_HEADERS")
        or globals().get("OPTION_QUOTES_HEADERS")
    )
    required_headers = _frente_22c_schema_required_headers(
        globals().get("REQUIRED_HEADERS")
        or globals().get("RTD_REQUIRED_HEADERS")
        or globals().get("OPTION_QUOTES_REQUIRED_HEADERS")
    )

    if workbook is not None:
        for key in (
            "DEFAULT_WORKBOOK_NAME",
            "WORKBOOK_NAME",
            "EXCEL_WORKBOOK_NAME",
            "DEFAULT_EXCEL_WORKBOOK_NAME",
        ):
            if key in globals():
                globals()[key] = workbook

    if sheet is not None:
        for key in (
            "DEFAULT_SHEET_NAME",
            "SHEET_NAME",
            "EXCEL_SHEET_NAME",
            "DEFAULT_EXCEL_SHEET_NAME",
        ):
            if key in globals():
                globals()[key] = sheet

    if headers:
        for key in (
            "HEADERS",
            "RTD_HEADERS",
            "OPTION_QUOTES_HEADERS",
        ):
            if key in globals():
                globals()[key] = list(headers)

    if required_headers:
        for key in (
            "REQUIRED_HEADERS",
            "RTD_REQUIRED_HEADERS",
            "OPTION_QUOTES_REQUIRED_HEADERS",
        ):
            if key in globals():
                globals()[key] = list(required_headers)

    globals()["normalize_header"] = _frente_22c_normalize_header


_frente_22c_apply_schema_contract()
# --- Fim Frente 22C ---
