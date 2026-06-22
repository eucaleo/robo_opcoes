#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Diagnostico da Fase 1 - Revisao funcional pos uso real"

mkdir -p docs/evidencias

OUT="docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_DIAGNOSTICO_BRUTO.txt"

{
  echo "REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_DIAGNOSTICO_BRUTO"
  echo
  echo "Data:"
  date '+%Y-%m-%d %H:%M:%S'
  echo
  echo "Branch:"
  git branch --show-current
  echo
  echo "Commit base:"
  git log --oneline -1
  echo
  echo "Status Git:"
  git status --short
  echo
  echo "Arquivos principais do projeto:"
  find . \
    -path './.git' -prune -o \
    -path './__pycache__' -prune -o \
    -path './.pytest_cache' -prune -o \
    -type f \
    | sed 's#^\./##' \
    | sort \
    | head -300

  echo
  echo "Busca por validadores numericos:"
  grep -RInE "strike|preco|price|premium|valor|quantidade|numeric|decimal|float|Decimal|replace|comma|virgula" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    --include='*.md' \
    . 2>/dev/null || true

  echo
  echo "Busca por cadastro de estrutura e legs:"
  grep -RInE "structure|estrutura|leg|legs|manual|salvar|save|apply|aplicar|option_symbol|simbolo" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    . 2>/dev/null || true

  echo
  echo "Busca por payoff:"
  grep -RInE "payoff|payoff_curve_points|curve|curva|break even|breakeven|equilibrio" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    . 2>/dev/null || true

  echo
  echo "Busca por decisoes:"
  grep -RInE "decision|decisao|decisão|decisoes|decisões|structure_decisions|canonical|mode" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    . 2>/dev/null || true

  echo
  echo "Busca por atualizar dados e pipeline:"
  grep -RInE "atualizar dados|Atualizar Dados|update data|pipeline|refresh|processadas|ignoradas|processed|ignored" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    . 2>/dev/null || true

  echo
  echo "Busca por RTD:"
  grep -RInE "RTD|rtd|rtd_option_quotes|option_quotes|quotes|cotacao|cotação|ticker" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    . 2>/dev/null || true

  echo
  echo "Busca por recalculo, snapshot e metricas:"
  grep -RInE "recalculo|recálculo|recalculate|snapshot|metric|metrica|métrica|financeira|financial|updated_at|created_at" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    . 2>/dev/null || true

  echo
  echo "Busca por duplicidade, alias e aba:"
  grep -RInE "duplic|alias|aba|tab|tabs|canonical|snapshot|structure_id|estrutura numero|estrutura número" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    --include='*.md' \
    . 2>/dev/null || true

  echo
  echo "Busca por mensagens em ingles visiveis:"
  grep -RInE "must be|success|error|failed|invalid|required|not found|updated|saved|numeric|snapshot did not change|unnecessary" \
    --include='*.py' \
    --include='*.js' \
    --include='*.ts' \
    --include='*.tsx' \
    --include='*.html' \
    . 2>/dev/null || true

  echo
  echo "Arquivos de banco encontrados:"
  find . \
    -path './.git' -prune -o \
    -type f \( \
      -name '*.db' -o \
      -name '*.sqlite' -o \
      -name '*.sqlite3' -o \
      -name '*.sql' \
    \) \
    -print 2>/dev/null || true

  echo
  echo "Testes existentes:"
  find . \
    -path './.git' -prune -o \
    -type f \( \
      -name 'test_*.py' -o \
      -name '*_test.py' \
    \) \
    -print 2>/dev/null || true

} > "${OUT}"

echo "[OK] Diagnostico salvo em ${OUT}"
