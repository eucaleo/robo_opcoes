#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_OPTION_HEADERS = [
    "codigo_opcao",
    "ativo_base",
    "call_put",
    "strike",
    "vencimento",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "vwap",
]


SEARCH_PATTERN = re.compile(
    r"LISTA_RTD|RTD_OPTION_QUOTES|RTD-BTG|RTD|win32com|GetActiveObject|Dispatch|"
    r"Excel\.Application|subprocess|Popen|check_output|os\.system|Preencher|preencher|"
    r"leg|perna|snapshot|sqlite|database|connect\(",
    re.IGNORECASE,
)


SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
}


TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".sql",
    ".json",
    ".ini",
    ".toml",
    ".yaml",
    ".yml",
    ".bat",
    ".ps1",
    ".sh",
}


def run_command(args, cwd, timeout=120):
    result = {
        "args": args,
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "error": None,
    }

    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        result["returncode"] = completed.returncode
        result["stdout"] = completed.stdout
        result["stderr"] = completed.stderr
    except Exception as exc:
        result["error"] = repr(exc)

    return result


def get_git_root(start_dir):
    result = run_command(["git", "rev-parse", "--show-toplevel"], start_dir, timeout=30)
    if result["returncode"] == 0 and result["stdout"].strip():
        return Path(result["stdout"].strip()).resolve(), result

    return Path(start_dir).resolve(), result


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", errors="replace")


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
        errors="replace",
    )


def relative_to_root(path, root):
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except Exception:
        return str(path)


def list_files(base_dir, root, max_files=5000):
    rows = []

    if not base_dir.exists():
        return rows

    for current_root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for name in files:
            file_path = Path(current_root) / name
            rows.append(relative_to_root(file_path, root))

            if len(rows) >= max_files:
                rows.append("LIMITE_DE_LISTAGEM_ATINGIDO")
                return rows

    return sorted(rows)


def search_references(root, max_hits=5000):
    hits = []

    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for name in files:
            file_path = Path(current_root) / name

            if file_path.suffix.lower() not in TEXT_EXTENSIONS:
                continue

            try:
                rel = relative_to_root(file_path, root)
                with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                    for line_no, line in enumerate(handle, start=1):
                        if SEARCH_PATTERN.search(line):
                            hits.append(f"{rel}:{line_no}: {line.rstrip()}")

                            if len(hits) >= max_hits:
                                hits.append("LIMITE_DE_BUSCA_ATINGIDO")
                                return hits
            except Exception as exc:
                hits.append(f"{relative_to_root(file_path, root)}:ERRO_LEITURA: {repr(exc)}")

    return hits


def parse_json_text(text):
    try:
        return json.loads(text)
    except Exception:
        return None


def add_check(checks, name, ok, detail="", critical=False):
    checks.append(
        {
            "name": name,
            "ok": bool(ok),
            "critical": bool(critical),
            "detail": detail,
        }
    )


def run_python_probe(root, script_rel_path, evidence_dir, output_name, extra_args=None, timeout=120):
    script_path = root / script_rel_path
    extra_args = extra_args or []

    result = {
        "script": script_rel_path,
        "exists": script_path.exists(),
        "args": extra_args,
        "returncode": None,
        "stdout_file": None,
        "stderr_file": None,
        "json": None,
        "error": None,
    }

    stdout_file = evidence_dir / f"{output_name}.stdout.txt"
    stderr_file = evidence_dir / f"{output_name}.stderr.txt"

    result["stdout_file"] = relative_to_root(stdout_file, root)
    result["stderr_file"] = relative_to_root(stderr_file, root)

    if not script_path.exists():
        result["error"] = "script_nao_encontrado"
        write_text(stdout_file, "")
        write_text(stderr_file, "script_nao_encontrado")
        return result

    command = [sys.executable, str(script_path)] + extra_args
    completed = run_command(command, root, timeout=timeout)

    result["returncode"] = completed["returncode"]
    result["error"] = completed["error"]

    write_text(stdout_file, completed["stdout"] or "")
    write_text(stderr_file, completed["stderr"] or "")

    parsed = parse_json_text(completed["stdout"] or "")
    result["json"] = parsed

    return result


def build_markdown_report(report):
    checks = report["checks"]
    failed_critical = [c for c in checks if c["critical"] and not c["ok"]]
    failed_non_critical = [c for c in checks if not c["critical"] and not c["ok"]]

    lines = []
    lines.append("# Verificacao de Retomada - RTD Excel BTG Online")
    lines.append("")
    lines.append(f"Data/hora: {report['generated_at_local']}")
    lines.append(f"Projeto: {report['project_root']}")
    lines.append(f"Branch: {report['git'].get('branch', '')}")
    lines.append(f"Diretorio de evidencias: {report['evidence_dir']}")
    lines.append("")
    lines.append("## Resultado geral")
    lines.append("")

    if failed_critical:
        lines.append("Status: FALHA_CRITICA")
    elif failed_non_critical:
        lines.append("Status: OK_COM_ALERTAS")
    else:
        lines.append("Status: OK")

    lines.append("")
    lines.append("## Checks")
    lines.append("")

    for check in checks:
        status = "OK" if check["ok"] else "FALHA"
        critical = "CRITICO" if check["critical"] else "INFORMATIVO"
        lines.append(f"- {status} | {critical} | {check['name']} | {check.get('detail', '')}")

    lines.append("")
    lines.append("## Arquivos de evidencia")
    lines.append("")

    for item in report.get("evidence_files", []):
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Pendencias criticas")
    lines.append("")

    if failed_critical:
        for check in failed_critical:
            lines.append(f"- {check['name']}: {check.get('detail', '')}")
    else:
        lines.append("- Nenhuma pendencia critica identificada.")

    lines.append("")
    lines.append("## Observacao")
    lines.append("")
    lines.append("Este script apenas verifica o estado de retomada.")
    lines.append("Ele nao altera logica operacional do sistema.")
    lines.append("Ele utiliza os probes existentes para confirmar Excel COM, workbook e abas RTD.")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="retorna codigo diferente de zero se houver falha critica",
    )
    args = parser.parse_args()

    start_dir = Path.cwd()
    root, git_root_result = get_git_root(start_dir)

    generated_at = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    run_id = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    frente_dir = root / "FRENTE_RTD_EXCEL_BTG_ONLINE"
    frente_output_dir = frente_dir / "output"

    frente_dir_existed = frente_dir.is_dir()
    frente_output_existed = frente_output_dir.is_dir()

    if frente_dir_existed:
        frente_output_dir.mkdir(parents=True, exist_ok=True)
        evidence_dir = frente_output_dir / f"retomada_{run_id}"
    else:
        fallback_output = root / "output"
        fallback_output.mkdir(parents=True, exist_ok=True)
        evidence_dir = fallback_output / f"retomada_rtd_excel_{run_id}"

    evidence_dir.mkdir(parents=True, exist_ok=True)

    checks = []
    evidence_files = []

    def evidence_path(name):
        path = evidence_dir / name
        evidence_files.append(relative_to_root(path, root))
        return path

    git_branch_result = run_command(["git", "branch", "--show-current"], root, timeout=30)
    git_status_result = run_command(["git", "status", "--short"], root, timeout=30)
    git_log_result = run_command(["git", "log", "--oneline", "-20"], root, timeout=30)

    write_text(evidence_path("git_rev_parse_root.txt"), git_root_result["stdout"] or git_root_result["stderr"] or "")
    write_text(evidence_path("git_branch.txt"), git_branch_result["stdout"] or git_branch_result["stderr"] or "")
    write_text(evidence_path("git_status_short.txt"), git_status_result["stdout"] or git_status_result["stderr"] or "")
    write_text(evidence_path("git_log_last_20.txt"), git_log_result["stdout"] or git_log_result["stderr"] or "")

    branch = (git_branch_result["stdout"] or "").strip()
    git_status = (git_status_result["stdout"] or "").strip()

    add_check(
        checks,
        "repositorio_git_detectado",
        git_root_result["returncode"] == 0,
        f"root={root}",
        critical=True,
    )
    add_check(
        checks,
        "frente_documental_existe",
        frente_dir_existed,
        relative_to_root(frente_dir, root),
        critical=True,
    )
    add_check(
        checks,
        "pasta_output_frente_existe",
        frente_output_existed,
        relative_to_root(frente_output_dir, root),
        critical=True,
    )
    add_check(
        checks,
        "branch_atual_identificada",
        bool(branch),
        branch,
        critical=False,
    )
    add_check(
        checks,
        "working_tree_sem_alteracoes_previas",
        git_status == "",
        "limpo" if git_status == "" else "existem alteracoes antes ou durante a verificacao",
        critical=False,
    )

    workbook_path = root / "LISTA_RTD.xlsm"
    add_check(
        checks,
        "workbook_lista_rtd_existe_na_raiz",
        workbook_path.exists(),
        relative_to_root(workbook_path, root),
        critical=True,
    )

    diagnose_script = root / "scripts" / "diagnose_excel_com.py"
    probe_script = root / "scripts" / "probe_excel_rtd_workbook.py"

    add_check(
        checks,
        "script_diagnose_excel_com_existe",
        diagnose_script.exists(),
        relative_to_root(diagnose_script, root),
        critical=True,
    )
    add_check(
        checks,
        "script_probe_excel_rtd_workbook_existe",
        probe_script.exists(),
        relative_to_root(probe_script, root),
        critical=True,
    )

    frente_files = list_files(frente_dir, root)
    output_files = list_files(frente_output_dir, root)
    project_hits = search_references(root)

    write_text(evidence_path("frente_files.txt"), "\n".join(frente_files) + "\n")
    write_text(evidence_path("frente_output_files.txt"), "\n".join(output_files) + "\n")
    write_text(evidence_path("project_search_hits.txt"), "\n".join(project_hits) + "\n")

    add_check(
        checks,
        "frente_documental_tem_arquivos",
        len(frente_files) > 0,
        f"arquivos_listados={len(frente_files)}",
        critical=True,
    )
    add_check(
        checks,
        "busca_referencias_projeto_executada",
        len(project_hits) > 0,
        f"ocorrencias={len(project_hits)}",
        critical=False,
    )

    probes = {}

    probes["diagnose_excel_com"] = run_python_probe(
        root,
        "scripts/diagnose_excel_com.py",
        evidence_dir,
        "diagnose_excel_com",
        timeout=120,
    )
    evidence_files.append(probes["diagnose_excel_com"]["stdout_file"])
    evidence_files.append(probes["diagnose_excel_com"]["stderr_file"])

    probes["probe_default"] = run_python_probe(
        root,
        "scripts/probe_excel_rtd_workbook.py",
        evidence_dir,
        "probe_excel_rtd_workbook_default",
        timeout=120,
    )
    evidence_files.append(probes["probe_default"]["stdout_file"])
    evidence_files.append(probes["probe_default"]["stderr_file"])

    probes["probe_rtd_option_quotes"] = run_python_probe(
        root,
        "scripts/probe_excel_rtd_workbook.py",
        evidence_dir,
        "probe_excel_rtd_option_quotes",
        extra_args=["--sheet", "RTD_OPTION_QUOTES"],
        timeout=120,
    )
    evidence_files.append(probes["probe_rtd_option_quotes"]["stdout_file"])
    evidence_files.append(probes["probe_rtd_option_quotes"]["stderr_file"])

    probes["probe_rtd_btg_lista"] = run_python_probe(
        root,
        "scripts/probe_excel_rtd_workbook.py",
        evidence_dir,
        "probe_excel_rtd_btg_lista",
        extra_args=["--sheet", "RTD-BTG LISTA"],
        timeout=120,
    )
    evidence_files.append(probes["probe_rtd_btg_lista"]["stdout_file"])
    evidence_files.append(probes["probe_rtd_btg_lista"]["stderr_file"])

    diagnose_ok = probes["diagnose_excel_com"]["returncode"] == 0
    default_json = probes["probe_default"]["json"] or {}
    option_json = probes["probe_rtd_option_quotes"]["json"] or {}
    btg_json = probes["probe_rtd_btg_lista"]["json"] or {}

    default_ok = probes["probe_default"]["returncode"] == 0 and default_json.get("ok") is True
    option_ok = probes["probe_rtd_option_quotes"]["returncode"] == 0 and option_json.get("ok") is True
    btg_ok = probes["probe_rtd_btg_lista"]["returncode"] == 0 and btg_json.get("ok") is True

    add_check(
        checks,
        "excel_com_diagnostico_executado",
        diagnose_ok,
        f"returncode={probes['diagnose_excel_com']['returncode']}",
        critical=True,
    )
    add_check(
        checks,
        "probe_workbook_default_ok",
        default_ok,
        f"returncode={probes['probe_default']['returncode']}",
        critical=True,
    )
    add_check(
        checks,
        "probe_rtd_option_quotes_ok",
        option_ok,
        f"returncode={probes['probe_rtd_option_quotes']['returncode']}",
        critical=True,
    )
    add_check(
        checks,
        "probe_rtd_btg_lista_ok",
        btg_ok,
        f"returncode={probes['probe_rtd_btg_lista']['returncode']}",
        critical=False,
    )

    sheets = option_json.get("sheets") or []
    selected_sheet = option_json.get("selected_sheet")
    headers = option_json.get("headers") or []
    missing_headers = [h for h in REQUIRED_OPTION_HEADERS if h not in headers]

    add_check(
        checks,
        "workbook_contem_aba_rtd_option_quotes",
        "RTD_OPTION_QUOTES" in sheets,
        f"sheets={sheets}",
        critical=True,
    )
    add_check(
        checks,
        "aba_rtd_option_quotes_selecionada",
        selected_sheet == "RTD_OPTION_QUOTES",
        f"selected_sheet={selected_sheet}",
        critical=True,
    )
    add_check(
        checks,
        "headers_obrigatorios_rtd_option_quotes",
        not missing_headers,
        "ok" if not missing_headers else f"faltando={missing_headers}",
        critical=True,
    )
    add_check(
        checks,
        "rtd_option_quotes_tem_linhas",
        int(option_json.get("row_count") or 0) >= 2,
        f"row_count={option_json.get('row_count')}",
        critical=True,
    )
    add_check(
        checks,
        "rtd_option_quotes_tem_colunas",
        int(option_json.get("col_count") or 0) >= len(REQUIRED_OPTION_HEADERS),
        f"col_count={option_json.get('col_count')}",
        critical=True,
    )

    report = {
        "generated_at_local": generated_at,
        "project_root": str(root),
        "evidence_dir": relative_to_root(evidence_dir, root),
        "frente_dir": relative_to_root(frente_dir, root),
        "frente_output_dir": relative_to_root(frente_output_dir, root),
        "git": {
            "branch": branch,
            "status_short": git_status,
        },
        "checks": checks,
        "probes": probes,
        "evidence_files": evidence_files,
    }

    report_json_path = evidence_path("retomada_check.json")
    report_md_path = evidence_path("retomada_check.md")

    write_json(report_json_path, report)
    write_text(report_md_path, build_markdown_report(report))

    failed_critical = [c for c in checks if c["critical"] and not c["ok"]]
    failed_non_critical = [c for c in checks if not c["critical"] and not c["ok"]]

    print(f"EVIDENCE_DIR={relative_to_root(evidence_dir, root)}")
    print(f"REPORT_JSON={relative_to_root(report_json_path, root)}")
    print(f"REPORT_MD={relative_to_root(report_md_path, root)}")

    if failed_critical:
        print("STATUS=FALHA_CRITICA")
        for check in failed_critical:
            print(f"FALHA_CRITICA={check['name']} | {check.get('detail', '')}")
    elif failed_non_critical:
        print("STATUS=OK_COM_ALERTAS")
        for check in failed_non_critical:
            print(f"ALERTA={check['name']} | {check.get('detail', '')}")
    else:
        print("STATUS=OK")

    if args.strict and failed_critical:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
