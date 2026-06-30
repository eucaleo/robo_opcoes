#!/usr/bin/env bash

set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

echo "Iniciando Fase 0 - Documentacao e verificacao operacional"
echo ""

echo "Etapa 1 de 2: auditoria operacional"
bash scripts/rtd_auditoria_fase0.sh
echo ""

echo "Etapa 2 de 2: consulta tecnica controlada"
bash scripts/rtd_consulta_projeto.sh
echo ""

echo "Fase 0 executada."
echo ""
echo "Arquivos gerados em:"
echo "docs/AUDITORIA_RTD_EXCEL_VIVO.md"
echo "docs/levantamentos/"
echo ""
echo "Proximo passo:"
echo "Revisar os relatorios gerados e executar git status."
