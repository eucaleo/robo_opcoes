# Auditoria de Desenvolvimento - RTD Excel BTG Online

Este arquivo registra a evolucao auditada da frente RTD Excel BTG Online.


## Camada reutilizavel de leitura RTD Excel

Data/hora: 09/07/2026 18:39:34
Branch: refactor/bd-unico-appdb
Evidencias: FRENTE_RTD_EXCEL_BTG_ONLINE/output/excel_rtd_reader_20260709_183928

### Alteracao executada

Criada a camada:

services/excel_rtd_reader.py

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


## Correcao arquitetural - services canonico

Data/hora: 09/07/2026 18:49:41
Branch: refactor/bd-unico-appdb

### Problema identificado

O leitor reutilizavel RTD Excel havia sido criado em:

app/services/excel_rtd_reader.py

Porem a pasta nativa/canonica de services do sistema ja existe desde o inicio em:

services/

### Correcao executada

O arquivo foi movido para:

services/excel_rtd_reader.py

O import do teste operacional foi corrigido para:

from services.excel_rtd_reader import read_excel_rtd_options_as_dict

A pasta app/services foi removida para evitar duplicidade arquitetural.

### Decisao arquitetural

A partir desta correcao, a frente RTD Excel deve reutilizar a pasta canonica services/ e nao criar nova arvore app/services/.

