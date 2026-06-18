# Fase 6.1 — Validacao operacional do pipeline RTD

## Objetivo
Registrar a validacao inicial do pipeline operacional de refresh RTD criado na Fase 6, mantendo a retomada funcional controlada conforme a ROTA_MESTRE_3.

## Escopo
Foram validados os scripts:

- `scripts/build_rtd_symbols.py`
- `scripts/import_rtd_option_quotes_wide_csv.py`
- `scripts/refresh_rtd_option_quotes_excel.ps1`
- `scripts/run_rtd_refresh_full.py`

O Excel permanece apenas como gateway RTD por meio de `LISTA_RTD.xlsm`.

## Comandos executados

- `git status --short`
- `python -m py_compile scripts/build_rtd_symbols.py scripts/import_rtd_option_quotes_wide_csv.py scripts/run_rtd_refresh_full.py`
- `python scripts/run_rtd_refresh_full.py --dry-run --db dados/derived.db`
- `git status --short`

## Resultado observado
O estado Git estava limpo antes da validacao.
A compilacao dos scripts Python foi concluida sem erro.
O dry-run do pipeline exibiu os comandos esperados para geracao de simbolos RTD, refresh da ponte Excel/RTD via `LISTA_RTD.xlsm` e importacao do CSV `dados/RTD_LINKS.csv` para o banco `dados/derived.db`.
Nenhuma execucao real do Excel foi feita durante o dry-run.
Nenhuma importacao real do CSV foi executada durante o dry-run.
Nenhuma alteracao funcional ampla em UI, API, repository ou servico foi realizada.
O Git permaneceu limpo apos a validacao.

## Estado reportado pelo pipeline
O pipeline reportou, antes da execucao simulada, o seguinte estado para a base informada:

```json
{
  "count": null,
  "max_updated_at": null
}
```
Esse resultado foi tratado como compatível com a etapa de validacao operacional, sem criacao manual de tabela nesta fase.

## Tabela `rtd_option_quotes`
Esta etapa nao teve como objetivo criar manualmente tabela nem alterar schema diretamente.
A eventual criacao, validacao ou atualizacao da tabela `rtd_option_quotes` deve permanecer subordinada ao pipeline controlado e aos scripts versionados.

## Criterio de encerramento
A Fase 6.1 e considerada encerrada porque:

- os scripts Python compilam sem erro;
- o dry-run do pipeline apresenta os comandos esperados;
- o Excel permanece tratado apenas como gateway RTD;
- nenhuma execucao real do Excel foi feita nesta validacao;
- nenhuma alteracao de schema foi feita manualmente;
- nenhuma alteracao em UI, API, repository ou servico foi realizada;
- o Git permaneceu limpo apos a validacao, exceto pela criacao deste checkpoint documental.

## Proxima etapa controlada
A proxima etapa deve preparar a execucao real controlada do pipeline RTD, explicitando previamente:

1. se o Excel sera aberto visivel ou oculto;
2. se `dados/RTD_LINKS.csv` podera ser criado ou sobrescrito;
3. se `dados/rtd_symbols.txt` podera ser criado ou sobrescrito;
4. se `dados/derived.db` podera ser atualizado;
5. quais validacoes serao feitas apos a execucao;
6. qual commit registrara o fechamento.

## Commit relacionado
A registrar apos commit deste checkpoint.
