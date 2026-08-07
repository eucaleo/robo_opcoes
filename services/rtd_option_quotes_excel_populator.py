import argparse
import os
import re
import time
from pathlib import Path

import win32com.client
from repositories import rtd_option_quotes_excel_populator_sql_boundary as _rtd_excel_populator_sql_boundary


ROOT_DIR = Path(__file__).resolve().parents[1]

DEFAULT_DB_PATH = ROOT_DIR / "dados" / "app.db"
DEFAULT_WORKBOOK_PATH = ROOT_DIR / "LISTA_RTD.xlsm"
DEFAULT_WORKBOOK_NAME = "LISTA_RTD.xlsm"
DEFAULT_SHEET_NAME = "RTD_OPTION_QUOTES"

OPTION_PATTERN = re.compile(r"^[A-Z]{4,6}[A-Z][0-9]{1,4}$")

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

RTD_FIELDS = [
    "QUOTE.UNDERLYING_SYMBOL",
    "QUOTE.OPTION_TYPE",
    "QUOTE.STRIKE_PRICE",
    "QUOTE.MATURITYDATE",
    "QUOTE.LAST_TRADE_PRICE",
    "QUOTE.LAST_TRADE_QUANTITY",
    "QUOTE.BID_PRICE",
    "QUOTE.ASK_PRICE",
    "QUOTE.VOLUME",
    "QUOTE.IMPLIED_VOLATILITY",
    "QUOTE.DELTA",
    "QUOTE.GAMMA",
    "QUOTE.THETA",
    "QUOTE.VEGA",
    "QUOTE.VWAP",
]


def normalize_symbol(value):
    return str(value or "").strip().upper()


def is_option_code(value):
    symbol = normalize_symbol(value)

    if not symbol:
        return False

    non_options = {
        "BPAC11",
        "BOVA11",
        "PRIO3",
        "PETR4",
        "VALE3",
        "ITUB4",
        "BBAS3",
        "WEGE3",
    }

    if symbol in non_options:
        return False

    return bool(OPTION_PATTERN.match(symbol))


def get_db_path():
    return Path(os.getenv("RTD_DB_PATH", str(DEFAULT_DB_PATH))).resolve()


def get_workbook_path():
    return Path(os.getenv("RTD_WORKBOOK_PATH", str(DEFAULT_WORKBOOK_PATH))).resolve()


def get_sheet_name():
    return os.getenv("RTD_OPTION_QUOTES_SHEET", DEFAULT_SHEET_NAME)


def validate_database(db_path):
    """Frente 66: delega acesso SQLite direto para boundary em repositories."""
    return _rtd_excel_populator_sql_boundary.validate_database(db_path)


def load_option_codes_from_db(db_path=None, include_archived=False):
    """Frente 66: delega acesso SQLite direto para boundary em repositories."""
    return _rtd_excel_populator_sql_boundary.load_option_codes_from_db(db_path, include_archived)


def get_excel_pid(excel):
    try:
        import win32process

        _thread_id, process_id = win32process.GetWindowThreadProcessId(excel.Hwnd)
        return process_id
    except Exception:
        return None


def create_isolated_excel(visible=False):
    excel = win32com.client.DispatchEx("Excel.Application")

    excel.Visible = bool(visible)
    excel.DisplayAlerts = False
    excel.EnableEvents = False
    excel.AskToUpdateLinks = False

    try:
        excel.ScreenUpdating = bool(visible)
    except Exception:
        pass

    try:
        excel.Interactive = bool(visible)
    except Exception:
        pass

    return excel


def get_attached_excel(visible=False):
    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
    except Exception:
        excel = win32com.client.Dispatch("Excel.Application")

    excel.Visible = bool(visible)
    excel.DisplayAlerts = False
    excel.EnableEvents = False
    excel.AskToUpdateLinks = False

    try:
        excel.ScreenUpdating = bool(visible)
    except Exception:
        pass

    return excel


def get_excel_application(isolated=True, visible=False):
    if isolated:
        return create_isolated_excel(visible=visible)

    return get_attached_excel(visible=visible)


def find_open_workbook(excel, workbook_path):
    target = str(Path(workbook_path).resolve()).lower()

    for workbook in excel.Workbooks:
        try:
            full_name = str(Path(workbook.FullName).resolve()).lower()
        except Exception:
            full_name = str(workbook.FullName).lower()

        if full_name == target:
            return workbook

    return None


def open_workbook_readonly(excel, workbook_path):
    workbook_path = Path(workbook_path).resolve()

    if not workbook_path.exists():
        raise FileNotFoundError(f"Workbook não encontrado: {workbook_path}")

    opened = find_open_workbook(excel, workbook_path)

    if opened is not None:
        return opened, False

    workbook = excel.Workbooks.Open(
        str(workbook_path),
        UpdateLinks=0,
        ReadOnly=True,
        AddToMru=False,
        IgnoreReadOnlyRecommended=True,
    )

    return workbook, True


def get_or_create_sheet(workbook, sheet_name):
    target = sheet_name.lower()

    for sheet in workbook.Worksheets:
        if str(sheet.Name).lower() == target:
            return sheet

    sheet = workbook.Worksheets.Add()
    sheet.Name = sheet_name
    return sheet


def build_formula(field_name, row_number):
    return f'=RTD("btg_pro_rtd","","{field_name}",$A{row_number})'


def populate_sheet(sheet, codes):
    if not codes:
        raise RuntimeError("Nenhum código de opção encontrado para popular a planilha.")

    last_row = len(codes) + 1
    rows_to_clear = max(1000, last_row + 20)

    sheet.Range(f"A1:P{rows_to_clear}").ClearContents()
    sheet.Range("A1:P1").Value = [HEADERS]
    sheet.Range(f"A2:A{last_row}").Value = [[code] for code in codes]

    formulas_matrix = []

    for row_number in range(2, last_row + 1):
        formulas_matrix.append(
            [build_formula(field_name, row_number) for field_name in RTD_FIELDS]
        )

    sheet.Range(f"B2:P{last_row}").Formula = formulas_matrix

    try:
        sheet.Columns("A:P").AutoFit()
    except Exception:
        pass


def calculate_excel(excel):
    try:
        excel.CalculateFullRebuild()
        return
    except Exception:
        pass

    try:
        excel.Calculate()
    except Exception:
        pass


def read_sheet_values(sheet, rows):
    result = []

    for row_number in range(1, rows + 1):
        values = sheet.Range(f"A{row_number}:P{row_number}").Value
        result.append(values)

    return result


def close_without_saving(workbook=None, excel=None, close_workbook=True, quit_excel=True):
    if workbook is not None and close_workbook:
        try:
            workbook.Close(SaveChanges=False)
        except Exception:
            try:
                workbook.Close(False)
            except Exception as exc:
                print(f"Falha ao fechar workbook sem salvar: {exc}")

    if excel is not None and quit_excel:
        try:
            excel.DisplayAlerts = False
        except Exception:
            pass

        try:
            excel.Quit()
        except Exception as exc:
            print(f"Falha ao encerrar Excel: {exc}")


def populate_rtd_option_quotes_excel(
    db_path=None,
    workbook_path=None,
    sheet_name=None,
    include_archived=False,
    wait_seconds=8,
    visible=False,
    isolated=True,
    close_on_finish=True,
    print_rows=0,
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
    workbook_opened_by_script = False

    print("=" * 80)
    print("RTD Option Quotes Excel Populator - NO SAVE MODE")
    print("=" * 80)
    print(f"Banco: {db_path}")
    print(f"Workbook: {workbook_path}")
    print(f"Aba: {sheet_name}")
    print(f"Modo isolado: {isolated}")
    print(f"Visível: {visible}")
    print(f"Fechar no final: {close_on_finish}")
    print(f"NUNCA SALVAR: True")
    print(f"Incluir archived: {include_archived}")
    print(f"Códigos encontrados: {len(codes)}")
    print(codes)
    print("=" * 80)

    try:
        excel = get_excel_application(
            isolated=isolated,
            visible=visible,
        )

        excel_pid = get_excel_pid(excel)
        print(f"Excel PID: {excel_pid}")

        workbook, workbook_opened_by_script = open_workbook_readonly(
            excel=excel,
            workbook_path=workbook_path,
        )

        print(f"Workbook aberto: {workbook.FullName}")
        print(f"Workbook aberto pelo script: {workbook_opened_by_script}")
        print(f"ReadOnly: {bool(workbook.ReadOnly)}")

        sheet = get_or_create_sheet(workbook, sheet_name)

        populate_sheet(sheet, codes)

        calculate_excel(excel)

        if wait_seconds and wait_seconds > 0:
            print(f"Aguardando {wait_seconds}s para atualização RTD...")
            time.sleep(wait_seconds)

        calculate_excel(excel)

        printed_values = []

        if print_rows and print_rows > 0:
            printed_values = read_sheet_values(sheet, print_rows)

            print("=" * 80)
            print("Amostra lida do Excel")
            print("=" * 80)

            for index, row_values in enumerate(printed_values, start=1):
                print(index, row_values)

        print("=" * 80)
        print("Concluído com sucesso.")
        print("Nenhum Save foi executado.")
        print("=" * 80)

        return {
            "codes": codes,
            "excel_pid": excel_pid,
            "printed_values": printed_values,
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
        description="Popula RTD_OPTION_QUOTES em Excel temporário, sem salvar, e fecha a instância."
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
        help="Inclui estruturas archived.",
    )

    parser.add_argument(
        "--wait",
        type=int,
        default=8,
        help="Segundos aguardando o RTD atualizar.",
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Mostra o Excel. Por padrão roda em silêncio.",
    )

    parser.add_argument(
        "--attach",
        action="store_true",
        help="Usa instância Excel existente. Por padrão cria uma instância isolada.",
    )

    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Não fecha o Excel no final.",
    )

    parser.add_argument(
        "--print-rows",
        type=int,
        default=12,
        help="Quantidade de linhas para imprimir como validação.",
    )

    args = parser.parse_args()

    isolated = not args.attach
    close_on_finish = not args.keep_open

    populate_rtd_option_quotes_excel(
        db_path=Path(args.db),
        workbook_path=Path(args.workbook),
        sheet_name=args.sheet,
        include_archived=args.include_archived,
        wait_seconds=args.wait,
        visible=args.visible,
        isolated=isolated,
        close_on_finish=close_on_finish,
        print_rows=args.print_rows,
    )


if __name__ == "__main__":
    main()


# >>> FRENTE 22A - RTD Option Quotes Excel Populator schema contract
# Adoção incremental: o populator de Excel RTD passa a preferir a API pública
# de services.rtd_option_quotes_schema quando disponível.
#
# Sem troca operacional ampla.
# Sem alteração de persistência.
# Sem operação de git.
#
# Regra preservada: option_type canônico somente CALL/PUT por extenso;
# C/V são compra/venda legado, não tipo de opção canônico.

def _frente_22a_rtd_option_quotes_schema_module():
    """Retorna o módulo canônico de schema RTD Option Quotes, se disponível."""
    import importlib

    try:
        return importlib.import_module("services.rtd_option_quotes_schema")
    except Exception:
        return None


def _frente_22a_call_schema_api(api_name, fallback=None):
    """Chama uma API pública do schema, preservando fallback local controlado."""
    schema_module = _frente_22a_rtd_option_quotes_schema_module()
    api = getattr(schema_module, api_name, None) if schema_module is not None else None

    if callable(api):
        try:
            return api()
        except Exception:
            pass

    if callable(fallback):
        return fallback()

    return fallback


def _frente_22a_as_list(value):
    if value is None:
        return []

    if isinstance(value, str):
        return [value]

    if isinstance(value, dict):
        return list(value.keys())

    try:
        return list(value)
    except TypeError:
        return [value]


def rtd_option_quotes_excel_populator_headers():
    """Headers do populator preferindo rtd_option_quotes_headers()."""
    fallback = globals().get("HEADERS", ())
    return _frente_22a_as_list(
        _frente_22a_call_schema_api("rtd_option_quotes_headers", fallback)
    )


def rtd_option_quotes_excel_populator_required_headers():
    """Headers obrigatórios preferindo rtd_option_quotes_required_headers()."""
    fallback = globals().get("REQUIRED_HEADERS", globals().get("HEADERS", ()))
    return _frente_22a_as_list(
        _frente_22a_call_schema_api("rtd_option_quotes_required_headers", fallback)
    )


def rtd_option_quotes_excel_populator_workbook_name():
    """Workbook público preferindo rtd_option_quotes_workbook_name()."""
    fallback = globals().get(
        "DEFAULT_WORKBOOK_NAME",
        globals().get("WORKBOOK_NAME", "LISTA_RTD.xlsm"),
    )
    return _frente_22a_call_schema_api("rtd_option_quotes_workbook_name", fallback)


def rtd_option_quotes_excel_populator_sheet_name():
    """Sheet pública preferindo rtd_option_quotes_sheet_name()."""
    fallback = globals().get(
        "DEFAULT_SHEET_NAME",
        globals().get("SHEET_NAME", "RTD_OPTION_QUOTES"),
    )
    return _frente_22a_call_schema_api("rtd_option_quotes_sheet_name", fallback)


# Publicação compatível: consumidores internos antigos que ainda leem constantes
# passam a enxergar os valores resolvidos pela API pública do schema.
_frente_22a_headers = rtd_option_quotes_excel_populator_headers()
if _frente_22a_headers:
    globals()["HEADERS"] = _frente_22a_headers

_frente_22a_required_headers = rtd_option_quotes_excel_populator_required_headers()
if _frente_22a_required_headers:
    globals()["REQUIRED_HEADERS"] = _frente_22a_required_headers

_frente_22a_workbook_name = rtd_option_quotes_excel_populator_workbook_name()
if _frente_22a_workbook_name:
    globals()["DEFAULT_WORKBOOK_NAME"] = _frente_22a_workbook_name
    globals()["WORKBOOK_NAME"] = _frente_22a_workbook_name

_frente_22a_sheet_name = rtd_option_quotes_excel_populator_sheet_name()
if _frente_22a_sheet_name:
    globals()["DEFAULT_SHEET_NAME"] = _frente_22a_sheet_name
    globals()["SHEET_NAME"] = _frente_22a_sheet_name

try:
    __all__
except NameError:
    __all__ = []

for _frente_22a_public_name in (
    "rtd_option_quotes_excel_populator_headers",
    "rtd_option_quotes_excel_populator_required_headers",
    "rtd_option_quotes_excel_populator_workbook_name",
    "rtd_option_quotes_excel_populator_sheet_name",
):
    if _frente_22a_public_name not in __all__:
        __all__.append(_frente_22a_public_name)

del _frente_22a_public_name
# <<< FRENTE 22A - RTD Option Quotes Excel Populator schema contract
