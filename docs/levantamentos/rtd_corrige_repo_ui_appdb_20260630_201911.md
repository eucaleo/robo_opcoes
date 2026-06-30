# Correção RTD operacional para app.db

Gerado em: 2026-06-30 20:19:11

## Objetivo

Remover uso operacional de `dados/derived.db` para leitura/gravação de cache RTD vivo.

## Alterações

### repositories/rtd_option_quotes_repository.py

- `- dados/derived.db: cache RTD e dados derivados` -> `- dados/app.db: cache RTD operacional`: `1` ocorrência(s)
- `def __init__(self, db_path: str | Path = "dados/derived.db") -> None:` -> `def __init__(self, db_path: str | Path = "dados/app.db") -> None:`: `1` ocorrência(s)

### UI/components/structure_editor_dialog.py

- `"""Atualiza uma opcao via RTD/Excel e grava o cache em dados/derived.db."""` -> `"""Atualiza uma opcao via RTD/Excel e grava o cache em dados/app.db."""`: `1` ocorrência(s)
- `db_path = project_root / "dados" / "derived.db"` -> `db_path = project_root / "dados" / "app.db"`: `2` ocorrência(s)
- WARN: padrão não encontrado: `rtd_db_path = project_root / "dados" / "derived.db"`

## Conclusão

RTD operacional passa a apontar para `dados/app.db` nos pontos corrigidos.
Não houve alteração de schema, tabelas ou dados.
