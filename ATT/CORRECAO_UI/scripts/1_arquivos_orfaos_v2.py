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
