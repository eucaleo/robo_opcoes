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
