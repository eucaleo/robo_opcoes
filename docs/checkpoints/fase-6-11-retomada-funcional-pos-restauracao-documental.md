# Fase 6.11 — Retomada funcional pós-restauração documental

## Status

Em andamento.

## Objetivo

Retomar o desenvolvimento funcional de forma controlada após a restauração documental da ROTA_MESTRE_3.

A fase parte da main já sincronizada com as Fases 6.7, 6.8, 6.9 e 6.10.

## Base

    ed7825c docs: sincroniza rota mestre 3 apos fases 6.7 a 6.9
    fase-6-10-restauracao-documental-rota-mestre-3

## Branch

    fase-6-11-retomada-funcional-pos-restauracao-documental

## Escopo permitido

    RTD
    canonical pricing
    pricing execution
    diagnóstico funcional
    testes automatizados
    documentação de checkpoint

## Escopo proibido

    alteração de UI/API
    alteração de banco
    migração
    limpeza destrutiva
    refatoração ampla sem teste
    mudança funcional sem evidência

## Baseline inicial

Testes executados:

    python -m pytest ATT/tests/test_canonical_pricing_facade.py -q
    python -m pytest ATT/tests/test_pricing_execution_service.py ATT/tests/test_pricing_execution_app_service.py -q

Evidências:

    docs/checkpoints/evidencias/fase-6-11-pytest-canonical-pricing-facade-baseline.txt
    docs/checkpoints/evidencias/fase-6-11-pytest-pricing-execution-baseline.txt
    docs/checkpoints/evidencias/fase-6-11-inventario-testes-rtd-option-canonical.txt

## Observação sobre filtro inicial

O filtro rtd_option_quotes não selecionou testes no baseline inicial.

Resultado observado:

    585 deselected

Portanto, a fase deve primeiro inventariar os nomes reais de testes e caminhos relacionados a RTD, options, quotes, canonical pricing e pricing execution antes de executar nova alteração funcional.

## Próxima microfatia candidata

Identificar o menor ponto funcional ainda descoberto no caminho RTD/canonical pricing e protegê-lo com teste automatizado antes de qualquer expansão de escopo.

