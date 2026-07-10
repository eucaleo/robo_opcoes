# Auditoria RTD Online

## Fase 1 - Transformar RTD em fonte online

Status: encerrada tecnicamente.

Commit de encerramento:

12601f8 refactor: remove subprocess RTD operacional do editor de estrutura

Critérios validados:

- Detecção de Excel/RTD aberta testada.
- Leitura de workbook RTD testada.
- Leitura da tabela RTD testada.
- Sincronização para rtd_option_quotes testada.
- Status RTD na UI testado.
- Bridge legado isolado.
- Subprocesso operacional removido do preenchimento de leg.

Testes de referência:

- ATT/tests/test_excel_rtd_connection_status.py
- ATT/tests/test_excel_rtd_connection_status_presenter.py
- ATT/tests/test_excel_rtd_reader.py
- ATT/tests/test_excel_rtd_workbook_probe_contract.py
- ATT/tests/test_rtd_option_quotes_sync_service.py
- ATT/tests/test_rtd_option_quotes_bridge.py
- ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py
- ATT/tests/test_structure_editor_dialog_no_rtd_subprocess.py

Resultado registrado:

23 passed

Grep proibitivo validado em UI/components/structure_editor_dialog.py:

- import subprocess
- subprocess.run
- Popen
- refresh_rtd_symbol_to_option_quotes

Resultado:

Sem ocorrências.

## Fase 2 - Snapshot centralizado

Status: em andamento.

Decisão técnica:

A tabela rtd_option_quotes passa a ser tratada formalmente como snapshot centralizado atual de cotações RTD.

Contrato operacional:

- Uma linha lógica por codigo_opcao.
- Símbolo normalizado por UPPER(TRIM(codigo_opcao)).
- Atualização por sobrescrita.
- Sem histórico intraday nesta fase.
- Histórico temporal será tratado somente na Fase 3.
- Candles serão tratados somente na Fase 4.

Primeiro fechamento técnico da Fase 2:

- Criar índice operacional por codigo_opcao.
- Criar índice único normalizado por UPPER(TRIM(codigo_opcao)).
- Criar índice auxiliar por ativo_base.
- Deduplicar resíduos legados de snapshot preservando a linha de maior id.
- Normalizar símbolos existentes.
- Testar o contrato físico do snapshot.

## Fase 2.2 - UI consumindo apenas snapshot centralizado

O fluxo do botao Preencher via RTD em StructureEditorDialog foi ajustado para
nao sincronizar Excel diretamente e nao depender de subprocessos.

Contrato operacional atual:

    UI -> RtdOptionQuotesRepository -> StructureLegRtdEnrichmentService

A tabela rtd_option_quotes passa a ser a unica fonte consultada pela tela para
preenchimento de legs via RTD. A atualizacao dessa tabela fica fora do fluxo da UI,
preservando separacao de responsabilidades:

- produtor externo mantem o snapshot RTD atualizado
- UI apenas consulta o snapshot
- enrichment monta os dados da leg a partir do repositorio
- ausencia de cotacao gera aviso orientando atualizar o snapshot

Guardrail adicionado em teste para impedir reintroducao de:

- rtd_option_quotes_sync_service na UI
- sync_rtd_option_quotes_from_excel na UI
