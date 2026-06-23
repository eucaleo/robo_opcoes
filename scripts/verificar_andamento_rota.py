from __future__ import annotations

import argparse
import os
import sqlite3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCUMENTS = [
    "docs/rotas/NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md",
    "docs/auditoria/AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_PLANO_EXECUCAO.md",
    "docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_2_NORMALIZACAO_NUMERICA.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_3_CADASTRO_ASSISTIDO.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_4_PAYOFF_DECISOES.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_ATUALIZAR_DADOS_PIPELINE.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_6_RTD.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_7_RECALCULO_METRICAS.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_8_DUPLICIDADE_ESTRUTURA.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_9_PORTUGUES_BRASIL.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_10_COMENTARIO_PAYOFF.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_11_VISIBILIDADE_ATUALIZACAO.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_12_ABA_ALIAS.md",
    "docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_13_VALIDACAO_INTEGRADA.md",
    "docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FECHAMENTO.md",
    "docs/checklists/CHECKLIST_REVISAO_FUNCIONAL_POS_USO_REAL.md",
    "docs/decisoes/DECISOES_REVISAO_FUNCIONAL_POS_USO_REAL.md",
]

ROUTE_KEYWORDS = [
    "NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL",
    "REVISAO_FUNCIONAL_POS_USO_REAL",
    "AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL",
    "payoff_pricing_engine",
    "PricingEngineStub",
    "pricing_engine_stub",
    "stub",
]


def run_command(args: list[str], check: bool = False) -> tuple[int, str, str]:
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())

    return result.returncode, result.stdout.strip(), result.stderr.strip()


def print_section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def print_subsection(title: str) -> None:
    print()
    print("-" * 100)
    print(title)
    print("-" * 100)


def git_summary() -> None:
    print_section("GIT")

    commands = [
        ("Branch atual", ["git", "branch", "--show-current"]),
        ("Status curto", ["git", "status", "--short"]),
        ("Últimos 15 commits", ["git", "log", "--oneline", "--decorate", "-15"]),
    ]

    for title, command in commands:
        print_subsection(title)
        code, out, err = run_command(command)
        if out:
            print(out)
        elif err:
            print(err)
        else:
            print("(sem saída)")

    print_subsection("Commits relacionados à nova rota")
    code, out, err = run_command(
        [
            "git",
            "log",
            "--oneline",
            "--decorate",
            "--all",
            "--grep=REVISAO_FUNCIONAL_POS_USO_REAL",
            "--grep=NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL",
            "--grep=payoff_pricing_engine",
            "--all-match",
        ]
    )

    if out:
        print(out)
    else:
        code, out, err = run_command(
            [
                "git",
                "log",
                "--oneline",
                "--decorate",
                "--all",
                "--",
                "docs/rotas",
                "docs/auditoria",
                "docs/checkpoints",
                "docs/evidencias",
                "docs/checklists",
                "docs/decisoes",
                "services",
                "repositories",
                "domain",
                "ATT/tests",
            ]
        )
        print(out or err or "(sem commits encontrados para os caminhos pesquisados)")


def document_summary() -> None:
    print_section("DOCUMENTOS DA ROTA")

    existing = []
    missing = []

    for relative_path in REQUIRED_DOCUMENTS:
        path = ROOT / relative_path
        if path.exists():
            existing.append(relative_path)
        else:
            missing.append(relative_path)

    print_subsection("Documentos encontrados")
    if existing:
        for item in existing:
            print(f"[OK] {item}")
    else:
        print("(nenhum documento obrigatório encontrado)")

    print_subsection("Documentos pendentes")
    if missing:
        for item in missing:
            print(f"[PENDENTE] {item}")
    else:
        print("(nenhum documento obrigatório pendente)")

    print_subsection("Arquivos Markdown relacionados")
    docs_root = ROOT / "docs"
    if docs_root.exists():
        related = []
        for path in docs_root.rglob("*.md"):
            text_path = str(path.relative_to(ROOT)).replace("\\", "/")
            if (
                "REVISAO_FUNCIONAL_POS_USO_REAL" in text_path
                or "NOVA_ROTA" in text_path
                or "AUDITORIA" in text_path
            ):
                related.append(text_path)

        if related:
            for item in sorted(related):
                print(item)
        else:
            print("(nenhum Markdown relacionado encontrado)")
    else:
        print("(diretório docs não encontrado)")


def search_summary() -> None:
    print_section("BUSCAS NO PROJETO")

    search_dirs = [
        "services",
        "repositories",
        "domain",
        "ATT/tests",
        "docs",
    ]

    for keyword in ROUTE_KEYWORDS:
        print_subsection(f"Ocorrências de: {keyword}")
        matches = []

        for directory in search_dirs:
            path = ROOT / directory
            if not path.exists():
                continue

            for file_path in path.rglob("*"):
                if not file_path.is_file():
                    continue

                if "__pycache__" in file_path.parts:
                    continue

                if file_path.suffix.lower() not in {".py", ".md", ".txt", ".sql", ".json"}:
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue

                if keyword in content:
                    matches.append(str(file_path.relative_to(ROOT)).replace("\\", "/"))

        if matches:
            for item in sorted(set(matches)):
                print(item)
        else:
            print("(sem ocorrências)")


def database_summary() -> None:
    print_section("BANCO DE DADOS")

    db_path = ROOT / "dados" / "app.db"

    if not db_path.exists():
        print("Banco não encontrado em dados/app.db")
        return

    print(f"Banco encontrado: {db_path.relative_to(ROOT)}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        print_subsection("Tabelas existentes")
        rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()

        for row in rows:
            print(row["name"])

        table_names = {row["name"] for row in rows}

        if "pricing_executions" in table_names:
            print_subsection("Últimas execuções de precificação")
            rows = conn.execute(
                """
                SELECT
                    id,
                    structure_id,
                    execution_engine,
                    execution_status,
                    theoretical_value,
                    created_at
                FROM pricing_executions
                ORDER BY id DESC
                LIMIT 10
                """
            ).fetchall()

            if rows:
                for row in rows:
                    print(
                        f"id={row['id']} | "
                        f"structure_id={row['structure_id']} | "
                        f"engine={row['execution_engine']} | "
                        f"status={row['execution_status']} | "
                        f"theoretical_value={row['theoretical_value']} | "
                        f"created_at={row['created_at']}"
                    )
            else:
                print("(sem registros em pricing_executions)")

        if "pricing_executions" in table_names:
            print_subsection("Resumo por motor de precificação")
            rows = conn.execute(
                """
                SELECT
                    execution_engine,
                    execution_status,
                    COUNT(*) AS total,
                    MAX(created_at) AS ultima_execucao
                FROM pricing_executions
                GROUP BY execution_engine, execution_status
                ORDER BY ultima_execucao DESC
                """
            ).fetchall()

            if rows:
                for row in rows:
                    print(
                        f"engine={row['execution_engine']} | "
                        f"status={row['execution_status']} | "
                        f"total={row['total']} | "
                        f"ultima_execucao={row['ultima_execucao']}"
                    )
            else:
                print("(sem resumo disponível)")

        if "structures" in table_names:
            print_subsection("Possíveis duplicidades em structures")
            columns = conn.execute("PRAGMA table_info(structures)").fetchall()
            column_names = {row["name"] for row in columns}

            candidate_columns = [
                name
                for name in ["id", "name", "structure_name", "underlying_asset", "status", "created_at"]
                if name in column_names
            ]

            if candidate_columns:
                rows = conn.execute(
                    """
                    SELECT COUNT(*) AS total
                    FROM structures
                    """
                ).fetchall()
                print(f"total_structures={rows[0]['total']}")

                if "id" in column_names:
                    rows = conn.execute(
                        """
                        SELECT id, COUNT(*) AS total
                        FROM structures
                        GROUP BY id
                        HAVING COUNT(*) > 1
                        ORDER BY total DESC
                        """
                    ).fetchall()

                    if rows:
                        for row in rows:
                            print(f"id={row['id']} | total={row['total']}")
                    else:
                        print("(sem duplicidade física por id em structures)")
            else:
                print("(tabela structures encontrada, mas sem colunas candidatas conhecidas)")

        if "rtd_option_quotes" in table_names:
            print_subsection("RTD option quotes")
            rows = conn.execute(
                """
                SELECT COUNT(*) AS total
                FROM rtd_option_quotes
                """
            ).fetchall()
            print(f"total_rtd_option_quotes={rows[0]['total']}")

        if "payoff_curve_points" in table_names:
            print_subsection("Payoff curve points")
            rows = conn.execute(
                """
                SELECT COUNT(*) AS total
                FROM payoff_curve_points
                """
            ).fetchall()
            print(f"total_payoff_curve_points={rows[0]['total']}")

        if "structure_decisions" in table_names:
            print_subsection("Structure decisions")
            rows = conn.execute(
                """
                SELECT COUNT(*) AS total
                FROM structure_decisions
                """
            ).fetchall()
            print(f"total_structure_decisions={rows[0]['total']}")

    finally:
        conn.close()


def test_summary(run_tests: bool) -> None:
    print_section("VALIDAÇÃO TÉCNICA")

    compile_targets = [
        path
        for path in ["repositories", "services", "domain", "ATT/tests"]
        if (ROOT / path).exists()
    ]

    if compile_targets:
        print_subsection("Compileall")
        code, out, err = run_command(
            ["python", "-m", "compileall", *compile_targets]
        )
        print(f"returncode={code}")
        if out:
            print(out)
        if err:
            print(err)
    else:
        print_subsection("Compileall")
        print("(nenhum alvo encontrado entre repositories, services, domain, ATT/tests)")

    print_subsection("Pytest")
    if not run_tests:
        print("não executado; use --run-tests para executar")
        return

    if (ROOT / "ATT" / "tests").exists():
        code, out, err = run_command(["python", "-m", "pytest", "ATT/tests", "-q"])
        print(f"returncode={code}")
        if out:
            print(out)
        if err:
            print(err)
    else:
        print("(ATT/tests não encontrado)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Executa pytest ATT/tests -q além da compilação.",
    )
    args = parser.parse_args()

    os.chdir(ROOT)

    print("RELATORIO DE ANDAMENTO DA NOVA ROTA")
    print(f"raiz={ROOT}")

    git_summary()
    document_summary()
    search_summary()
    database_summary()
    test_summary(run_tests=args.run_tests)


if __name__ == "__main__":
    main()
