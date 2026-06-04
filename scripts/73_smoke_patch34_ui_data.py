"""
73_smoke_patch34_ui_data.py
Smoke de integracao para patch_34: UIDataModel sem mocks, derived.db real.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from UI.models.ui_data import UIDataModel


def check(label: str, condition: bool, detail: str = "") -> bool:
    status = "OK  " if condition else "FAIL"
    line = f"  [{status}] {label}"
    if detail:
        line += f" -- {detail}"
    print(line)
    return condition


def main() -> int:
    print("=" * 50)
    print("  smoke patch_34: UIDataModel")
    print("=" * 50)
    failures = 0

    # instancia
    try:
        m = UIDataModel()
        m.refresh()
        print("  [OK  ] UIDataModel instanciado e refresh() executado")
    except Exception as exc:
        print(f"  [FAIL] UIDataModel: {exc}")
        return 1

    # _structure_filter_col -- canonica
    try:
        col = m._structure_filter_col({"structure_id": "structure_id"})
        failures += 0 if check(
            "_structure_filter_col retorna str 'structure_id'",
            col == "structure_id" and isinstance(col, str)
        ) else 1
    except Exception as exc:
        print(f"  [FAIL] _structure_filter_col: {exc}")
        failures += 1

    # _structure_filter_col -- rejeita aba
    try:
        m._structure_filter_col({"aba": "aba"})
        print("  [FAIL] _structure_filter_col({'aba'}) deveria ter lancado RuntimeError")
        failures += 1
    except RuntimeError:
        print("  [OK  ] _structure_filter_col({'aba'}) lancou RuntimeError corretamente")

    # _resolve_structure_key -- string numerica
    try:
        val = m._resolve_structure_key("7")
        failures += 0 if check(
            "_resolve_structure_key('7') == 7",
            val == 7 and isinstance(val, int)
        ) else 1
    except Exception as exc:
        print(f"  [FAIL] _resolve_structure_key: {exc}")
        failures += 1

    # _resolve_structure_key -- rejeita nao numerico
    try:
        m._resolve_structure_key("BOVA11")
        print("  [FAIL] _resolve_structure_key('BOVA11') deveria ter lancado ValueError")
        failures += 1
    except ValueError:
        print("  [OK  ] _resolve_structure_key('BOVA11') lancou ValueError corretamente")

    # get_structure_ids
    try:
        ids = m.get_structure_ids()
        failures += 0 if check(
            "get_structure_ids() lista nao vazia",
            isinstance(ids, list) and len(ids) > 0,
            str(ids[:5])
        ) else 1
    except Exception as exc:
        print(f"  [FAIL] get_structure_ids(): {exc}")
        failures += 1
        ids = []

    # get_abas alias
    try:
        failures += 0 if check(
            "get_abas() == get_structure_ids()",
            m.get_abas() == m.get_structure_ids()
        ) else 1
    except Exception as exc:
        print(f"  [FAIL] get_abas(): {exc}")
        failures += 1

    # get_decisions sem filtro
    try:
        rows = m.get_decisions(filters={})
        failures += 0 if check(
            "get_decisions() retorna lista",
            isinstance(rows, list),
            f"{len(rows)} linhas"
        ) else 1
        if rows:
            failures += 0 if check(
                "rows: structure_id nunca nulo",
                all(r.get("structure_id") is not None for r in rows)
            ) else 1
            failures += 0 if check(
                "rows: aba presente (compat leitura)",
                all("aba" in r for r in rows)
            ) else 1
    except Exception as exc:
        print(f"  [FAIL] get_decisions(): {exc}")
        failures += 1
        rows = []

    # get_decisions com filtro structure_id valido
    if ids:
        try:
            filtered = m.get_decisions(filters={"structure_id": ids[0]})
            failures += 0 if check(
                f"get_decisions(structure_id={ids[0]!r}) filtra",
                isinstance(filtered, list),
                f"{len(filtered)} linhas"
            ) else 1
        except Exception as exc:
            print(f"  [FAIL] get_decisions filtrado: {exc}")
            failures += 1

    # get_decisions com filtro aba legado -- nao deve filtrar, nao deve crashar
    try:
        rows_aba = m.get_decisions(filters={"aba": "qualquer"})
        failures += 0 if check(
            "get_decisions({'aba': ...}) nao crasha (retorna todos)",
            isinstance(rows_aba, list)
        ) else 1
    except Exception as exc:
        print(f"  [FAIL] get_decisions filtro aba: {exc}")
        failures += 1

    # get_decisions com structure_id invalido -- deve lancar ValueError
    try:
        m.get_decisions(filters={"structure_id": "BOVA11"})
        print("  [FAIL] get_decisions({'structure_id': 'BOVA11'}) deveria ter lancado ValueError")
        failures += 1
    except ValueError:
        print("  [OK  ] get_decisions({'structure_id': 'BOVA11'}) lancou ValueError corretamente")

    # check_database_status -- sem mode=aba/id
    try:
        status = m.check_database_status()
        failures += 0 if check(
            "check_database_status: mode=canonical presente",
            "mode=canonical" in status
        ) else 1
        failures += 0 if check(
            "check_database_status: sem mode=aba",
            "mode=aba" not in status
        ) else 1
    except Exception as exc:
        print(f"  [FAIL] check_database_status(): {exc}")
        failures += 1

    # resumo
    print("=" * 50)
    if failures == 0:
        print("RESULTADO: PASS -- patch_34 smoke OK")
    else:
        print(f"RESULTADO: FAIL -- {failures} verificacao(oes) falharam")
    print("=" * 50)

    return failures


if __name__ == "__main__":
    sys.exit(main())
