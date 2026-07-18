from __future__ import annotations

import os
import subprocess
from pathlib import Path
from datetime import datetime, date


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "FRENTE_RTD_EXCEL_BTG_ONLINE"
AUDITORIA = TARGET / "AUDITORIA_UI"


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    return p.returncode, p.stdout, p.stderr


def title(txt: str) -> None:
    print()
    print("=" * 80)
    print(txt)
    print("=" * 80)


def main() -> int:
    today = date.today()

    title("CONTEXTO")
    print(f"Root:      {ROOT}")
    print(f"Target:    {TARGET}")
    print(f"Auditoria: {AUDITORIA}")
    print(f"Hoje:      {today.isoformat()}")

    title("1) EXISTENCIA ATUAL DAS PASTAS")
    print(f"Existe FRENTE_RTD_EXCEL_BTG_ONLINE? {TARGET.exists()}")
    print(f"Existe AUDITORIA_UI?                 {AUDITORIA.exists()}")

    if TARGET.exists():
        files = [p for p in TARGET.rglob("*") if p.is_file()]
        print(f"Arquivos atuais dentro de FRENTE_RTD_EXCEL_BTG_ONLINE: {len(files)}")
        for p in files[:80]:
            print(f"  - {p.relative_to(ROOT)}")
        if len(files) > 80:
            print(f"  ... mais {len(files) - 80} arquivos")

    title("2) GIT STATUS --PORCELAIN")
    rc, out, err = run(["git", "status", "--porcelain=v1", "--untracked-files=all"])
    if err.strip():
        print(err.strip())
    if out.strip():
        for line in out.splitlines():
            if "FRENTE_RTD_EXCEL_BTG_ONLINE" in line:
                print(line)
    else:
        print("Sem alterações no working tree.")

    title("3) ARQUIVOS RASTREADOS DELETADOS SEGUNDO O GIT")
    rc, out, err = run(["git", "ls-files", "--deleted"])
    deleted = [
        line for line in out.splitlines()
        if line.startswith("FRENTE_RTD_EXCEL_BTG_ONLINE/")
    ]
    if deleted:
        for line in deleted:
            print(line)
    else:
        print("Nenhum arquivo rastreado deletado nessa pasta segundo git ls-files --deleted.")

    title("4) STASHES EXISTENTES")
    rc, out, err = run(["git", "stash", "list"])
    if not out.strip():
        print("Nenhum stash encontrado.")
    else:
        print(out.strip())

    title("5) ARQUIVOS DA FRENTE ENCONTRADOS DENTRO DOS STASHES")
    if out.strip():
        stash_lines = out.splitlines()
        for line in stash_lines:
            stash_ref = line.split(":", 1)[0].strip()
            print()
            print(f"--- {stash_ref} ---")

            # tracked/modificados no stash normal
            rc1, out1, err1 = run([
                "git", "stash", "show",
                "--name-status",
                "--include-untracked",
                stash_ref,
            ])

            found = False
            for l in out1.splitlines():
                if "FRENTE_RTD_EXCEL_BTG_ONLINE" in l:
                    print(l)
                    found = True

            # untracked podem estar no terceiro parent do stash
            rc2, out2, err2 = run([
                "git", "ls-tree",
                "-r",
                "--name-only",
                f"{stash_ref}^3",
            ])

            if rc2 == 0:
                for l in out2.splitlines():
                    if l.startswith("FRENTE_RTD_EXCEL_BTG_ONLINE/"):
                        print(f"UNTRACKED_IN_STASH\t{l}")
                        found = True

            if not found:
                print("Nenhum arquivo da frente encontrado nesse stash.")

    title("6) BUSCA EM HISTORICO DE SHELL POR COMANDOS rm")
    candidates = []

    home = Path.home()

    # Git Bash / MSYS
    candidates.append(home / ".bash_history")
    candidates.append(home / ".zsh_history")

    # PowerShell PSReadLine
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(
            Path(appdata)
            / "Microsoft"
            / "Windows"
            / "PowerShell"
            / "PSReadLine"
            / "ConsoleHost_history.txt"
        )

    found_rm = False
    for hist in candidates:
        if not hist.exists():
            continue

        try:
            mtime = datetime.fromtimestamp(hist.stat().st_mtime)
            print()
            print(f"Historico: {hist}")
            print(f"Modificado em: {mtime}")

            lines = hist.read_text(errors="ignore").splitlines()
            matches = []
            for i, line in enumerate(lines, start=1):
                low = line.lower()
                if (
                    "rm " in low
                    or low.startswith("rm ")
                    or "remove-item" in low
                    or "del " in low
                    or low.startswith("del ")
                ):
                    if (
                        "frente_rtd_excel_btg_online" in low
                        or "auditoria_ui" in low
                        or "projeto" in low
                    ):
                        matches.append((i, line))

            if matches:
                found_rm = True
                print("Possiveis comandos de remocao relacionados:")
                for i, line in matches[-50:]:
                    print(f"{i}: {line}")
            else:
                print("Nenhum comando rm/del/remove-item relacionado encontrado nesse historico.")

        except Exception as e:
            print(f"Erro lendo {hist}: {e}")

    if not found_rm:
        print()
        print("Nao encontrei comandos rm/del/remove-item relacionados nos historicos locais lidos.")
        print("Obs: .bash_history normalmente nao tem timestamp por comando, entao isso nao prova que nao ocorreu hoje.")

    title("7) RECOMENDACAO")
    print("Se os documentos aparecem como UNTRACKED_IN_STASH no stash@{0}, restaure apenas a pasta assim:")
    print()
    print('  git restore --source=stash@{0}^3 -- "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI"')
    print()
    print("Se o comando acima falhar, use:")
    print()
    print('  git checkout stash@{0}^3 -- "FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI"')
    print()
    print("Depois confira:")
    print()
    print('  git status --short')
    print('  find FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_UI -type f | wc -l')

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
