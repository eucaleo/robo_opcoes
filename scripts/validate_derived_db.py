#!/usr/bin/env python3
"""
Script para validar consistencia do banco derived.db
- Nao depende de get_derived_connection (que pode nao existir no seu layout)
- Faz auto-discovery do caminho do derived.db
"""
from __future__ import annotations

import os
import sys
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.derived_repo import validate_snapshot_consistency


def _find_derived_db() -> Path | None:
    # 1) env (prioridade)
    env = os.environ.get("DERIVED_DB_PATH") or os.environ.get("DERIVED_DB") or os.environ.get("DERIVED_DB_FILE")
    if env:
        p = Path(env)
        if p.exists():
            return p

    # 2) caminhos padrao comuns no repo
    candidates = [
        PROJECT_ROOT / "dados" / "app.db",
        PROJECT_ROOT / "data" / "derived.db",
        PROJECT_ROOT / "derived.db",
        PROJECT_ROOT / "db" / "derived.db",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def main() -> int:
    print("=== VALIDACAO DO BANCO DERIVED.DB ===")

    db_path = _find_derived_db()
    if not db_path:
        print("[ERROR] derived.db nao encontrado.")
        print("        Defina DERIVED_DB_PATH (ou DERIVED_DB) apontando para o arquivo.")
        return 2

    print(f"[INFO] Usando derived.db em: {db_path}")

    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()

        # Estatisticas basicas (se tabelas existirem)
        def safe_count(table: str) -> int | None:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                return int(cur.fetchone()[0])
            except Exception:
                return None

        points_count = safe_count("payoff_curve_points")
        decisions_count = safe_count("structure_decisions")

        if points_count is not None:
            print(f"[INFO] Pontos: {points_count}")
        else:
            print("[WARN] Tabela payoff_curve_points nao acessivel (ou nao existe).")

        if decisions_count is not None:
            print(f"[INFO] Decisoes: {decisions_count}")
        else:
            print("[WARN] Tabela structure_decisions nao acessivel (ou nao existe).")

        print("[INFO] Validando consistencia (pontos <-> decisoes)...")
        ok = validate_snapshot_consistency(conn)

        if ok:
            print("[OK] BANCO ESTA CONSISTENTE")
            return 0
        else:
            print("[ERROR] BANCO POSSUI INCONSISTENCIAS")
            return 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
