"""
patch_32 -- Auditoria de wiring da UI

Objetivo:
  Mapear exatamente o que cada componente/modelo da UI
  importa e de onde lê dados hoje.

  Responde:
    - A UI ainda lê rtd_* (legado)?
    - A UI já consome StructuresRepository?
    - A UI já consome DerivedRepo / derived.db?
    - Há imports quebrados após o fix do __init__.py?

DECISÃO PERMANENTE [patch_32:aba_alias_readonly] -- 2026-06-01
  'aba' removido de LEGACY_TERMS. get_abas() é alias readonly de
  get_structure_ids() em ui_data.py -- não é acoplamento legado.
  ALIAS_READONLY_TERMS criado para rastrear sem gerar alerta MISTO.
  Não reverter. Não reabrir.

Execução:
  python ATT/patches/patch_32_audit_ui_wiring.py
"""

import sys
import ast
import json
from pathlib import Path
from datetime import datetime

#  Paths 
RAIZ      = Path(__file__).resolve().parent.parent.parent
UI_DIR    = RAIZ / "UI"
BAK_DIR   = RAIZ / "BAK"
DOCS_DIR  = RAIZ / "docs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

#  Termos que indicam acoplamento LEGADO 
# NOTA: 'aba' foi removido intencionalmente -- ver DECISÃO PERMANENTE no topo.
LEGACY_TERMS = [
    "rtd_analise_robo",
    "rtd_analise_robo_legs",
    "manual_analise_robo_legs",
    "read_structure_legs",
    "read_structure_summary",
    "derived_service",
    "robo_legs_service",
    "robo_legs_repository",
]

#  Termos alias readonly -- rastreados sem gerar alerta LEGADO 
# DECISÃO PERMANENTE patch_32:aba_alias_readonly (2026-06-01)
# Presença aceita e intencional. NÃO migrar. NÃO alertar.
ALIAS_READONLY_TERMS = [
    "get_abas",   # alias de get_structure_ids() em ui_data.py
    "aba",        # campo de leitura retrocompatível -- NÃO é chave de filtro SQL
]

#  Termos canônicos 
CANONICAL_TERMS = [
    "StructuresRepository",
    "structures_repository",
    "DerivedRepo",
    "derived_repo",
    "PricingExecutionAppService",
    "canonical_input_service",
    "market_snapshot_selector",
    "structure_id",
]

DERIVED_DB_TERMS = [
    "derived.db",
    "payoff_curve_points",
    "payoff_curve_summary",
    "structure_decisions",
]


#  Coleta arquivos Python da UI 
def coletar_arquivos_ui() -> list[Path]:
    return sorted(UI_DIR.rglob("*.py"))


#  Extrai imports e chamadas de um arquivo 
def analisar_arquivo(path: Path) -> dict:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"arquivo": str(path.relative_to(RAIZ)), "erro": str(e)}

    resultado = {
        "arquivo":        str(path.relative_to(RAIZ)),
        "imports":        [],
        "legado":         [],
        "canonico":       [],
        "derived_db":     [],
        "alias_readonly": [],   # rastreado sem gerar alerta LEGADO
        "linhas_totais":  source.count("\n"),
    }

    # imports via AST
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    resultado["imports"].append(node.module)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        resultado["imports"].append(alias.name)
    except SyntaxError:
        resultado["imports"].append("(erro de sintaxe -- AST falhou)")

    # varredura textual por termos
    linhas = source.splitlines()
    for i, linha in enumerate(linhas, 1):
        for termo in LEGACY_TERMS:
            if termo in linha:
                resultado["legado"].append({
                    "termo":  termo,
                    "linha":  i,
                    "trecho": linha.strip()[:120],
                })
        for termo in CANONICAL_TERMS:
            if termo in linha:
                resultado["canonico"].append({
                    "termo":  termo,
                    "linha":  i,
                    "trecho": linha.strip()[:120],
                })
        for termo in DERIVED_DB_TERMS:
            if termo in linha:
                resultado["derived_db"].append({
                    "termo":  termo,
                    "linha":  i,
                    "trecho": linha.strip()[:120],
                })
        #  alias readonly: rastreia sem alertar 
        for termo in ALIAS_READONLY_TERMS:
            if termo in linha:
                resultado["alias_readonly"].append({
                    "termo":  termo,
                    "linha":  i,
                    "trecho": linha.strip()[:120],
                })

    return resultado


#  Classifica wiring de cada arquivo 
def classificar(analise: dict) -> str:
    tem_legado   = len(analise.get("legado", [])) > 0
    tem_canonico = len(analise.get("canonico", [])) > 0
    tem_derived  = len(analise.get("derived_db", [])) > 0
    # alias_readonly NÃO entra no cálculo de classificação

    if tem_legado and not tem_canonico:
        return "LEGADO_PURO"
    if tem_legado and tem_canonico:
        return "MISTO"
    if tem_canonico or tem_derived:
        return "CANONICO"
    return "NEUTRO"


#  Gera relatório Markdown 
def gerar_markdown(resultados: list[dict]) -> str:
    linhas = [
        "# Auditoria de Wiring da UI -- patch_32",
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "> **DECISÃO PERMANENTE** `patch_32:aba_alias_readonly` -- "
        "`aba` removido de LEGACY_TERMS. "
        "`get_abas()` é alias readonly de `get_structure_ids()`. "
        "Não é legado. Não reabrir.",
        "",
        "## Resumo por arquivo",
        "",
        "| Arquivo | Classificação | Legado | Canônico | Derived DB | Alias Readonly |",
        "|---------|--------------|--------|----------|------------|----------------|",
    ]

    for r in resultados:
        if "erro" in r:
            linhas.append(f"| {r['arquivo']} | ERRO | - | - | - | - |")
            continue
        cls   = classificar(r)
        emoji = {
            "LEGADO_PURO": "[ERRO]",
            "MISTO":       "[PARCIAL]",
            "CANONICO":    "[OK]",
            "NEUTRO":      "",
        }.get(cls, "")

        linhas.append(
            f"| `{r['arquivo']}` | {emoji} {cls} "
            f"| {len(r['legado'])} | {len(r['canonico'])} "
            f"| {len(r['derived_db'])} | {len(r['alias_readonly'])} |"
        )

    # Detalhes por arquivo
    linhas += ["", "---", "", "## Detalhes por arquivo", ""]

    for r in resultados:
        if "erro" in r:
            continue
        cls = classificar(r)
        if cls == "NEUTRO" and not r.get("alias_readonly"):
            continue

        linhas.append(f"### `{r['arquivo']}` -- {cls}")
        linhas.append("")

        if r["imports"]:
            linhas.append("**Imports detectados:**")
            for imp in sorted(set(r["imports"])):
                linhas.append(f"- `{imp}`")
            linhas.append("")

        if r["legado"]:
            linhas.append("**[AVISO] Acoplamentos LEGADO:**")
            for oc in r["legado"]:
                linhas.append(
                    f"- L{oc['linha']} `{oc['termo']}`  `{oc['trecho']}`"
                )
            linhas.append("")

        if r["canonico"]:
            linhas.append("**[OK] Referências CANÔNICAS:**")
            for oc in r["canonico"]:
                linhas.append(
                    f"- L{oc['linha']} `{oc['termo']}`  `{oc['trecho']}`"
                )
            linhas.append("")

        if r["derived_db"]:
            linhas.append("**[PACOTE] Referências derived.db:**")
            for oc in r["derived_db"]:
                linhas.append(
                    f"- L{oc['linha']} `{oc['termo']}`  `{oc['trecho']}`"
                )
            linhas.append("")

        if r.get("alias_readonly"):
            linhas.append(
                "**[INFO] Alias readonly (aceito -- DECISÃO PERMANENTE -- não migrar):**"
            )
            for oc in r["alias_readonly"]:
                linhas.append(
                    f"- L{oc['linha']} `{oc['termo']}`  `{oc['trecho']}`"
                )
            linhas.append("")

    # Sumário final
    contagem = {"LEGADO_PURO": 0, "MISTO": 0, "CANONICO": 0, "NEUTRO": 0}
    for r in resultados:
        if "erro" not in r:
            contagem[classificar(r)] += 1

    linhas += [
        "---",
        "",
        "## Sumário final",
        "",
        f"- [ERRO] LEGADO_PURO : {contagem['LEGADO_PURO']} arquivo(s)",
        f"- [PARCIAL] MISTO       : {contagem['MISTO']} arquivo(s)",
        f"- [OK] CANÔNICO    : {contagem['CANONICO']} arquivo(s)",
        f"-  NEUTRO      : {contagem['NEUTRO']} arquivo(s)",
        "",
        "### Ação recomendada",
        "- LEGADO_PURO  migrar para domínio canônico",
        "- MISTO        avaliar caso a caso; priorizar remoção do legado",
        "- CANÔNICO     manter; validar no smoke",
        "- Alias readonly  nenhuma ação necessária (decisão permanente registrada)",
        "",
    ]

    return "\n".join(linhas)


#  Main 
def run():
    print("=" * 60)
    print("  patch_32 -- Auditoria wiring UI")
    print(f"  Raiz : {RAIZ}")
    print("=" * 60)

    arquivos = coletar_arquivos_ui()
    print(f"\n  Arquivos encontrados em UI/: {len(arquivos)}")

    resultados = []
    for arq in arquivos:
        analise = analisar_arquivo(arq)
        cls     = classificar(analise) if "erro" not in analise else "ERRO"
        emoji   = {"LEGADO_PURO": "[ERRO]", "MISTO": "[PARCIAL]",
                   "CANONICO": "[OK]", "NEUTRO": ""}.get(cls, "")
        print(f"  {emoji}  {analise['arquivo']}  [{cls}]")
        resultados.append(analise)

    # Salva JSON bruto em BAK
    BAK_DIR.mkdir(exist_ok=True)
    json_path = BAK_DIR / f"patch_32_ui_wiring_{TIMESTAMP}.json"
    json_path.write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"\n  [SAVE]  JSON bruto salvo: {json_path.relative_to(RAIZ)}")

    # Salva Markdown em docs/
    DOCS_DIR.mkdir(exist_ok=True)
    md_path    = DOCS_DIR / "audit_ui_wiring_patch32.md"
    md_content = gerar_markdown(resultados)
    md_path.write_text(md_content, encoding="utf-8")
    print(f"  [ARQUIVO]  Relatório salvo : {md_path.relative_to(RAIZ)}")

    # Sumário no terminal
    contagem = {"LEGADO_PURO": 0, "MISTO": 0, "CANONICO": 0, "NEUTRO": 0}
    for r in resultados:
        if "erro" not in r:
            contagem[classificar(r)] += 1

    print("\n" + "=" * 60)
    print("  SUMÁRIO")
    print(f"  [ERRO] LEGADO_PURO : {contagem['LEGADO_PURO']}")
    print(f"  [PARCIAL] MISTO       : {contagem['MISTO']}")
    print(f"  [OK] CANÔNICO    : {contagem['CANONICO']}")
    print(f"   NEUTRO      : {contagem['NEUTRO']}")
    print("=" * 60)

    if contagem["LEGADO_PURO"] > 0:
        print(
            f"\n  [AVISO]  {contagem['LEGADO_PURO']} arquivo(s) LEGADO_PURO "
            "-- wiring canônico necessário"
        )
        return 1

    print("\n  [OK]  UI sem acoplamentos LEGADO_PURO detectados")
    return 0


if __name__ == "__main__":
    sys.exit(run())
