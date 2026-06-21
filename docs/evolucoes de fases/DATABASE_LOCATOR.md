# Database Locator & Scanner

## Objetivo
Localizar e analisar automaticamente todos os bancos SQLite no repositório:
- Encontrar arquivos `.db`, `.sqlite`, `.sqlite3`
- Examinar estrutura de tabelas e contagem de registros
- Gerar relatório detalhado
- Sugerir configuração correta para outros scripts

## Uso

### Execução simples:
```bash
# Via Python direto
python scripts/db_locator.py

# Via wrapper bash (com relatório)
bash scripts/find_dbs.sh

# Com salvamento de relatório
python scripts/db_locator.py --save-report
