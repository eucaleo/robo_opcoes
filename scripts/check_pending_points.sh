#!/usr/bin/env bash
set -euo pipefail

# =========================
# Config
# =========================
DERIVED_DB_DEFAULT="dados/derived.db"
RAW_DB_DEFAULT="dados/raw.db"

DERIVED_DB="${DERIVED_DB:-$DERIVED_DB_DEFAULT}"
RAW_DB="${RAW_DB:-$RAW_DB_DEFAULT}"

RED=$'\033[0;31m'
GRN=$'\033[0;32m'
YEL=$'\033[0;33m'
BLU=$'\033[0;34m'
NC=$'\033[0m'

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

say() { printf "%s\n" "$*"; }
ok()  { PASS_COUNT=$((PASS_COUNT+1)); say "${GRN}[PASS]${NC} $*"; }
fail(){ FAIL_COUNT=$((FAIL_COUNT+1)); say "${RED}[FAIL]${NC} $*"; }
warn(){ WARN_COUNT=$((WARN_COUNT+1)); say "${YEL}[WARN]${NC} $*"; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { fail "Comando ausente: $1"; return 1; }
}

# sqlite3 é ideal; se não tiver, ainda fazemos checagens de paths/docs/grep
HAVE_SQLITE=0
if command -v sqlite3 >/dev/null 2>&1; then HAVE_SQLITE=1; fi

run_sql() {
  local db="$1"
  local sql="$2"
  sqlite3 -noheader -batch "$db" "$sql"
}

file_exists() {
  [[ -f "$1" ]] && ok "Arquivo existe: $1" || fail "Arquivo ausente: $1"
}

# grep portable (git bash tem)
# OBS: exclui .txt (inclui backups tipo .sh.txt) para evitar falsos positivos de referências antigas
count_grep() {
  local pattern="$1"
  local root="${2:-.}"
  grep -RInI \
    --exclude-dir=.git \
    --exclude-dir=.venv \
    --exclude-dir=node_modules \
    --exclude-dir=__pycache__ \
    --exclude="check_pending_points.sh" \
    --exclude="*.txt" \
    -- "$pattern" "$root" 2>/dev/null | wc -l
}



# =========================
# Início
# =========================
say "${BLU}==> Check de pendências (padrão dados/ + contratos + schema + timestamps + UI)${NC}"
say "Repo: $(pwd)"
say "DERIVED_DB=$DERIVED_DB"
say "RAW_DB=$RAW_DB"
say ""

# 0) sanity git
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ok "Dentro de um repositório Git"
else
  warn "Não parece estar dentro de um repo Git (algumas checagens podem ser menos úteis)"
fi

# 1) Padrão único dados/
if [[ -d "dados" ]]; then
  ok "Diretório dados/ existe"
else
  fail "Diretório dados/ não existe"
fi

# Falha se sobrou referência antiga (case-sensitive; em Windows o FS pode ser case-insensitive)
if [[ "$(count_grep "Data/" .)" -gt 0 ]]; then
  fail "Há referências a 'Data/' — padronize para 'dados/'"
fi

if [[ "$(count_grep "data/" .)" -gt 0 ]]; then
  fail "Há referências a 'data/' — padronize para 'dados/'"
fi

# Confirma que o novo padrão aparece em algum lugar (informativo)
if [[ "$(count_grep "dados/" .)" -eq 0 ]]; then
  warn "Não encontrei referências a 'dados/' (ok se você usa env vars/config externo), mas revise."
else
  ok "Projeto padronizado em 'dados/'"
fi

# 1.1) Buscar referências suspeitas a paths fora do padrão
# Ajuste se você tiver nomes/paths específicos que não quer sinalizar.
SUSPECT1=$(count_grep "dados/" .)
SUSPECT2=$(count_grep "data\\\\\\" .)   # windows-ish path "data\"
SUSPECT3=$(count_grep "derived\\.db" .) # só para ter visibilidade

if [[ "$SUSPECT1" -eq 0 ]]; then ok "Sem referências a 'dados/' no código"; else warn "Há $SUSPECT1 referências a 'dados/' (revise)"; fi
if [[ "$SUSPECT2" -eq 0 ]]; then ok "Sem referências a 'data\\' no código"; else warn "Há $SUSPECT2 referências a 'data\\' (revise)"; fi
if [[ "$SUSPECT3" -gt 0 ]]; then ok "Referências a derived.db encontradas: $SUSPECT3 (informativo)"; else warn "Nenhuma referência a derived.db encontrada (talvez centralizado por config)"; fi

# 2) Arquivos de doc pendentes
file_exists "docs/system_map.md"
file_exists "docs/baseline_v2.md"
file_exists "report_v2.md"
file_exists "ENTRADA_E_ATUALIZACAO_ESTRUTURAS.md"
file_exists "scripts/test_system_consistency.sh"

# 3) Bancos existem onde devem (dados/)
if [[ -f "$DERIVED_DB" ]]; then ok "derived DB existe em $DERIVED_DB"; else fail "derived DB não encontrado em $DERIVED_DB"; fi
if [[ -f "$RAW_DB" ]]; then ok "raw DB existe em $RAW_DB"; else warn "raw DB não encontrado em $RAW_DB (ok se não for exigido nesse estágio)"; fi

# 4) Contrato canônico payoff: payoff_curve_points(point_spot, point_pl) + view rtd_payoff_points
if [[ "$HAVE_SQLITE" -eq 1 && -f "$DERIVED_DB" ]]; then
  # 4.1 tabela existe?
  TBL=$(run_sql "$DERIVED_DB" "SELECT name FROM sqlite_master WHERE type='table' AND name='payoff_curve_points';" || true)
  if [[ "$TBL" == "payoff_curve_points" ]]; then
    ok "Tabela payoff_curve_points existe"
    # colunas
    COLS=$(run_sql "$DERIVED_DB" "PRAGMA table_info(payoff_curve_points);" | awk -F'|' '{print $2}' | tr '\n' ' ')
    echo "$COLS" | grep -q "point_spot" && ok "payoff_curve_points tem coluna point_spot" || fail "payoff_curve_points sem coluna point_spot"
    echo "$COLS" | grep -q "point_pl"   && ok "payoff_curve_points tem coluna point_pl"   || fail "payoff_curve_points sem coluna point_pl"

    # não pode ter spot/pl físicos
    echo "$COLS" | grep -qE '(^| )spot( |$)' && fail "payoff_curve_points tem coluna física 'spot' (não deve)" || ok "Sem coluna física 'spot' (ok)"
    echo "$COLS" | grep -qE '(^| )pl( |$)'   && fail "payoff_curve_points tem coluna física 'pl' (não deve)"   || ok "Sem coluna física 'pl' (ok)"
  else
    fail "Tabela payoff_curve_points não existe"
  fi

  # 4.2 view compatível existe?
  VW=$(run_sql "$DERIVED_DB" "SELECT name FROM sqlite_master WHERE type='view' AND name='rtd_payoff_points';" || true)
  if [[ "$VW" == "rtd_payoff_points" ]]; then
    ok "View rtd_payoff_points existe"
    # testa colunas spot/pl via PRAGMA table_info(view) (funciona em sqlite)
    VCOLS=$(run_sql "$DERIVED_DB" "PRAGMA table_info(rtd_payoff_points);" | awk -F'|' '{print $2}' | tr '\n' ' ')
    echo "$VCOLS" | grep -qE '(^| )spot( |$)' && ok "View expõe coluna 'spot' (compat)" || fail "View não expõe coluna 'spot'"
    echo "$VCOLS" | grep -qE '(^| )pl( |$)'   && ok "View expõe coluna 'pl' (compat)"   || fail "View não expõe coluna 'pl'"
  else
    fail "View rtd_payoff_points não existe"
  fi
else
  warn "Sem sqlite3 ou sem derived.db -> pulando checagens SQL de payoff"
fi

# 5) structure_decisions schema completo (checa colunas-chave)
if [[ "$HAVE_SQLITE" -eq 1 && -f "$DERIVED_DB" ]]; then
  SD=$(run_sql "$DERIVED_DB" "SELECT name FROM sqlite_master WHERE type='table' AND name='structure_decisions';" || true)
  if [[ "$SD" == "structure_decisions" ]]; then
    ok "Tabela structure_decisions existe"
    SDCOLS=$(run_sql "$DERIVED_DB" "PRAGMA table_info(structure_decisions);" | awk -F'|' '{print $2}' | tr '\n' ' ')
    for c in level pl_atual pl_max pl_pct_of_max dte_min why_json; do
      echo "$SDCOLS" | grep -qE "(^| )$c( |$)" && ok "structure_decisions tem coluna $c" || fail "structure_decisions sem coluna $c"
    done
  else
    fail "Tabela structure_decisions não existe"
  fi
else
  warn "Sem sqlite3 ou sem derived.db -> pulando checagem SQL de structure_decisions"
fi

# 6) Sincronismo de timestamps (checagem genérica)
# Como não temos o SQL exato aqui, fazemos:
# - lista de tabelas com colunas comuns (snapshot_ts / asof / updated_at) e compara min/max entre as principais.
if [[ "$HAVE_SQLITE" -eq 1 && -f "$DERIVED_DB" ]]; then
  # tenta descobrir colunas candidatas (heurística)
  CAND_COL=$(run_sql "$DERIVED_DB" "
    WITH cols AS (
      SELECT m.name AS tbl, p.name AS col
      FROM sqlite_master m
      JOIN pragma_table_info(m.name) p
      WHERE m.type='table'
    )
    SELECT col, COUNT(*) AS n
    FROM cols
    WHERE col IN ('snapshot_ts','asof','as_of','ts','timestamp','updated_at','created_at')
    GROUP BY col
    ORDER BY n DESC;
  " || true)

  if [[ -n "${CAND_COL// }" ]]; then
    ok "Encontradas colunas candidatas a timestamp (heurística):"
    echo "$CAND_COL" | sed 's/^/  - /'
    warn "Validação de divergência exata depende da query oficial do projeto (recomendo colar a query canônica aqui depois)"
  else
    warn "Não achei colunas padrão de timestamp (snapshot_ts/asof/updated_at...). Se existe outra convenção, ajuste o script."
  fi
else
  warn "Sem sqlite3 ou sem derived.db -> pulando checagem de timestamps"
fi

# 7) UI entrypoint (smoke import)
# Não executa a UI (sem X), mas tenta importar o módulo.
if [[ -f "UI/main_window.py" || -f "UI/__init__.py" ]]; then
  if command -v python >/dev/null 2>&1; then
    if python -c "import UI.main_window" >/dev/null 2>&1; then
      ok "Import UI.main_window OK"
    else
      warn "Falha ao importar UI.main_window (pode ser dependência/ambiente; vale rodar localmente)"
    fi
  else
    warn "python não encontrado -> pulando smoke import da UI"
  fi
else
  warn "Pasta UI/ não encontrada como esperado -> ajuste conforme sua estrutura"
fi

# 8) Scripts de análise v2 (se existirem)
for f in scripts/analyze_code_imports_v2.py scripts/analyze_pipeline_entrypoints_v2.py scripts/analyze_sql_usage_v2.py; do
  if [[ -f "$f" ]]; then ok "Script existe: $f"; else warn "Script ausente (pendente v2): $f"; fi
done

# 9) Final summary
say ""
say "${BLU}==> RESUMO${NC}"
say "PASS: $PASS_COUNT"
say "WARN: $WARN_COUNT"
say "FAIL: $FAIL_COUNT"
say ""

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  say "${RED}Há falhas. O que está marcado como FAIL é o que falta/está divergente.${NC}"
  exit 2
else
  say "${GRN}Sem FAIL. (WARN ainda pode indicar pendências de doc/heurísticas)${NC}"
  exit 0
fi
