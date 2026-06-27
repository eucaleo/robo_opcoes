#!/usr/bin/env bash
set -u

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR" || exit 1

OUT_DIR="reports/payoff_runtime_focado"
mkdir -p "$OUT_DIR"

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_FILE="$OUT_DIR/runtime_focado_payoff_${STAMP}.txt"

echo "Conferencia Runtime Focada - Payoff por estrutura individual" > "$OUT_FILE"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUT_FILE"
echo "Branch: $(git branch --show-current 2>/dev/null)" >> "$OUT_FILE"
echo "Commit: $(git rev-parse --short HEAD 2>/dev/null)" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

run_grep() {
    local title="$1"
    local pattern="$2"

    echo "============================================================" >> "$OUT_FILE"
    echo "$title" >> "$OUT_FILE"
    echo "Pattern: $pattern" >> "$OUT_FILE"
    echo "============================================================" >> "$OUT_FILE"

    git grep -n -I -E "$pattern" -- . \
      ':(exclude)docs/**' \
      ':(exclude)reports/**' \
      ':(exclude).git/**' \
      ':(exclude)docs/evidencias/**' \
      ':(exclude)docs/checkpoints/evidencias/**' \
      >> "$OUT_FILE" 2>/dev/null || true

    echo "" >> "$OUT_FILE"
}

run_file_context() {
    local title="$1"
    local file="$2"
    local start="$3"
    local end="$4"

    echo "============================================================" >> "$OUT_FILE"
    echo "$title" >> "$OUT_FILE"
    echo "Arquivo: $file Linhas: $start-$end" >> "$OUT_FILE"
    echo "============================================================" >> "$OUT_FILE"

    if [ -f "$file" ]; then
        sed -n "${start},${end}p" "$file" >> "$OUT_FILE" 2>/dev/null || true
    else
        echo "Arquivo nao encontrado." >> "$OUT_FILE"
    fi

    echo "" >> "$OUT_FILE"
}

run_grep "1. Labels de Preco ref em runtime" \
"Preço ref|Preco ref|preco ref|spot_ref_label|_last_pl_at_spot_ref|pl_at_spot_ref"

run_grep "2. Valor 66.84 ou fallback estatico em runtime" \
"66[,.]84|DEFAULT_MARKET_BY_ASSET|static_fallback|is_static_fallback|allow_static_fallback|market_snapshot_source"

run_grep "3. Possivel uso de ativo-base como chave principal" \
"WHERE.*underlying|where.*underlying|filter.*underlying|query.*underlying|GROUP BY.*underlying|group by.*underlying|ativo_base|underlying_asset"

run_grep "4. Consultas obrigatorias por structure_id" \
"structure_id|structureId|WHERE.*structure_id|where.*structure_id|read_by_structure_id|get_legs_by_structure_id|list_snapshots_for_structure"

run_grep "5. Motor payoff / pricing / persistencia" \
"payoff|PayoffPricingEngine|calculate_payoff|spot_price|spot_ref|current.?PL|intr[ií]nseco|extr[ií]nseco|expiration"

run_grep "6. UI payoff e details panel" \
"Payoff no vencimento|PL atual|Preço base|Preço usado|Resultado simulado|curva|break.?even|breakeven|chart|grafico|gráfico"

run_file_context "Contexto UI details_panel Preco ref" \
"UI/components/details_panel.py" 520 710

run_file_context "Contexto UI payoff_chart Preco ref" \
"UI/components/payoff_chart.py" 360 420

run_file_context "Contexto market_snapshot_provider" \
"services/market_snapshot_provider.py" 1 230

run_file_context "Contexto payoff domain" \
"domain/payoff.py" 120 190

run_file_context "Contexto payoff_pricing_engine" \
"services/payoff_pricing_engine.py" 1 150

echo "Relatorio gerado em: $OUT_FILE"
