# RTD Excel Online - Fase 1 - Contrato arquitetural

## Objetivo

Registrar o fechamento da Fase 1 da integração RTD Excel Online.

A Fase 1 valida a leitura e sondagem do Excel desktop ativo via COM, sem abrir novas instâncias do Excel e sem recorrer a mecanismos externos como subprocessos, xlwings ou automações paralelas.

## Garantias da Fase 1

A implementação da Fase 1 garante que:

- O Excel é acessado somente quando já existe uma instância ativa.
- Não há abertura de nova instância do Excel no fluxo validado.
- Não há uso de Dispatch.
- Não há uso de DispatchEx.
- Não há uso de subprocess no fluxo da Fase 1.
- Não há uso de xlwings no fluxo da Fase 1.
- O acesso direto a win32com fica centralizado no gateway COM.
- A chamada direta a GetActiveObject fica centralizada no gateway COM.
- A UI consulta o status RTD Excel por payload formatado.
- O menu operacional expõe a ação Status RTD Excel.

## Gateway COM

O acesso COM direto fica restrito a:

services/excel_rtd_com_access.py

Esse arquivo centraliza:

- Import direto de win32com.client.
- Chamada direta a GetActiveObject.
- Normalização do erro quando não há Excel ativo.

## Arquivos cobertos pelo contrato arquitetural

O contrato arquitetural da Fase 1 cobre os arquivos:

services/excel_rtd_com_access.py
services/excel_rtd_reader.py
services/excel_rtd_workbook_probe.py
services/rtd_excel_probe_service.py
rtd_bridge/excel_rtd_connection_status.py
rtd_bridge/excel_rtd_connection_status_presenter.py
UI/modern/dark_window.py

## Teste de contrato arquitetural

O contrato está automatizado em:

ATT/tests/test_excel_rtd_phase1_architecture_contract.py

Esse teste verifica:

- Arquivos esperados da Fase 1 existem.
- subprocess e xlwings não são importados.
- win32com só é importado diretamente no gateway COM.
- Dispatch e DispatchEx não são chamados.
- GetActiveObject só é chamado diretamente no gateway COM.

## Testes de validação

Com Excel desktop aberto e workbook operacional carregado, executar:

python -m pytest ATT/tests/test_excel_rtd_reader.py ATT/tests/test_excel_rtd_workbook_probe_contract.py ATT/tests/test_excel_rtd_connection_status.py ATT/tests/test_excel_rtd_connection_status_presenter.py ATT/tests/test_rtd_excel_probe_service.py ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py ATT/tests/test_excel_rtd_phase1_architecture_contract.py -q

Resultado registrado no fechamento:

31 passed

## Observação operacional

O teste operacional de UI e Excel depende de ambiente real:

- Excel desktop aberto.
- Workbook LISTA_RTD.xlsm aberto.
- Aba RTD_OPTION_QUOTES disponível.
- Cabeçalhos obrigatórios presentes.
- Excel acessível via COM pela mesma sessão e permissão do processo Python.

Se o Excel não estiver aberto ou não estiver acessível pela Running Object Table, o teste operacional deve falhar.

## Commits relacionados

3fe0da0 Centraliza acesso COM da sondagem RTD Excel fase 1
f84d4af Adiciona contrato arquitetural RTD Excel fase 1

## Status final

Fase 1 RTD Excel Online fechada com:

- Acesso COM centralizado.
- Contrato arquitetural automatizado.
- Teste operacional real validado.
- Pacote de testes da Fase 1 aprovado.
