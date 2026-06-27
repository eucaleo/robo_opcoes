from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re
import subprocess
import sys


PATTERN = (
    r"pre[cç]o.?ref|preco_ref|reference.?price|"
    r"spot_ref|spot.?ref|Preço ref|Preco ref|preco ref|pl_at_spot_ref"
)


def run_git_grep() -> list[str]:
    cmd = [
        "git",
        "grep",
        "-n",
        "-I",
        "-E",
        PATTERN,
        "--",
        ".",
        ":!docs/**",
        ":!reports/**",
    ]

    proc = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
    )

    if proc.returncode not in (0, 1):
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)

    return proc.stdout.splitlines()


def classify(path: str, content: str) -> str:
    lower_path = path.lower()
    lower = content.lower()

    if lower_path.startswith("att/tests/"):
        return "TESTE_FIXTURE_OU_EXPECTATIVA"

    if lower_path.startswith("db/") or path == "create_payoff_summary_table.py":
        return "PERSISTENCIA_COMPATIBILIDADE"

    if lower_path.startswith("domain/"):
        return "DOMINIO_CALCULO_INTERNO"

    if lower_path.startswith("services/"):
        return "SERVICO_PAYLOAD_INTERNO"

    if lower_path.startswith("ui/"):
        if re.search(r"preço ref|preco ref", lower):
            return "UI_LABEL_BLOQUEANTE"

        if "preço base atual" in lower or "preco base atual" in lower:
            return "UI_LABEL_ATUALIZADO"

        return "UI_NOME_INTERNO_COMPATIBILIDADE"

    if lower_path.startswith("scripts/"):
        if "seed_" in lower_path:
            return "SCRIPT_SEED_DADOS_TESTE"

        return "SCRIPT_DIAGNOSTICO_OU_AUDITORIA"

    return "A_CLASSIFICAR"


def build_report(groups: dict[str, list[tuple[str, str, str]]]) -> Path:
    out_dir = Path("reports/payoff_conferencia")
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = out_dir / f"classificacao_nomenclatura_preco_payoff_{stamp}.txt"

    with out_file.open("w", encoding="utf-8") as f:
        f.write("Classificacao de nomenclatura de preco no payoff\n")
        f.write(f"Gerado em: {datetime.now().isoformat(timespec='seconds')}\n")
        f.write("Escopo: codigo versionado, excluindo docs e reports\n")
        f.write("\n")

        f.write("Resumo por classe\n")
        f.write("=================\n")

        for cls in sorted(groups):
            f.write(f"{cls}: {len(groups[cls])}\n")

        f.write("\n")

        for cls in sorted(groups):
            f.write("\n")
            f.write(cls + "\n")
            f.write("=" * len(cls) + "\n")

            for path, line_no, content in groups[cls]:
                f.write(f"{path}:{line_no}: {content}\n")

    return out_file


def main() -> int:
    lines = run_git_grep()
    groups: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

    for line in lines:
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue

        path, line_no, content = parts
        cls = classify(path, content)
        groups[cls].append((path, line_no, content))

    out_file = build_report(groups)

    print(f"Relatorio gerado em: {out_file}")
    print("")
    print("Resumo por classe")
    print("=================")

    for cls in sorted(groups):
        print(f"{cls}: {len(groups[cls])}")

    blockers = groups.get("UI_LABEL_BLOQUEANTE", [])

    if blockers:
        print("")
        print("ATENCAO: existem labels bloqueantes na UI.")

        for path, line_no, content in blockers:
            print(f"{path}:{line_no}: {content}")

        return 2

    print("")
    print("OK: nenhuma ocorrencia classificada como UI_LABEL_BLOQUEANTE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
