# Fase 8C — Conclusão da origem da verdade das legs atuais

## Objetivo

Formalizar a conclusão da auditoria sobre a origem da verdade das legs atuais antes de qualquer integração funcional entre rtd_option_quotes, snapshots de mercado, serviços e cálculo.

## Evidência base

Arquivo de diagnóstico:

- docs/checkpoints/fase-8c-diagnostico-origem-verdade-legs.txt

Commit do diagnóstico:

- 589cb3f docs: registra diagnostico origem verdade legs fase 8c

## Bancos auditados

- dados/app.db
- dados/derived.db

## Resultado em dados/app.db

Tabelas relevantes encontradas:

- structure_legs
- rtd_analise_robo_legs
- rtd_option_quotes
- structures

Tabelas candidatas inexistentes:

- analise_robo_legs
- robo_legs

## Resultado em dados/derived.db

Nenhuma tabela candidata relevante foi encontrada para reconciliar legs com cotações RTD.

Foi identificada apenas a tabela structure_decisions, sem aplicação direta nesta reconciliação.

## Comparação entre fontes

Total de códigos detectados:

- structure_legs: 20 códigos
- rtd_analise_robo_legs: 20 códigos
- rtd_option_quotes: 8 códigos

Colunas usadas:

- structure_legs: symbol
- rtd_analise_robo_legs: ativo
- rtd_option_quotes: codigo_opcao

## Resultado da reconciliação

Comparação entre structure_legs e rtd_option_quotes:

- matches exatos: 0

Comparação entre rtd_analise_robo_legs e rtd_option_quotes:

- matches exatos: 0

## Interpretação

structure_legs e rtd_analise_robo_legs representam o mesmo conjunto operacional antigo de legs.

rtd_option_quotes representa outro conjunto de opções, importado da fonte lista_rtd_excel.

Não há correspondência direta por código de opção entre as legs canônicas atuais e as cotações persistidas em rtd_option_quotes.

## Decisão

rtd_option_quotes não deve ser integrada diretamente ao fluxo de snapshot, cálculo ou UI como fonte de mercado das estruturas atuais enquanto não existir reconciliação canônica com structure_legs.

A integração direta neste momento criaria risco de associar cotações atuais a estruturas ou pernas antigas/incorretas.

## Classificação das fontes

structure_legs:

- fonte canônica atual das pernas do sistema
- desatualizada frente aos códigos atuais em rtd_option_quotes

rtd_analise_robo_legs:

- fonte legada/espelho de análise de legs
- alinhada ao conjunto antigo de structure_legs
- não alinhada aos códigos atuais de rtd_option_quotes

rtd_option_quotes:

- fonte persistida de cotações RTD de opções
- contém cotações atuais
- não possui vínculo de estrutura/perna

## Bloqueio funcional

Ficam bloqueadas nesta etapa:

- integração direta de rtd_option_quotes no snapshot de estruturas
- integração direta de rtd_option_quotes no cálculo de estruturas
- exposição na UI como dado operacional de estrutura
- substituição automática de cotações de legs sem vínculo canônico

## Próxima etapa recomendada

Abrir a próxima etapa como:

Fase 8D — Definição do ponto seguro de integração RTD sem acoplar cotações a legs incorretas.

Objetivos da Fase 8D:

1. Identificar onde o sistema resolve cotações por ticker.
2. Definir adapter somente-leitura para rtd_option_quotes.
3. Garantir que o adapter só retorne cotação quando o ticker da leg existir em structure_legs.
4. Criar teste comprovando que códigos não vinculados não entram no cálculo.
5. Manter UI e cálculo sem alteração visual nesta etapa.

## Arquivos funcionais alterados nesta fase

Nenhum.

## Resultado

Fase 8C concluída como diagnóstico e decisão documental.

## Status

Concluída.
