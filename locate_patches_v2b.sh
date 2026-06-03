#!/usr/bin/env bash
# locate_patches_v2b.sh — versão corrigida (sem subshell com pipe problemático)
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

banner() { echo -e "\n${CYAN}${BOLD}══════════════════════════════════════${NC}"; echo -e "${CYAN}${BOLD}  $1${NC}"; echo -e "${CYAN}${BOLD}══════════════════════════════════════${NC}"; }
ok()     { echo -e "  ${GREEN}✔ $1${NC}"; }
warn()   { echo -e "  ${YELLOW}⚠ $1${NC}"; }
err()    { echo -e "  ${RED}✘ $1${NC}"; }
info()   { echo -e "  → $1"; }

locate() {
    local file="$1" pattern="$2" label="$3"
    if [[ ! -f "$file" ]]; then err "Não encontrado: $file"; return; fi
    local results
    results=$(grep -n "$pattern" "$file" 2>/dev/null || true)
    if [[ -n "$results" ]]; then
        ok "$label"
        echo "$results" | sed 's/^/    /'
    else
        warn "$label — NÃO ENCONTRADO"
    fi
}

dump_defs() {
    local file="$1"
    if [[ ! -f "$file" ]]; then err "Não encontrado: $file"; return; fi
    echo -e "\n  ${BOLD}Todos os 'def' em $file:${NC}"
    grep -n "def " "$file" | sed 's/^/    /' || true
}

F1="repositories/structures_repository.py"
F2="UI/components/structure_editor_dialog.py"
F4="UI/components/structures_list_panel.py"

# ── P1 ────────────────────────────────────────────────────────────────────────
banner "P1 — $F1"
locate "$F1" "def replace_legs"            "def replace_legs"
locate "$F1" "if not legs"                 "guarda if not legs"
locate "$F1" "legs list must not be empty" "raise vazia"
locate "$F1" "DELETE FROM structure_legs"  "DELETE structure_legs"
locate "$F1" "INSERT INTO structure_legs"  "INSERT structure_legs"
locate "$F1" "def count_legs"              "def count_legs (novo)"
locate "$F1" "COUNT"                       "COUNT existente"
dump_defs "$F1"

# ── P2 ────────────────────────────────────────────────────────────────────────
banner "P2 — $F2"
locate "$F2" "def _cmd_save"              "def _cmd_save"
locate "$F2" "replace_legs"              "chamadas replace_legs"
locate "$F2" "legs_payload"              "legs_payload"
locate "$F2" "leg_tree\|_tv_leg\|_leg_tree\|_tree_leg" "widget treeview de legs"
locate "$F2" "get_children"              "get_children"
locate "$F2" "showwarning"               "showwarning"
locate "$F2" "def _build_legs_payload"   "def _build_legs_payload (novo)"
dump_defs "$F2"

# ── P3 ────────────────────────────────────────────────────────────────────────
banner "P3 — $F1 (list_structures)"
locate "$F1" "def list_structures"        "def list_structures"
locate "$F1" "include_archived"           "parâmetro include_archived"
locate "$F1" "n_legs"                     "n_legs já presente"
locate "$F1" "ORDER BY"                   "ORDER BY"
locate "$F1" "row_factory"                "row_factory"

# ── P4 ────────────────────────────────────────────────────────────────────────
banner "P4 — $F4"
locate "$F4" "def _populate"             "def _populate_*"
locate "$F4" "def _refresh\|def _load\|def _update\|def _render" "outros métodos de carga"
locate "$F4" "\.insert("                 "insert no treeview"
locate "$F4" "n_legs"                    "n_legs existente"
locate "$F4" "legs"                      "referências a legs"
locate "$F4" "replace_legs"             "replace_legs no list_panel"
locate "$F4" "list_structures"          "chamada list_structures"
dump_defs "$F4"

# ── SUMÁRIO ───────────────────────────────────────────────────────────────────
banner "SUMÁRIO"
for f in "$F1" "$F2" "$F4"; do
    if [[ -f "$f" ]]; then
        lines=$(wc -l < "$f")
        ok "$f  →  $lines linhas"
    else
        err "$f — NÃO ENCONTRADO"
    fi
done

echo -e "\n${GREEN}${BOLD}Localização v2b concluída.${NC}\n"
