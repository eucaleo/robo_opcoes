"""
patch_72_structure_audit_log.py
===============================
Registra formalmente o patch_72 no projeto ATT.

Escopo:
  - Tabela structure_audit_log com registro automático de ações
    create, update, archive, add_leg e replace_legs.
  - Método _log_action() privado para inserção atômica dentro
    da transação principal.
  - get_audit_log() e get_full_audit_log() para consulta filtrada
    por structure_id, action e limit.
  - ensure_structures_schema atualizado com CREATE TABLE IF NOT EXISTS
    e índices idx_audit_log_structure_id e idx_audit_log_changed_at.
  - Snapshot before/after em JSON para cada entrada.
  - Atomicidade garantida: falha na operação principal não grava log;
    log não bloqueia operação em caso de erro interno.
  - Sem sqlite3 legado importado diretamente.
  - 37 passed em pytest.
"""

PATCH_ID = "patch_72"
PATCH_DESC = (
    "StructuresRepository: tabela structure_audit_log com registro automatico "
    "de acoes create, update, archive, add_leg e replace_legs; metodo log_action() "
    "privado para insercao atomica dentro da transacao principal; get_audit_log() "
    "e get_full_audit_log() para consulta filtrada por structure_id, action e limit; "
    "ensure_structures_schema atualizado com CREATE TABLE IF NOT EXISTS e indices "
    "idx_audit_log_structure_id e idx_audit_log_changed_at; snapshot before/after "
    "em JSON para cada entrada; atomicidade garantida: falha na operacao principal "
    "nao grava log, log nao bloqueia operacao em caso de erro interno; "
    "sem sqlite3 legado importado diretamente; 37 passed em pytest."
)


def run(dry_run: bool = False) -> None:
    """Ponto de entrada do patch. Apenas documenta — sem migrações DDL aqui."""
    print(f"[{PATCH_ID}] {PATCH_DESC}")
    if dry_run:
        print(f"[{PATCH_ID}] dry-run: nenhuma alteração aplicada.")
    else:
        print(f"[{PATCH_ID}] registrado com sucesso.")


if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv
    run(dry_run=dry)
