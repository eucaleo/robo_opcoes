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
