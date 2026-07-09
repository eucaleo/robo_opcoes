# Auditoria de Desenvolvimento - RTD Excel BTG Online

Este arquivo registra a evolucao auditada da frente RTD Excel BTG Online.


## Camada reutilizavel de leitura RTD Excel

Data/hora: 09/07/2026 18:39:34
Branch: refactor/bd-unico-appdb
Evidencias: FRENTE_RTD_EXCEL_BTG_ONLINE/output/excel_rtd_reader_20260709_183928

### Alteracao executada

Criada a camada:

app/services/excel_rtd_reader.py

Criado o teste operacional:

scripts/test_excel_rtd_reader.py

### Responsabilidades implementadas

- Anexar ao Excel ja aberto via COM.
- Localizar workbook LISTA_RTD.xlsm.
- Localizar aba RTD_OPTION_QUOTES.
- Ler UsedRange em bloco.
- Normalizar cabecalhos.
- Validar campos obrigatorios.
- Normalizar registros de opcoes.
- Retornar resultado estruturado sem gravar banco.
- Manter esta etapa sem historico, candles, alertas ou UI.

### Teste executado

python scripts/verify_rtd_excel_resume.py --strict

python scripts/test_excel_rtd_reader.py --sheet RTD_OPTION_QUOTES --min-records 1

### Conclusao

A camada reutilizavel de leitura RTD Excel foi criada e validada contra a planilha RTD viva.

Proximo passo previsto:

Integrar esta camada ao snapshot atual, ainda sem historico temporal e sem candles.

