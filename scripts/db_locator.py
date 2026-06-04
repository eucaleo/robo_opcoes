#!/usr/bin/env python3
"""
Database Locator & Scanner
Localiza arquivos .db no repositório e examina sua estrutura/conteúdo.
"""

import sqlite3
import sys
from pathlib import Path
import json
from datetime import datetime
import os

class DatabaseLocator:
    def __init__(self, repo_root="."):
        self.repo_root = Path(repo_root).resolve()
        self.found_dbs = []
        
    def scan_for_databases(self, max_depth=3):
        """Procura arquivos .db no repositório"""
        print(f"[INFO] Escaneando por bancos SQLite em: {self.repo_root}")
        print(f"   Profundidade máxima: {max_depth} níveis\n")
        
        for root, dirs, files in os.walk(self.repo_root):
            # Limita profundidade
            level = root[len(str(self.repo_root)):].count(os.sep)
            if level >= max_depth:
                dirs.clear()  # Não desce mais
                continue
                
            # Ignora algumas pastas comuns
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.pytest_cache', 'node_modules'}]
            
            for file in files:
                if file.endswith('.db') or file.endswith('.sqlite') or file.endswith('.sqlite3'):
                    db_path = Path(root) / file
                    rel_path = db_path.relative_to(self.repo_root)
                    self.found_dbs.append({
                        'name': file,
                        'full_path': str(db_path),
                        'relative_path': str(rel_path),
                        'size_bytes': db_path.stat().st_size if db_path.exists() else 0,
                        'directory': str(db_path.parent.relative_to(self.repo_root))
                    })
        
        print(f"[INFO] Encontrados {len(self.found_dbs)} arquivo(s) de banco:")
        for db in self.found_dbs:
            size_mb = db['size_bytes'] / (1024*1024)
            print(f"   [INFO] {db['relative_path']} ({size_mb:.1f} MB)")
        print()
    
    def analyze_database(self, db_info):
        """Analisa estrutura e conteúdo de um banco"""
        db_path = db_info['full_path']
        print(f"[INFO] Analisando: {db_info['relative_path']}")
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Lista tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
                tables = [row[0] for row in cursor.fetchall()]
                
                print(f"   [INFO] Tabelas ({len(tables)}):")
                
                table_info = {}
                for table in tables:
                    try:
                        # Conta registros
                        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                        count = cursor.fetchone()[0]
                        
                        # Pega estrutura da tabela
                        cursor.execute(f"PRAGMA table_info(`{table}`)")
                        columns = cursor.fetchall()
                        
                        table_info[table] = {
                            'row_count': count,
                            'columns': len(columns),
                            'column_names': [col[1] for col in columns]
                        }
                        
                        print(f"      - {table}: {count:,} registros, {len(columns)} colunas")
                        
                    except Exception as e:
                        print(f"      - {table}: ERRO ao acessar - {e}")
                        table_info[table] = {'error': str(e)}
                
                return {
                    'accessible': True,
                    'table_count': len(tables),
                    'tables': table_info
                }
                
        except Exception as e:
            print(f"   [ERROR] ERRO ao conectar: {e}")
            return {
                'accessible': False,
                'error': str(e)
            }
    
    def generate_report(self):
        """Gera relatório detalhado"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'repo_root': str(self.repo_root),
            'databases': []
        }
        
        for db_info in self.found_dbs:
            analysis = self.analyze_database(db_info)
            
            db_report = {
                **db_info,
                **analysis
            }
            report['databases'].append(db_report)
            print()  # Linha em branco após cada DB
        
        return report
    
    def save_report(self, report, output_file="ATT/reports/database_scan.json"):
        """Salva relatório em JSON"""
        output_path = self.repo_root / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Relatório salvo em: {output_path.relative_to(self.repo_root)}")
    
    def print_summary(self, report):
        """Imprime resumo visual"""
        print("="*60)
        print("[INFO] RESUMO DO SCAN DE BANCOS")
        print("="*60)
        
        if not report['databases']:
            print("[ERROR] Nenhum banco de dados encontrado!")
            return
        
        print(f"[INDICE]  Total de bancos: {len(report['databases'])}")
        
        accessible_count = sum(1 for db in report['databases'] if db.get('accessible', False))
        print(f"[OK] Acessíveis: {accessible_count}")
        print(f"[ERROR] Com problemas: {len(report['databases']) - accessible_count}")
        print()
        
        # Bancos principais esperados
        expected_dbs = ['app.db', 'derived.db']
        found_expected = {}
        
        for expected in expected_dbs:
            matches = [db for db in report['databases'] if db['name'] == expected]
            if matches:
                db = matches[0]  # Pega primeiro match
                found_expected[expected] = db['relative_path']
                print(f"[OK] {expected}: {db['relative_path']}")
            else:
                found_expected[expected] = None
                print(f"[ERROR] {expected}: NÃO ENCONTRADO")
        
        print()
        print("[INFO] CONFIGURAÇÃO SUGERIDA PARA PREFLIGHT:")
        print("   Atualizar caminhos dos bancos para:")
        
        for expected, path in found_expected.items():
            if path:
                print(f"   - {expected}: {path}")
            else:
                print(f"   - {expected}: CRIAR OU LOCALIZAR")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Database Locator & Scanner")
        print("Uso: python db_locator.py [diretorio_raiz] [--save-report]")
        return 0
    
    repo_root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else "."
    save_report = '--save-report' in sys.argv
    
    locator = DatabaseLocator(repo_root)
    locator.scan_for_databases()
    
    report = locator.generate_report()
    locator.print_summary(report)
    
    if save_report:
        locator.save_report(report)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
