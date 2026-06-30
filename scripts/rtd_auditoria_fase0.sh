#!/usr/bin/env bash

set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

AUDIT="docs/AUDITORIA_RTD_EXCEL_VIVO.md"
PLAN="docs/PLANO_RTD_EXCEL_VIVO.md"
OUTDIR="docs/levantamentos"
RUN_ID="$(date '+%Y%m%d_%H%M%S')"
CHECKLIST="$OUTDIR/checklist_operacional_rtd_$RUN_ID.md"

mkdir -p docs "$OUTDIR"

echo "Auditoria Fase 0: preparando arquivo de auditoria"

if [ ! -s "$AUDIT" ]; then
    cat > "$AUDIT" <<'AUDITEOF'
# Auditoria RTD Excel Vivo

## Objetivo

Acompanhar a implementação da arquitetura RTD sempre online com Excel aberto.

## Escopo

Baseado no documento:

    docs/PLANO_RTD_EXCEL_VIVO.md

## Regras operacionais principais

- Não migrar para web.
- Não utilizar emojis.
- Manter o escopo do projeto.
- Efetuar buscas de dados e arquivos antes de alterações.
- Toda mudança deve ser testada após concluída.
- Após o encerramento de fase, o teste deve compor todas as fases encerradas.
- Evitar códigos intermediários em explicações.
- Em alterações, gerar código automatizado via Git Bash.
- A cada alteração concluída e testada, commitar.
- Não codar sem rumo.
- Se necessário, buscar a evolução no Git.
- Atualizar este arquivo com testes, conclusões e evolução.

## Fases

### Fase 0: Documentação e verificação operacional

Status inicial:

    Em andamento.

### Fase 1: Transformar RTD em fonte online

Status inicial:

    Não iniciada.

### Fase 2: Snapshot centralizado

Status inicial:

    Não iniciada.

### Fase 3: Histórico intraday

Status inicial:

    Não iniciada.

### Fase 4: Motor de candles

Status inicial:

    Não iniciada.

### Fase 5: UI operacional em tempo real

Status inicial:

    Não iniciada.

### Fase 6: Retenção, limpeza e consolidação

Status inicial:

    Não iniciada.

### Fase 7: Alertas e decisão operacional

Status inicial:

    Não iniciada.

AUDITEOF
fi

echo "Auditoria Fase 0: verificando Git"

BRANCH="$(git branch --show-current 2>/dev/null || echo 'nao identificado')"
LAST_COMMIT="$(git log -1 --oneline 2>/dev/null || echo 'sem commit identificado')"
GIT_STATUS="$(git status --short 2>/dev/null || true)"

echo "Auditoria Fase 0: verificando Excel de forma segura"

EXCEL_INFO="Verificacao automatica nao executada"

if command -v powershell.exe >/dev/null 2>&1; then
    if command -v timeout >/dev/null 2>&1; then
        EXCEL_INFO="$(timeout 8s powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-Process EXCEL -ErrorAction SilentlyContinue | Select-Object -First 5 Id,ProcessName,MainWindowTitle | Format-Table -AutoSize | Out-String" 2>/dev/null | tr -d '\r' || true)"
    else
        EXCEL_INFO="Comando timeout nao encontrado. Verificacao automatica do Excel ignorada para evitar travamento."
    fi
fi

if [ -z "$EXCEL_INFO" ]; then
    EXCEL_INFO="Excel nao identificado em execucao, ou sem janela detectavel."
fi

echo "Auditoria Fase 0: procurando LISTA_RTD.xlsm"

RTD_FILES="$(find . -maxdepth 5 -type f -iname 'LISTA_RTD.xlsm' 2>/dev/null | sort || true)"

echo "Auditoria Fase 0: gerando checklist"

{
    echo "# Checklist operacional RTD Excel Vivo"
    echo ""
    echo "Data: $(date '+%d/%m/%Y %H:%M:%S')"
    echo "Raiz do projeto: $ROOT"
    echo ""
    echo "## Documentacao"
    echo ""
    if [ -f "$PLAN" ]; then
        echo "- Plano oficial encontrado: sim"
    else
        echo "- Plano oficial encontrado: nao"
    fi
    echo "- Arquivo de auditoria encontrado: sim"
    echo ""
    echo "## Git"
    echo ""
    echo "- Branch atual:"
    echo ""
    echo "    $BRANCH"
    echo ""
    echo "- Ultimo commit:"
    echo ""
    echo "    $LAST_COMMIT"
    echo ""
    echo "- Status resumido:"
    echo ""
    if [ -n "$GIT_STATUS" ]; then
        echo "$GIT_STATUS" | sed 's/^/    /'
    else
        echo "    Sem alteracoes identificadas pelo git status --short."
    fi
    echo ""
    echo "## Processo Excel"
    echo ""
    echo "$EXCEL_INFO" | sed 's/^/    /'
    echo ""
    echo "## Arquivo LISTA_RTD.xlsm"
    echo ""
    if [ -n "$RTD_FILES" ]; then
        echo "- Arquivo LISTA_RTD.xlsm encontrado no projeto:"
        echo ""
        echo "$RTD_FILES" | sed 's/^/    /'
    else
        echo "- Arquivo LISTA_RTD.xlsm nao encontrado dentro da pasta do projeto."
        echo "- Observacao: isso nao impede o uso se o arquivo estiver em outro caminho e aberto no Excel."
    fi
    echo ""
    echo "## Checklist manual da corretora e RTD"
    echo ""
    echo "- Programa da corretora aberto: pendente confirmacao manual"
    echo "- Corretora conectada: pendente confirmacao manual"
    echo "- LISTA_RTD.xlsm aberto no Excel: pendente confirmacao manual"
    echo "- Macros habilitadas: pendente confirmacao manual"
    echo "- Calculo automatico do Excel ativo: pendente confirmacao manual"
    echo "- Aba RTD identificada: pendente confirmacao manual"
    echo "- Celulas RTD atualizando: pendente confirmacao manual"
    echo "- Campo simbolo disponivel: pendente confirmacao manual"
    echo "- Campo bid disponivel: pendente confirmacao manual"
    echo "- Campo ask disponivel: pendente confirmacao manual"
    echo "- Campo ultimo disponivel: pendente confirmacao manual"
    echo "- Campo VWAP disponivel: pendente confirmacao manual"
    echo "- Campo volume disponivel: pendente confirmacao manual"
    echo "- Campos de gregas disponiveis: pendente confirmacao manual"
    echo "- Ultima atualizacao visivel: pendente confirmacao manual"
    echo ""
    echo "## Status RTD futuro para UI"
    echo ""
    echo "- Excel aberto"
    echo "- Workbook correto aberto"
    echo "- Aba RTD encontrada"
    echo "- Corretora conectada"
    echo "- Ultima atualizacao recebida"
    echo "- Quantidade de simbolos ativos"
    echo "- Quantidade de simbolos com erro"
    echo "- Tempo desde ultima atualizacao"
    echo "- Status geral: online, atrasado, erro ou offline"
    echo ""
    echo "## Resultado"
    echo ""
    echo "- Checklist gerado para validacao operacional."
    echo "- Nenhuma alteracao funcional executada."
} > "$CHECKLIST"

echo "Auditoria Fase 0: atualizando auditoria"

{
    echo ""
    echo "## Registro Fase 0 - $(date '+%d/%m/%Y %H:%M:%S')"
    echo ""
    echo "### Acao"
    echo ""
    echo "Geracao de checklist operacional seguro para a frente RTD Excel vivo."
    echo ""
    echo "### Arquivos verificados"
    echo ""
    echo "- $PLAN"
    echo "- $AUDIT"
    echo ""
    echo "### Arquivo de checklist gerado"
    echo ""
    echo "- $CHECKLIST"
    echo ""
    echo "### Resultado"
    echo ""
    echo "- Auditoria preparada."
    echo "- Checklist operacional preparado."
    echo "- Nenhuma alteracao funcional realizada."
    echo ""
    echo "### Pendencias"
    echo ""
    echo "- Executar consulta tecnica do projeto."
    echo "- Confirmar manualmente Excel, corretora, LISTA_RTD.xlsm e campos RTD."
    echo "- Mapear arquivos atuais que usam subprocesso, RTD, Excel e banco."
    echo ""
    echo "### Teste"
    echo ""
    echo "- Script de auditoria executado com mensagens de progresso."
    echo "- Checklist gerado em docs/levantamentos."
    echo ""
    echo "### Commit"
    echo ""
    echo "- Pendente."
} >> "$AUDIT"

echo "Auditoria Fase 0 concluida:"
echo "$AUDIT"
echo ""
echo "Checklist operacional gerado:"
echo "$CHECKLIST"
