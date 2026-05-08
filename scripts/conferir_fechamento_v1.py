import os
import sys
import sqlite3
from pathlib import Path

FAIL = 0


def ok(msg):  # noqa
    print(f"[OK]  {msg}")


def warn(msg):  # noqa
    print(f"[WARN] {msg}")


def bad(msg):  # noqa
    global FAIL
    print(f"[FAIL] {msg}")
    FAIL = 1


def exists_file(p: Path, label: str):
    if p.is_file():
        ok(f"{label}: {p}")
        return True
    bad(f"{label} ausente: {p}")
    return False


def get_objects(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT name, type, sql FROM sqlite_master "
        "WHERE type IN ('table','view') ORDER BY type, name"
    )
    return cur.fetchall()


def has_object(conn, name: str, obj_type=None):
    cur = conn.cursor()
    if obj_type:
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE name=? AND type=? LIMIT 1",
            (name, obj_type),
        )
    else:
        cur.execute("SELECT 1 FROM sqlite_master WHERE name=? LIMIT 1", (name,))
    return cur.fetchone() is not None


def table_columns(conn, table: str):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    # PRAGMA columns: cid, name, type, notnull, dflt_value, pk
    return [r[1] for r in cur.fetchall()]


def require_columns(conn, table: str, cols: list[str], strict=True):
    if not has_object(conn, table, "table"):
        bad(f"Tabela não encontrada: {table}")
        return
    existing = set(table_columns(conn, table))
    missing = [c for c in cols if c not in existing]
    if missing:
        (bad if strict else warn)(f"Colunas ausentes em {table}: {missing}")
    else:
        ok(f"Colunas OK em {table}: {cols}")


def main():
    project_root = Path(".").resolve()

    print("== Conferência de fechamento (executed_v1) via Python ==")

    # 1) Arquivos-chave
    required_files = [
        "db/config.py",
        "db/derived_repo.py",
        "services/derived_service.py",
        "domain/payoff.py",
        "domain/payoff_features.py",
        "bridge_ingest_csv.py",
        "UI/main_window.py",
        "docs/executed_v1.md",
    ]
    for f in required_files:
        exists_file(project_root / f, f"Arquivo existe")

    # 2) Excel local (RDP)
    excel_xlsm = project_root / "OPERACOES_E_OPCOES.xlsm"
    if excel_xlsm.is_file():
        ok("Excel (xlsm) presente localmente (conexão RDP)")
    else:
        warn("Excel (xlsm) NÃO encontrado. Se sua operação depende do RDP, recoloque-o na raiz.")

    # 3) DB paths (fonte da verdade: data/)
    raw_db = project_root / "data" / "app.db"
    derived_db = project_root / "data" / "derived.db"
    exists_file(raw_db, "Raw DB")
    exists_file(derived_db, "Derived DB")

    # 4) Confusão comum: derived.db na raiz
    root_derived = project_root / "derived.db"
    if root_derived.exists():
        warn(f"Encontrado derived.db na raiz: {root_derived} (legado/armadilha de path).")
    else:
        ok("Não existe derived.db na raiz (bom)")

    # 5) Checagens de schema no derived
    if derived_db.is_file():
        conn = sqlite3.connect(str(derived_db))
        try:
            objs = get_objects(conn)
            ok(f"Objetos no derived.db: {len(objs)}")
            # Debug curto (nomes)
            print("[INFO] " + ", ".join([f"{n}:{t}" for (n, t, _sql) in objs][:20]))

            # Contrato canônico esperado (baseline/executed_v1b)
            # Payoff canônico
            if has_object(conn, "payoff_curve_points", "table"):
                ok("Tabela canônica payoff_curve_points existe")
                require_columns(
                    conn,
                    "payoff_curve_points",
                    ["timestamp", "aba", "point_spot", "point_pl"],
                    strict=True,
                )
            else:
                bad("Tabela payoff_curve_points NÃO existe (contrato canônico não atendido)")

            # View compat (opcional)
            if has_object(conn, "rtd_payoff_points", "view"):
                ok("VIEW compat rtd_payoff_points existe")
            else:
                warn("VIEW compat rtd_payoff_points não encontrada (ok se a UI lê direto payoff_curve_points)")

            # Decisions schema
            if has_object(conn, "structure_decisions", "table"):
                ok("Tabela structure_decisions existe")
                # Campos base + ricos (ricos podem ser NULL, mas devem existir no schema final v1b)
                require_columns(
                    conn,
                    "structure_decisions",
                    ["timestamp", "aba", "decision", "spot_ref", "meta_json", "created_at"],
                    strict=True,
                )
                require_columns(
                    conn,
                    "structure_decisions",
                    ["level", "pl_atual", "pl_max", "pl_pct_of_max", "dte_min", "why_json"],
                    strict=False,  # deixa como WARN se ainda estiver em MVP
                )
            else:
                bad("Tabela structure_decisions NÃO existe")

            # 6) Integridade mínima: toda decisão tem pontos payoff
            if has_object(conn, "structure_decisions", "table") and has_object(conn, "payoff_curve_points", "table"):
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT d.aba, d.timestamp
                    FROM structure_decisions d
                    LEFT JOIN (
                        SELECT aba, timestamp, COUNT(*) AS n
                        FROM payoff_curve_points
                        GROUP BY aba, timestamp
                    ) p
                    ON p.aba = d.aba AND p.timestamp = d.timestamp
                    WHERE p.n IS NULL OR p.n = 0
                    ORDER BY d.aba, d.timestamp
                    LIMIT 20
                    """
                )
                missing = cur.fetchall()
                if missing:
                    bad(f"Decisões sem payoff correspondente (amostra): {missing}")
                else:
                    ok("Toda decisão tem payoff correspondente (aba,timestamp)")

        finally:
            conn.close()

    print("== RESULTADO ==")
    if FAIL:
        print("FAIL")
        sys.exit(1)
    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
