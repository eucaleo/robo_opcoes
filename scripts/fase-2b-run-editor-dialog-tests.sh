#!/usr/bin/env bash
set -euo pipefail

TEST_FILE="ATT/tests/test_structure_editor_dialog.py"
EVID_DIR="docs/checkpoints/evidencias"
EVID_FILE="$EVID_DIR/fase-2b-pytest-editor-dialog-atual.txt"

mkdir -p "$EVID_DIR"

echo "Rodando pytest focado em $TEST_FILE..."
python -m pytest "$TEST_FILE" -q > "$EVID_FILE" 2>&1

cat "$EVID_FILE"

echo
echo "Evidência salva em:"
echo "$EVID_FILE"
