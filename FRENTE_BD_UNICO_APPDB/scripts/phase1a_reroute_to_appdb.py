from pathlib import Path

ROOT = Path.cwd()

changed = []


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def patch_file(rel: str, replacements: list[tuple[str, str]]) -> None:
    path = ROOT / rel
    if not path.exists():
        print(f"[SKIP] {rel} inexistente")
        return

    original = read_text(path)
    text = original

    for old, new in replacements:
        text = text.replace(old, new)

    if text != original:
        write_text(path, text)
        changed.append(rel)
        print(f"[OK] alterado: {rel}")
    else:
        print(f"[NOOP] sem mudanca: {rel}")


def patch_db_config() -> None:
    rel = "db/config.py"
    path = ROOT / rel

    if not path.exists():
        print(f"[SKIP] {rel} inexistente")
        return

    original = read_text(path)
    text = original

    old_line = 'DERIVED_DB_PATH = Path(os.getenv("DERIVED_DB_PATH", str(_PROJECT_ROOT / "dados/derived.db"))).resolve()'
    new_block = '''APP_DB_PATH = Path(os.getenv("APP_DB_PATH", str(_PROJECT_ROOT / "dados/app.db"))).resolve()

# Compatibilidade temporaria:
# APIs legadas ainda importam DERIVED_DB_PATH/get_derived_connection,
# mas o arquivo fisico canonico passa a ser dados/app.db.
DERIVED_DB_PATH = APP_DB_PATH'''

    if "APP_DB_PATH" not in text and old_line in text:
        text = text.replace(old_line, new_block)

    text = text.replace("DERIVED_DB_PATH.parent.mkdir(parents=True, exist_ok=True)", "APP_DB_PATH.parent.mkdir(parents=True, exist_ok=True)")
    text = text.replace("sqlite3.connect(str(DERIVED_DB_PATH))", "sqlite3.connect(str(APP_DB_PATH))")

    # Fallback conservador caso o arquivo tenha formato ligeiramente diferente.
    text = text.replace('str(_PROJECT_ROOT / "dados/derived.db")', 'str(_PROJECT_ROOT / "dados/app.db")')
    text = text.replace('"dados/derived.db"', '"dados/app.db"')
    text = text.replace("'dados/derived.db'", "'dados/app.db'")

    if text != original:
        write_text(path, text)
        changed.append(rel)
        print(f"[OK] alterado: {rel}")
    else:
        print(f"[NOOP] sem mudanca: {rel}")


COMMON_PATH_REPLACEMENTS = [
    ('"dados/derived.db"', '"dados/app.db"'),
    ("'dados/derived.db'", "'dados/app.db'"),
    ('/ "dados" / "derived.db"', '/ "dados" / "app.db"'),
    ("/ 'dados' / 'derived.db'", "/ 'dados' / 'app.db'"),
    ("Default: dados/derived.db", "Default: dados/app.db"),
    ("default: dados/derived.db", "default: dados/app.db"),
    ("dados/derived.db.", "dados/app.db."),
    ("dados/derived.db`", "dados/app.db`"),
]


patch_db_config()

for rel in [
    "repositories/rtd_option_quotes_repository.py",
    "db/derived_repo.py",
    "db/reader.py",
    "db/writer.py",
    "domain/payoff_features.py",
    "UI/components/structure_editor_dialog.py",
    "UI/components/details_panel.py",
    "UI/models/ui_data.py",
    "ATT/tests/conftest.py",
    "ATT/tests/test_ui_data_migration.py",
    "ATT/tests/test_structure_editor_integration.py",
    "ATT/checks/check_end_to_end.py",
    "ATT/checks/check_structures.py",
    "scripts/purge_derived_snapshots.py",
    "scripts/repair_derived_db_consistency.py",
    "scripts/validate_derived_db.py",
    "db/migrations/add_structure_id_to_payoff_curve_points.py",
]:
    patch_file(rel, COMMON_PATH_REPLACEMENTS)

print()
print("===== RESUMO =====")
if changed:
    for rel in changed:
        print(f"CHANGED {rel}")
else:
    print("Nenhum arquivo alterado.")
