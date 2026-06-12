from __future__ import annotations

import os
import re
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
DADOS_DIR = ROOT / "dados"

CUTOFF_DATE = "2026-06-06"

EXPECTED_PHASES = {
    2: {
        "name": "Diagnóstico do Fluxo Atual",
        "doc_patterns": ["FASE_2", "fase_2"],
        "grep_terms": ["fase 2", "fase_2", "diagnostico do fluxo atual", "diagnóstico do fluxo atual"],
    },
    3: {
        "name": "Classificação das Fontes de Dados",
        "doc_patterns": ["FASE_3", "fase_3"],
        "grep_terms": ["fase 3", "fase_3", "classifica fontes", "classificação das fontes"],
    },
    4: {
        "name": "Auditoria de Dependência do Excel",
        "doc_patterns": ["FASE_4", "fase_4"],
        "grep_terms": ["fase 4", "fase_4", "dependencia excel", "dependência excel"],
    },
    5: {
        "name": "Isolamento Bridge/Excel",
        "doc_patterns": ["FASE_5", "fase_5"],
        "grep_terms": ["fase 5", "fase_5", "isolamento bridge", "adaptador legado"],
    },
    6: {
        "name": "Camada Canônica de Leitura",
        "doc_patterns": ["FASE_6", "fase_6"],
        "grep_terms": ["fase 6", "fase_6", "camada canonica", "camada canônica"],
    },
    7: {
        "name": "Isolamento de Nomes Físicos Legados",
        "doc_patterns": ["FASE_7", "fase_7"],
        "grep_terms": ["fase 7", "fase_7", "nomes fisicos", "nomes físicos"],
    },
    8: {
        "name": "Banco Como Fonte da Verdade",
        "doc_patterns": ["FASE_8", "fase_8"],
        "grep_terms": ["fase 8", "fase_8", "banco fonte", "fonte da verdade"],
    },
}


@dataclass
class CommitInfo:
    sha: str
    date: str
    subject: str
    is_empty: bool | None = None


def run(cmd: list[str], cwd: Path = ROOT, check: bool = False) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Comando falhou: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def parse_git_log(output: str) -> list[CommitInfo]:
    commits: list[CommitInfo] = []
    for line in output.splitlines():
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        sha, date, subject = parts
        commits.append(CommitInfo(sha=sha.strip(), date=date.strip(), subject=subject.strip()))
    return commits


def get_commit_is_empty(sha: str) -> bool | None:
    parents = run(["git", "show", "-s", "--format=%P", sha])
    if not parents:
        return None

    first_parent = parents.split()[0]
    diff = run(["git", "diff", "--name-only", f"{first_parent}..{sha}"])
    return diff.strip() == ""


def find_docs_for_phase(phase: int) -> list[Path]:
    cfg = EXPECTED_PHASES[phase]
    matches: list[Path] = []
    if not DOCS_DIR.exists():
        return matches

    for path in DOCS_DIR.rglob("*"):
        if not path.is_file():
            continue
        name_lower = path.name.lower()
        for pattern in cfg["doc_patterns"]:
            if pattern.lower() in name_lower:
                matches.append(path)
                break
    return sorted(set(matches))


def find_git_evidence_for_phase(phase: int) -> list[CommitInfo]:
    terms = EXPECTED_PHASES[phase]["grep_terms"]

    commits_by_sha: dict[str, CommitInfo] = {}

    for term in terms:
        output = run([
            "git",
            "log",
            "--all",
            "--date=short",
            "--format=%h|%ad|%s",
            "--grep",
            term,
            "-i",
        ])
        for commit in parse_git_log(output):
            commits_by_sha[commit.sha] = commit

    return list(commits_by_sha.values())


def doc_last_commit(path: Path) -> CommitInfo | None:
    rel = path.relative_to(ROOT).as_posix()
    output = run([
        "git",
        "log",
        "-1",
        "--date=short",
        "--format=%h|%ad|%s",
        "--",
        rel,
    ])
    commits = parse_git_log(output)
    if not commits:
        return None
    return commits[0]


def date_is_after_or_equal(date_str: str, cutoff: str = CUTOFF_DATE) -> bool:
    try:
        return datetime.fromisoformat(date_str).date() >= datetime.fromisoformat(cutoff).date()
    except Exception:
        return False


def list_phase_docs() -> None:
    section("DOCUMENTOS DE FASE LOCALIZADOS")

    if not DOCS_DIR.exists():
        print("docs/ não encontrado.")
        return

    files = sorted(
        p for p in DOCS_DIR.rglob("*")
        if p.is_file() and "fase" in p.name.lower()
    )

    if not files:
        print("Nenhum documento de fase encontrado.")
        return

    for p in files:
        rel = p.relative_to(ROOT)
        last = doc_last_commit(p)
        if last:
            after = "SIM" if date_is_after_or_equal(last.date) else "NÃO"
            print(f"- {rel} | último commit: {last.sha} | data: {last.date} | >= {CUTOFF_DATE}: {after} | {last.subject}")
        else:
            print(f"- {rel} | sem commit identificado")


def audit_git_basics() -> None:
    section("GIT - ESTADO ATUAL")

    print("Branch:")
    print(run(["git", "branch", "--show-current"]) or "(não identificado)")

    print()
    print("Status --short:")
    status = run(["git", "status", "--short"])
    print(status if status else "(working tree limpo)")

    print()
    print("Últimos 20 commits com datas:")
    print(run(["git", "log", "--oneline", "--decorate", "--date=short", "--format=%h %ad %d %s", "-20"]))


def audit_phase_route() -> None:
    section("CONFERÊNCIA DA ROTA POR FASE")

    for phase in sorted(EXPECTED_PHASES):
        cfg = EXPECTED_PHASES[phase]
        docs = find_docs_for_phase(phase)
        evidence = find_git_evidence_for_phase(phase)

        print()
        print(f"Fase {phase} - {cfg['name']}")
        print("-" * 88)

        if docs:
            print("Documentos:")
            for doc in docs:
                rel = doc.relative_to(ROOT)
                last = doc_last_commit(doc)
                if last:
                    after = "SIM" if date_is_after_or_equal(last.date) else "NÃO"
                    print(f"  - {rel} | {last.sha} | {last.date} | >= {CUTOFF_DATE}: {after} | {last.subject}")
                else:
                    print(f"  - {rel} | sem commit identificado")
        else:
            print("Documentos: NÃO ENCONTRADO")

        if evidence:
            print("Evidências em commits:")
            for c in evidence:
                c.is_empty = get_commit_is_empty(c.sha)
                empty_txt = "vazio" if c.is_empty else "com diff" if c.is_empty is False else "sem pai/indeterminado"
                after = "SIM" if date_is_after_or_equal(c.date) else "NÃO"
                print(f"  - {c.sha} | {c.date} | >= {CUTOFF_DATE}: {after} | {empty_txt} | {c.subject}")
        else:
            print("Evidências em commits: NÃO ENCONTRADO")

        if not docs and evidence:
            print("Status sugerido: há evidência Git, mas falta documento versionado da fase.")
        elif docs and evidence:
            print("Status sugerido: fase possui documento e evidência Git.")
        elif docs and not evidence:
            print("Status sugerido: há documento, mas pouca evidência textual no log.")
        else:
            print("Status sugerido: fase sem evidência suficiente nesta auditoria.")


def audit_specific_phase7() -> None:
    section("FOCO RÁPIDO - FASE 7")

    sha = "fc4d438"
    exists = run(["git", "cat-file", "-t", sha])
    if exists != "commit":
        print(f"Commit {sha} não encontrado.")
        return

    print("Commit citado:")
    print(run(["git", "show", "-s", "--date=short", "--format=%h|%ad|%s|parents=%P", sha]))

    is_empty = get_commit_is_empty(sha)
    print()
    print(f"Commit vazio ou sem alteração de arquivos: {'SIM' if is_empty else 'NÃO'}")

    print()
    print("Arquivos alterados no commit:")
    files = run(["git", "diff", "--name-status", f"{sha}^..{sha}"])
    print(files if files else "(nenhum arquivo alterado)")

    print()
    print("Conclusão automática:")
    if is_empty:
        print("A Fase 7 tem evidência de fechamento no Git, mas não possui documento/alteração associada nesse commit.")
    else:
        print("A Fase 7 possui alterações associadas ao commit.")


def get_sqlite_tables(db_path: Path) -> list[str]:
    if not db_path.exists():
        return []
    with sqlite3.connect(str(db_path)) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table','view') ORDER BY name"
        ).fetchall()
    return [r[0] for r in rows]


def count_table(db_path: Path, table: str) -> int | None:
    try:
        with sqlite3.connect(str(db_path)) as conn:
            row = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()
            return int(row[0])
    except Exception:
        return None


def audit_databases() -> None:
    section("BANCOS SQLITE - CONFERÊNCIA OPERACIONAL")

    dbs = [
        DADOS_DIR / "app.db",
        DADOS_DIR / "derived.db",
    ]

    for db in dbs:
        rel = db.relative_to(ROOT) if db.exists() else db
        print()
        print(f"Banco: {rel}")

        if not db.exists():
            print("Status: NÃO ENCONTRADO")
            continue

        size = db.stat().st_size
        print(f"Status: encontrado | tamanho: {size} bytes")

        tables = get_sqlite_tables(db)
        print("Tabelas/views:")
        for t in tables:
            count = count_table(db, t)
            if count is None:
                print(f"  - {t}")
            else:
                print(f"  - {t}: {count}")

    app_db = DADOS_DIR / "app.db"
    if app_db.exists():
        print()
        print("Estruturas 44-48 em dados/app.db:")
        try:
            with sqlite3.connect(str(app_db)) as conn:
                rows = conn.execute(
                    """
                    SELECT id, name, underlying_asset, alias_legacy_aba, status
                    FROM structures
                    WHERE id BETWEEN 44 AND 48
                    ORDER BY id
                    """
                ).fetchall()

            if rows:
                for row in rows:
                    print(f"  - id={row[0]} | name={row[1]} | underlying={row[2]} | alias={row[3]} | status={row[4]}")
            else:
                print("  Nenhuma estrutura 44-48 encontrada.")
        except Exception as exc:
            print(f"  Erro ao consultar structures: {exc}")

        print()
        print("Pernas normalizadas por estrutura 44-48:")
        try:
            with sqlite3.connect(str(app_db)) as conn:
                rows = conn.execute(
                    """
                    SELECT s.id, s.alias_legacy_aba, COUNT(l.id) AS legs
                    FROM structures s
                    LEFT JOIN structure_legs l ON l.structure_id = s.id
                    WHERE s.id BETWEEN 44 AND 48
                    GROUP BY s.id, s.alias_legacy_aba
                    ORDER BY s.id
                    """
                ).fetchall()

            if rows:
                for row in rows:
                    print(f"  - structure_id={row[0]} | alias={row[1]} | structure_legs={row[2]}")
            else:
                print("  Nenhuma estrutura 44-48 encontrada.")
        except Exception as exc:
            print(f"  Erro ao consultar structure_legs: {exc}")


def audit_scripts() -> None:
    section("SCRIPTS OPERACIONAIS E DE VALIDAÇÃO")

    candidates = [
        "scripts/db_locator.py",
        "scripts/validate_derived_db.py",
        "scripts/run_smoke_quick.py",
        "scripts/run_smoke_full.py",
        "run_derived_pipeline.py",
        "validate_derived_db.py",
        "bridge_ingest_csv.py",
    ]

    for rel in candidates:
        path = ROOT / rel
        print(f"- {rel}: {'OK' if path.exists() else 'não encontrado'}")


def main() -> None:
    print("CONFERÊNCIA DA ROTA DE DESENVOLVIMENTO")
    print(f"Projeto: {ROOT}")
    print(f"Data de corte: {CUTOFF_DATE}")
    print(f"Executado em UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")

    audit_git_basics()
    list_phase_docs()
    audit_phase_route()
    audit_specific_phase7()
    audit_databases()
    audit_scripts()

    section("RESUMO DE LEITURA ESPERADO")
    print(
        "Use este relatório para decidir a próxima etapa sem pular fase:\n"
        "- Se Fase 7 só tiver commit vazio, registre como fechamento sem documento próprio.\n"
        "- Se Fase 8 tem commits técnicos após a auditoria, ela provavelmente está em andamento.\n"
        "- Se structure_legs já estiver populada para 44-48, a pendência central da Fase 8 pode ter sido tratada.\n"
        "- Se derived.db validar e os smokes existirem/passarem, aí sim avaliar avanço para a próxima fase da rota.\n"
    )


if __name__ == "__main__":
    main()
