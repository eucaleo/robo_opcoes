# Mapa do contrato RTD/Excel — Fase 2

Documento de encerramento da Fase 2 da `ROTA_MESTRE_2`.

Baseado nos diagnósticos:

- `docs/fase_2_auditoria_contrato_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.json`

## Escopo

Esta fase auditou, sem alteração funcional, arquivos locais relacionados ao contrato entre RTD, Excel e bridge.

Nenhum arquivo operacional foi modificado.

## Classificação dos arquivos

### `dados/RTD_LINKS.csv`

- Existe: `True`
- Classe: `fonte local RTD em formato atributo/valor`
- Papel provável: Contrato simples para atributos de opções vindos de RTD/Excel.
- Criticidade: `alta`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `7`
- Decisão: Preservar como contrato estável para auditoria da Fase 3.

Cabeçalho identificado:

`codigo_opcao`, `ativo_base`, `campo`, `valor`, `atualizado_em`

### `bridge/analise_robo.csv`

- Existe: `True`
- Classe: `resumo agregado por estrutura/aba`
- Papel provável: Arquivo consolidado com métricas por ativo/aba, incluindo gregas líquidas, PL e alertas.
- Criticidade: `alta`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `5`
- Decisão: Tratar como saída agregada/exportada do fluxo atual.

Cabeçalho identificado:

`ABA`, `SPOT`, `NUM_PERNAS`, `DTE_MIN`, `PL_REALISTA_TOTAL`, `DELTA_LIQ`, `GAMMA_LIQ`, `THETA_LIQ`, `VEGA_LIQ`, `SPREAD_MEDIO`, `SPREAD_PCT_MEDIO`, `ALERTAS_V2`

### `bridge/analise_robo_legs.csv`

- Existe: `True`
- Classe: `snapshot operacional por perna`
- Papel provável: Arquivo mais completo para pernas de estruturas, contendo bid, ask, spread, IV, gregas, strike, vencimento, DTE e PL.
- Criticidade: `alta`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `20`
- Decisão: Tratar como principal contrato operacional de pernas para leitura/auditoria.

Cabeçalho identificado:

`TIMESTAMP`, `ABA`, `ATIVO`, `C/V`, `CALL_/_PUT`, `QUANT`, `VALOR_EXECUTADO`, `BID`, `ASK`, `SPREAD`, `SPREAD_PCT`, `IV`, `DELTA`, `GAMMA`, `THETA`, `VEGA`, `STRIKE`, `VENCIMENTO`, `DTE`, `PL_REALISTA`

### `bridge/hist_robo.csv`

- Existe: `True`
- Classe: `histórico legado ou série temporal`
- Papel provável: Histórico com múltiplos registros por timestamp e conjunto reduzido de colunas.
- Criticidade: `média`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `2400`
- Decisão: Preservar como fonte histórica/legado; não usar como contrato primário sem normalização.

Cabeçalho identificado:

`TIMESTAMP`, `ABA`, `ATIVO`, `C/V`, `QUANT`, `VALOR_EXECUTADO`, `BID`, `ASK`, `DELTA`, `GAMMA`, `THETA`, `VEGA`, `PL_REALISTA`

### `bridge/configuracoes.csv`

- Existe: `True`
- Classe: `configuração operacional`
- Papel provável: Parâmetros de operação, limites e janelas de snapshot.
- Criticidade: `média`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `4`
- Decisão: Auditar encoding e nomes de parâmetros antes de qualquer uso automatizado.

Cabeçalho identificado:

`Par�metro`, `Valor`, `Descri��o`

### `bridge/analise_raiox.csv`

- Existe: `True`
- Classe: `relatório textual derivado`
- Papel provável: Resumo textual de análise por aba.
- Criticidade: `baixa`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `25`
- Decisão: Tratar como derivado/explicativo, não como fonte canônica.

Cabeçalho identificado:

`ABA`, `TIMESTAMP`, `ANALISE_RAIOX`

### `bridge/consolidacoes.csv`

- Existe: `True`
- Classe: `consolidação financeira por aba`
- Papel provável: Totais executados, totais atuais, ganho atual, PL realizado e PL total.
- Criticidade: `média`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `5`
- Decisão: Tratar como derivado consolidado; validar contra pernas antes de uso como verdade.

Cabeçalho identificado:

`TIMESTAMP`, `ABA`, `PERNAS_ABERTAS`, `TOTAL_EXECUTADO_ABERTO`, `TOTAL_ATUAL_ABERTO`, `GANHO_ATUAL_ABERTO`, `PL_REALIZADO`, `PL_TOTAL`, `OBS`

### `bridge/encerramentos_manuais.csv`

- Existe: `True`
- Classe: `eventos manuais`
- Papel provável: Registro manual de encerramentos, com delimitador divergente.
- Criticidade: `média`
- Delimitador provável: `;`
- Linhas estimadas sem cabeçalho: `6`
- Decisão: Preservar como entrada manual/eventual; exige tratamento específico de delimitador.

Cabeçalho identificado:

`Data`, `ABA`, `Código`, `Tipo`, `Qtd`, `Preço Real`, `Motivo`, `Observação`, ``, ``, ``

### `bridge/rolls_detectados.csv`

- Existe: `True`
- Classe: `eventos de roll`
- Papel provável: Registro de eventos de abertura/roll detectados, com códigos, preços e observações.
- Criticidade: `média`
- Delimitador provável: `,`
- Linhas estimadas sem cabeçalho: `20`
- Decisão: Tratar como log/evento operacional; auditar encoding antes de automatizar.

Cabeçalho identificado:

`Data`, `ABA`, `Evento`, `C�digo_Rolado`, `Qtd`, `Pre�o_Saida`, `C�digo_Entrada`, `Pre�o_Entrada`, `PL_Real`, `PL_Estimado`, `Dif_%`, `Obs`

## Achados principais

### 1. Existem dois formatos diferentes de contrato

Foi identificado um contrato em formato atributo/valor:

- `dados/RTD_LINKS.csv`

E contratos tabulares por linha operacional:

- `bridge/analise_robo.csv`
- `bridge/analise_robo_legs.csv`
- `bridge/hist_robo.csv`
- demais arquivos `bridge/*.csv`

### 2. `bridge/analise_robo_legs.csv` é o contrato operacional mais rico

O arquivo contém campos relevantes para automação de opções:

- ativo/código da opção
- compra/venda
- call/put
- quantidade
- preço executado
- bid/ask
- spread
- volatilidade implícita
- gregas
- strike
- vencimento
- DTE
- PL realista

Portanto, deve ser tratado como candidato principal para leitura estruturada de pernas.

### 3. `bridge/analise_robo.csv` é agregado por estrutura/aba

O arquivo consolida métricas por `ABA`, como spot, número de pernas, DTE mínimo, PL total, gregas líquidas, spread médio e alertas.

Deve ser tratado como resumo derivado, não como fonte completa de pernas.

### 4. `bridge/hist_robo.csv` tem perfil histórico/legado

O arquivo possui volume maior e cabeçalho mais reduzido que `analise_robo_legs.csv`.

Deve ser preservado para histórico, mas não promovido a contrato canônico sem etapa própria de normalização.

### 5. Há divergência de delimitador

A maioria dos arquivos usa vírgula como delimitador.

Foi identificado uso de ponto e vírgula em:

- `bridge/encerramentos_manuais.csv`

Qualquer automação futura deve considerar delimitador por arquivo, não um delimitador global fixo.

### 6. Há sinais de problema de encoding

Foram identificados textos com caracteres corrompidos em arquivos como:

- `bridge/configuracoes.csv`
- `bridge/rolls_detectados.csv`

Exemplos observados no diagnóstico:

- `Par�metro`
- `Descri��o`
- `C�digo_Rolado`
- `Pre�o_Saida`
- `posi��o`

Nenhuma correção foi realizada nesta fase.

## Respostas às perguntas da Fase 2

### 1. Qual é o papel de `dados/RTD_LINKS.csv`?

É uma fonte local RTD em formato atributo/valor por opção, com colunas:

`codigo_opcao`, `ativo_base`, `campo`, `valor`, `atualizado_em`.

### 2. Quais colunas existem nos CSVs da pasta `bridge/`?

As colunas estão registradas no diagnóstico automático e resumidas neste mapa, arquivo por arquivo.

### 3. Quais arquivos parecem ser fonte primária?

Candidatos principais:

- `dados/RTD_LINKS.csv`, para atributos RTD/opções
- `bridge/analise_robo_legs.csv`, para pernas operacionais
- `bridge/encerramentos_manuais.csv`, para eventos manuais

### 4. Quais arquivos parecem ser derivados/exportados?

Prováveis derivados/exportados:

- `bridge/analise_robo.csv`
- `bridge/analise_raiox.csv`
- `bridge/consolidacoes.csv`
- `bridge/rolls_detectados.csv`

### 5. Há inconsistência de nomes de colunas entre arquivos?

Sim. Há diferenças relevantes, por exemplo:

- `ATIVO` em arquivos de pernas contra `codigo_opcao` em `RTD_LINKS.csv`
- `C/V` como nome operacional com caractere especial
- `CALL_/_PUT` como nome não canônico
- `Preço`/`Pre�o` em arquivos com encoding inconsistente

### 6. Há dependência direta ou indireta do Excel `.xlsm`?

A estrutura dos arquivos indica dependência indireta do Excel/bridge, mas esta fase não inspecionou o conteúdo interno do `.xlsm`.

A dependência deve ser tratada como provável até auditoria específica do arquivo Excel ou dos pontos de exportação.

### 7. Quais arquivos devem ser preservados como contrato estável?

Devem ser preservados para as próximas fases:

- `dados/RTD_LINKS.csv`
- `bridge/analise_robo_legs.csv`
- `bridge/analise_robo.csv`
- `bridge/hist_robo.csv`, como histórico/legado

### 8. Quais arquivos devem ser tratados como legado ou compatibilidade?

Devem ser tratados com cautela ou compatibilidade:

- `bridge/hist_robo.csv`
- `bridge/configuracoes.csv`
- `bridge/encerramentos_manuais.csv`
- `bridge/rolls_detectados.csv`

## Decisão de encerramento da Fase 2

A Fase 2 está encerrada como auditoria documental.

Ficam definidos como contratos prioritários para análise posterior:

1. `dados/RTD_LINKS.csv`
2. `bridge/analise_robo_legs.csv`
3. `bridge/analise_robo.csv`
4. `bridge/hist_robo.csv`

A próxima fase deve auditar a persistência de cotações RTD/opções sem alterar schema, ingestão ou cálculo.

Nenhuma alteração funcional foi autorizada por este documento.