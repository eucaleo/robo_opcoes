# AUDITORIA_ROTA_MESTRE_3

## Objetivo

Este arquivo registra a auditoria contínua da ROTA_MESTRE_3 — Reconciliação pós-backup e retomada controlada.

A finalidade é manter rastreabilidade entre plano, execução, testes, decisões e Git.

---

## Regras desta auditoria

1. Nenhuma alteração funcional deve ocorrer sem fase definida.
2. Nenhuma limpeza destrutiva deve ocorrer antes do inventário.
3. Nenhuma tabela deve ser criada antes da auditoria de schema.
4. Nenhuma alteração em UI, API, repository ou serviço deve ocorrer antes do mapa de impacto.
5. Cada fase deve ter comandos e resultados registrados.
6. Cada fase encerrada deve ter commit relacionado.
7. Se houver dúvida sobre histórico, consultar o Git antes de alterar.
8. O banco local não deve ser versionado.
9. Arquivos operacionais devem ser classificados antes de exclusão.
10. O Excel permanece apenas como gateway RTD.

---

## Estado inicial conhecido

```text
branch: fase-12-fechamento-ciclo
commit HEAD inicial conhecido: 17a173c
estado informado: banco limpo
rtd_option_quotes: ausente
structures: vazia
structure_legs: vazia
```

---

# Fase 0 — Marco documental e congelamento da rota

## Status

Encerrada.

## Objetivo

Criar os documentos de controle da ROTA_MESTRE_3 e congelar a retomada antes de qualquer alteração funcional.

## Arquivos alterados

```text
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
docs/AUDITORIA_ROTA_MESTRE_3.md
```

## Comandos executados

```bash
ls -l docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md docs/AUDITORIA_ROTA_MESTRE_3.md 2>/dev/null || true
sed -n "1,160p" docs/AUDITORIA_ROTA_MESTRE_3.md 2>/dev/null || echo "AUDITORIA_ROTA_MESTRE_3.md ainda não existe"
tail -n 30 docs/AUDITORIA_ROTA_MESTRE_3.md 2>/dev/null || true
git status -sb
```

## Resultado observado

O arquivo de auditoria anterior estava incompleto/corrompido e continha trecho inválido com delimitador inserido no conteúdo.

Também foi observado:

```text
D OPERACOES_E_OPCOES.xlsm
?? _usage_audit/
?? docs/AUDITORIA_ROTA_MESTRE_3.md
```

## Evidências antecipadas sobre rtd_option_quotes

A auditoria em dados/app.db retornou:

```text
Status: error
Erro: table not found: rtd_option_quotes
```

O teste do auditor passou:

```text
ATT/tests/test_audit_rtd_option_quotes.py: 7 passed
```

O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:

```text
Tentadas: RTD_OPTION_QUOTES, RTD_PROBE_OPTIONS
Disponível: RTD-BTG LISTA
```

## Testes executados

Nenhum teste funcional pertence à Fase 0.

Foram executados diagnósticos e testes antecipados para evidência da futura Fase 3.

## Pendências

- Conferir se os dois documentos foram gerados completos.
- Conferir git diff.
- Classificar OPERACOES_E_OPCOES.xlsm.
- Classificar _usage_audit/.
- Commitar documentação da Fase 0.

## Decisão tomada

A Fase 0 foi encerrada após criação, conferência e commit dos documentos de controle.

Nenhuma alteração funcional está autorizada.

Nenhuma tabela deve ser criada.

Nenhuma limpeza destrutiva está autorizada.

## Commit relacionado

```text
8556050 docs: inicia ROTA_MESTRE_3 de reconciliacao pos-backup
```
