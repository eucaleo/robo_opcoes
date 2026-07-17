# Relatório 32.8 - Correção de caminhos de retorno em derived_service.py

- Arquivo alterado: `services/derived_service.py`
- Backup: `C:\users\eucal\projeto\services\derived_service.py.bak_32_8_20260717_202357`
- Status: correção aplicada

## Motivo

Após os patches 32.6/32.7, os blocos finais de persistência ficaram condicionados a:

```python
if enriched_decision.get("structure_id") is not None:
```

Isso poderia fazer `save_decision()` ou `save_decision_from_canonical_payload()` retornarem `None`
silenciosamente caso o `structure_id` não fosse resolvido.

## Correção

- Mantida a recuperação/normalização de `structure_id`.
- Mantido o espelhamento de `structure_id` em `meta`.
- O bloco `with connect_app()` voltou a executar fora do `if`.
- O `return save_decision(...)` voltou a executar fora do `if`.

## Alterações automáticas

- Bloco `with connect_app()` dedentado: `True`
- Bloco `return save_decision(...)` dedentado: `True`

## Validação

`py_compile` executado com sucesso para `services/derived_service.py`.

## Efeito esperado

A função continua tentando recuperar `structure_id`, mas não perde o caminho final de persistência/delegação.
