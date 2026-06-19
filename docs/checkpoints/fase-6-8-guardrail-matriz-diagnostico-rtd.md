# Fase 6.8 — Guardrail da matriz de diagnóstico RTD canônica

## Objetivo

Adicionar guardrail automatizado para a transformação canônica usada pela CanonicalPricingFacade, protegendo o comportamento diagnosticado na Fase 6.7.

## Escopo

Foi criado o teste:

- ATT/tests/test_canonical_pricing_facade.py

A fase não altera código de produção. O foco é preservar o comportamento atual da montagem do pricing_payload.

## Guardrails adicionados

O teste cobre:

1. underlying_asset vem explicitamente da estrutura, não da aba legada.
2. snapshot_aba permanece apenas como metadado.
3. Preços em formato brasileiro são normalizados.
4. expiration_date é normalizada para data ISO.
5. side e position_side são inferidos pela quantidade quando ausentes.
6. side ou position_side explícitos têm precedência sobre a inferência.
7. spot_price pode ser resolvido por fallback no banco.
8. spot_price menor ou igual a zero sem fallback válido gera erro e impede execução OK.

## Evidências

Arquivo de evidência:

- docs/checkpoints/evidencias/fase-6-8-pytest-guardrail-matriz-diagnostico-rtd.txt

Resultados registrados:

    python -m pytest ATT/tests/test_canonical_pricing_facade.py -q
    .......                                            [100%]
    7 passed in 0.30s

    python -m pytest ATT/tests/test_pricing_execution_service.py ATT/tests/test_pricing_execution_app_service.py -q
    ...........                                        [100%]
    11 passed in 1.08s

## Observação

A branch também contém o cherry-pick da Fase 6.7:

    4960ca0 docs: consolidate fase 6.7 rtd canonical diagnostics

Isso mantém a Fase 6.8 como continuação direta do diagnóstico RTD canônico.
