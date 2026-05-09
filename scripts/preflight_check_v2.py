#!/usr/bin/env python3
"""
Preflight Environment Check v2
Verifica se o ambiente está pronto para rodar pipelines críticas.
Atualizado para usar paths padronizados (dados/app.db, dados/derived.db)
"""

import sqlite3
import sys
from pathlib import Path
import json
from datetime import datetime
import os

class PreflightChecker:
    def __init__(self, repo_root="."):
        self.repo_root = Path(repo_root).resolve()
        self.results = {"timestamp": datetime.now().isoformat(), "checks": {}}
        
    def _find_db(self, db_name):
        """Procura banco com prioridade em dados/, fallback para raiz"""
        candidates = [
            self.repo_root / "dados" / db_name,  # Padrão atual
            self.repo_root / db_name,           # Legacy fallback
        ]
        
        for path in candidates:
            if path.exists() and path.is_file():
                return path
        return None
    
    def check_database(self, db_name, required=True):
        """Verifica se banco existe e é acessível"""
        check_name = f"database_{db_name.replace('.', '_')}"
        
        db_path = self._find_db(db_name)
        
        if not db_path:
            self.results["checks"][check_name] = {
                "status": "FAIL" if required else "WARN",
                "message": f"Database {db_name} não encontrado",
                "searched": ["dados/" + db_name, db_name]
            }
            return False
            
        try:
            # Testa conexão
            with sqlite3.connect(str(db_path)) as conn:
                cursor = conn.execute("SELECT 1")
                cursor.fetchone()
            
            # Verifica se está na localização padrão
            is_standard = db_path == self.repo_root / "dados" / db_name
            location_msg = "localização padrão" if is_standard else f"localização legacy ({db_path.relative_to(self.repo_root)})"
            
            self.results["checks"][check_name] = {
                "status": "PASS",
                "message": f"Database {db_name} OK ({location_msg})",
                "path": str(db_path.relative_to(self.repo_root)),
                "is_standard_location": is_standard
            }
            return True
            
        except Exception as e:
            self.results["checks"][check_name] = {
                "status": "FAIL",
                "message": f"Erro ao acessar {db_name}: {e}",
                "path": str(db_path.relative_to(self.repo_root))
            }
            return False
    
    def check_directories(self):
        """Verifica estrutura de diretórios essenciais"""
        required_dirs = ["dados", "scripts", "bridge"]
        
        for dir_name in required_dirs:
            dir_path = self.repo_root / dir_name
            check_name = f"directory_{dir_name}"
            
            if dir_path.exists() and dir_path.is_dir():
                self.results["checks"][check_name] = {
                    "status": "PASS",
                    "message": f"Diretório {dir_name}/ OK"
                }
            else:
                self.results["checks"][check_name] = {
                    "status": "WARN",
                    "message": f"Diretório {dir_name}/ não encontrado"
                }
    
    def check_env_vars(self):
        """Verifica variáveis de ambiente relevantes"""
        env_vars = ["APP_DB_PATH", "DERIVED_DB_PATH"]
        
        for var in env_vars:
            value = os.environ.get(var)
            check_name = f"env_{var.lower()}"
            
            if value:
                # Verifica se o arquivo existe
                path = Path(value)
                if not path.is_absolute():
                    path = self.repo_root / value
                
                exists = path.exists()
                self.results["checks"][check_name] = {
                    "status": "PASS" if exists else "WARN",
                    "message": f"{var}={value} ({'existe' if exists else 'NÃO EXISTE'})"
                }
            else:
                self.results["checks"][check_name] = {
                    "status": "INFO",
                    "message": f"{var} não definida (usando auto-discovery)"
                }
    
    def run_all_checks(self):
        """Executa todos os checks"""
        print("[INFO] Preflight Check v2 - Verificando ambiente...")
        print(f"[INFO] Repo: {self.repo_root}\n")
        
        # Checks principais
        self.check_directories()
        self.check_env_vars()
        
        # Checks de bancos (críticos)
        app_ok = self.check_database("app.db", required=True)
        derived_ok = self.check_database("derived.db", required=True)
        
        # Resultados
        print("=" * 50)
        passed = failed = warned = 0
        
        for check_name, result in self.results["checks"].items():
            status = result["status"]
            message = result["message"]
            
            if status == "PASS":
                print(f"[OK] {message}")
                passed += 1
            elif status == "FAIL":
                print(f"[ERROR] {message}")
                failed += 1
            elif status == "WARN":
                print(f"[WARN]  {message}")
                warned += 1
            else:  # INFO
                print(f"[INFO]  {message}")
        
        print("=" * 50)
        print(f"Resultado: {passed} OK, {failed} FALHOU, {warned} AVISOS")
        
        # Salvar relatório
        report_path = self.repo_root / "ATT" / "reports" / "preflight_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Relatório salvo: {report_path.relative_to(self.repo_root)}")
        
        # Status final
        if failed > 0:
            print("\n[ERROR] PREFLIGHT FALHOU - Corrija os erros antes de continuar")
            return 1
        elif not app_ok or not derived_ok:
            print("\n[ERROR] BANCOS CRÍTICOS INDISPONÍVEIS")
            return 1
        elif warned > 0:
            print("\n[WARN]  PREFLIGHT OK COM AVISOS")
            return 0
        else:
            print("\n[OK] PREFLIGHT OK - Ambiente pronto!")
            return 0

def main():
    checker = PreflightChecker()
    return checker.run_all_checks()

if __name__ == "__main__":
    sys.exit(main())
