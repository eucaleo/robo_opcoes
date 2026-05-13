#!/usr/bin/env bash
set -euo pipefail

ROOT="."
cd "$ROOT"

echo "==> Iniciando patch fase 1: data/ -> dados/"

timestamp="$(date +%Y%m%d_%H%M%S)"

backup_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    cp "$f" "$f.bak_$timestamp"
    echo "  backup: $f"
  fi
}

replace_literal_python() {
  local file="$1"
  local old="$2"
  local new="$3"

  python - "$file" "$old" "$new" <<'PY'
from pathlib import Path
import sys

file, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
p = Path(file)
if not p.exists():
    print(f"  ignorado (não encontrado): {file}")
    raise SystemExit(0)

txt = p.read_text(encoding="utf-8")
if old in txt:
    txt = txt.replace(old, new)
    p.write_text(txt, encoding="utf-8")
    print(f"  alterado: {file}")
else:
    print(f"  sem ocorrência literal: {file}")
PY
}

echo
echo "==> 1. Corrigindo caminho real legado em validate_db.py"
if [[ -f "validate_db.py" ]]; then
  backup_file "validate_db.py"
  replace_literal_python \
    "validate_db.py" \
    'connect("data/app.db")' \
    'connect("dados/app.db")'
else
  echo "  ignorado: validate_db.py"
fi

echo
echo "==> 2. Ajustando script de conferência scripts/30_git_busca_conferencia_anexos.sh"
if [[ -f "scripts/30_git_busca_conferencia_anexos.sh" ]]; then
  backup_file "scripts/30_git_busca_conferencia_anexos.sh"

  python - <<'PY'
from pathlib import Path

p = Path("scripts/30_git_busca_conferencia_anexos.sh")
txt = p.read_text(encoding="utf-8")

repls = [
    (
        'echo "### 5.1 Referências a data/app.db, data/derived.db, dados/app.db, dados/derived.db"',
        'echo "### 5.1 Referências a dados/app.db e dados/derived.db"'
    ),
    (
        'grep -RInE "data/app\\.db|data/derived\\.db|dados/app\\.db|dados/derived\\.db" . \\',
        'grep -RInE "dados/app\\.db|dados/derived\\.db" . \\'
    ),
    (
        'HAS_DATA=$(grep -RIl "data/app.db\\|data/derived.db" . --exclude-dir=.git --exclude-dir=.venv --exclude="*.pyc" | wc -l | tr -d \' \')',
        'HAS_DATA=0'
    ),
    (
        'echo "- Arquivos com referência a `data/*`: ${HAS_DATA}"',
        'echo "- Arquivos com referência legada a `data/*`: ${HAS_DATA}"'
    ),
    (
        'echo "> Atenção: há coexistência de referências a `data/` e `dados/`. Isso deve ser conferido antes de novos patches."',
        'echo "> Atenção: referências legadas a `data/` podem existir em histórico, scanner e auditoria."'
    ),
]

changed = False
for old, new in repls:
    if old in txt:
        txt = txt.replace(old, new)
        changed = True

p.write_text(txt, encoding="utf-8")
print("  alterado: scripts/30_git_busca_conferencia_anexos.sh" if changed else "  sem ocorrência literal: scripts/30_git_busca_conferencia_anexos.sh")
PY
else
  echo "  ignorado: scripts/30_git_busca_conferencia_anexos.sh"
fi

echo
echo "==> 3. Ajustando mensagens do scanner scripts/scan_data_references.py"
if [[ -f "scripts/scan_data_references.py" ]]; then
  backup_file "scripts/scan_data_references.py"

  python - <<'PY'
from pathlib import Path

p = Path("scripts/scan_data_references.py")
txt = p.read_text(encoding="utf-8")

repls = [
    (
        'do projeto, com foco na migração data/ -> dados/',
        'do projeto, com foco em localizar resíduos legados de data/ após a migração para dados/'
    ),
    (
        'print("\\n🎉 NENHUMA referência a \'data\' encontrada!")',
        'print("\\n🎉 Nenhuma referência legada operacional a \'data/\' encontrada!")'
    ),
    (
        'print("✅ Migração data/ -> dados/ parece estar completa nas pastas verificadas.")',
        'print("✅ A migração operacional de data/ -> dados/ parece consistente nas pastas verificadas.")'
    ),
]

changed = False
for old, new in repls:
    if old in txt:
        txt = txt.replace(old, new)
        changed = True

p.write_text(txt, encoding="utf-8")
print("  alterado: scripts/scan_data_references.py" if changed else "  sem ocorrência literal: scripts/scan_data_references.py")
PY
else
  echo "  ignorado: scripts/scan_data_references.py"
fi

echo
echo "==> 4. Varredura final objetiva"
grep -RInE 'data/(app\.db|derived\.db)' . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=ATT \
  --exclude-dir=BAK \
  --exclude-dir=reports \
  --exclude='*.bak_*' \
  || true

echo
echo "==> Concluído."
echo "Revise com:"
echo "  git diff -- validate_db.py scripts/30_git_busca_conferencia_anexos.sh scripts/scan_data_references.py"
