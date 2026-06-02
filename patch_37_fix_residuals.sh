#!/usr/bin/env bash
# =============================================================================
# patch_37_fix_residuals.sh
# Remove residuos que sobraram em ui_data.py apos patch_37
# Linhas alvo (conforme grep):
#   75:    @_cache_abas.setter
#   76:    def _cache_abas(self, value: List[str]):
#   224:   (apenas menção em docstring — não remover código, só avaliar)
# =============================================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_err()  { echo -e "${RED}[ERR]${NC}   $1"; }
log_info() { echo -e "        $1"; }

PY="/c/Users/eucal/AppData/Local/Programs/Python/Python313/python.exe"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UI_DATA="$SCRIPT_DIR/UI/models/ui_data.py"

if [[ ! -f "$UI_DATA" ]]; then
    log_err "Arquivo nao encontrado: $UI_DATA"
    exit 1
fi

# Backup antes de qualquer alteracao
TS="$(date '+%Y%m%d_%H%M%S')"
cp "$UI_DATA" "${UI_DATA}.bak_fix_${TS}"
log_ok "Backup criado: ui_data.py.bak_fix_${TS}"
echo ""

# ---------------------------------------------------------------------------
# Mostra contexto ao redor das linhas residuais (para diagnostico)
# ---------------------------------------------------------------------------
log_info "Contexto atual em ui_data.py (linhas 65-110):"
echo "---"
sed -n '65,110p' "$UI_DATA" | cat -n | sed 's/^/  /'
echo "---"
echo ""
log_info "Contexto linha 224 (linhas 218-232):"
echo "---"
sed -n '218,232p' "$UI_DATA" | cat -n | sed 's/^/  /'
echo "---"
echo ""

# ---------------------------------------------------------------------------
# Script Python para remover residuos
# ---------------------------------------------------------------------------
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/fix_residuals.py" << 'PYEOF'
import sys, re

path = sys.argv[1]
src  = open(path, encoding="utf-8").read()
original = src

changes = []

# ------------------------------------------------------------------
# Residuo 1: @_cache_abas.setter + def _cache_abas(self, value) + corpo
# Captura o setter que ficou orfao apos remocao do @property
# ------------------------------------------------------------------
pattern_setter = re.compile(
    r"\n[ \t]*@_cache_abas\.setter\n"
    r"[ \t]*def _cache_abas\(self[^)]*\)[^\n]*\n"
    r"(?:[ \t]+[^\n]*\n)*",
    re.DOTALL,
)

new_src, n = pattern_setter.subn("\n", src)
if n > 0:
    changes.append(f"@_cache_abas.setter removido ({n} ocorrencia(s))")
    src = new_src

# ------------------------------------------------------------------
# Residuo 2: linha 224 — apenas docstring mencionando get_abas()
# Verifica se e comentario/docstring (seguro manter ou limpar texto)
# ------------------------------------------------------------------
pattern_docref = re.compile(
    r'("""[^"]*?)Substitui get_abas\(\) e get_structures\(\)([^"]*?""")',
    re.DOTALL,
)
new_src, n = pattern_docref.subn(r'\1Substitui get_structures()\2', src)
if n > 0:
    changes.append(f"Referencia a get_abas() em docstring atualizada ({n} ocorrencia(s))")
    src = new_src

# Limpeza de linhas em branco multiplas
src = re.sub(r"\n{3,}", "\n\n", src)

if src == original:
    print("[WARN] Nenhuma alteracao adicional detectada.")
    print("       Verifique manualmente as linhas reportadas.")
    sys.exit(0)

open(path, "w", encoding="utf-8").write(src)
print(f"[OK]  ui_data.py corrigido. Alteracoes:")
for c in changes:
    print(f"       - {c}")
PYEOF

log_info "Aplicando correcoes..."
"$PY" "$TMP_DIR/fix_residuals.py" "$UI_DATA"
echo ""

# ---------------------------------------------------------------------------
# Verificacao final
# ---------------------------------------------------------------------------
log_info "Verificacao final em ui_data.py..."
hits=$(grep -n "update_abas\|get_abas\|_cache_abas" "$UI_DATA" 2>/dev/null || true)

if [[ -n "$hits" ]]; then
    log_warn "Ainda existem referencias:"
    while IFS= read -r line; do
        # Ignora se for apenas comentario
        if echo "$line" | grep -q "^\s*#"; then
            log_info "  (comentario — OK) $line"
        else
            log_warn "  $line"
        fi
    done <<< "$hits"
else
    log_ok "Nenhum residuo encontrado em ui_data.py."
fi

echo ""
echo "============================================="
log_ok "Correcao de residuos concluida."
echo "============================================="
echo ""
echo "Verifique o resultado completo:"
echo "  sed -n '65,110p' UI/models/ui_data.py"
