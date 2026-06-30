# Correção de caminho app.db

Gerado em: 2026-06-30 20:07:51

## Objetivo

Padronizar caminhos legados `data/app.db` para o caminho oficial `dados/app.db`.

## Arquivos processados

### db/sqlite.py

- Backup: `backups/rtd_corrige_path_appdb_20260630_200751/sqlite.py`
- Alterações:
  - `Path("data") / "app.db"` -> `Path("dados") / "app.db"`: `1` ocorrência(s)

### validate_db.py

- Backup: `backups/rtd_corrige_path_appdb_20260630_200751/validate_db.py`
- Alterações:
  - `"data/app.db"` -> `"dados/app.db"`: `1` ocorrência(s)

## Validação sintática

- OK: arquivos Python compilados com sucesso.

## Validação do banco oficial

- `dados/app.db` existe: `True`
- `rtd_option_quotes`: `11`
- `rtd_underlying_quotes`: `2`

## Busca residual

- OK: nenhuma referência residual a `data/app.db` nos arquivos processados.

## Conclusão

Correção limitada ao caminho do banco operacional. Não houve alteração em schema, tabelas ou dados.
