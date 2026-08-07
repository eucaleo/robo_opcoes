from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

from services import canonical_pricing_facade as _facade


_IMPORTED_GLOBAL_NAMES = ['_quote_ident', '_to_float']

for _name in _IMPORTED_GLOBAL_NAMES:
    if hasattr(_facade, _name):
        globals()[_name] = getattr(_facade, _name)


# Funcoes SQL extraidas da camada service pela Frente 58.
# Este modulo fica em repositories para concentrar o boundary SQLite persistido.


def _get_structure_info(structure_id: int, db_path: Path) -> tuple[str, str]:
    """
    Retorna (alias_legacy_aba, underlying_asset) para a estrutura.

    Raises ValueError se:
      - estrutura não existir
      - alias_legacy_aba for nulo (sem aba legada mapeada)
    """
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT alias_legacy_aba, underlying_asset FROM structures WHERE id = ?",
            (structure_id,),
        ).fetchone()

    if row is None:
        raise ValueError(f"structure not found: {structure_id}")

    aba = row["alias_legacy_aba"]
    if not aba:
        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")

    underlying_asset = row["underlying_asset"]  # NOT NULL -- sempre presente

    return aba, underlying_asset

def _lookup_spot_price(db_path: Path, underlying_asset: str) -> float:
    """
    Procura spot positivo no app.db.

    Caso confirmado:
      estrutura SMAL11 possui spot positivo disponível na base canônica/staging.
      spot observado = 124.66
    """
    if not underlying_asset:
        return 0.0

    symbol_candidates = {
        "aba",
        "ativo",
        "asset",
        "symbol",
        "ticker",
        "underlying_asset",
        "codigo",
        "papel",
    }

    price_candidates = {
        "spot",
        "spot_price",
        "underlying_price",
        "last_price",
        "price",
        "preco",
        "preco_atual",
        "valor",
        "cotacao",
        "ultimo",
        "fechamento",
        "close",
    }

    try:
        with sqlite3.connect(str(db_path)) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()

            for (table_name,) in tables:
                columns_info = conn.execute(
                    f"PRAGMA table_info({_quote_ident(table_name)})"
                ).fetchall()

                columns = [row[1] for row in columns_info]
                lower_to_real = {col.lower(): col for col in columns}

                symbol_cols = [
                    lower_to_real[name]
                    for name in symbol_candidates
                    if name in lower_to_real
                ]

                price_cols = [
                    lower_to_real[name]
                    for name in price_candidates
                    if name in lower_to_real
                ]

                if not symbol_cols or not price_cols:
                    continue

                for symbol_col in symbol_cols:
                    for price_col in price_cols:
                        query = (
                            f"SELECT {_quote_ident(price_col)} "
                            f"FROM {_quote_ident(table_name)} "
                            f"WHERE UPPER(CAST({_quote_ident(symbol_col)} AS TEXT)) = UPPER(?) "
                            f"AND {_quote_ident(price_col)} IS NOT NULL "
                            f"LIMIT 20"
                        )

                        try:
                            rows = conn.execute(query, (underlying_asset,)).fetchall()
                        except Exception:
                            continue

                        for row in rows:
                            price = _to_float(row[0], 0.0)
                            if price > 0:
                                return price
    except Exception:
        return 0.0

    return 0.0

