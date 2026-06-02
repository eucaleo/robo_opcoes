"""
Smoke test — Fase 4 / Etapa D
Valida CRUD completo do StructuresRepository.

Fluxo (9 etapas):
  1. garantir schema
  2. criar estrutura
  3. adicionar 2 legs
  4. listar estruturas
  5. buscar estrutura com legs
  6. atualizar metadados
  7. substituir legs
  8. arquivar estrutura
  9. reler e validar resultado final
"""

import sys
from pathlib import Path

# ── garante que o raiz do projeto está no path ──────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from infra.bootstrap_structures_schema import ensure_structures_schema
from repositories.structures_repository import StructuresRepository
from scripts._smoke_context import update_context, clear_context


# ── helpers ─────────────────────────────────────────────────────────────────

def _assert(condition: bool, msg: str) -> None:
    if not condition:
        raise AssertionError(f"FALHOU: {msg}")


def _ok(msg: str) -> None:
    print(f"  ✓ {msg}")


# ── etapas ──────────────────────────────────────────────────────────────────

def etapa_1_garantir_schema() -> None:
    print("\n[1/9] Garantindo schema...")
    ensure_structures_schema()
    _ok("schema criado/confirmado em dados/app.db")


def etapa_2_criar_estrutura(repo: StructuresRepository) -> int:
    print("\n[2/9] Criando estrutura...")

    structure_id = repo.create_structure({
        "name": "BOVA11 Condor Maio/2026",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "status": "active",
        "notes": "smoke test fase 4",
    })

    _assert(isinstance(structure_id, int) and structure_id > 0,
            "structure_id deve ser inteiro positivo")
    _ok(f"estrutura criada: id={structure_id}")

    update_context(structure_id=structure_id)
    return structure_id


def etapa_3_adicionar_legs(repo: StructuresRepository, structure_id: int) -> None:
    print("\n[3/9] Adicionando 2 legs...")

    leg1_id = repo.add_leg(structure_id, {
        "position_side": "LONG",
        "option_type": "CALL",
        "symbol": "BOVAE195",
        "strike": 195.0,
        "expiration_date": "2026-05-15",
        "quantity": 1000,
        "premium": None,
        "multiplier": 1.0,
        "leg_order": 1,
        "notes": "leg 1 — smoke",
    })

    leg2_id = repo.add_leg(structure_id, {
        "position_side": "SHORT",
        "option_type": "CALL",
        "symbol": "BOVAE200",
        "strike": 200.0,
        "expiration_date": "2026-05-15",
        "quantity": 1000,
        "premium": None,
        "multiplier": 1.0,
        "leg_order": 2,
        "notes": "leg 2 — smoke",
    })

    _assert(isinstance(leg1_id, int) and leg1_id > 0, "leg1_id deve ser positivo")
    _assert(isinstance(leg2_id, int) and leg2_id > 0, "leg2_id deve ser positivo")
    _assert(leg1_id != leg2_id, "legs devem ter ids distintos")
    _ok(f"legs inseridas: leg1_id={leg1_id}, leg2_id={leg2_id}")


def etapa_4_listar_estruturas(repo: StructuresRepository, structure_id: int) -> None:
    print("\n[4/9] Listando estruturas ativas...")

    lista = repo.list_structures(include_archived=False)

    _assert(isinstance(lista, list), "list_structures deve retornar lista")
    ids = [s["id"] for s in lista]
    _assert(structure_id in ids, f"structure_id={structure_id} deve aparecer na listagem")

    for s in lista:
        _assert(s["status"] == "active",
                f"listagem sem archived deve conter só active — encontrou: {s['status']}")

    _ok(f"{len(lista)} estrutura(s) ativa(s) listada(s)")


def etapa_5_buscar_com_legs(repo: StructuresRepository, structure_id: int) -> None:
    print("\n[5/9] Buscando estrutura com legs...")

    structure = repo.get_structure(structure_id)

    _assert(structure is not None, "get_structure não deve retornar None")
    _assert(structure["id"] == structure_id, "id deve bater")
    _assert(structure["underlying_asset"] == "BOVA11", "underlying_asset deve ser BOVA11")
    _assert(structure["alias_legacy_aba"] == "BOVA11", "alias_legacy_aba deve ser BOVA11")
    _assert("legs" in structure, "estrutura deve conter campo 'legs'")

    legs = structure["legs"]
    _assert(len(legs) == 2, f"deve ter 2 legs, encontrou {len(legs)}")

    orders = [leg["leg_order"] for leg in legs]
    _assert(orders == sorted(orders), "legs devem estar ordenadas por leg_order")

    sides = {leg["position_side"] for leg in legs}
    _assert("LONG" in sides and "SHORT" in sides,
            "deve ter um LONG e um SHORT")

    _ok(f"estrutura carregada com {len(legs)} legs — ordem e lados corretos")


def etapa_6_atualizar_metadados(repo: StructuresRepository, structure_id: int) -> None:
    print("\n[6/9] Atualizando metadados da estrutura...")

    repo.update_structure(structure_id, {
        "name": "BOVA11 Condor Maio/2026 — Atualizada",
        "notes": "atualizado pelo smoke fase 4",
    })

    updated = repo.get_structure(structure_id)

    _assert(updated is not None, "estrutura deve existir após update")
    _assert(updated["name"] == "BOVA11 Condor Maio/2026 — Atualizada",
            "name deve refletir o update")
    _assert(updated["notes"] == "atualizado pelo smoke fase 4",
            "notes deve refletir o update")
    _assert(updated["underlying_asset"] == "BOVA11",
            "underlying_asset não deve mudar")
    _assert(len(updated["legs"]) == 2,
            "legs não devem ser afetadas pelo update de metadados")

    _ok("metadados atualizados e legs preservadas")


def etapa_7_substituir_legs(repo: StructuresRepository, structure_id: int) -> None:
    print("\n[7/9] Substituindo legs (replace_legs)...")

    novas_legs = [
        {
            "position_side": "LONG",
            "option_type": "PUT",
            "symbol": "BOVAM190",
            "strike": 190.0,
            "expiration_date": "2026-06-20",
            "quantity": 2000,
            "premium": 1.50,
            "multiplier": 1.0,
            "leg_order": 1,
            "notes": "nova leg 1",
        },
        {
            "position_side": "SHORT",
            "option_type": "PUT",
            "symbol": "BOVAM185",
            "strike": 185.0,
            "expiration_date": "2026-06-20",
            "quantity": 2000,
            "premium": 0.80,
            "multiplier": 1.0,
            "leg_order": 2,
            "notes": "nova leg 2",
        },
        {
            "position_side": "LONG",
            "option_type": "PUT",
            "symbol": "BOVAM180",
            "strike": 180.0,
            "expiration_date": "2026-06-20",
            "quantity": 2000,
            "premium": 0.40,
            "multiplier": 1.0,
            "leg_order": 3,
            "notes": "nova leg 3",
        },
    ]

    repo.replace_legs(structure_id, novas_legs)

    after = repo.get_structure(structure_id)
    legs = after["legs"]

    _assert(len(legs) == 3, f"após replace deve ter 3 legs, encontrou {len(legs)}")

    strikes = [leg["strike"] for leg in legs]
    _assert(190.0 in strikes, "strike 190 deve estar presente")
    _assert(185.0 in strikes, "strike 185 deve estar presente")
    _assert(180.0 in strikes, "strike 180 deve estar presente")

    for leg in legs:
        _assert(leg["option_type"] == "PUT", "todas as novas legs devem ser PUT")
        _assert(leg["expiration_date"] == "2026-06-20",
                "vencimento deve ser 2026-06-20")

    _ok(f"replace_legs OK — {len(legs)} legs novas, antigas removidas")


def etapa_8_arquivar(repo: StructuresRepository, structure_id: int) -> None:
    print("\n[8/9] Arquivando estrutura...")

    repo.archive_structure(structure_id)

    archived = repo.get_structure(structure_id)
    _assert(archived is not None, "estrutura deve existir após archive")
    _assert(archived["status"] == "archived",
            f"status deve ser 'archived', encontrou '{archived['status']}'")

    lista_ativas = repo.list_structures(include_archived=False)
    ids_ativos = [s["id"] for s in lista_ativas]
    _assert(structure_id not in ids_ativos,
            "estrutura arquivada NÃO deve aparecer na listagem de ativas")

    lista_todas = repo.list_structures(include_archived=True)
    ids_todas = [s["id"] for s in lista_todas]
    _assert(structure_id in ids_todas,
            "estrutura arquivada DEVE aparecer com include_archived=True")

    _ok("estrutura arquivada e ausente da listagem de ativas")


def etapa_9_validar_estado_final(repo: StructuresRepository, structure_id: int) -> None:
    print("\n[9/9] Validando estado final...")

    final = repo.get_structure(structure_id)

    _assert(final is not None, "estrutura deve ser recuperável no estado final")
    _assert(final["id"] == structure_id, "id deve bater")
    _assert(final["status"] == "archived", "status final deve ser archived")
    _assert(final["name"] == "BOVA11 Condor Maio/2026 — Atualizada",
            "name deve refletir o update da etapa 6")
    _assert(len(final["legs"]) == 3,
            f"deve ter 3 legs (do replace), encontrou {len(final['legs'])}")
    _assert(final["underlying_asset"] == "BOVA11",
            "underlying_asset deve ser BOVA11")

    _ok("estado final consistente — todas as operações persistidas corretamente")


# ── main ────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("SMOKE — Fase 4 / StructuresRepository")
    print("=" * 60)

    clear_context()
    repo = StructuresRepository(db_path="dados/app.db")

    etapa_1_garantir_schema()
    structure_id = etapa_2_criar_estrutura(repo)
    etapa_3_adicionar_legs(repo, structure_id)
    etapa_4_listar_estruturas(repo, structure_id)
    etapa_5_buscar_com_legs(repo, structure_id)
    etapa_6_atualizar_metadados(repo, structure_id)
    etapa_7_substituir_legs(repo, structure_id)
    etapa_8_arquivar(repo, structure_id)
    etapa_9_validar_estado_final(repo, structure_id)

    print("\n" + "=" * 60)
    print("✅  SMOKE FASE 4 — TODAS AS ETAPAS OK")
    print("=" * 60)


if __name__ == "__main__":
    main()
