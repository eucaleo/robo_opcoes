#!/usr/bin/env python3
"""
patch_62_apply.py
-----------------
Valida pré-condições e registra a aplicação do patch_62 no PATCHES.md.

Não modifica código-fonte automaticamente — as edições acima são aplicadas
manualmente (ou via seu editor). Este script apenas:
  1. Verifica que _aba_resolver_mixin.py existe
  2. Verifica que _resolve_aba_from_structure_id NÃO está mais duplicado
  3. Verifica que get_payoff_by_aba tem warnings.warn
  4. Atualiza PATCHES.md
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = []


def check(label: str, condition: bool, detail: str = ""):
    status = "OK" if condition else "FAIL"
    CHECKS.append((status, label, detail))
    return condition


def run_checks():
    # 1. Mixin existe
    mixin = ROOT / "repositories" / "_aba_resolver_mixin.py"
    check(
        "mixin criado",
        mixin.exists(),
        str(mixin),
    )

    # 2. robo_legs_repository NÃO define mais _resolve_aba_from_structure_id
    legs_repo = (ROOT / "repositories" / "robo_legs_repository.py").read_text(encoding="utf-8")
    duplicated_legs = bool(
        re.search(r"def _resolve_aba_from_structure_id", legs_repo)
    )
    check(
        "robo_legs_repository sem _resolve_aba local",
        not duplicated_legs,
        "remova o método local da classe",
    )

    # 3. robo_legs_repository herda AbaResolverMixin
    check(
        "robo_legs_repository herda AbaResolverMixin",
        "AbaResolverMixin" in legs_repo,
    )

    # 4. robo_legs_status_repository NÃO define mais _resolve_aba_from_structure_id
    status_repo = (ROOT / "repositories" / "robo_legs_status_repository.py").read_text(encoding="utf-8")
    duplicated_status = bool(
        re.search(r"def _resolve_aba_from_structure_id", status_repo)
    )
    check(
        "robo_legs_status_repository sem _resolve_aba local",
        not duplicated_status,
        "remova o método local da classe",
    )

    # 5. robo_legs_status_repository herda AbaResolverMixin
    check(
        "robo_legs_status_repository herda AbaResolverMixin",
        "AbaResolverMixin" in status_repo,
    )

    # 6. L251 corrigido: não passa string nua para ref=
    check(
        "get_legs_by_structure_id usa StructureRef (não str nua)",
        "StructureRef(aba=aba" in legs_repo,
        "verifique L251",
    )

    # 7. get_payoff_by_aba tem deprecation warning
    svc = (ROOT / "services" / "derived_service.py").read_text(encoding="utf-8")
    check(
        "get_payoff_by_aba tem DeprecationWarning",
        "DeprecationWarning" in svc,
    )


def update_patches_md():
    patches_md = ROOT / "PATCHES.md"
    entry = """
---

## patch_62 — Auditoria wrappers `aba` / deduplicação AbaResolverMixin

**Data:** auto-registrado por patch_62_apply.py

### Alterações
| Arquivo | Ação |
|---|---|
| `repositories/_aba_resolver_mixin.py` | CRIADO — mixin compartilhado |
| `repositories/robo_legs_repository.py` | Herda mixin, remove método local, corrige L251 |
| `repositories/robo_legs_status_repository.py` | Herda mixin, remove método local |
| `services/derived_service.py` | Deprecação formal de `get_payoff_by_aba()` |

### Residuos confirmados como falsos positivos
- `db/derived_repo.py` — `aba` é coluna SQL e parâmetro interno, coberto por `_unwrap_aba()`
- `domain/payoff_features.py:148` — tupla de valores internos, sem wrapper
- `services/derived_service.py` linhas 181, 196, 260, 276 — passagem normal de parâmetro

### Pendente (patch_65)
- Remoção definitiva de `get_payoff_by_aba()`
"""
    content = patches_md.read_text(encoding="utf-8") if patches_md.exists() else ""
    if "patch_62" not in content:
        with open(patches_md, "a", encoding="utf-8") as f:
            f.write(entry)
        print("PATCHES.md atualizado.")
    else:
        print("PATCHES.md já contém entrada patch_62, pulando.")


def main():
    print("=" * 60)
    print("  VALIDAÇÃO patch_62")
    print("=" * 60)

    run_checks()

    all_ok = True
    for status, label, detail in CHECKS:
        icon = "✓" if status == "OK" else "✗"
        print(f"  [{icon}] {label}")
        if status == "FAIL" and detail:
            print(f"        → {detail}")
        if status == "FAIL":
            all_ok = False

    print("=" * 60)

    if all_ok:
        update_patches_md()
        print("\n  patch_62 validado com sucesso.")
        sys.exit(0)
    else:
        print("\n  Corrija os itens marcados com [✗] e rode novamente.")
        sys.exit(1)


if __name__ == "__main__":
    main()
