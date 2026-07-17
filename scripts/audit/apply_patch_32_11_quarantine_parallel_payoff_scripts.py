from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path.cwd()
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = ROOT / "scripts" / "recalculate_payoff_curve_points_once.py"

REPORT_JSON = OUT_DIR / "RELATORIO_32_11_PATCH_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.json"
REPORT_MD = OUT_DIR / "RELATORIO_32_11_PATCH_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.md"

HEADER = '''"""
ATENCAO - MANUTENCAO / EMERGENCIA

Este script nao e fluxo oficial de recalculo de payoff.
Este script nao deve ser chamado pela UI.
Este script nao deve substituir PayoffRefreshCommandService.
Este script nao deve ser usado como motor produtivo.

Classificacao:
maintenance / legacy / emergencia

Fluxo oficial:
UI -> PayoffRefreshCommandService -> PricingExecutionAppService

Regras:
- usar somente com backup;
- usar somente em manutencao controlada;
- validar persistencia depois da execucao;
- nao criar dependencia da UI para este script.

NAO E FLUXO OFICIAL.
"""
'''


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


status = "ok"
error = None
backup_path = None
changed = False

try:
    if not TARGET.exists():
        status = "error"
        error = f"Arquivo nao encontrado: {TARGET}"
    else:
        text = TARGET.read_text(encoding="utf-8", errors="replace")

        if "ATENCAO - MANUTENCAO / EMERGENCIA" in text:
            changed = False
        else:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup = TARGET.with_name(TARGET.name + f".bak_32_11_{stamp}")
            shutil.copy2(TARGET, backup)
            backup_path = rel(backup)

            lines = text.splitlines(keepends=True)
            insert_at = 0

            if lines and lines[0].startswith("#!"):
                insert_at = 1

            if insert_at < len(lines):
                low = lines[insert_at].lower()
                if "coding" in low or "encoding" in low:
                    insert_at += 1

            new_text = "".join(lines[:insert_at])
            if new_text and not new_text.endswith("\n\n"):
                if new_text.endswith("\n"):
                    new_text += "\n"
                else:
                    new_text += "\n\n"

            new_text += HEADER + "\n"
            new_text += "".join(lines[insert_at:])

            TARGET.write_text(new_text, encoding="utf-8")
            changed = True

except Exception as exc:
    status = "error"
    error = repr(exc)

report = {
    "status": status,
    "objective": "Aplicar cabecalho de quarentena no script paralelo de payoff.",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "target": rel(TARGET),
    "changed": changed,
    "backup_path": backup_path,
    "error": error,
    "conclusion": (
        "Script paralelo classificado como manutencao, legado ou emergencia. "
        "Fluxo oficial permanece via PayoffRefreshCommandService."
    ),
}

REPORT_JSON.write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

md_lines = [
    "# Relatorio 32.11 - Patch quarentena scripts paralelos de payoff",
    "",
    f"Status: {status}",
    "",
    "Objetivo",
    "",
    "Aplicar cabecalho de quarentena no script paralelo de payoff.",
    "",
    "Arquivo alterado",
    "",
    f"- {rel(TARGET)}",
    "",
    "Resultado",
    "",
    f"- changed: {changed}",
    f"- backup_path: {backup_path}",
    f"- error: {error}",
    "",
    "Conclusao",
    "",
    report["conclusion"],
    "",
]

REPORT_MD.write_text("\n".join(md_lines), encoding="utf-8")

print(f"OK: relatorio JSON gerado em {REPORT_JSON}")
print(f"OK: relatorio MD gerado em {REPORT_MD}")
print(f"Status 32.11 patch: {status}")
