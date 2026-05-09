#!/bin/bash
set -euo pipefail

# Descobre a raiz do repositório a partir de ATT/patches
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

mkdir -p scripts docs

# Verificação do report necessário
if [ ! -f "ATT/reports/sql_report_v3.json" ]; then
  echo "[ERRO] Não encontrado: ATT/reports/sql_report_v3.json"
  echo "       Rode antes o patch_01_analyze_repo.sh para gerar os relatórios."
  exit 1
fi

# Cria/atualiza o gerador
cat > scripts/gen_module_map_v2.py <<'PY'
import json
from collections import defaultdict
from pathlib import Path

SQL_REPORT = Path("ATT/reports/sql_report_v3.json")
DOC_OUT = Path("docs/MAPA_MODULOS_FUNCOES.md")

def main():
    if not SQL_REPORT.exists():
        print(f"[ERRO] Não encontrado: {SQL_REPORT}")
        raise SystemExit(1)

    with SQL_REPORT.open(encoding='utf-8') as f:
        report = json.load(f)

    # tabela -> arquivo -> [(linha, contexto)]
    mapping = defaultdict(lambda: defaultdict(list))

    # Estrutura esperada: { "arquivo": [ {"table": ..., "line": ..., "context": ..., "op": ...}, ... ] }
    for filename, entries in report.items():
        if not isinstance(entries, list):
            continue
        for item in entries:
            table = (item.get('table') or '').strip()
            if not table:
                continue
            # heurística simples anti-ruído
            if table.startswith("#") or len(table) > 64:
                continue
            line = item.get('line') or "?"
            context = (item.get('context') or '').strip()
            op = (item.get('op') or '').upper()
            if op:
                context = f"[{op}] {context}" if context else f"[{op}]"
            mapping[table][filename].append((line, context))

    with DOC_OUT.open('w', encoding='utf-8') as out:
        out.write("# Mapa de Uso de SQL — Tabela x Arquivo/Função (v2)\n\n")
        out.write("> Fonte: ATT/reports/sql_report_v3.json\n\n")
        for table in sorted(mapping):
            out.write(f"## {table}\n\n")
            for filename in sorted(mapping[table]):
                entries = mapping[table][filename]
                out.write(f"- **{filename}**\n")
                for line, context in entries:
                    ctx = f" `{context}`" if context else ""
                    out.write(f"    - linha {line}:{ctx}\n")
            out.write("\n---\n\n")
    print(f"[OK] Mapa gerado em {DOC_OUT}")

if __name__ == "__main__":
    main()
PY

# Seleciona binário do Python
PYTHON_BIN="${PYTHON_BIN:-python}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

# Executa gerador
"$PYTHON_BIN" -u scripts/gen_module_map_v2.py

# Log no executed_v2.md
if [ -f "docs/executed_v2.md" ]; then
  {
    echo ""
    echo "---"
    echo ""
    echo "### patch_03_gen_module_map.sh"
    echo "- Gera/recria docs/MAPA_MODULOS_FUNCOES.md a partir de ATT/reports/sql_report_v3.json"
  } >> docs/executed_v2.md
fi

echo "Patch 03 (GEN módulo map) aplicado com sucesso. Confira docs/MAPA_MODULOS_FUNCOES.md"
