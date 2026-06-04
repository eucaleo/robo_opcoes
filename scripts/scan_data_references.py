#!/usr/bin/env python3
"""
Script para localizar todas as referências à string "data" nas pastas específicas
do projeto, com foco na migração data/ -> dados/
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def find_data_references(project_root: str = ".") -> Dict[str, List[Tuple[int, str]]]:
    """
    Busca referências à string "data" nos arquivos das pastas específicas.
    
    Returns:
        Dict com filename -> [(line_number, line_content), ...]
    """
    
    # Pastas para escanear (conforme solicitado)
    target_dirs = ["bridge", "db", "domain", "scripts", "services", "UI"]
    
    # Extensões de arquivo para considerar
    extensions = {".py", ".sh", ".md", ".txt", ".yml", ".yaml", ".json", ".sql"}
    
    results = {}
    project_path = Path(project_root).resolve()
    
    # substitua sua lista patterns por esta:
    patterns = [
        r'(?i)(["\'])data[\\/]',         # "data/"  ou 'data\' (windows)
        r'(?i)\bdata[\\/]',              # data/ ou data\ no início de token
        r'(?i)[\\/]data[\\/]',           # /data/ ou \data\
        r'(?i)\bdata[\\/]app\.db\b',     # data/app.db ou data\app.db
        r'(?i)\bdata[\\/]derived\.db\b', # data/derived.db ou data\derived.db
    ]

    
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    print(f"[BUSCA] Escaneando pastas: {', '.join(target_dirs)}")
    print(f" Projeto: {project_path}")
    print("=" * 60)
    
    for dir_name in target_dirs:
        dir_path = project_path / dir_name
        if not dir_path.exists():
            print(f"[AVISO]  Pasta não encontrada: {dir_name}")
            continue
            
        print(f"[DIR] Escaneando: {dir_name}/")
        
        # Recursivo através da pasta
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                # Filtrar por extensão
                if not any(file.endswith(ext) for ext in extensions):
                    continue
                
                file_path = Path(root) / file
                relative_path = file_path.relative_to(project_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    matches = []
                    for line_num, line in enumerate(lines, 1):
                        # Verificar cada pattern
                        for pattern in compiled_patterns:
                            if pattern.search(line):
                                matches.append((line_num, line.rstrip()))
                                break  # Evitar duplicatas na mesma linha
                    
                    if matches:
                        results[str(relative_path)] = matches
                        
                except Exception as e:
                    print(f"[FALHOU] Erro lendo {relative_path}: {e}")
    
    return results

def print_results(results: Dict[str, List[Tuple[int, str]]]) -> None:
    """Imprime os resultados de forma organizada."""
    
    if not results:
        print("\n NENHUMA referência a 'data' encontrada!")
        print("[OK] Migração data/ -> dados/ parece estar completa nas pastas verificadas.")
        return
    
    print(f"\n[LISTA] RESULTADOS: {len(results)} arquivo(s) com referências a 'data'")
    print("=" * 60)
    
    total_lines = 0
    for filepath, matches in sorted(results.items()):
        print(f"\n[ARQUIVO] {filepath}")
        print("-" * len(filepath))
        
        for line_num, line_content in matches:
            total_lines += 1
            # Destacar a palavra "data" na linha
            highlighted = re.sub(
                r'(\bdata\b)', 
                r'>>> \1 <<<', 
                line_content, 
                flags=re.IGNORECASE
            )
            print(f"  {line_num:3d}: {highlighted}")
    
    print(f"\n[RELATORIO] RESUMO:")
    print(f"   * Arquivos afetados: {len(results)}")
    print(f"   * Linhas com referências: {total_lines}")
    
def suggest_fixes(results: Dict[str, List[Tuple[int, str]]]) -> None:
    """Sugere correções automáticas comuns."""
    
    if not results:
        return
    
    print(f"\n[CONFIG] SUGESTÕES DE CORREÇÃO:")
    print("=" * 40)
    
    common_fixes = {
        r'"data/': r'"dados/',
        r"'data/": r"'dados/",
        r'/data/': r'/dados/',
        r'\\data\\': r'\\dados\\',
        r'data\.db': r'dados.db',
    }
    
    for filepath, matches in sorted(results.items()):
        needs_fix = False
        for line_num, line_content in matches:
            for old_pattern, new_pattern in common_fixes.items():
                if re.search(old_pattern, line_content, re.IGNORECASE):
                    needs_fix = True
                    break
        
        if needs_fix:
            print(f"\n[NOTA] {filepath}:")
            for old, new in common_fixes.items():
                print(f"   sed -i 's|{old}|{new}|g' {filepath}")

def main():
    """Função principal."""
    print("[DEPLOY] SCANNER DE REFERÊNCIAS 'data' -> 'dados'")
    print("Restrito às pastas: bridge, db, domain, scripts, services, UI")
    print("=" * 60)
    
    # Executar scan
    results = find_data_references()
    
    # Mostrar resultados
    print_results(results)
    
    # Sugerir correções
    suggest_fixes(results)
    
    print("\n" + "=" * 60)
    print("[OK] Scan concluído!")

if __name__ == "__main__":
    main()
