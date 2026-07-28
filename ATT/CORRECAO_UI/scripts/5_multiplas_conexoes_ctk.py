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
