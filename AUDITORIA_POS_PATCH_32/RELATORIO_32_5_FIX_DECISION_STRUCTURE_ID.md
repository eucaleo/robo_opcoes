# Relatorio 32.5 - Fix decision structure_id

- Arquivo alterado: services\derived_payoff_persistence.py
- Backup: services\derived_payoff_persistence.py.bak_32_5_20260717_200712
- Status: patch aplicado
- Correcao: garantir decision_dict structure_id antes de salvar structure_decisions

Motivo:
O payoff passou a ser salvo apos o patch 32.4, mas a decisao falhou com NOT NULL constraint failed em structure_decisions.structure_id.

Efeito esperado:
A chamada save_decision_from_canonical_payload passa a receber decision_dict com structure_id preenchido.
