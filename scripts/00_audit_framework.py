"""
Auditoria de framework e stack tecnológica do projeto.
Objetivo: identificar o que já está em uso antes do patch_10.

Execute:
    python scripts/00_audit_framework.py
"""

import sys
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SEP = "=" * 60


def _ok(label, val):
    print(f"  ✓ {label}: {val}")


def _warn(label, val):
    print(f"  ⚠ {label}: {val}")


def _miss(label):
    print(f"  ✗ {label}: NÃO ENCONTRADO")


# ── 1. Python ────────────────────────────────────────────────

def audit_python():
    print(f"\n[1/7] Python")
    _ok("versão", sys.version.split()[0])
    _ok("executável", sys.executable)


# ── 2. Pacotes instalados (pip freeze) ───────────────────────

FRAMEWORKS_DE_INTERESSE = [
    # UI / Web
    "streamlit", "flask", "fastapi", "uvicorn", "django",
    "nicegui", "gradio", "dash", "bottle", "tornado",
    # Templates
    "jinja2",
    # API helpers
    "pydantic", "marshmallow", "attrs",
    # HTTP client
    "requests", "httpx", "aiohttp",
    # DB / ORM
    "sqlalchemy", "alembic", "peewee",
    # Data
    "pandas", "numpy", "openpyxl", "xlrd", "xlwt",
    # Test
    "pytest", "hypothesis",
    # Outros utilitários comuns
    "python-dotenv", "click", "typer", "rich", "loguru",
]

def audit_packages():
    print(f"\n[2/7] Pacotes instalados (relevantes)")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True, text=True
        )
        installed = {
            line.split("==")[0].lower().strip()
            for line in result.stdout.splitlines()
            if "==" in line
        }
        found = []
        for pkg in FRAMEWORKS_DE_INTERESSE:
            if pkg.lower() in installed:
                found.append(pkg)
                _ok("instalado", pkg)
        if not found:
            _warn("nenhum framework de interesse encontrado", "")
    except Exception as e:
        _warn("erro ao checar pacotes", str(e))


# ── 3. Estrutura de pastas relevante ─────────────────────────

DIRS_DE_INTERESSE = [
    "api", "app", "ui", "frontend", "web", "views",
    "templates", "static", "pages", "components",
    "services", "repositories", "domain", "infra",
    "scripts", "patches", "docs", "dados", "BAK",
]

def audit_dirs():
    print(f"\n[3/7] Pastas do projeto")
    for d in DIRS_DE_INTERESSE:
        path = PROJECT_ROOT / d
        if path.exists():
            files = list(path.iterdir())
            _ok(f"/{d}", f"{len(files)} item(s)")
        else:
            _miss(f"/{d}")


# ── 4. Arquivos de entrada / ponto de início do app ──────────

ENTRYPOINTS = [
    "app.py", "main.py", "run.py", "server.py",
    "app/main.py", "app/app.py", "ui/app.py",
    "api/app.py", "api/main.py",
]

def audit_entrypoints():
    print(f"\n[4/7] Possíveis entrypoints do app")
    found_any = False
    for ep in ENTRYPOINTS:
        path = PROJECT_ROOT / ep
        if path.exists():
            size = path.stat().st_size
            _ok(ep, f"{size} bytes")
            # tenta mostrar as primeiras 5 linhas
            try:
                lines = path.read_text(encoding="utf-8").splitlines()[:5]
                for l in lines:
                    if l.strip():
                        print(f"      │ {l}")
            except Exception:
                pass
            found_any = True
    if not found_any:
        _miss("nenhum entrypoint padrão encontrado")


# ── 5. Presença de API já existente ──────────────────────────

API_INDICATORS = [
    "api/", "routes/", "controllers/",
]
API_PATTERNS = [
    "@app.route", "@router.", "app.add_url_rule",
    "APIRouter", "Blueprint", "st.title", "st.sidebar",
    "gr.Interface", "gr.Blocks",
]

def audit_api_presence():
    print(f"\n[5/7] Indicadores de API / UI já existente")
    for pattern in API_PATTERNS:
        hits = []
        for py in PROJECT_ROOT.rglob("*.py"):
            # ignora venv / cache
            if any(p in str(py) for p in [".venv", "venv", "__pycache__", ".git"]):
                continue
            try:
                if pattern in py.read_text(encoding="utf-8", errors="ignore"):
                    hits.append(py.relative_to(PROJECT_ROOT))
            except Exception:
                pass
        if hits:
            _ok(f'"{pattern}" encontrado em', len(hits))
            for h in hits[:4]:
                print(f"      → {h}")
            if len(hits) > 4:
                print(f"      ... +{len(hits) - 4} arquivo(s)")
        else:
            _miss(f'"{pattern}"')


# ── 6. Banco de dados ─────────────────────────────────────────

def audit_databases():
    print(f"\n[6/7] Bancos de dados")
    for db in PROJECT_ROOT.rglob("*.db"):
        if any(p in str(db) for p in [".venv", "venv", "__pycache__"]):
            continue
        size_kb = db.stat().st_size / 1024
        _ok(str(db.relative_to(PROJECT_ROOT)), f"{size_kb:.1f} KB")

    for db in PROJECT_ROOT.rglob("*.sqlite3"):
        if any(p in str(db) for p in [".venv", "venv", "__pycache__"]):
            continue
        size_kb = db.stat().st_size / 1024
        _warn(str(db.relative_to(PROJECT_ROOT)), f"{size_kb:.1f} KB (sqlite3 solto)")


# ── 7. requirements.txt / pyproject.toml ─────────────────────

def audit_requirements():
    print(f"\n[7/7] Arquivos de dependências")
    for fname in ["requirements.txt", "pyproject.toml", "setup.py",
                  "setup.cfg", "Pipfile", "environment.yml"]:
        path = PROJECT_ROOT / fname
        if path.exists():
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            _ok(fname, f"{len(lines)} linha(s)")
            # primeiras linhas relevantes
            for l in lines[:15]:
                if l.strip() and not l.strip().startswith("#"):
                    print(f"      │ {l}")
        else:
            _miss(fname)


# ── main ─────────────────────────────────────────────────────

def main():
    print(SEP)
    print("AUDITORIA DE FRAMEWORK / STACK — projeto")
    print(SEP)

    audit_python()
    audit_packages()
    audit_dirs()
    audit_entrypoints()
    audit_api_presence()
    audit_databases()
    audit_requirements()

    print(f"\n{SEP}")
    print("✅  Auditoria concluída — cole o output acima")
    print(SEP)


if __name__ == "__main__":
    main()
