# Auditoria RTD - Nova UI - BOVAK900

## Contexto

A nova UI passou a oferecer acao de preenchimento de perna por simbolo RTD.

O ticker testado foi BOVAK900.

Premissas funcionais:

    - BOVAK900 e ticker valido de opcao B3.
    - O ativo-base correspondente e BOVA11.
    - A fonte de verdade persistida deve ser banco SQLite.
    - O Excel/RTD atua apenas como ponte dinamica.
    - dados/app.db e banco persistente.
    - dados/derived.db e banco volatil/derivado.

## Evidencias

A auditoria local confirmou:

    - rtd_option_quotes existe em dados/app.db.
    - rtd_option_quotes existe em dados/derived.db.
    - Ha registros RTD oriundos de BTG_RTD_EXCEL.
    - Existem opcoes de BOVA11 persistidas, como:
        - BOVAG34
        - BOVAH186
        - BOVAS61
        - BOVAT158
    - Nao ha registro direto para BOVAK900 em nenhum banco auditado.
    - A nova UI chama StructureLegRtdEnrichmentService.
    - O servico consulta RtdOptionQuotesRepository.
    - O repository apenas le rtd_option_quotes.
    - Nao foi identificado pipeline produtivo versionado ativo de refresh/import RTD option quotes.
    - Scripts historicos como import_rtd_links_to_option_quotes.py, run_rtd_refresh_full.py e similares aparecem em evidencias/documentacao, mas nao como fluxo ativo atual.

## Causa raiz

A nova UI consulta o cache rtd_option_quotes, mas nao aciona antes a ponte RTD/Excel para hidratar o ticker solicitado.

Fluxo atual observado:

    UI
        -> enrich(symbol)
            -> SELECT em rtd_option_quotes
                WHERE codigo_opcao = symbol

Fluxo necessario:

    UI
        -> solicitar ou hidratar ticker na ponte RTD/Excel
        -> persistir ou atualizar rtd_option_quotes
        -> ler rtd_option_quotes
        -> preencher perna

## Diagnostico

O erro observado:

    option quote not found for symbol: BOVAK900

nao significa ticker invalido.

Significa que BOVAK900 ainda nao foi persistido no banco consultado e a nova UI nao chamou a rotina que deveria buscar o ticker no RTD/Excel e gravar no banco.

## Inconsistencia adicional

dados/app.db possui registros RTD mais recentes do que dados/derived.db.

Isso conflita com a premissa de que dados volateis/RTD deveriam viver em derived.db.

E necessario definir e corrigir o alvo unico de escrita/leitura de cotacoes RTD.

## Correcao necessaria

1. Separar claramente:

    - app_db_path para estruturas persistentes.
    - derived_db_path para cotacoes RTD volateis.

2. No botao [RTD] Preencher por Simbolo, executar:

    - refresh ou hidratacao RTD do simbolo.
    - depois enriquecimento via repository.

3. Restaurar ou recriar um servico produtivo de refresh/import RTD option quotes.

4. Garantir teste automatizado cobrindo:

    - clicar preencher RTD.
    - chamar refresh_symbol("BOVAK900").
    - depois chamar enrich(...).

5. Garantir que a leitura de rtd_option_quotes use o banco definido como fonte volatil oficial.

## Estado

Pendente de correcao funcional.
