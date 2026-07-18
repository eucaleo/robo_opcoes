# Resultado Backend Sem UI 34

Gerado em: `2026-07-17T21:25:29`
Projeto: `C:\users\eucal\projeto`
Banco: `C:\users\eucal\projeto\dados\app.db`
Backup: `C:\users\eucal\projeto\dados\app.backup_backend_sem_ui_34_20260717_212529.db`

Status geral: `error`

## Estrutura usada

- `structure_id`: `2`

## Contagens antes

- `pricing_executions`: `149`
- `structure_snapshots`: `179`
- `payoff_curve_points`: `3535`
- `structure_decisions`: `16`

## Contagens depois


## Deltas


## Último payoff da estrutura


## Retorno do PayoffRefreshCommandService

```json
null
```

## Erro, se houver

```text
Traceback (most recent call last):
  File "C:\users\eucal\projeto\FRENTE_RTD_EXCEL_BTG_ONLINE\AUDITORIA_CENTRO_VERDADE_34\validar_backend_sem_ui_34.py", line 436, in main
    service = instantiate_command_service()
  File "C:\users\eucal\projeto\FRENTE_RTD_EXCEL_BTG_ONLINE\AUDITORIA_CENTRO_VERDADE_34\validar_backend_sem_ui_34.py", line 223, in instantiate_command_service
    from services.payoff_refresh_command_service import PayoffRefreshCommandService
ModuleNotFoundError: No module named 'services'

```
