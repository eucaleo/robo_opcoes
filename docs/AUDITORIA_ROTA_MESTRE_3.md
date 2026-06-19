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
D planilha RTD legada abolida
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
- Classificar ponte RTD atual e planilha RTD legada abolida.
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

---

# Fase 1 — Higiene controlada do estado Git

## Status

Concluída.

## Objetivo

Classificar alterações pendentes no estado Git antes de qualquer limpeza destrutiva ou retomada funcional.

## Diagnóstico executado

~~~text
git status -sb
git diff --name-status
git ls-files --stage -- arquivo RTD legado
git cat-file -s HEAD:arquivo RTD legado
git log --oneline -10 -- arquivo RTD legado
find _usage_audit -maxdepth 3 -type f
~~~

## Resultado observado

~~~text
branch: fase-12-fechamento-ciclo
ahead: 5
planilha RTD legada: removida do working tree
_usage_audit/: diretório local não versionado
~~~

O arquivo anteriormente usado como ponte RTD foi abolido do sistema.

A ponte RTD atual passa a ser:

~~~text
LISTA_RTD.xlsm
~~~

A remoção da planilha RTD legada não deve ser revertida.

Nenhuma referência documental nova deve ressuscitar o arquivo abolido.

## Substituição documental executada

Foi executada substituição em documentos Markdown para consolidar o nome atual da ponte RTD:

~~~text
LISTA_RTD.xlsm
~~~

Após a substituição, a busca documental não retornou referências ao nome legado.

## Classificação de _usage_audit/

O diretório `_usage_audit/` existe localmente, possui aproximadamente 20K e contém 13 arquivos de auditoria de uso de scripts.

Arquivos observados:

~~~text
_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_arquivos_encontrados.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_git_log.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_referencias.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_referencias_testes.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_arquivos_encontrados.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_git_log.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_referencias.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_referencias_testes.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_arquivos_encontrados.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_git_log.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_referencias.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_referencias_testes.txt
_usage_audit/uso_scripts_2026-06-16_13-40-00/RESUMO.md
~~~

## Decisão sobre _usage_audit/

O diretório `_usage_audit/` foi classificado como evidência documental da auditoria de uso de scripts.

Decisão tomada: versionar o diretório integralmente, sem limpeza destrutiva.

A classificação foi concluída após conferência de tamanho, conteúdo e staging seletivo.

## Restrições mantidas

Nenhuma alteração funcional está autorizada.

Nenhuma tabela deve ser criada.

Nenhuma limpeza destrutiva está autorizada.

## Commit relacionado

~~~text
440c6d5 docs: substitui referencia da planilha RTD legada
cb92957 docs: adiciona evidencias de auditoria de uso
~~~

## Encerramento da Fase 1

A Fase 1 foi encerrada com working tree limpo.

Resultado final observado:

~~~text
git status -sb
## fase-12-fechamento-ciclo...origin/fase-12-fechamento-ciclo [ahead 7]
~~~

A planilha `LISTA_RTD.xlsm` foi preservada como ponte RTD oficial e testada.

A planilha RTD legada abolida foi removida do versionamento. A entrada `LISTA_RTD.xlsx` deixou de ser tratada como ponte RTD oficial.

O diretório `_usage_audit/` foi versionado como evidência de auditoria.

Nenhuma alteração funcional foi executada.

Nenhuma tabela foi criada.

Nenhuma limpeza destrutiva adicional foi executada.

---

## Nota de supersessão — LISTA_RTD.xlsx

Esta auditoria pode conter referências históricas a `LISTA_RTD.xlsx` feitas durante a reconciliação da ponte RTD.

A interpretação atual consolidada está definida em `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`:

- `LISTA_RTD.xlsm` é a ponte RTD operacional oficial.
- `LISTA_RTD.xlsx` é referência legada/histórica.
- Referências anteriores a `LISTA_RTD.xlsx` nesta auditoria devem ser lidas como evidência do processo de reconciliação, não como contrato operacional vigente.

---

# Fase 6.7 — Consolidação de diagnóstico RTD/canonical pricing

## Status

Concluída documentalmente.

## Objetivo

Consolidar o diagnóstico do fluxo RTD/canonical pricing e registrar baseline documental antes da criação de novos guardrails.

## Arquivos de checkpoint e evidência

    docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md
    docs/checkpoints/evidencias/fase-6-7-inventario-diagnostico-rtd-canonical.txt
    docs/checkpoints/evidencias/fase-6-7-pytest-baseline-canonical-rtd.txt
    docs/checkpoints/evidencias/fase-6-7-pytest-baseline-rtd-option-quotes.txt
    docs/checkpoints/evidencias/fase-6-7-recorte-funcional-rtd-canonical.txt

## Commit relacionado

    4960ca0 docs: consolidate fase 6.7 rtd canonical diagnostics

## Resultado observado

A fase registrou inventário, baseline e recorte funcional do caminho RTD/canonical pricing.

Nenhuma alteração funcional destrutiva foi registrada nesta fase.

---

# Fase 6.8 — Guardrail da matriz de diagnóstico RTD/canonical pricing

## Status

Concluída e integrada.

## Objetivo

Adicionar proteção automatizada para a matriz de diagnóstico RTD/canonical pricing.

## Arquivos alterados ou adicionados

    ATT/tests/test_canonical_pricing_facade.py
    docs/checkpoints/fase-6-8-guardrail-matriz-diagnostico-rtd.md
    docs/checkpoints/evidencias/fase-6-8-pytest-guardrail-matriz-diagnostico-rtd.txt

## Commits relacionados

    b2ad0b3 test: add guardrail matriz diagnostico rtd canonical
    4cb1b7b merge: integra fase 6.8 guardrail matriz diagnostico rtd canonical

## Resultado observado

A fase adicionou guardrail de teste para proteger a matriz de diagnóstico RTD/canonical.

A integração foi realizada por merge controlado na linha principal.

Nenhuma alteração de UI/API foi executada.

O Excel permaneceu apenas como gateway RTD.

---

# Fase 6.9 — Ajuste de parsing numérico RTD no canonical pricing

## Status

Concluída, integrada e etiquetada.

## Objetivo

Tornar o parsing numérico de preços RTD no canonical pricing mais robusto e proteger o comportamento com testes.

## Arquivos alterados ou adicionados

    services/canonical_pricing_facade.py
    ATT/tests/test_canonical_pricing_facade.py
    docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md
    docs/checkpoints/evidencias/fase-6-9-pytest-canonical-pricing-rtd-number-formats.txt
    docs/checkpoints/evidencias/fase-6-9-pytest-pricing-execution-services.txt

## Commits relacionados

    beba13f fix: robust rtd canonical pricing number parsing
    dddbec8 merge: integra fase 6.9 ajuste rtd canonical pricing

## Tag relacionada

    fase-6-9-rtd-canonical-pricing

## Resultado observado

A fase ajustou o parsing numérico RTD no canonical pricing e adicionou cobertura para formatos numéricos.

As evidências de pytest foram registradas em docs/checkpoints/evidencias/.

A fase foi integrada à main no commit dddbec8.

---

# Fase 6.10 — Restauração e sincronização documental da ROTA_MESTRE_3

## Status

Em encerramento.

## Objetivo

Restaurar os documentos principais da ROTA_MESTRE_3, confirmar seu conteúdo e sincronizar a auditoria com as Fases 6.7, 6.8 e 6.9.

## Branch

    fase-6-10-restaura-documentacao-rota-mestre-3

## Arquivos restaurados

    docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
    docs/AUDITORIA_ROTA_MESTRE_3.md

## Commit de restauração

    1a20cea docs: restaura rota mestre 3 e auditoria

## Comandos executados

    git checkout main
    git pull --ff-only origin main
    git checkout -b fase-6-10-restaura-documentacao-rota-mestre-3
    git ls-tree -r --name-only 8a56969 docs | grep -E "ROTA_MESTRE_3|AUDITORIA_ROTA_MESTRE_3"
    git show 8a56969:docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md | sed -n '1,120p'
    git show 8a56969:docs/AUDITORIA_ROTA_MESTRE_3.md | sed -n '1,160p'
    git checkout 8a56969 -- docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md docs/AUDITORIA_ROTA_MESTRE_3.md
    git status --short
    git diff --check
    git add docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md docs/AUDITORIA_ROTA_MESTRE_3.md
    git commit -m "docs: restaura rota mestre 3 e auditoria"

## Resultado observado

    A  docs/AUDITORIA_ROTA_MESTRE_3.md
    A  docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md

Após commit:

    1a20cea docs: restaura rota mestre 3 e auditoria

O working tree ficou limpo.

## Observação sobre erro de terminal

Após o commit, houve colagem acidental de prompt e saída do terminal como se fossem comandos.

Foram observados erros como:

    bash: syntax error near unexpected token '('
    bash: $: command not found

Esses erros não representaram falha do Git nem alteração funcional. O estado final observado permaneceu consistente.

## Sincronização executada

Foram localizados e registrados os artefatos das Fases 6.7, 6.8 e 6.9:

    docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md
    docs/checkpoints/fase-6-8-guardrail-matriz-diagnostico-rtd.md
    docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md

Evidências relacionadas:

    docs/checkpoints/evidencias/fase-6-7-inventario-diagnostico-rtd-canonical.txt
    docs/checkpoints/evidencias/fase-6-7-pytest-baseline-canonical-rtd.txt
    docs/checkpoints/evidencias/fase-6-7-pytest-baseline-rtd-option-quotes.txt
    docs/checkpoints/evidencias/fase-6-7-recorte-funcional-rtd-canonical.txt
    docs/checkpoints/evidencias/fase-6-8-pytest-guardrail-matriz-diagnostico-rtd.txt
    docs/checkpoints/evidencias/fase-6-9-pytest-canonical-pricing-rtd-number-formats.txt
    docs/checkpoints/evidencias/fase-6-9-pytest-pricing-execution-services.txt

## Decisão

A Fase 6.10 é estritamente documental.

Nenhuma alteração funcional está autorizada nesta fase.

Nenhuma alteração de banco está autorizada nesta fase.

Nenhuma alteração de UI/API está autorizada nesta fase.

A próxima etapa somente poderá avançar após commit e integração da documentação restaurada e sincronizada.
