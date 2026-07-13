from services.rtd_excel_probe_service import ExcelRtdProbeService


class FakeCell:
    def __init__(self, value):
        self.Value = value


class FakeColumns:
    def __init__(self, count):
        self.Count = count


class FakeUsedRange:
    def __init__(self, count):
        self.Columns = FakeColumns(count)


class FakeWorksheet:
    def __init__(self, name, headers):
        self.Name = name
        self._headers = headers
        self.UsedRange = FakeUsedRange(len(headers))

    def Cells(self, row, col):
        if row != 1:
            return FakeCell(None)

        index = col - 1

        if index < 0 or index >= len(self._headers):
            return FakeCell(None)

        return FakeCell(self._headers[index])


class FakeCollection:
    def __init__(self, items):
        self._items = list(items)
        self.Count = len(self._items)

    def Item(self, index):
        return self._items[index - 1]

    def __iter__(self):
        return iter(self._items)


class FakeWorkbook:
    def __init__(self, name, worksheets, full_name=None):
        self.Name = name
        self.FullName = full_name or f"C:/fake/{name}"
        self.Worksheets = FakeCollection(worksheets)


class FakeExcel:
    def __init__(self, workbooks):
        self.Workbooks = FakeCollection(workbooks)


def test_probe_retorna_erro_controlado_quando_excel_nao_esta_aberto():
    service = ExcelRtdProbeService(get_active_excel=lambda: None)

    result = service.probe()

    assert result.ok is False
    assert result.excel_running is False
    assert result.workbook_found is False
    assert "Excel" in result.message


def test_probe_detecta_workbook_ausente():
    excel = FakeExcel(
        [
            FakeWorkbook(
                "OUTRO.xlsm",
                [
                    FakeWorksheet("RTD_OPTION_QUOTES", ["Ativo", "Compra", "Venda"]),
                ],
            )
        ]
    )

    service = ExcelRtdProbeService(get_active_excel=lambda: excel)

    result = service.probe()

    assert result.ok is False
    assert result.excel_running is True
    assert result.workbook_found is False
    assert result.worksheet_found is False


def test_probe_detecta_aba_ausente():
    excel = FakeExcel(
        [
            FakeWorkbook(
                "LISTA_RTD.xlsm",
                [
                    FakeWorksheet("OUTRA_ABA", ["Ativo", "Compra", "Venda"]),
                ],
            )
        ]
    )

    service = ExcelRtdProbeService(get_active_excel=lambda: excel)

    result = service.probe()

    assert result.ok is False
    assert result.excel_running is True
    assert result.workbook_found is True
    assert result.worksheet_found is False


def test_probe_valida_workbook_aba_e_cabecalhos_por_alias():
    excel = FakeExcel(
        [
            FakeWorkbook(
                "LISTA_RTD.xlsm",
                [
                    FakeWorksheet("RTD_OPTION_QUOTES", ["Ativo", "Compra", "Venda"]),
                ],
            )
        ]
    )

    service = ExcelRtdProbeService(get_active_excel=lambda: excel)

    result = service.probe()

    assert result.ok is True
    assert result.excel_running is True
    assert result.workbook_found is True
    assert result.worksheet_found is True
    assert result.workbook_name == "LISTA_RTD.xlsm"
    assert result.worksheet_name == "RTD_OPTION_QUOTES"
    assert result.headers["ativo"] == 1
    assert result.headers["compra"] == 2
    assert result.headers["venda"] == 3
    assert result.missing_headers == []


def test_probe_reporta_cabecalhos_obrigatorios_ausentes():
    excel = FakeExcel(
        [
            FakeWorkbook(
                "LISTA_RTD.xlsm",
                [
                    FakeWorksheet("RTD_OPTION_QUOTES", ["Ativo"]),
                ],
            )
        ]
    )

    service = ExcelRtdProbeService(get_active_excel=lambda: excel)

    result = service.probe()

    assert result.ok is False
    assert result.excel_running is True
    assert result.workbook_found is True
    assert result.worksheet_found is True
    assert result.missing_headers == ["bid", "ask"]


def test_probe_permite_validacao_de_cabecalhos_configuravel():
    excel = FakeExcel(
        [
            FakeWorkbook(
                "LISTA_RTD.xlsm",
                [
                    FakeWorksheet("RTD_OPTION_QUOTES", ["Ticker", "Delta", "Gamma"]),
                ],
            )
        ]
    )

    service = ExcelRtdProbeService(get_active_excel=lambda: excel)

    result = service.probe(required_headers=("ticker", "delta", "gamma"))

    assert result.ok is True
    assert result.missing_headers == []
    assert result.headers["ticker"] == 1
    assert result.headers["delta"] == 2
    assert result.headers["gamma"] == 3


def test_probe_aceita_codigo_opcao_como_alias_de_ticker_real_da_aba_rtd():
    excel = FakeExcel(
        [
            FakeWorkbook(
                "LISTA_RTD.xlsm",
                [
                    FakeWorksheet(
                        "RTD_OPTION_QUOTES",
                        [
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
                        ],
                    ),
                ],
            )
        ]
    )

    service = ExcelRtdProbeService(get_active_excel=lambda: excel)

    result = service.probe()

    assert result.ok is True
    assert result.missing_headers == []
    assert result.headers["codigo_opcao"] == 1
    assert result.headers["bid"] == 8
    assert result.headers["ask"] == 9
