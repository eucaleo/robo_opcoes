"""Status do snapshot RTD de opções.

Frente 54a:
- isola a leitura de MAX(updated_at) da tabela rtd_option_quotes;
- evita SQL direto na UI;
- mantém a UI consumindo uma função de serviço pequena e segura.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Optional, Union


def read_rtd_option_quotes_max_updated_at(
    db_path: Union[str, Path],
) -> Optional[str]:
    """Retorna o maior updated_at presente em rtd_option_quotes.

    Em caso de banco indisponível, tabela ausente ou erro SQLite, retorna None.
    """
    try:
        with sqlite3.connect(str(db_path), timeout=1.0) as conn:
            row = conn.execute(
                "SELECT MAX(updated_at) FROM rtd_option_quotes"
            ).fetchone()
    except (sqlite3.Error, OSError):
        return None

    if not row or row[0] is None:
        return None

    return str(row[0])
