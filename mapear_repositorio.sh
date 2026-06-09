#!/usr/bin/env bash

set -euo pipefail

# ============================================================
# Script de auditoria/mapeamento do repositório
# Objetivo:
# - Mapear pastas e arquivos existentes
# - Identificar arquivos grandes
# - Listar extensões utilizadas
# - Mapear possíveis lixos/caches/builds
# - Mapear arquivos Excel/CSV/parquet/json/db
# - Gerar relatórios para limpeza antes da refatoração
#
# Segurança:
# - Este script NÃO apaga nenhum arquivo
# ============================================================

ROOT_DIR="${1:-.}"
AUDIT_DIR="_repo_audit"
TIMESTAMP="$(date +"%Y-%m-%d_%H-%M-%S")"
OUT_DIR="${AUDIT_DIR}/audit_${TIMESTAMP}"

mkdir -p "$OUT_DIR"

echo "============================================================"
echo " Iniciando auditoria do repositório"
echo " Diretório alvo: $ROOT_DIR"
echo " Saída: $OUT_DIR"
echo "============================================================"

# ------------------------------------------------------------
# 1. Informações gerais
# ------------------------------------------------------------

{
  echo "AUDITORIA DO REPOSITÓRIO"
  echo "Data: $(date)"
  echo "Diretório analisado: $(realpath "$ROOT_DIR")"
  echo ""

  echo "Sistema:"
  uname -a || true
  echo ""

  echo "Resumo de tamanho:"
  du -sh "$ROOT_DIR" 2>/dev/null || true
  echo ""

  echo "Quantidade total de arquivos:"
  find "$ROOT_DIR" -type f \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" | wc -l
  echo ""

  echo "Quantidade total de pastas:"
  find "$ROOT_DIR" -type d \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" | wc -l
  echo ""
} > "$OUT_DIR/00_resumo_geral.txt"

# ------------------------------------------------------------
# 2. Árvore de diretórios
# ------------------------------------------------------------

if command -v tree >/dev/null 2>&1; then
  tree -a -I ".git|$AUDIT_DIR|node_modules|__pycache__|.venv|venv|dist|build" "$ROOT_DIR" \
    > "$OUT_DIR/01_arvore_resumida.txt" || true

  tree -a "$ROOT_DIR" \
    -I ".git|$AUDIT_DIR" \
    > "$OUT_DIR/02_arvore_completa_sem_git.txt" || true
else
  echo "Comando 'tree' não encontrado. Usando find." > "$OUT_DIR/01_arvore_resumida.txt"

  find "$ROOT_DIR" \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    | sort > "$OUT_DIR/02_arvore_completa_sem_git.txt"
fi

# ------------------------------------------------------------
# 3. Lista completa de arquivos
# ------------------------------------------------------------

find "$ROOT_DIR" -type f \
  -not -path "*/.git/*" \
  -not -path "*/$AUDIT_DIR/*" \
  | sort > "$OUT_DIR/03_lista_arquivos.txt"

# ------------------------------------------------------------
# 4. Lista completa de pastas
# ------------------------------------------------------------

find "$ROOT_DIR" -type d \
  -not -path "*/.git/*" \
  -not -path "*/$AUDIT_DIR/*" \
  | sort > "$OUT_DIR/04_lista_pastas.txt"

# ------------------------------------------------------------
# 5. Tamanho por pasta de primeiro nível
# ------------------------------------------------------------

{
  echo "Tamanho por item no diretório raiz:"
  echo ""

  find "$ROOT_DIR" -mindepth 1 -maxdepth 1 \
    -not -name ".git" \
    -not -name "$AUDIT_DIR" \
    -exec du -sh {} \; 2>/dev/null | sort -h
} > "$OUT_DIR/05_tamanho_por_item_raiz.txt"

# ------------------------------------------------------------
# 6. Arquivos maiores
# ------------------------------------------------------------

{
  echo "Top 100 maiores arquivos:"
  echo ""

  find "$ROOT_DIR" -type f \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    -exec du -h {} + 2>/dev/null | sort -hr | head -100
} > "$OUT_DIR/06_arquivos_maiores.txt"

# ------------------------------------------------------------
# 7. Extensões encontradas
# ------------------------------------------------------------

{
  echo "Extensões encontradas:"
  echo ""

  find "$ROOT_DIR" -type f \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    | awk '
      {
        n=$0
        sub(/^.*\//, "", n)
        if (n !~ /\./) {
          ext="[sem_extensao]"
        } else {
          ext=n
          sub(/^.*\./, ".", ext)
          ext=tolower(ext)
        }
        count[ext]++
      }
      END {
        for (e in count) print count[e], e
      }
    ' | sort -nr
} > "$OUT_DIR/07_extensoes_encontradas.txt"

# ------------------------------------------------------------
# 8. Possíveis arquivos temporários/lixo/cache/build
# ------------------------------------------------------------

{
  echo "Possíveis arquivos/pastas de cache, build, temporários ou lixo:"
  echo ""

  find "$ROOT_DIR" \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    \( \
      -name "__pycache__" -o \
      -name ".pytest_cache" -o \
      -name ".mypy_cache" -o \
      -name ".ruff_cache" -o \
      -name ".cache" -o \
      -name ".venv" -o \
      -name "venv" -o \
      -name "node_modules" -o \
      -name "dist" -o \
      -name "build" -o \
      -name ".DS_Store" -o \
      -name "Thumbs.db" -o \
      -name "*.pyc" -o \
      -name "*.pyo" -o \
      -name "*.log" -o \
      -name "*.tmp" -o \
      -name "*.bak" -o \
      -name "*.old" -o \
      -name "*~" \
    \) | sort
} > "$OUT_DIR/08_possiveis_lixos.txt"

# ------------------------------------------------------------
# 9. Arquivos de dados importantes para o projeto
# ------------------------------------------------------------

{
  echo "Arquivos de dados encontrados:"
  echo ""

  find "$ROOT_DIR" -type f \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    \( \
      -iname "*.csv" -o \
      -iname "*.xlsx" -o \
      -iname "*.xlsm" -o \
      -iname "*.xls" -o \
      -iname "*.json" -o \
      -iname "*.jsonl" -o \
      -iname "*.parquet" -o \
      -iname "*.db" -o \
      -iname "*.sqlite" -o \
      -iname "*.sqlite3" -o \
      -iname "*.duckdb" \
    \) \
    -exec du -h {} + 2>/dev/null | sort -hr
} > "$OUT_DIR/09_arquivos_dados.txt"

# ------------------------------------------------------------
# 10. Arquivos relacionados ao Excel, RTD, Bridge e rotas
# ------------------------------------------------------------

{
  echo "Arquivos possivelmente relacionados a Excel, RTD, Bridge, rotas e ingestão:"
  echo ""

  find "$ROOT_DIR" -type f \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    | grep -Ei "excel|rtd|bridge|ingest|ingestao|rota|route|snapshot|cotacao|cotacoes|option|opcoes|estrutura|perna|position|posicao|btg" \
    | sort || true
} > "$OUT_DIR/10_excel_rtd_bridge_rotas.txt"

# ------------------------------------------------------------
# 11. Arquivos Python e módulos principais
# ------------------------------------------------------------

{
  echo "Arquivos Python encontrados:"
  echo ""

  find "$ROOT_DIR" -type f \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    -iname "*.py" \
    | sort
} > "$OUT_DIR/11_arquivos_python.txt"

# ------------------------------------------------------------
# 12. Arquivos de configuração
# ------------------------------------------------------------

{
  echo "Arquivos de configuração encontrados:"
  echo ""

  find "$ROOT_DIR" -type f \
    -not -path "*/.git/*" \
    -not -path "*/$AUDIT_DIR/*" \
    \( \
      -iname "pyproject.toml" -o \
      -iname "requirements*.txt" -o \
      -iname "setup.py" -o \
      -iname "setup.cfg" -o \
      -iname "poetry.lock" -o \
      -iname "Pipfile" -o \
      -iname "Pipfile.lock" -o \
      -iname "package.json" -o \
      -iname "package-lock.json" -o \
      -iname "dockerfile" -o \
      -iname "docker-compose*.yml" -o \
      -iname "*.env" -o \
      -iname ".env*" -o \
      -iname "*.toml" -o \
      -iname "*.yaml" -o \
      -iname "*.yml" \
    \) | sort
} > "$OUT_DIR/12_arquivos_configuracao.txt"

# ------------------------------------------------------------
# 13. Possíveis duplicados por hash
# ------------------------------------------------------------

{
  echo "Possíveis arquivos duplicados por hash SHA256:"
  echo ""

  if command -v sha256sum >/dev/null 2>&1; then
    find "$ROOT_DIR" -type f \
      -not -path "*/.git/*" \
      -not -path "*/$AUDIT_DIR/*" \
      -print0 \
      | xargs -0 sha256sum 2>/dev/null \
      | sort \
      | awk '
        {
          hash=$1
          file=$0
          sub(/^[^ ]+  /, "", file)
          files[hash]=files[hash] "\n  " file
          count[hash]++
        }
        END {
          for (h in count) {
            if (count[h] > 1) {
              print "HASH:", h
              print files[h]
              print ""
            }
          }
        }
      '
  else
    echo "sha256sum não disponível neste sistema."
  fi
} > "$OUT_DIR/13_possiveis_duplicados.txt"

# ------------------------------------------------------------
# 14. Status Git, se existir
# ------------------------------------------------------------

if [ -d "$ROOT_DIR/.git" ]; then
  {
    echo "Status Git:"
    echo ""

    git -C "$ROOT_DIR" status --short || true

    echo ""
    echo "Arquivos rastreados:"
    git -C "$ROOT_DIR" ls-files || true

    echo ""
    echo "Arquivos ignorados:"
    git -C "$ROOT_DIR" status --ignored --short || true
  } > "$OUT_DIR/14_git_status.txt"
else
  echo "Este diretório não parece ser um repositório Git." > "$OUT_DIR/14_git_status.txt"
fi

# ------------------------------------------------------------
# 15. Relatório consolidado em Markdown
# ------------------------------------------------------------

REPORT="$OUT_DIR/RELATORIO_AUDITORIA.md"

{
  echo "# Relatório de Auditoria do Repositório"
  echo ""
  echo "**Data:** $(date)"
  echo ""
  echo "**Diretório analisado:** \`$(realpath "$ROOT_DIR")\`"
  echo ""
  echo "## Objetivo"
  echo ""
  echo "Mapear a estrutura atual do projeto antes da limpeza e da refatoração da rota mestre."
  echo ""
  echo "## Arquivos gerados"
  echo ""
  echo "- \`00_resumo_geral.txt\`"
  echo "- \`01_arvore_resumida.txt\`"
  echo "- \`02_arvore_completa_sem_git.txt\`"
  echo "- \`03_lista_arquivos.txt\`"
  echo "- \`04_lista_pastas.txt\`"
  echo "- \`05_tamanho_por_item_raiz.txt\`"
  echo "- \`06_arquivos_maiores.txt\`"
  echo "- \`07_extensoes_encontradas.txt\`"
  echo "- \`08_possiveis_lixos.txt\`"
  echo "- \`09_arquivos_dados.txt\`"
  echo "- \`10_excel_rtd_bridge_rotas.txt\`"
  echo "- \`11_arquivos_python.txt\`"
  echo "- \`12_arquivos_configuracao.txt\`"
  echo "- \`13_possiveis_duplicados.txt\`"
  echo "- \`14_git_status.txt\`"
  echo ""
  echo "## Próximo passo sugerido"
  echo ""
  echo "Após revisar estes relatórios, classificar os arquivos em:"
  echo ""
  echo "1. **Manter**"
  echo "2. **Remover**"
  echo "3. **Arquivar fora do projeto**"
  echo "4. **Migrar para nova estrutura**"
  echo "5. **Auditar manualmente antes de decidir**"
  echo ""
  echo "Nenhum arquivo foi apagado por este script."
} > "$REPORT"

echo ""
echo "============================================================"
echo " Auditoria concluída."
echo " Relatórios gerados em:"
echo " $OUT_DIR"
echo "============================================================"
echo ""
echo "Relatório principal:"
echo "$REPORT"
echo ""
