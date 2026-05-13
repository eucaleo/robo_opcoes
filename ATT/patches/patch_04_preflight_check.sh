#!/bin/bash
set -euo pipefail

# Descobre a raiz do repositório a partir de ATT/patches
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

mkdir -p scripts docs

# === Cria o verificador de ambiente ===
cat > scripts/preflight_check_v2.py <<'PY'
#!/usr/bin/env python3
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

class PreflightChecker:
    def __init__(self, repo_root="."):
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0

    def check(self, description, condition, is_warning=False):
        self.checks_total += 1
        if condition:
            self.checks_passed += 1
            print(f"[OK] {description}")
            return True
        else:
            if is_warning:
                print(f"[WARN] {description}")
                self.warnings.append(description)
            else:
                print(f"[ERR] {description}")
                self.errors.append(description)
            return False

    def check_directory_structure(self):
        print("\n=== Estrutura de Diretórios ===")
        essential_dirs = [
            "scripts", "UI", "db", "domain", "services",
            "ATT", "ATT/patches", "docs"
        ]
        for d in essential_dirs:
            self.check(f"Diretório {d} existe", (self.repo_root / d).exists())

    def check_database_files(self):
        print("\n=== Bancos de Dados ===")
        app_db = self.repo_root / "app.db"
        derived_db = self.repo_root / "derived.db"

        self.check("app.db existe", app_db.exists())
        self.check("derived.db existe", derived_db.exists(), is_warning=True)

        if app_db.exists():
            try:
                with sqlite3.connect(app_db) as conn:
                    cur = conn.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = {r[0] for r in cur.fetchall()}

                    self.check("Tabela rtd_analise_robo existe", "rtd_analise_robo" in tables)
                    self.check("Tabela rtd_analise_robo_legs existe", "rtd_analise_robo_legs" in tables)

                    if "rtd_analise_robo" in tables:
                        cur.execute("SELECT COUNT(*) FROM rtd_analise_robo")
                        count = cur.fetchone()[0]
                        self.check(f"rtd_analise_robo tem dados (count={count})", count > 0, is_warning=True)
            except Exception as e:
                self.check(f"Consegue abrir app.db (sqlite3): {e}", False)

    def check_script_files(self):
        print("\n=== Scripts Críticos ===")
        essential = [
            "scripts/run_derived_pipeline.py",
            "bridge_ingest_csv.py",
            "UI/main_window.py",
        ]
        for p in essential:
            self.check(f"Arquivo {p} existe", (self.repo_root / p).exists())

    def check_reports(self):
        print("\n=== Relatórios ===")
        reports_dir = self.repo_root / "ATT" / "reports"
        self.check("ATT/reports existe", reports_dir.exists(), is_warning=True)

        if reports_dir.exists():
            for name in ["sql_report_v3.json", "entrypoints_report_v2.json", "imports_report_v2.json"]:
                rp = reports_dir / name
                self.check(f"{name} existe", rp.exists(), is_warning=True)
                if rp.exists():
                    self.check(f"{name} não vazio", rp.stat().st_size > 10, is_warning=True)

    def check_python_modules(self):
        print("\n=== Python (módulos) ===")
        for mod, warn in [("sqlite3", False), ("tkinter", False), ("pathlib", False), ("pandas", True)]:
            try:
                __import__(mod)
                self.check(f"Módulo {mod} disponível", True)
            except ImportError:
                self.check(f"Módulo {mod} disponível", False, is_warning=warn)

    def run(self):
        print(f"Preflight Check v2 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Repo: {self.repo_root.resolve()}")

        self.check_directory_structure()
        self.check_database_files()
        self.check_script_files()
        self.check_reports()
        self.check_python_modules()

        print("\n=== Resumo ===")
        print(f"Passou: {self.checks_passed}/{self.checks_total}")
        if self.errors:
            print("ERROS:")
            for e in self.errors:
                print(f" - {e}")
        if self.warnings:
            print("AVISOS:")
            for w in self.warnings:
                print(f" - {w}")

        return 0 if not self.errors else 1

def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    return PreflightChecker(repo_root).run()

if __name__ == "__main__":
    raise SystemExit(main())
PY

# === Wrapper bash ===
cat > scripts/preflight.sh <<'BASH'
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

PYTHON_BIN="${PYTHON_BIN:-python}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

"$PYTHON_BIN" scripts/preflight_check_v2.py
BASH

# === Doc ===
cat > docs/PREFLIGHT_CHECK.md <<'DOC'
# Preflight Environment Check

## Para que serve
Checar se o repositório está “pronto” antes de rodar pipeline/UI:
- diretórios e scripts essenciais existem
- `app.db` existe e tem tabelas base
- relatórios em `ATT/reports` existem (warning se faltar)
- módulos Python básicos disponíveis

## Como usar
```bash
bash scripts/preflight.sh
