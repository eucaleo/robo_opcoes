from pathlib import Path
from datetime import datetime
import shutil
import re

AUDIT_PATH = Path("docs/auditoria_fase_9_cadastro_estruturas.md")
REPO_PATH = Path("repositories/structures_repository.py")
UI_PATH = Path("UI/components/structure_editor_dialog.py")

for path in (AUDIT_PATH, REPO_PATH, UI_PATH):
    if not path.exists():
        raise SystemExit(f"[ERRO] Arquivo não encontrado: {path}")

backup_dir = Path(f".fase9_backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
backup_dir.mkdir(exist_ok=True)

for path in (AUDIT_PATH, REPO_PATH, UI_PATH):
    shutil.copy2(path, backup_dir / path.name)

print(f"[OK] Backups criados em {backup_dir}")

audit_text = AUDIT_PATH.read_text(encoding="utf-8")

audit_append = """
### Correção Fase 9 — criação atômica de estrutura com legs

Diagnóstico:

O fluxo anterior da UI criava primeiro a estrutura e depois gravava as legs em operação separada.
Em caso de falha na gravação das legs, poderia sobrar estrutura persistida sem pernas.

Correção aplicada:

Foi criado método transacional create_structure_with_legs() no repository canônico.
A UI passou a usar esse método no cadastro de nova estrutura.

Arquivos alterados:

- repositories/structures_repository.py
- UI/components/structure_editor_dialog.py

Validação esperada:

- python -m py_compile repositories/structures_repository.py UI/components/structure_editor_dialog.py
- python -m pytest ATT/tests/test_structures_repository.py ATT/tests/test_structure_editor_dialog.py ATT/tests/test_structure_editor_integration.py
"""

if "### Correção Fase 9 — criação atômica de estrutura com legs" in audit_text:
    print("[SKIP] Auditoria já contém registro da correção.")
else:
    AUDIT_PATH.write_text(
        audit_text.rstrip() + "\n\n" + audit_append.strip() + "\n",
        encoding="utf-8",
    )
    print("[OK] Auditoria atualizada.")

repo_text = REPO_PATH.read_text(encoding="utf-8")

method = '''
    def create_structure_with_legs(
        self,
        data: dict[str, Any],
        legs: list[dict[str, Any]],
    ) -> int:
        """
        Cria uma estrutura e suas legs em uma única transação.

        Garante que não exista estrutura persistida sem legs caso a gravação
        de alguma perna falhe.
        """
        payload = _normalize_structure_payload(data)
        validated_legs = [_validate_leg(leg) for leg in legs]

        if not validated_legs:
            raise ValueError("estrutura deve ter ao menos uma leg")

        now = _utc_now_iso()

        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                INSERT INTO structures (
                    name, underlying_asset, alias_legacy_aba,
                    status, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["name"],
                    payload["underlying_asset"],
                    payload["alias_legacy_aba"],
                    payload["status"],
                    payload["notes"],
                    now,
                    now,
                ),
            )
            new_id = int(cursor.lastrowid)

            self._log_action(
                conn,
                structure_id=new_id,
                action="CREATE",
                before=None,
                after={
                    **payload,
                    "id": new_id,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            for leg in validated_legs:
                conn.execute(
                    """
                    INSERT INTO structure_legs (
                        structure_id, position_side, option_type, symbol,
                        strike, expiration_date, quantity, premium,
                        multiplier, leg_order, notes, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        new_id,
                        leg["position_side"],
                        leg["option_type"],
                        leg["symbol"],
                        leg["strike"],
                        leg["expiration_date"],
                        leg["quantity"],
                        leg["premium"],
                        leg["multiplier"],
                        leg["leg_order"],
                        leg["notes"],
                        now,
                        now,
                    ),
                )

            self._log_action(
                conn,
                structure_id=new_id,
                action="REPLACE_LEGS",
                before=None,
                after={
                    "legs_count": len(validated_legs),
                    "replaced_at": now,
                },
            )

            conn.commit()
            return new_id

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

'''

if "def create_structure_with_legs(" in repo_text:
    print("[SKIP] create_structure_with_legs já existe.")
else:
    marker = "    # ------------------------------------------------------------------\n    # READ\n    # ------------------------------------------------------------------"

    if marker in repo_text:
        repo_text = repo_text.replace(marker, method + marker, 1)
    else:
        match = re.search(r"(?m)^    def (list_structures|get_structure)\(", repo_text)
        if not match:
            raise SystemExit("[ERRO] Não encontrei ponto seguro para inserir create_structure_with_legs no repository.")
        repo_text = repo_text[:match.start()] + method + repo_text[match.start():]

    REPO_PATH.write_text(repo_text, encoding="utf-8")
    print("[OK] Método create_structure_with_legs adicionado.")

ui_text = UI_PATH.read_text(encoding="utf-8")

if "create_structure_with_legs(" in ui_text:
    print("[SKIP] UI já usa create_structure_with_legs.")
else:
    pattern = re.compile(
        r"(?ms)^            if self\._structure_id is None:\n"
        r"(?P<body>.*?)"
        r"^            else:"
    )

    match = pattern.search(ui_text)

    if not match:
        raise SystemExit("[ERRO] Bloco if self._structure_id is None não encontrado na UI.")

    body = match.group("body")

    if "create_structure(" not in body or "replace_legs(" not in body:
        raise SystemExit("[ERRO] Bloco de criação antigo não contém create_structure + replace_legs.")

    replacement = (
        "            if self._structure_id is None:\n"
        "                # --- Modo criacao ---\n"
        "                sid = self._repo.create_structure_with_legs(\n"
        "                    structure_data,\n"
        "                    legs_payload,\n"
        "                )\n"
        "            else:"
    )

    ui_text = ui_text[:match.start()] + replacement + ui_text[match.end():]
    UI_PATH.write_text(ui_text, encoding="utf-8")
    print("[OK] UI alterada para criação atômica.")

print("[OK] Alterações aplicadas.")
