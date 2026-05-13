# PATCH-01 — Auditoria Inicial Estruturada

## Objetivo
Executar uma auditoria inicial do repositório para levantar:

- estrutura de diretórios
- arquivos de configuração
- scripts existentes
- dependências declaradas
- indícios de legado
- pontos sensíveis para refatoração futura

## Saídas geradas
Os arquivos de saída serão gravados em:

- `ATT/paches/PATCH-01-auditoria-inicial/output/tree.txt`
- `ATT/paches/PATCH-01-auditoria-inicial/output/files.txt`
- `ATT/paches/PATCH-01-auditoria-inicial/output/configs.txt`
- `ATT/paches/PATCH-01-auditoria-inicial/output/scripts.txt`
- `ATT/paches/PATCH-01-auditoria-inicial/output/deps.txt`
- `ATT/paches/PATCH-01-auditoria-inicial/output/legado.txt`
- `ATT/paches/PATCH-01-auditoria-inicial/output/resumo.txt`

## Execução
```bash
bash ATT/paches/PATCH-01-auditoria-inicial/run-auditoria.sh
