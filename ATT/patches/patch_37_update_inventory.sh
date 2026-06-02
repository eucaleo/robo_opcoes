#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log_ok()   { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_info() { echo -e "        $1"; }

PROJECT_ROOT="/c/users/eucal/projeto"
ATT_DIR="$PROJECT_ROOT/ATT"
TESTS_DIR="$ATT_DIR/tests"
PATCHES_DIR="$PROJECT_ROOT/ATT/patches"

# Localiza inventário
INVENTORY=""
for candidate in \
    "$ATT_DIR/PATCHES.md" \
    "$ATT_DIR/CHANGELOG.md" \
    "$PROJECT_ROOT/PATCHES.md" \
    "$PROJECT_ROOT/docs/PATCHES.md"
do
    [[ -f "$candidate" ]] && { INVENTORY="$candidate"; break; }
done

if [[ -z "$INVENTORY" ]]; then
    log_warn "Inventário não encontrado. Criando $ATT_DIR/PATCHES.md..."
    mkdir -p "$ATT_DIR"
    INVENTORY="$ATT_DIR/PATCHES.md"
    printf '# Inventário de Patches\n\n| Patch | Data | Status | Branch | Descrição |\n|-------|------|--------|--------|-----------|\n' > "$INVENTORY"
    log_ok "Criado: $INVENTORY"
fi

grep -q "patch_37" "$INVENTORY" 2>/dev/null \
    && { log_warn "patch_37 já registrado — nenhuma alteração."; exit 0; }

TS="$(date '+%Y%m%d_%H%M%S')"
cp "$INVENTORY" "${INVENTORY}.bak_${TS}"

echo "| patch_37 | $(date '+%Y-%m-%d') | ✅ Aplicado | patch/3a-canonical-domain-decoupling | Remoção resíduos aba/abas: \`_cache_abas\`, \`get_abas()\`, \`update_abas()\` — arquivos: \`ui_data.py\`, \`filters_panel.py\`, \`main_window.py\` |" >> "$INVENTORY"
log_ok "patch_37 registrado em $INVENTORY"

# Inventário de testes
TEST_INVENTORY=""
for candidate in "$TESTS_DIR/README.md" "$ATT_DIR/TEST_INVENTORY.md"; do
    [[ -f "$candidate" ]] && { TEST_INVENTORY="$candidate"; break; }
done

if [[ -n "$TEST_INVENTORY" ]]; then
    grep -q "test_patch37" "$TEST_INVENTORY" 2>/dev/null \
        && log_warn "test_patch37 já no inventário de testes." \
        || { echo "| test_patch37_residuals.py | patch_37 | Remoção resíduos aba/abas | AST + funcional + não-regressão |" >> "$TEST_INVENTORY"
             log_ok "Teste registrado em $TEST_INVENTORY"; }
else
    log_info "Inventário de testes não encontrado — pulando."
fi

echo ""
echo "============================================="
log_ok "Inventário atualizado: $INVENTORY"
echo "============================================="
echo ""
echo "Proximos passos:"
echo "  1. Revisar: $INVENTORY"
echo "  2. python -m pytest $TESTS_DIR/test_patch37_residuals.py -v"
echo ""
