"""
Smoke test patch_10 -- Structures API (FastAPI local)
Pré-requisito: servidor rodando em http://localhost:8000
Execute em terminal separado:
    uvicorn main:app --reload --port 8000

Rode o smoke:
    python scripts/11_smoke_structures_api.py
"""

import sys
import requests
from pathlib import Path

BASE = "http://localhost:8000"
SEP  = "=" * 55
OK   = 0
FAIL = 0


def check(label: str, condition: bool, detail: str = ""):
    global OK, FAIL
    if condition:
        print(f"   {label}")
        OK += 1
    else:
        print(f"  [x] {label}   {detail}")
        FAIL += 1


def section(title: str):
    print(f"\n{SEP}\n{title}\n{SEP}")


#  helpers 

def post(path, payload):
    return requests.post(f"{BASE}{path}", json=payload)

def get(path, params=None):
    return requests.get(f"{BASE}{path}", params=params or {})

def put(path, payload):
    return requests.put(f"{BASE}{path}", json=payload)


#  testes 

def test_create_valid():
    section("1. CREATE -- válido")
    r = post("/structures", {
        "name": "BOVA11 Condor Teste",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "notes": "smoke test patch_10"
    })
    check("status 201", r.status_code == 201, r.text)
    data = r.json()
    check("id presente", "id" in data, str(data))
    check("status=active", data.get("status") == "active")
    check("name correto", data.get("name") == "BOVA11 Condor Teste")
    return data.get("id")


def test_create_invalid():
    section("2. CREATE -- inválido (name vazio)")
    r = post("/structures", {
        "name": "",
        "underlying_asset": "BOVA11"
    })
    check("status 400", r.status_code == 400, r.text)


def test_get(structure_id: int):
    section("3. GET by ID")
    r = get(f"/structures/{structure_id}")
    check("status 200", r.status_code == 200, r.text)
    data = r.json()
    check("id confere", data.get("id") == structure_id)
    check("legs presente", "legs" in data)


def test_get_not_found():
    section("4. GET -- not found")
    r = get("/structures/999999")
    check("status 404", r.status_code == 404, r.text)


def test_list():
    section("5. LIST")
    r = get("/structures")
    check("status 200", r.status_code == 200, r.text)
    data = r.json()
    check("total presente", "total" in data)
    check("items é lista", isinstance(data.get("items"), list))
    check("total >= 1", data.get("total", 0) >= 1)


def test_list_filter(structure_id: int):
    section("6. LIST -- filtro por underlying_asset")
    r = get("/structures", {"underlying_asset": "BOVA11"})
    check("status 200", r.status_code == 200, r.text)
    data = r.json()
    check("retornou itens", data.get("total", 0) >= 1)


def test_update(structure_id: int):
    section("7. UPDATE")
    r = put(f"/structures/{structure_id}", {"notes": "atualizado pelo smoke"})
    check("status 200", r.status_code == 200, r.text)
    data = r.json()
    check("notes atualizado", data.get("notes") == "atualizado pelo smoke")


def test_add_leg(structure_id: int):
    section("8. ADD LEG")
    r = post(f"/structures/{structure_id}/legs", {
        "position_side": "LONG",
        "option_type": "CALL",
        "strike": 130.0,
        "expiration_date": "2026-06-20",
        "quantity": 1000,
        "leg_order": 1
    })
    check("status 201", r.status_code == 201, r.text)
    data = r.json()
    check("legs tem 1 item", len(data.get("legs", [])) >= 1)


def test_add_leg_invalid(structure_id: int):
    section("9. ADD LEG -- inválido (position_side errado)")
    r = post(f"/structures/{structure_id}/legs", {
        "position_side": "COMPRA",
        "option_type": "CALL",
        "strike": 130.0,
        "expiration_date": "2026-06-20",
        "quantity": 1000,
    })
    check("status 400", r.status_code == 400, r.text)


def test_replace_legs(structure_id: int):
    section("10. REPLACE LEGS")
    r = put(f"/structures/{structure_id}/legs", {"legs": [
        {
            "position_side": "LONG",
            "option_type": "CALL",
            "strike": 125.0,
            "expiration_date": "2026-06-20",
            "quantity": 2000,
            "leg_order": 1
        },
        {
            "position_side": "SHORT",
            "option_type": "CALL",
            "strike": 135.0,
            "expiration_date": "2026-06-20",
            "quantity": 2000,
            "leg_order": 2
        }
    ]})
    check("status 200", r.status_code == 200, r.text)
    data = r.json()
    check("2 legs após replace", len(data.get("legs", [])) == 2)


def test_archive(structure_id: int):
    section("11. ARCHIVE")
    r = post(f"/structures/{structure_id}/archive", {})
    check("status 200", r.status_code == 200, r.text)
    data = r.json()
    check("status=archived", data.get("status") == "archived")


def test_list_archived(structure_id: int):
    section("12. LIST -- include_archived=true")
    r = get("/structures", {"include_archived": "true"})
    check("status 200", r.status_code == 200, r.text)
    data = r.json()
    ids = [s["id"] for s in data.get("items", [])]
    check("estrutura arquivada aparece", structure_id in ids)


#  main 

def main():
    print(SEP)
    print("SMOKE -- patch_10: Structures API")
    print(SEP)

    # verifica servidor
    try:
        requests.get(BASE, timeout=3)
    except Exception:
        print(f"\n[FALHOU]  Servidor não está rodando em {BASE}")
        print("    Execute em outro terminal:")
        print("    uvicorn main:app --reload --port 8000\n")
        sys.exit(1)

    sid = test_create_valid()
    test_create_invalid()

    if sid:
        test_get(sid)
        test_get_not_found()
        test_list()
        test_list_filter(sid)
        test_update(sid)
        test_add_leg(sid)
        test_add_leg_invalid(sid)
        test_replace_legs(sid)
        test_archive(sid)
        test_list_archived(sid)
    else:
        print("\n[AVISO]  CREATE falhou -- pulando testes dependentes")

    print(f"\n{SEP}")
    print(f"RESULTADO: {OK}   {FAIL} [x]")
    print(SEP)
    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()
