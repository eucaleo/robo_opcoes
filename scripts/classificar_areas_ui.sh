#!/usr/bin/env bash
set -euo pipefail

echo "== Classificando arquivos UI por area da matriz =="

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

DATA_ATUAL="$(date '+%Y-%m-%d %H:%M:%S %z')"
BRANCH_ATUAL="$(git branch --show-current)"

INVENTARIO_DOC="docs/INVENTARIO_ARQUIVOS_UI.md"
MATRIZ_DOC="docs/MATRIZ_EQUIVALENCIA_UI.md"
DEV_DOC="docs/DESENVOLVIMENTO_UI.md"
AUDIT_DOC="reports/auditoria/AUDITORIA_REFACTOR_UI.md"
CLASSIFICACAO_DOC="docs/CLASSIFICACAO_AREAS_UI.md"

for alvo in "$INVENTARIO_DOC" "$MATRIZ_DOC" "$DEV_DOC" "$AUDIT_DOC"; do
  if [ ! -f "$alvo" ]; then
    echo "ERRO: documento esperado nao encontrado: $alvo"
    exit 1
  fi
done

python - <<'PY'
from pathlib import Path
import re
import subprocess

data_atual = subprocess.check_output(
    ["date", "+%Y-%m-%d %H:%M:%S %z"],
    text=True,
).strip()

branch = subprocess.check_output(
    ["git", "branch", "--show-current"],
    text=True,
).strip()

saida = Path("docs/CLASSIFICACAO_AREAS_UI.md")

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

sinais_ui = [
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
    "tkinter",
    "customtkinter",
    "pyqt",
    "pyside",
    "streamlit",
    "dash",
    "plotly",
    "matplotlib",
]

padroes_area = {
    "Decisoes": [
        r"decis[aã]o",
        r"decisoes",
        r"decisions",
        r"decision",
    ],
    "Terminal VWAP": [
        r"\bvwap\b",
        r"terminal",
    ],
    "Payoff curve": [
        r"payoff",
        r"curve",
        r"curva",
    ],
    "UIDataModel": [
        r"uidatamodel",
        r"ui_data_model",
        r"data\s*model",
        r"view\s*model",
    ],
    "Tema dark / UI moderna": [
        r"\bdark\b",
        r"theme",
        r"tema",
        r"modern",
        r"moderna",
    ],
    "Navegacao / abas / layout": [
        r"\btab\b",
        r"\btabs\b",
        r"aba",
        r"abas",
        r"layout",
        r"navigation",
        r"navegacao",
        r"router",
    ],
    "Estados / mensagens / feedback": [
        r"status",
        r"message",
        r"mensagem",
        r"toast",
        r"alert",
        r"warning",
        r"error",
        r"erro",
        r"empty",
        r"vazio",
    ],
    "Banco/dados/pipeline - fora do escopo visual": [
        r"database",
        r"\bdb\b",
        r"sql",
        r"sqlite",
        r"postgres",
        r"pipeline",
        r"repository",
        r"repositories",
        r"service",
        r"services",
        r"dao",
        r"model",
        r"schema",
    ],
}

entrypoint_padroes = [
    r"if\s+__name__\s*==\s*['\"]__main__['\"]",
    r"\bmainloop\(",
    r"\bQApplication\(",
    r"\bst\.set_page_config\(",
    r"\bapp\.run\(",
]

bibliotecas_ui = [
    r"\btkinter\b",
    r"\bttk\b",
    r"\bcustomtkinter\b",
    r"\bctk\b",
    r"\bPyQt[56]?\b",
    r"\bPySide[26]?\b",
    r"\bQApplication\b",
    r"\bQWidget\b",
    r"\bQMainWindow\b",
    r"\bstreamlit\b",
    r"\bst\.",
    r"\bdash\b",
    r"\bplotly\b",
    r"\bFigureCanvas\b",
    r"\bNavigationToolbar\b",
]

def deve_excluir(path: Path) -> bool:
    return bool(set(path.parts) & excluir_dirs)

def ler(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

def tem_regex(texto: str, padroes) -> bool:
    return any(re.search(p, texto, flags=re.IGNORECASE) for p in padroes)

arquivos = []

for path in sorted(Path(".").rglob("*")):
    if not path.is_file():
        continue
    if deve_excluir(path):
        continue
    if path.suffix.lower() not in extensoes_alvo:
        continue

    rel = path.as_posix()
    texto = ler(path)
    alvo = rel + "\n" + texto

    caminho_lower = rel.lower()
    texto_lower = texto.lower()

    tem_sinal_ui = (
        any(s in caminho_lower for s in sinais_ui)
        or tem_regex(texto, bibliotecas_ui)
        or tem_regex(texto, [r"\bPanel\b", r"\bTab\b", r"\bWidget\b", r"\bDialog\b", r"\bWindow\b", r"\bView\b", r"\bScreen\b"])
    )

    if not tem_sinal_ui:
        continue

    areas = []
    for area, padroes in padroes_area.items():
        if tem_regex(alvo, padroes):
            areas.append(area)

    if not areas:
        areas.append("UI geral / pendente de classificacao fina")

    entrypoint = tem_regex(texto, entrypoint_padroes)

    linhas = texto.count("\n") + 1 if texto else 0

    arquivos.append({
        "path": rel,
        "linhas": linhas,
        "areas": areas,
        "entrypoint": entrypoint,
    })

areas_ordenadas = [
    "Decisoes",
    "Terminal VWAP",
    "Payoff curve",
    "UIDataModel",
    "Tema dark / UI moderna",
    "Navegacao / abas / layout",
    "Estados / mensagens / feedback",
    "Banco/dados/pipeline - fora do escopo visual",
    "UI geral / pendente de classificacao fina",
]

por_area = {area: [] for area in areas_ordenadas}
entrypoints = []

for item in arquivos:
    if item["entrypoint"]:
        entrypoints.append(item)
    for area in item["areas"]:
        por_area.setdefault(area, []).append(item)

def tabela(lista):
    if not lista:
        return "_Nenhum candidato identificado nesta area._\n"

    out = [
        "| Arquivo | Linhas | Observacao inicial |",
        "|---|---:|---|",
    ]

    vistos = set()
    for item in sorted(lista, key=lambda x: x["path"]):
        if item["path"] in vistos:
            continue
        vistos.add(item["path"])

        obs = "PENDENTE - classificar manualmente contra UI canonica"
        if item["entrypoint"]:
            obs = "PENDENTE - possivel entrypoint, preservar ate auditoria propria"
        if "Banco/dados/pipeline - fora do escopo visual" in item["areas"]:
            obs = "FORA_ESCOPO_VISUAL - nao misturar com refactor de UI"

        path = item["path"].replace("|", "/")
        obs = obs.replace("|", "/")
        out.append(f"| `{path}` | {item['linhas']} | {obs} |")

    return "\n".join(out) + "\n"

resumo = []
for area in areas_ordenadas:
    caminhos = {i["path"] for i in por_area.get(area, [])}
    resumo.append((area, len(caminhos)))

conteudo = f"""# Classificacao Inicial dos Arquivos UI por Area

Data: {data_atual}

Branch: {branch}

## Objetivo

Este documento classifica, de forma inicial e diagnostica, os arquivos candidatos de UI por area da matriz global de equivalencia.

Documentos relacionados:

- `docs/INVENTARIO_ARQUIVOS_UI.md`
- `docs/MATRIZ_EQUIVALENCIA_UI.md`

## Escopo desta fatia

Esta etapa apenas organiza candidatos por area.

Nao altera comportamento.

Nao altera banco.

Nao altera services, repositories ou regra de negocio.

Nao altera entrypoint principal.

Nao declara equivalencia completa de nenhuma area.

## Metodo

A classificacao foi gerada por varredura estatica de caminhos e conteudo.

Os grupos abaixo sao candidatos iniciais e ainda exigem revisao manual.

## Resumo por area

| Area | Quantidade de candidatos |
|---|---:|
"""

for area, qtd in resumo:
    conteudo += f"| {area} | {qtd} |\n"

conteudo += f"""| Possiveis entrypoints | {len({i["path"] for i in entrypoints})} |

## Possiveis entrypoints

Regra: preservar estes arquivos ate auditoria propria e plano de rollback.

{tabela(entrypoints)}

"""

for area in areas_ordenadas:
    conteudo += f"## {area}\n\n"
    conteudo += tabela(por_area.get(area, []))
    conteudo += "\n"

conteudo += """## Leitura operacional

Esta classificacao inicial deve ser usada para preencher a matriz global por area, aba e fluxo.

### Decisoes

A frente Decisoes permanece como area com equivalencia parcial operacional, conforme auditoria ja registrada.

### Terminal VWAP

Permanece fora do escopo da branch atual ate auditoria propria.

### Payoff curve

Permanece fora do escopo da branch atual ate auditoria propria.

### UIDataModel

Permanece fora do escopo da branch atual ate mapeamento de consumidores e contratos.

### Banco/dados/pipeline

Itens classificados como banco, dados, services, repositories ou pipeline nao devem ser tratados como refactor visual.

## Proxima acao recomendada

Criar uma matriz cruzada por area contendo:

- area;
- arquivos candidatos;
- status atual;
- evidencia;
- risco;
- proxima acao.

Essa matriz cruzada deve orientar a escolha da proxima fatia pequena de desenvolvimento.
"""

saida.write_text(conteudo, encoding="utf-8", newline="\n")

print(f"Gerado: {saida}")
print(f"Total de candidatos UI classificados: {len(arquivos)}")
print(f"Possiveis entrypoints: {len(entrypoints)}")
for area, qtd in resumo:
    print(f"{area}: {qtd}")
PY

MARKER_DEV="Referencia classificacao inicial dos arquivos UI por area"

if ! grep -q "$MARKER_DEV" "$DEV_DOC"; then
  cat >> "$DEV_DOC" <<EOF_DEV

---

## $MARKER_DEV

Data: $DATA_ATUAL

Foi criada a classificacao inicial dos arquivos candidatos de UI por area:

    docs/CLASSIFICACAO_AREAS_UI.md

Esta classificacao complementa o inventario inicial e deve orientar o preenchimento da matriz global de equivalencia.

Regra operacional:

Arquivos classificados como possiveis entrypoints, banco, dados, services, repositories ou pipeline permanecem preservados ate auditoria propria.

EOF_DEV
  echo "Atualizado: $DEV_DOC"
else
  echo "Marcador ja existe em $DEV_DOC"
fi

MARKER_MATRIZ="Referencia classificacao inicial por area"

if ! grep -q "$MARKER_MATRIZ" "$MATRIZ_DOC"; then
  cat >> "$MATRIZ_DOC" <<EOF_MATRIZ

---

## $MARKER_MATRIZ

Data: $DATA_ATUAL

Foi criada a classificacao inicial dos arquivos candidatos de UI por area:

    docs/CLASSIFICACAO_AREAS_UI.md

A classificacao devera ser usada para transformar o inventario bruto em uma matriz operacional por area, aba e fluxo.

Esta classificacao ainda nao declara equivalencia completa.

EOF_MATRIZ
  echo "Atualizado: $MATRIZ_DOC"
else
  echo "Marcador ja existe em $MATRIZ_DOC"
fi

MARKER_AUDIT="Checkpoint classificacao inicial dos arquivos UI por area"

if ! grep -q "$MARKER_AUDIT" "$AUDIT_DOC"; then
  cat >> "$AUDIT_DOC" <<EOF_AUDIT

---

## $MARKER_AUDIT

Data: $DATA_ATUAL

Branch: $BRANCH_ATUAL

Foi criada a classificacao inicial dos arquivos candidatos de UI por area:

    docs/CLASSIFICACAO_AREAS_UI.md

### Decisao

Este checkpoint permanece documental/diagnostico.

Nao houve alteracao de banco, regra de negocio, services, repositories ou entrypoint principal.

### Areas preservadas

- Terminal VWAP permanece fora do escopo da branch atual;
- payoff curve permanece fora do escopo da branch atual;
- UIDataModel permanece fora do escopo da branch atual;
- banco/dados/pipeline permanecem fora do escopo visual;
- possiveis entrypoints permanecem preservados.

### Proxima fatia recomendada

Criar matriz cruzada de area x arquivos x status x risco x proxima acao.

EOF_AUDIT
  echo "Atualizado: $AUDIT_DOC"
else
  echo "Marcador ja existe em $AUDIT_DOC"
fi

python - <<'PY'
from pathlib import Path

arquivos = [
    Path("docs/CLASSIFICACAO_AREAS_UI.md"),
    Path("docs/INVENTARIO_ARQUIVOS_UI.md"),
    Path("docs/MATRIZ_EQUIVALENCIA_UI.md"),
    Path("docs/DESENVOLVIMENTO_UI.md"),
    Path("reports/auditoria/AUDITORIA_REFACTOR_UI.md"),
    Path("scripts/classificar_areas_ui.sh"),
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

echo "== Fim da classificacao por area =="
