from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


# --- INICIO FRENTE 26 EXCEL RTD WORKBOOK DIAGNOSTIC PROBE SCHEMA PUBLIC API ---
# Frente 26: ponte local para o probe diagnostico de workbook Excel RTD
# preferir services/rtd_option_quotes_schema.py como fonte canonica de
# workbook, sheet, headers e campos RTD quando a API publica estiver disponivel.
#
# Sem troca de persistencia.
# Sem troca de fluxo operacional amplo.
# Regra preservada: option_type canonico somente CALL/PUT por extenso;
# C/V sao compra/venda legado, nao tipo canonico de opcao.

try:
    from services import rtd_option_quotes_schema as _frente26_rtd_option_quotes_schema
except Exception:
    _frente26_rtd_option_quotes_schema = None


def _frente26_get_rtd_option_quotes_schema():
    return _frente26_rtd_option_quotes_schema


def _frente26_schema_value(names, fallback=None):
    schema = _frente26_get_rtd_option_quotes_schema()
    if schema is None:
        return fallback

    for name in names:
        value = getattr(schema, name, None)
        if value is None:
            continue
        if callable(value):
            try:
                return value()
            except TypeError:
                continue
            except Exception:
                continue
        return value

    return fallback


def _frente26_public_workbook_name(fallback="LISTA_RTD.xlsm"):
    value = _frente26_schema_value(
        (
            "DEFAULT_WORKBOOK_NAME",
            "WORKBOOK_NAME",
            "RTD_OPTION_QUOTES_WORKBOOK_NAME",
            "get_default_workbook_name",
            "get_workbook_name",
        ),
        fallback,
    )
    return value or fallback


def _frente26_public_sheet_name(fallback="RTD_OPTION_QUOTES"):
    value = _frente26_schema_value(
        (
            "DEFAULT_SHEET_NAME",
            "SHEET_NAME",
            "RTD_OPTION_QUOTES_SHEET_NAME",
            "get_default_sheet_name",
            "get_sheet_name",
        ),
        fallback,
    )
    return value or fallback


def _frente26_public_headers(fallback=()):
    value = _frente26_schema_value(
        (
            "HEADERS",
            "RTD_OPTION_QUOTES_HEADERS",
            "OPTION_QUOTES_HEADERS",
            "get_headers",
            "get_option_quotes_headers",
            "get_rtd_option_quotes_headers",
        ),
        fallback,
    )
    return list(value or fallback)


def _frente26_public_required_headers(fallback=()):
    value = _frente26_schema_value(
        (
            "REQUIRED_HEADERS",
            "REQUIRED_COLUMNS",
            "RTD_OPTION_QUOTES_REQUIRED_HEADERS",
            "get_required_headers",
            "get_required_columns",
            "get_option_quotes_required_headers",
            "get_rtd_option_quotes_required_headers",
        ),
        fallback,
    )
    return list(value or fallback)


def _frente26_public_rtd_fields(fallback=()):
    value = _frente26_schema_value(
        (
            "RTD_FIELDS",
            "OPTION_QUOTES_RTD_FIELDS",
            "get_rtd_fields",
            "get_option_quotes_rtd_fields",
        ),
        fallback,
    )
    return list(value or fallback)


def _frente26_normalize_header(value):
    schema = _frente26_get_rtd_option_quotes_schema()
    normalizer = getattr(schema, "normalize_header", None) if schema is not None else None
    if callable(normalizer):
        try:
            return normalizer(value)
        except Exception:
            pass

    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")


# --- FIM FRENTE 26 EXCEL RTD WORKBOOK DIAGNOSTIC PROBE SCHEMA PUBLIC API ---

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.excel_rtd_workbook_probe import (  # noqa: E402
    DEFAULT_WORKBOOK_NAME,
    ExcelRtdWorkbookProbe,
    ExcelRtdWorkbookProbeConfig,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnostica o workbook RTD aberto no Excel sem gravar banco."
    )
    parser.add_argument(
        "--workbook",
        default=DEFAULT_WORKBOOK_NAME,
        help="Nome do workbook alvo. Padrao: LISTA_RTD.xlsm",
    )
    parser.add_argument(
        "--sheet",
        default=None,
        help="Aba preferencial. Se omitida, usa a primeira aba encontrada.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=8,
        help="Quantidade maxima de linhas para amostra.",
    )
    parser.add_argument(
        "--max-cols",
        type=int,
        default=40,
        help="Quantidade maxima de colunas para amostra.",
    )

    args = parser.parse_args()

    probe = ExcelRtdWorkbookProbe(
        config=ExcelRtdWorkbookProbeConfig(
            workbook_name=args.workbook,
            preferred_sheet=args.sheet,
            max_rows=args.max_rows,
            max_cols=args.max_cols,
        )
    )

    result = probe.run()

    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))

    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
