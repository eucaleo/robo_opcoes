# Fase 2B - Analise da normalizacao numerica

Data: 2026-06-21
Branch: fase-3a4-auto-pricing-manual-save

## Objetivo

Fechar a normalizacao numerica do cadastro manual de estrutura, conforme rota de revisao funcional pos uso real.

## Arquivos investigados

- UI/components/structure_editor_dialog.py
- repositories/structures_repository.py
- services/canonical_pricing_facade.py
- services/structure_leg_rtd_enrichment_service.py
- repositories/market_snapshot_repository.py
- ATT/tests/test_structure_editor_dialog.py
- ATT/tests/test_structures_repository.py

## Evidencias geradas

- docs/checkpoints/evidencias/fase-2b-grep-validacoes-numericas.txt
- docs/checkpoints/evidencias/fase-2b-grep-campos-numericos.txt
- docs/checkpoints/evidencias/fase-2b-gitgrep-normalizacao-existente.txt
- docs/checkpoints/evidencias/fase-2b-pytest-editor-dialog-atual.txt

## Conclusao inicial

O fluxo manual principal passa por UI/components/structure_editor_dialog.py.

Foram encontrados conversores locais:

- _parse_decimal
- _parse_int

A normalizacao ja cobre ou parece cobrir:

- strike com virgula e ponto
- premium com virgula
- multiplier com virgula

Pontos ainda a validar:

- quantity com inteiro string
- quantity com decimal inteiro, exemplo 1,0 e 1.0
- quantity com decimal fracionado, exemplo 1,5
- mensagens de erro para texto invalido
- persistencia final em repositories/structures_repository.py

## Proxima acao

Executar testes focados do editor e, se necessario, adicionar testes para quantity e mensagens de erro antes de alterar codigo.
