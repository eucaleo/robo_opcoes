#!/usr/bin/env python3
# =============================================================================
# patch_28_migrate_structures.py  (v2 — bugs #1 #2 #3 corrigidos)
# =============================================================================

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

APP_DB     = Path("./dados/app.db")
DERIVED_DB = Path("./dados/derived.db")
BACKUP_DIR = Path("./dados/backups")

ABA_CATALOG: dict[str, dict] = {
    "BOVA11": {
        "name":             "BOVA11 Condor Maio/2026",
        "underlying_asset": "BOVA11",
        "notes":            "Canônico — migrado do legado",
    },
    "EMBJ3": {
        "name":             "EMBJ3 Estrutura Maio/2026",
        "underlying_asset": "EMBJ3",
        "notes":            "Criado na migração patch_28",
    },
    "PRIO3": {
        "name":             "PRIO3 Estrutura Maio/2026",
        "underlying_asset": "PRIO3",
        "notes":            "Criado na migração patch_28",
    },
    "SBSP3": {
        "name":             "SBSP3 Estrutura Maio/2026",
        "underlying_asset": "SBSP3",
        "notes":            "Criado na migração patch_28",
    },
    "SMAL11": {
        "name":             "SMAL11 Estrutura Maio/2026",
        "underlying_asset": "SMAL11",
        "notes":            "Criado na migração patch_28",
    },
}

NOW = datetime.now(timezone.utc).isoformat()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def log(msg: str, level: str = "INFO") -> None:
    icons = {"INFO": "ℹ️ ", "OK": "✅", "WARN": "⚠️ ", "ERR": "❌", "DRY": "🔵"}
    print(f"  {icons.get(level, '  ')} [{level}] {msg}")


def backup_db(src: Path) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = BACKUP_DIR / f"{src.stem}_{ts}.db"
    shutil.copy2(src, dst)
    log(f"Backup criado: {dst}", "OK")
    return dst


def connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def parse_float(val) -> float | None:
    if val is None:
        return None
    try:
        return float(str(val).replace(",", ".").strip())
    except (ValueError, TypeError):
        return None


def parse_date(val) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    try:
        from datetime import timedelta
        base = datetime(1899, 12, 30)
        return (base + timedelta(days=float(s))).strftime("%Y-%m-%d")
    except Exception:
        pass
    return s


def _map_call_put(cv, call_put) -> tuple[str, str]:
    side = "LONG"  if str(cv or "C").upper().startswith("C") else "SHORT"
    kind = "CALL"  if str(call_put or "CALL").upper().startswith("C") else "PUT"
    return side, kind


# ─────────────────────────────────────────────────────────────────────────────
# ESTADO SIMULADO (usado pelo dry-run para Op 3 e Op 4)
# ─────────────────────────────────────────────────────────────────────────────

class SimState:
    """
    Mantém em memória o estado que o banco TERIA após as operações,
    sem nunca gravar nada. Permite que Op 3 e Op 4 em dry-run sejam
    completamente fiéis ao que aconteceria de verdade.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        # Carrega estado atual do banco
        rows = conn.execute(
            "SELECT id, name, underlying_asset, alias_legacy_aba, status "
            "FROM structures ORDER BY id"
        ).fetchall()
        self.structures: dict[int, dict] = {
            r["id"]: dict(r) for r in rows
        }
        # Legs existentes
        legs = conn.execute(
            "SELECT id, structure_id FROM structure_legs"
        ).fetchall()
        self.legs: dict[int, list[int]] = {}  # structure_id → [leg_ids]
        for l in legs:
            self.legs.setdefault(l["structure_id"], []).append(l["id"])

        self._next_id = max(self.structures.keys(), default=0) + 1
        self._next_structure_id = self._next_id

        # Legs simuladas (structure_id → list of dicts)
        self.sim_legs: dict[int, list[dict]] = {}

    def delete_structures(self, ids: list[int]) -> None:
        for sid in ids:
            self.structures.pop(sid, None)
            self.legs.pop(sid, None)

    def set_active(self, sid: int) -> None:
        if sid in self.structures:
            self.structures[sid]["status"] = "active"

    def create_structure(self, aba: str, meta: dict) -> int:
        new_id = self._next_structure_id
        self._next_structure_id += 1
        self.structures[new_id] = {
            "id":                 new_id,
            "name":               meta["name"],
            "underlying_asset":   meta["underlying_asset"],
            "alias_legacy_aba":   aba,
            "status":             "active",
        }
        return new_id

    def set_legs(self, structure_id: int, legs: list[dict]) -> None:
        self.sim_legs[structure_id] = legs

    def count_legs(self, structure_id: int) -> int:
        # Prioriza legs simuladas (pós-migração)
        if structure_id in self.sim_legs:
            return len(self.sim_legs[structure_id])
        return len(self.legs.get(structure_id, []))

    def active_structures(self) -> list[dict]:
        return [s for s in self.structures.values() if s["status"] == "active"]

    def all_structures_sorted(self) -> list[dict]:
        return sorted(self.structures.values(), key=lambda s: s["id"])


# ─────────────────────────────────────────────────────────────────────────────
# OP 1
# ─────────────────────────────────────────────────────────────────────────────

def op1_clean_structures(
    conn: sqlite3.Connection,
    dry: bool,
    sim: SimState,
) -> dict[str, int]:
    print("\n── Op 1: Limpeza de duplicatas em structures ──")

    rows = conn.execute(
        "SELECT id, name, underlying_asset, alias_legacy_aba, status "
        "FROM structures ORDER BY alias_legacy_aba, id"
    ).fetchall()

    by_alias: dict[str, list] = {}
    for r in rows:
        alias = r["alias_legacy_aba"] or ""
        by_alias.setdefault(alias, []).append(dict(r))

    canonical_ids: dict[str, int] = {}

    for alias, group in by_alias.items():
        log(f"alias='{alias}' → {len(group)} registros encontrados")

        def sort_key(r):
            # Preferência: active > archived, sem "Atualizada", menor id
            is_active  = 0 if r["status"] == "active" else 1
            has_update = 1 if "Atualizada" in r["name"] or "Atualizada" in r["name"] else 0
            return (is_active, has_update, r["id"])

        group.sort(key=sort_key)
        keeper    = group[0]
        to_delete = group[1:]

        log(f"  → Mantendo  id={keeper['id']}  '{keeper['name']}'  [{keeper['status']}]")
        canonical_ids[alias] = keeper["id"]

        if to_delete:
            ids_del = [r["id"] for r in to_delete]
            log(f"  → Deletando ids={ids_del}  ({len(ids_del)} duplicatas)")

            if dry:
                sim.delete_structures(ids_del)
                log(f"  → [DRY] Simulando deleção de {len(ids_del)} registros", "DRY")
            else:
                conn.execute(
                    f"DELETE FROM structure_legs WHERE structure_id IN "
                    f"({','.join('?' * len(ids_del))})", ids_del
                )
                conn.execute(
                    f"DELETE FROM structures WHERE id IN "
                    f"({','.join('?' * len(ids_del))})", ids_del
                )
                log(f"  → Deletadas {len(ids_del)} duplicatas + suas legs", "OK")

        if keeper["status"] != "active":
            if dry:
                sim.set_active(keeper["id"])
                log(f"  → [DRY] Simulando reativação de id={keeper['id']}", "DRY")
            else:
                conn.execute(
                    "UPDATE structures SET status='active', updated_at=? WHERE id=?",
                    (NOW, keeper["id"])
                )
                log(f"  → Reativado id={keeper['id']}", "OK")

    return canonical_ids


# ─────────────────────────────────────────────────────────────────────────────
# OP 2
# ─────────────────────────────────────────────────────────────────────────────

def op2_create_missing_structures(
    conn: sqlite3.Connection,
    dry: bool,
    sim: SimState,
    canonical_ids: dict[str, int],
) -> dict[str, int]:
    print("\n── Op 2: Criar structures ausentes ──")

    for aba, meta in ABA_CATALOG.items():
        if aba in canonical_ids:
            log(f"'{aba}' já existe → id={canonical_ids[aba]}  (pulado)")
            continue

        log(f"'{aba}' ausente → criando structure canônica")

        if dry:
            # FIX #2: Em dry-run, atribui ID simulado para Op 3 poder usá-lo
            new_id = sim.create_structure(aba, meta)
            canonical_ids[aba] = new_id
            log(f"  → [DRY] Simularia INSERT → id_simulado={new_id}  '{meta['name']}'", "DRY")
        else:
            cur = conn.execute("""
                INSERT INTO structures
                    (name, underlying_asset, alias_legacy_aba, status, notes,
                     created_at, updated_at)
                VALUES (?, ?, ?, 'active', ?, ?, ?)
            """, (
                meta["name"], meta["underlying_asset"], aba,
                meta.get("notes"), NOW, NOW,
            ))
            new_id = cur.lastrowid
            if new_id is None:
                raise RuntimeError(f"INSERT de structure '{aba}' não retornou lastrowid")
            canonical_ids[aba] = new_id
            log(f"  → Criada id={new_id}  '{meta['name']}'", "OK")

    return canonical_ids


# ─────────────────────────────────────────────────────────────────────────────
# OP 3
# ─────────────────────────────────────────────────────────────────────────────

def _migrate_from_table(
    conn: sqlite3.Connection,
    table: str,
    canonical_ids: dict[str, int],
    dry: bool,
    sim: SimState,
    source_label: str,
) -> dict[str, int]:
    print(f"\n── Op 3: Migração de {table} ──")

    rows = conn.execute(
        f"SELECT * FROM {table} ORDER BY aba, timestamp DESC"
    ).fetchall()

    if not rows:
        log(f"Tabela {table} vazia — nada a migrar", "WARN")
        return {}

    # Pega snapshot mais recente por aba
    latest_by_aba: dict[str, list]  = {}
    seen_ts:       dict[str, str]   = {}

    for r in rows:
        aba = r["aba"]
        ts  = str(r["timestamp"] or "")
        if aba not in seen_ts:
            seen_ts[aba]       = ts
            latest_by_aba[aba] = []
        if ts == seen_ts[aba]:
            latest_by_aba[aba].append(dict(r))

    stats: dict[str, int] = {}

    for aba, legs in latest_by_aba.items():
        sid = canonical_ids.get(aba)

        # FIX #2: Em dry-run, canonical_ids já tem IDs simulados da Op 2
        if sid is None:
            log(f"aba='{aba}' sem structure canônica — pulado", "WARN")
            continue

        log(f"aba='{aba}' → structure_id={sid}  ts={seen_ts[aba]}  legs={len(legs)}")

        if dry:
            # FIX #1: Registra legs simuladas no SimState para Op 4 usar
            sim.set_legs(sid, legs)
            log(f"  → [DRY] Inseriria {len(legs)} legs para aba='{aba}'", "DRY")
        else:
            conn.execute(
                "DELETE FROM structure_legs WHERE structure_id = ?", (sid,)
            )
            for order, leg in enumerate(legs, 1):
                side, kind = _map_call_put(leg.get("cv"), leg.get("call_put"))
                conn.execute("""
                    INSERT INTO structure_legs
                        (structure_id, position_side, option_type, symbol,
                         strike, expiration_date, quantity, premium,
                         multiplier, leg_order, notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1.0, ?, ?, ?, ?)
                """, (
                    sid, side, kind,
                    str(leg.get("ativo") or "").strip() or None,
                    parse_float(leg.get("strike")),
                    parse_date(leg.get("vencimento")),
                    parse_float(leg.get("quant")) or 1.0,
                    parse_float(leg.get("valor_executado")),
                    order,
                    f"migrado de {table} ({source_label})",
                    NOW, NOW,
                ))
            log(f"  → {len(legs)} legs inseridas", "OK")

        stats[aba] = len(legs)

    return stats


def op3_migrate_legs(
    conn: sqlite3.Connection,
    dry: bool,
    sim: SimState,
    canonical_ids: dict[str, int],
) -> None:
    stats_rtd = _migrate_from_table(
        conn, "rtd_analise_robo_legs", canonical_ids, dry, sim, "RTD"
    )
    stats_manual = _migrate_from_table(
        conn, "manual_analise_robo_legs", canonical_ids, dry, sim, "MANUAL"
    )

    print()
    log("Resumo de migração de legs:")
    for aba in sorted(set(list(stats_rtd.keys()) + list(stats_manual.keys()))):
        rtd_n    = stats_rtd.get(aba, 0)
        manual_n = stats_manual.get(aba, 0)
        final_n  = manual_n if manual_n > 0 else rtd_n
        origin   = "MANUAL" if manual_n > 0 else "RTD"
        log(f"  aba='{aba}'  legs_finais={final_n}  origem={origin}")


# ─────────────────────────────────────────────────────────────────────────────
# OP 4
# ─────────────────────────────────────────────────────────────────────────────

def op4_verify(
    conn: sqlite3.Connection,
    dry: bool,
    sim: SimState,
) -> None:
    print("\n── Op 4: Verificação final ──")

    if dry:
        # FIX #1 + #3: Usa estado SIMULADO, não o banco real
        all_structs = sim.all_structures_sorted()
        print()
        print("  (estado simulado — o que o banco TERIA após a migração)\n")
    else:
        rows = conn.execute("""
            SELECT s.id, s.name, s.underlying_asset, s.alias_legacy_aba, s.status
            FROM structures s ORDER BY s.id
        """).fetchall()
        all_structs = [dict(r) for r in rows]

    print(f"  {'ID':<6} {'Ativo':<8} {'Alias':<8} {'Status':<10} "
          f"{'Legs':<7} {'Nome'}")
    print(f"  {'─'*6} {'─'*8} {'─'*8} {'─'*10} {'─'*7} {'─'*40}")

    for s in all_structs:
        sid    = s["id"]
        n_legs = sim.count_legs(sid) if dry else conn.execute(
            "SELECT COUNT(*) AS n FROM structure_legs WHERE structure_id=?", (sid,)
        ).fetchone()["n"]

        legs_ok = "✅" if n_legs > 0 else "⚠️ "
        print(
            f"  {sid:<6} {s['underlying_asset']:<8} "
            f"{(s['alias_legacy_aba'] or '—'):<8} {s['status']:<10} "
            f"{legs_ok}{n_legs:<5} {s['name']}"
        )

    # Totais
    active_count = sum(1 for s in all_structs if s["status"] == "active")
    legs_count   = sum(sim.count_legs(s["id"]) for s in all_structs) if dry else \
                   conn.execute("SELECT COUNT(*) AS n FROM structure_legs").fetchone()["n"]

    print()
    if dry:
        log(f"[DRY] structures active esperadas: {active_count}   "
            f"structure_legs esperadas: {legs_count}", "DRY")
    else:
        log(f"structures active: {active_count}   "
            f"structure_legs total: {legs_count}", "OK")

    # FIX #3: Cruzamento derived.db usa aliases simulados
    print()
    print("  Cruzamento com derived.db:")

    derived = connect(DERIVED_DB)
    derived_abas   = {r[0] for r in derived.execute(
        "SELECT DISTINCT aba FROM structure_decisions"
    ).fetchall()}
    derived_payoff = {r[0] for r in derived.execute(
        "SELECT DISTINCT aba FROM payoff_curve_points"
    ).fetchall()}
    derived.close()

    active_aliases = {
        s["alias_legacy_aba"]
        for s in all_structs
        if s["status"] == "active" and s["alias_legacy_aba"]
    }

    all_ok = True
    for aba in sorted(active_aliases):
        in_dec    = "✅" if aba in derived_abas    else "⚠️  ausente"
        in_payoff = "✅" if aba in derived_payoff  else "⚠️  ausente"
        if "ausente" in in_dec or "ausente" in in_payoff:
            all_ok = False
        print(f"    aba='{aba}'  decisions={in_dec}  payoff={in_payoff}")

    if not all_ok:
        print()
        log(
            "Algumas abas não têm dados em derived.db — "
            "isso é esperado para as 4 estruturas novas (EMBJ3/PRIO3/SBSP3/SMAL11). "
            "derived.db será atualizado pelo pipeline de análise.",
            "WARN"
        )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="patch_28 v2 — Migração legado → structures canônico"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force",   action="store_true")
    args = parser.parse_args()
    dry  = args.dry_run

    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  patch_28 v2 — Migração legado → structures canônico        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"  Modo: {'🔵 DRY-RUN (sem gravação)' if dry else '🟢 REAL (gravará no banco)'}")
    print(f"  app.db:     {APP_DB.resolve()}")
    print(f"  derived.db: {DERIVED_DB.resolve()}")

    for path in (APP_DB, DERIVED_DB):
        if not path.exists():
            print(f"\n❌ {path} não encontrado")
            sys.exit(1)

    if not dry and not args.force:
        print()
        print("  ⚠️  Esta operação irá:")
        print("      1. Deletar 34 duplicatas de structures")
        print("      2. Criar 4 novas structures (EMBJ3, PRIO3, SBSP3, SMAL11)")
        print("      3. Substituir todas as structure_legs com dados do legado")
        print()
        resp = input("  Confirma? [s/N] ").strip().lower()
        if resp not in ("s", "sim", "y", "yes"):
            print("  Operação cancelada.")
            sys.exit(0)

    if not dry:
        print()
        backup_db(APP_DB)

    conn = connect(APP_DB)
    sim  = SimState(conn)  # carrega snapshot inicial

    try:
        with conn:
            canonical_ids = op1_clean_structures(conn, dry, sim)
            canonical_ids = op2_create_missing_structures(conn, dry, sim, canonical_ids)
            op3_migrate_legs(conn, dry, sim, canonical_ids)

        op4_verify(conn, dry, sim)

        print()
        if dry:
            print("  🔵 DRY-RUN concluído — execute sem --dry-run para aplicar")
        else:
            print("  ✅ patch_28 aplicado com sucesso")
            print(f"  Backup disponível em: {BACKUP_DIR}/")

    except Exception as exc:
        print(f"\n  ❌ Erro: {exc}")
        print("  Transação revertida — banco intacto.")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        conn.close()
# ---------------------------------------------------------------------------
# Entrypoints esperados pelo audit_patches
# ---------------------------------------------------------------------------

def migrate(dry_run: bool = False, force: bool = False) -> None:
    """
    Entrypoint canônico para o script de auditoria e chamadas programáticas.
    Equivalente a rodar: python patch_28_migrate_structures.py [--dry-run] [--force]
    """
    import sys

    # Injeta args para que main() leia corretamente
    _orig_argv = sys.argv[:]
    sys.argv = [sys.argv[0]]
    if dry_run:
        sys.argv.append("--dry-run")
    if force:
        sys.argv.append("--force")
    try:
        main()
    finally:
        sys.argv = _orig_argv


# Alias esperado por alguns checkers
run = migrate


if __name__ == "__main__":
    main()
