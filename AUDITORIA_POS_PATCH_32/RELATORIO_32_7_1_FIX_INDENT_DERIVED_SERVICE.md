# Relatório 32.7.1 - Correção de indentação em derived_service.py

- Arquivo alterado: services/derived_service.py
- Backup: services\derived_service.py.bak_32_7_1_20260717_201758
- Status: indentação corrigida

Motivo:
O patch 32.7 deixou o corpo do bloco with connect_app() sem indentação interna, causando IndentationError.

Correção:
As chamadas ensure_derived_tables(conn) e insert_structure_decision foram recuadas para dentro do bloco with.

Efeito esperado:
services/derived_service.py deve compilar novamente e o teste backend pode prosseguir.
