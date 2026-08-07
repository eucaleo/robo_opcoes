from __future__ import annotations

import sqlite3
import argparse
import os
import re
import time
from pathlib import Path
import win32com.client

# Frente 66: boundary de SQL local para services/rtd_option_quotes_excel_populator.py.
# SQL direto tolerado nesta camada por estar em repositories.

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
_frente_22a_headers = rtd_option_quotes_excel_populator_headers()
_frente_22a_required_headers = rtd_option_quotes_excel_populator_required_headers()
_frente_22a_workbook_name = rtd_option_quotes_excel_populator_workbook_name()
_frente_22a_sheet_name = rtd_option_quotes_excel_populator_sheet_name()

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
def validate_database(db_path):
    if not db_path.exists():
        raise FileNotFoundError(f"Banco não encontrado: {db_path}")

    required_tables = {
        "structures",
        "structure_legs",
        "rtd_option_quotes",
    }

    with sqlite3.connect(db_path) as con:
        rows = con.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    existing_tables = {row[0] for row in rows}
    missing_tables = required_tables - existing_tables

    if missing_tables:
        raise RuntimeError(
            "Tabelas obrigatórias ausentes no banco: "
            + ", ".join(sorted(missing_tables))
        )
def load_option_codes_from_db(db_path=None, include_archived=False):
    db_path = Path(db_path or get_db_path())
    validate_database(db_path)

    codes = set()

    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row

        if include_archived:
            sql_legs = """
                SELECT DISTINCT l.symbol AS symbol
                FROM structure_legs l
                JOIN structures s ON s.id = l.structure_id
                WHERE l.symbol IS NOT NULL
                  AND TRIM(l.symbol) <> ''
            """
        else:
            sql_legs = """
                SELECT DISTINCT l.symbol AS symbol
                FROM structure_legs l
                JOIN structures s ON s.id = l.structure_id
                WHERE l.symbol IS NOT NULL
                  AND TRIM(l.symbol) <> ''
                  AND COALESCE(s.status, 'active') = 'active'
            """

        sql_cache = """
            SELECT DISTINCT codigo_opcao AS symbol
            FROM rtd_option_quotes
            WHERE codigo_opcao IS NOT NULL
              AND TRIM(codigo_opcao) <> ''
        """

        for row in con.execute(sql_legs):
            symbol = normalize_symbol(row["symbol"])
            if is_option_code(symbol):
                codes.add(symbol)

        for row in con.execute(sql_cache):
            symbol = normalize_symbol(row["symbol"])
            if is_option_code(symbol):
                codes.add(symbol)

    return sorted(codes)
