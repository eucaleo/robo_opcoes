#!/usr/bin/env bash
set -euo pipefail

echo "== Criando matriz cruzada area x arquivos x status x risco =="

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

DATA_ATUAL="$(date '+%Y-%m-%d %H:%M:%S %z')"
BRANCH_ATUAL="$(git branch --show-current)"

INVENTARIO_DOC="docs/INVENTARIO_ARQUIVOS_UI.md"
CLASSIFICACAO_DOC="docs/CLASSIFICACAO_AREAS_UI.md"
MATRIZ_DOC="docs/MATRIZ_EQUIVALENCIA_UI.md"
DEV_DOC="docs/DESENVOLVIMENTO_UI.md"
AUDIT_DOC="reports/auditoria/AUDITORIA_REFACTOR_UI.md"
CRUZADA_DOC="docs/MATRIZ_CRUZADA_AREAS_UI.md"

for alvo in "$INVENTARIO_DOC" "$CLASSIFICACAO_DOC" "$MATRIZ_DOC" "$DEV_DOC" "$AUDIT_DOC"; do
  if [ ! -f "$alvo" ]; then
    echo "ERRO: documento esperado nao encontrado: $alvo"
    exit 1
  fi
done

python - <<'PY'
from pathlib import Path
import re
import subprocess
from collections import defaultdict

data_atual = subprocess.check_output(
    ["date", "+%Y-%m-%d %H:%M:%S %z"],
    text=True,
).strip()

branch = subprocess.check_output(
    ["git", "branch", "--show-current"],
    text=True,
).strip()

saida = Path("docs/MATRIZ_CRUZADA_AREAS_UI.md")

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

def status_risco_acao(area: str, entrypoint: bool):
    if entrypoint:
        return (
            "PRESERVAR_ENTRYPOINT",
            "ALTO",
            "Auditar separadamente antes de qualquer alteracao",
        )

    if area == "Banco/dados/pipeline - fora do escopo visual":
        return (
            "FORA_ESCOPO_VISUAL",
            "ALTO",
            "Nao misturar com refactor visual; abrir auditoria propria se necessario",
        )

    if area == "Decisoes":
        return (
            "EQUIVALENCIA_PARCIAL_OPERACIONAL",
            "MEDIO",
            "Cruzar arquivos canonicos e modernos; validar smoke manual da area",
        )

    if area == "Terminal VWAP":
        return (
            "FORA_ESCOPO_BRANCH_ATUAL",
            "ALTO",
            "Abrir auditoria propria antes de qualquer refactor",
        )

    if area == "Payoff curve":
        return (
            "FORA_ESCOPO_BRANCH_ATUAL",
            "ALTO",
            "Abrir auditoria propria de fluxo, colmap e renderizacao",
        )

    if area == "UIDataModel":
        return (
            "FORA_ESCOPO_BRANCH_ATUAL",
            "ALTO",
            "Mapear consumidores e contratos antes de alterar",
        )

    if area == "Tema dark / UI moderna":
        return (
            "PENDENTE_CLASSIFICACAO_FINA",
            "MEDIO",
            "Identificar se o arquivo pertence a UI moderna/dark ou suporte visual",
        )

    if area == "Navegacao / abas / layout":
        return (
            "PENDENTE_SMOKE_MANUAL",
            "MEDIO",
            "Criar roteiro de navegacao entre abas antes de declarar equivalencia",
        )

    if area == "Estados / mensagens / feedback":
        return (
            "PENDENTE_CHECKLIST_ESTADOS",
            "MEDIO",
            "Validar estados vazios, erro, selecao invalida e mensagens",
        )

    return (
        "PENDENTE_CLASSIFICACAO_FINA",
        "BAIXO",
        "Classificar manualmente contra UI canonica",
    )

def evidencia(area: str, entrypoint: bool):
    if entrypoint:
        return "Sinais estaticos de entrypoint"
    if area == "Banco/dados/pipeline - fora do escopo visual":
        return "Sinais de dados/services/repositories/pipeline"
    return "Varredura estatica de caminho e conteudo"

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

    tem_sinal_ui = (
        any(s in caminho_lower for s in sinais_ui)
        or tem_regex(texto, bibliotecas_ui)
        or tem_regex(texto, [
            r"\bPanel\b",
            r"\bTab\b",
            r"\bWidget\b",
            r"\bDialog\b",
            r"\bWindow\b",
            r"\bView\b",
            r"\bScreen\b",
        ])
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

linhas_matriz = []
resumo_area = defaultdict(int)
resumo_status = defaultdict(int)
resumo_risco = defaultdict(int)

for item in arquivos:
    for area in item["areas"]:
        status, risco, acao = status_risco_acao(area, item["entrypoint"])
        ev = evidencia(area, item["entrypoint"])

        linhas_matriz.append({
            "area": area,
            "path": item["path"],
            "linhas": item["linhas"],
            "status": status,
            "risco": risco,
            "evidencia": ev,
            "acao": acao,
        })

        resumo_area[area] += 1
        resumo_status[status] += 1
        resumo_risco[risco] += 1

linhas_matriz.sort(key=lambda x: (
    areas_ordenadas.index(x["area"]) if x["area"] in areas_ordenadas else 999,
    x["path"],
))

def esc(valor):
    return str(valor).replace("|", "/").replace("\n", " ").strip()

def tabela_resumo(dados, titulo_chave):
    if not dados:
        return "_Nenhum dado._\n"

    out = [
        f"| {titulo_chave} | Quantidade |",
        "|---|---:|",
    ]

    for chave in sorted(dados):
        out.append(f"| {esc(chave)} | {dados[chave]} |")

    return "\n".join(out) + "\n"

def tabela_matriz(lista):
    if not lista:
        return "_Nenhuma linha identificada._\n"

    out = [
        "| Area | Arquivo | Linhas | Status inicial | Risco | Evidencia | Proxima acao |",
        "|---|---|---:|---|---|---|---|",
    ]

    for row in lista:
        out.append(
            f"| {esc(row['area'])} "
            f"| `{esc(row['path'])}` "
            f"| {row['linhas']} "
            f"| {esc(row['status'])} "
            f"| {esc(row['risco'])} "
            f"| {esc(row['evidencia'])} "
            f"| {esc(row['acao'])} |"
        )

    return "\n".join(out) + "\n"

conteudo = f"""# Matriz Cruzada de Areas da UI

Data: {data_atual}

Branch: {branch}

## Objetivo

Este documento cruza areas da UI com arquivos candidatos, status inicial, risco, evidencia e proxima acao.

Documentos relacionados:

- `docs/MATRIZ_EQUIVALENCIA_UI.md`
- `docs/INVENTARIO_ARQUIVOS_UI.md`
- `docs/CLASSIFICACAO_AREAS_UI.md`

## Escopo desta fatia

Esta etapa e somente diagnostica/documental.

Nao altera comportamento.

Nao altera banco.

Nao altera services, repositories ou regra de negocio.

Nao altera entrypoint principal.

Nao declara equivalencia completa de nenhuma area.

## Regras aplicadas

1. Possiveis entrypoints sao classificados como `PRESERVAR_ENTRYPOINT`.
2. Banco, dados, services, repositories e pipeline sao classificados como `FORA_ESCOPO_VISUAL`.
3. Decisoes permanece como `EQUIVALENCIA_PARCIAL_OPERACIONAL`.
4. Terminal VWAP permanece fora do escopo da branch atual.
5. Payoff curve permanece fora do escopo da branch atual.
6. UIDataModel permanece fora do escopo da branch atual.
7. Demais areas exigem classificacao fina e smoke manual antes de equivalencia.

## Resumo por area

{tabela_resumo(resumo_area, "Area")}

## Resumo por status

{tabela_resumo(resumo_status, "Status")}

## Resumo por risco

{tabela_resumo(resumo_risco, "Risco")}

## Matriz cruzada

{tabela_matriz(linhas_matriz)}

## Leitura operacional

A matriz cruzada mostra que ha sobreposicao entre areas.

Um mesmo arquivo pode aparecer em mais de uma area quando contem sinais de multiplos fluxos.

Essa sobreposicao nao autoriza refactor conjunto.

Cada alteracao futura deve escolher uma fatia pequena e preservar as demais areas.

## Decisao operacional

A branch atual continua adequada para documentar e estabilizar a frente de Decisoes.

As areas abaixo continuam protegidas contra alteracao nesta branch:

- Terminal VWAP;
- Payoff curve;
- UIDataModel;
- banco/dados/pipeline;
- possiveis entrypoints.

## Proxima fatia recomendada

Criar checklist de smoke manual para a area Decisoes, usando os arquivos classificados como candidatos e preservando entrypoints.

Esse checklist deve cobrir:

- abertura da tela;
- estados vazios;
- selecao invalida;
- carregamento com dados;
- mensagens de status;
- comparacao com UI canonica;
- rollback simples.
"""

saida.write_text(conteudo, encoding="utf-8", newline="\n")

print(f"Gerado: {saida}")
print(f"Arquivos candidatos: {len(arquivos)}")
print(f"Linhas da matriz cruzada: {len(linhas_matriz)}")
print("Resumo por risco:")
for chave in sorted(resumo_risco):
    print(f"  {chave}: {resumo_risco[chave]}")
PY

MARKER_DEV="Referencia matriz cruzada de areas UI"

if ! grep -q "$MARKER_DEV" "$DEV_DOC"; then
  cat >> "$DEV_DOC" <<EOF_DEV

---

## $MARKER_DEV

Data: $DATA_ATUAL

Foi criada a matriz cruzada de areas da UI:

    docs/MATRIZ_CRUZADA_AREAS_UI.md

A matriz cruza:

- area;
- arquivo;
- status inicial;
- risco;
- evidencia;
- proxima acao.

Regra operacional:

A matriz cruzada nao autoriza alteracao conjunta de areas. Cada proxima fatia deve escolher um escopo pequeno e preservar entrypoints, banco, dados, services, repositories e pipeline.

EOF_DEV
  echo "Atualizado: $DEV_DOC"
else
  echo "Marcador ja existe em $DEV_DOC"
fi

MARKER_MATRIZ="Referencia matriz cruzada de areas UI"

if ! grep -q "$MARKER_MATRIZ" "$MATRIZ_DOC"; then
  cat >> "$MATRIZ_DOC" <<EOF_MATRIZ

---

## $MARKER_MATRIZ

Data: $DATA_ATUAL

Foi criada a matriz cruzada de areas da UI:

    docs/MATRIZ_CRUZADA_AREAS_UI.md

A matriz cruzada passa a orientar a escolha das proximas fatias pequenas por risco, area e status.

Esta matriz ainda nao declara equivalencia completa de nenhuma area.

EOF_MATRIZ
  echo "Atualizado: $MATRIZ_DOC"
else
  echo "Marcador ja existe em $MATRIZ_DOC"
fi

MARKER_AUDIT="Checkpoint matriz cruzada de areas UI"

if ! grep -q "$MARKER_AUDIT" "$AUDIT_DOC"; then
  cat >> "$AUDIT_DOC" <<EOF_AUDIT

---

## $MARKER_AUDIT

Data: $DATA_ATUAL

Branch: $BRANCH_ATUAL

Foi criada a matriz cruzada de areas da UI:

    docs/MATRIZ_CRUZADA_AREAS_UI.md

### Decisao

Este checkpoint permanece documental/diagnostico.

Nao houve alteracao de banco, regra de negocio, services, repositories ou entrypoint principal.

### Areas protegidas

- Terminal VWAP;
- payoff curve;
- UIDataModel;
- banco/dados/pipeline;
- possiveis entrypoints.

### Proxima fatia recomendada

Criar checklist de smoke manual para Decisoes, sem alterar codigo de runtime.

EOF_AUDIT
  echo "Atualizado: $AUDIT_DOC"
else
  echo "Marcador ja existe em $AUDIT_DOC"
fi

python - <<'PY'
from pathlib import Path

arquivos = [
    Path("docs/MATRIZ_CRUZADA_AREAS_UI.md"),
    Path("docs/MATRIZ_EQUIVALENCIA_UI.md"),
    Path("docs/DESENVOLVIMENTO_UI.md"),
    Path("reports/auditoria/AUDITORIA_REFACTOR_UI.md"),
    Path("scripts/cruzar_matriz_areas_ui.sh"),
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

echo "== Fim da matriz cruzada =="
