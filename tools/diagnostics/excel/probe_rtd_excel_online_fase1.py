

# --- INICIO FRENTE 25 EXCEL RTD DIAGNOSTIC PROBE SCHEMA PUBLIC API ---
# Frente 25: ponte local para o probe diagnostico Excel RTD preferir
# services/rtd_option_quotes_schema.py como fonte canonica de workbook,
# sheet, headers e campos RTD quando a API publica estiver disponivel.
#
# Sem troca de persistencia.
# Sem troca de fluxo operacional amplo.
# Regra preservada: option_type canonico somente CALL/PUT por extenso;
# C/V sao compra/venda legado, nao tipo canonico de opcao.

try:
    from services import rtd_option_quotes_schema as _frente25_rtd_option_quotes_schema
except Exception:
    _frente25_rtd_option_quotes_schema = None


def _frente25_get_rtd_option_quotes_schema():
    return _frente25_rtd_option_quotes_schema


def _frente25_call_schema_public_api(api_name, fallback=None):
    schema = _frente25_get_rtd_option_quotes_schema()
    if schema is None:
        return fallback

    api = getattr(schema, api_name, None)
    if callable(api):
        try:
            return api()
        except TypeError:
            return fallback
        except Exception:
            return fallback

    return fallback


def _frente25_first_schema_value(api_names, fallback=None):
    marker = object()
    for api_name in api_names:
        value = _frente25_call_schema_public_api(api_name, marker)
        if value is not marker:
            return value
    return fallback


def _frente25_as_list(value):
    if value is None:
        return None
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    return value


def _frente25_apply_rtd_option_quotes_schema_defaults():
    workbook_fallback = (
        globals().get("DEFAULT_WORKBOOK_NAME")
        or globals().get("RTD_WORKBOOK_NAME")
        or globals().get("WORKBOOK_NAME")
    )
    sheet_fallback = (
        globals().get("DEFAULT_SHEET_NAME")
        or globals().get("RTD_SHEET_NAME")
        or globals().get("SHEET_NAME")
    )
    headers_fallback = (
        globals().get("HEADERS")
        or globals().get("RTD_HEADERS")
        or globals().get("EXPECTED_HEADERS")
    )
    fields_fallback = (
        globals().get("RTD_FIELDS")
        or globals().get("FIELDS")
    )
    required_fallback = (
        globals().get("REQUIRED_HEADERS")
        or globals().get("REQUIRED_FIELDS")
        or headers_fallback
    )

    workbook_name = _frente25_first_schema_value(
        (
            "get_rtd_option_quotes_workbook_name",
            "get_option_quotes_workbook_name",
            "get_default_workbook_name",
            "get_workbook_name",
        ),
        workbook_fallback,
    )
    sheet_name = _frente25_first_schema_value(
        (
            "get_rtd_option_quotes_sheet_name",
            "get_option_quotes_sheet_name",
            "get_default_sheet_name",
            "get_sheet_name",
        ),
        sheet_fallback,
    )
    headers = _frente25_as_list(
        _frente25_first_schema_value(
            (
                "get_rtd_option_quotes_headers",
                "get_option_quote_headers",
                "get_option_quotes_headers",
                "get_excel_headers",
                "get_headers",
            ),
            headers_fallback,
        )
    )
    fields = _frente25_as_list(
        _frente25_first_schema_value(
            (
                "get_rtd_option_quotes_fields",
                "get_option_quote_fields",
                "get_option_quotes_fields",
                "get_rtd_fields",
                "get_fields",
            ),
            fields_fallback,
        )
    )
    required_headers = _frente25_as_list(
        _frente25_first_schema_value(
            (
                "get_rtd_option_quotes_required_headers",
                "get_option_quote_required_headers",
                "get_required_headers",
                "get_required_fields",
            ),
            required_fallback,
        )
    )

    if workbook_name:
        globals()["DEFAULT_WORKBOOK_NAME"] = workbook_name
        if "RTD_WORKBOOK_NAME" in globals():
            globals()["RTD_WORKBOOK_NAME"] = workbook_name
        if "WORKBOOK_NAME" in globals():
            globals()["WORKBOOK_NAME"] = workbook_name

    if sheet_name:
        globals()["DEFAULT_SHEET_NAME"] = sheet_name
        if "RTD_SHEET_NAME" in globals():
            globals()["RTD_SHEET_NAME"] = sheet_name
        if "SHEET_NAME" in globals():
            globals()["SHEET_NAME"] = sheet_name

    if headers:
        globals()["HEADERS"] = headers
        if "RTD_HEADERS" in globals():
            globals()["RTD_HEADERS"] = headers
        if "EXPECTED_HEADERS" in globals():
            globals()["EXPECTED_HEADERS"] = headers

    if fields:
        globals()["RTD_FIELDS"] = fields
        if "FIELDS" in globals():
            globals()["FIELDS"] = fields

    if required_headers:
        globals()["REQUIRED_HEADERS"] = required_headers
        if "REQUIRED_FIELDS" in globals():
            globals()["REQUIRED_FIELDS"] = required_headers


_frente25_apply_rtd_option_quotes_schema_defaults()
# --- FIM FRENTE 25 EXCEL RTD DIAGNOSTIC PROBE SCHEMA PUBLIC API ---
