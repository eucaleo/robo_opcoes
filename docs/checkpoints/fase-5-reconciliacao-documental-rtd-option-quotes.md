# Fase 5 - Reconciliação documental RTD_OPTION_QUOTES vs sistema

## Escopo

Reconciliação somente leitura entre o contrato RTD observado no Excel LISTA_RTD.xlsm, aba RTD_OPTION_QUOTES, e a estrutura atual do sistema para a tabela rtd_option_quotes.

Esta fase não altera comportamento funcional.

## Garantias desta fase

- Evidência somente leitura.
- Nenhuma alteração funcional realizada.
- Nenhum Excel alterado.
- Nenhum banco alterado.
- Nenhuma migração criada.
- Nenhuma alteração em UI, API, repositories ou services.
- Objetivo: permitir reconciliação campo a campo entre o contrato Excel e a tabela rtd_option_quotes.

## Estado Git observado

- Branch: fase-12-fechamento-ciclo
- Base inicial da reconciliação: 5488d5f
- Modo: documental / somente leitura

## Evidências geradas

- docs/checkpoints/evidencias/fase-5-reconciliacao-inicial-rtd-sistema.txt
- docs/checkpoints/evidencias/fase-5-reconciliacao-focada-rtd-option-quotes-sistema.txt

## Arquivos funcionais relevantes identificados

- infra/bootstrap_rtd_option_quotes_schema.py
- repositories/rtd_option_quotes_repository.py
- scripts/import_lista_rtd_excel_to_option_quotes.py
- scripts/run_lista_rtd_option_quotes_pipeline.py
- scripts/import_rtd_links_to_option_quotes.py
- scripts/run_rtd_option_quotes_pipeline.py
- services/canonical_pricing_facade.py

## Contrato Excel observado

A aba RTD_OPTION_QUOTES usa o provider RTD:

- btg_pro_rtd

Formato observado:

- Coluna A: código/símbolo da opção.
- Colunas B:O: fórmulas RTD.
- Total: 14 campos RTD por linha.

Tópicos RTD observados:

- QUOTE.UNDERLYING_SYMBOL
- QUOTE.OPTION_TYPE
- QUOTE.STRIKE_PRICE
- QUOTE.MATURITYDATE
- QUOTE.LAST_TRADE_PRICE
- QUOTE.LAST_TRADE_QUANTITY
- QUOTE.BID_PRICE
- QUOTE.ASK_PRICE
- QUOTE.VOLUME
- QUOTE.IMPLIED_VOLATILITY
- QUOTE.DELTA
- QUOTE.GAMMA
- QUOTE.THETA
- QUOTE.VEGA

## Schema atual da tabela rtd_option_quotes

O schema declarado em infra/bootstrap_rtd_option_quotes_schema.py contém:

- id
- codigo_opcao
- ativo_base
- call_put
- strike
- vencimento
- ultimo_preco
- ultima_quantidade
- bid
- ask
- volume
- iv
- delta
- gamma
- theta
- vega
- source
- raw_json
- updated_at
- created_at

A tabela possui unicidade por:

- UNIQUE(codigo_opcao)

## Matriz de reconciliação campo a campo

| Origem Excel / RTD | Coluna sistema | Uso observado | Status |
|---|---|---|---|
| Coluna A / código da opção | codigo_opcao | Chave lógica da cotação; usada pelo repository e pelo pricing para localizar a opção | Reconciliado |
| QUOTE.UNDERLYING_SYMBOL | ativo_base | Identificação do ativo base; usada para listagens por ativo | Reconciliado |
| QUOTE.OPTION_TYPE | call_put | Tipo da opção; usado em ordenação/listagem e metadados | Reconciliado |
| QUOTE.STRIKE_PRICE | strike | Strike da opção; usado em metadados/listagem | Reconciliado |
| QUOTE.MATURITYDATE | vencimento | Vencimento da opção; usado em metadados/listagem | Reconciliado |
| QUOTE.LAST_TRADE_PRICE | ultimo_preco | Principal preço RTD usado pelo fluxo de pricing quando disponível | Reconciliado |
| QUOTE.LAST_TRADE_QUANTITY | ultima_quantidade | Quantidade do último negócio; preservada como dado de cotação | Reconciliado |
| QUOTE.BID_PRICE | bid | Melhor compra; preservada como dado de cotação e disponível ao sistema | Reconciliado |
| QUOTE.ASK_PRICE | ask | Melhor venda; preservada como dado de cotação e disponível ao sistema | Reconciliado |
| QUOTE.VOLUME | volume | Volume; preservado como dado de cotação | Reconciliado |
| QUOTE.IMPLIED_VOLATILITY | iv | Volatilidade implícita; preservada como dado de cotação | Reconciliado |
| QUOTE.DELTA | delta | Grega delta; preservada como dado de cotação | Reconciliado |
| QUOTE.GAMMA | gamma | Grega gamma; preservada como dado de cotação | Reconciliado |
| QUOTE.THETA | theta | Grega theta; preservada como dado de cotação | Reconciliado |
| QUOTE.VEGA | vega | Grega vega; preservada como dado de cotação | Reconciliado |

## Campos sistêmicos sem origem direta no Excel RTD

| Campo | Finalidade | Status |
|---|---|---|
| id | Chave técnica/autoincremento | Sistêmico |
| source | Origem da importação/cotação | Sistêmico |
| raw_json | Preservação de payload bruto/metadados | Sistêmico |
| updated_at | Controle de atualização | Sistêmico |
| created_at | Controle de criação | Sistêmico |

## Fluxo funcional reconciliado

Fluxo atual identificado:

- LISTA_RTD.xlsm
- aba RTD_OPTION_QUOTES
- scripts/import_lista_rtd_excel_to_option_quotes.py
- rtd_option_quotes
- repositories/rtd_option_quotes_repository.py
- services/canonical_pricing_facade.py
- pricing_payload / pricing_executions

Fluxo legado/alternativo identificado:

- RTD_LINKS.csv
- scripts/import_rtd_links_to_option_quotes.py
- rtd_option_quotes
- audit/pipeline

## Observações relevantes

- A tabela rtd_option_quotes funciona como staging/cache operacional das cotações RTD de opções.
- O repository RtdOptionQuotesRepository é de leitura.
- O bootstrap cria/valida schema vazio, sem inserir dados fictícios.
- O CanonicalPricingFacade resolve o banco efetivo da tabela rtd_option_quotes.
- Há histórico documental e funcional do fluxo antigo baseado em RTD_LINKS.csv.
- O fluxo novo baseado em LISTA_RTD.xlsm está representado pelos scripts import_lista_rtd_excel_to_option_quotes.py e run_lista_rtd_option_quotes_pipeline.py.

## Pontos de atenção para fases futuras

1. Atualizar documentação textual que ainda descreve rtd_option_quotes apenas como tabela alimentada por CSV, pois o fluxo Excel LISTA_RTD.xlsm agora também é fonte operacional.
2. Preservar compatibilidade do schema atual antes de qualquer alteração funcional.
3. Validar, em fase posterior, se source deve diferenciar claramente:
   - rtd_links
   - lista_rtd_excel
   - outros provedores/fontes futuras
4. Confirmar em fase posterior se bid, ask, iv e gregas serão apenas dados rastreáveis ou também insumos diretos de pricing.
5. Não alterar banco, Excel, UI, API ou motor de cálculo sem fase específica de implementação.

## Conclusão

A reconciliação documental inicial indica que o contrato RTD observado na aba RTD_OPTION_QUOTES está compatível com o schema atual de rtd_option_quotes.

Todos os 14 tópicos RTD observados possuem coluna correspondente na tabela.

A ponte documental Excel RTD -> tabela -> repository -> pricing está mapeada e pronta para orientar fases posteriores, sem alteração funcional nesta fase.
