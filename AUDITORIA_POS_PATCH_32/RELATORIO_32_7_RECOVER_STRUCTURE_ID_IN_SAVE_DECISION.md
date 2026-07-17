# Relatório 32.7 - Recover structure_id in save_decision

Arquivo alterado: services/derived_service.py
Backup: services\derived_service.py.bak_32_7_20260717_201607
Status: patch aplicado
Patch em save_decision_from_canonical_payload: True
Patch em save_decision: True

Motivo:
O patch 32.6 ainda permitiu que structure_id se perdesse dentro de save_decision.

Correção:
Recuperar structure_id diretamente do payload original decision, de decision_dict, de meta e por último via _resolve_structure_id.

Efeito esperado:
structure_decisions deve aumentar após execução OK.
