"""
patch_66_import_legacy_structures.py
=====================================
Fase 7 — Migracao definitiva das legs legadas para o modelo canonico.

Para cada aba presente nas tabelas legadas (rtd_analise_robo_legs e
manual_analise_robo_legs), localiza a structure canonica correspondente
via alias_legacy_aba e, se ainda nao houver legs em structure_legs,
importa o snapshot mais recente (MANUAL tem prioridade sobre RTD quando
o timestamp manual for mais recente).

Conversoes aplicadas:
  - vencimento (serial Excel float) -> DATE ISO (YYYY-MM-DD)
  - cv 'C' -> position_side 'LONG'
  - cv 'V' -> position_side 'SHORT'
  - call_put passado como option_type (CALL/PUT)
  - quant  -> quantity (INTEGER)
  - valor_executado -> premium (REAL)
  - strike -> strike (REAL)

Idempotente: se structure_legs ja tiver registros para o structure_id,
             a aba e pulada sem erro.

Autor: patch_66 | 2026-06-04
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------
DB_PATH = Path("dados/app.db")
DRY_RUN = "--dry-run" in sys.argv  # execute com --dry-run para simular


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def excel_serial_to_iso(serial_raw: str) -> str:
    """
    Converte serial Excel (ex: '46157,125' ou '46157.125') para 'YYYY-MM-DD'.
    O serial Excel conta dias a partir de 1899-12-30.
    """
    try:
        # aceita virgula ou ponto como separador decimal
        val = float(str(serial_raw).replace(",", "."))
        base = datetime(1899, 12, 30)
        dt = base + timedelta(days=int(val))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        # se ja for ISO ou formato desconhecido, retorna como esta
        return str(serial_raw)


def map_position_side(cv: str) -> str:
    mapping = {"C": "LONG", "V": "SHORT"}
    result = mapping.get(str(cv).strip().upper())
    if result is None:
        raise ValueError(f"cv desconhecido: '{cv}' (esperado 'C' ou 'V')")
    return result


def safe_float(val) -> float | None:
    if val is None or str(val).strip() == "":
        return None
    try:
        return float(str(val).replace(",", "."))
    except ValueError:
        return None


def safe_int(val) -> int | None:
    f = safe_float(val)
    return int(f) if f is not None else None


# ---------------------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------------------

def get_structures_by_alias(conn: sqlite3.Connection) -> dict[str, dict]:
    """Retorna dict {alias_legacy_aba: {id, name, status}}"""
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, alias_legacy_aba, status
        FROM structures
        WHERE alias_legacy_aba IS NOT NULL
        ORDER BY alias_legacy_aba
    """)
    return {
        row[2]: {"id": row[0], "name": row[1], "status": row[3]}
        for row in cur.fetchall()
    }


def has_legs(conn: sqlite3.Connection, structure_id: int) -> bool:
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM structure_legs WHERE structure_id = ?",
        (structure_id,)
    )
    return cur.fetchone()[0] > 0


def get_latest_snapshot(conn: sqlite3.Connection, aba: str) -> tuple[list[dict], str]:
    """
    Retorna (legs, source_label) do snapshot mais recente para a aba.
    Prioridade: MANUAL se timestamp manual >= RTD, senao RTD.
    """
    cur = conn.cursor()

    # Busca max timestamp manual
    cur.execute("""
        SELECT MAX(timestamp) FROM manual_analise_robo_legs WHERE aba = ?
    """, (aba,))
    ts_manual_raw = cur.fetchone()[0]

    # Busca max timestamp RTD
    cur.execute("""
        SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?
    """, (aba,))
    ts_rtd_raw = cur.fetchone()[0]

    def parse_ts(ts_str: str | None) -> datetime | None:
        if not ts_str:
            return None
        for fmt in ("%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        return None

    ts_manual = parse_ts(ts_manual_raw)
    ts_rtd = parse_ts(ts_rtd_raw)

    # Decide fonte
    use_manual = (
        ts_manual is not None
        and (ts_rtd is None or ts_manual >= ts_rtd)
    )

    if use_manual:
        source_table = "manual_analise_robo_legs"
        ts_used = ts_manual_raw
        source_label = f"manual_analise_robo_legs (ts={ts_manual_raw})"
    elif ts_rtd is not None:
        source_table = "rtd_analise_robo_legs"
        ts_used = ts_rtd_raw
        source_label = f"rtd_analise_robo_legs (ts={ts_rtd_raw})"
    else:
        return [], "sem_dados"

    cur.execute(f"""
        SELECT ativo, cv, call_put, quant, valor_executado,
               strike, vencimento, delta, gamma, theta, vega, iv
        FROM {source_table}
        WHERE aba = ? AND timestamp = ?
        ORDER BY rowid
    """, (aba, ts_used))

    cols = [
        "ativo", "cv", "call_put", "quant", "valor_executado",
        "strike", "vencimento", "delta", "gamma", "theta", "vega", "iv"
    ]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    return rows, source_label


# ---------------------------------------------------------------------------
# Import principal
# ---------------------------------------------------------------------------

def import_legs_for_structure(
    conn: sqlite3.Connection,
    structure_id: int,
    aba: str,
    legs_raw: list[dict],
    source_label: str,
    now_iso: str,
) -> int:
    """
    Insere legs no modelo canonico. Retorna quantidade inserida.
    """
    cur = conn.cursor()
    inserted = 0

    for order, leg in enumerate(legs_raw, start=1):
        position_side = map_position_side(leg["cv"])
        option_type = str(leg["call_put"]).strip().upper()
        symbol = str(leg["ativo"]).strip() if leg["ativo"] else None
        strike = safe_float(leg["strike"])
        expiration_date = excel_serial_to_iso(leg["vencimento"])
        quantity = safe_int(leg["quant"])
        premium = safe_float(leg["valor_executado"])

        if strike is None:
            raise ValueError(f"strike nulo na leg {order} da aba '{aba}'")
        if quantity is None:
            raise ValueError(f"quantity nulo na leg {order} da aba '{aba}'")
        if option_type not in ("CALL", "PUT"):
            raise ValueError(f"option_type invalido '{option_type}' na leg {order} da aba '{aba}'")

        notes = f"migrado de {source_label}"

        if not DRY_RUN:
            cur.execute("""
                INSERT INTO structure_legs (
                    structure_id, position_side, option_type, symbol,
                    strike, expiration_date, quantity, premium,
                    multiplier, leg_order, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1.0, ?, ?, ?, ?)
            """, (
                structure_id, position_side, option_type, symbol,
                strike, expiration_date, quantity, premium,
                order, notes, now_iso, now_iso,
            ))

        print(
            f"    leg {order:02d} | {position_side:5s} {option_type:4s} "
            f"| {symbol:12s} | strike={strike:>10.2f} "
            f"| exp={expiration_date} | qty={quantity:>6d} | prem={premium}"
        )
        inserted += 1

    return inserted


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def run():
    if not DB_PATH.exists():
        print(f"[ERRO] Banco nao encontrado: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    print("=" * 70)
    print(f"patch_66 -- import legacy structures -> canonico")
    print(f"DRY_RUN  = {DRY_RUN}")
    print(f"DB       = {DB_PATH}")
    print(f"NOW      = {now_iso}")
    print("=" * 70)

    structures = get_structures_by_alias(conn)
    print(f"\nStructures com alias_legacy_aba: {len(structures)}")
    for alias, s in structures.items():
        print(f"  id={s['id']:3d}  alias={alias:20s}  status={s['status']}  name={s['name']}")

    # Todas as abas presentes nas tabelas legadas
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT aba FROM rtd_analise_robo_legs
        UNION
        SELECT DISTINCT aba FROM manual_analise_robo_legs
        ORDER BY aba
    """)
    abas_legadas = [r[0] for r in cur.fetchall()]

    print(f"\nAbas legadas encontradas: {abas_legadas}")
    print()

    total_inserted = 0
    total_skipped = 0
    total_errors = 0
    report = []

    for aba in abas_legadas:
        print(f"\n{'─'*60}")
        print(f"ABA: {aba}")

        # Verifica se existe structure canonica
        if aba not in structures:
            msg = f"  [SKIP] Nao ha structure com alias_legacy_aba='{aba}'. Pule ou crie manualmente."
            print(msg)
            report.append({"aba": aba, "status": "SEM_STRUCTURE", "detail": msg})
            total_skipped += 1
            continue

        s = structures[aba]
        structure_id = s["id"]
        print(f"  structure_id={structure_id}  name={s['name']}")

        # Idempotencia
        if has_legs(conn, structure_id):
            msg = f"  [SKIP] structure_id={structure_id} ja possui legs. Idempotencia ativa."
            print(msg)
            report.append({"aba": aba, "status": "JA_MIGRADO", "detail": msg})
            total_skipped += 1
            continue

        # Busca snapshot
        legs_raw, source_label = get_latest_snapshot(conn, aba)
        if not legs_raw:
            msg = f"  [ERRO] Nenhum snapshot encontrado para aba='{aba}'"
            print(msg)
            report.append({"aba": aba, "status": "SEM_SNAPSHOT", "detail": msg})
            total_errors += 1
            continue

        print(f"  fonte: {source_label}")
        print(f"  legs no snapshot: {len(legs_raw)}")

        try:
            n = import_legs_for_structure(
                conn, structure_id, aba, legs_raw, source_label, now_iso
            )
            if not DRY_RUN:
                conn.commit()
            total_inserted += n
            status = "DRY_RUN_OK" if DRY_RUN else "IMPORTADO"
            report.append({
                "aba": aba,
                "status": status,
                "detail": f"{n} legs importadas de {source_label}",
            })
            print(f"  [{status}] {n} legs processadas")
        except Exception as exc:
            conn.rollback()
            msg = f"  [ERRO] {exc}"
            print(msg)
            report.append({"aba": aba, "status": "ERRO", "detail": str(exc)})
            total_errors += 1

    # Relatorio final
    print(f"\n{'='*70}")
    print("RELATORIO FINAL")
    print(f"{'='*70}")
    print(f"  Total abas processadas : {len(abas_legadas)}")
    print(f"  Legs inseridas         : {total_inserted}")
    print(f"  Abas puladas (skip)    : {total_skipped}")
    print(f"  Erros                  : {total_errors}")
    print()
    for r in report:
        icon = {"IMPORTADO": "OK", "DRY_RUN_OK": "~~", "JA_MIGRADO": "--",
                "SEM_STRUCTURE": "?!", "SEM_SNAPSHOT": "!!", "ERRO": "!!"}.get(r["status"], "??")
        print(f"  [{icon}] {r['aba']:20s}  {r['status']:15s}  {r['detail']}")

    if total_errors > 0:
        print(f"\n[ATENCAO] {total_errors} erro(s) encontrado(s). Verifique acima.")
        sys.exit(1)

    if DRY_RUN:
        print("\n[DRY_RUN] Nenhuma alteracao foi gravada no banco.")
    else:
        print("\n[OK] Migracao concluida com sucesso.")

    conn.close()


if __name__ == "__main__":
    run()
