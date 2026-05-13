# scripts/db_probe_manual_vs_rtd.py
from __future__ import annotations

import sys
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    # scripts/ -> repo root
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def main() -> None:
    _ensure_repo_on_syspath()

    from db.config import connect_app  # noqa: E402

    con = connect_app()
    cur = con.cursor()

    def table_exists(name: str) -> bool:
        # SQLite-friendly existence test
        try:
            cur.execute(f"SELECT 1 FROM {name} LIMIT 1")
            cur.fetchone()
            return True
        except Exception:
            return False

    tables = [
        "manual_analise_robo_legs",
        "rtd_analise_robo_legs",
        "robo_legs_snapshot",
        "robo_snapshot",
    ]

    print("== Table existence ==")
    for t in tables:
        print(f"{t}: {'OK' if table_exists(t) else 'MISSING'}")

    print("\n== Quick stats (if table exists) ==")
    for t in tables:
        if not table_exists(t):
            continue
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            n = cur.fetchone()[0]
            print(f"{t}: rows={n}")
        except Exception as e:
            print(f"{t}: rows=? ({e})")

    print("\n== Manual vs RTD by aba (top 20) ==")
    if table_exists("manual_analise_robo_legs"):
        try:
            cur.execute(
                """
                SELECT aba, COUNT(*) AS n
                FROM manual_analise_robo_legs
                GROUP BY aba
                ORDER BY n DESC
                LIMIT 20
                """
            )
            for aba, n in cur.fetchall():
                print(f"manual: aba={aba} rows={n}")
        except Exception as e:
            print(f"manual group by aba failed: {e}")

    if table_exists("rtd_analise_robo_legs"):
        try:
            cur.execute(
                """
                SELECT aba, COUNT(*) AS n
                FROM rtd_analise_robo_legs
                GROUP BY aba
                ORDER BY n DESC
                LIMIT 20
                """
            )
            for aba, n in cur.fetchall():
                print(f"rtd: aba={aba} rows={n}")
        except Exception as e:
            print(f"rtd group by aba failed: {e}")

    print("\n== MAX(timestamp) (best effort) ==")
    for t in ("manual_analise_robo_legs", "rtd_analise_robo_legs"):
        if not table_exists(t):
            continue
        try:
            cur.execute(f"SELECT MAX(timestamp) FROM {t}")
            mx = cur.fetchone()[0]
            print(f"{t}: max_timestamp={mx}")
        except Exception as e:
            print(f"{t}: max_timestamp=? ({e})")

    try:
        con.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()
