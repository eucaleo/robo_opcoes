"""
tmp_test_structure_ref.py  —  TEMPORÁRIO (remover após patch_53)

Valida comportamento do StructureRef antes de aplicar nos callers.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.domain.refs.structure_ref import StructureRef

errors = []

def check(name, condition, detail=""):
    if not condition:
        errors.append(f"❌ FALHOU: {name} — {detail}")
    else:
        print(f"   ✅ {name}")

print("\n🔎 Testando StructureRef...\n")

# --- Factory from_id (caminho novo)
ref_new = StructureRef.from_id(42)
check("from_id cria structure_id correto",   ref_new.structure_id == 42)
check("from_id sem alias_legacy_aba",        ref_new.alias_legacy_aba is None)
check("db_key novo retorna int",             ref_new.db_key() == 42)
check("db_column novo retorna structure_id", ref_new.db_column() == "structure_id")

# --- Factory from_aba (caminho legado)
ref_leg = StructureRef.from_aba(aba="PETR4_CALL_120", structure_id=7)
check("from_aba guarda alias_legacy_aba",    ref_leg.alias_legacy_aba == "PETR4_CALL_120")
check("from_aba guarda structure_id",        ref_leg.structure_id == 7)
check("db_key legado retorna string aba",    ref_leg.db_key() == "PETR4_CALL_120")
check("db_column legado retorna 'aba'",      ref_leg.db_column() == "aba")

# --- Frozen (imutável)
try:
    ref_new.structure_id = 99  # type: ignore
    errors.append("❌ FALHOU: deveria ser frozen/imutável")
except Exception:
    print("   ✅ frozen=True funciona (imutável)")

# --- __str__
check("str com legado menciona legacy",      "legacy" in str(ref_leg))
check("str sem legado não menciona legacy",  "legacy" not in str(ref_new))

# --- Resultado
print()
if errors:
    for e in errors:
        print(e)
    print(f"\n💥 {len(errors)} erro(s) encontrado(s). Corrija antes de continuar.")
    sys.exit(1)
else:
    print("🎉 Todos os testes passaram! StructureRef está pronto.\n")
    sys.exit(0)
