#!/usr/bin/env bash
# =============================================================================
# patch_37_apply.sh  (v4 — caminho absoluto Python 3.13 Windows)
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

# ---------------------------------------------------------------------------
# Python: caminho absoluto — ignora aliases da Microsoft Store
# ---------------------------------------------------------------------------
PY="/c/Users/eucal/AppData/Local/Programs/Python/Python313/python.exe"

if [[ ! -f "$PY" ]]; then
    log_err "Python nao encontrado em: $PY"
    log_err "Ajuste a variavel PY no topo do script."
    exit 1
fi

PY_VER=$("$PY" -c "import sys; print(sys.version.split()[0])" 2>/dev/null)
log_ok "Python: $PY ($PY_VER)"

# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

UI_DATA="$PROJECT_ROOT/UI/models/ui_data.py"
FILTERS="$PROJECT_ROOT/UI/components/filters_panel.py"
MAIN_WIN="$PROJECT_ROOT/UI/main_window.py"

echo ""
echo "============================================="
echo "  patch_37 - remocao de residuos aba/abas"
echo "============================================="
echo "  Raiz do projeto : $PROJECT_ROOT"
echo "  Python          : $PY_VER"
echo "  Data/hora       : $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="
echo ""

# ---------------------------------------------------------------------------
# Verifica arquivos
# ---------------------------------------------------------------------------
for f in "$UI_DATA" "$FILTERS" "$MAIN_WIN"; do
    if [[ ! -f "$f" ]]; then
        log_err "Arquivo nao encontrado: $f"
        exit 1
    fi
done
log_ok "Todos os arquivos-alvo encontrados."
echo ""

# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------
TS="$(date '+%Y%m%d_%H%M%S')"
for f in "$UI_DATA" "$FILTERS" "$MAIN_WIN"; do
    cp "$f" "${f}.bak_${TS}"
done
log_ok "Backups criados com sufixo .bak_${TS}"
echo ""

# ---------------------------------------------------------------------------
# Scripts Python em arquivos temporarios
# ---------------------------------------------------------------------------
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

# ---- Script 1: ui_data.py --------------------------------------------------
cat > "$TMP_DIR/fix_ui_data.py" << 'PYEOF'
import sys, re

path = sys.argv[1]
src  = open(path, encoding="utf-8").read()

# Remove: bloco de comentario + @property _cache_abas + @_cache_abas.setter
pattern_prop = re.compile(
    r"[ \t]*# -{10,}\n"
    r"[ \t]*#.*[Cc]ompat.*\n"
    r"[ \t]*# -{10,}\n"
    r"[ \t]*@property\n"
    r"[ \t]*def _cache_abas.*?"
    r"(?=\n[ \t]*@|\n[ \t]*def |\nclass |\Z)",
    re.DOTALL,
)

# Remove: metodo get_abas()
pattern_get = re.compile(
    r"\n[ \t]*def get_abas\(self\).*?"
    r"(?=\n[ \t]*def |\nclass |\Z)",
    re.DOTALL,
)

new_src = pattern_prop.sub("", src)
new_src = pattern_get.sub("\n", new_src)
new_src = re.sub(r"\n{3,}", "\n\n", new_src)

if new_src == src:
    print("[WARN] ui_data.py: nenhuma alteracao detectada.")
    sys.exit(0)

open(path, "w", encoding="utf-8").write(new_src)
print("[OK]  ui_data.py: _cache_abas e get_abas() removidos.")
PYEOF

# ---- Script 2: filters_panel.py --------------------------------------------
cat > "$TMP_DIR/fix_filters.py" << 'PYEOF'
import sys, re

path = sys.argv[1]
src  = open(path, encoding="utf-8").read()

# Remove metodo update_abas() e seu corpo inteiro
pattern = re.compile(
    r"\n[ \t]*def update_abas\(self[^)]*\)[^\n]*\n"
    r"(?:[ \t]+[^\n]*\n)*",
)

new_src = pattern.sub("\n", src)
new_src = re.sub(r"\n{3,}", "\n\n", new_src)

if new_src == src:
    print("[WARN] filters_panel.py: nenhuma alteracao detectada.")
    sys.exit(0)

open(path, "w", encoding="utf-8").write(new_src)
print("[OK]  filters_panel.py: update_abas() removido.")
PYEOF

# ---- Script 3: main_window.py ----------------------------------------------
cat > "$TMP_DIR/fix_main_window.py" << 'PYEOF'
import sys, re

path = sys.argv[1]
src  = open(path, encoding="utf-8").read()

# Substituicao literal (mais segura que regex para blocos indentados)
OLD = (
    "                try:\n"
    "                    self.filters_panel.update_structures(\n"
    "                        self.data_model.get_structures()\n"
    "                    )\n"
    "                except Exception:\n"
    "                    try:\n"
    "                        self.filters_panel.update_abas(self.data_model.get_abas())\n"
    "                    except Exception:\n"
    "                        pass\n"
)

NEW = (
    "                try:\n"
    "                    self.filters_panel.update_structures(\n"
    "                        self.data_model.get_structures()\n"
    "                    )\n"
    "                except Exception:\n"
    "                    pass\n"
)

if OLD not in src:
    # Fallback: regex tolerante a espacos variaveis
    pattern = re.compile(
        r"([ \t]+)try:\n"
        r"(?:[ \t]+self\.filters_panel\.update_structures\(\n)"
        r"(?:[ \t]+self\.data_model\.get_structures\(\)\n)"
        r"(?:[ \t]+\)\n)"
        r"\1except Exception:\n"
        r"[ \t]+try:\n"
        r"[ \t]+self\.filters_panel\.update_abas\(self\.data_model\.get_abas\(\)\)\n"
        r"[ \t]+except Exception:\n"
        r"[ \t]+pass\n"
    )
    def replacer(m):
        i = m.group(1)
        return (
            f"{i}try:\n"
            f"{i}    self.filters_panel.update_structures(\n"
            f"{i}        self.data_model.get_structures()\n"
            f"{i}    )\n"
            f"{i}except Exception:\n"
            f"{i}    pass\n"
        )
    new_src = pattern.sub(replacer, src)
else:
    new_src = src.replace(OLD, NEW)

new_src = re.sub(r"\n{3,}", "\n\n", new_src)

if new_src == src:
    print("[WARN] main_window.py: nenhuma alteracao detectada.")
    sys.exit(0)

open(path, "w", encoding="utf-8").write(new_src)
print("[OK]  main_window.py: bloco fallback update_abas() removido.")
PYEOF

# ===========================================================================
# Executa os 3 scripts
# ===========================================================================
log_info "Processando: UI/models/ui_data.py"
"$PY" "$TMP_DIR/fix_ui_data.py" "$UI_DATA"
echo ""

log_info "Processando: UI/components/filters_panel.py"
"$PY" "$TMP_DIR/fix_filters.py" "$FILTERS"
echo ""

log_info "Processando: UI/main_window.py"
"$PY" "$TMP_DIR/fix_main_window.py" "$MAIN_WIN"
echo ""

# ===========================================================================
# Verificacao pos-patch
# ===========================================================================
echo "---------------------------------------------"
log_info "Verificacao pos-patch..."
echo ""

RESIDUALS=0
for f in "$UI_DATA" "$FILTERS" "$MAIN_WIN"; do
    hits=$(grep -n "update_abas\|get_abas\|_cache_abas" "$f" 2>/dev/null || true)
    if [[ -n "$hits" ]]; then
        log_warn "Residuos encontrados em: $f"
        while IFS= read -r line; do
            log_info "  $line"
        done <<< "$hits"
        RESIDUALS=1
    fi
done

if [[ $RESIDUALS -eq 0 ]]; then
    log_ok "Nenhum residuo encontrado."
fi

echo ""
echo "============================================="
if [[ $RESIDUALS -eq 0 ]]; then
    log_ok "patch_37 aplicado com sucesso!"
else
    log_warn "patch_37 aplicado com avisos — revisar itens acima."
fi
echo "============================================="
echo ""

echo "Proximos passos:"
echo "  1. $PY -m pytest UI/tests/test_patch36_main_window.py -v"
echo "  2. find . -name '*.bak_*' -delete   (apos confirmar OK)"
echo ""
