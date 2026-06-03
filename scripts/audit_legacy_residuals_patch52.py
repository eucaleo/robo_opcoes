# scripts/audit_legacy_residuals_patch52.py
"""
patch_52 — Auditoria de residuos ativos do legado (baseline fase 7)

Varre services/, repositories/, domain/ em busca de uso de 'aba'
que nao seja alias_legacy_aba ou wrapper de compatibilidade controlada.

Classifica cada ocorrencia:
  alias_ok          — uso de alias_legacy_aba (esperado, nao e residuo)
  bridge_controlado — wrapper/fallback documentado explicitamente
  residuo_ativo     — uso de 'aba' como dado operacional real (alvo de remocao)

Saidas:
  ATT/reports/legacy_residuals_patch52.md
  ATT/reports/legacy_residuals_patch52.json
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCAN_DIRS = [
    "services",
    "repositories",
    "domain",
    "db",
    "api",
    "UI",
]

REPORTS_DIR = PROJECT_ROOT / "ATT" / "reports"

# Padroes que caracterizam residuo ativo
# ORDEM IMPORTA — loop para no primeiro match por linha.
# Padroes mais especificos devem vir antes dos mais genericos.
RESIDUO_PATTERNS = [
    # assinatura de funcao com parametro 'aba'
    (r"def\s+\w+\s*\([^)]*\baba\b[^)]*\)", "param_aba_em_assinatura"),
    # filtragem SQL
    (r"WHERE\s+aba\s*=",                    "sql_where_aba"),
    (r"AND\s+aba\s*=",                      "sql_and_aba"),
    # get_legs chamado com aba como primeiro arg posicional ou kwarg
    (r"get_legs\s*\(\s*aba",               "get_legs_com_aba"),
    (r"read_structure_legs\s*\(",           "read_structure_legs_direto"),
    (r"read_structure_summary\s*\(",        "read_structure_summary_direto"),
    # kwarg aba='...' ou aba="..." ou aba=variavel  — MAIS ESPECIFICO que comparacao_aba
    # deve vir antes de comparacao_aba para que o break pare aqui primeiro
    (r"\baba\s*=\s*(?!None\b)['\"\w]",     "kwarg_aba"),
    # comparacao generica aba = / aba != / aba < etc  — MENOS ESPECIFICO, vem por ultimo
    (r'(?<!alias_legacy_)\baba\b\s*[=!<>]', "comparacao_aba"),
]

# Padroes que indicam uso controlado/esperado (nao sao residuos)
ALIAS_OK_PATTERNS = [
    r"alias_legacy_aba",
    r"get_abas\s*\(\s*\)",
    r"ALIAS_READONLY_TERMS",
    r"#\s*BRIDGE LEGADO",
    r"#\s*wrapper de compatibilidade",
    r"#\s*alias readonly",
    r"@unittest\.skip",
]

# Arquivos que sao explicitamente ponte/bridge (bridge_controlado por definicao)
BRIDGE_FILES = {
    "services/legacy_robo_legs_fallback.py",
    "services/canonical_input_service.py",
    "repositories/robo_legs_repository.py",
    "repositories/robo_legs_status_repository.py",
    "services/robo_legs_service.py",
    "services/derived_service.py",
}


# ---------------------------------------------------------------------------
# Estruturas de dados
# ---------------------------------------------------------------------------

@dataclass
class Ocorrencia:
    arquivo: str
    linha: int
    conteudo: str
    padrao: str
    classificacao: str  # alias_ok | bridge_controlado | residuo_ativo


@dataclass
class RelatorioArquivo:
    arquivo: str
    total_ocorrencias: int
    residuos_ativos: int
    bridge_controlado: int
    alias_ok: int
    ocorrencias: list = field(default_factory=list)


@dataclass
class Relatorio:
    gerado_em: str
    raiz: str
    total_arquivos_varridos: int
    total_ocorrencias: int
    total_residuos_ativos: int
    total_bridge_controlado: int
    total_alias_ok: int
    arquivos: list = field(default_factory=list)
    residuos_por_arquivo: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Classificacao
# ---------------------------------------------------------------------------

def _linha_tem_alias_ok(linha: str) -> bool:
    for p in ALIAS_OK_PATTERNS:
        if re.search(p, linha):
            return True
    return False


def _classificar(arquivo_rel: str, linha: str, padrao: str) -> str:
    if _linha_tem_alias_ok(linha):
        return "alias_ok"
    if arquivo_rel in BRIDGE_FILES:
        return "bridge_controlado"
    return "residuo_ativo"


# ---------------------------------------------------------------------------
# Varredura
# ---------------------------------------------------------------------------

def _varrer_arquivo(caminho: Path, raiz: Path) -> list[Ocorrencia]:
    arquivo_rel = str(caminho.relative_to(raiz)).replace("\\", "/")
    ocorrencias = []

    try:
        linhas = caminho.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return ocorrencias

    for num, linha in enumerate(linhas, start=1):
        linha_strip = linha.strip()

        # ignora comentarios puros e linhas vazias
        if not linha_strip or linha_strip.startswith("#"):
            continue

        for padrao_re, nome_padrao in RESIDUO_PATTERNS:
            if re.search(padrao_re, linha, re.IGNORECASE):
                classificacao = _classificar(arquivo_rel, linha, nome_padrao)
                ocorrencias.append(Ocorrencia(
                    arquivo=arquivo_rel,
                    linha=num,
                    conteudo=linha.rstrip(),
                    padrao=nome_padrao,
                    classificacao=classificacao,
                ))
                break  # uma ocorrencia por linha — para no padrao mais especifico

    return ocorrencias


def varrer_projeto(raiz: Path) -> list[Ocorrencia]:
    todas = []
    for dir_rel in SCAN_DIRS:
        dir_abs = raiz / dir_rel
        if not dir_abs.exists():
            continue
        for py in sorted(dir_abs.rglob("*.py")):
            todas.extend(_varrer_arquivo(py, raiz))
    return todas


# ---------------------------------------------------------------------------
# Construcao do relatorio
# ---------------------------------------------------------------------------

def construir_relatorio(ocorrencias: list[Ocorrencia], raiz: Path) -> Relatorio:
    agrupado: dict[str, list[Ocorrencia]] = {}
    for oc in ocorrencias:
        agrupado.setdefault(oc.arquivo, []).append(oc)

    rel = Relatorio(
        gerado_em=datetime.now().isoformat(timespec="seconds"),
        raiz=str(raiz),
        total_arquivos_varridos=sum(
            1 for d in SCAN_DIRS
            for _ in (raiz / d).rglob("*.py")
            if (raiz / d).exists()
        ),
        total_ocorrencias=len(ocorrencias),
        total_residuos_ativos=sum(1 for o in ocorrencias if o.classificacao == "residuo_ativo"),
        total_bridge_controlado=sum(1 for o in ocorrencias if o.classificacao == "bridge_controlado"),
        total_alias_ok=sum(1 for o in ocorrencias if o.classificacao == "alias_ok"),
    )

    for arq, ocs in sorted(agrupado.items()):
        ra = RelatorioArquivo(
            arquivo=arq,
            total_ocorrencias=len(ocs),
            residuos_ativos=sum(1 for o in ocs if o.classificacao == "residuo_ativo"),
            bridge_controlado=sum(1 for o in ocs if o.classificacao == "bridge_controlado"),
            alias_ok=sum(1 for o in ocs if o.classificacao == "alias_ok"),
            ocorrencias=[asdict(o) for o in ocs],
        )
        rel.arquivos.append(asdict(ra))

    rel.residuos_por_arquivo = {
        arq: sum(1 for o in ocs if o.classificacao == "residuo_ativo")
        for arq, ocs in agrupado.items()
        if any(o.classificacao == "residuo_ativo" for o in ocs)
    }

    return rel


# ---------------------------------------------------------------------------
# Geracao de saidas
# ---------------------------------------------------------------------------

def gerar_markdown(rel: Relatorio, destino: Path) -> None:
    linhas = [
        "# patch_52 — Relatorio de Residuos Ativos do Legado",
        "",
        f"**Gerado em:** {rel.gerado_em}  ",
        f"**Raiz varrida:** `{rel.raiz}`  ",
        f"**Arquivos varridos:** {rel.total_arquivos_varridos}  ",
        "",
        "## Resumo geral",
        "",
        "| Classificacao       | Quantidade |",
        "|---------------------|------------|",
        f"| residuo_ativo       | {rel.total_residuos_ativos} |",
        f"| bridge_controlado   | {rel.total_bridge_controlado} |",
        f"| alias_ok            | {rel.total_alias_ok} |",
        f"| **total**           | **{rel.total_ocorrencias}** |",
        "",
        "## Residuos ativos por arquivo",
        "",
    ]

    if rel.residuos_por_arquivo:
        linhas += [
            "| Arquivo | Residuos ativos |",
            "|---------|-----------------|",
        ]
        for arq, qtd in sorted(
            rel.residuos_por_arquivo.items(), key=lambda x: -x[1]
        ):
            linhas.append(f"| `{arq}` | {qtd} |")
    else:
        linhas.append("_Nenhum residuo ativo encontrado._")

    linhas += ["", "## Detalhamento por arquivo", ""]

    for bloco in rel.arquivos:
        linhas += [
            f"### `{bloco['arquivo']}`",
            "",
            f"- total: {bloco['total_ocorrencias']}",
            f"- residuo_ativo: {bloco['residuos_ativos']}",
            f"- bridge_controlado: {bloco['bridge_controlado']}",
            f"- alias_ok: {bloco['alias_ok']}",
            "",
            "| Linha | Classificacao | Padrao | Conteudo |",
            "|-------|--------------|--------|----------|",
        ]
        for oc in bloco["ocorrencias"]:
            conteudo = oc["conteudo"].replace("|", "\\|").strip()
            linhas.append(
                f"| {oc['linha']} | `{oc['classificacao']}` "
                f"| `{oc['padrao']}` | `{conteudo}` |"
            )
        linhas.append("")

    linhas += [
        "---",
        "",
        "## Proximos passos",
        "",
        "1. Validar cada `residuo_ativo` listado acima",
        "2. Confirmar quais sao alvo direto do patch_53",
        "3. Executar patch_53 para eliminar o bridge `canonical_input_service`",
        "   substituindo importes dinamicos por injecao explicita",
        "",
        "_Fim do relatorio patch_52_",
    ]

    destino.write_text("\n".join(linhas), encoding="utf-8")


def gerar_json(rel: Relatorio, destino: Path) -> None:
    destino.write_text(
        json.dumps(asdict(rel), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("patch_52 — iniciando varredura de residuos legado...")
    print(f"raiz: {PROJECT_ROOT}")

    ocorrencias = varrer_projeto(PROJECT_ROOT)
    rel = construir_relatorio(ocorrencias, PROJECT_ROOT)

    md_path = REPORTS_DIR / "legacy_residuals_patch52.md"
    json_path = REPORTS_DIR / "legacy_residuals_patch52.json"

    gerar_markdown(rel, md_path)
    gerar_json(rel, json_path)

    print(f"arquivos varridos : {rel.total_arquivos_varridos}")
    print(f"residuos_ativos   : {rel.total_residuos_ativos}")
    print(f"bridge_controlado : {rel.total_bridge_controlado}")
    print(f"alias_ok          : {rel.total_alias_ok}")
    print(f"relatorio md      : {md_path}")
    print(f"relatorio json    : {json_path}")

    return 0 if rel.total_residuos_ativos == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
