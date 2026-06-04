"""
scripts/40_patch_legacy_coupling_isolation.py

patch_40: Isolamento de acoplamento legado -- aba como identidade

Objetivo:
  1. Adicionar _resolve_aba() em robo_legs_repository.py
     (aceita structure_id OU aba, resolve para aba via structures)
  2. Adicionar sobrecarga get_legs_by_structure_id() no mesmo repo
  3. Adicionar latest_timestamps_by_structure_id() em robo_legs_status_repository.py
  4. Adicionar get_payoff_by_structure_id() em derived_service.py
  5. Adicionar get_legs_by_structure_id() em robo_legs_service.py
  6. NÃO alterar assinaturas existentes (backward compatible)

Uso:
  python scripts/40_patch_legacy_coupling_isolation.py [--dry-run]
"""

import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DRY_RUN = False


def log(msg: str):
    print(f"[patch40] {msg}")


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak_{ts}")
    shutil.copy2(path, bak)
    log(f"  backup  {bak.name}")
    return bak


def write_file(path: Path, content: str):
    if DRY_RUN:
        log(f"  [DRY-RUN] escreveria {path.relative_to(ROOT)}")
        return
    path.write_text(content, encoding="utf-8")
    log(f"  escrito  {path.relative_to(ROOT)}")


def patch_robo_legs_repository():
    """
    Adiciona ao final de robo_legs_repository.py:
    - _resolve_aba_from_structure_id() (método privado)
    - get_legs_by_structure_id()
    - has_manual_by_structure_id()
    - list_timestamps_by_structure_id()
    """
    path = ROOT / "repositories" / "robo_legs_repository.py"
    if not path.exists():
        log(f"  ERRO: {path} não encontrado")
        return False

    content = path.read_text(encoding="utf-8")

    # Verificar se já foi patcheado
    if "get_legs_by_structure_id" in content:
        log("  robo_legs_repository.py já contém get_legs_by_structure_id -- skip")
        return True

    backup(path)

    addon = '''

    # 
    # patch_40: métodos canônicos por structure_id
    # Os métodos legados (por aba) são mantidos sem alteração.
    # 

    def _resolve_aba_from_structure_id(self, structure_id: int) -> Optional[str]:
        """
        Resolve structure_id  alias_legacy_aba via structures em app.db.
        Retorna None se não encontrado.
        """
        sql = """
            SELECT alias_legacy_aba
            FROM structures
            WHERE id = ?
              AND alias_legacy_aba IS NOT NULL
              AND alias_legacy_aba != \'\'
            LIMIT 1
        """
        with sqlite_conn(self.config.app_db_path) as conn:
            row = conn.execute(sql, (structure_id,)).fetchone()
        return row["alias_legacy_aba"] if row else None

    def get_legs_by_structure_id(
        self,
        structure_id: int,
        timestamp: Any,
    ) -> List[RoboLegDTO]:
        """
        Ponto de entrada canônico: recebe structure_id, resolve para aba,
        delega para get_legs() existente.
        Levanta ValueError se structure_id não mapeado.
        """
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            raise ValueError(
                f"structure_id={structure_id} sem alias_legacy_aba em structures"
            )
        return self.get_legs(aba=aba, timestamp=timestamp)

    def has_manual_by_structure_id(
        self,
        structure_id: int,
        timestamp: Any,
    ) -> bool:
        """Versão canônica de has_manual() por structure_id."""
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            return False
        return self.has_manual(aba=aba, timestamp=timestamp)

    def list_timestamps_by_structure_id(
        self,
        structure_id: int,
        prefer: str = "manual_then_rtd",
    ) -> List[str]:
        """Versão canônica de list_timestamps() por structure_id."""
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            raise ValueError(
                f"structure_id={structure_id} sem alias_legacy_aba em structures"
            )
        return self.list_timestamps(aba=aba, prefer=prefer)
'''

    new_content = content.rstrip() + "\n" + addon + "\n"
    write_file(path, new_content)
    log("  robo_legs_repository.py -- 4 métodos canônicos adicionados")
    return True


def patch_robo_legs_status_repository():
    """
    Adiciona latest_timestamps_by_structure_id() ao final de
    robo_legs_status_repository.py.
    """
    path = ROOT / "repositories" / "robo_legs_status_repository.py"
    if not path.exists():
        log(f"  ERRO: {path} não encontrado")
        return False

    content = path.read_text(encoding="utf-8")

    if "latest_timestamps_by_structure_id" in content:
        log("  robo_legs_status_repository.py já patcheado -- skip")
        return True

    backup(path)

    addon = '''

    # 
    # patch_40: método canônico por structure_id
    # 

    def _resolve_aba_from_structure_id(self, structure_id: int) -> Optional[str]:
        """Resolve structure_id  alias_legacy_aba via app.db."""
        sql = """
            SELECT alias_legacy_aba
            FROM structures
            WHERE id = ?
              AND alias_legacy_aba IS NOT NULL
              AND alias_legacy_aba != \'\'
            LIMIT 1
        """
        with sqlite_conn(self.config.app_db_path) as conn:
            row = conn.execute(sql, (structure_id,)).fetchone()
        return row["alias_legacy_aba"] if row else None

    def latest_timestamps_by_structure_id(
        self,
        structure_id: int,
    ) -> "Tuple[Optional[datetime], Optional[datetime]]":
        """
        Versão canônica de latest_timestamps() por structure_id.
        Retorna (manual_latest_ts, rtd_latest_ts).
        """
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            return (None, None)
        return self.latest_timestamps(aba=aba)
'''

    new_content = content.rstrip() + "\n" + addon + "\n"

    # Garantir import de sqlite_conn se não estiver presente
    if "from infra.sqlite_conn import sqlite_conn" not in new_content:
        new_content = (
            "from infra.sqlite_conn import sqlite_conn\n" + new_content
        )

    write_file(path, new_content)
    log("  robo_legs_status_repository.py -- 2 métodos canônicos adicionados")
    return True


def patch_derived_service():
    """
    Adiciona get_payoff_by_structure_id() em derived_service.py,
    mantendo get_payoff_by_aba() intacta (backward compat).
    """
    path = ROOT / "services" / "derived_service.py"
    if not path.exists():
        log(f"  ERRO: {path} não encontrado")
        return False

    content = path.read_text(encoding="utf-8")

    if "get_payoff_by_structure_id" in content:
        log("  derived_service.py já patcheado -- skip")
        return True

    backup(path)

    # Inserir imediatamente após get_payoff_by_aba()
    insertion = '''

def get_payoff_by_structure_id(structure_id: int):
    """
    patch_40: ponto de entrada canônico por structure_id.
    Resolve structure_id  aba via cache, delega para get_payoff_by_aba().
    """
    if not _ABA_CACHE_LOADED:
        _load_aba_cache()

    # Inverter o cache para structure_id  aba
    sid_to_aba = {v: k for k, v in _ABA_TO_STRUCTURE_ID.items()}
    aba = sid_to_aba.get(structure_id)

    if aba is None:
        return []  # structure_id não mapeado -- retorna lista vazia

    return get_payoff_by_aba(aba)

'''

    # Inserir após o bloco get_payoff_by_aba
    marker = "def get_recent_decisions():"
    if marker not in content:
        # Fallback: appenda no final
        new_content = content.rstrip() + "\n" + insertion
    else:
        new_content = content.replace(
            marker,
            insertion.rstrip() + "\n\n\n" + marker,
        )

    write_file(path, new_content)
    log("  derived_service.py -- get_payoff_by_structure_id() adicionada")
    return True


def patch_robo_legs_service():
    """
    Adiciona get_legs_by_structure_id() em robo_legs_service.py.
    """
    path = ROOT / "services" / "robo_legs_service.py"
    if not path.exists():
        log(f"  ERRO: {path} não encontrado")
        return False

    content = path.read_text(encoding="utf-8")

    if "get_legs_by_structure_id" in content:
        log("  robo_legs_service.py já patcheado -- skip")
        return True

    backup(path)

    addon = '''
    def get_legs_by_structure_id(
        self,
        structure_id: int,
        timestamp: Any,
        validate: bool = True,
    ) -> "List[RoboLegDTO]":
        """
        patch_40: ponto de entrada canônico por structure_id.
        Delega para repo.get_legs_by_structure_id() e valida.
        """
        legs = self.repo.get_legs_by_structure_id(
            structure_id=structure_id,
            timestamp=timestamp,
        )
        if validate:
            report = validate_legs(legs)
            if not report.is_ok():
                first = report.errors[0]
                raise ValueError(
                    f"Legs inválidas: {first.code} field={first.field} "
                    f"structure_id={structure_id}"
                )
        return legs
'''

    new_content = content.rstrip() + "\n" + addon + "\n"
    write_file(path, new_content)
    log("  robo_legs_service.py -- get_legs_by_structure_id() adicionada")
    return True


def run_verification():
    """Verifica rapidamente se os métodos foram inseridos."""
    log("\nVerificação pós-patch:")
    checks = [
        ("repositories/robo_legs_repository.py",       "get_legs_by_structure_id"),
        ("repositories/robo_legs_repository.py",       "_resolve_aba_from_structure_id"),
        ("repositories/robo_legs_status_repository.py","latest_timestamps_by_structure_id"),
        ("services/derived_service.py",                "get_payoff_by_structure_id"),
        ("services/robo_legs_service.py",              "get_legs_by_structure_id"),
    ]
    all_ok = True
    for rel, symbol in checks:
        path = ROOT / rel
        found = path.exists() and symbol in path.read_text(encoding="utf-8")
        status = "OK" if found else "FALHOU"
        if not found:
            all_ok = False
        log(f"  [{status}] {rel}  {symbol}")
    return all_ok


def main():
    global DRY_RUN
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    DRY_RUN = args.dry_run

    if DRY_RUN:
        log("=== MODO DRY-RUN -- nenhum arquivo será alterado ===\n")

    log("patch_40: Isolamento de acoplamento legado -- aba como identidade")
    log("=" * 60)

    results = []

    log("\n[1/4] repositories/robo_legs_repository.py")
    results.append(patch_robo_legs_repository())

    log("\n[2/4] repositories/robo_legs_status_repository.py")
    results.append(patch_robo_legs_status_repository())

    log("\n[3/4] services/derived_service.py")
    results.append(patch_derived_service())

    log("\n[4/4] services/robo_legs_service.py")
    results.append(patch_robo_legs_service())

    if not DRY_RUN:
        ok = run_verification()
    else:
        ok = True

    log("\n" + "=" * 60)
    if all(results) and ok:
        log("patch_40 concluido com sucesso.")
        log("Proximos passos:")
        log("  1. python -m pytest ATT/tests/ -x -q")
        log("  2. git add -p  (revisar cada hunk)")
        log("  3. git commit -m 'feat(patch40): adiciona métodos canônicos por structure_id'")
    else:
        log("patch_40 concluido com ERROS -- revisar saída acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()
