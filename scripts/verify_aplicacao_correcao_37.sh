#!/usr/bin/env bash

set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

AUDIT_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_CORRECAO_37"
mkdir -p "$AUDIT_DIR"

TERMINAL_LOG="$AUDIT_DIR/terminal_verificacao_correcao_37.txt"
SUMMARY="$AUDIT_DIR/00_resumo_verificacao_correcao_37.txt"

: > "$SUMMARY"

exec > >(tee "$TERMINAL_LOG") 2>&1

FAIL=0

if command -v python >/dev/null 2>&1; then
    PYTHON_CMD=(python)
elif command -v py >/dev/null 2>&1; then
    PYTHON_CMD=(py -3)
else
    echo "ERRO: python nao encontrado no PATH."
    exit 1
fi

log() {
    echo "$*" | tee -a "$SUMMARY" >/dev/null
}

section() {
    echo
    echo "==> $*"
    echo
    {
        echo
        echo "==> $*"
        echo
    } >> "$SUMMARY"
}

mark_fail() {
    FAIL=1
    log "FALHA: $*"
}

mark_ok() {
    log "OK: $*"
}

run_capture() {
    local title="$1"
    local outfile="$2"
    shift 2

    section "$title"

    {
        echo "COMANDO:"
        printf '%q ' "$@"
        echo
        echo
        "$@"
        local code=$?
        echo
        echo "EXIT_CODE=$code"
        return "$code"
    } > "$outfile" 2>&1

    local code=$?

    cat "$outfile"

    if [ "$code" -ne 0 ]; then
        mark_fail "$title retornou exit code $code"
    else
        mark_ok "$title"
    fi
}

section "verificacao 37 - inicio"
log "Projeto: $ROOT"
log "Saida: $AUDIT_DIR"
log "Python: ${PYTHON_CMD[*]}"
log "Regra: este script nao faz git add, nao faz commit e nao faz push."

section "status git antes da verificacao"
git status --short | tee "$AUDIT_DIR/01_git_status_antes.txt"

section "branch atual"
git branch --show-current | tee "$AUDIT_DIR/02_branch_atual.txt"

section "rodando guardrail oficial existente"
if [ -f "scripts/verify_payoff_center_of_truth_scope.py" ]; then
    run_capture \
        "scripts/verify_payoff_center_of_truth_scope.py" \
        "$AUDIT_DIR/03_guardrail_oficial.txt" \
        "${PYTHON_CMD[@]}" "scripts/verify_payoff_center_of_truth_scope.py"
else
    echo "ERRO: scripts/verify_payoff_center_of_truth_scope.py nao encontrado." | tee "$AUDIT_DIR/03_guardrail_oficial.txt"
    mark_fail "guardrail oficial ausente"
fi

section "varredura objetiva de tokens proibidos na UI"
AUDIT_DIR="$AUDIT_DIR" "${PYTHON_CMD[@]}" - <<'PY' > "$AUDIT_DIR/04_tokens_proibidos_ui.txt" 2>&1
from pathlib import Path
import os
import sys

root = Path.cwd()
ui_root = root / "UI"

tokens = [
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
]

ignore_dirs = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "FRENTE_RTD_EXCEL_BTG_ONLINE",
}

findings = []

if not ui_root.exists():
    print("ERRO: pasta UI nao encontrada.")
    sys.exit(1)

for path in ui_root.rglob("*.py"):
    rel_parts = set(path.relative_to(root).parts)
    if rel_parts & ignore_dirs:
        continue

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        findings.append((str(path.relative_to(root)), 0, "ERRO_LEITURA", str(exc)))
        continue

    lines = text.splitlines()

    for index, line in enumerate(lines, start=1):
        line_lower = line.lower()

        for token in tokens:
            if token.lower() in line_lower:
                findings.append(
                    (
                        str(path.relative_to(root)),
                        index,
                        token,
                        line.strip(),
                    )
                )

if findings:
    print("ERRO: tokens proibidos encontrados na UI.")
    print()
    for file_path, line_no, token, line in findings:
        print(f"{file_path}:{line_no}: token={token}: {line}")
    sys.exit(1)

print("OK: nenhum token proibido encontrado na UI.")
sys.exit(0)
PY

TOKENS_CODE=$?
cat "$AUDIT_DIR/04_tokens_proibidos_ui.txt"

if [ "$TOKENS_CODE" -ne 0 ]; then
    mark_fail "UI ainda contem token proibido"
else
    mark_ok "UI sem tokens proibidos"
fi

section "validacao cirurgica do PayoffRefreshCommandService"
AUDIT_DIR="$AUDIT_DIR" "${PYTHON_CMD[@]}" - <<'PY' > "$AUDIT_DIR/05_payoff_refresh_command_service_contrato.txt" 2>&1
from pathlib import Path
import sys

path = Path("services/payoff_refresh_command_service.py")

if not path.exists():
    print("ERRO: services/payoff_refresh_command_service.py nao existe.")
    sys.exit(1)

text = path.read_text(encoding="utf-8", errors="replace")

checks = [
    ("importa PricingExecutionAppService", "PricingExecutionAppService" in text),
    ("chama execute_pricing", "execute_pricing(" in text),
    ("possui guard de active", "_ensure_active_structure" in text or "status != \"active\"" in text or "status != 'active'" in text),
    ("mede timestamp antes", "before_ts" in text or "latest_payoff_timestamp" in text),
    ("mede payoff depois", "after_ts" in text or "_latest_payoff_summary" in text),
    ("conta pontos persistidos", "payoff_points_count" in text or "COUNT(" in text),
    ("verifica decisao", "decision_found" in text or "structure_decisions" in text),
    ("retorna status ok", '"ok"' in text or "'ok'" in text),
    ("retorna status warning", '"warning"' in text or "'warning'" in text),
    ("retorna status error", '"error"' in text or "'error'" in text),
]

failed = False

for label, ok in checks:
    if ok:
        print(f"OK: {label}")
    else:
        print(f"FALHA: {label}")
        failed = True

if failed:
    sys.exit(1)

print()
print("OK: contrato minimo do PayoffRefreshCommandService parece atendido.")
sys.exit(0)
PY

CMD_CODE=$?
cat "$AUDIT_DIR/05_payoff_refresh_command_service_contrato.txt"

if [ "$CMD_CODE" -ne 0 ]; then
    mark_fail "contrato minimo do PayoffRefreshCommandService nao confirmado"
else
    mark_ok "contrato minimo do PayoffRefreshCommandService confirmado"
fi

section "validacao cirurgica do DerivedPayoffPersistence"
AUDIT_DIR="$AUDIT_DIR" "${PYTHON_CMD[@]}" - <<'PY' > "$AUDIT_DIR/06_derived_payoff_persistence_contrato.txt" 2>&1
from pathlib import Path
import sys

path = Path("services/derived_payoff_persistence.py")

if not path.exists():
    print("ERRO: services/derived_payoff_persistence.py nao existe.")
    sys.exit(1)

text = path.read_text(encoding="utf-8", errors="replace")

checks = [
    ("possui classe DerivedPayoffPersistence", "class DerivedPayoffPersistence" in text),
    ("possui metodo persist ou equivalente", "def persist" in text or ".persist(" in text),
    ("possui guard de active", "_is_active_structure" in text or "status == \"active\"" in text or "status == 'active'" in text),
    ("referencia payoff_curve_points", "payoff_curve_points" in text),
    ("referencia structure_decisions", "structure_decisions" in text),
]

failed = False

for label, ok in checks:
    if ok:
        print(f"OK: {label}")
    else:
        print(f"FALHA: {label}")
        failed = True

if failed:
    sys.exit(1)

print()
print("OK: contrato minimo do DerivedPayoffPersistence parece atendido.")
sys.exit(0)
PY

DERIVED_CODE=$?
cat "$AUDIT_DIR/06_derived_payoff_persistence_contrato.txt"

if [ "$DERIVED_CODE" -ne 0 ]; then
    mark_fail "contrato minimo do DerivedPayoffPersistence nao confirmado"
else
    mark_ok "contrato minimo do DerivedPayoffPersistence confirmado"
fi

section "validacao de wiring backend"
AUDIT_DIR="$AUDIT_DIR" "${PYTHON_CMD[@]}" - <<'PY' > "$AUDIT_DIR/07_wiring_backend.txt" 2>&1
from pathlib import Path
import sys

files = [
    Path("services/pricing_execution_orchestration_service.py"),
    Path("services/pricing_execution_persistence_service.py"),
    Path("services/canonical_pricing_facade.py"),
]

combined = ""

for path in files:
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="replace")
        combined += f"\n\n### {path}\n{text}"
    else:
        print(f"AVISO: arquivo nao encontrado: {path}")

checks = [
    ("referencia DerivedPayoffPersistence", "DerivedPayoffPersistence" in combined),
    ("usa payoff_persistence_port", "payoff_persistence_port" in combined),
    ("referencia PricingExecutionPersistenceService", "PricingExecutionPersistenceService" in combined),
    ("referencia SystemSnapshotsRepository", "SystemSnapshotsRepository" in combined),
]

failed = False

for label, ok in checks:
    if ok:
        print(f"OK: {label}")
    else:
        print(f"FALHA: {label}")
        failed = True

print()
print("Ocorrencias relevantes:")
for token in [
    "DerivedPayoffPersistence",
    "payoff_persistence_port",
    "PricingExecutionPersistenceService",
    "SystemSnapshotsRepository",
]:
    count = combined.count(token)
    print(f"{token}: {count}")

if failed:
    sys.exit(1)

sys.exit(0)
PY

WIRING_CODE=$?
cat "$AUDIT_DIR/07_wiring_backend.txt"

if [ "$WIRING_CODE" -ne 0 ]; then
    mark_fail "wiring backend nao confirmado"
else
    mark_ok "wiring backend confirmado"
fi

section "verificacao especifica do subprocess.run em UI/main_window.py"
{
    if [ -f "UI/main_window.py" ]; then
        grep -n "subprocess\.run\|subprocess\.Popen\|os\.system" "UI/main_window.py" || true
    else
        echo "AVISO: UI/main_window.py nao encontrado."
    fi
} | tee "$AUDIT_DIR/08_subprocess_main_window.txt"

if [ -f "UI/main_window.py" ] && grep -q "subprocess\.run\|subprocess\.Popen\|os\.system" "UI/main_window.py"; then
    mark_fail "UI/main_window.py ainda contem chamada subprocess/os.system"
else
    mark_ok "UI/main_window.py sem subprocess.run/subprocess.Popen/os.system"
fi

section "verificacao do painel terminal payoff"
{
    if [ -f "UI/components/terminal_vwap_payoff_dark_panel.py" ]; then
        grep -n \
            "_load_payoff_points\|_load_persisted_payoff_points\|_calculate_payoff_points_for_range\|_calculate_payoff_from_legs\|_calculate_leg_payoff\|_collect_payoff_strikes\|_calculate_payoff_spot_range\|PayoffRefreshCommandService\|MAX(timestamp)\|ORDER BY timestamp" \
            "UI/components/terminal_vwap_payoff_dark_panel.py" || true
    else
        echo "AVISO: UI/components/terminal_vwap_payoff_dark_panel.py nao encontrado."
    fi
} | tee "$AUDIT_DIR/09_terminal_payoff_scope.txt"

section "verificacao de quarentena do script paralelo"
{
    SCRIPT_PATH="scripts/recalculate_payoff_curve_points_once.py"

    if [ -f "$SCRIPT_PATH" ]; then
        grep -n \
            "ATENCAO\|ATENÇÃO\|manutencao\|manutenção\|emergencia\|emergência\|nao e fluxo oficial\|não é fluxo oficial\|PayoffRefreshCommandService" \
            "$SCRIPT_PATH" || true
    else
        echo "AVISO: $SCRIPT_PATH nao encontrado."
    fi
} | tee "$AUDIT_DIR/10_quarentena_script_paralelo.txt"

if [ -f "scripts/recalculate_payoff_curve_points_once.py" ]; then
    if grep -qi "fluxo oficial\|PayoffRefreshCommandService\|manutencao\|manutenção\|emergencia\|emergência" "scripts/recalculate_payoff_curve_points_once.py"; then
        mark_ok "script paralelo possui marcador de quarentena ou referencia ao fluxo oficial"
    else
        mark_fail "script paralelo sem marcador claro de quarentena"
    fi
fi

section "checagem de sintaxe python nos arquivos centrais"
PY_FILES=()

for file in \
    "scripts/verify_payoff_center_of_truth_scope.py" \
    "services/payoff_refresh_command_service.py" \
    "services/derived_payoff_persistence.py" \
    "services/pricing_execution_persistence_service.py" \
    "services/pricing_execution_orchestration_service.py" \
    "services/canonical_pricing_facade.py" \
    "UI/main_window.py" \
    "UI/components/terminal_vwap_payoff_dark_panel.py"
do
    if [ -f "$file" ]; then
        PY_FILES+=("$file")
    fi
done

if [ "${#PY_FILES[@]}" -gt 0 ]; then
    run_capture \
        "py_compile arquivos centrais" \
        "$AUDIT_DIR/11_py_compile_arquivos_centrais.txt" \
        "${PYTHON_CMD[@]}" -m py_compile "${PY_FILES[@]}"
else
    echo "ERRO: nenhum arquivo python central encontrado." | tee "$AUDIT_DIR/11_py_compile_arquivos_centrais.txt"
    mark_fail "nenhum arquivo python central encontrado para py_compile"
fi

section "diff atual sem adicionar ao git"
git diff --stat | tee "$AUDIT_DIR/12_git_diff_stat.txt"
git diff --name-only | tee "$AUDIT_DIR/13_git_diff_name_only.txt"

section "status git depois da verificacao"
git status --short | tee "$AUDIT_DIR/14_git_status_depois.txt"

section "resultado final"

if [ "$FAIL" -eq 0 ]; then
    log "RESULTADO: OK"
    log "A correcao passou na verificacao automatizada 37."
    log "Relatorios gerados em: $AUDIT_DIR"
    echo
    echo "RESULTADO: OK"
    echo "Relatorios gerados em: $AUDIT_DIR"
else
    log "RESULTADO: FALHA"
    log "A correcao ainda nao esta encerrada."
    log "Abra os arquivos 03 a 11 dentro de: $AUDIT_DIR"
    echo
    echo "RESULTADO: FALHA"
    echo "Abra os arquivos 03 a 11 dentro de:"
    echo "$AUDIT_DIR"
fi

echo
echo "IMPORTANTE: nenhum git add, commit ou push foi executado por este script."
echo

if [ -t 0 ]; then
    read -r -p "Pressione ENTER para fechar..."
fi

exit "$FAIL"
