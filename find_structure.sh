#!/usr/bin/env bash
# find_structure.sh — Mapeia estrutura real do projeto
# Execute: ./find_structure.sh > estrutura.txt 2>&1

echo "====== ESTRUTURA DE DIRETÓRIOS ======"
find . -type f -name "*.py" | sort

echo ""
echo "====== ARQUIVOS COM 'structure_editor' ======"
find . -type f | grep -i "structure_editor"

echo ""
echo "====== ARQUIVOS COM 'structures_list' ======"
find . -type f | grep -i "structures_list"

echo ""
echo "====== ARQUIVOS COM 'list_panel' ======"
find . -type f | grep -i "list_panel"

echo ""
echo "====== ARQUIVOS COM 'editor_dialog' ======"
find . -type f | grep -i "editor_dialog"

echo ""
echo "====== TODO .PY QUE CONTÉM '_cmd_save' ======"
grep -rl "_cmd_save" . --include="*.py"

echo ""
echo "====== TODO .PY QUE CONTÉM '_populate_tree' ======"
grep -rl "_populate_tree" . --include="*.py"

echo ""
echo "====== TODO .PY QUE CONTÉM 'replace_legs' ======"
grep -rl "replace_legs" . --include="*.py"

echo ""
echo "====== TODO .PY QUE CONTÉM 'list_structures' ======"
grep -rl "list_structures" . --include="*.py"

echo ""
echo "====== PASTAS UI / VIEWS / DIALOGS / PANELS ======"
find . -type d | sort
