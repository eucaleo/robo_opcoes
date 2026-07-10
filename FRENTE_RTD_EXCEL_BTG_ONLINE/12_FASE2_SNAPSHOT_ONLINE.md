# Fase 2 parcial: snapshot RTD online de opcoes

Data: 2026-07-09

## Decisao

A tabela rtd_option_quotes passa a ser tratada como o snapshot atual centralizado de opcoes vindo do Excel RTD vivo.

## Fluxo implementado

Origem: LISTA_RTD.xlsm, aba RTD_OPTION_QUOTES.

Leitor: services.excel_rtd_reader.read_excel_rtd_options_as_dict.

Servico de sincronizacao: services.rtd_option_quotes_sync_service.sync_rtd_option_quotes_from_excel.

Repositorio: repositories.rtd_option_quotes_repository.RtdOptionQuotesRepository.upsert_many.

Destino: dados/app.db, tabela rtd_option_quotes.

## Escopo incluido

- Sincronizacao em bloco.
- Sobrescrita por codigo_opcao.
- Uma linha logica por simbolo.
- Normalizacao defensiva de numeros no repositorio.
- Preservacao de created_at.
- Atualizacao de updated_at.
- Script operacional scripts/sync_excel_rtd_option_quotes.py.
- Script de loop scripts/run_excel_rtd_option_quotes_snapshot_loop.py.
- Testes sem dependencia real do Excel.

## Fora do escopo nesta etapa

- Historico intraday.
- Candles.
- Alertas.
- Atualizacao de UI.
- Remocao de scripts legados.
- Consulta RTD sob demanda por simbolo.

## Criterio atendido

A aplicacao passa a ter uma ponte direta entre o Excel RTD vivo e o snapshot atual rtd_option_quotes, sem depender do fluxo legado CSV ou subprocesso para consulta individual.
