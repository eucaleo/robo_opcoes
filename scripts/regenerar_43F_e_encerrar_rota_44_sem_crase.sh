#!/usr/bin/env bash
set -u

python - <<'PY'
from pathlib import Path
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta

ROOT = Path.cwd()

BASE = Path("FRENTE_RTD_EXCEL_BTG_ONLINE")
AUD = BASE / "AUDITORIA_CENTRO_VERDADE_34"
SEQ = AUD / "VERIFICACAO_COMMITS_SEQUENCIA_FULL_43"

OUT43 = SEQ / "43F_CONSOLIDACAO_FINAL_PRE_COMMIT"
OUT44 = SEQ / "44_ENCERRAMENTO_ROTA_CENTRO_VERDADE"

SP_TZ = timezone(timedelta(hours=-3))
NOW = datetime.now(SP_TZ).strftime("%Y-%m-%d %H:%M:%S %z")

FORBIDDEN = [
    "compute_payoff_from_canonical_input",
    "_calculate_payoff_from_legs",
    "_calculate_payoff_points_for_range",
    "_calculate_leg_payoff",
    "_collect_payoff_strikes",
    "_calculate_payoff_spot_range",
    "subprocess.run",
    "subprocess.Popen",
    "os.system",
    "INSERT INTO payoff_curve_points",
    "INSERT INTO structure_decisions",
    "recalculate_payoff_curve_points_once",
]

MANDATORY_DIRS = [
    BASE,
    AUD,
    AUD / "GUARDRAILS_36",
    AUD / "UI_CLEANUP_35",
    AUD / "VERIFICACAO_BACKEND_EXECUTE_PRICING_42",
    SEQ,
    SEQ / "43C_UI_BLOCK_E_PRINTF_FIX",
    SEQ / "43D_UI_TEXT_CLEANUP_E_GUARDRAIL",
    SEQ / "43E_DOCUMENTACAO_ENCERRAMENTO_FASE",
]

PY_COMPILE_FILES = [
    Path("UI/components/details_panel.py"),
    Path("UI/components/structure_editor_dialog.py"),
    Path("UI/main_window.py"),
]

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
}

def clean_text(value):
    text = str(value)
    text = text.replace(chr(96), "'")
    return text

def run_cmd(args):
    try:
        proc = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return proc.returncode, clean_text(proc.stdout)
    except Exception as exc:
        return 999, clean_text(exc)

def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean_text(text), encoding="utf-8")

def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        clean_text(json.dumps(payload, ensure_ascii=False, indent=2)) + "\n",
        encoding="utf-8",
    )

def rel(path):
    return str(path).replace("\\", "/")

def list_relevant_artifacts():
    roots = [
        AUD,
        SEQ,
    ]
    rows = []
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file():
                rows.append(rel(p))
    return rows

def git_info():
    rc_branch, branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    rc_head, head = run_cmd(["git", "rev-parse", "--short", "HEAD"])
    return {
        "branch": branch.strip() if rc_branch == 0 else "indisponivel",
        "head": head.strip() if rc_head == 0 else "indisponivel",
    }

def git_log_full():
    rc, out = run_cmd([
        "git",
        "log",
        "--date=short",
        "--pretty=format:    - %ad | %h | %s",
    ])
    if rc != 0:
        return "    - FALHA ao consultar git log\n" + indent(out)
    return out.strip() + "\n"

def indent(text, spaces=4):
    prefix = " " * spaces
    lines = clean_text(text).splitlines()
    if not lines:
        return prefix + "\n"
    return "\n".join(prefix + line for line in lines) + "\n"

def validate_dirs():
    rows = []
    ok = True
    for d in MANDATORY_DIRS:
        if d.exists() and d.is_dir():
            rows.append("OK: " + rel(d))
        else:
            rows.append("FALHA: ausente: " + rel(d))
            ok = False
    return ok, "\n".join(rows) + "\n"

def validate_diff_check():
    rc, out = run_cmd(["git", "diff", "--check"])
    if rc == 0:
        return True, "OK: git diff --check sem problemas.\n"
    return False, "FALHA: git diff --check encontrou problemas.\n" + out

def validate_py_compile():
    missing = []
    for p in PY_COMPILE_FILES:
        if not p.exists():
            missing.append(rel(p))
    if missing:
        return False, "FALHA: arquivos ausentes para py_compile:\n" + indent("\n".join(missing))

    rc, out = run_cmd([sys.executable, "-m", "py_compile"] + [rel(p) for p in PY_COMPILE_FILES])
    if rc == 0:
        return True, "OK: py_compile final passou.\n"
    return False, "FALHA: py_compile final falhou.\n" + out

def iter_ui_files():
    ui = ROOT / "UI"
    if not ui.exists():
        return
    for current_root, dirs, files in os.walk(ui):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith((".py", ".md", ".txt")):
                yield Path(current_root) / name

def validate_guardrail_ui():
    rows = []
    ok = True

    rows.append("# Guardrail UI final - Rodada 43F")
    rows.append("")
    rows.append("## Tokens fortes proibidos")
    rows.append("")

    files = list(iter_ui_files() or [])

    for token in FORBIDDEN:
        hits = []
        for p in files:
            try:
                txt = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if token in txt:
                hits.append(rel(p.relative_to(ROOT)))

        rows.append("Token analisado: " + token)
        if hits:
            ok = False
            rows.append("Resultado: FALHA, token presente em UI.")
            for h in hits:
                rows.append("    - " + h)
        else:
            rows.append("Resultado: OK, token ausente em UI.")
        rows.append("")

    rows.append("")
    rows.append("## Busca informativa permitida")
    rows.append("")
    info_tokens = [
        "structure_decisions",
        "payoff_curve_points",
        "run_pipeline",
        "fluxo externo legado",
        "processos externos",
    ]

    info_hits = []
    for p in files:
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for n, line in enumerate(lines, start=1):
            if any(tok in line for tok in info_tokens):
                info_hits.append(rel(p.relative_to(ROOT)) + ":" + str(n) + ":" + line)

    if info_hits:
        rows.extend("    " + clean_text(x) for x in info_hits)
    else:
        rows.append("    Sem ocorrencias informativas.")

    return ok, "\n".join(rows) + "\n"

def validate_no_backtick(paths):
    bad = []
    for base in paths:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file():
                txt = p.read_text(encoding="utf-8", errors="replace")
                if chr(96) in txt:
                    bad.append(rel(p))
    if bad:
        return False, "FALHA: arquivos com crase:\n" + "\n".join(bad) + "\n"
    return True, "OK: nenhum arquivo gerado contem crase.\n"

def make_43f(git, dirs_ok, dirs_txt, diff_ok, diff_txt, py_ok, py_txt, guard_ok, guard_txt, status_txt, artifacts):
    OUT43.mkdir(parents=True, exist_ok=True)

    log = []
    log.append("Rodada 43F regenerada sem printf fragil")
    log.append("Data: " + NOW)
    log.append("Raiz: " + rel(ROOT))
    log.append("Branch: " + git["branch"])
    log.append("HEAD: " + git["head"])
    log.append("Saida: " + rel(OUT43))
    log.append("")
    log.append("Controles:")
    log.append("    Diretorios obrigatorios: " + ("OK" if dirs_ok else "FALHA"))
    log.append("    git diff --check: " + ("OK" if diff_ok else "FALHA"))
    log.append("    py_compile: " + ("OK" if py_ok else "FALHA"))
    log.append("    Guardrail UI: " + ("OK" if guard_ok else "FALHA"))
    write_text(OUT43 / "00_log_43F.txt", "\n".join(log) + "\n")

    report = []
    report.append("# Rodada 43F - Consolidacao final pre-commit")
    report.append("")
    report.append("## Resultado")
    report.append("")
    report.append("Status: " + ("OK" if all([dirs_ok, diff_ok, py_ok, guard_ok]) else "FALHA"))
    report.append("")
    report.append("## Escopo")
    report.append("")
    report.append("    - Verificar commits anteriores.")
    report.append("    - Adicionar sequencia full de desenvolvimento e correcao.")
    report.append("    - Conferir artefatos gerados nas pastas da frente RTD e centro de verdade.")
    report.append("    - Reexecutar testes finais antes de qualquer fechamento controlado.")
    report.append("    - Nao executar stage, commit ou push.")
    report.append("    - Gerar documentacao sem crase para evitar arquivo incompleto.")
    report.append("")
    report.append("## Resultado dos controles")
    report.append("")
    report.append("    - Diretorios obrigatorios: " + ("OK" if dirs_ok else "FALHA"))
    report.append("    - git diff --check: " + ("OK" if diff_ok else "FALHA"))
    report.append("    - py_compile: " + ("OK" if py_ok else "FALHA"))
    report.append("    - Guardrail UI: " + ("OK" if guard_ok else "FALHA"))
    report.append("    - Sem crase nos arquivos gerados: validacao executada ao final")
    report.append("")
    report.append("## Decisao")
    report.append("")
    if all([dirs_ok, diff_ok, py_ok, guard_ok]):
        report.append("A fase 43F esta apta para encerramento controlado da rota em rodada 44.")
    else:
        report.append("A fase 43F nao esta apta para encerramento. Corrigir falhas antes da rodada 44.")
    report.append("")
    report.append("## Restricoes mantidas")
    report.append("")
    report.append("    - Sem git add.")
    report.append("    - Sem git commit.")
    report.append("    - Sem git push.")
    write_text(OUT43 / "01_relatorio_consolidacao_final_43F.md", "\n".join(report) + "\n")

    seq_doc = []
    seq_doc.append("# Sequencia full de desenvolvimento e correcao - Rodada 43F")
    seq_doc.append("")
    seq_doc.append("## Objetivo")
    seq_doc.append("")
    seq_doc.append("Consolidar, em ordem historica e tecnica, a frente de centralizacao do payoff no backend, a limpeza da UI, os guardrails e as validacoes finais antes de qualquer commit controlado.")
    seq_doc.append("")
    seq_doc.append("## Centro de verdade consolidado")
    seq_doc.append("")
    seq_doc.append("    UI")
    seq_doc.append("      -> PayoffRefreshCommandService")
    seq_doc.append("        -> PricingExecutionAppService")
    seq_doc.append("          -> PricingExecutionOrchestrationService")
    seq_doc.append("            -> PricingExecutionService")
    seq_doc.append("            -> PricingExecutionPersistenceService")
    seq_doc.append("              -> PricingExecutionsRepository")
    seq_doc.append("              -> SystemSnapshotsRepository")
    seq_doc.append("              -> DerivedPayoffPersistence")
    seq_doc.append("                -> payoff_curve_points")
    seq_doc.append("                -> structure_decisions")
    seq_doc.append("")
    seq_doc.append("## Regra operacional final")
    seq_doc.append("")
    seq_doc.append("    UI:")
    seq_doc.append("      - nao recalcula payoff")
    seq_doc.append("      - nao executa pipeline local")
    seq_doc.append("      - nao abre processos externos para recalc ou pipeline")
    seq_doc.append("      - nao grava payoff_curve_points")
    seq_doc.append("      - nao grava structure_decisions")
    seq_doc.append("      - apenas rele dados persistidos e renderiza")
    seq_doc.append("")
    seq_doc.append("    Backend:")
    seq_doc.append("      - executa pricing")
    seq_doc.append("      - persiste snapshots")
    seq_doc.append("      - persiste payoff derivado")
    seq_doc.append("      - persiste decisoes")
    seq_doc.append("      - valida estruturas active")
    seq_doc.append("")
    seq_doc.append("## Linha do tempo completa dos commits")
    seq_doc.append("")
    seq_doc.append(git_log_full().rstrip())
    write_text(OUT43 / "02_sequencia_full_desenvolvimento_correcao_43F.md", "\n".join(seq_doc) + "\n")

    write_text(OUT43 / "03_commits_anteriores_completos_43F.md", "# Commits anteriores completos - Rodada 43F\n\n" + git_log_full())

    inv = []
    inv.append("Inventario de artefatos relevantes - Rodada 43F")
    inv.append("")
    inv.extend("    - " + a for a in artifacts)
    write_text(OUT43 / "04_inventario_artefatos_relevantes_43F.txt", "\n".join(inv) + "\n")

    tests = []
    tests.append("Testes finais - Rodada 43F")
    tests.append("")
    tests.append("1. git diff --check")
    tests.append(diff_txt.rstrip())
    tests.append("")
    tests.append("2. py_compile arquivos centrais")
    tests.append(py_txt.rstrip())
    write_text(OUT43 / "05_testes_finais_43F.txt", "\n".join(tests) + "\n")

    write_text(OUT43 / "06_guardrail_ui_final_43F.txt", guard_txt)

    status_doc = []
    status_doc.append("Git status e diff final - Rodada 43F")
    status_doc.append("")
    status_doc.append("Branch: " + git["branch"])
    status_doc.append("HEAD: " + git["head"])
    status_doc.append("")
    status_doc.append("## git status --short")
    status_doc.append("")
    status_doc.append(status_txt.rstrip() if status_txt.strip() else "Sem alteracoes reportadas.")
    write_text(OUT43 / "07_git_status_diff_final_43F.txt", "\n".join(status_doc) + "\n")

    matrix = []
    matrix.append("# Matriz de evidencias final - Rodada 43F")
    matrix.append("")
    matrix.append("## Evidencias obrigatorias")
    matrix.append("")
    for name in [
        "00_log_43F.txt",
        "01_relatorio_consolidacao_final_43F.md",
        "02_sequencia_full_desenvolvimento_correcao_43F.md",
        "03_commits_anteriores_completos_43F.md",
        "04_inventario_artefatos_relevantes_43F.txt",
        "05_testes_finais_43F.txt",
        "06_guardrail_ui_final_43F.txt",
        "07_git_status_diff_final_43F.txt",
        "08_matriz_evidencias_final_43F.md",
        "09_resumo_tecnico_43F.json",
    ]:
        matrix.append("    - " + rel(OUT43 / name))
    matrix.append("")
    matrix.append("## Evidencias anteriores verificadas")
    matrix.append("")
    matrix.append(dirs_txt.rstrip())
    matrix.append("")
    matrix.append("## Criterios de encerramento")
    matrix.append("")
    matrix.append("    - Diretorios obrigatorios presentes.")
    matrix.append("    - Sequencia de commits anteriores registrada.")
    matrix.append("    - Sequencia full de desenvolvimento e correcao gerada.")
    matrix.append("    - git diff --check OK.")
    matrix.append("    - py_compile OK.")
    matrix.append("    - Guardrail UI OK.")
    matrix.append("    - Nenhum git add, git commit ou git push executado por este script.")
    matrix.append("    - Arquivos gerados sem crase.")
    write_text(OUT43 / "08_matriz_evidencias_final_43F.md", "\n".join(matrix) + "\n")

    write_json(OUT43 / "09_resumo_tecnico_43F.json", {
        "rodada": "43F",
        "data": NOW,
        "branch": git["branch"],
        "head": git["head"],
        "status": "OK" if all([dirs_ok, diff_ok, py_ok, guard_ok]) else "FALHA",
        "controles": {
            "diretorios_obrigatorios": dirs_ok,
            "git_diff_check": diff_ok,
            "py_compile": py_ok,
            "guardrail_ui": guard_ok,
            "sem_git_add_commit_push": True,
        },
        "saida": rel(OUT43),
    })

def make_44(git, all_ok, dirs_ok, diff_ok, py_ok, guard_ok, status_txt):
    OUT44.mkdir(parents=True, exist_ok=True)

    write_text(OUT44 / "00_log_44.txt", "\n".join([
        "Rodada 44 - Encerramento da rota centro de verdade",
        "Data: " + NOW,
        "Raiz: " + rel(ROOT),
        "Branch: " + git["branch"],
        "HEAD: " + git["head"],
        "Saida: " + rel(OUT44),
        "Status: " + ("OK" if all_ok else "FALHA"),
        "",
    ]))

    termo = []
    termo.append("# Encerramento da rota - Centro de verdade payoff")
    termo.append("")
    termo.append("## Status")
    termo.append("")
    termo.append("Status: " + ("ENCERRADA TECNICAMENTE" if all_ok else "NAO ENCERRADA"))
    termo.append("")
    termo.append("## Escopo encerrado")
    termo.append("")
    termo.append("    - Centralizacao do payoff no backend.")
    termo.append("    - Remocao de calculo local de payoff na UI.")
    termo.append("    - Bloqueio de processos externos e pipeline local na UI.")
    termo.append("    - Leitura UI baseada em dados persistidos.")
    termo.append("    - Persistencia backend de payoff_curve_points e structure_decisions.")
    termo.append("    - Guardrails documentais e tecnicos da rota.")
    termo.append("")
    termo.append("## Decisao")
    termo.append("")
    if all_ok:
        termo.append("A rota exposta no documento de desenvolvimento fica encerrada tecnicamente nesta rodada 44.")
        termo.append("")
        termo.append("A proxima acao permitida e revisao humana do diff, seguida de etapa separada de stage e commit controlado, se aprovado.")
    else:
        termo.append("A rota nao pode ser encerrada porque um ou mais controles finais falharam.")
    termo.append("")
    termo.append("## Restricoes")
    termo.append("")
    termo.append("    - Este encerramento nao executa git add.")
    termo.append("    - Este encerramento nao executa git commit.")
    termo.append("    - Este encerramento nao executa git push.")
    write_text(OUT44 / "01_termo_encerramento_rota_44.md", "\n".join(termo) + "\n")

    checklist = []
    checklist.append("# Checklist de encerramento - Rodada 44")
    checklist.append("")
    checklist.append("    - 43F regenerada sem printf fragil: OK")
    checklist.append("    - Diretorios obrigatorios: " + ("OK" if dirs_ok else "FALHA"))
    checklist.append("    - git diff --check: " + ("OK" if diff_ok else "FALHA"))
    checklist.append("    - py_compile: " + ("OK" if py_ok else "FALHA"))
    checklist.append("    - Guardrail UI: " + ("OK" if guard_ok else "FALHA"))
    checklist.append("    - Sem crase nos artefatos 43F e 44: validado ao final")
    checklist.append("    - Sem git add, commit ou push: OK")
    write_text(OUT44 / "02_checklist_encerramento_44.md", "\n".join(checklist) + "\n")

    decisao = []
    decisao.append("# Decisao operacional - Rodada 44")
    decisao.append("")
    decisao.append("## Resultado")
    decisao.append("")
    decisao.append("    - Resultado: " + ("aprovado para fechamento controlado posterior" if all_ok else "reprovado para fechamento"))
    decisao.append("")
    decisao.append("## Conduta apos esta rodada")
    decisao.append("")
    decisao.append("    - Revisar visualmente os arquivos 43F e 44.")
    decisao.append("    - Confirmar que o diff final contem somente o escopo aprovado.")
    decisao.append("    - Somente em etapa separada executar git add e git commit, se aprovado.")
    write_text(OUT44 / "03_decisao_operacional_44.md", "\n".join(decisao) + "\n")

    evid = []
    evid.append("# Evidencias referenciadas - Rodada 44")
    evid.append("")
    evid.append("## Rodada 43F")
    evid.append("")
    for p in sorted(OUT43.glob("*")):
        if p.is_file():
            evid.append("    - " + rel(p))
    evid.append("")
    evid.append("## Rodada 44")
    evid.append("")
    for name in [
        "00_log_44.txt",
        "01_termo_encerramento_rota_44.md",
        "02_checklist_encerramento_44.md",
        "03_decisao_operacional_44.md",
        "04_evidencias_referenciadas_44.md",
        "05_status_git_pre_commit_44.txt",
        "06_resumo_tecnico_44.json",
    ]:
        evid.append("    - " + rel(OUT44 / name))
    write_text(OUT44 / "04_evidencias_referenciadas_44.md", "\n".join(evid) + "\n")

    status = []
    status.append("Status git pre-commit - Rodada 44")
    status.append("")
    status.append("Branch: " + git["branch"])
    status.append("HEAD: " + git["head"])
    status.append("")
    status.append("## git status --short")
    status.append("")
    status.append(status_txt.rstrip() if status_txt.strip() else "Sem alteracoes reportadas.")
    write_text(OUT44 / "05_status_git_pre_commit_44.txt", "\n".join(status) + "\n")

    write_json(OUT44 / "06_resumo_tecnico_44.json", {
        "rodada": "44",
        "data": NOW,
        "branch": git["branch"],
        "head": git["head"],
        "status": "ENCERRADA_TECNICAMENTE" if all_ok else "NAO_ENCERRADA",
        "controles": {
            "diretorios_obrigatorios": dirs_ok,
            "git_diff_check": diff_ok,
            "py_compile": py_ok,
            "guardrail_ui": guard_ok,
            "sem_git_add_commit_push": True,
        },
        "rota": "centro_de_verdade_payoff",
        "saida": rel(OUT44),
    })

def main():
    print("==> Regenerando 43F e preparando encerramento 44 sem printf fragil")
    print("Data:", NOW)
    print("Raiz:", rel(ROOT))

    OUT43.mkdir(parents=True, exist_ok=True)
    OUT44.mkdir(parents=True, exist_ok=True)

    git = git_info()
    print("Branch:", git["branch"])
    print("HEAD:", git["head"])

    print("")
    print("==> Validando diretorios obrigatorios")
    dirs_ok, dirs_txt = validate_dirs()
    print(dirs_txt.rstrip())

    print("")
    print("==> Gerando inventario de artefatos")
    artifacts = list_relevant_artifacts()

    print("")
    print("==> Executando git diff --check")
    diff_ok, diff_txt = validate_diff_check()
    print(diff_txt.rstrip())

    print("")
    print("==> Executando py_compile")
    py_ok, py_txt = validate_py_compile()
    print(py_txt.rstrip())

    print("")
    print("==> Executando guardrail UI")
    guard_ok, guard_txt = validate_guardrail_ui()
    print("Guardrail UI:", "OK" if guard_ok else "FALHA")

    rc_status, status_txt = run_cmd(["git", "status", "--short"])

    print("")
    print("==> Gerando 43F")
    make_43f(git, dirs_ok, dirs_txt, diff_ok, diff_txt, py_ok, py_txt, guard_ok, guard_txt, status_txt, artifacts)

    all_ok = all([dirs_ok, diff_ok, py_ok, guard_ok])

    print("")
    print("==> Gerando 44 encerramento de rota")
    make_44(git, all_ok, dirs_ok, diff_ok, py_ok, guard_ok, status_txt)

    print("")
    print("==> Validando ausencia de crase nos artefatos gerados")
    no_bt_ok, no_bt_txt = validate_no_backtick([OUT43, OUT44])
    print(no_bt_txt.rstrip())

    if not no_bt_ok:
        raise SystemExit(1)

    if not all_ok:
        print("")
        print("==> Resultado final")
        print("FALHA: controles finais nao passaram. Rota nao encerrada.")
        print("43F:", rel(OUT43))
        print("44:", rel(OUT44))
        raise SystemExit(1)

    print("")
    print("==> Resultado final")
    print("OK: 43F regenerada sem warnings de printf.")
    print("OK: 44 gerada com encerramento tecnico da rota.")
    print("Relatorio 43F:", rel(OUT43 / "01_relatorio_consolidacao_final_43F.md"))
    print("Sequencia 43F:", rel(OUT43 / "02_sequencia_full_desenvolvimento_correcao_43F.md"))
    print("Termo 44:", rel(OUT44 / "01_termo_encerramento_rota_44.md"))
    print("Checklist 44:", rel(OUT44 / "02_checklist_encerramento_44.md"))
    print("Status 44:", rel(OUT44 / "05_status_git_pre_commit_44.txt"))
    print("")
    print("Restricao mantida: nenhum git add, commit ou push foi executado.")

if __name__ == "__main__":
    main()
PY
