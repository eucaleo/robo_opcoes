#!/bin/bash
# =====================================================================
# 7_fix_duplicate_recursive_methods.sh
# Corrige metodos duplicados/self-recursivos em derived_service.py
# Toda saida (logs, backups, script auxiliar) fica isolada em:
#   C:\Users\eucal\projeto\ATT\CORRECAO_UI
# Uso:
#   bash 7_fix_duplicate_recursive_methods.sh "/c/Users/eucal/projeto"
# =====================================================================

PROJ="${1:-.}"
WORKDIR="/c/Users/eucal/projeto/ATT/CORRECAO_UI"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$WORKDIR/backup_$TS"
LOG="$WORKDIR/7_fix_duplicate_recursive_methods_$TS.log"
PYHELPER="$WORKDIR/_fix_helper.py"

mkdir -p "$WORKDIR"
mkdir -p "$BACKUP_DIR"

{
  echo "==================================================="
  echo "FIX AUTOMATICO - metodos duplicados/self-recursivos"
  echo "Data: $(date)"
  echo "Projeto alvo: $PROJ"
  echo "Backup em: $BACKUP_DIR"
  echo "==================================================="
  echo ""
} > "$LOG"

# ---------------------------------------------------------------------
# Gera o script Python auxiliar como ARQUIVO SEPARADO (evita problema
# de heredoc quebrar no Git Bash / MINGW)
# ---------------------------------------------------------------------
cat > "$PYHELPER" << 'PYEOF'
import sys, re, shutil, os

log_path = sys.argv[1]
backup_dir = sys.argv[2]
cases = sys.argv[3:]

def log(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

any_error = False

for case in cases:
    try:
        file_path, func_name = case.split("|")
    except ValueError:
        log(f"[ERRO] Caso mal formatado: {case}")
        any_error = True
        continue

    if not os.path.isfile(file_path):
        log(f"[SKIP] Arquivo nao encontrado: {file_path}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    def_pattern = re.compile(r"^(\s*)def " + re.escape(func_name) + r"\(")
    def_lines = [(i, def_pattern.match(l).group(1)) for i, l in enumerate(lines) if def_pattern.match(l)]

    if len(def_lines) < 2:
        log(f"[SKIP] '{func_name}' em {file_path} nao esta duplicada (ou ja corrigida).")
        continue

    last_idx, indent = def_lines[-1]

    end_idx = last_idx + 1
    while end_idx < len(lines):
        line = lines[end_idx]
        if line.strip() == "":
            end_idx += 1
            continue
        current_indent = len(line) - len(line.lstrip(" "))
        if current_indent <= len(indent):
            break
        end_idx += 1

    block = "".join(lines[last_idx:end_idx])

    if f"{func_name}(" not in block.split("\n", 1)[-1]:
        log(f"[ATENCAO] '{func_name}' em {file_path} duplicada, mas NAO parece stub self-recursivo. Revisao manual necessaria.")
        continue

    rel_name = os.path.basename(file_path)
    shutil.copy2(file_path, os.path.join(backup_dir, rel_name))

    new_lines = lines[:last_idx] + lines[end_idx:]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    log(f"[OK] Removido stub duplicado de '{func_name}' em {file_path} (linhas {last_idx+1}-{end_idx}).")
    log(f"     Mantida a definicao original (com logica real) na primeira ocorrencia.")
    log("")

log("===================================================")
if any_error:
    log("Fix concluido COM AVISOS. Verifique mensagens [ERRO]/[ATENCAO] acima.")
else:
    log("Fix concluido com sucesso.")
log(f"Backups do(s) arquivo(s) original(is) em: {backup_dir}")
log("Revise o diff antes de commitar!")
log("===================================================")
PYEOF

# ---------------------------------------------------------------------
# Verifica se python esta disponivel (python3 ou python)
# ---------------------------------------------------------------------
PYEXE=""
if command -v python3 >/dev/null 2>&1; then
    PYEXE="python3"
elif command -v python >/dev/null 2>&1; then
    PYEXE="python"
else
    echo "[ERRO] Python nao encontrado no PATH. Instale/ajuste o PATH e tente novamente." | tee -a "$LOG"
    echo ""
    echo "Pressione ENTER para fechar..."
    read _dummy
    exit 1
fi

echo "[INFO] Usando interpretador: $PYEXE" | tee -a "$LOG"

# ---------------------------------------------------------------------
# Executa o helper Python (sem heredoc, sem set -e, com tratamento de erro)
# ---------------------------------------------------------------------
"$PYEXE" "$PYHELPER" "$LOG" "$BACKUP_DIR" \
  "$PROJ/services/derived_service.py|get_payoff_by_structure_id" \
  "$PROJ/services/derived_service.py|save_payoff_curve"

PYEXIT=$?

echo ""
if [ $PYEXIT -ne 0 ]; then
    echo "[ERRO] O script Python terminou com codigo $PYEXIT. Veja o log:"
else
    echo "[SUCESSO] Processo finalizado. Veja o log:"
fi
echo "  $LOG"
echo ""
echo "Backup dos arquivos originais em:"
echo "  $BACKUP_DIR"
echo ""
echo "Pressione ENTER para fechar esta janela..."
read _dummy
