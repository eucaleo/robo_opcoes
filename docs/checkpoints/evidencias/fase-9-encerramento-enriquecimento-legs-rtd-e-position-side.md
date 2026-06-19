# Fase 9 — Encerramento: Enriquecimento de Legs por RTD e Ajuste Canônico de position_side

## Status

Encerrada com sucesso.

Data de validação: 2026-06-19

Branch de trabalho:

    fase-6-11-retomada-funcional-pos-restauracao-documental

## Contexto

A Fase 9 foi iniciada para implementar o enriquecimento de pernas de estruturas usando dados persistidos em rtd_option_quotes.

O objetivo funcional era permitir que uma perna fosse informada de forma mínima, usando symbol ou codigo_opcao, e que o sistema enriquecesse automaticamente os campos necessários antes da persistência canônica.

Fluxo esperado:

    symbol / codigo_opcao
        -> rtd_option_quotes
        -> enriquecimento da leg
        -> payload canônico
        -> structures_repository
        -> structure_legs

## Diretrizes respeitadas

Durante a fase foram respeitadas as diretrizes da rota de desenvolvimento:

- não migrar para web;
- não alterar UI sem necessidade;
- não acoplar UI diretamente ao Excel;
- manter o banco como fonte da verdade;
- evitar arquivos legados como fonte operacional principal;
- auditar antes de alterar;
- testar após mudanças relevantes;
- registrar evidências da evolução;
- preservar compatibilidade sempre que possível.

## Diagnóstico inicial

Durante a abertura da fase, foram identificados scripts e testes citados em documentação histórica que não existem no estado atual do repositório.

Arquivos ausentes identificados:

    scripts/audit_rtd_option_quotes.py
    scripts/validate_app_db.py
    ATT/tests/test_canonical_pricing_facade_rtd_db_path.py

Decisão tomada:

    Prosseguir usando apenas arquivos reais do branch atual.

Essa decisão é compatível com a rota, pois quando scripts históricos não existirem mais, deve prevalecer o mapeamento real do branch atual.

## Baseline inicial

Antes da implementação funcional, foi executado baseline corrigido apenas com testes existentes.

Comando executado:

    python -m pytest ATT/tests/test_structures_repository.py ATT/tests/test_structures_api.py ATT/tests/test_structures_legs_endpoints.py ATT/tests/test_structure_editor_dialog.py ATT/tests/test_structure_editor_integration.py ATT/tests/test_structure_input_mapper.py ATT/tests/test_structure_market_input_assembler.py ATT/tests/test_pricing_input_service.py ATT/tests/test_canonical_input_service.py -q

Resultado:

    185 passed in 16.23s

## Implementação principal da Fase 9

Foi criado o service:

    services/structure_leg_rtd_enrichment_service.py

Responsabilidade:

    Receber uma leg mínima baseada em symbol ou codigo_opcao,
    consultar rtd_option_quotes,
    e devolver uma leg enriquecida e canônica para persistência.

Foi criado o teste correspondente:

    ATT/tests/test_structure_leg_rtd_enrichment_service.py

O ciclo test-first foi respeitado:

1. teste vermelho por ausência do service;
2. criação do service;
3. teste verde.

Comando executado:

    python -m pytest ATT/tests/test_structure_leg_rtd_enrichment_service.py -q

Resultado:

    5 passed

## Derivação controlada: ajuste do contrato position_side

Durante a Fase 9, foi identificada pelo usuário uma inconsistência de domínio relevante.

O sistema vinha usando como contrato canônico:

    LONG / SHORT

Essa nomenclatura foi considerada inadequada para o uso operacional do sistema em português brasileiro.

A observação foi feita pelo usuário Carlos, que indicou que a nomenclatura correta para o domínio do sistema deveria ser:

    COMPRADO / VENDIDO

Ou, como aliases de entrada:

    C / V

Essa derivação foi aceita como necessária porque position_side é parte central do contrato de negócio de estruturas e pernas.

Manter LONG / SHORT como saída canônica causaria confusão para o usuário final e para a semântica do sistema.

## Decisão de contrato

Contrato canônico de negócio, API e persistência:

    COMPRADO
    VENDIDO

Aliases aceitos na entrada:

    C        -> COMPRADO
    COMPRA   -> COMPRADO
    COMPRADO -> COMPRADO
    LONG     -> COMPRADO

    V        -> VENDIDO
    VENDA    -> VENDIDO
    VENDIDO  -> VENDIDO
    SHORT    -> VENDIDO

Decisão sobre BUY e SELL:

    BUY e SELL não devem ser aceitos no contrato principal da API nova.

Motivo:

    Evitar mistura desnecessária entre português e inglês no contrato principal do sistema.

Caso algum fluxo legado precise lidar com BUY ou SELL, isso deve permanecer isolado em adaptadores ou importadores legados.

## Arquivos criados ou alterados

Arquivo criado:

    domain/position_side.py

Responsabilidade:

    Normalizar o lado da posição para o contrato canônico COMPRADO/VENDIDO.

Funções principais:

    normalize_position_side
    to_pricing_engine_side

Arquivo alterado:

    api/structures_controller.py

Alterações principais:

- LegRequest.position_side deixou de validar apenas LONG ou SHORT;
- passou a aceitar string;
- passou a normalizar via normalize_position_side;
- aliases de entrada são aceitos;
- a saída para o repository passa a ser canônica.

Arquivo alterado:

    repositories/structures_repository.py

Alterações principais:

- VALID_POSITION_SIDES passou a usar CANONICAL_POSITION_SIDES;
- _validate_leg passou a normalizar position_side;
- entradas C, V, LONG e SHORT continuam compatíveis;
- persistência passa a usar COMPRADO e VENDIDO;
- leg_order foi mantido aceitando zero, conforme contrato validado nos endpoints.

Arquivo alterado:

    services/structure_leg_rtd_enrichment_service.py

Alteração principal:

- enrichment passou a normalizar position_side usando o normalizador central;
- entrada com alias retorna saída canônica.

Testes alterados:

    ATT/tests/test_structure_leg_rtd_enrichment_service.py
    ATT/tests/test_structures_legs_endpoints.py
    ATT/tests/test_structures_api.py
    ATT/tests/test_structures_repository.py
    ATT/tests/test_legacy_structure_legs_importer_integration.py

Os testes foram ajustados para não esperar mais LONG / SHORT como saída canônica em structures.

## Validações executadas

Validação da API de structures e endpoints de legs:

    python -m pytest ATT/tests/test_structures_legs_endpoints.py ATT/tests/test_structures_api.py -q

Resultado:

    94 passed

Validação do enrichment RTD:

    python -m pytest ATT/tests/test_structure_leg_rtd_enrichment_service.py -q

Resultado:

    5 passed

Validação combinada de API, legs e enrichment:

    python -m pytest ATT/tests/test_structures_legs_endpoints.py ATT/tests/test_structures_api.py ATT/tests/test_structure_leg_rtd_enrichment_service.py -q

Resultado:

    99 passed

Validação do repository e importador legado:

    python -m pytest ATT/tests/test_legacy_structure_legs_importer_integration.py ATT/tests/test_structures_repository.py -q

Resultado:

    26 passed

Validação final completa:

    pytest

Resultado:

    580 passed, 10 skipped in 35.71s

## Resultado final da fase

A Fase 9 entregou:

- service de enriquecimento de legs por RTD;
- uso de symbol e codigo_opcao para buscar dados em rtd_option_quotes;
- preenchimento automático de option_type, strike, expiration_date e underlying_asset;
- normalização central de position_side;
- contrato canônico brasileiro para estruturas;
- compatibilidade de entrada com aliases antigos;
- testes focados passando;
- suíte completa passando.

## Observação sobre cálculo interno

Alguns serviços de cálculo e pricing ainda podem usar LONG / SHORT como convenção técnica interna.

Isso não invalida o novo contrato de negócio.

Decisão:

    Camada de negócio, API e persistência:
        COMPRADO / VENDIDO

    Bordas técnicas de cálculo, quando necessário:
        COMPRADO -> LONG
        VENDIDO  -> SHORT

A conversão deve ser feita por to_pricing_engine_side.

## Pendências conhecidas

- Revisar futuramente os testes marcados como skipped.
- Auditar serviços de cálculo que ainda dependem de LONG / SHORT.
- Garantir que integrações futuras com pricing convertam explicitamente COMPRADO / VENDIDO para a convenção técnica esperada.
- Documentar o contrato canônico de position_side em documentação de contratos do domínio ou API, se ainda não existir.

## Decisão de encerramento

A Fase 9 pode ser considerada encerrada.

A derivação sobre LONG / SHORT foi causada por decisão do usuário, por necessidade de adequação do sistema ao domínio operacional brasileiro.

Essa derivação foi controlada, testada e incorporada como melhoria de contrato de negócio, sem quebrar a suíte de testes.

Resultado final:

    580 passed, 10 skipped

