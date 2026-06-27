from pathlib import Path

REPLACEMENTS = {
    Path("UI/components/details_panel.py"): {
        'text="Preço ref.:"': 'text="Preço base atual:"',
    },
    Path("UI/components/payoff_chart.py"): {
        'label="Preço ref.",': 'label="Preço base atual",',
        'f"Preço ref.: {_fmt_number_br(spot_ref, 2)}\\n"':
            'f"Preço base atual: {_fmt_number_br(spot_ref, 2)}\\n"',
    },
}

changed = []

for path, replacements in REPLACEMENTS.items():
    if not path.exists():
        print(f"AVISO: arquivo nao encontrado: {path}")
        continue

    original = path.read_text(encoding="utf-8")
    updated = original

    for old, new in replacements.items():
        updated = updated.replace(old, new)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        changed.append(str(path))
        print(f"Atualizado: {path}")
    else:
        print(f"Sem alteracao: {path}")

if changed:
    print("")
    print("Arquivos alterados:")
    for item in changed:
        print(f"- {item}")
else:
    print("")
    print("Nenhum arquivo alterado.")
