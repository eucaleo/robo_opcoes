#!/usr/bin/env bash
set -euo pipefail

echo "== Inventariando arquivos reais relacionados a UI =="

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

DATA_ATUAL="$(date '+%Y-%m-%d %H:%M:%S %z')"
BRANCH_ATUAL="$(git branch --show-current)"

INVENTARIO_DOC="docs/INVENTARIO_ARQUIVOS_UI.md"
MATRIZ_DOC="docs/MATRIZ_EQUIVALENCIA_UI.md"
DEV_DOC="docs/DESENVOLVIMENTO_UI.md"
AUDIT_DOC="reports/auditoria/AUDITORIA_REFACTOR_UI.md"

for alvo in "$MATRIZ_DOC" "$DEV_DOC" "$AUDIT_DOC"; do
  if [ ! -f "$alvo" ]; then
    echo "ERRO: documento esperado nao encontrado: $alvo"
    exit 1
  fi
done

python - <<'PY'
from pathlib import Path
import re
import subprocess
from datetime import datetime

base = Path(".").resolve()

data_atual = subprocess.check_output(
    ["date", "+%Y-%m-%d %H:%M:%S %z"],
    text=True,
).strip()

branch = subprocess.check_output(
    ["git", "branch", "--show-current"],
    text=True,
).strip()

saida = Path("docs/INVENTARIO_ARQUIVOS_UI.md")

excluir_dirs = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".cache",
    "logs",
}

extensoes_alvo = {
    ".py",
    ".ui",
    ".qss",
    ".css",
    ".scss",
    ".html",
    ".htm",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".md",
}

palavras_caminho = [
    "ui",
    "gui",
    "view",
    "views",
    "screen",
    "screens",
    "panel",
    "panels",
    "tab",
    "tabs",
    "widget",
    "widgets",
    "dialog",
    "dialogs",
    "window",
    "windows",
    "layout",
    "layouts",
    "page",
    "pages",
    "frontend",
    "interface",
]

padroes_conteudo = {
    "tkinter": r"\btkinter\b|\bttk\b|\bTk\(|\bmainloop\(",
    "customtkinter": r"\bcustomtkinter\b|\bctk\b|\bCTk",
    "pyqt/pyside": r"\bPyQt[56]?\b|\bPySide[26]?\b|\bQApplication\b|\bQWidget\b|\bQMainWindow\b",
    "streamlit": r"\bstreamlit\b|\bst\.",
    "dash/plotly": r"\bdash\b|\bplotly\b",
    "matplotlib_ui": r"\bFigureCanvas\b|\bNavigationToolbar\b",
    "textual/rich": r"\btextual\b|\brich\b",
    "flask_fastapi_template": r"\brender_template\b|\bTemplateResponse\b",
    "ui_terms": r"\bPanel\b|\bTab\b|\bWidget\b|\bDialog\b|\bWindow\b|\bView\b|\bScreen\b|\bLayout\b",
    "decisoes": r"decis[aã]o|decisoes|decisions",
    "payoff": r"payoff",
    "vwap": r"vwap|VWAP",
    "dark": r"dark|theme|tema",
}

entrypoint_padroes = [
    r"if\s+__name__\s*==\s*['\"]__main__['\"]",
    r"\bmainloop\(",
    r"\bQApplication\(",
    r"\bst\.set_page_config\(",
    r"\bapp\.run\(",
]

def deve_excluir(path: Path) -> bool:
    partes = set(path.parts)
    return bool(partes & excluir_dirs)

def ler_texto(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

arquivos = []

for path in sorted(Path(".").rglob("*")):
    if not path.is_file():
        continue
    if deve_excluir(path):
        continue
    if path.suffix.lower() not in extensoes_alvo:
        continue

    rel = path.as_posix()
    rel_lower = rel.lower()
    nome_lower = path.name.lower()
    texto = ler_texto(path)
    texto_lower = texto.lower()

    motivos = []
    score = 0

    if any(p in rel_lower for p in palavras_caminho):
        motivos.append("caminho/nome sugere UI")
        score += 2

    hits = []
    for nome, padrao in padroes_conteudo.items():
        if re.search(padrao, texto, flags=re.IGNORECASE):
            hits.append(nome)

    if hits:
        motivos.append("conteudo: " + ", ".join(hits))
        score += len(hits) * 2

    entrypoint = any(re.search(p, texto) for p in entrypoint_padroes)
    if entrypoint:
        motivos.append("possivel entrypoint")
        score += 3

    if score > 0:
        linhas = texto.count("\n") + 1 if texto else 0
        arquivos.append({
            "path": rel,
            "ext": path.suffix.lower(),
            "linhas": linhas,
            "score": score,
            "motivos": motivos,
            "entrypoint": entrypoint,
            "hits": hits,
        })

arquivos.sort(key=lambda x: (-x["score"], x["path"]))

provaveis_ui = [a for a in arquivos if a["score"] >= 4]
possiveis_ui = [a for a in arquivos if a["score"] < 4]
entrypoints = [a for a in arquivos if a["entrypoint"]]

def tabela(lista):
    if not lista:
        return "_Nenhum arquivo identificado nesta classificacao._\n"

    out = []
    out.append("| Arquivo | Linhas | Sinais | Observacao inicial |")
    out.append("|---|---:|---|---|")
    for a in lista:
        sinais = "; ".join(a["motivos"]).replace("|", "/")
        obs = "PENDENTE"
        if a["entrypoint"]:
            obs = "PENDENTE - possivel entrypoint, preservar ate auditoria propria"
        out.append(f"| `{a['path']}` | {a['linhas']} | {sinais} | {obs} |")
    return "\n".join(out) + "\n"

conteudo = f"""# Inventario Inicial de Arquivos Reais da UI

Data: {data_atual}

Branch: {branch}

## Objetivo

Este documento registra um inventario inicial dos arquivos do repositorio que possuem sinais de participacao na UI.

A finalidade e apoiar o preenchimento da matriz global de equivalencia da UI sem alterar comportamento, banco, services, repositories ou entrypoint principal.

Documento relacionado:

- `docs/MATRIZ_EQUIVALENCIA_UI.md`

## Escopo desta fatia

Esta etapa e somente diagnostica/documental.

Nao declara equivalencia completa de nenhuma area.

Nao autoriza substituicao da UI canonica.

Nao altera caminho principal de execucao.

## Metodo de identificacao

O inventario foi gerado por varredura estatica de arquivos com extensoes de codigo, layout, estilo e documentacao.

Foram considerados sinais como:

- nomes de caminho relacionados a UI;
- uso de bibliotecas de interface;
- termos como panel, tab, widget, view, screen e layout;
- referencias a decisoes, payoff, VWAP e tema dark;
- possiveis entrypoints.

## Resumo quantitativo

| Classificacao | Quantidade |
|---|---:|
| Provaveis arquivos de UI | {len(provaveis_ui)} |
| Possiveis arquivos relacionados a UI | {len(possiveis_ui)} |
| Possiveis entrypoints | {len(entrypoints)} |
| Total com algum sinal | {len(arquivos)} |

## Possiveis entrypoints identificados

{tabela(entrypoints)}

## Provaveis arquivos de UI

{tabela(provaveis_ui)}

## Possiveis arquivos relacionados a UI

{tabela(possiveis_ui)}

## Leitura operacional inicial

Os arquivos listados acima devem ser tratados como candidatos.

Cada candidato ainda precisa ser classificado na matriz global como:

- CANONICA;
- EQUIVALENTE;
- EQUIVALENCIA_PARCIAL_OPERACIONAL;
- EXPERIMENTAL;
- PENDENTE;
- FORA_ESCOPO.

## Regras de seguranca

1. Possiveis entrypoints nao devem ser alterados nesta frente.
2. Arquivos de banco/dados/pipeline nao devem ser misturados com refactor visual.
3. Areas Terminal VWAP, payoff curve e UIDataModel exigem auditoria propria.
4. A UI canonica permanece preservada ate decisao explicita.
5. Este inventario nao substitui smoke manual.

## Proxima acao recomendada

Cruzar este inventario com a matriz global para abrir uma tabela por area/aba/fluxo.

A proxima fatia recomendada e documentar:

- arquivos candidatos da UI canonica;
- arquivos candidatos da UI moderna/dark;
- lacunas por aba;
- areas que exigem auditoria propria.
"""

saida.write_text(conteudo, encoding="utf-8", newline="\n")
print(f"Gerado: {saida}")
print(f"Total com sinais: {len(arquivos)}")
print(f"Provaveis UI: {len(provaveis_ui)}")
print(f"Possiveis UI: {len(possiveis_ui)}")
print(f"Possiveis entrypoints: {len(entrypoints)}")
PY

MARKER_DEV="Referencia inventario inicial de arquivos reais da UI"

if ! grep -q "$MARKER_DEV" "$DEV_DOC"; then
  cat >> "$DEV_DOC" <<EOF_DEV

---

## $MARKER_DEV

Data: $DATA_ATUAL

Foi criado o inventario inicial de arquivos reais relacionados a UI:

    docs/INVENTARIO_ARQUIVOS_UI.md

Este inventario deve ser usado para preencher a matriz global de equivalencia da UI com base em arquivos concretos do repositorio.

Regra operacional:

Nenhum arquivo identificado como possivel entrypoint deve ser alterado sem auditoria propria e plano de rollback.

EOF_DEV
  echo "Atualizado: $DEV_DOC"
else
  echo "Marcador ja existe em $DEV_DOC"
fi

MARKER_MATRIZ="Referencia inventario inicial de arquivos reais"

if ! grep -q "$MARKER_MATRIZ" "$MATRIZ_DOC"; then
  cat >> "$MATRIZ_DOC" <<EOF_MATRIZ

---

## $MARKER_MATRIZ

Data: $DATA_ATUAL

Foi criado o inventario inicial de arquivos reais relacionados a UI:

    docs/INVENTARIO_ARQUIVOS_UI.md

Este inventario passa a ser insumo para preencher a matriz por area, aba e fluxo.

A classificacao da matriz ainda deve ser feita manualmente ou em fatias documentadas, pois a varredura estatica apenas identifica candidatos.

EOF_MATRIZ
  echo "Atualizado: $MATRIZ_DOC"
else
  echo "Marcador ja existe em $MATRIZ_DOC"
fi

MARKER_AUDIT="Checkpoint inventario inicial de arquivos reais da UI"

if ! grep -q "$MARKER_AUDIT" "$AUDIT_DOC"; then
  cat >> "$AUDIT_DOC" <<EOF_AUDIT

---

## $MARKER_AUDIT

Data: $DATA_ATUAL

Branch: $BRANCH_ATUAL

Foi criado o inventario inicial de arquivos reais relacionados a UI:

    docs/INVENTARIO_ARQUIVOS_UI.md

### Decisao

Este checkpoint permanece diagnostico/documental.

Nao houve alteracao de banco, regra de negocio, services, repositories ou entrypoint principal.

### Uso esperado

O inventario deve apoiar as proximas fatias de classificacao da matriz global de equivalencia da UI.

### Proxima fatia recomendada

Classificar os arquivos candidatos por area:

- UI canonica;
- UI moderna/dark;
- Decisoes;
- Terminal VWAP;
- payoff curve;
- UIDataModel;
- banco/dados/pipeline fora de escopo da UI visual.

EOF_AUDIT
  echo "Atualizado: $AUDIT_DOC"
else
  echo "Marcador ja existe em $AUDIT_DOC"
fi

python - <<'PY'
from pathlib import Path

arquivos = [
    Path("docs/INVENTARIO_ARQUIVOS_UI.md"),
    Path("docs/MATRIZ_EQUIVALENCIA_UI.md"),
    Path("docs/DESENVOLVIMENTO_UI.md"),
    Path("reports/auditoria/AUDITORIA_REFACTOR_UI.md"),
    Path("scripts/inventariar_arquivos_ui.sh"),
]

for path in arquivos:
    if not path.exists():
        continue

    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()

    while lines and lines[-1].strip() == "":
        lines.pop()

    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Normalizado EOF: {path}")
PY

echo "== Fim do inventario inicial de UI =="
