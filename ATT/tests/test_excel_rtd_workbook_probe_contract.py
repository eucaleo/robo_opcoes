from services.excel_rtd_workbook_probe import (
    ExcelRtdProbeError,
    ExcelRtdWorkbookProbe,
    ExcelRtdWorkbookProbeConfig,
    _normalize_excel_value_matrix,
)


class FakeExcelAdapter:
    def __init__(self, workbooks=None, samples=None, error=None):
        self.workbooks = workbooks or []
        self.samples = samples or {}
        self.error = error
        self.read_calls = []

    def list_workbooks(self):
        if self.error:
            raise self.error

        return self.workbooks

    def read_sheet_sample(self, *, workbook_full_name, sheet_name, max_rows, max_cols):
        self.read_calls.append(
            {
                "workbook_full_name": workbook_full_name,
                "sheet_name": sheet_name,
                "max_rows": max_rows,
                "max_cols": max_cols,
            }
        )

        return self.samples[(workbook_full_name, sheet_name)]


def test_probe_returns_controlled_status_when_excel_is_unavailable():
    probe = ExcelRtdWorkbookProbe(
        adapter=FakeExcelAdapter(error=ExcelRtdProbeError("Excel nao esta aberto"))
    )

    result = probe.run()

    assert result.ok is False
    assert result.status == "excel_unavailable"
    assert "Excel nao esta aberto" in result.message


def test_probe_returns_workbook_not_found_with_workbooks_seen():
    adapter = FakeExcelAdapter(
        workbooks=[
            {
                "name": "OUTRA_PLANILHA.xlsx",
                "full_name": "C:/tmp/OUTRA_PLANILHA.xlsx",
                "sheets": ["Planilha1"],
            }
        ]
    )

    probe = ExcelRtdWorkbookProbe(adapter=adapter)

    result = probe.run()

    assert result.ok is False
    assert result.status == "workbook_not_found"
    assert result.workbooks_seen == ["OUTRA_PLANILHA.xlsx"]


def test_probe_finds_lista_rtd_and_reads_first_sheet_sample():
    adapter = FakeExcelAdapter(
        workbooks=[
            {
                "name": "LISTA_RTD.xlsm",
                "full_name": "C:/users/eucal/projeto/LISTA_RTD.xlsm",
                "sheets": ["RTD_LINKS", "OUTRA"],
            }
        ],
        samples={
            ("C:/users/eucal/projeto/LISTA_RTD.xlsm", "RTD_LINKS"): {
                "headers": ["codigo_opcao", "bid", "ask", "vwap"],
                "rows": [["BOVAG195", 1.2, 1.3, 100.5]],
                "row_count": 2,
                "col_count": 4,
            }
        },
    )

    probe = ExcelRtdWorkbookProbe(adapter=adapter)

    result = probe.run()

    assert result.ok is True
    assert result.status == "ok"
    assert result.workbook_name == "LISTA_RTD.xlsm"
    assert result.selected_sheet == "RTD_LINKS"
    assert result.headers == ["codigo_opcao", "bid", "ask", "vwap"]
    assert result.sample_rows == [["BOVAG195", 1.2, 1.3, 100.5]]
    assert result.row_count == 2
    assert result.col_count == 4
    assert adapter.read_calls == [
        {
            "workbook_full_name": "C:/users/eucal/projeto/LISTA_RTD.xlsm",
            "sheet_name": "RTD_LINKS",
            "max_rows": 8,
            "max_cols": 40,
        }
    ]


def test_probe_respects_preferred_sheet_when_available():
    adapter = FakeExcelAdapter(
        workbooks=[
            {
                "name": "LISTA_RTD.xlsm",
                "full_name": "C:/LISTA_RTD.xlsm",
                "sheets": ["CAPA", "RTD_LINKS"],
            }
        ],
        samples={
            ("C:/LISTA_RTD.xlsm", "RTD_LINKS"): {
                "headers": ["ativo", "ultimo_preco"],
                "rows": [["BOVA11", 120.0]],
                "row_count": 2,
                "col_count": 2,
            }
        },
    )

    probe = ExcelRtdWorkbookProbe(
        config=ExcelRtdWorkbookProbeConfig(preferred_sheet="RTD_LINKS"),
        adapter=adapter,
    )

    result = probe.run()

    assert result.ok is True
    assert result.selected_sheet == "RTD_LINKS"


def test_probe_returns_sheet_not_found_when_workbook_has_no_sheets():
    adapter = FakeExcelAdapter(
        workbooks=[
            {
                "name": "LISTA_RTD.xlsm",
                "full_name": "C:/LISTA_RTD.xlsm",
                "sheets": [],
            }
        ]
    )

    probe = ExcelRtdWorkbookProbe(adapter=adapter)

    result = probe.run()

    assert result.ok is False
    assert result.status == "sheet_not_found"


def test_normalize_excel_value_matrix_handles_none_scalar_row_and_matrix():
    assert _normalize_excel_value_matrix(None) == []
    assert _normalize_excel_value_matrix("A1") == [["A1"]]
    assert _normalize_excel_value_matrix(("A", "B")) == [["A", "B"]]
    assert _normalize_excel_value_matrix((("A", "B"), (1, 2))) == [["A", "B"], [1, 2]]
