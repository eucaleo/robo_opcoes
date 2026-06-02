#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
log_ok()   { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_err()  { echo -e "${RED}[ERR]${NC}   $1"; }
log_info() { echo -e "        $1"; }

PY="/c/Users/eucal/AppData/Local/Programs/Python/Python313/python.exe"
PROJECT_ROOT="/c/users/eucal/projeto"
UI_DATA="$PROJECT_ROOT/UI/models/ui_data.py"
TESTS_DIR="$PROJECT_ROOT/ATT/tests"

if [[ ! -f "$UI_DATA" ]]; then log_err "Não encontrado: $UI_DATA"; exit 1; fi

echo ""
echo "============================================="
echo "  patch_38 - polish pós-patch_37"
echo "============================================="
echo "  Arquivo  : $UI_DATA"
echo "  Data/hora: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================="
echo ""

TS="$(date '+%Y%m%d_%H%M%S')"
cp "$UI_DATA" "${UI_DATA}.bak_p38_${TS}"
log_ok "Backup: ui_data.py.bak_p38_${TS}"
echo ""

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/patch38.py" << 'PYEOF'
import sys, re

path = sys.argv[1]
src  = open(path, encoding="utf-8").read()
original = src
changes = []

# Fix 1: get_structures() lazy-load
OLD_GS = (
    "    def get_structures(self) -> List[str]:\n"
    "        return self._cache_structures\n"
)
NEW_GS = (
    "    def get_structures(self) -> List[str]:\n"
    "        \"\"\"Alias de get_structure_ids() para compatibilidade.\"\"\"\n"
    "        if not self._cache_structures:\n"
    "            self._cache_structures = self._load_structures()\n"
    "        return list(self._cache_structures)\n"
)
if OLD_GS in src:
    src = src.replace(OLD_GS, NEW_GS)
    changes.append("get_structures(): lazy-load adicionado")
else:
    pat = re.compile(
        r"(    def get_structures\(self\) -> List\[str\]:)\n"
        r"(        return self\._cache_structures\n)"
    )
    new_src, n = pat.subn(
        "    def get_structures(self) -> List[str]:\n"
        '        """Alias de get_structure_ids() para compatibilidade."""\n'
        "        if not self._cache_structures:\n"
        "            self._cache_structures = self._load_structures()\n"
        "        return list(self._cache_structures)\n",
        src
    )
    if n > 0:
        src = new_src
        changes.append("get_structures(): lazy-load adicionado (regex)")
    else:
        print("[WARN] get_structures(): padrao nao encontrado.")

# Fix 2: comentário cortado
OLD_C = "                    # aba espelha para compat de leitura; nunca mais usado como chave de\n"
NEW_C = "                    # aba espelha structure_id para compat de leitura (patch_3a)\n"
if OLD_C in src:
    src = src.replace(OLD_C, NEW_C)
    changes.append("Comentario cortado corrigido")
else:
    pat_c = re.compile(r"([ \t]+# aba espelha para compat de leitura; nunca mais usado como chave de\n)")
    new_src, n = pat_c.subn(
        lambda m: m.group(1).replace(
            "aba espelha para compat de leitura; nunca mais usado como chave de",
            "aba espelha structure_id para compat de leitura (patch_3a)"
        ), src
    )
    if n > 0:
        src = new_src
        changes.append("Comentario corrigido (regex)")
    else:
        print("[INFO] Comentario: padrao nao encontrado.")

src = re.sub(r"\n{3,}", "\n\n", src)

if src == original:
    print("[WARN] Nenhuma alteracao realizada.")
    sys.exit(0)

open(path, "w", encoding="utf-8").write(src)
print("[OK]  patch_38 aplicado:")
for c in changes:
    print(f"       - {c}")
PYEOF

log_info "Aplicando patch_38..."
"$PY" "$TMP_DIR/patch38.py" "$UI_DATA"
echo ""

echo "---------------------------------------------"
log_info "Verificacao pos-patch_38..."
echo ""

WARNS=0
grep -A5 "def get_structures" "$UI_DATA" | grep -q "_load_structures" \
    && log_ok "get_structures(): lazy-load confirmado" \
    || { log_warn "get_structures(): lazy-load NAO encontrado"; WARNS=$((WARNS+1)); }

grep -q "aba espelha structure_id para compat" "$UI_DATA" \
    && log_ok "Comentario: corrigido" \
    || log_info "Comentario: nao encontrado (pode ja estar correto)"

for term in "_cache_abas" "get_abas" "update_abas"; do
    grep -q "$term" "$UI_DATA" 2>/dev/null \
        && { log_warn "Residuo ainda presente: $term"; WARNS=$((WARNS+1)); } \
        || true
done

[[ $WARNS -eq 0 ]] && log_ok "Nenhum residuo encontrado"

echo ""
echo "============================================="
[[ $WARNS -eq 0 ]] && log_ok "patch_38 concluido com sucesso." \
                   || log_warn "patch_38 concluido com $WARNS aviso(s)."
echo "============================================="
echo ""
echo "Proximos passos:"
echo "  1. $PY -m pytest $TESTS_DIR/test_patch37_residuals.py -v"
echo "  2. bash /c/users/eucal/Projeto/ATT/patches/patch_37_update_inventory.sh"
echo ""
