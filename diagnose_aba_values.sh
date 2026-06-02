#!/usr/bin/env bash
# =============================================================================
# diagnose_aba_values.sh
# Revela os valores EXATOS (com hex dump) das colunas 'aba' nas 3 tabelas
# =============================================================================

APP_DB="${APP_DB:-./dados/app.db}"
DERIVED_DB="${DERIVED_DB:-./dados/derived.db}"

sq() { sqlite3 -separator '|' "$1" "$2" 2>/dev/null; }

echo ""
echo "════════════════════════════════════════════════════════"
echo " VALORES EXATOS DA COLUNA 'aba' EM CADA TABELA"
echo "════════════════════════════════════════════════════════"

echo ""
echo "── rtd_analise_robo_legs (legado RTD) ──"
sq "$APP_DB" "
  SELECT DISTINCT aba,
         LENGTH(aba) AS len,
         HEX(aba)    AS hex_val,
         ativo
  FROM rtd_analise_robo_legs
  ORDER BY aba;
" | while IFS='|' read -r aba len hex ativo; do
    printf "  aba=%-20s len=%-3s ativo_exemplo=%s\n" "'$aba'" "$len" "$ativo"
    printf "  hex: %s\n\n" "$hex"
done

echo ""
echo "── manual_analise_robo_legs (legado manual) ──"
sq "$APP_DB" "
  SELECT DISTINCT aba,
         LENGTH(aba) AS len,
         HEX(aba)    AS hex_val,
         ativo
  FROM manual_analise_robo_legs
  ORDER BY aba;
" | while IFS='|' read -r aba len hex ativo; do
    printf "  aba=%-20s len=%-3s ativo_exemplo=%s\n" "'$aba'" "$len" "$ativo"
    printf "  hex: %s\n\n" "$hex"
done

echo ""
echo "── structure_decisions (derived.db) ──"
sq "$DERIVED_DB" "
  SELECT DISTINCT aba,
         LENGTH(aba) AS len,
         HEX(aba)    AS hex_val
  FROM structure_decisions
  ORDER BY aba;
" | while IFS='|' read -r aba len hex; do
    printf "  aba=%-20s len=%-3s\n" "'$aba'" "$len"
    printf "  hex: %s\n\n" "$hex"
done

echo ""
echo "── payoff_curve_points (derived.db) ──"
sq "$DERIVED_DB" "
  SELECT DISTINCT aba,
         LENGTH(aba) AS len,
         HEX(aba)    AS hex_val
  FROM payoff_curve_points
  ORDER BY aba;
" | while IFS='|' read -r aba len hex; do
    printf "  aba=%-20s len=%-3s\n" "'$aba'" "$len"
    printf "  hex: %s\n\n" "$hex"
done

echo ""
echo "── structures.alias_legacy_aba (app.db — canônico) ──"
sq "$APP_DB" "
  SELECT DISTINCT id, name, alias_legacy_aba,
         LENGTH(alias_legacy_aba) AS len,
         HEX(alias_legacy_aba)    AS hex_val,
         status
  FROM structures
  ORDER BY id;
" | while IFS='|' read -r id name alias len hex status; do
    printf "  [%s] %-35s alias=%-15s len=%-3s %s\n" \
        "$id" "$name" "'$alias'" "$len" "$status"
done

echo ""
echo "════════════════════════════════════════════════════════"
echo " DIAGNÓSTICO DE DUPLICATAS EM structures"
echo "════════════════════════════════════════════════════════"
sq "$APP_DB" "
  SELECT underlying_asset,
         alias_legacy_aba,
         status,
         COUNT(*) AS total,
         MIN(id)  AS id_min,
         MAX(id)  AS id_max
  FROM structures
  GROUP BY underlying_asset, alias_legacy_aba, status
  ORDER BY underlying_asset, status;
" | while IFS='|' read -r und alias status total id_min id_max; do
    printf "  %-10s alias=%-12s status=%-10s count=%-3s ids=%s..%s\n" \
        "$und" "'$alias'" "$status" "$total" "$id_min" "$id_max"
done

echo ""
echo "════════════════════════════════════════════════════════"
echo " OUTRAS ESTRUTURAS PRESENTES NAS TABELAS LEGADAS"
echo " (não cobertas pelos IDs 1-5 de structures)"
echo "════════════════════════════════════════════════════════"
echo "  Ativos distintos em rtd_analise_robo_legs:"
sq "$APP_DB" "
  SELECT DISTINCT
    aba,
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
      aba,
      'legs',''),'OVA','BOVA'),'MBJ','EMBJ'),'RIO','RIO'),'MAL','SMAL'
    ) AS ativo_inferido
  FROM rtd_analise_robo_legs
  ORDER BY aba;
" | while IFS='|' read -r aba inf; do
    printf "  aba=%-15s → ativo_inferido=%s\n" "$aba" "$inf"
done
