# ATT/patches/patch_70_mainwindow_dialog_wiring.py
"""
patch_70 -- Wiring MainWindow <-> StructureEditorDialog
Data  : 2026-06-05
Status: pendente

Problema
--------
MainWindow._on_structure_edit_request() referencia self._db_path
que nunca foi definido em __init__, causando AttributeError em runtime.
_setup_structures_tab usava db_path hardcoded duplicando a constante
PROJECT_ROOT / "dados" / "app.db".

Solução
-------
1. Definir self._db_path em __init__, logo após self.root — ponto
   canônico único para o caminho do banco principal.
2. _setup_structures_tab passa self._db_path ao StructuresListPanel
   (elimina hardcode duplicado).
3. _on_structure_edit_request já estava correto — apenas documentado
   com referência ao patch.

Arquivos modificados
--------------------
- UI/main_window.py  (3 hunks)

Testes cobertos
---------------
ATT/tests/test_patch70_integration.py
  TestPatch70StaticChecks         (6 testes)
  TestOnStructureEditRequestCriar (4 testes)
  TestOnStructureEditRequestEditar(3 testes)
  TestLoadExisting                (3 testes)
  TestCmdSave                    (10 testes)
  TestIntegracaoLegs              (3 testes)
  Total: 29 testes
"""

CHANGES = [
    {
        "file": "UI/main_window.py",
        "hunk": 1,
        "description": "Definir self._db_path em __init__",
        "after_line": "self.root.geometry(\"1400x900\")",
        "insert": "        self._db_path = str(PROJECT_ROOT / \"dados\" / \"app.db\")"
                  "  # patch_70",
    },
    {
        "file": "UI/main_window.py",
        "hunk": 2,
        "description": "_setup_structures_tab: db_path=self._db_path",
        "replace": "db_path=str(PROJECT_ROOT / \"dados\" / \"app.db\")",
        "with":    "db_path=self._db_path,  # patch_70",
    },
    {
        "file": "UI/main_window.py",
        "hunk": 3,
        "description": "Docstring de _on_structure_edit_request atualizada",
    },
]
