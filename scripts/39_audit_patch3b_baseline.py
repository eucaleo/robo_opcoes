"""
scripts/39_audit_patch3b_baseline.py

Auditoria pre-patch_39 — baseline para branch patch/3b
Objetivo:
  1. Mapear residuos de arquivos fora de lugar (raiz, services/, etc.)
  2. Verificar duplicidade dos .sh soltos vs ATT/patches/
  3. Detectar referencias a "aba" como identidade no dominio/services
  4. Verificar se derived_service e domain/payoff ainda leem raw DB direto
  5. Verificar se o fluxo canonico Structure+Snapshot->derived esta fechado
  6. Inspecionar bridge/last_export.txt (residuo ou estado ativo?)
  7. Gerar relatorio em scripts/auditoria_patch39_YYYYMMDD_HHMM.md

Uso:
  python scripts/39_audit_patch3b_baseline.py
"""

import os
import re
import sys
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

REPORT_NAME = (
    f"scripts/auditoria_patch39_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
)

# Arquivos suspeitos confirmados na listagem anterior
SUSPECTED_RESIDUALS = [
    "diagnose_aba_values.sh",
    "diagnose_migration.sh",
    "patch_37_apply.sh",
    "patch_37_fix_residuals.sh",
    "services/Novo Documento de Texto.txt",
    "bridge/last_export.txt",
]

# Diretorios canonicos de scripts e patches
CANONICAL_SCRIPTS_DIR = ROOT / "scripts"
CANONICAL_PATCHES_DIR = ROOT / "ATT" / "patches"

# Modulos criticos para verificacao de acoplamento legado
DOMAIN_FILES_TO_CHECK = [
    "domain/payoff.py",
    "domain/decision.py",
    "services/derived_service.py",
    "services/robo_legs_service.py",
    "services/robo_legs_status_service.py",
    "repositories/robo_legs_repository.py",
    "repositories/robo_legs_status_repository.py",
]

# Padroes que indicam acoplamento legado perigoso
LEGACY_PATTERNS = {
    "aba_como_identidade": [
        r'WHERE\s+aba\s*=',
        r'by_aba\s*\(',
        r'get_legs\s*\(\s*aba',
        r'read_structure_legs\s*\(',
        r'read_structure_summary\s*\(',
        r'"aba"\s*:\s*aba',
        r"'aba'\s*:\s*aba",
        r'filter.*aba.*=',
    ],
    "leitura_raw_db_direto": [
        r'rtd_analise_robo_legs',
        r'rtd_analise_robo\b',
        r'manual_analise_robo_legs',
        r'FROM\s+rtd_',
        r'FROM\s+manual_analise',
        r'SELECT.*FROM.*rtd_',
    ],
    "fluxo_canonico_fechado": [
        r'StructureInput',
        r'MarketSnapshotInput',
        r'CalculationRequest',
        r'canonical_input_service',
        r'structure_input_mapper',
        r'pricing_execution_service',
    ],
}

# Padroes que indicam fluxo canonico ja presente
CANONICAL_PATTERNS = [
    r'structure_id',
    r'StructureInput',
    r'MarketSnapshotInput',
    r'alias_legacy_aba',
    r'pricing_execution',
]

# ---------------------------------------------------------------------------
# UTILIDADES
# ---------------------------------------------------------------------------

def md5_file(path: Path) -> str:
    try:
        h = hashlib.md5()
        h.update(path.read_bytes())
        return h.hexdigest()
    except Exception:
        return "ERRO_LEITURA"


def file_line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except Exception:
        return -1


def grep_pattern_in_file(pattern: str, path: Path):
    """Retorna lista de (linha_num, conteudo) onde o padrao bate."""
    results = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        rx = re.compile(pattern, re.IGNORECASE)
        for i, line in enumerate(lines, 1):
            if rx.search(line):
                results.append((i, line.rstrip()))
    except Exception:
        pass
    return results


def find_all_refs_in_project(pattern: str, extensions=(".py",)):
    """Varre todo o projeto buscando o padrao nos arquivos com extensao dada."""
    hits = []
    for ext in extensions:
        for f in ROOT.rglob(f"*{ext}"):
            if ".git" in f.parts:
                continue
            matches = grep_pattern_in_file(pattern, f)
            if matches:
                hits.append((f.relative_to(ROOT), matches))
    return hits


def git_tracked(relative_path: str) -> bool:
    """Verifica se o arquivo esta rastreado pelo git."""
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", relative_path],
        cwd=ROOT,
        capture_output=True,
    )
    return result.returncode == 0


def find_canonical_counterpart(filename: str) -> Path | None:
    """Procura arquivo com mesmo nome em ATT/patches/ ou scripts/."""
    stem = Path(filename).name
    for candidate in [CANONICAL_PATCHES_DIR, CANONICAL_SCRIPTS_DIR]:
        found = list(candidate.rglob(stem))
        if found:
            return found[0]
    return None


# ---------------------------------------------------------------------------
# SECOES DO RELATORIO
# ---------------------------------------------------------------------------

sections = []


def section(title: str, content: str):
    sections.append(f"\n## {title}\n\n{content}\n")


def run_audit():

    print(f"[audit] Raiz do projeto: {ROOT}")
    print(f"[audit] Relatorio sera salvo em: {ROOT / REPORT_NAME}")
    print()

    # -----------------------------------------------------------------------
    # SECAO 1 — Metadados
    # -----------------------------------------------------------------------
    meta = (
        f"- Data/hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- Raiz: `{ROOT}`\n"
        f"- Branch: {_git_branch()}\n"
        f"- Ultimo commit: {_git_last_commit()}\n"
    )
    section("Metadados da Auditoria", meta)

    # -----------------------------------------------------------------------
    # SECAO 2 — Residuos suspeitos
    # -----------------------------------------------------------------------
    print("[audit] 1/6 Verificando residuos suspeitos...")
    residual_lines = []
    residuals_confirmed = []

    for rel in SUSPECTED_RESIDUALS:
        path = ROOT / rel
        tracked = git_tracked(rel)
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        lines = file_line_count(path) if exists else 0

        # verificar duplicidade com canonico
        counterpart = find_canonical_counterpart(rel) if exists else None
        if counterpart and counterpart.exists():
            md5_this = md5_file(path)
            md5_counter = md5_file(counterpart)
            dup_status = (
                "DUPLICADO (MD5 identico)"
                if md5_this == md5_counter
                else f"CONTEUDO DIFERENTE (MD5: {md5_this[:8]} vs {md5_counter[:8]})"
            )
        else:
            dup_status = "SEM CONTRAPARTE em ATT/patches/ ou scripts/"

        status_icon = "TRACKED" if tracked else "UNTRACKED"
        residual_lines.append(
            f"- `{rel}`\n"
            f"  - Git: {status_icon} | Existe: {exists} | "
            f"Tamanho: {size}B | Linhas: {lines}\n"
            f"  - Duplicidade: {dup_status}\n"
        )
        if tracked:
            residuals_confirmed.append(rel)

    residual_content = (
        "Arquivos inspecionados:\n\n"
        + "".join(residual_lines)
        + f"\n**Total rastreados pelo git (candidatos a remocao):** {len(residuals_confirmed)}\n"
        + "\nLista para `git rm`:\n```\n"
        + "\n".join(residuals_confirmed)
        + "\n```\n"
    )
    section("Residuos Suspeitos — Analise de Duplicidade e Rastreamento", residual_content)

    # -----------------------------------------------------------------------
    # SECAO 3 — Referencias a "aba" como identidade no dominio
    # -----------------------------------------------------------------------
    print("[audit] 2/6 Detectando acoplamento legado por aba...")
    aba_lines = []

    for rel in DOMAIN_FILES_TO_CHECK:
        path = ROOT / rel
        if not path.exists():
            aba_lines.append(f"- `{rel}` — ARQUIVO NAO ENCONTRADO\n")
            continue

        hits_by_category = {}
        for category, patterns in LEGACY_PATTERNS.items():
            hits = []
            for pat in patterns:
                found = grep_pattern_in_file(pat, path)
                hits.extend(found)
            if hits:
                hits_by_category[category] = hits

        if hits_by_category:
            aba_lines.append(f"- `{rel}` — **ACOPLAMENTO DETECTADO**\n")
            for cat, hits in hits_by_category.items():
                aba_lines.append(f"  - Categoria: `{cat}`\n")
                for lineno, content in hits[:5]:  # max 5 exemplos por padrao
                    snippet = content.strip()[:120]
                    aba_lines.append(f"    - L{lineno}: `{snippet}`\n")
        else:
            aba_lines.append(f"- `{rel}` — limpo (sem padroes legados detectados)\n")

    section(
        "Acoplamento Legado — Referencias a 'aba' e raw DB",
        "".join(aba_lines),
    )

    # -----------------------------------------------------------------------
    # SECAO 4 — Varredura global de referencias a tabelas raw
    # -----------------------------------------------------------------------
    print("[audit] 3/6 Varredura global de referencias a tabelas raw...")
    raw_refs = []
    for pat in LEGACY_PATTERNS["leitura_raw_db_direto"]:
        hits = find_all_refs_in_project(pat, extensions=(".py",))
        for relpath, matches in hits:
            raw_refs.append(f"- `{relpath}` (padrao: `{pat}`)\n")
            for lineno, content in matches[:3]:
                raw_refs.append(f"  - L{lineno}: `{content.strip()[:100]}`\n")

    if not raw_refs:
        raw_refs = ["Nenhuma referencia a tabelas raw encontrada no codigo Python.\n"]

    section(
        "Varredura Global — Leituras Diretas de Tabelas Raw (rtd_/manual_)",
        "".join(raw_refs),
    )

    # -----------------------------------------------------------------------
    # SECAO 5 — Verificar se fluxo canonico esta presente
    # -----------------------------------------------------------------------
    print("[audit] 4/6 Verificando presenca do fluxo canonico...")
    canonical_lines = []
    for pat in CANONICAL_PATTERNS:
        hits = find_all_refs_in_project(pat, extensions=(".py",))
        canonical_lines.append(
            f"- Padrao `{pat}`: encontrado em {len(hits)} arquivo(s)\n"
        )
        for relpath, matches in hits[:3]:
            canonical_lines.append(f"  - `{relpath}`\n")

    section(
        "Fluxo Canonico — Presenca de StructureInput / MarketSnapshotInput / pricing_execution",
        "".join(canonical_lines),
    )

    # -----------------------------------------------------------------------
    # SECAO 6 — Inspecionar bridge/last_export.txt
    # -----------------------------------------------------------------------
    print("[audit] 5/6 Inspecionando bridge/last_export.txt...")
    bridge_path = ROOT / "bridge" / "last_export.txt"
    if bridge_path.exists():
        try:
            content = bridge_path.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()
            preview = "\n".join(lines[:20])
            bridge_info = (
                f"- Existe: sim\n"
                f"- Git rastreado: {git_tracked('bridge/last_export.txt')}\n"
                f"- Tamanho: {bridge_path.stat().st_size}B\n"
                f"- Linhas: {len(lines)}\n"
                f"- Ultima modificacao: "
                f"{datetime.fromtimestamp(bridge_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"Preview (primeiras 20 linhas):\n```\n{preview}\n```\n"
            )
        except Exception as e:
            bridge_info = f"- Erro ao ler arquivo: {e}\n"
    else:
        bridge_info = "- Arquivo nao encontrado.\n"

    section("bridge/last_export.txt — Inspecao", bridge_info)

    # -----------------------------------------------------------------------
    # SECAO 7 — Resumo executivo e plano de acao
    # -----------------------------------------------------------------------
    print("[audit] 6/6 Gerando resumo executivo...")
    summary = (
        "### O que esta confirmado\n\n"
        "- Residuos identificados e classificados (ver Secao 2)\n"
        "- Acoplamentos legados mapeados por arquivo e linha (ver Secao 3)\n"
        "- Referencias globais a tabelas raw identificadas (ver Secao 4)\n"
        "- Presenca do fluxo canonico verificada (ver Secao 5)\n"
        "- bridge/last_export.txt inspecionado (ver Secao 6)\n\n"
        "### Acoes imediatas recomendadas\n\n"
        "1. Para cada arquivo na lista da Secao 2 com status TRACKED e "
        "duplicidade DUPLICADO: executar `git rm` sem risco\n"
        "2. Para arquivos TRACKED com CONTEUDO DIFERENTE: revisar manualmente "
        "antes de remover\n"
        "3. Para cada acoplamento legado da Secao 3: registrar como tarefa "
        "do patch_39 ou patch_40\n"
        "4. Para bridge/last_export.txt: decidir se e artefato de estado ativo "
        "ou residuo, conforme preview da Secao 6\n\n"
        "### Proximos patches sugeridos\n\n"
        "- patch_39: limpeza de residuos rastreados (baseada neste relatorio)\n"
        "- patch_40: isolamento de acoplamentos legados identificados\n"
        "- patch_41: validacao de fechamento do fluxo canonico ponta a ponta\n"
    )
    section("Resumo Executivo e Plano de Acao", summary)

    # -----------------------------------------------------------------------
    # GRAVAR RELATORIO
    # -----------------------------------------------------------------------
    report_path = ROOT / REPORT_NAME
    report_path.parent.mkdir(parents=True, exist_ok=True)

    header = (
        f"# Auditoria patch_39 — baseline patch/3b\n\n"
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    full_report = header + "".join(sections)
    report_path.write_text(full_report, encoding="utf-8")

    print()
    print(f"[audit] Relatorio salvo em: {report_path}")
    print(f"[audit] Secoes geradas: {len(sections)}")
    print("[audit] Concluido.")


# ---------------------------------------------------------------------------
# HELPERS GIT
# ---------------------------------------------------------------------------

def _git_branch() -> str:
    r = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return r.stdout.strip() if r.returncode == 0 else "desconhecida"


def _git_last_commit() -> str:
    r = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return r.stdout.strip() if r.returncode == 0 else "desconhecido"


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_audit()
    sys.exit(0)
