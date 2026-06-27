#!/usr/bin/env bash
set -u

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR" || exit 1

OUT_DIR="reports/payoff_conferencia"
mkdir -p "$OUT_DIR"

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_FILE="$OUT_DIR/buscas_git_payoff_${STAMP}.txt"

echo "Conferencia Git/Grep - Payoff por estrutura individual" > "$OUT_FILE"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUT_FILE"
echo "Branch: $(git branch --show-current 2>/dev/null)" >> "$OUT_FILE"
echo "Commit: $(git rev-parse --short HEAD 2>/dev/null)" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

run_section() {
    local title="$1"
    local pattern="$2"
    local pathspec="${3:-.}"

    echo "============================================================" >> "$OUT_FILE"
    echo "$title" >> "$OUT_FILE"
    echo "Pattern: $pattern" >> "$OUT_FILE"
    echo "Pathspec: $pathspec" >> "$OUT_FILE"
    echo "============================================================" >> "$OUT_FILE"

    git grep -n -I -E "$pattern" -- "$pathspec" ':!docs/**' ':!reports/**' ':!scripts/conferir_payoff_buscas_git.sh' >> "$OUT_FILE" 2>/dev/null || true
    echo "" >> "$OUT_FILE"
}

run_section "1. Termos antigos de comparacao incompatível" \
"validateComparableStructures|Não é possível comparar estruturas com ativos-base diferentes|comparação entre duas estruturas incompatíveis|Estruturas de ativos diferentes não puderem"

run_section "2. Campos e labels de preco de referencia" \
"pre[cç]o.?ref|preco_ref|reference.?price|spot_ref|spot.?ref|Preço ref"

run_section "3. Valores hardcoded suspeitos" \
"66[,.]84|198[,.]35|124[,.]66|168[,.]67|87[,.]37|37[,.]42|61[,.]80|170[,.]78|170[,.]55|53[,.]20|53[,.]2"

run_section "4. Fallback estatico e DEFAULT_MARKET_BY_ASSET" \
"DEFAULT_MARKET_BY_ASSET|static_fallback|is_static_fallback|fallback.?static|hardcoded|mock.?market|fake.?market"

run_section "5. Market snapshot, canonical e pricing" \
"MarketSnapshotProvider|CanonicalPricingFacade|PricingInputService|market_snapshot_source|snapshot_source|is_current_market|spot_price"

run_section "6. Payoff geral" \
"calculatePayoff|calculate_payoff|PayoffPricingEngine|payoff|break.?even|intr[ií]nseco|extr[ií]nseco|expiration.?payoff|current.?PL|mark.?to.?market|marcação|marcacao"

run_section "7. Consultas por structure_id" \
"structure_id|structureId|structure.id|structures.id|WHERE.*structure|where.*structure|filter.*structure|query.*structure"

run_section "8. Possivel uso indevido de underlying como chave de carga" \
"underlying_asset|underlying|ativo_base|ativo.?base|WHERE.*underlying|where.*underlying|filter.*underlying|query.*underlying|group.*underlying"

run_section "9. Pernas, snapshots e metricas" \
"structure_legs|structure_leg_snapshots|legs|pernas|snapshots|metrics|metricas|métricas|derived_payoff|payoff_persistence"

run_section "10. UI grafico payoff e labels" \
"Preço ref|Preco ref|preco ref|PL atual|Payoff no vencimento|Resultado simulado|curva|vencimento|ganho|perda|break.?even|chart|graph|grafico|gráfico" \
"ATT"

run_section "11. UI geral fora de ATT se existir" \
"Preço ref|Preco ref|preco ref|PL atual|Payoff no vencimento|Resultado simulado|curva|vencimento|ganho|perda|break.?even|chart|graph|grafico|gráfico" \
"src"

run_section "12. Testes existentes relacionados" \
"payoff|pricing|canonical|snapshot|structure_id|underlying|static_fallback|Preço ref|preco_ref" \
"tests"

run_section "13. Testes em ATT se existir" \
"payoff|pricing|canonical|snapshot|structure_id|underlying|static_fallback|Preço ref|preco_ref" \
"ATT/tests"

echo "Relatorio gerado em: $OUT_FILE"
