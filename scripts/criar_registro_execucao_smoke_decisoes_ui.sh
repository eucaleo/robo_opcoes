#!/usr/bin/env bash
set -euo pipefail

echo "== Criando template de registro de execucao do smoke de Decisoes sem crases =="

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

DATA_ATUAL="$(date '+%Y-%m-%d %H:%M:%S %z')"
BRANCH_ATUAL="$(git branch --show-current)"
COMMIT_ATUAL="$(git rev-parse --short HEAD)"

MATRIZ_DOC="docs/MATRIZ_EQUIVALENCIA_UI.md"
SMOKE_DOC="docs/SMOKE_MANUAL_DECISOES_UI.md"
DEV_DOC="docs/DESENVOLVIMENTO_UI.md"
AUDIT_DOC="reports/auditoria/AUDITORIA_REFACTOR_UI.md"
REGISTRO_DOC="docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md"

for alvo in "$MATRIZ_DOC" "$SMOKE_DOC" "$DEV_DOC" "$AUDIT_DOC"; do
  if [ ! -f "$alvo" ]; then
    echo "ERRO: documento esperado nao encontrado: $alvo"
    exit 1
  fi
done

python - <<'PY'
from pathlib import Path
import subprocess
import re

data_atual = subprocess.check_output(
    ["date", "+%Y-%m-%d %H:%M:%S %z"],
    text=True,
).strip()

branch = subprocess.check_output(
    ["git", "branch", "--show-current"],
    text=True,
).strip()

commit = subprocess.check_output(
    ["git", "rev-parse", "--short", "HEAD"],
    text=True,
).strip()

dev_doc = Path("docs/DESENVOLVIMENTO_UI.md")
matriz_doc = Path("docs/MATRIZ_EQUIVALENCIA_UI.md")
audit_doc = Path("reports/auditoria/AUDITORIA_REFACTOR_UI.md")
registro_doc = Path("docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md")

marker_dev = "Referencia template de registro de execucao do smoke de Decisoes"
marker_matriz = "Referencia template de registro de execucao do smoke de Decisoes"
marker_audit = "Checkpoint template de registro de execucao do smoke de Decisoes"

def remove_marker_section(path: Path, marker: str) -> None:
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8", errors="replace")

    pattern = re.compile(
        r"\n---\n\n## " + re.escape(marker) + r"\n.*?(?=\n---\n\n## |\Z)",
        re.DOTALL,
    )

    text = pattern.sub("", text)

    lines = text.splitlines()
    while lines and lines[-1].strip() == "":
        lines.pop()

    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

remove_marker_section(dev_doc, marker_dev)
remove_marker_section(matriz_doc, marker_matriz)
remove_marker_section(audit_doc, marker_audit)

conteudo = f"""# Registro de Execucao do Smoke Manual - UI Decisoes

Data de criacao do template: {data_atual}

Branch base: {branch}

Commit base: {commit}

## Objetivo

Este documento deve ser preenchido apos a execucao do checklist de smoke manual da area Decisoes.

Checklist relacionado:

    docs/SMOKE_MANUAL_DECISOES_UI.md

Documentos de contexto:

    docs/MATRIZ_EQUIVALENCIA_UI.md
    docs/MATRIZ_CRUZADA_AREAS_UI.md
    docs/CLASSIFICACAO_AREAS_UI.md
    docs/INVENTARIO_ARQUIVOS_UI.md
    reports/auditoria/AUDITORIA_REFACTOR_UI.md

## Escopo

Este registro documenta uma execucao manual.

Nao altera comportamento.

Nao altera UI runtime.

Nao altera banco.

Nao altera services, repositories ou regra de negocio.

Nao altera entrypoint principal.

Nao declara equivalencia completa automaticamente.

## Identificacao da execucao

Preencher no momento do teste:

| Campo | Valor |
|---|---|
| Data/hora real da execucao | PENDENTE |
| Responsavel | PENDENTE |
| Branch testada | {branch} |
| Commit testado | {commit} |
| Sistema operacional | PENDENTE |
| Ambiente | Local |
| Base/dataset utilizado | PENDENTE |
| UI canonica utilizada? | PENDENTE |
| UI moderna/dark utilizada? | PENDENTE |
| Comando usado para abrir a aplicacao | PENDENTE |
| Observacoes de ambiente | PENDENTE |

## Resultado resumido

| Grupo | Resultado | Observacao |
|---|---|---|
| Abertura da aplicacao | PENDENTE | PENDENTE |
| Acesso a area Decisoes | PENDENTE | PENDENTE |
| Navegacao basica | PENDENTE | PENDENTE |
| Estado vazio | PENDENTE | PENDENTE |
| Selecao invalida/incompleta | PENDENTE | PENDENTE |
| Carregamento com dados validos | PENDENTE | PENDENTE |
| Mensagens/status/erros | PENDENTE | PENDENTE |
| Tema dark/UI moderna | PENDENTE | PENDENTE |
| Comparacao com UI canonica | PENDENTE | PENDENTE |
| Rollback/retorno seguro | PENDENTE | PENDENTE |

Legenda sugerida:

    OK
    OK_COM_OBSERVACAO
    FALHOU
    NAO_APLICAVEL
    NAO_TESTADO

## Registro detalhado

### 1. Preparacao

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 2. Abertura da aplicacao

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 3. Acesso a area Decisoes

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 4. Estado vazio

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 5. Selecao invalida ou incompleta

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 6. Carregamento com dados validos

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 7. Mensagens, status e erros

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 8. Tema dark / UI moderna

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 9. Comparacao com UI canonica

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 10. Rollback / retorno seguro

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

## Divergencias encontradas

| ID | Severidade | Descricao | UI canonica | UI moderna/dark | Evidencia | Acao recomendada | Status |
|---|---|---|---|---|---|---|---|
| D-001 | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

Se nenhuma divergencia for encontrada, substituir a tabela por:

    Nenhuma divergencia encontrada nesta execucao.

## Erros ou logs relevantes

    PENDENTE

## Evidencias anexadas ou referenciadas

| Tipo | Caminho/link | Descricao |
|---|---|---|
| Screenshot | PENDENTE | PENDENTE |
| Log | PENDENTE | PENDENTE |
| Observacao manual | PENDENTE | PENDENTE |

## Classificacao final da execucao

Preencher apos o teste:

| Campo | Valor |
|---|---|
| Smoke executado ate o fim? | PENDENTE |
| Houve erro bloqueante? | PENDENTE |
| Houve divergencia critica contra UI canonica? | PENDENTE |
| Estado vazio aprovado? | PENDENTE |
| Selecao invalida aprovada? | PENDENTE |
| Dados validos aprovados? | PENDENTE |
| Mensagens/status aprovados? | PENDENTE |
| Tema dark aprovado para uso parcial? | PENDENTE |
| Pode manter equivalencia parcial operacional? | PENDENTE |
| Pode evoluir para equivalencia completa? | NAO, depende de decisao explicita posterior |

## Decisao apos execucao

Selecionar uma opcao:

- [ ] Manter EQUIVALENCIA_PARCIAL_OPERACIONAL sem nova alteracao.
- [ ] Manter EQUIVALENCIA_PARCIAL_OPERACIONAL e abrir correcao pequena.
- [ ] Rebaixar status por falha critica.
- [ ] Solicitar nova auditoria antes de runtime.
- [ ] Propor evolucao controlada para equivalencia completa em nova branch/fatia.

Justificativa:

    PENDENTE

## Proxima acao recomendada

Preencher apos o teste:

    PENDENTE

## Restricoes mantidas

Mesmo apos o preenchimento deste registro:

- UI canonica permanece preservada ate decisao explicita;
- Terminal VWAP permanece fora do escopo desta branch;
- payoff curve permanece fora do escopo desta branch;
- UIDataModel permanece fora do escopo desta branch;
- banco/dados/pipeline permanecem fora do escopo visual;
- possiveis entrypoints permanecem preservados.
"""

registro_doc.write_text(conteudo, encoding="utf-8", newline="\n")
print(f"Gerado: {registro_doc}")

dev_append = f"""

---

## {marker_dev}

Data: {data_atual}

Foi criado o template de registro de execucao do smoke manual da area Decisoes:

    docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md

Este documento deve ser preenchido apos a execucao do checklist:

    docs/SMOKE_MANUAL_DECISOES_UI.md

Regra operacional:

O preenchimento do registro nao declara equivalencia completa automaticamente. A UI canonica permanece preservada ate decisao explicita.
"""

matriz_append = f"""

---

## {marker_matriz}

Data: {data_atual}

Foi criado o template de registro de execucao do smoke manual da area Decisoes:

    docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md

A area Decisoes permanece como equivalencia parcial operacional ate execucao do smoke, registro de evidencias e decisao explicita posterior.
"""

audit_append = f"""

---

## {marker_audit}

Data: {data_atual}

Branch: {branch}

Commit base: {commit}

Foi criado o template de registro de execucao do smoke manual da area Decisoes:

    docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md

### Decisao

Este checkpoint permanece documental.

Nao houve alteracao de banco, regra de negocio, services, repositories, runtime de UI ou entrypoint principal.

### Uso esperado

O registro deve ser preenchido apos execucao do checklist de smoke manual.

### Restricoes mantidas

- UI canonica preservada;
- Terminal VWAP fora do escopo da branch atual;
- payoff curve fora do escopo da branch atual;
- UIDataModel fora do escopo da branch atual;
- banco/dados/pipeline fora do escopo visual;
- possiveis entrypoints preservados.
"""

dev_doc.write_text(
    dev_doc.read_text(encoding="utf-8", errors="replace").rstrip() + dev_append,
    encoding="utf-8",
    newline="\n",
)
print(f"Atualizado: {dev_doc}")

matriz_doc.write_text(
    matriz_doc.read_text(encoding="utf-8", errors="replace").rstrip() + matriz_append,
    encoding="utf-8",
    newline="\n",
)
print(f"Atualizado: {matriz_doc}")

audit_doc.write_text(
    audit_doc.read_text(encoding="utf-8", errors="replace").rstrip() + audit_append,
    encoding="utf-8",
    newline="\n",
)
print(f"Atualizado: {audit_doc}")

for path in [
    registro_doc,
    matriz_doc,
    dev_doc,
    audit_doc,
]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()

    while lines and lines[-1].strip() == "":
        lines.pop()

    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Normalizado EOF: {path}")

for path in [
    registro_doc,
]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if chr(96) in raw:
        raise SystemExit(f"ERRO: crase encontrada em {path}")

print("Validado: template sem crases")
PY

python - <<'PY'
from pathlib import Path

path = Path("scripts/criar_registro_execucao_smoke_decisoes_ui.sh")
raw = path.read_text(encoding="utf-8", errors="replace")
lines = raw.splitlines()

while lines and lines[-1].strip() == "":
    lines.pop()

path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

if chr(96) in path.read_text(encoding="utf-8", errors="replace"):
    raise SystemExit(f"ERRO: crase encontrada em {path}")

print(f"Normalizado EOF: {path}")
print("Validado: script sem crases")
PY

echo "== Fim do template sem crases =="
