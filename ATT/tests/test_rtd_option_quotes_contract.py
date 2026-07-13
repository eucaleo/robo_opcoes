import pytest

from ATT.rtd_option_quotes_contract import (
    INPUT_FIELD,
    RESULT_FIELDS,
    REQUIRED_FIELDS,
    RtdOptionQuotesContractError,
    build_header_map,
    input_field,
    required_fields,
    result_fields,
    rtd_functions,
    validate_headers,
)


def test_required_fields_list_all_expected_headers():
    assert required_fields() == (
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
    )


def test_rtd_functions_expose_expected_mapping():
    functions = rtd_functions()

    assert functions["codigo_opcao"] == "entrada do sistema"
    assert functions["ativo_base"] == "QUOTE.UNDERLYING_SYMBOL"
    assert functions["call_put"] == "QUOTE.OPTION_TYPE"
    assert functions["strike"] == "QUOTE.STRIKE_PRICE"
    assert functions["vencimento"] == "QUOTE.MATURITYDATE"
    assert functions["ultimo_preco"] == "QUOTE.LAST_TRADE_PRICE"
    assert functions["ultima_quantidade"] == "QUOTE.LAST_TRADE_QUANTITY"
    assert functions["bid"] == "QUOTE.BID_PRICE"
    assert functions["ask"] == "QUOTE.ASK_PRICE"
    assert functions["volume"] == "QUOTE.VOLUME"
    assert functions["iv"] == "QUOTE.IMPLIED_VOLATILITY"
    assert functions["delta"] == "QUOTE.DELTA"
    assert functions["gamma"] == "QUOTE.GAMMA"
    assert functions["theta"] == "QUOTE.THETA"
    assert functions["vega"] == "QUOTE.VEGA"
    assert functions["vwap"] == "QUOTE.VWAP"


def test_input_field_is_codigo_opcao():
    assert input_field() == "codigo_opcao"
    assert INPUT_FIELD == "codigo_opcao"


def test_result_fields_exclude_only_input_field():
    assert "codigo_opcao" not in result_fields()
    assert result_fields() == RESULT_FIELDS
    assert set(result_fields()) == set(REQUIRED_FIELDS) - {"codigo_opcao"}


def test_validate_headers_accepts_complete_contract():
    header_map = validate_headers(required_fields())

    assert header_map.column_index("codigo_opcao") == 0
    assert header_map.column_index("ativo_base") == 1
    assert header_map.column_index("vwap") == 15


def test_validate_headers_accepts_different_order_and_extra_fields():
    headers = (
        "campo_extra",
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

    header_map = validate_headers(headers)

    assert header_map.column_index("codigo_opcao") == 16
    assert header_map.column_index("vwap") == 1
    assert header_map.column_index("campo_extra") == 0


def test_input_column_index_returns_codigo_opcao_position():
    headers = ("ativo_base", "codigo_opcao", *required_fields()[2:])

    header_map = validate_headers(headers)

    assert header_map.input_column_index() == 1


def test_result_column_indexes_return_only_rtd_result_fields():
    header_map = validate_headers(required_fields())

    result_indexes = header_map.result_column_indexes()

    assert "codigo_opcao" not in result_indexes
    assert result_indexes["ativo_base"] == 1
    assert result_indexes["vwap"] == 15


def test_validate_headers_rejects_missing_required_header():
    headers = tuple(field for field in required_fields() if field != "vwap")

    with pytest.raises(RtdOptionQuotesContractError, match="vwap"):
        validate_headers(headers)


def test_validate_headers_rejects_duplicate_header():
    headers = list(required_fields())
    headers.append("vwap")

    with pytest.raises(RtdOptionQuotesContractError, match="duplicado"):
        validate_headers(headers)


def test_validate_headers_rejects_empty_header():
    headers = list(required_fields())
    headers.append(" ")

    with pytest.raises(RtdOptionQuotesContractError, match="vazio"):
        validate_headers(headers)


def test_validate_headers_rejects_non_text_header():
    headers = list(required_fields())
    headers.append(123)

    with pytest.raises(RtdOptionQuotesContractError, match="esperado texto"):
        validate_headers(headers)


def test_column_index_rejects_unknown_field():
    header_map = build_header_map(required_fields())

    with pytest.raises(RtdOptionQuotesContractError, match="campo nao mapeado"):
        header_map.column_index("campo_inexistente")
