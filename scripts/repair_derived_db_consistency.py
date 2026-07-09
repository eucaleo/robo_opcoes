#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_like_repo(con: sqlite3.Connection) -> tuple[bool, int, int]:
    cur = con.cursor()

    cur.execute("""
        SELECT d.aba, d.timestamp, COUNT(p.point_spot) AS point_count
        FROM structure_decisions d
        LEFT JOIN payoff_curve_points p
               ON d.aba = p.aba
              AND d.timestamp = p.timestamp
        GROUP BY d.aba, d.timestamp
        HAVING point_count = 0
    """)
    orphan_decisions = cur.fetchall()

    cur.execute("""
        SELECT p.aba, p.timestamp, COUNT(DISTINCT p.point_spot)
        FROM payoff_curve_points p
        LEFT JOIN structure_decisions d
               ON p.aba = d.aba
              AND p.timestamp = d.timestamp
        WHERE d.aba IS NULL
        GROUP BY p.aba, p.timestamp
    """)
    orphan_points = cur.fetchall()

    return (
        not orphan_decisions and not orphan_points,
        len(orphan_decisions),
        len(orphan_points),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repara inconsistências de snapshots em dados/derived.db"
    )
    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do derived.db. Default: dados/app.db",
    )
    parser.add_argument(
        "--max-delta-seconds",
        type=float,
        default=0.25,
        help="Delta máximo para alinhar decisão ao snapshot de pontos. Default: 0.25s",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica alterações. Sem isso roda em dry-run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Modo simulação explícito. É o padrão quando --apply não é usado.",
    )
    parser.add_argument(
        "--prune-unmatched-decisions",
        action="store_true",
        help="Remove decisões que continuam sem pontos depois do alinhamento.",
    )
    parser.add_argument(
        "--prune-unmatched-points",
        action="store_true",
        help="Remove pontos que continuam sem decisão depois do alinhamento.",
    )
    args = parser.parse_args()

    if args.apply and args.dry_run:
        parser.error("use --apply ou --dry-run, não ambos")

    db = Path(args.db)

    print("=== REPARO DE CONSISTENCIA DO DERIVED.DB ===")
    print(f"[INFO] DB: {db.resolve()}")
    print(f"[INFO] Existe: {db.exists()}")

    if not db.exists():
        print("[ERROR] Banco não encontrado.")
        return 2

    if args.apply:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = db.with_suffix(db.suffix + f".bak-{stamp}")
        shutil.copy2(db, backup)
        print(f"[INFO] Backup criado: {backup}")
    else:
        print("[DRY-RUN] Nenhuma alteração será aplicada.")

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row

    try:
        ok0, od0, op0 = validate_like_repo(con)
        print()
        print("=== ESTADO INICIAL ===")
        print(f"[INFO] Consistente: {ok0}")
        print(f"[INFO] Decisões sem pontos: {od0}")
        print(f"[INFO] Pontos sem decisão: {op0}")

        points = con.execute("""
            SELECT
                structure_id,
                aba,
                timestamp,
                COUNT(*) AS n
            FROM payoff_curve_points
            GROUP BY structure_id, aba, timestamp
            ORDER BY structure_id, aba, timestamp
        """).fetchall()

        decisions = con.execute("""
            SELECT
                id,
                structure_id,
                aba,
                timestamp
            FROM structure_decisions
            ORDER BY structure_id, aba, timestamp
        """).fetchall()

        updates: list[tuple[str, int, float, str, str, int | None, str]] = []
        used_decision_ids: set[int] = set()

        for p in points:
            candidates = []
            for d in decisions:
                if d["id"] in used_decision_ids:
                    continue
                if d["aba"] != p["aba"]:
                    continue
                if d["structure_id"] != p["structure_id"]:
                    continue

                try:
                    delta = abs(
                        (
                            parse_ts(d["timestamp"]) - parse_ts(p["timestamp"])
                        ).total_seconds()
                    )
                except Exception:
                    continue

                if delta <= args.max_delta_seconds:
                    candidates.append((delta, d))

            if not candidates:
                continue

            delta, nearest = min(candidates, key=lambda item: item[0])
            used_decision_ids.add(nearest["id"])

            if nearest["timestamp"] != p["timestamp"]:
                updates.append(
                    (
                        p["timestamp"],
                        nearest["id"],
                        delta,
                        nearest["timestamp"],
                        p["timestamp"],
                        p["structure_id"],
                        p["aba"],
                    )
                )

        print()
        print("=== ALINHAMENTOS ENCONTRADOS ===")
        if not updates:
            print("[INFO] Nenhum timestamp próximo para alinhar.")
        else:
            for _, decision_id, delta, old_ts, new_ts, sid, aba in updates:
                print(
                    f"[MATCH] decision_id={decision_id} "
                    f"sid={sid} aba={aba} delta={delta:.6f}s"
                )
                print(f"        decisão antiga: {old_ts}")
                print(f"        novo timestamp: {new_ts}")

        if args.apply:
            with con:
                for new_ts, decision_id, *_rest in updates:
                    con.execute(
                        """
                        UPDATE structure_decisions
                           SET timestamp = ?
                         WHERE id = ?
                        """,
                        (new_ts, decision_id),
                    )
            print(f"[APPLY] Decisões alinhadas: {len(updates)}")
        else:
            print(f"[DRY-RUN] Decisões que seriam alinhadas: {len(updates)}")

        ok1, od1, op1 = validate_like_repo(con)
        print()
        print("=== APOS ALINHAMENTO ===")
        print(f"[INFO] Consistente: {ok1}")
        print(f"[INFO] Decisões sem pontos: {od1}")
        print(f"[INFO] Pontos sem decisão: {op1}")

        deleted_decisions = 0
        deleted_points = 0

        if args.prune_unmatched_decisions:
            rows = con.execute("""
                SELECT d.id, d.structure_id, d.aba, d.timestamp
                FROM structure_decisions d
                LEFT JOIN payoff_curve_points p
                       ON d.aba = p.aba
                      AND d.timestamp = p.timestamp
                WHERE p.aba IS NULL
                GROUP BY d.id, d.structure_id, d.aba, d.timestamp
                ORDER BY d.structure_id, d.aba, d.timestamp
            """).fetchall()

            print()
            print("=== DECISOES ORFAS A REMOVER ===")
            if not rows:
                print("[INFO] Nenhuma decisão órfã.")
            else:
                for r in rows:
                    print(dict(r))

            if args.apply and rows:
                ids = [int(r["id"]) for r in rows]
                placeholders = ",".join("?" for _ in ids)
                with con:
                    cur = con.execute(
                        f"DELETE FROM structure_decisions WHERE id IN ({placeholders})",
                        ids,
                    )
                    deleted_decisions = cur.rowcount
                print(f"[APPLY] Decisões órfãs removidas: {deleted_decisions}")
            elif rows:
                print(f"[DRY-RUN] Decisões órfãs que seriam removidas: {len(rows)}")

        if args.prune_unmatched_points:
            rows = con.execute("""
                SELECT p.structure_id, p.aba, p.timestamp, COUNT(*) AS n
                FROM payoff_curve_points p
                LEFT JOIN structure_decisions d
                       ON p.aba = d.aba
                      AND p.timestamp = d.timestamp
                WHERE d.aba IS NULL
                GROUP BY p.structure_id, p.aba, p.timestamp
                ORDER BY p.structure_id, p.aba, p.timestamp
            """).fetchall()

            print()
            print("=== PONTOS ORFAOS A REMOVER ===")
            if not rows:
                print("[INFO] Nenhum grupo de pontos órfão.")
            else:
                for r in rows:
                    print(dict(r))

            if args.apply and rows:
                with con:
                    cur = con.execute("""
                        DELETE FROM payoff_curve_points
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM structure_decisions d
                            WHERE d.aba = payoff_curve_points.aba
                              AND d.timestamp = payoff_curve_points.timestamp
                        )
                    """)
                    deleted_points = cur.rowcount
                print(f"[APPLY] Pontos órfãos removidos: {deleted_points}")
            elif rows:
                print(f"[DRY-RUN] Grupos de pontos órfãos que seriam removidos: {len(rows)}")

        ok2, od2, op2 = validate_like_repo(con)
        print()
        print("=== ESTADO FINAL ===")
        print(f"[INFO] Consistente: {ok2}")
        print(f"[INFO] Decisões sem pontos: {od2}")
        print(f"[INFO] Pontos sem decisão: {op2}")
        print(f"[INFO] Decisões alinhadas: {len(updates)}")
        print(f"[INFO] Decisões removidas: {deleted_decisions}")
        print(f"[INFO] Pontos removidos: {deleted_points}")

        if ok2:
            print("[OK] derived.db consistente.")
            return 0

        print("[WARN] derived.db ainda inconsistente.")
        return 1

    finally:
        con.close()


if __name__ == "__main__":
    raise SystemExit(main())
