#!/usr/bin/env bash
# =============================================================================
# diagnose_migration.sh
# Diagnóstico pré-migração: verifica tabelas legadas, estruturas canônicas
# e pontos de convergência entre app.db e derived.db
#
# Uso:
#   chmod +x diagnose_migration.sh
#   ./diagnose_migration.sh
#
# Opcional — sobrescrever caminhos padrão:
#   APP_DB=/outro/caminho/app.db DERIVED_DB=/outro/caminho/derived.db ./diagnose_migration.sh
# =============================================================================

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO — ajuste se necessário
# ─────────────────────────────────────────────────────────────────────────────
APP_DB="${APP_DB:-./db/app.db}"
DERIVED_DB="${DERIVED_DB:-./db/derived.db}"

# Tabelas legadas candidatas (legs)
LEGACY_LEGS_TABLES=(
    "rtd_analise_robo_legs"
    "manual_analise_robo_legs"
    "legs"
    "structure_legs"
    "rtd_legs"
)

# Tabelas legadas candidatas (estruturas / abas)
LEGACY_ABA_TABLES=(
    "aba"
    "abas"
    "rtd_abas"
    "structures"
    "rtd_structures"
)

# Tabelas de consolidação em derived.db
DERIVED_CONSOL_TABLES=(
    "structure_decisions"
    "rtd_consolidacoes"
    "rtd_consolidations"
    "decisions"
    "rtd_decisions"
)

# Tabelas de payoff em derived.db
DERIVED_PAYOFF_TABLES=(
    "payoff_curve_points"
    "rtd_payoff_points"
    "rtd_payoff_curva"
    "payoff_points"
)

# ─────────────────────────────────────────────────────────────────────────────
# CORES
# ─────────────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

ok()   { echo -e "  ${GREEN}✅ $*${RESET}"; }
warn() { echo -e "  ${YELLOW}⚠️  $*${RESET}"; }
err()  { echo -e "  ${RED}❌ $*${RESET}"; }
info() { echo -e "  ${CYAN}ℹ️  $*${RESET}"; }
hdr()  { echo -e "\n${BOLD}$*${RESET}"; echo "$(printf '─%.0s' {1..70})"; }

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS sqlite3
# ─────────────────────────────────────────────────────────────────────────────
sq() {
    # sq <db_path> <sql>
    sqlite3 -separator '|' "$1" "$2" 2>/dev/null
}

table_exists() {
    # table_exists <db_path> <table_name>
    local result
    result=$(sq "$1" "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='$2';")
    [[ "$result" == "1" ]]
}

row_count() {
    # row_count <db_path> <table_name>
    sq "$1" "SELECT COUNT(*) FROM \"$2\";" 2>/dev/null || echo "ERR"
}

columns_of() {
    # columns_of <db_path> <table_name>  → lista separada por vírgulas
    sq "$1" "PRAGMA table_info(\"$2\");" \
        | awk -F'|' '{print $2}' \
        | paste -sd ',' -
}

first_match_col() {
    # first_match_col <cols_csv> <candidate1> [candidate2 ...]
    local cols="$1"; shift
    for c in "$@"; do
        if echo "$cols" | grep -qw "$c"; then
            echo "$c"
            return 0
        fi
    done
    echo ""
}

# ─────────────────────────────────────────────────────────────────────────────
# INÍCIO
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║        DIAGNÓSTICO PRÉ-MIGRAÇÃO — patch_28                          ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════════════╝${RESET}"
echo -e "  app.db     → ${CYAN}${APP_DB}${RESET}"
echo -e "  derived.db → ${CYAN}${DERIVED_DB}${RESET}"
echo -e "  Executado em: $(date '+%Y-%m-%d %H:%M:%S')"


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 1 — Verificação de existência dos arquivos
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 1 — Arquivos de banco de dados"

if [[ -f "$APP_DB" ]]; then
    size=$(du -sh "$APP_DB" | cut -f1)
    ok "app.db encontrado     (${size})"
else
    err "app.db NÃO encontrado em: ${APP_DB}"
    echo -e "  ${YELLOW}→ Defina APP_DB=/caminho/correto e re-execute.${RESET}"
    # Não aborta — continua para derived
fi

if [[ -f "$DERIVED_DB" ]]; then
    size=$(du -sh "$DERIVED_DB" | cut -f1)
    ok "derived.db encontrado (${size})"
else
    err "derived.db NÃO encontrado em: ${DERIVED_DB}"
    echo -e "  ${YELLOW}→ Defina DERIVED_DB=/caminho/correto e re-execute.${RESET}"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 2 — Todas as tabelas do app.db
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 2 — Tabelas existentes em app.db"

if [[ -f "$APP_DB" ]]; then
    ALL_APP_TABLES=$(sq "$APP_DB" \
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

    if [[ -z "$ALL_APP_TABLES" ]]; then
        warn "Nenhuma tabela encontrada em app.db"
    else
        while IFS= read -r tbl; do
            cnt=$(row_count "$APP_DB" "$tbl")
            printf "  %-40s %s linhas\n" "$tbl" "$cnt"
        done <<< "$ALL_APP_TABLES"
    fi
else
    warn "app.db ausente — bloco ignorado"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 3 — Todas as tabelas do derived.db
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 3 — Tabelas existentes em derived.db"

if [[ -f "$DERIVED_DB" ]]; then
    ALL_DERIVED_TABLES=$(sq "$DERIVED_DB" \
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

    if [[ -z "$ALL_DERIVED_TABLES" ]]; then
        warn "Nenhuma tabela encontrada em derived.db"
    else
        while IFS= read -r tbl; do
            cnt=$(row_count "$DERIVED_DB" "$tbl")
            printf "  %-40s %s linhas\n" "$tbl" "$cnt"
        done <<< "$ALL_DERIVED_TABLES"
    fi
else
    warn "derived.db ausente — bloco ignorado"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 4 — Tabelas legadas de legs no app.db
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 4 — Tabelas legadas de LEGS em app.db"

FOUND_LEGS_TABLE=""

if [[ -f "$APP_DB" ]]; then
    for tbl in "${LEGACY_LEGS_TABLES[@]}"; do
        if table_exists "$APP_DB" "$tbl"; then
            cnt=$(row_count "$APP_DB" "$tbl")
            cols=$(columns_of "$APP_DB" "$tbl")
            ok "Encontrada: ${tbl}  (${cnt} linhas)"
            info "Colunas: ${cols}"

            # Detecta coluna de aba/estrutura
            aba_col=$(first_match_col "$cols" aba sheet tab structure_id estrutura)
            if [[ -n "$aba_col" ]]; then
                info "→ Coluna de estrutura/aba detectada: '${aba_col}'"

                # Lista abas distintas
                echo -e "  ${CYAN}  Abas/estruturas distintas (top 30):${RESET}"
                sq "$APP_DB" \
                    "SELECT DISTINCT \"${aba_col}\", COUNT(*) as n
                     FROM \"${tbl}\"
                     GROUP BY \"${aba_col}\"
                     ORDER BY \"${aba_col}\"
                     LIMIT 30;" \
                    | while IFS='|' read -r aba_val cnt_legs; do
                        printf "    %-35s %s legs\n" "$aba_val" "$cnt_legs"
                    done
            else
                warn "→ Coluna aba/estrutura NÃO detectada automaticamente"
                info "→ Colunas disponíveis: ${cols}"
            fi

            # Detecta coluna de underlying_asset
            und_col=$(first_match_col "$cols" \
                underlying_asset underlying ticker ativo asset symbol)
            if [[ -n "$und_col" ]]; then
                info "→ Coluna de ativo detectada: '${und_col}'"
                echo -e "  ${CYAN}  Ativos distintos (top 20):${RESET}"
                sq "$APP_DB" \
                    "SELECT DISTINCT \"${und_col}\" FROM \"${tbl}\" ORDER BY 1 LIMIT 20;" \
                    | while IFS= read -r v; do printf "    %s\n" "$v"; done
            else
                warn "→ Coluna underlying_asset NÃO detectada automaticamente"
            fi

            [[ -z "$FOUND_LEGS_TABLE" ]] && FOUND_LEGS_TABLE="$tbl"
            echo ""
        else
            err "Não existe: ${tbl}"
        fi
    done

    if [[ -z "$FOUND_LEGS_TABLE" ]]; then
        warn "Nenhuma tabela legada de legs encontrada entre as candidatas"
    fi
else
    warn "app.db ausente — bloco ignorado"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 5 — Tabela canônica structures no app.db
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 5 — Tabela canônica STRUCTURES em app.db"

if [[ -f "$APP_DB" ]]; then
    if table_exists "$APP_DB" "structures"; then
        cnt=$(row_count "$APP_DB" "structures")
        cols=$(columns_of "$APP_DB" "structures")
        ok "structures existe (${cnt} linhas)"
        info "Colunas: ${cols}"

        if [[ "$cnt" -gt 0 ]]; then
            echo -e "  ${CYAN}  Registros existentes (top 20):${RESET}"
            sq "$APP_DB" \
                "SELECT id, name, underlying_asset,
                        COALESCE(alias_legacy_aba,'—') AS alias,
                        status
                 FROM structures
                 ORDER BY id
                 LIMIT 20;" \
                | while IFS='|' read -r id name und alias status; do
                    printf "    [%s] %-30s %-10s alias=%-15s %s\n" \
                        "$id" "$name" "$und" "$alias" "$status"
                done
        else
            warn "Tabela structures está VAZIA — migração ainda não realizada"
        fi

        # Verifica structure_legs
        if table_exists "$APP_DB" "structure_legs"; then
            leg_cnt=$(row_count "$APP_DB" "structure_legs")
            leg_cols=$(columns_of "$APP_DB" "structure_legs")
            ok "structure_legs existe (${leg_cnt} linhas)"
            info "Colunas: ${leg_cols}"
        else
            err "structure_legs NÃO existe — schema canônico incompleto"
        fi

    else
        err "Tabela 'structures' NÃO existe em app.db"
        warn "→ Execute o script de criação do schema canônico primeiro"
    fi
else
    warn "app.db ausente — bloco ignorado"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 6 — Tabelas de consolidação em derived.db
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 6 — Tabela de CONSOLIDAÇÕES em derived.db"

FOUND_CONSOL_TABLE=""

if [[ -f "$DERIVED_DB" ]]; then
    for tbl in "${DERIVED_CONSOL_TABLES[@]}"; do
        if table_exists "$DERIVED_DB" "$tbl"; then
            cnt=$(row_count "$DERIVED_DB" "$tbl")
            cols=$(columns_of "$DERIVED_DB" "$tbl")
            ok "Encontrada: ${tbl}  (${cnt} linhas)"
            info "Colunas: ${cols}"

            aba_col=$(first_match_col "$cols" aba sheet tab structure_id)
            if [[ -n "$aba_col" ]]; then
                info "→ Coluna de estrutura detectada: '${aba_col}'"
                echo -e "  ${CYAN}  Estruturas distintas no derived.db (top 30):${RESET}"
                sq "$DERIVED_DB" \
                    "SELECT DISTINCT \"${aba_col}\" AS aba, COUNT(*) AS n
                     FROM \"${tbl}\"
                     GROUP BY \"${aba_col}\"
                     ORDER BY \"${aba_col}\"
                     LIMIT 30;" \
                    | while IFS='|' read -r aba_val n; do
                        printf "    %-35s %s registros\n" "$aba_val" "$n"
                    done

                # Timestamp mais recente
                ts_col=$(first_match_col "$cols" timestamp ts decided_at dt_ref)
                if [[ -n "$ts_col" ]]; then
                    last_ts=$(sq "$DERIVED_DB" \
                        "SELECT MAX(\"${ts_col}\") FROM \"${tbl}\";")
                    info "→ Timestamp mais recente: ${last_ts}"
                fi
            else
                warn "→ Coluna aba/estrutura NÃO detectada"
            fi

            [[ -z "$FOUND_CONSOL_TABLE" ]] && FOUND_CONSOL_TABLE="$tbl"
            break   # usa apenas a primeira encontrada
        else
            err "Não existe: ${tbl}"
        fi
    done
else
    warn "derived.db ausente — bloco ignorado"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 7 — Tabelas de payoff em derived.db
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 7 — Tabela de PAYOFF em derived.db"

if [[ -f "$DERIVED_DB" ]]; then
    for tbl in "${DERIVED_PAYOFF_TABLES[@]}"; do
        if table_exists "$DERIVED_DB" "$tbl"; then
            cnt=$(row_count "$DERIVED_DB" "$tbl")
            cols=$(columns_of "$DERIVED_DB" "$tbl")
            ok "Encontrada: ${tbl}  (${cnt} linhas)"
            info "Colunas: ${cols}"

            aba_col=$(first_match_col "$cols" aba sheet tab structure_id)
            if [[ -n "$aba_col" ]]; then
                echo -e "  ${CYAN}  Estruturas com payoff (top 20):${RESET}"
                sq "$DERIVED_DB" \
                    "SELECT DISTINCT \"${aba_col}\" AS aba, COUNT(*) AS n_pontos
                     FROM \"${tbl}\"
                     GROUP BY \"${aba_col}\"
                     ORDER BY \"${aba_col}\"
                     LIMIT 20;" \
                    | while IFS='|' read -r aba_val n; do
                        printf "    %-35s %s pontos\n" "$aba_val" "$n"
                    done
            fi
            break
        else
            err "Não existe: ${tbl}"
        fi
    done
else
    warn "derived.db ausente — bloco ignorado"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 8 — Cruzamento: abas do derived.db vs alias em structures
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 8 — CRUZAMENTO derived.db × app.db (structures)"

if [[ -f "$APP_DB" && -f "$DERIVED_DB" && -n "$FOUND_CONSOL_TABLE" ]]; then
    if table_exists "$APP_DB" "structures"; then

        aba_col_derived=$(first_match_col \
            "$(columns_of "$DERIVED_DB" "$FOUND_CONSOL_TABLE")" \
            aba sheet tab structure_id)

        if [[ -n "$aba_col_derived" ]]; then
            echo -e "  ${CYAN}Abas em derived.db COM alias mapeado em structures:${RESET}"
            sq "$DERIVED_DB" \
                "SELECT DISTINCT \"${aba_col_derived}\" FROM \"${FOUND_CONSOL_TABLE}\" ORDER BY 1;" \
                | while IFS= read -r aba_val; do
                    # Verifica se existe alias na tabela structures do app.db
                    match=$(sq "$APP_DB" \
                        "SELECT id, name FROM structures
                         WHERE alias_legacy_aba = '${aba_val}' LIMIT 1;")
                    if [[ -n "$match" ]]; then
                        sid=$(echo "$match" | cut -d'|' -f1)
                        sname=$(echo "$match" | cut -d'|' -f2)
                        printf "  ${GREEN}  ✅ %-30s → structures.id=%s (%s)${RESET}\n" \
                            "$aba_val" "$sid" "$sname"
                    else
                        printf "  ${YELLOW}  ⚠️  %-30s → SEM mapeamento em structures${RESET}\n" \
                            "$aba_val"
                    fi
                done
        else
            warn "Coluna aba não detectada em ${FOUND_CONSOL_TABLE} — cruzamento ignorado"
        fi
    else
        warn "Tabela structures ausente — cruzamento ignorado"
    fi
else
    warn "Condições insuficientes para cruzamento (derived.db, app.db ou tabela de consolidação ausentes)"
fi


# ─────────────────────────────────────────────────────────────────────────────
# BLOCO 9 — Sample de 3 linhas de cada tabela legada encontrada
# ─────────────────────────────────────────────────────────────────────────────
hdr "BLOCO 9 — SAMPLE de dados legados (3 linhas por tabela)"

if [[ -f "$APP_DB" ]]; then
    for tbl in "${LEGACY_LEGS_TABLES[@]}"; do
        if table_exists "$APP_DB" "$tbl"; then
            echo -e "  ${CYAN}Tabela: ${tbl}${RESET}"
            sq "$APP_DB" "SELECT * FROM \"${tbl}\" LIMIT 3;" \
                | while IFS= read -r line; do
                    echo "    $line"
                done
            echo ""
        fi
    done
else
    warn "app.db ausente — bloco ignorado"
fi


# ─────────────────────────────────────────────────────────────────────────────
# RESUMO FINAL
# ─────────────────────────────────────────────────────────────────────────────
hdr "RESUMO — Checklist pré-migração"

echo ""
printf "  %-55s " "app.db existe?"
[[ -f "$APP_DB" ]]             && ok "SIM" || err "NÃO"

printf "  %-55s " "derived.db existe?"
[[ -f "$DERIVED_DB" ]]         && ok "SIM" || err "NÃO"

printf "  %-55s " "Tabela 'structures' existe em app.db?"
([[ -f "$APP_DB" ]] && table_exists "$APP_DB" "structures") \
                               && ok "SIM" || err "NÃO"

printf "  %-55s " "Tabela 'structure_legs' existe em app.db?"
([[ -f "$APP_DB" ]] && table_exists "$APP_DB" "structure_legs") \
                               && ok "SIM" || err "NÃO"

printf "  %-55s " "Tabela legada de legs encontrada?"
[[ -n "$FOUND_LEGS_TABLE" ]]   && ok "$FOUND_LEGS_TABLE" || warn "NÃO ENCONTRADA"

printf "  %-55s " "Tabela de consolidações em derived.db?"
[[ -n "$FOUND_CONSOL_TABLE" ]] && ok "$FOUND_CONSOL_TABLE" || warn "NÃO ENCONTRADA"

echo ""
echo -e "${BOLD}  Próximos passos recomendados com base neste diagnóstico:${RESET}"
echo -e "  1. Revise as abas marcadas com ⚠️  no Bloco 8 → precisam de alias mapeado"
echo -e "  2. Confirme a coluna 'aba' detectada no Bloco 4 antes de rodar patch_28"
echo -e "  3. Guarde este output (./diagnose_migration.sh > resultado_diagnostico.txt)"
echo ""
echo -e "${BOLD}  Para salvar o output:${RESET}"
echo -e "  ${CYAN}./diagnose_migration.sh 2>&1 | tee resultado_diagnostico.txt${RESET}"
echo ""
