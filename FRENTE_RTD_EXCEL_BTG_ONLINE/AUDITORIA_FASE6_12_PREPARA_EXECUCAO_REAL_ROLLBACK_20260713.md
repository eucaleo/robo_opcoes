# Fase 6.12 - Preparacao da execucao real controlada com rollback

Marcador inicio: INICIO_AUDITORIA_FASE6_12_PREPARA_EXECUCAO_REAL_ROLLBACK_20260713

Data: 13/07/2026

## Natureza

Fase de preparacao read-only da execucao real controlada de limpeza.

Esta fase nao executa limpeza real, nao remove registros e nao altera o banco original.

## Entradas obrigatorias

- Manifesto da Fase 6.10.
- Relatorio da Fase 6.10.
- Manifesto da Fase 6.11.
- Backup fisico validado da Fase 6.11.
- Banco canonico `dados/app.db`.
- Branch correta.
- Working tree limpo.

## Validacoes obrigatorias

- Conferir SHA256 atual do banco contra a Fase 6.10.
- Conferir SHA256 atual do banco contra a Fase 6.11.
- Conferir SQLite integrity_check do banco atual.
- Conferir existencia do backup fisico.
- Conferir SHA256 do backup fisico.
- Conferir SQLite integrity_check do backup fisico.
- Conferir lista de IDs elegiveis.
- Conferir que os 60 IDs elegiveis permanecem presentes.
- Conferir que 0 IDs estao bloqueados.
- Documentar rollback.
- Manter limpeza real bloqueada.

## Rollback documentado

Em caso de necessidade apos fase posterior:

1. Parar qualquer processo que escreva no banco.
2. Preservar copia do banco pos-execucao para auditoria, se necessario.
3. Restaurar `dados/app.db` a partir do backup fisico validado da Fase 6.11.
4. Calcular SHA256 do banco restaurado.
5. Comparar SHA256 restaurado contra o backup validado.
6. Executar SQLite integrity_check.
7. Registrar resultado em auditoria.

## Criterio de aceite

A Fase 6.12 e considerada valida se:

- pre-flight for gerado;
- backup fisico estiver validado;
- rollback estiver documentado;
- IDs elegiveis forem confirmados;
- banco permanecer inalterado;
- registros removidos forem 0;
- limpeza real permanecer nao aprovada;
- testes automatizados passarem;
- auditoria for atualizada;
- commit for realizado.

## Decisao

A Fase 6.12 prepara a Fase 6.13, mas nao autoriza execucao real.

Marcador fim: FIM_AUDITORIA_FASE6_12_PREPARA_EXECUCAO_REAL_ROLLBACK_20260713
