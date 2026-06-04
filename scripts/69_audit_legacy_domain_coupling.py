#!/usr/bin/env python3
"""
scripts/69_audit_legacy_domain_coupling.py

Patch 24 -- Auditoria de acoplamento legado nos módulos de domínio.

Objetivo:
  Varrer os módulos domain/ e reportar, de forma estruturada, todos os pontos
  de acoplamento com o modelo legado (aba, timestamp, rtd_analise_robo, etc.),
  classificando-os por severidade e sugerindo o caminho de desacoplamento.

Saída:
  - Relatório em texto no stdout
  - JSON estruturado em dados/audit_domain_coupling_patch24.json

Uso:
  python scripts/69_audit_legacy_domain_coupling.py
"""

import ast
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

#  Configuração 

DOMAIN_DIR = Path("domain")
OUTPUT_JSON = Path("dados/audit_domain_coupling_patch24.json")

# Termos legados a serem detectados
LEGACY_TERMS = {
    "aba":                ("CRÍTICO",  "Referência direta ao identificador legado 'aba'"),
    "rtd_analise_robo":   ("CRÍTICO",  "Query direta na tabela legada rtd_analise_robo"),
    "manual_analise":     ("CRÍTICO",  "Query direta na tabela legada manual_analise"),
    "read_structure_summary": ("CRÍTICO", "Função legada de leitura do banco RTD"),
    "compute_payoff_for_aba": ("CRÍTICO", "Função legada de cálculo de payoff por aba"),
    "get_app_db_connection":  ("CRÍTICO", "Conexão direta ao banco de dados da aplicação legada"),
    "timestamp":          ("MODERADO", "Campo timestamp com semântica legada como chave de upsert"),
    "ON CONFLICT(timestamp, aba)": ("MODERADO", "Chave composta legada no banco derivado"),
    "legacy_timestamp":   ("BAIXO",    "Campo de rastreabilidade legado (aceitável como metadata)"),
    "legacy aba":         ("BAIXO",    "Comentário/string descrevendo caminho legado"),
}

# Funções/classes canônicas -- servem como referência positiva no relatório
CANONICAL_MARKERS = {
    "compute_payoff_from_canonical_input",
    "compute_decision_from_contract",
    "compute_decision_from_payoff",
    "compute_decision_from_inputs",
    "CanonicalStructureMarketInput",
}


#  Dataclasses de resultado 

@dataclass
class CouplingOccurrence:
    file        : str
    line        : int
    term        : str
    severity    : str
    description : str
    snippet     : str


@dataclass
class FileAuditResult:
    file                : str
    total_occurrences   : int
    critical            : int
    moderate            : int
    low                 : int
    canonical_markers   : list[str]
    occurrences         : list[CouplingOccurrence] = field(default_factory=list)


@dataclass
class AuditReport:
    patch               : str = "patch_24"
    description         : str = "Auditoria de acoplamento legado nos módulos domain/"
    total_critical      : int = 0
    total_moderate      : int = 0
    total_low           : int = 0
    files               : list[FileAuditResult] = field(default_factory=list)
    summary             : list[str] = field(default_factory=list)
    recommendations     : list[str] = field(default_factory=list)


#  Engine de varredura 

def _audit_file(path: Path) -> FileAuditResult:
    """Varre um arquivo .py e retorna os acoplamentos encontrados."""
    lines = path.read_text(encoding="utf-8").splitlines()
    occurrences: list[CouplingOccurrence] = []

    # Detecta marcadores canônicos presentes no arquivo
    found_canonical: list[str] = []
    for marker in CANONICAL_MARKERS:
        if any(marker in line for line in lines):
            found_canonical.append(marker)

    # Varre linha a linha pelos termos legados
    for lineno, raw_line in enumerate(lines, start=1):
        for term, (severity, description) in LEGACY_TERMS.items():
            if term in raw_line:
                # Evita contar linhas que são apenas comentários de documentação
                # se o termo for de baixa severidade
                stripped = raw_line.strip()
                is_comment = stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''")

                # Termos críticos são reportados mesmo em comentários
                # (indicam que o path foi pelo menos cogitado)
                if is_comment and severity == "BAIXO":
                    continue

                occurrences.append(CouplingOccurrence(
                    file        = str(path),
                    line        = lineno,
                    term        = term,
                    severity    = severity,
                    description = description,
                    snippet     = raw_line.rstrip(),
                ))

    # Deduplica por (linha, term) -- uma linha pode conter múltiplos matches
    seen: set[tuple[int, str]] = set()
    unique: list[CouplingOccurrence] = []
    for occ in occurrences:
        key = (occ.line, occ.term)
        if key not in seen:
            seen.add(key)
            unique.append(occ)

    critical  = sum(1 for o in unique if o.severity == "CRÍTICO")
    moderate  = sum(1 for o in unique if o.severity == "MODERADO")
    low       = sum(1 for o in unique if o.severity == "BAIXO")

    return FileAuditResult(
        file              = str(path),
        total_occurrences = len(unique),
        critical          = critical,
        moderate          = moderate,
        low               = low,
        canonical_markers = found_canonical,
        occurrences       = unique,
    )


def _build_recommendations(report: AuditReport) -> list[str]:
    recs: list[str] = []

    # Analisa por arquivo
    for fr in report.files:
        fname = Path(fr.file).name

        if fname == "decision.py" and fr.critical > 0:
            recs.append(
                "decision.py  Remover compute_decision_for_aba() inteiramente. "
                "O __main__ com get_app_db_connection + query rtd_analise_robo "
                "deve ser excluído ou substituído por script autônomo em scripts/."
            )
        if fname == "payoff_features.py" and fr.moderate > 0:
            recs.append(
                "payoff_features.py  Migrar chave de upsert de (timestamp, aba) "
                "para (structure_id, reference_date). Manter aba como coluna "
                "opcional de rastreabilidade, sem participar da constraint UNIQUE."
            )
        if fname == "market_snapshot.py":
            recs.append(
                "market_snapshot.py  Campo 'aba: str' permanece aceitável como "
                "identificador de snapshot ao vivo (UI/RTD). Não requer remoção -- "
                "apenas garantir que não é usado como FK para o banco canônico."
            )

    # Recomendações gerais
    if report.total_critical > 0:
        recs.append(
            "GERAL  Nenhuma função de domain/ deve importar ou chamar "
            "funções com sufixo '_for_aba'. Todo caminho de decisão e payoff "
            "deve passar por compute_*_from_canonical_input / compute_*_from_contract."
        )
    recs.append(
        "GERAL  Após aplicar as correções acima, re-executar este script "
        "para confirmar total_critical == 0 antes de merge na branch main."
    )

    return recs


def run_audit() -> AuditReport:
    report = AuditReport()

    py_files = sorted(DOMAIN_DIR.glob("*.py"))
    if not py_files:
        print(f"[ERRO] Nenhum .py encontrado em {DOMAIN_DIR.resolve()}", file=sys.stderr)
        sys.exit(1)

    for path in py_files:
        result = _audit_file(path)
        if result.total_occurrences > 0 or result.canonical_markers:
            report.files.append(result)
            report.total_critical += result.critical
            report.total_moderate += result.moderate
            report.total_low      += result.low

    report.recommendations = _build_recommendations(report)

    # Sumário executivo
    report.summary = [
        f"Arquivos auditados : {len(py_files)}",
        f"Arquivos com ocorrências : {len(report.files)}",
        f"Ocorrências CRÍTICAS  : {report.total_critical}",
        f"Ocorrências MODERADAS : {report.total_moderate}",
        f"Ocorrências BAIXAS    : {report.total_low}",
        f"Status geral : {'[AVISO]  REQUER AÇÃO' if report.total_critical > 0 else '[OK] LIMPO'}",
    ]

    return report


#  Renderização 

SEV_ICON = {"CRÍTICO": "[ERRO]", "MODERADO": "[PARCIAL]", "BAIXO": "[INFO]"}

SEPARATOR = "" * 78


def _print_report(report: AuditReport) -> None:
    print(f"\n{''*78}")
    print(f"  PATCH 24 -- Auditoria de Acoplamento Legado . domain/")
    print(f"{''*78}\n")

    print("SUMÁRIO EXECUTIVO")
    print(SEPARATOR)
    for line in report.summary:
        print(f"  {line}")
    print()

    for fr in report.files:
        fname = Path(fr.file).name
        print(SEPARATOR)
        print(f"  [ARQUIVO] {fname}  |  "
              f"[ERRO] {fr.critical}  [PARCIAL] {fr.moderate}  [INFO] {fr.low}  "
              f"total={fr.total_occurrences}")

        if fr.canonical_markers:
            print(f"  [OK] Marcadores canônicos: {', '.join(fr.canonical_markers)}")

        if fr.occurrences:
            print()
            for occ in fr.occurrences:
                icon = SEV_ICON.get(occ.severity, "")
                print(f"  {icon} L{occ.line:>4}  [{occ.severity:<8}]  term='{occ.term}'")
                print(f"          {occ.snippet.strip()}")
        print()

    print(SEPARATOR)
    print("  RECOMENDAÇÕES DE DESACOPLAMENTO")
    print(SEPARATOR)
    for i, rec in enumerate(report.recommendations, start=1):
        # Quebra linha para leitura confortável no terminal
        words = rec.split()
        lines_out: list[str] = []
        current = f"  {i}. "
        indent  = "     "
        for word in words:
            if len(current) + len(word) + 1 > 78:
                lines_out.append(current)
                current = indent + word
            else:
                current += ("" if current.endswith(". ") or current == indent else " ") + word
        lines_out.append(current)
        print("\n".join(lines_out))
        print()

    print(f"{''*78}\n")


def _save_json(report: AuditReport) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    def _serialize(obj):
        if hasattr(obj, "__dataclass_fields__"):
            return asdict(obj)
        return str(obj)

    data = asdict(report)
    OUTPUT_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=_serialize),
        encoding="utf-8",
    )
    print(f"  [DIR] JSON salvo em: {OUTPUT_JSON.resolve()}\n")


#  Entry-point 

def main() -> None:
    report = run_audit()
    _print_report(report)
    _save_json(report)

    # Exit code não-zero se houver críticos (útil para CI)
    sys.exit(1 if report.total_critical > 0 else 0)


if __name__ == "__main__":
    main()
