# scripts/diagnose_patch10.py
"""
Diagnóstico patch_10 -- roda direto: python scripts/diagnose_patch10.py
Não precisa de pytest nem de display gráfico.
Verifica: arquivos, imports, banco, métodos esperados.
"""
import sys
import os
import sqlite3
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PASS = "[OK]"
FAIL = "[FALHOU]"
WARN = "[AVISO] "

results = []

def check(label, fn):
    try:
        fn()
        results.append((PASS, label))
        print(f"  {PASS} {label}")
    except Exception as e:
        results.append((FAIL, f"{label}  {e}"))
        print(f"  {FAIL} {label}")
        print(f"       {e}")


print("\n" + "="*60)
print("  DIAGNÓSTICO PATCH_10 -- Fase 5 Estruturas")
print("="*60)

#  1. Arquivos existem 
print("\n[1] Arquivos no disco")

FILES = {
    "StructuresListPanel":    ROOT / "UI/components/structures_list_panel.py",
    "StructureEditorDialog":  ROOT / "UI/components/structure_editor_dialog.py",
    "StructuresRepository":   ROOT / "repositories/structures_repository.py",
    "MainWindow":             ROOT / "UI/main_window.py",
}

for name, path in FILES.items():
    check(f"{name} existe em {path.relative_to(ROOT)}",
          lambda p=path: (_ for _ in ()).throw(FileNotFoundError(p)) if not p.exists() else None)

#  2. Sintaxe / imports 
print("\n[2] Importação dos módulos")

def _import(path, modname):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

check("repositories.structures_repository importa",
      lambda: __import__("repositories.structures_repository"))

check("UI.components.structures_list_panel importa",
      lambda: __import__("UI.components.structures_list_panel",
                          fromlist=["StructuresListPanel"]))

check("UI.components.structure_editor_dialog importa",
      lambda: __import__("UI.components.structure_editor_dialog",
                          fromlist=["StructureEditorDialog"]))

#  3. main_window.py tem os métodos novos 
print("\n[3] main_window.py -- métodos patch_10")

mw_src = (ROOT / "UI/main_window.py").read_text(encoding="utf-8")

for method in [
    "_setup_structures_tab",
    "_on_structure_selected",
    "_on_structure_edit_request",
]:
    check(f"Método '{method}' presente",
          lambda m=method: (_ for _ in ()).throw(
              AssertionError(f"'{m}' não encontrado")) if m not in mw_src else None)

for imp in [
    "from UI.components.structures_list_panel import StructuresListPanel",
    "from UI.components.structure_editor_dialog import StructureEditorDialog",
]:
    check(f"Import '{imp.split()[-1]}' presente",
          lambda i=imp: (_ for _ in ()).throw(
              AssertionError(f"import ausente")) if i not in mw_src else None)

check("db_path usa PROJECT_ROOT (path absoluto)",
      lambda: (_ for _ in ()).throw(
          AssertionError("db_path hardcoded como string simples detectado")
      ) if '"dados/app.db"' in mw_src and "PROJECT_ROOT" not in mw_src else None)

#  4. Banco de dados 
print("\n[4] Banco app.db -- tabelas structures e structure_legs")

DB_CANDIDATES = [
    ROOT / "dados" / "app.db",
    ROOT / "app.db",
    ROOT / "data" / "app.db",
]

db_found = None
for c in DB_CANDIDATES:
    if c.exists():
        db_found = c
        break

if db_found:
    print(f"  {PASS} Banco encontrado: {db_found.relative_to(ROOT)}")

    def check_tables():
        conn = sqlite3.connect(db_found)
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = {r[0] for r in cur.fetchall()}
        conn.close()
        missing = {"structures", "structure_legs"} - tables
        if missing:
            raise AssertionError(f"Tabelas ausentes: {missing}")

    check("Tabelas structures + structure_legs existem", check_tables)

    def check_columns():
        conn = sqlite3.connect(db_found)
        cur = conn.execute("PRAGMA table_info(structures)")
        cols_s = {r[1] for r in cur.fetchall()}
        cur = conn.execute("PRAGMA table_info(structure_legs)")
        cols_l = {r[1] for r in cur.fetchall()}
        conn.close()

        req_s = {"id","name","underlying_asset","status"}
        req_l = {"id","structure_id","position_side","option_type","strike","expiration_date","quantity"}

        miss_s = req_s - cols_s
        miss_l = req_l - cols_l
        if miss_s:
            raise AssertionError(f"structures faltam colunas: {miss_s}")
        if miss_l:
            raise AssertionError(f"structure_legs faltam colunas: {miss_l}")

    check("Colunas obrigatórias presentes", check_columns)

    def check_repo_live():
        from repositories.structures_repository import StructuresRepository
        repo = StructuresRepository(str(db_found))
        rows = repo.list_structures(include_archived=True)
        print(f"        {len(rows)} estrutura(s) no banco")

    check("StructuresRepository.list_structures() roda no banco real", check_repo_live)

else:
    print(f"  {WARN} app.db não encontrado em nenhum candidato:")
    for c in DB_CANDIDATES:
        print(f"       {c}")

#  5. Resumo 
print("\n" + "="*60)
total  = len(results)
passed = sum(1 for r in results if r[0] == PASS)
failed = total - passed

print(f"  Resultado: {passed}/{total} checks passaram")
if failed:
    print(f"\n  {FAIL} Falhas:")
    for r in results:
        if r[0] == FAIL:
            print(f"    * {r[1]}")
else:
    print(f"\n  {PASS} Tudo OK -- patch_10 pronto para smoke manual")

print("="*60 + "\n")
sys.exit(0 if failed == 0 else 1)
