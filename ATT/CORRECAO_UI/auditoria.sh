#!/bin/bash
# =====================================================================
# Script de Auditoria Automatizada - Sistema RTD/Excel -> SQLite -> UI
# Execução: bash auditoria.sh
# =====================================================================

set -e

# --- Configuração de caminhos ---
BASE_PROJETO="C:/Users/eucal/projeto"
PASTA_CORRECAO="C:/Users/eucal/projeto/ATT/CORRECAO_UI"
PASTA_SCRIPTS="${PASTA_CORRECAO}/scripts"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PASTA_RESULTADOS="${PASTA_CORRECAO}/resultados/${TIMESTAMP}"

mkdir -p "$PASTA_SCRIPTS"
mkdir -p "$PASTA_RESULTADOS"

echo "======================================================"
echo " Iniciando auditoria em: $TIMESTAMP"
echo " Base do projeto: $BASE_PROJETO"
echo " Resultados serão salvos em: $PASTA_RESULTADOS"
echo "======================================================"

# ---------------------------------------------------------------------
# 1. Geração dos scripts Python de auditoria (gravados em disco)
# ---------------------------------------------------------------------

cat > "${PASTA_SCRIPTS}/1_arquivos_orfaos.py" << 'EOF'
# 1_arquivos_orfaos_v2.py
import ast
import os
import sys

BASE = sys.argv[1]

def listar_py_files(base):
    for root, _, files in os.walk(base):
        if "_deprecated" in root or "resultados" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)

def caminho_para_modulo(caminho, base):
    """Converte caminho de arquivo em dotted path relativo ao BASE."""
    rel = os.path.relpath(caminho, base).replace("\\", "/")
    if rel.endswith("__init__.py"):
        rel = rel[: -len("/__init__.py")]
    else:
        rel = rel[: -len(".py")]
    return rel.replace("/", ".")

def extrair_imports(caminho):
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=caminho)
    except SyntaxError:
        return []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                # import relativo -> resolvido depois usando o pacote do arquivo
                imports.append(("__RELATIVE__", node.level, node.module))
            elif node.module:
                imports.append(node.module)
    return imports

arquivos = list(listar_py_files(BASE))
modulo_de = {a: caminho_para_modulo(a, BASE) for a in arquivos}
modulos_existentes = set(modulo_de.values())

referenciados = set()

for arq in arquivos:
    for imp in extrair_imports(arq):
        if isinstance(imp, tuple):
            # import relativo — resolve com base no pacote do arquivo atual
            _, level, mod = imp
            pacote_atual = modulo_de[arq].split(".")[:-level]
            alvo = ".".join(pacote_atual + ([mod] if mod else []))
            candidatos = [m for m in modulos_existentes if m == alvo or m.startswith(alvo + ".")]
            referenciados.update(candidatos)
        else:
            # import absoluto — casa por prefixo (ex: services.derived_service)
            candidatos = [m for m in modulos_existentes if m == imp or imp.startswith(m + ".") or m.startswith(imp + ".")]
            referenciados.update(candidatos)

print(f"Total de arquivos .py: {len(arquivos)}")
print(f"Total referenciados: {len(referenciados)}\n")

print("=== CANDIDATOS REAIS A ORFAOS (nunca importados) ===\n")
orfaos = []
for a in sorted(arquivos):
    m = modulo_de[a]
    if m not in referenciados and not m.endswith("__init__") and "__main__" not in m:
        orfaos.append(a)
        print(a)

print(f"\nTotal: {len(orfaos)}")
print("\nOBS: entry points (main_window.py, dark_window.py, __main__.py) e arquivos")
print("chamados só por 'python arquivo.py' (scripts standalone) SEMPRE aparecerão")
print("aqui como 'órfãos' — isso é esperado e não indica código morto de verdade.")
EOF

cat > "${PASTA_SCRIPTS}/2_funcoes_duplicadas.py" << 'EOF'
import ast
import os
import sys
from collections import defaultdict

BASE = sys.argv[1]
PALAVRAS_CHAVE = ["vwap", "payoff", "perna", "rtd", "atualiza",
                  "refresh", "grafico", "snapshot", "excel", "sqlite", "conexao"]

def listar_py_files(base):
    for root, _, files in os.walk(base):
        if "_deprecated" in root or "resultados" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)

funcoes_por_nome = defaultdict(list)

for caminho in listar_py_files(BASE):
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=caminho)
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            nome_lower = node.name.lower()
            if any(p in nome_lower for p in PALAVRAS_CHAVE):
                funcoes_por_nome[node.name].append((caminho, node.lineno))

print("=== FUNCOES DUPLICADAS (mesmo nome em arquivos diferentes) ===\n")
duplicadas = 0
for nome, ocorrencias in sorted(funcoes_por_nome.items()):
    if len(ocorrencias) > 1:
        duplicadas += 1
        print(f"[DUPLICADA] {nome}  ({len(ocorrencias)} ocorrencias)")
        for caminho, linha in ocorrencias:
            print(f"     -> {caminho}:{linha}")
        print()

print(f"\nTotal de nomes de funcao duplicados: {duplicadas}")

print("\n=== FUNCOES UNICAS (referencia) ===\n")
for nome, ocorrencias in sorted(funcoes_por_nome.items()):
    if len(ocorrencias) == 1:
        caminho, linha = ocorrencias[0]
        print(f"{nome}: {caminho}:{linha}")
EOF

cat > "${PASTA_SCRIPTS}/3_sqlite_commit.py" << 'EOF'
import re
import os
import sys

BASE = sys.argv[1]

def listar_py_files(base):
    for root, _, files in os.walk(base):
        if "_deprecated" in root or "resultados" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)

padrao_execute = re.compile(r"\.execute\s*\(", re.IGNORECASE)
padrao_executemany = re.compile(r"\.executemany\s*\(", re.IGNORECASE)
padrao_commit = re.compile(r"\.commit\s*\(", re.IGNORECASE)
padrao_connect = re.compile(r"sqlite3\.connect\s*\(", re.IGNORECASE)
padrao_isolation = re.compile(r"isolation_level", re.IGNORECASE)
padrao_wal = re.compile(r"journal_mode", re.IGNORECASE)

print("=== ARQUIVOS COM OPERACOES SQLite ===\n")

alerta_sem_commit = []

for caminho in listar_py_files(BASE):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        conteudo = f.read()

    tem_execute = bool(padrao_execute.search(conteudo)) or bool(padrao_executemany.search(conteudo))
    tem_commit = bool(padrao_commit.search(conteudo))
    tem_connect = bool(padrao_connect.search(conteudo))
    tem_isolation = bool(padrao_isolation.search(conteudo))
    tem_wal = bool(padrao_wal.search(conteudo))

    if tem_execute or tem_connect:
        print(f"{caminho}")
        print(f"   execute/executemany: {tem_execute}")
        print(f"   commit presente:     {tem_commit}")
        print(f"   connect presente:    {tem_connect}")
        print(f"   isolation_level:     {tem_isolation}")
        print(f"   journal_mode (WAL):  {tem_wal}")
        print()

        if tem_execute and not tem_commit:
            alerta_sem_commit.append(caminho)

print("\n=== ALERTA: execute() SEM commit() no mesmo arquivo ===\n")
for a in alerta_sem_commit:
    print(f"[RISCO] {a}")

print(f"\nTotal de arquivos em risco: {len(alerta_sem_commit)}")
EOF

cat > "${PASTA_SCRIPTS}/4_ui_refresh.py" << 'EOF'
import re
import os
import sys

BASE = sys.argv[1]

def listar_py_files(base):
    for root, _, files in os.walk(base):
        if "_deprecated" in root or "resultados" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)

padroes = {
    "after()":            re.compile(r"\.after\s*\("),
    "threading.Thread":   re.compile(r"threading\.Thread\s*\("),
    "canvas.draw":        re.compile(r"canvas\.draw"),
    "mainloop()":         re.compile(r"\.mainloop\s*\("),
    "CTk()":              re.compile(r"CTk\s*\("),
    "queue.Queue":        re.compile(r"queue\.Queue\s*\("),
    "matplotlib Figure":  re.compile(r"Figure\s*\("),
    "ax.clear/cla":       re.compile(r"\.(clear|cla)\s*\("),
    "RTD (win32com/xlwings)": re.compile(r"(win32com|xlwings)"),
}

print("=== MECANISMOS DE REFRESH DE UI POR ARQUIVO ===\n")

resumo = {k: [] for k in padroes}

for caminho in listar_py_files(BASE):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        conteudo = f.read()
    achados = [nome for nome, pad in padroes.items() if pad.search(conteudo)]
    if achados:
        print(f"{caminho}")
        for a in achados:
            print(f"   -> {a}")
            resumo[a].append(caminho)
        print()

print("\n=== RESUMO GLOBAL ===\n")
for nome, arquivos in resumo.items():
    print(f"{nome}: {len(arquivos)} arquivo(s)")
    for a in arquivos:
        print(f"     {a}")
EOF

cat > "${PASTA_SCRIPTS}/5_multiplas_conexoes_ctk.py" << 'EOF'
import re
import os
import sys

BASE = sys.argv[1]

def listar_py_files(base):
    for root, _, files in os.walk(base):
        if "_deprecated" in root or "resultados" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)

padrao_root = re.compile(r"(customtkinter\.CTk|ctk\.CTk|tk\.Tk)\s*\(")

print("=== ARQUIVOS QUE INSTANCIAM JANELA RAIZ (CTk/Tk) ===\n")
print("Objetivo: detectar mais de uma raiz sendo criada no sistema (conflito de UI)\n")

total = 0
for caminho in listar_py_files(BASE):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        linhas = f.readlines()
    for i, linha in enumerate(linhas, 1):
        if padrao_root.search(linha):
            print(f"{caminho}:{i}  ->  {linha.strip()}")
            total += 1

print(f"\nTotal de instanciacoes de janela raiz encontradas: {total}")
print("Se total > 1 em arquivos diferentes de teste, investigar conflito de mainloop.")
EOF

echo ">> Scripts Python gerados em: $PASTA_SCRIPTS"

# ---------------------------------------------------------------------
# 2. Execução dos scripts com captura de saída
# ---------------------------------------------------------------------

echo ""
echo "Executando auditorias..."
echo ""

python "${PASTA_SCRIPTS}/1_arquivos_orfaos.py" "$BASE_PROJETO" \
    > "${PASTA_RESULTADOS}/1_arquivos_orfaos.txt" 2>&1
echo "[OK] 1_arquivos_orfaos.txt"

python "${PASTA_SCRIPTS}/2_funcoes_duplicadas.py" "$BASE_PROJETO" \
    > "${PASTA_RESULTADOS}/2_funcoes_duplicadas.txt" 2>&1
echo "[OK] 2_funcoes_duplicadas.txt"

python "${PASTA_SCRIPTS}/3_sqlite_commit.py" "$BASE_PROJETO" \
    > "${PASTA_RESULTADOS}/3_sqlite_commit.txt" 2>&1
echo "[OK] 3_sqlite_commit.txt"

python "${PASTA_SCRIPTS}/4_ui_refresh.py" "$BASE_PROJETO" \
    > "${PASTA_RESULTADOS}/4_ui_refresh.txt" 2>&1
echo "[OK] 4_ui_refresh.txt"

python "${PASTA_SCRIPTS}/5_multiplas_conexoes_ctk.py" "$BASE_PROJETO" \
    > "${PASTA_RESULTADOS}/5_multiplas_conexoes_ctk.txt" 2>&1
echo "[OK] 5_multiplas_conexoes_ctk.txt"

# ---------------------------------------------------------------------
# 3. Consolidação em relatório único
# ---------------------------------------------------------------------

RELATORIO="${PASTA_RESULTADOS}/RELATORIO_CONSOLIDADO.txt"

{
  echo "############################################################"
  echo "# RELATORIO CONSOLIDADO DE AUDITORIA"
  echo "# Data/Hora: $TIMESTAMP"
  echo "# Base do projeto: $BASE_PROJETO"
  echo "############################################################"
  echo ""

  for arq in "${PASTA_RESULTADOS}"/*.txt; do
    nome=$(basename "$arq")
    if [ "$nome" != "RELATORIO_CONSOLIDADO.txt" ]; then
      echo "===================================================="
      echo "ARQUIVO: $nome"
      echo "===================================================="
      cat "$arq"
      echo ""
      echo ""
    fi
  done
} > "$RELATORIO"

echo ""
echo "======================================================"
echo " Auditoria concluida."
echo " Relatorio consolidado: $RELATORIO"
echo " Pasta de resultados: $PASTA_RESULTADOS"
echo "======================================================"
