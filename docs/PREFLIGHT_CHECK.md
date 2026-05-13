# Preflight Environment Check

## Objetivo
Automatizar verificações críticas do ambiente antes de rodar pipelines importantes, garantindo que:
- Bancos de dados essenciais existem e têm estrutura correta
- Scripts críticos estão presentes
- Ambiente Python tem dependências mínimas
- Relatórios de análise estão atualizados

## Uso

### Execução simples:
```bash
# Via Python direto
python scripts/preflight_check_v2.py

# Via wrapper bash
bash scripts/preflight.sh

