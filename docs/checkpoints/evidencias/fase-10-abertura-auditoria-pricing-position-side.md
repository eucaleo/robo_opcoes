# Fase 10 — Abertura: Auditoria de Pricing e Conversão Técnica de position_side

## Status

Aberta.

## Contexto

A Fase 9 consolidou o contrato canônico de negócio, API e persistência para position_side como:

    COMPRADO
    VENDIDO

Também foi criado o conversor técnico para bordas internas de cálculo que ainda usam:

    LONG
    SHORT

## Objetivo

Auditar os serviços de cálculo, pricing e montagem de payloads para garantir que:

- COMPRADO / VENDIDO permaneçam como contrato de negócio;
- LONG / SHORT fiquem restritos a bordas técnicas;
- toda conversão seja explícita;
- o conversor canônico seja usado nas integrações com pricing;
- a suíte permaneça verde.

## Plano inicial

1. Localizar usos de LONG e SHORT no código.
2. Classificar usos legítimos e usos indevidos.
3. Verificar payloads enviados ao pricing.
4. Adicionar testes de proteção se necessário.
5. Executar suíte completa.
