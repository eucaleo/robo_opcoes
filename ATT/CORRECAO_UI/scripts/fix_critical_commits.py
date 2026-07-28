#!/usr/bin/env python3
"""
CORREÇÃO DE COMMITS FALTANTES NOS ARQUIVOS CRÍTICOS
====================================================
Analisa e corrige arquivos que fazem INSERT/UPDATE/DELETE sem commit().
Executar via Git Bash: python scripts/fix_critical_commits.py

MODO SEGURO: Primeiro executa em modo --dry-run para ver o que seria alterado.
             Depois execute com --apply para aplicar as correções.
"""

import os
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

# ─── CONFIGURAÇÃO ───────────────────────────────────────────
PROJETO_RAIZ = Path(r"C:\Users\eucal\projeto")
BACKUP_DIR = PROJETO_RAIZ / "ATT" / "CORRECAO_UI" / "backups" / f"commit_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Arquivos críticos que fazem ESCRITA e precisam de commit
# Baseado na auditoria: têm execute=True, commit=False, NÃO são só leitura
ARQUIVOS_CRITICOS = [
    "services/derived_service.py",
    "services/canonical_pricing_facade.py",
    "services/derived_payoff_persistence.py",
    "services/rtd_option_quotes_excel_sync.py",
    "services/payoff_refresh_command_service.py",
    "services/system_recalculation_command_service.py",
    "services/pricing_execution_orchestration_service.py",
    "repositories/market_snapshot_repository.py",
    "repositories/system_snapshots_repository.py",
    "repositories/rtd_option_quotes_intraday_history_repository.py",
    "repositories/robo_legs_repository.py",
    "repositories/robo_legs_status_repository.py",
    "db/writer.py",
    "db/derived_repo.py",
    "infra/sqlite_conn.py",
    "infra/bootstrap_rtd_option_quotes_schema.py",
    "infra/bootstrap_structures_schema.py",
]

SEPARADOR = "=" * 70


class ArquivoInfo(NamedTuple):
    caminho: Path
    conteudo_original: str
    tem_insert: bool
    tem_update: bool
    tem_delete: bool
    tem_commit: bool
    tem_isolation_level: bool
    tem_connect: bool
    funcoes_escrita: list[str]


def analisar_arquivo(caminho: Path) -> ArquivoInfo:
    """Analisa um arquivo Python em busca de operações de escrita sem commit."""
    conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
    
    tem_commit = ".commit()" in conteudo or "conn.commit()" in conteudo
    tem_isolation_level = "isolation_level" in conteudo
    tem_connect = "sqlite3.connect" in conteudo or ".connect(" in conteudo
    
    # Detectar operações de escrita
    tem_insert = bool(re.search(
        r'(?:execute|executemany)\s*\(\s*["\'].*?(?:INSERT|REPLACE)\s',
        conteudo, re.IGNORECASE
    ))
    tem_update = bool(re.search(
        r'(?:execute|executemany)\s*\(\s*["\'].*?\bUPDATE\b',
        conteudo, re.IGNORECASE
    ))
    tem_delete = bool(re.search(
        r'(?:execute|executemany)\s*\(\s*["\'].*?\bDELETE\b',
        conteudo, re.IGNORECASE
    ))
    
    # Encontrar funções que fazem escrita
    linhas = conteudo.splitlines()
    funcoes_escrita = []
    funcao_atual = None
    
    for i, linha in enumerate(linhas, 1):
        if linha.strip().startswith("def "):
            funcao_atual = linha.strip().split("(")[0].replace("def ", "")
        if funcao_atual and re.search(
            r'(?:INSERT|UPDATE|DELETE|REPLACE)\s',
            linha, re.IGNORECASE
        ):
            if funcao_atual not in funcoes_escrita:
                funcoes_escrita.append(funcao_atual)
    
    return ArquivoInfo(
        caminho=caminho,
        conteudo_original=conteudo,
        tem_insert=tem_insert,
        tem_update=tem_update,
        tem_delete=tem_delete,
        tem_commit=tem_commit,
        tem_isolation_level=tem_isolation_level,
        tem_connect=tem_connect,
        funcoes_escrita=funcoes_escrita,
    )


def gerar_correcao(info: ArquivoInfo) -> str | None:
    """Gera o conteúdo corrigido com commit() adicionado onde necessário."""
    if info.tem_commit or info.tem_isolation_level:
        return None  # Já tem commit ou autocommit
    
    if not (info.tem_insert or info.tem_update or info.tem_delete):
        return None  # Só leitura, não precisa de commit
    
    conteudo = info.conteudo_original
    linhas = conteudo.splitlines()
    novas_linhas = []
    modificado = False
    
    # Padrão: encontrar funções que fazem execute() de escrita e 
    # adicionar conn.commit() antes do return ou no final da função
    
    dentro_funcao = False
    indent_funcao = ""
    funcao_tem_escrita = False
    
    for i, linha in enumerate(linhas):
        novas_linhas.append(linha)
        
        # Detectar início de função
        if linha.strip().startswith("def "):
            dentro_funcao = True
            indent_funcao = linha[:len(linha) - len(linha.lstrip())]
            funcao_tem_escrita = False
            continue
        
        # Detectar escrita dentro da função
        if dentro_funcao and re.search(
            r'(?:INSERT|UPDATE|DELETE|REPLACE)\s',
            linha, re.IGNORECASE
        ):
            funcao_tem_escrita = True
        
        # Detectar fim da função (linha com menos indentação que a função)
        if dentro_funcao and linha.strip() and not linha.startswith(indent_funcao + " "):
            if funcao_tem_escrita and not info.tem_commit:
                # Adicionar commit antes de sair da função
                commit_line = f"{indent_funcao}    conn.commit()"
                novas_linhas.insert(-1, commit_line)
                modificado = True
            dentro_funcao = False
            funcao_tem_escrita = False
    
    if not modificado:
        return None
    
    return "\n".join(novas_linhas)


def aplicar_correcoes(dry_run: bool = True):
    """Analisa e corrige todos os arquivos críticos."""
    print(SEPARADOR)
    print("  CORREÇÃO DE COMMITS FALTANTES")
    print(f"  Modo: {'DRY-RUN (simulação)' if dry_run else 'APLICAÇÃO REAL'}")
    print(f"  Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEPARADOR)
    
    if not dry_run:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\n📁 Backups em: {BACKUP_DIR}")
    
    arquivos_modificados = 0
    arquivos_ok = 0
    arquivos_nao_encontrados = 0
    
    for relpath in ARQUIVOS_CRITICOS:
        caminho = PROJETO_RAIZ / relpath
        print(f"\n{'─' * 60}")
        print(f"📄 {relpath}")
        
        if not caminho.exists():
            print(f"   ❌ Arquivo não encontrado: {caminho}")
            arquivos_nao_encontrados += 1
            continue
        
        info = analisar_arquivo(caminho)
        
        # Resumo
        print(f"   connect: {info.tem_connect} | "
              f"INSERT: {info.tem_insert} | "
              f"UPDATE: {info.tem_update} | "
              f"DELETE: {info.tem_delete}")
        print(f"   commit(): {info.tem_commit} | "
              f"isolation_level: {info.tem_isolation_level}")
        
        # Classificar
        if info.tem_commit or info.tem_isolation_level:
            print(f"   ✓ Já possui commit ou autocommit — OK")
            arquivos_ok += 1
            continue
        
        if not (info.tem_insert or info.tem_update or info.tem_delete):
            print(f"   ✓ Apenas leitura (SELECT) — não precisa de commit")
            arquivos_ok += 1
            continue
        
        # PRECISA DE CORREÇÃO
        print(f"   ⚠️ ESCRITA SEM COMMIT! Funções: {info.funcoes_escrita}")
        
        if not dry_run:
            # Fazer backup
            backup_path = BACKUP_DIR / relpath.replace("/", "_").replace("\\", "_")
            shutil.copy2(caminho, backup_path)
            
            # Estratégia: usar isolation_level=None para autocommit
            # É mais seguro que tentar adicionar commit() manualmente
            conteudo = info.conteudo_original
            
            # Substituir sqlite3.connect(...) por sqlite3.connect(..., isolation_level=None)
            # Padrão 1: sqlite3.connect(db_path)
            # Padrão 2: sqlite3.connect(str(db_path))
            
            novo_conteudo = re.sub(
                r'(sqlite3\.connect\s*\([^)]+)\)',
                r'\1, isolation_level=None)',
                conteudo
            )
            
            # Se nenhuma substituição foi feita, tentar padrão alternativo
            if novo_conteudo == conteudo:
                novo_conteudo = re.sub(
                    r'(\.connect\s*\([^)]+)\)',
                    r'\1, isolation_level=None)',
                    conteudo
                )
            
            if novo_conteudo != conteudo:
                caminho.write_text(novo_conteudo, encoding="utf-8")
                print(f"   ✅ CORRIGIDO: isolation_level=None adicionado ao connect()")
                print(f"   📁 Backup salvo em: {backup_path}")
                arquivos_modificados += 1
            else:
                print(f"   ⚠️ Não foi possível corrigir automaticamente")
                print(f"   🔧 AÇÃO MANUAL NECESSÁRIA: adicione conn.commit() após execute()")
        else:
            print(f"   🔧 [DRY-RUN] Seria corrigido com isolation_level=None")
            arquivos_modificados += 1
    
    # ─── Resumo final ───
    print(f"\n{SEPARADOR}")
    print("  RESUMO")
    print(SEPARADOR)
    print(f"  Arquivos OK: {arquivos_ok}")
    print(f"  Arquivos corrigidos{' (simulação)' if dry_run else ''}: {arquivos_modificados}")
    print(f"  Arquivos não encontrados: {arquivos_nao_encontrados}")
    
    if dry_run and arquivos_modificados > 0:
        print(f"\n  Execute com --apply para aplicar as correções:")
        print(f"  python scripts/fix_critical_commits.py --apply")


def main():
    dry_run = "--apply" not in sys.argv
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Uso: python fix_critical_commits.py [--apply] [--help]")
        print("  --apply   Aplica as correções (sem flag = dry-run)")
        print("  --help    Mostra esta ajuda")
        return 0
    
    aplicar_correcoes(dry_run=dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
