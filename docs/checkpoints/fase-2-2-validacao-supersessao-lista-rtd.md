# Fase 2.2 — Validação da supersessão LISTA_RTD

Data: 2026-06-17 09:44:22 -0300

## Objetivo

Validar que a decisão de supersessão de `LISTA_RTD.xlsx` por `LISTA_RTD.xlsm` foi registrada, publicada e está coerente com o estado atual do repositório.

## Estado Git

```text
## fase-12-fechamento-ciclo...origin/fase-12-fechamento-ciclo
?? docs/checkpoints/fase-2-2-validacao-supersessao-lista-rtd.md
```

## Último commit

```text
4cb4f50 docs: registra supersessao de LISTA_RTD xlsx
 docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md     | 10 ++++++
 .../2026-06-17-supersessao-lista-rtd-xlsx.md       | 39 ++++++++++++++++++++++
 2 files changed, 49 insertions(+)
```

## Decisão registrada

```text
# Decisão — Supersessão de LISTA_RTD.xlsx por LISTA_RTD.xlsm

Data: 2026-06-17

## Contexto

Durante a reconciliação da ponte RTD, foram encontradas referências remanescentes a `LISTA_RTD.xlsx` em documentos históricos, checkpoints, validações antigas e no mapeamento documental `docs/mapeamento_automacao_opcoes_rtd.json`.

Também foi confirmado que os scripts funcionais atuais usam `LISTA_RTD.xlsm` como workbook padrão:

- `scripts/import_lista_rtd_excel_to_option_quotes.py`
- `scripts/run_lista_rtd_option_quotes_pipeline.py`

## Decisão

A ponte RTD operacional oficial passa a ser, de forma consolidada:

`LISTA_RTD.xlsm`

A planilha `LISTA_RTD.xlsx` fica classificada como referência legada/histórica e não deve ser usada como ponte operacional atual.

## Regra de interpretação

Referências antigas a `LISTA_RTD.xlsx` em documentos, checkpoints, auditorias ou mapeamentos anteriores devem ser lidas como histórico do processo, salvo se uma nova evidência funcional ativa demonstrar consumo real em código de produção.

## Impacto

- Não alterar checkpoints históricos apenas para trocar nomes.
- Não reintroduzir `LISTA_RTD.xlsx` como dependência operacional.
- Manter `LISTA_RTD.xlsx` protegido no `.gitignore`.
- Manter `LISTA_RTD.xlsm` versionável e tratado como ponte RTD oficial.
- Documentos vivos podem receber notas de supersessão para evitar ambiguidade.

## Evidências

Checkpoints relacionados:

- `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md`
- `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`
```

## Nota registrada na Rota Mestre 3

```text
### Fase 5 — Reconciliação RTD/Excel

Validar workbook, abas disponíveis e contrato de leitura.

### Fase 6 — Retomada funcional controlada

Somente após banco, arquivos e contratos estarem reconciliados.

---

## Status atual

Fase 0 em andamento.

A rota ainda não autoriza alteração funcional, criação de tabela ou limpeza destrutiva.

## Nota de supersessão — LISTA_RTD.xlsx

A partir da reconciliação registrada em `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md` e `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`, a ponte RTD operacional oficial é `LISTA_RTD.xlsm`.

Referências anteriores a `LISTA_RTD.xlsx` devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.

A decisão formal está registrada em:

- `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`
```

## Verificação de referências operacionais fora de docs

```text
scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
scripts/import_lista_rtd_excel_to_option_quotes.py:537:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
```

## Resultado

- `LISTA_RTD.xlsm` permanece como ponte RTD operacional oficial.
- `LISTA_RTD.xlsx` permanece classificada como referência legada/histórica.
- A decisão viva foi registrada em `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`.
- A Rota Mestre 3 recebeu nota de supersessão.
- Nenhuma alteração funcional foi realizada nesta etapa.

## Decisão de fechamento

A reconciliação documental da ponte RTD fica concluída para esta etapa.
