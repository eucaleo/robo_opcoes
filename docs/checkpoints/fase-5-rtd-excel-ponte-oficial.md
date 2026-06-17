# Checkpoint - Fase 5 - Ponte oficial RTD Excel

Data: 2026-06-17  
Branch: fase-12-fechamento-ciclo  
Modo: somente leitura / documental

## Objetivo

Registrar a identificacao e o mapeamento inicial da ponte oficial RTD via Excel, usando o arquivo `LISTA_RTD.xlsm` como fonte observada.

Esta fase foi conduzida sem alteracoes funcionais no sistema.

## Evidencias registradas

Foram adicionadas as seguintes evidencias:

- `docs/checkpoints/evidencias/fase-5-inventario-lista-rtd-xlsm.txt`
- `docs/checkpoints/evidencias/fase-5-mapa-formulas-rtd-lista-rtd.txt`

## Arquivo analisado

Arquivo:

- `LISTA_RTD.xlsm`

Propriedades observadas:

- Tamanho: 9126 bytes
- SHA256: `95e949390df399766497d1a64289dc1bcc917e6e9df820eeac4833e26c0bfda1`
- Formato: XLSM valido como pacote ZIP Office Open XML
- Macros VBA: nao encontradas (`xl/vbaProject.bin` ausente)

## Abas identificadas

Foram identificadas duas abas no workbook:

### 1. RTD_OPTION_QUOTES

Arquivo interno:

- `xl/worksheets/sheet1.xml`

Dimensao declarada:

- `A1:O5`

Formula RTD observada:

- 56 formulas RTD

Padrao observado:

- 4 linhas de ativos/simbolos
- 14 campos RTD por linha
- Simbolo referenciado em `$A2`, `$A3`, `$A4`, `$A5`
- Campos observados:
  - `QUOTE.UNDERLYING_SYMBOL`
  - `QUOTE.OPTION_TYPE`
  - `QUOTE.STRIKE_PRICE`
  - `QUOTE.MATURITYDATE`
  - `QUOTE.LAST_TRADE_PRICE`
  - `QUOTE.LAST_TRADE_QUANTITY`
  - `QUOTE.BID_PRICE`
  - `QUOTE.ASK_PRICE`
  - `QUOTE.VOLUME`
  - `QUOTE.IMPLIED_VOLATILITY`
  - `QUOTE.DELTA`
  - `QUOTE.GAMMA`
  - `QUOTE.THETA`
  - `QUOTE.VEGA`

### 2. RTD-BTG LISTA

Arquivo interno:

- `xl/worksheets/sheet2.xml`

Dimensao declarada:

- `A2:B95`

Formula RTD observada:

- 93 formulas RTD

Padrao observado:

- Catalogo/lista de topicos RTD
- Todas as formulas observadas referenciam o ativo `BPAC11`
- A aba aparenta funcionar como matriz documental de topicos suportados pelo RTD BTG

## Total observado

Total de formulas RTD encontradas no workbook:

- 149 formulas RTD

## Observacoes importantes

Foram observados topicos potencialmente semelhantes, mas distintos, por exemplo:

- `QUOTE.CHGPERCENT`
- `QUOTE.CHANGE_PERCENT`

Nenhuma normalizacao, correcao ou deduplicacao foi realizada nesta fase.

A regra adotada foi preservar o contrato observado no Excel exatamente como encontrado.

## Decisoes da Fase 5

A partir das evidencias coletadas, fica registrado que:

1. `LISTA_RTD.xlsm` e a fonte observada da ponte oficial RTD Excel.
2. A aba `RTD_OPTION_QUOTES` contem o subconjunto mais diretamente relacionado a opcoes.
3. A aba `RTD-BTG LISTA` contem uma lista ampla de topicos RTD associados ao provedor `btg_pro_rtd`.
4. A proxima etapa deve ser de reconciliacao documental entre:
   - campos RTD observados no Excel;
   - modelo/tabela `rtd_option_quotes`;
   - campos atualmente consumidos pela aplicacao;
   - comportamento esperado da tela/opcoes.
5. Nenhuma implementacao deve ser feita antes de novo checkpoint autorizando alteracao funcional.

## Restricoes mantidas

Durante esta fase:

- Nenhuma alteracao foi feita no arquivo Excel.
- Nenhuma alteracao foi feita em banco de dados.
- Nenhuma alteracao foi feita em UI.
- Nenhuma alteracao foi feita em API.
- Nenhuma alteracao foi feita em repositories funcionais.
- Nenhuma alteracao foi feita em services.
- Nenhuma migracao foi criada.
- Nenhum teste destrutivo foi executado.

## Proximo passo recomendado

Criar uma reconciliacao somente leitura/documental entre o contrato RTD observado e a estrutura atual do sistema, antes de qualquer mudanca funcional.

