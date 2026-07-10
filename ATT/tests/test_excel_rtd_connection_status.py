from __future__ import annotations

from rtd_bridge.excel_rtd_connection_status import (
    DEFAULT_WORKBOOK_NAME,
    DEFAULT_WORKSHEET_NAME,
    REQUIRED_OPTION_QUOTE_HEADERS,
    check_excel_rtd_connection_status,
)


class FakeCell:
    def __init__(self, value):
        self.Value = value


class FakeColumns:
    def __init__(self, count: int):
        self.Count = count


class FakeUsedRange:
    def __init__(self, count: int):
        self.Columns = FakeColumns(count)


class FakeWorksheet:
    def __init__(self, name: str, headers: tuple[str, ...]):
        self.Name = name
        self._headers = headers
        self.UsedRange = FakeUsedRange(len(headers))

    def Cells(self, row: int, column: int):
        if row != 1:
            return FakeCell(None)

        index = column - 1

        if index < 0 or index >= len(self._headers):
            return FakeCell(None)

        return FakeCell(self._headers[index])


class FakeWorksheets:
    def __init__(self, worksheets: list[FakeWorksheet]):
        self._worksheets = worksheets
        self.Count = len(worksheets)

    def Item(self, key):
        if isinstance(key, int):
            return self._worksheets[key - 1]

        for worksheet in self._worksheets:
            if worksheet.Name == key:
                return worksheet

        raise KeyError(key)


class FakeWorkbook:
    def __init__(
        self,
        name: str,
        full_name: str,
        worksheets: list[FakeWorksheet],
    ):
        self.Name = name
        self.FullName = full_name
        self.Worksheets = FakeWorksheets(worksheets)


class FakeWorkbooks:
    def __init__(self, workbooks: list[FakeWorkbook]):
        self._workbooks = workbooks
        self.Count = len(workbooks)

    def Item(self, key: int):
        return self._workbooks[key - 1]


class FakeExcel:
    def __init__(self, workbooks: list[FakeWorkbook]):
        self.Workbooks = FakeWorkbooks(workbooks)


def test_status_is_ready_when_excel_workbook_sheet_and_headers_are_valid() -> None:
    worksheet = FakeWorksheet(
        DEFAULT_WORKSHEET_NAME,
        REQUIRED_OPTION_QUOTE_HEADERS,
    )
    workbook = FakeWorkbook(
        DEFAULT_WORKBOOK_NAME,
        f"C:/tmp/{DEFAULT_WORKBOOK_NAME}",
        [worksheet],
    )
    excel = FakeExcel([workbook])

    status = check_excel_rtd_connection_status(excel_app=excel)

    assert status.is_ready is True
    assert status.pywin32_available is True
    assert status.excel_running is True
    assert status.workbook_open is True
    assert status.worksheet_available is True
    assert status.required_headers_ok is True
    assert status.missing_headers == ()
    assert status.message == "RTD Excel pronto para leitura."


def test_status_reports_missing_workbook() -> None:
    excel = FakeExcel([])

    status = check_excel_rtd_connection_status(excel_app=excel)

    assert status.is_ready is False
    assert status.pywin32_available is True
    assert status.excel_running is True
    assert status.workbook_open is False
    assert status.worksheet_available is False
    assert status.required_headers_ok is False
    assert status.missing_headers == REQUIRED_OPTION_QUOTE_HEADERS
    assert "Workbook obrigatório não está aberto" in status.message


def test_status_reports_missing_worksheet() -> None:
    workbook = FakeWorkbook(
        DEFAULT_WORKBOOK_NAME,
        f"C:/tmp/{DEFAULT_WORKBOOK_NAME}",
        [],
    )
    excel = FakeExcel([workbook])

    status = check_excel_rtd_connection_status(excel_app=excel)

    assert status.is_ready is False
    assert status.workbook_open is True
    assert status.worksheet_available is False
    assert status.required_headers_ok is False
    assert status.missing_headers == REQUIRED_OPTION_QUOTE_HEADERS
    assert "Aba obrigatória ausente" in status.message


def test_status_reports_missing_required_header() -> None:
    headers = tuple(
        header
        for header in REQUIRED_OPTION_QUOTE_HEADERS
        if header != "iv"
    )
    worksheet = FakeWorksheet(DEFAULT_WORKSHEET_NAME, headers)
    workbook = FakeWorkbook(
        DEFAULT_WORKBOOK_NAME,
        f"C:/tmp/{DEFAULT_WORKBOOK_NAME}",
        [worksheet],
    )
    excel = FakeExcel([workbook])

    status = check_excel_rtd_connection_status(excel_app=excel)

    assert status.is_ready is False
    assert status.workbook_open is True
    assert status.worksheet_available is True
    assert status.required_headers_ok is False
    assert status.missing_headers == ("iv",)
    assert status.message == (
        "Cabeçalho obrigatório ausente na aba RTD_OPTION_QUOTES: iv"
    )


def test_status_accepts_headers_moved_to_different_columns() -> None:
    moved_headers = (
        "vwap",
        "vega",
        "theta",
        "gamma",
        "delta",
        "iv",
        "volume",
        "ask",
        "bid",
        "ultima_quantidade",
        "ultimo_preco",
        "vencimento",
        "strike",
        "call_put",
        "ativo_base",
        "codigo_opcao",
    )
    worksheet = FakeWorksheet(DEFAULT_WORKSHEET_NAME, moved_headers)
    workbook = FakeWorkbook(
        DEFAULT_WORKBOOK_NAME,
        f"C:/tmp/{DEFAULT_WORKBOOK_NAME}",
        [worksheet],
    )
    excel = FakeExcel([workbook])

    status = check_excel_rtd_connection_status(excel_app=excel)

    assert status.is_ready is True
    assert status.detected_headers == moved_headers
    assert status.missing_headers == ()
