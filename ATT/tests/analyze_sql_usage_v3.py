#!/usr/bin/env python3

import re
from pathlib import Path
from typing import List, Dict, Any

def should_skip_dir(dirpath: str) -> bool:
    """Filtros de diretórios (copiado de _scan_utils_v2.py)"""
    norm = dirpath.replace("\\", "/")
    parts = norm.split("/")

    DEFAULT_EXCLUDE_DIRS = {
        '.git', '__pycache__', '.pytest_cache', 
        'node_modules', '.vscode', '.idea', 'dist', 'build', 
        'LIXO'
    }

    if any(p in DEFAULT_EXCLUDE_DIRS for p in parts):
        return True

    # backup_*
    if any(p.startswith("backup_") for p in parts):
        return True

    # site-packages
    if "/site-packages/" in norm:
        return True

    return False

def get_python_files() -> List[Path]:
    """Busca arquivos .py no projeto (copiado de _scan_utils_v2.py)"""
    files = []
    base = Path(".")
    
    for file_path in base.rglob("*.py"):
        if should_skip_dir(str(file_path.parent)):
            continue
        files.append(file_path)
    
    return sorted(files)

def extract_sql_tables_from_content(content: str, filepath: str) -> List[Dict[str, Any]]:
    """
    Extrai tabelas SQL de strings/queries dentro do código Python.
    Ignora imports Python (from ... import ...).
    """
    results = []
    lines = content.splitlines()
    
    # Regex para capturar SQL dentro de strings
    sql_patterns = [
        r'(?:FROM|JOIN|INTO|UPDATE|CREATE\s+TABLE)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        r'(?:from|join|into|update|create\s+table)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
    ]
    
    for i, line in enumerate(lines, 1):
        # Pula linhas que são claramente imports Python
        if line.strip().startswith('from ') and ' import ' in line:
            continue
            
        # Procura por padrões SQL na linha
        for pattern in sql_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for table in matches:
                # Filtra nomes que claramente não são tabelas SQL
                if table.lower() not in ['tkinter', 'typing', 'datetime', 'pathlib', 'sqlite3', 
                                       'matplotlib', 'json', 'pandas', 'real', 'dict', 'set']:
                    results.append({
                        'line': i,
                        'table': table,
                        'context': line.strip()[:100]  # primeiros 100 chars da linha
                    })
    
    return results

def analyze_sql_usage(output_path: str = "ATT/reports/sql_report_v3.json"):
    """Analisa uso de SQL nos arquivos Python do projeto."""
    
    all_results = {}
    python_files = get_python_files()
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tables = extract_sql_tables_from_content(content, str(file_path))
            
            if tables:  # só incluir arquivos que têm tabelas SQL
                rel_path = str(file_path).replace("\\", "/")
                all_results[rel_path] = tables
                
        except Exception as e:
            print(f"[analyze_sql_usage_v3] Erro ao processar {file_path}: {e}")
    
    # Salvar resultado
    import json
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"[analyze_sql_usage_v3] OK (filtered) - wrote {output_path}")
    return all_results

if __name__ == "__main__":
    analyze_sql_usage()
