# Frente 21D - consumo incremental da API publica workbook/sheet
from __future__ import annotations

# --- INICIO FRENTE 27 RTD EXCEL PROBE SERVICE SCHEMA REQUIRED HEADERS CONTRACT ---
# Frente 27: ponte local para o service de probe Excel RTD preferir
# services/rtd_option_quotes_schema.py como fonte canonica dos headers
# obrigatorios de rtd_option_quotes.
#
# Objetivo: evitar que o probe aprove planilha incompleta validando apenas
# ticker, bid e ask quando a API publica de schema estiver disponivel.
#
# Sem troca de persistencia.
# Sem troca operacional ampla.
# Regra preservada: option_type canonico somente CALL/PUT por extenso;
# C/V sao compra/venda legado.

try:
    from services import rtd_option_quotes_schema as _frente27_rtd_option_quotes_schema
except Exception:
    _frente27_rtd_option_quotes_schema = None


def _frente27_get_rtd_option_quotes_schema():
    return _frente27_rtd_option_quotes_schema


def _frente27_as_tuple(value):
    if value is None:
        return tuple()
    if isinstance(value, str):
        return (value,)
    try:
        return tuple(value)
    except TypeError:
        return tuple()


def _frente27_get_required_headers():
    schema = _frente27_get_rtd_option_quotes_schema()

    if schema is not None:
        for name in (
            "get_required_headers",
            "get_required_rtd_headers",
            "get_rtd_required_headers",
            "get_option_quotes_required_headers",
            "get_option_quote_required_headers",
            "required_headers",
            "headers",
            "get_headers",
            "get_rtd_headers",
            "get_option_quotes_headers",
            "get_option_quote_headers",
        ):
            candidate = getattr(schema, name, None)
            if candidate is None:
                continue
            try:
                value = candidate() if callable(candidate) else candidate
            except Exception:
                continue
            headers = _frente27_as_tuple(value)
            if headers:
                return headers

        for name in (
            "REQUIRED_HEADERS",
            "RTD_REQUIRED_HEADERS",
            "OPTION_QUOTES_REQUIRED_HEADERS",
            "OPTION_QUOTE_REQUIRED_HEADERS",
            "HEADERS",
            "RTD_HEADERS",
            "RTD_FIELDS",
        ):
            value = getattr(schema, name, None)
            headers = _frente27_as_tuple(value)
            if headers:
                return headers

    return (
        "ticker",
        "bid",
        "ask",
        "last",
        "volume",
        "option_type",
        "strike",
        "expiration_date",
        "delta",
        "gamma",
        "theta",
        "vega",
    )


# --- FIM FRENTE 27 RTD EXCEL PROBE SERVICE SCHEMA REQUIRED HEADERS CONTRACT ---
def _frente21d_rtd_option_quotes_schema_contract():
    """
    Obtém o contrato canônico RTD Option Quotes.

    Reusa o helper introduzido em frentes anteriores quando disponível e mantém
    fallback local para evitar troca operacional ampla.
    """
    helper = globals().get("_frente21a_rtd_option_quotes_schema_contract")
    if callable(helper):
        return helper()

    from services import rtd_option_quotes_schema

    return rtd_option_quotes_schema


def _frente21d_schema_public_text(function_name, candidate_names, default):
    """
    Lê texto público do schema, preferindo API pública e aceitando constantes
    históricas apenas como compatibilidade.
    """
    schema = _frente21d_rtd_option_quotes_schema_contract()

    public_getter = getattr(schema, function_name, None)
    if callable(public_getter):
        value = public_getter()
        if isinstance(value, str) and value.strip():
            return value.strip()

    for name in candidate_names:
        value = getattr(schema, name, None)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return str(default).strip()


def _canonical_rtd_option_quotes_workbook_name(default=None):
    """
    Nome canônico da pasta de trabalho RTD Option Quotes a partir do schema.
    """
    return _frente21d_schema_public_text(
        "rtd_option_quotes_workbook_name",
        (
            "RTD_OPTION_QUOTES_WORKBOOK_NAME",
            "DEFAULT_RTD_OPTION_QUOTES_WORKBOOK_NAME",
            "DEFAULT_WORKBOOK_NAME",
            "WORKBOOK_NAME",
            "EXCEL_WORKBOOK_NAME",
            "DEFAULT_EXCEL_WORKBOOK_NAME",
        ),
        default or "LISTA_RTD.xlsm",
    )


def _canonical_rtd_option_quotes_sheet_name(default=None):
    """
    Nome canônico da planilha RTD Option Quotes a partir do schema.
    """
    return _frente21d_schema_public_text(
        "rtd_option_quotes_sheet_name",
        (
            "RTD_OPTION_QUOTES_SHEET_NAME",
            "DEFAULT_RTD_OPTION_QUOTES_SHEET_NAME",
            "DEFAULT_SHEET_NAME",
            "SHEET_NAME",
            "EXCEL_SHEET_NAME",
            "DEFAULT_EXCEL_SHEET_NAME",
        ),
        default or "RTD_OPTION_QUOTES",
    )


"""Probe controlado do Excel RTD BTG Online.

Este módulo faz apenas diagnóstico de conexão com Excel/Workbook/Aba.
Ele não abre Excel, não grava banco, não dispara subprocessos e não inicia coleta.
"""


# Frente 21A - RTD Option Quotes canonical schema probe bridge
def _frente21a_rtd_option_quotes_schema_contract():
    """
    Retorna o módulo de contrato canônico RTD Option Quotes.

    Mantido como ponte local para adoção incremental do contrato
    `services/rtd_option_quotes_schema.py` sem trocar fluxo operacional,
    persistência, bridge ou importadores nesta frente.
    """
    from services import rtd_option_quotes_schema

    return rtd_option_quotes_schema

def _frente21b_headers_from_schema_value(value: object) -> tuple[str, ...]:
    """
    Extrai headers/fields consumíveis de diferentes formatos possíveis do
    contrato canônico RTD Option Quotes.

    Esta função existe para evitar acoplamento a um único nome interno de
    constante em services/rtd_option_quotes_schema.py.
    """
    if value is None:
        return ()

    if isinstance(value, str):
        text = value.strip()
        return (text,) if text else ()

    if isinstance(value, dict):
        if value and all(isinstance(key, str) for key in value.keys()):
            return tuple(str(key).strip() for key in value.keys() if str(key).strip())

        extracted: list[str] = []
        for item in value.values():
            extracted.extend(_frente21b_headers_from_schema_value(item))
        return tuple(dict.fromkeys(extracted))

    if isinstance(value, (list, tuple, set, frozenset)):
        ordered = list(value)
        if isinstance(value, (set, frozenset)):
            ordered = sorted(ordered, key=lambda item: str(item))

        if ordered and all(isinstance(item, str) for item in ordered):
            return tuple(str(item).strip() for item in ordered if str(item).strip())

        extracted: list[str] = []
        for item in ordered:
            if isinstance(item, dict):
                for key in (
                    "header",
                    "headers",
                    "name",
                    "field",
                    "fields",
                    "column",
                    "columns",
                    "db_column",
                    "excel_header",
                    "rtd_field",
                    "canonical_name",
                ):
                    if key in item:
                        extracted.extend(_frente21b_headers_from_schema_value(item.get(key)))
            else:
                for attr in (
                    "header",
                    "name",
                    "field",
                    "column",
                    "db_column",
                    "excel_header",
                    "rtd_field",
                    "canonical_name",
                ):
                    if hasattr(item, attr):
                        extracted.extend(_frente21b_headers_from_schema_value(getattr(item, attr)))

        return tuple(dict.fromkeys(str(item).strip() for item in extracted if str(item).strip()))

    for attr in (
        "headers",
        "required_headers",
        "fields",
        "columns",
        "field_names",
        "column_names",
    ):
        if hasattr(value, attr):
            headers = _frente21b_headers_from_schema_value(getattr(value, attr))
            if headers:
                return headers

    return ()


def _frente21b_text_tokens(*values: object) -> set[str]:
    text = " ".join(str(value) for value in values if value is not None).upper()
    return set(re.findall(r"[A-Z0-9_]+", text))


def _frente21b_header_score(name: str, headers: tuple[str, ...]) -> int:
    """
    Pontua candidatos para evitar pegar listas públicas não relacionadas.

    O objetivo é preferir constantes/estruturas com sinais de contrato RTD
    Option Quotes: headers, fields, columns, ticker/symbol, bid/ask etc.
    """
    if not headers:
        return 0

    tokens = _frente21b_text_tokens(name, *headers)

    score = 0

    for token in ("HEADER", "HEADERS", "FIELD", "FIELDS", "COLUMN", "COLUMNS"):
        if token in tokens:
            score += 8

    for token in ("RTD", "OPTION", "OPTIONS", "QUOTE", "QUOTES", "CANONICAL", "REQUIRED"):
        if token in tokens:
            score += 4

    if len(headers) >= 3:
        score += 6

    if tokens & {"TICKER", "SYMBOL", "CODIGO", "CÓDIGO", "ATIVO", "UNDERLYING"}:
        score += 8

    if tokens & {"BID", "COMPRA"}:
        score += 5

    if tokens & {"ASK", "VENDA"}:
        score += 5

    if tokens & {"LAST", "LAST_PRICE", "ULTIMO", "ÚLTIMO", "PRECO", "PREÇO", "PRICE"}:
        score += 3

    if tokens & {"SQL", "QUERY", "CREATE", "INSERT", "UPDATE", "DELETE", "DROP"}:
        score -= 20

    return score


def _canonical_required_rtd_option_quote_headers() -> tuple[str, ...]:
    """
    Retorna headers obrigatórios a partir do contrato canônico RTD Option Quotes.

    Frente 21B:
    - o consumidor continua sendo o probe RTD Excel;
    - a fonte de verdade é services/rtd_option_quotes_schema.py;
    - não há dependência de um único nome interno de constante;
    - não há troca operacional ampla.
    """
    schema = _frente21a_rtd_option_quotes_schema_contract()
    public_required_headers = getattr(schema, "rtd_option_quotes_required_headers", None)
    if callable(public_required_headers):
        headers = public_required_headers()
        if headers:
            return tuple(str(item) for item in headers)


    preferred_names = (
        "REQUIRED_HEADERS",
        "REQUIRED_FIELDS",
        "REQUIRED_COLUMNS",
        "RTD_OPTION_QUOTES_REQUIRED_HEADERS",
        "RTD_OPTION_QUOTES_REQUIRED_FIELDS",
        "RTD_OPTION_QUOTES_REQUIRED_COLUMNS",
        "REQUIRED_RTD_OPTION_QUOTES_HEADERS",
        "CANONICAL_REQUIRED_HEADERS",
        "CANONICAL_REQUIRED_FIELDS",
        "HEADERS",
        "FIELDS",
        "COLUMNS",
        "RTD_FIELDS",
        "RTD_OPTION_QUOTES_HEADERS",
        "RTD_OPTION_QUOTES_FIELDS",
        "RTD_OPTION_QUOTES_COLUMNS",
        "CANONICAL_HEADERS",
        "CANONICAL_FIELDS",
        "CANONICAL_COLUMNS",
        "SCHEMA",
        "OPTION_QUOTES_SCHEMA",
        "RTD_OPTION_QUOTES_SCHEMA",
    )

    for name in preferred_names:
        value = getattr(schema, name, None)
        headers = _frente21b_headers_from_schema_value(value)
        if headers:
            return headers

    ranked: list[tuple[int, str, tuple[str, ...]]] = []

    for name in dir(schema):
        if name.startswith("_"):
            continue

        try:
            value = getattr(schema, name)
        except Exception:
            continue

        if callable(value):
            continue

        headers = _frente21b_headers_from_schema_value(value)
        score = _frente21b_header_score(name, headers)

        if score > 0:
            ranked.append((score, name, headers))

    if ranked:
        ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return ranked[0][2]

    raise RuntimeError(
        "Contrato RTD Option Quotes sem headers consumíveis. "
        "Esperado em services/rtd_option_quotes_schema.py."
    )

def _normalize_rtd_option_quote_header_via_contract(value: object) -> str:
    """
    Normaliza header pelo contrato canônico quando a função estiver disponível.

    Fallback mínimo preserva compatibilidade local do probe e não cria novo
    contrato paralelo.
    """
    schema = _frente21a_rtd_option_quotes_schema_contract()
    normalize = getattr(schema, "normalize_header", None)

    if callable(normalize):
        return str(normalize(value))

    return str(value or "").strip().lower().replace(" ", "_")

from dataclasses import asdict, dataclass, field
import os
import re
import unicodedata
from typing import Any, Callable, Iterable


DEFAULT_WORKBOOK_NAME = _canonical_rtd_option_quotes_workbook_name("LISTA_RTD.xlsm")
DEFAULT_WORKSHEET_NAME = "RTD_OPTION_QUOTES"

DEFAULT_REQUIRED_HEADERS = (
    "ticker",
    "bid",
    "ask",
)

HEADER_ALIASES = {
    "ticker": (
        "ticker",
        "ativo",
        "codigo",
        "codigo_ativo",
        "codigo_opcao",
        "opcao",
        "codigo_da_opcao",
        "symbol",
        "underlying",
    ),
    "bid": (
        "bid",
        "compra",
        "preco_compra",
        "best_bid",
    ),
    "ask": (
        "ask",
        "venda",
        "preco_venda",
        "best_ask",
    ),
}


class ExcelProbeDependencyError(RuntimeError):
    """Dependência COM/pywin32 indisponível."""


class ExcelNotRunningError(RuntimeError):
    """Excel não está aberto ou não está registrado no COM ativo."""


@dataclass(frozen=True)
class ExcelRtdProbeResult:
    ok: bool = False
    excel_running: bool = False
    workbook_found: bool = False
    worksheet_found: bool = False
    workbook_name: str | None = None
    workbook_path: str | None = None
    worksheet_name: str | None = None
    headers: dict[str, int] = field(default_factory=dict)
    raw_headers: dict[str, int] = field(default_factory=dict)
    required_headers: list[str] = field(default_factory=list)
    missing_headers: list[str] = field(default_factory=list)
    message: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExcelRtdProbeService:
    """Serviço de diagnóstico do Excel RTD.

    A dependência de Excel pode ser injetada nos testes via get_active_excel.
    Em produção, usa get_active_excel_application("Excel.Application").
    """

    def __init__(
        self,
        get_active_excel: Callable[[], Any] | None = None,
    ) -> None:
        self._get_active_excel = get_active_excel or _default_get_active_excel

    def probe(
        self,
        workbook_name: str = DEFAULT_WORKBOOK_NAME,
        worksheet_name: str = DEFAULT_WORKSHEET_NAME,
        required_headers: Iterable[str] = DEFAULT_REQUIRED_HEADERS,
    ) -> ExcelRtdProbeResult:
        required_headers_list = list(required_headers)

        try:
            excel = self._get_active_excel()
        except ExcelNotRunningError as exc:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Excel não está aberto ou não foi encontrado via COM ativo.",
                error=str(exc),
            )
        except ExcelProbeDependencyError as exc:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Dependência de automação Excel indisponível.",
                error=str(exc),
            )
        except Exception as exc:  # pragma: no cover - defesa contra COM instável
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Falha inesperada ao acessar Excel via COM.",
                error=str(exc),
            )

        if excel is None:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=False,
                required_headers=required_headers_list,
                message="Excel não retornou instância ativa.",
            )

        workbook = _find_workbook(excel, workbook_name)

        if workbook is None:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=True,
                workbook_found=False,
                required_headers=required_headers_list,
                message=f"Workbook '{workbook_name}' não encontrado no Excel ativo.",
            )

        found_workbook_name = _safe_str(getattr(workbook, "Name", None))
        found_workbook_path = _safe_str(getattr(workbook, "FullName", None))

        worksheet = _find_worksheet(workbook, worksheet_name)

        if worksheet is None:
            return ExcelRtdProbeResult(
                ok=False,
                excel_running=True,
                workbook_found=True,
                worksheet_found=False,
                workbook_name=found_workbook_name,
                workbook_path=found_workbook_path,
                required_headers=required_headers_list,
                message=(
                    f"Workbook '{workbook_name}' encontrado, "
                    f"mas aba '{worksheet_name}' não localizada."
                ),
            )

        headers, raw_headers = _read_header_row(worksheet)
        missing_headers = _missing_required_headers(headers, required_headers_list)

        ok = len(missing_headers) == 0

        return ExcelRtdProbeResult(
            ok=ok,
            excel_running=True,
            workbook_found=True,
            worksheet_found=True,
            workbook_name=found_workbook_name,
            workbook_path=found_workbook_path,
            worksheet_name=_safe_str(getattr(worksheet, "Name", None)),
            headers=headers,
            raw_headers=raw_headers,
            required_headers=required_headers_list,
            missing_headers=missing_headers,
            message=(
                "Probe Excel RTD validado com sucesso."
                if ok
                else "Probe Excel RTD encontrou cabeçalhos obrigatórios ausentes."
            ),
        )


def _default_get_active_excel() -> Any:
    try:
        from services.excel_rtd_com_access import get_active_excel_application, import_win32com_client
        import_win32com_client()
    except ModuleNotFoundError as exc:
        raise ExcelProbeDependencyError(
            "Módulo win32com.client não disponível. Instale pywin32 no ambiente Windows."
        ) from exc

    try:
        return get_active_excel_application("Excel.Application")
    except Exception as exc:
        raise ExcelNotRunningError(
            "Excel.Application não encontrado via GetActiveObject."
        ) from exc


def _find_workbook(excel: Any, workbook_name: str) -> Any | None:
    expected = workbook_name.casefold()

    for workbook in _iter_com_collection(getattr(excel, "Workbooks", [])):
        name = _safe_str(getattr(workbook, "Name", None)).casefold()
        full_name = _safe_str(getattr(workbook, "FullName", None))
        basename = os.path.basename(full_name).casefold() if full_name else ""

        if name == expected or basename == expected:
            return workbook

    return None


def _find_worksheet(workbook: Any, worksheet_name: str) -> Any | None:
    expected = worksheet_name.casefold()

    for worksheet in _iter_com_collection(getattr(workbook, "Worksheets", [])):
        name = _safe_str(getattr(worksheet, "Name", None)).casefold()

        if name == expected:
            return worksheet

    return None


def _read_header_row(worksheet: Any) -> tuple[dict[str, int], dict[str, int]]:
    headers: dict[str, int] = {}
    raw_headers: dict[str, int] = {}

    max_columns = _used_range_columns_count(worksheet)

    for col in range(1, max_columns + 1):
        value = _cell_value(worksheet, 1, col)

        if value is None:
            continue

        raw = str(value).strip()

        if not raw:
            continue

        normalized = normalize_header(raw)

        if not normalized:
            continue

        headers.setdefault(normalized, col)
        raw_headers.setdefault(raw, col)

    return headers, raw_headers


def _used_range_columns_count(worksheet: Any) -> int:
    used_range = getattr(worksheet, "UsedRange", None)

    if used_range is None:
        return 256

    columns = getattr(used_range, "Columns", None)

    if columns is None:
        return 256

    count = getattr(columns, "Count", None)

    try:
        parsed = int(count)
    except (TypeError, ValueError):
        return 256

    if parsed <= 0:
        return 256

    return min(parsed, 1024)


def _cell_value(worksheet: Any, row: int, col: int) -> Any:
    cell_accessor = getattr(worksheet, "Cells", None)

    if cell_accessor is None:
        return None

    try:
        cell = cell_accessor(row, col)
    except TypeError:
        return None

    return getattr(cell, "Value", None)


def _missing_required_headers(
    normalized_headers: dict[str, int],
    required_headers: Iterable[str],
) -> list[str]:
    missing: list[str] = []

    for required in required_headers:
        aliases = _aliases_for(required)

        if not any(alias in normalized_headers for alias in aliases):
            missing.append(required)

    return missing


def _aliases_for(header: str) -> tuple[str, ...]:
    normalized = normalize_header(header)
    aliases = {normalized}

    for alias in HEADER_ALIASES.get(normalized, ()):
        alias_normalized = normalize_header(alias)

        if alias_normalized:
            aliases.add(alias_normalized)

    return tuple(sorted(aliases))


def normalize_header(value: Any) -> str:
    if value is None:
        return ""

    text = str(value).strip().casefold()

    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")

    return text


def _iter_com_collection(collection: Any) -> Iterable[Any]:
    count = getattr(collection, "Count", None)
    item = getattr(collection, "Item", None)

    if count is not None and item is not None:
        try:
            parsed_count = int(count)
        except (TypeError, ValueError):
            parsed_count = 0

        if parsed_count > 0:
            for index in range(1, parsed_count + 1):
                yield item(index)

            return

    try:
        yield from collection
    except TypeError:
        return


def _safe_str(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()

    return text or None
