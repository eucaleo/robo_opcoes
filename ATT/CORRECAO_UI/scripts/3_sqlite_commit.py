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
