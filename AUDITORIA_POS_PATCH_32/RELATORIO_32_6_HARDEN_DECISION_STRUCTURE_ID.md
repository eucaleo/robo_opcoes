# Relatório 32.6 - Harden decision structure_id

- Arquivo alterado: services/derived_service.py
- Backup: services\derived_service.py.bak_32_6_20260717_201327
- Status: patch aplicado
- Patch em save_decision_from_canonical_payload: True
- Patch em save_decision: True

Motivo:
O patch 32.5 garantiu structure_id em DerivedPayoffPersistence, mas a decisão ainda chegou ao insert final sem structure_id no topo de decision_dict.

Erro observado:
sqlite3.IntegrityError: NOT NULL constraint failed: structure_decisions.structure_id

Correção:
Adicionar barreiras em services/derived_service.py para garantir structure_id no topo de enriched_decision antes de chamar save_decision e antes do insert final em structure_decisions.

Efeito esperado:
structure_decisions deve aumentar após execução OK, junto com payoff_curve_points.
