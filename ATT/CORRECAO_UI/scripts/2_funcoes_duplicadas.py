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
