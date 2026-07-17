# Relatório 32.8.1 - Ajuste cosmético de indentação em derived_service.py

- Arquivo alterado: services/derived_service.py
- Status: indentação visual normalizada

Motivo:
Após o patch 32.8, o código compilava e o backend persistia corretamente, mas o diff exibia indentação visual irregular em blocos de retorno.

Correção:
Normalizada a indentação do bloco `with connect_app()` em `save_decision` e dos argumentos de `save_decision(...)` em `save_decision_from_canonical_payload`.

Efeito esperado:
Sem mudança funcional. Apenas melhora de legibilidade/manutenção.
