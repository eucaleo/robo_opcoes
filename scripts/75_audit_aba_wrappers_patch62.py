"""
Script de auditoria para patch_62.
Mapeia todos os pontos de uso de 'aba' como dado operacional
nos wrappers de compatibilidade remanescentes.

Executar:
    python scripts/75_audit_aba_wrappers_patch62.py
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

ROOT = Path(__file__).resolve().parent.parent

TARGET_FILES = [
    "repositories/robo_legs_repository.py",
    "repositories/robo_legs_status_repository.py",
    "services/derived_service.py",
    "domain/payoff_features.py",
    "db/derived_repo.py",
]

# Padroes que indicam uso operacional de 'aba' (nao apenas comentario)
WRAPPER_PATTERNS = [
    "_resolve_aba_from_structure_id",
    "get_payoff_by_aba",
    "get_legs_by_aba",
    "get_legs(",
    ".get(\"aba\"",
    ".get('aba'",
    "[\"aba\"]",
    "['aba']",
    "aba=",
    ", aba,",
    "(aba,",
    "alias_legacy_aba",
    "aba_str",
    "_unwrap_aba",
]

# Padroes que indicam que a linha e apenas bridge/alias -- nao e residuo perigoso
BRIDGE_OK_PATTERNS = [
    "alias_legacy_aba",
    "_unwrap_aba",
    "aba_str",
    "# BRIDGE",
    "# bridge",
    "# alias",
    "# readonly",
    "# compat",
    "alias readonly",
]


@dataclass
class WrapperOccurrence:
    arquivo: str
    linha: int
    conteudo: str
    pattern: str
    classificacao: str  -- "BRIDGE_OK" | "WRAPPER_ATIVO" | "RESIDUO_SUSPEITO"


def classificar(linha: str, pattern: str) -> str:
    for bp in BRIDGE_OK_PATTERNS:
        if bp in linha:
            return "BRIDGE_OK"
    if "_resolve_aba_from_structure_id" in linha:
        return "WRAPPER_ATIVO"
    if "get_payoff_by_aba" in linha or "get_legs_by_aba" in linha:
        return "WRAPPER_ATIVO"
    if ".get(\"aba\"" in linha or ".get('aba'" in linha:
        return "BRIDGE_OK"
    if "[\"aba\"]" in linha or "['aba']" in linha:
        return "BRIDGE_OK"
    return "RESIDUO_SUSPEITO"


def auditar_arquivo(rel_path: str) -> List[WrapperOccurrence]:
    path = ROOT / rel_path
    ocorrencias = []
    if not path.exists():
        print(f"  [AUSENTE] {rel_path}")
        return ocorrencias

    linhas = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, linha in enumerate(linhas, start=1):
        linha_stripped = linha.strip()
        if linha_stripped.startswith("#"):
            continue
        for pattern in WRAPPER_PATTERNS:
            if pattern in linha:
                clf = classificar(linha, pattern)
                ocorrencias.append(WrapperOccurrence(
                    arquivo=rel_path,
                    linha=i,
                    conteudo=linha.rstrip(),
                    pattern=pattern,
                    classificacao=clf,
                ))
                break  -- um match por linha
    return ocorrencias


def main() -> None:
    print("=" * 70)
    print("  AUDITORIA DE WRAPPERS ABA -- pre-patch_62")
    print(f"  ROOT: {ROOT}")
    print("=" * 70)

    todas: List[WrapperOccurrence] = []

    for rel in TARGET_FILES:
        print(f"\n-- {rel} " + "-" * (60 - len(rel)))
        ocorrencias = auditar_arquivo(rel)
        if not ocorrencias:
            print("  [OK] nenhum padrao de wrapper encontrado")
        for oc in ocorrencias:
            marker = {
                "BRIDGE_OK": "  [OK]  ",
                "WRAPPER_ATIVO": "  [WRAP]",
                "RESIDUO_SUSPEITO": "  [!]  ",
            }.get(oc.classificacao, "  [?]  ")
            print(f"{marker} L{oc.linha:04d} | {oc.conteudo[:80]}")
        todas.extend(ocorrencias)

    print("\n" + "=" * 70)
    print("  RESUMO")
    print("=" * 70)

    bridge_ok = [o for o in todas if o.classificacao == "BRIDGE_OK"]
    wrappers  = [o for o in todas if o.classificacao == "WRAPPER_ATIVO"]
    suspeitos = [o for o in todas if o.classificacao == "RESIDUO_SUSPEITO"]

    print(f"  BRIDGE_OK        : {len(bridge_ok):3d}  (adapter layer -- correto)")
    print(f"  WRAPPER_ATIVO    : {len(wrappers):3d}  (wrappers de compatibilidade -- revisar)")
    print(f"  RESIDUO_SUSPEITO : {len(suspeitos):3d}  (candidatos a remocao ou documentacao)")

    if suspeitos:
        print("\n  Suspeitos para revisar:")
        for o in suspeitos:
            print(f"    {o.arquivo}:{o.linha} -- {o.conteudo.strip()[:70]}")

    print("\n  Wrappers ativos (precisam de decisao arquitetural):")
    for o in wrappers:
        print(f"    {o.arquivo}:{o.linha} -- {o.conteudo.strip()[:70]}")

    print("=" * 70)


if __name__ == "__main__":
    main()
