# scripts/65_smoke_pipeline_real_execution.py
"""
patch_16 — Smoke: pipeline real ponta a ponta com structure_id do banco.

Cenários (5/5):
  S1  structure_id válido            → status ok, meta presente
  S2  snapshot_source registrado     → meta["snapshot_source"] não vazio
  S3  pricing_payload montado        → canonical_input não é None
  S4  persisted retornado            → persisted não é None
  S5  structure_id inválido          → status error, sem crash
"""

import sys
import os

# Garante imports locais
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.canonical_pricing_facade import CanonicalPricingFacade

# ── Configuração ──────────────────────────────────────────────────────────────
# Ajuste para um structure_id existente em dados/app.db
VALID_STRUCTURE_ID   = 1
INVALID_STRUCTURE_ID = -99

PASS = "✅ PASS"
FAIL = "❌ FAIL"

results: list[tuple[str, str, str]] = []  # (cenario, status, detalhe)


def run(label: str, fn) -> None:
    try:
        ok, detail = fn()
        results.append((label, PASS if ok else FAIL, detail))
    except Exception as exc:
        results.append((label, FAIL, f"exception: {exc}"))


# ── Instância da fachada ──────────────────────────────────────────────────────
facade = CanonicalPricingFacade()


# ── S1: structure_id válido → status ok ──────────────────────────────────────
def s1():
    resp = facade.execute_pricing(structure_id=VALID_STRUCTURE_ID)
    ok = resp.get("status") == "ok"
    return ok, f"status={resp.get('status')}"

run("S1 status ok para structure_id válido", s1)


# ── S2: snapshot_source registrado no meta ────────────────────────────────────
def s2():
    resp = facade.execute_pricing(structure_id=VALID_STRUCTURE_ID)
    source = resp.get("meta", {}).get("snapshot_source")
    ok = bool(source)
    return ok, f"snapshot_source={source!r}"

run("S2 meta.snapshot_source presente", s2)


# ── S3: canonical_input (pricing_payload) montado ────────────────────────────
def s3():
    resp = facade.execute_pricing(structure_id=VALID_STRUCTURE_ID)
    ok = resp.get("canonical_input") is not None
    keys = list((resp.get("canonical_input") or {}).keys())
    return ok, f"canonical_input keys={keys}"

run("S3 canonical_input não é None", s3)


# ── S4: persisted retornado ───────────────────────────────────────────────────
def s4():
    resp = facade.execute_pricing(structure_id=VALID_STRUCTURE_ID)
    ok = resp.get("persisted") is not None
    return ok, f"persisted={type(resp.get('persisted')).__name__}"

run("S4 persisted retornado", s4)


# ── S5: structure_id inválido → status error, sem crash ──────────────────────
def s5():
    resp = facade.execute_pricing(structure_id=INVALID_STRUCTURE_ID)
    ok = resp.get("status") == "error"
    return ok, f"status={resp.get('status')}, msg={resp.get('error_message', '')[:60]}"

run("S5 structure_id inválido → status error sem crash", s5)


# ── Relatório ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("patch_16 | smoke: pipeline real ponta a ponta")
print("=" * 65)

passed = 0
for label, status, detail in results:
    print(f"{status}  {label}")
    print(f"        {detail}")
    if status == PASS:
        passed += 1

total = len(results)
print("=" * 65)
print(f"Resultado: {passed}/{total} OK")
print("=" * 65)

sys.exit(0 if passed == total else 1)
