# scripts/list_abas_rtd.py
from __future__ import annotations

import sys
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def main() -> None:
    _ensure_repo_on_syspath()
    from db.config import connect_app  # noqa: E402

    con = connect_app()
    cur = con.cursor()

    cur.execute("SELECT aba, COUNT(*) n FROM rtd_analise_robo_legs GROUP BY aba ORDER BY aba")
    rows = cur.fetchall()

    print("Abas em rtd_analise_robo_legs:")
    for aba, n in rows:
        print(f"- {aba}: {n} legs")

    con.close()


if __name__ == "__main__":
    main()
