# Fase 6.11 - Backup fisico controlado

Marcador inicio: INICIO_AUDITORIA_FASE6_11_BACKUP_FISICO_CONTROLADO_20260713

Data: 13/07/2026

## Natureza

Fase de criacao de backup fisico local antes de qualquer limpeza real.

Esta fase nao executa limpeza e nao altera o banco original.

## Entradas obrigatorias

- Manifesto da Fase 6.10.
- Banco `dados/app.db`.
- SHA256 registrado na Fase 6.10.
- Working tree limpo.
- Branch correta.

## Guardrails

- Validar SHA256 atual do banco contra o manifesto da Fase 6.10.
- Validar integridade SQLite do banco original.
- Criar copia fisica local.
- Validar SHA256 do backup.
- Validar integridade SQLite do backup.
- Nao versionar o arquivo `.db` de backup.
- Nao autorizar limpeza real nesta fase.

## Criterio de aceite

A Fase 6.11 e considerada valida se:

- o banco atual tiver SHA256 igual ao registrado na Fase 6.10;
- o backup fisico for criado;
- o SHA256 do backup for igual ao original;
- o integrity_check do original retornar ok;
- o integrity_check do backup retornar ok;
- o manifesto de backup for gerado;
- o relatorio de backup for gerado;
- os testes automatizados passarem.

## Decisao

A limpeza real permanece bloqueada.

Marcador fim: FIM_AUDITORIA_FASE6_11_BACKUP_FISICO_CONTROLADO_20260713
