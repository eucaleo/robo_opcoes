#!/usr/bin/env bash
set -euo pipefail

MODE="${1:---dry-run}"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
TARGET="services/structure_leg_rtd_enrichment_service.py"

if [[ -z "${PROJECT_ROOT}" ]]; then
  echo "[ERRO] Execute este script dentro de um repositório Git."
  exit 1
fi

cd "${PROJECT_ROOT}"

if [[ ! -f "${TARGET}" ]]; then
  echo "[ERRO] Arquivo não encontrado: ${TARGET}"
  exit 1
fi

echo "============================================================"
echo "PATCH — PRESERVAR PRÊMIO DE ENTRADA / PREÇO RTD ATUAL"
echo "============================================================"
echo "Projeto : ${PROJECT_ROOT}"
echo "Arquivo : ${TARGET}"
echo "Modo    : ${MODE}"
echo

OLD='                leg["premium"] = price
                leg["current_price"] = price'

NEW='                # O prêmio representa o custo/preço de entrada da leg.
                # O preço RTD atual é mantido em campo separado para a UI
                # e para eventuais cálculos de marcação a mercado.
                leg["current_price"] = price'

if ! grep -Fq 'leg["premium"] = price' "${TARGET}"; then
  if grep -Fq 'leg["current_price"] = price' "${TARGET}"; then
    echo "[OK] Patch já parece estar aplicado. Nenhuma alteração necessária."
    exit 0
  fi

  echo "[ERRO] Bloco esperado não encontrado; patch cancelado por segurança."
  exit 1
fi

echo "Alteração prevista:"
echo '  - Não sobrescrever leg["premium"] com cotação RTD.'
echo '  - Manter cotação RTD exclusivamente em leg["current_price"].'
echo

case "${MODE}" in
  --dry-run)
    echo "[OK] Dry-run concluído. Nenhum arquivo foi alterado."
    ;;
  --apply)
    TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
    BACKUP="${TARGET}.bak.${TIMESTAMP}"

    cp "${TARGET}" "${BACKUP}"
    echo "[OK] Backup criado: ${BACKUP}"

    python - "${TARGET}" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

old = '''                leg["premium"] = price
                leg["current_price"] = price'''

new = '''                # O prêmio representa o custo/preço de entrada da leg.
                # O preço RTD atual é mantido em campo separado para a UI
                # e para eventuais cálculos de marcação a mercado.
                leg["current_price"] = price'''

if old not in text:
    raise SystemExit("Bloco esperado não encontrado; arquivo não alterado.")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
PY

    echo "[OK] Atualizado: ${TARGET}"
    echo
    echo "[OK] Patch aplicado com sucesso."
    ;;
  *)
    echo "[ERRO] Uso:"
    echo "  bash $0 --dry-run"
    echo "  bash $0 --apply"
    exit 2
    ;;
esac
