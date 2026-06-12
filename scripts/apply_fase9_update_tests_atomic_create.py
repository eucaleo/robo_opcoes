from pathlib import Path
from datetime import datetime
import shutil
import re

DIALOG_TEST = Path("ATT/tests/test_structure_editor_dialog.py")
INTEGRATION_TEST = Path("ATT/tests/test_structure_editor_integration.py")

for path in (DIALOG_TEST, INTEGRATION_TEST):
    if not path.exists():
        raise SystemExit(f"[ERRO] Arquivo não encontrado: {path}")

backup_dir = Path(f".fase9_tests_backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
backup_dir.mkdir(exist_ok=True)

for path in (DIALOG_TEST, INTEGRATION_TEST):
    shutil.copy2(path, backup_dir / path.name)

print(f"[OK] Backups dos testes criados em {backup_dir}")


def replace_test_function(text: str, name: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(?ms)^    def {re.escape(name)}\(self\):\n"
        rf".*?"
        rf"(?=^    def test_|^class |\Z)"
    )

    if not pattern.search(text):
        raise SystemExit(f"[ERRO] Teste não encontrado: {name}")

    return pattern.sub(replacement.rstrip() + "\n\n", text, count=1)


# ---------------------------------------------------------------------
# ATT/tests/test_structure_editor_dialog.py
# ---------------------------------------------------------------------

dialog_text = DIALOG_TEST.read_text(encoding="utf-8")

dialog_text = replace_test_function(
    dialog_text,
    "test_create_structure_chamado_com_campos_corretos",
    '''
    def test_create_structure_chamado_com_campos_corretos(self):
        dlg = self._make_dialog()
        dlg._f_name.set("PRIO3 Trava")
        dlg._f_underlying.set("PRIO3")
        dlg._f_alias.set("PRIO3")
        dlg._f_status.set("active")
        dlg._f_notes.set("")

        dlg._cmd_save()

        self.mock_repo.create_structure_with_legs.assert_called_once()
        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args

        structure_arg = args[0]

        self.assertEqual(structure_arg["name"], "PRIO3 Trava")
        self.assertEqual(structure_arg["underlying_asset"], "PRIO3")
        self.assertEqual(structure_arg["alias_legacy_aba"], "PRIO3")
        self.assertEqual(structure_arg["status"], "active")
        self.assertEqual(structure_arg["notes"], "")
'''
)

dialog_text = replace_test_function(
    dialog_text,
    "test_replace_legs_chamado_apos_create",
    '''
    def test_replace_legs_chamado_apos_create(self):
        dlg = self._make_dialog()
        dlg._f_name.set("X")
        dlg._f_underlying.set("Y")
        dlg._f_status.set("active")
        dlg._legs_rows = [{
            "position_side": "LONG", "option_type": "CALL", "strike": 100.0,
            "expiration_date": "2026-05-15", "quantity": 1000,
            "premium": None, "multiplier": 1, "symbol": None,
        }]

        dlg._cmd_save()

        self.mock_repo.create_structure_with_legs.assert_called_once()
        args, _kwargs = self.mock_repo.create_structure_with_legs.call_args

        structure_arg = args[0]
        legs_arg = args[1]

        self.assertEqual(structure_arg["name"], "X")
        self.assertEqual(structure_arg["underlying_asset"], "Y")
        self.assertEqual(len(legs_arg), 1)
        self.assertEqual(legs_arg[0]["position_side"], "LONG")
        self.assertEqual(legs_arg[0]["option_type"], "CALL")
        self.assertEqual(legs_arg[0]["strike"], 100.0)
'''
)

DIALOG_TEST.write_text(dialog_text, encoding="utf-8")
print("[OK] test_structure_editor_dialog.py atualizado.")


# ---------------------------------------------------------------------
# ATT/tests/test_structure_editor_integration.py
# ---------------------------------------------------------------------

integration_text = INTEGRATION_TEST.read_text(encoding="utf-8")

integration_text = replace_test_function(
    integration_text,
    "test_exception_nao_propaga",
    '''
    def test_exception_nao_propaga(self):
        dlg = self._dlg(structure_id=None)
        dlg._repo.create_structure_with_legs.side_effect = Exception("DB offline")
        with patch("tkinter.messagebox.showerror"):
            dlg._cmd_save()
        self.assertFalse(dlg.saved)
'''
)

integration_text = replace_test_function(
    integration_text,
    "test_replace_legs_sid_correto_criacao",
    '''
    def test_replace_legs_sid_correto_criacao(self):
        dlg = self._dlg(structure_id=None)
        dlg._repo.create_structure_with_legs.return_value = 77

        dlg._cmd_save()

        dlg._repo.create_structure_with_legs.assert_called_once()
        args, _kwargs = dlg._repo.create_structure_with_legs.call_args

        self.assertEqual(len(args), 2)
        self.assertIsInstance(args[0], dict)
        self.assertEqual(args[1], [])

        dlg._repo.create_structure.assert_not_called()
        dlg._repo.replace_legs.assert_not_called()
'''
)

integration_text = replace_test_function(
    integration_text,
    "test_replace_legs_recebe_2_legs",
    '''
    def test_replace_legs_recebe_2_legs(self):
        dlg = self._dlg_com_legs(structure_id=None)
        dlg._repo.create_structure_with_legs.return_value = 5

        dlg._cmd_save()

        dlg._repo.create_structure_with_legs.assert_called_once()
        args, _kwargs = dlg._repo.create_structure_with_legs.call_args

        legs_arg = args[1]

        self.assertEqual(len(legs_arg), 2)
'''
)

INTEGRATION_TEST.write_text(integration_text, encoding="utf-8")
print("[OK] test_structure_editor_integration.py atualizado.")

print("[OK] Testes atualizados para criação atômica.")
