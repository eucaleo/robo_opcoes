from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def _now_ts() -> str:
    # mantém padrão semelhante ao RTD exibido no seu DB: "14/04/2026 17:55:51"
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def _table_exists(cur, name: str) -> bool:
    cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",
        (name,),
    )
    return cur.fetchone() is not None


def _table_columns(cur, name: str) -> list[str]:
    cur.execute(f"PRAGMA table_info({name})")
    # PRAGMA table_info -> (cid, name, type, notnull, dflt_value, pk)
    return [row[1] for row in cur.fetchall()]


def main() -> None:
    _ensure_repo_on_syspath()
    from db.config import connect_app  # noqa: E402

    ap = argparse.ArgumentParser(
        description="Seed manual_analise_robo_legs copiando legs do rtd_analise_robo_legs"
    )
    ap.add_argument("--aba", required=True, help="Aba alvo (ex: BOVA11)")
    ap.add_argument(
        "--timestamp",
        default=None,
        help="Timestamp para gravar no manual (default: agora, formato dd/mm/YYYY HH:MM:SS)",
    )
    ap.add_argument(
        "--truncate-aba",
        action="store_true",
        help="Apaga registros existentes no manual para essa aba antes de inserir",
    )
    args = ap.parse_args()

    aba = args.aba
    ts = args.timestamp or _now_ts()

    con = connect_app()
    cur = con.cursor()

    if not _table_exists(cur, "rtd_analise_robo_legs"):
        raise SystemExit("Tabela rtd_analise_robo_legs não existe.")

    if not _table_exists(cur, "manual_analise_robo_legs"):
        raise SystemExit("Tabela manual_analise_robo_legs não existe.")

    manual_cols = _table_columns(cur, "manual_analise_robo_legs")
    rtd_cols = _table_columns(cur, "rtd_analise_robo_legs")

    # Só copiamos colunas que existam em ambos.
    common = [c for c in manual_cols if c in rtd_cols]
    if "aba" not in common:
        raise SystemExit("Coluna 'aba' não encontrada em ambas as tabelas.")

    # Garantir timestamp no insert (se existir no manual)
    has_ts_in_manual = "timestamp" in manual_cols
    has_ts_in_common = "timestamp" in common

    # Vamos montar SELECT do RTD:
    # - usamos as colunas comuns
    # - se timestamp existir no manual mas não for comum, forçamos no INSERT
    select_cols = common[:]  # cópia

    # Buscar legs do RTD pela aba no timestamp mais recente do RTD
    cur.execute("SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba=?", (aba,))
    rtd_max = cur.fetchone()[0]
    if not rtd_max:
        raise SystemExit(f"Nenhum timestamp encontrado no RTD para aba={aba}")

    if args.truncate_aba:
        cur.execute("DELETE FROM manual_analise_robo_legs WHERE aba=?", (aba,))

    # Carrega linhas RTD do snapshot mais recente (mesma lógica do payoff)
    cols_sql = ", ".join(select_cols)
    cur.execute(
        f"SELECT {cols_sql} FROM rtd_analise_robo_legs WHERE aba=? AND timestamp=?",
        (aba, rtd_max),
    )
    rows = cur.fetchall()
    if not rows:
        raise SystemExit(f"Nenhuma leg no RTD para aba={aba} timestamp={rtd_max}")

    # Montar INSERT no manual:
    insert_cols = common[:]
    values_rows = []
    if has_ts_in_manual and not has_ts_in_common:
        # timestamp existe no manual, mas não veio do RTD (improvável); força coluna no insert
        insert_cols = insert_cols + ["timestamp"]
        for r in rows:
            values_rows.append(tuple(r) + (ts,))
    elif has_ts_in_common:
        # timestamp veio do RTD, mas queremos sobrescrever no manual com ts informado
        # para ficar explícito que o manual é "mais novo" (e dominar na seleção).
        ts_idx = insert_cols.index("timestamp")
        for r in rows:
            r = list(r)
            r[ts_idx] = ts
            values_rows.append(tuple(r))
    else:
        # manual não tem timestamp (muito improvável dado seu uso de MAX(timestamp))
        values_rows = rows

    placeholders = ", ".join(["?"] * len(insert_cols))
    insert_cols_sql = ", ".join(insert_cols)

    cur.executemany(
        f"INSERT INTO manual_analise_robo_legs ({insert_cols_sql}) VALUES ({placeholders})",
        values_rows,
    )
    con.commit()
    con.close()

    print("✅ Seed concluído:")
    print(f"- aba={aba}")
    print(f"- rtd_max_timestamp={rtd_max}")
    print(f"- manual_timestamp_written={ts}")
    print(f"- rows_inserted={len(values_rows)}")


if __name__ == "__main__":
    main()
