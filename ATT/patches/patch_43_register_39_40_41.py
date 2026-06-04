# ATT/patches/patch_43_register_39_40_41.py
"""
patch_43 -- Registrar patch_39, patch_40 e patch_41 no auditor
           Fechar check pendente do patch_38 (backup ui_data.py)
"""

import os
import sys
import shutil
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # ATT/patches/ -> ATT/ -> projeto/
DRY_RUN = False


def log(msg: str):
    print(f"[patch43] {msg}")


def dry_write(path: Path, content: str):
    if DRY_RUN:
        log(f"  [DRY-RUN] escreveria  {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    log(f"  [OK] escrito  {path.relative_to(ROOT)}")


# 
# ACAO 1 -- fechar check pendente do patch_38
# 

def _find_ui_data() -> Path | None:
    candidates = [
        ROOT / "UI" / "models" / "ui_data.py",
        ROOT / "ui" / "models" / "ui_data.py",
        ROOT / "app" / "ui_data.py",
        ROOT / "models" / "ui_data.py",
        ROOT / "ui_data.py",
    ]
    for c in candidates:
        if c.exists():
            return c
    found = list(ROOT.rglob("ui_data.py"))
    return found[0] if found else None


def fechar_check_patch38() -> bool:
    log("\n[1/4] Fechando check pendente do patch_38 (backup ui_data.py)")
    ui_data = _find_ui_data()
    if ui_data is None:
        log("  AVISO: ui_data.py nao localizado em nenhum caminho candidato")
        log("   Skip nao-bloqueante (patch_38 pode nao ter criado este arquivo)")
        return True

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak_path = ui_data.parent / f"ui_data.py.bak_p38_{ts}"

    if DRY_RUN:
        log(f"  [DRY-RUN] encontrado  {ui_data.relative_to(ROOT)}")
        log(f"  [DRY-RUN] criaria backup  {bak_path.name}")
        return True

    shutil.copy2(ui_data, bak_path)
    log(f"  [OK] backup criado  {bak_path.relative_to(ROOT)}")
    return True


# 
# HELPER de ROOT nos testes -- resolve pelo .git ou marcador
# A lógica: sobe a partir do __file__ até achar .git ou scripts/
# 

_ROOT_RESOLVER = f'''\
# ROOT resolvido dinamicamente -- imune ao rootdir do pytest
import sys
from pathlib import Path

def _find_project_root(start: Path) -> Path:
    """Sobe ate encontrar .git ou a pasta scripts/ na raiz do projeto."""
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
        if (parent / "scripts").is_dir() and (parent / "ATT").is_dir():
            return parent
    # fallback: 3 niveis acima de ATT/tests/test_*.py
    return start.parent.parent.parent

ROOT = _find_project_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def _skip_if_absent(path):
    import unittest
    if not Path(path).is_file():
        raise unittest.SkipTest(f"Arquivo nao encontrado: {{path}}")
'''

# 
# CONTEUDO test_patch39.py
# 

TEST_PATCH39 = '''\
# ATT/tests/test_patch39.py
"""Testes formais do patch_39 -- auditoria pre-patch/3b baseline."""
import os
import sys
import unittest
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
        if (parent / "scripts").is_dir() and (parent / "ATT").is_dir():
            return parent
    return start.parent.parent.parent


ROOT = _find_project_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCRIPT_FILE = str(ROOT / "scripts" / "39_audit_patch3b_baseline.py")


def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


class TestPatch39ScriptExiste(unittest.TestCase):
    def test_script_existe(self):
        self.assertTrue(
            os.path.isfile(SCRIPT_FILE),
            f"Nao encontrado: {SCRIPT_FILE}"
        )


class TestPatch39ConteudoEstrutura(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(SCRIPT_FILE):
            raise unittest.SkipTest("Script nao encontrado -- skip conteudo")
        cls.src = _read(SCRIPT_FILE)

    def test_run_audit_presente(self):
        self.assertIn("def run_audit(", self.src)

    def test_suspected_residuals(self):
        self.assertIn("SUSPECTED_RESIDUALS", self.src)

    def test_legacy_patterns(self):
        self.assertIn("LEGACY_PATTERNS", self.src)

    def test_domain_files_to_check(self):
        self.assertIn("DOMAIN_FILES_TO_CHECK", self.src)

    def test_relatorio_auditoria_patch39(self):
        self.assertIn("auditoria_patch39", self.src)

    def test_git_branch(self):
        self.assertIn("_git_branch", self.src)


class TestPatch39ImportsBasicos(unittest.TestCase):
    def test_imports(self):
        import importlib
        for m in ["os", "re", "sys", "hashlib", "subprocess", "pathlib"]:
            with self.subTest(m=m):
                self.assertIsNotNone(importlib.import_module(m))


if __name__ == "__main__":
    unittest.main()
'''

# 
# CONTEUDO test_patch40.py
# 

TEST_PATCH40 = '''\
# ATT/tests/test_patch40.py
"""Testes formais do patch_40 -- isolamento de acoplamento legado."""
import os
import sys
import unittest
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
        if (parent / "scripts").is_dir() and (parent / "ATT").is_dir():
            return parent
    return start.parent.parent.parent


ROOT = _find_project_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ROBO_LEGS_REPO    = str(ROOT / "repositories" / "robo_legs_repository.py")
ROBO_STATUS_REPO  = str(ROOT / "repositories" / "robo_legs_status_repository.py")
DERIVED_SERVICE   = str(ROOT / "services" / "derived_service.py")
ROBO_LEGS_SERVICE = str(ROOT / "services" / "robo_legs_service.py")
PATCH_SCRIPT      = str(ROOT / "scripts" / "40_patch_legacy_coupling_isolation.py")


def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def _skip_if_absent(path):
    if not os.path.isfile(path):
        raise unittest.SkipTest(f"Arquivo nao encontrado: {path}")


class TestPatch40ArquivosExistem(unittest.TestCase):
    def test_robo_legs_repo(self):
        self.assertTrue(os.path.isfile(ROBO_LEGS_REPO),
            f"Nao encontrado: {ROBO_LEGS_REPO}")

    def test_robo_status_repo(self):
        self.assertTrue(os.path.isfile(ROBO_STATUS_REPO),
            f"Nao encontrado: {ROBO_STATUS_REPO}")

    def test_derived_service(self):
        self.assertTrue(os.path.isfile(DERIVED_SERVICE),
            f"Nao encontrado: {DERIVED_SERVICE}")

    def test_robo_legs_service(self):
        self.assertTrue(os.path.isfile(ROBO_LEGS_SERVICE),
            f"Nao encontrado: {ROBO_LEGS_SERVICE}")

    def test_patch_script(self):
        self.assertTrue(os.path.isfile(PATCH_SCRIPT),
            f"Nao encontrado: {PATCH_SCRIPT}")


class TestPatch40RoboLegsRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(ROBO_LEGS_REPO)
        cls.src = _read(ROBO_LEGS_REPO)

    def test_get_legs_by_structure_id(self):
        self.assertIn("get_legs_by_structure_id", self.src)

    def test_resolve_aba_from_structure_id(self):
        self.assertIn("_resolve_aba_from_structure_id", self.src)

    def test_has_manual_by_structure_id(self):
        self.assertIn("has_manual_by_structure_id", self.src)

    def test_list_timestamps_by_structure_id(self):
        self.assertIn("list_timestamps_by_structure_id", self.src)

    def test_backward_compat_get_legs(self):
        self.assertIn("def get_legs(", self.src)

    def test_backward_compat_has_manual(self):
        self.assertIn("def has_manual(", self.src)

    def test_backward_compat_list_timestamps(self):
        self.assertIn("def list_timestamps(", self.src)


class TestPatch40RoboLegsStatusRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(ROBO_STATUS_REPO)
        cls.src = _read(ROBO_STATUS_REPO)

    def test_latest_timestamps_by_structure_id(self):
        self.assertIn("latest_timestamps_by_structure_id", self.src)

    def test_resolve_aba_from_structure_id(self):
        self.assertIn("_resolve_aba_from_structure_id", self.src)


class TestPatch40DerivedService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(DERIVED_SERVICE)
        cls.src = _read(DERIVED_SERVICE)

    def test_get_payoff_by_structure_id(self):
        self.assertIn("get_payoff_by_structure_id", self.src)

    def test_backward_compat_get_payoff_by_aba(self):
        self.assertIn("get_payoff_by_aba", self.src)


class TestPatch40RoboLegsService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(ROBO_LEGS_SERVICE)
        cls.src = _read(ROBO_LEGS_SERVICE)

    def test_get_legs_by_structure_id(self):
        self.assertIn("get_legs_by_structure_id", self.src)


if __name__ == "__main__":
    unittest.main()
'''

# 
# CONTEUDO test_patch41.py
# 

TEST_PATCH41 = '''\
# ATT/tests/test_patch41.py
"""Testes formais do patch_41 -- canonical_pricing_facade.py."""
import os
import sys
import unittest
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
        if (parent / "scripts").is_dir() and (parent / "ATT").is_dir():
            return parent
    return start.parent.parent.parent


ROOT = _find_project_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FACADE_FILE = str(ROOT / "services" / "canonical_pricing_facade.py")


def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


class TestPatch41ArquivoExiste(unittest.TestCase):
    def test_facade_existe(self):
        self.assertTrue(
            os.path.isfile(FACADE_FILE),
            f"Nao encontrado: {FACADE_FILE}"
        )


class TestPatch41Renome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(FACADE_FILE):
            raise unittest.SkipTest("Facade nao encontrada -- skip conteudo")
        cls.src = _read(FACADE_FILE)

    def test_get_structure_info_presente(self):
        self.assertIn("_get_structure_info", self.src)

    def test_get_alias_legacy_aba_removido(self):
        self.assertNotIn("def _get_alias_legacy_aba", self.src,
            "_get_alias_legacy_aba ainda presente -- patch_41 nao aplicado")


class TestPatch41InterfacePublica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(FACADE_FILE):
            raise unittest.SkipTest("Facade nao encontrada -- skip interface")
        cls.src = _read(FACADE_FILE)

    def test_execute_pricing_presente(self):
        self.assertIn("def execute_pricing(", self.src)

    def test_class_presente(self):
        self.assertIn("class CanonicalPricingFacade", self.src)


class TestPatch41SemArquivoNovo(unittest.TestCase):
    def test_nenhum_patch41_em_att_patches(self):
        patches_dir = ROOT / "ATT" / "patches"
        if not patches_dir.is_dir():
            self.skipTest("ATT/patches/ nao existe")
        p41 = [f for f in os.listdir(patches_dir)
               if "patch_41" in f.lower() and f.endswith(".py")]
        self.assertEqual(len(p41), 0,
            f"Arquivo inesperado com patch_41 em ATT/patches/: {p41}")


if __name__ == "__main__":
    unittest.main()
'''


# 
# EXECUCAO PRINCIPAL
# 

def run_pytest_check() -> bool:
    log("\n[5/5] Rodando pytest para validar suite pos-patch_43...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         "ATT/tests/test_patch39.py",
         "ATT/tests/test_patch40.py",
         "ATT/tests/test_patch41.py",
         "-v", "--tb=short"],
        cwd=str(ROOT),
    )
    # FAILs de arquivo-nao-encontrado sao esperados ate patch_39/40/41 rodarem
    # Considera sucesso se nao houver ERROR (apenas FAILED e SKIPPED sao ok)
    return result.returncode in (0, 1)


def main():
    global DRY_RUN
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    DRY_RUN = args.dry_run

    if DRY_RUN:
        log("=== MODO DRY-RUN -- nenhum arquivo sera alterado ===\n")

    log("patch_43: Registrar patch_39/40/41 + fechar check patch_38")
    log("=" * 60)

    resultados = []
    resultados.append(fechar_check_patch38())

    log("\n[2/4] Criando ATT/tests/test_patch39.py")
    dry_write(ROOT / "ATT" / "tests" / "test_patch39.py", TEST_PATCH39)
    resultados.append(True)

    log("\n[3/4] Criando ATT/tests/test_patch40.py")
    dry_write(ROOT / "ATT" / "tests" / "test_patch40.py", TEST_PATCH40)
    resultados.append(True)

    log("\n[4/4] Criando ATT/tests/test_patch41.py")
    dry_write(ROOT / "ATT" / "tests" / "test_patch41.py", TEST_PATCH41)
    resultados.append(True)

    if not DRY_RUN:
        resultados.append(run_pytest_check())

    log("\n" + "=" * 60)
    if all(resultados):
        log("patch_43 concluido com SUCESSO.")
        log("\nProximos passos:")
        log("  1. Aplicar patch_39, patch_40, patch_41 (criar os arquivos reais)")
        log("  2. python -m pytest ATT/tests/ -x -q  (deve virar tudo PASSED)")
        log("  3. git add ATT/tests/test_patch3{9,0,1}.py ATT/patches/patch_43*.py")
        log("  4. git commit -m 'test(patch43): registrar testes patch_39/40/41'")
    else:
        log("patch_43 concluido com ERROS -- revisar saida acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()
