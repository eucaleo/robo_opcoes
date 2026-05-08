import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(p: Path):
    b = p.with_suffix(p.suffix + f".backup_debug_{TS}")
    b.write_bytes(p.read_bytes())
    print(f"[FIX_DEBUG] Backup: {b}")

def ensure_import_once(text: str, import_line: str) -> str:
    if import_line in text:
        return text
    lines = text.splitlines(True)
    # acha o último bloco de imports no topo
    last_imp = -1
    for i, ln in enumerate(lines[:200]):  # só no começo do arquivo
        if ln.startswith("import ") or ln.startswith("from "):
            last_imp = i
        elif last_imp != -1 and ln.strip() and not ln.startswith("#"):
            break
    insert_at = last_imp + 1 if last_imp != -1 else 0
    lines.insert(insert_at, import_line + "\n")
    return "".join(lines)

def replace_ui_debug_prints(text: str) -> str:
    # print(f"[UI][DEBUG] ...")
    text = re.sub(
        r'print\(\s*f"\[UI\]\[DEBUG\]\s*(.*?)"\s*\)',
        r'debug(f"\1")',
        text
    )
    # print("[UI][DEBUG]", ...)
    text = re.sub(
        r'print\(\s*"\[UI\]\[DEBUG\]"\s*,\s*(.*?)\)',
        r'debug(\1)',
        text
    )
    return text

def replace_payoffchart_prints(text: str) -> str:
    # print("[PayoffChart] DEBUG ...")
    text = re.sub(
        r'print\(\s*"\[PayoffChart\]\s*(DEBUG|FIX|CLEAR)\s*(.*?)"\s*(,.*?)?\)',
        lambda m: 'payoff_debug(' + '"{}{}"'.format(
            (m.group(1) + " ") if m.group(1) else "",
            m.group(2)
        ) + (m.group(3) or "") + ')',
        text
    )
    # print(f"[PayoffChart] DEBUG ...")
    text = re.sub(
        r'print\(\s*f"\[PayoffChart\]\s*(DEBUG|FIX|CLEAR)\s*(.*?)"\s*(,.*?)?\)',
        lambda m: 'payoff_debug(' + 'f"{}{}"'.format(
            (m.group(1) + " ") if m.group(1) else "",
            m.group(2)
        ) + (m.group(3) or "") + ')',
        text
    )
    return text

def write_if_changed(p: Path, new: str):
    old = p.read_text(encoding="utf-8")
    if old == new:
        print(f"[FIX_DEBUG] (no-op) {p.relative_to(ROOT)}")
        return
    p.write_text(new, encoding="utf-8")
    print(f"[FIX_DEBUG] ✅ Atualizado: {p.relative_to(ROOT)}")

def main():
    main_window = ROOT / "UI" / "main_window.py"
    payoff_chart = ROOT / "UI" / "components" / "payoff_chart.py"

    for p in (main_window, payoff_chart):
        if not p.exists():
            print(f"[FIX_DEBUG] ⚠️ Arquivo não encontrado: {p}")
            continue
        backup(p)

    if main_window.exists():
        t = main_window.read_text(encoding="utf-8")
        t = ensure_import_once(t, "from UI.debug_utils import debug, info")
        t = replace_ui_debug_prints(t)
        write_if_changed(main_window, t)

    if payoff_chart.exists():
        t = payoff_chart.read_text(encoding="utf-8")
        t = ensure_import_once(t, "from UI.debug_utils import payoff_debug, payoff_info")
        t = replace_payoffchart_prints(t)
        write_if_changed(payoff_chart, t)

    # debug_utils: deixa leitura dinâmica (como você já aplicou)
    debug_utils = ROOT / "UI" / "debug_utils.py"
    if debug_utils.exists():
        # não reescreve se já tem is_debug()
        t = debug_utils.read_text(encoding="utf-8")
        if "def is_debug()" not in t:
            backup(debug_utils)
            debug_utils.write_text(
                '"""\n'
                "debug_utils.py - Controle centralizado de logs da UI\n\n"
                "Env vars:\n"
                "- UI_DEBUG=1    : debug detalhado\n"
                "- UI_DEBUG=0    : silencioso (default)\n"
                '"""\n\n'
                "import os\n\n"
                "def is_debug():\n"
                '    """Lê UI_DEBUG dinamicamente (não congela no import)"""\n'
                '    return os.environ.get("UI_DEBUG", "0").strip() in ("1", "true", "True", "on")\n\n'
                "def debug(*args, **kwargs):\n"
                '    """Log apenas se UI_DEBUG=1"""\n'
                "    if is_debug():\n"
                "        print(\"[UI][DEBUG]\", *args, **kwargs)\n\n"
                "def info(*args, **kwargs):\n"
                '    """Log sempre (info level)"""\n'
                "    print(\"[UI]\", *args, **kwargs)\n\n"
                "def payoff_debug(*args, **kwargs):\n"
                '    """Log de payoff chart apenas se debug ativo"""\n'
                "    if is_debug():\n"
                "        print(\"[PayoffChart] DEBUG\", *args, **kwargs)\n\n"
                "def payoff_info(*args, **kwargs):\n"
                '    """Log de payoff sempre"""\n'
                "    print(\"[PayoffChart]\", *args, **kwargs)\n",
                encoding="utf-8",
            )
            print(f"[FIX_DEBUG] ✅ Atualizado: UI/debug_utils.py")

if __name__ == "__main__":
    main()
