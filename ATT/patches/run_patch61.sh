#!/usr/bin/env bash
# patch_61 -- cleanup tmp scripts + commit
# Executar a partir da raiz do projeto:
#   bash ATT/patches/run_patch61.sh

set -e

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "=== patch_61: dry-run ==="
python ATT/patches/patch_61_cleanup_tmp_scripts.py --dry-run

echo ""
read -rp "Confirmar execucao real? [s/N] " CONFIRM
if [[ "$CONFIRM" != "s" && "$CONFIRM" != "S" ]]; then
    echo "Abortado."
    exit 0
fi

echo ""
echo "=== patch_61: execucao ==="
python ATT/patches/patch_61_cleanup_tmp_scripts.py

echo ""
echo "=== pytest patch_61 ==="
python -m pytest ATT/tests/test_patch61.py -v

echo ""
echo "=== git status ==="
git status

echo ""
echo "=== git add + commit ==="
git add -A
git commit -m "chore(scripts): patch_61 -- remove tmp_* residuals from patch_53b"

echo ""
echo "=== git push ==="
git push

echo ""
echo "patch_61 concluido e publicado."
