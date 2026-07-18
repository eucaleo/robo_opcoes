from pathlib import Path
from datetime import datetime

ROOT = Path(".").resolve()
TARGET = ROOT / "services" / "derived_service.py"
REPORT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT = REPORT_DIR / "RELATORIO_32_7_1_FIX_INDENT_DERIVED_SERVICE.md"

def fail(msg):
    raise SystemExit("ERRO: " + msg)

if not TARGET.exists():
    fail("arquivo não encontrado: " + str(TARGET))

text = TARGET.read_text(encoding="utf-8")

backup = TARGET.with_suffix(
    TARGET.suffix + ".bak_32_7_1_" + datetime.now().strftime("%Y%m%d_%H%M%S")
)
backup.write_text(text, encoding="utf-8")

old = """        with connect_app() as conn:
        ensure_derived_tables(conn)
        return insert_structure_decision(
            conn=conn,
            timestamp=ts,
            aba=storage_key,
            decision_dict=enriched_decision,
        )
"""

new = """        with connect_app() as conn:
            ensure_derived_tables(conn)
            return insert_structure_decision(
                conn=conn,
                timestamp=ts,
                aba=storage_key,
                decision_dict=enriched_decision,
            )
"""

if old not in text:
    fail("padrão de indentação quebrada não encontrado em services/derived_service.py")

text = text.replace(old, new, 1)
TARGET.write_text(text, encoding="utf-8")

REPORT.write_text(
    "# Relatório 32.7.1 - Correção de indentação em derived_service.py\n\n"
    "- Arquivo alterado: services/derived_service.py\n"
    "- Backup: " + str(backup.relative_to(ROOT)) + "\n"
    "- Status: indentação corrigida\n\n"
    "Motivo:\n"
    "O patch 32.7 deixou o corpo do bloco with connect_app() sem indentação interna, causando IndentationError.\n\n"
    "Correção:\n"
    "As chamadas ensure_derived_tables(conn) e insert_structure_decision foram recuadas para dentro do bloco with.\n\n"
    "Efeito esperado:\n"
    "services/derived_service.py deve compilar novamente e o teste backend pode prosseguir.\n",
    encoding="utf-8",
)

print("OK: indentação corrigida")
print("OK: relatório gerado em " + str(REPORT))
print("OK: backup criado em " + str(backup))
