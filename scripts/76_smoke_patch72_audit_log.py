# scripts/76_smoke_patch72_audit_log.py
"""
Smoke test do patch_72 -- structure_audit_log.
Valida: CREATE / UPDATE / ARCHIVE / ADD_LEG / REPLACE_LEGS geram entradas corretas.
Execucao: python scripts/76_smoke_patch72_audit_log.py
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from repositories.structures_repository import StructuresRepository

PASS = "[OK]"
FAIL = "[FALHOU]"


def _tmp_db() -> str:
    f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    path = f.name
    f.close()

    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("""
        CREATE TABLE structures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            underlying_asset TEXT NOT NULL,
            alias_legacy_aba TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE structure_legs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            structure_id INTEGER NOT NULL,
            position_side TEXT NOT NULL,
            option_type TEXT NOT NULL,
            symbol TEXT,
            strike REAL NOT NULL,
            expiration_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            premium REAL,
            multiplier REAL NOT NULL DEFAULT 1,
            leg_order INTEGER NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE
        )
    """)
    conn.execute("""
        CREATE TABLE structure_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            structure_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            changed_by TEXT,
            changed_at TEXT NOT NULL,
            before_json TEXT,
            after_json TEXT,
            notes TEXT,
            FOREIGN KEY (structure_id) REFERENCES structures(id)
        )
    """)
    conn.commit()
    conn.close()
    return path


def _check(label: str, condition: bool) -> bool:
    status = PASS if condition else FAIL
    print(f"  {status}  {label}")
    return condition


def run_smoke() -> bool:
    tmp = _tmp_db()
    repo = StructuresRepository(db_path=tmp)
    ok = True

    print("\n-- patch_72 smoke: structure_audit_log --\n")

    # 1. CREATE
    sid = repo.create_structure({"name": "Condor BOVA11", "underlying_asset": "BOVA11"})
    log = repo.get_audit_log(sid)
    ok &= _check("CREATE gera 1 entrada no log",        len(log) == 1)
    ok &= _check("CREATE action == CREATE",             log[0]["action"] == "CREATE")
    ok &= _check("CREATE before_json e None",           log[0]["before_json"] is None)
    after = json.loads(log[0]["after_json"])
    ok &= _check("CREATE after_json contem name",       after.get("name") == "Condor BOVA11")

    # 2. UPDATE
    repo.update_structure(sid, {"name": "Condor BOVA11 v2"})
    log = repo.get_audit_log(sid)
    update_entry = next((e for e in log if e["action"] == "UPDATE"), None)
    ok &= _check("UPDATE gera entrada no log",          update_entry is not None)
    if update_entry:
        before = json.loads(update_entry["before_json"])
        after  = json.loads(update_entry["after_json"])
        ok &= _check("UPDATE before contem nome antigo", before.get("name") == "Condor BOVA11")
        ok &= _check("UPDATE after contem nome novo",    after.get("name") == "Condor BOVA11 v2")

    # 3. ADD_LEG
    repo.add_leg(sid, {
        "position_side": "LONG", "option_type": "CALL",
        "strike": 120.0, "expiration_date": "2027-03-20",
        "quantity": 500, "multiplier": 1.0, "leg_order": 1,
    })
    log = repo.get_audit_log(sid)
    add_entry = next((e for e in log if e["action"] == "ADD_LEG"), None)
    ok &= _check("ADD_LEG gera entrada no log",         add_entry is not None)

    # 4. REPLACE_LEGS
    repo.replace_legs(sid, [
        {"position_side": "LONG",  "option_type": "CALL",
         "strike": 130.0, "expiration_date": "2027-03-20",
         "quantity": 1000, "multiplier": 1.0, "leg_order": 1},
        {"position_side": "SHORT", "option_type": "PUT",
         "strike": 110.0, "expiration_date": "2027-03-20",
         "quantity": 1000, "multiplier": 1.0, "leg_order": 2},
    ])
    log = repo.get_audit_log(sid)
    replace_entry = next((e for e in log if e["action"] == "REPLACE_LEGS"), None)
    ok &= _check("REPLACE_LEGS gera entrada no log",    replace_entry is not None)
    if replace_entry:
        after = json.loads(replace_entry["after_json"])
        ok &= _check("REPLACE_LEGS after legs_count == 2", after.get("legs_count") == 2)

    # 5. ARCHIVE
    repo.archive_structure(sid)
    log = repo.get_audit_log(sid)
    archive_entry = next((e for e in log if e["action"] == "ARCHIVE"), None)
    ok &= _check("ARCHIVE gera entrada no log",         archive_entry is not None)
    if archive_entry:
        before = json.loads(archive_entry["before_json"])
        after  = json.loads(archive_entry["after_json"])
        ok &= _check("ARCHIVE before status active",    before.get("status") == "active")
        ok &= _check("ARCHIVE after status archived",   after.get("status") == "archived")

    # 6. get_full_audit_log
    s2 = repo.create_structure({"name": "S2", "underlying_asset": "VALE3"})
    full = repo.get_full_audit_log()
    ok &= _check("get_full_audit_log retorna > 1 estrutura", len({e["structure_id"] for e in full}) >= 2)
    creates = repo.get_full_audit_log(action="CREATE")
    ok &= _check("get_full_audit_log filtro action funciona", all(e["action"] == "CREATE" for e in creates))
    limited = repo.get_full_audit_log(limit=3)
    ok &= _check("get_full_audit_log limit respeitado",  len(limited) <= 3)

    # cleanup
    os.unlink(tmp)

    print()
    result = "PASSOU" if ok else "FALHOU"
    print(f"-- resultado: {result} --\n")
    return ok


if __name__ == "__main__":
    success = run_smoke()
    sys.exit(0 if success else 1)
