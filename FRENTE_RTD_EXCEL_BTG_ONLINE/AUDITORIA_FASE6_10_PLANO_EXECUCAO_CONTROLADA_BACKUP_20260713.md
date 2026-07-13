# Fase 6.10 - Plano de execucao controlada com backup

Marcador inicio: INICIO_AUDITORIA_FASE6_10_PLANO_EXECUCAO_CONTROLADA_BACKUP_20260713

Data: 13/07/2026

## Natureza

Fase nao destrutiva da frente RTD Excel BTG Online.

Esta etapa prepara o plano operacional para uma eventual limpeza real futura, consolidando:

- regra canonica de timezone local;
- lista de IDs elegiveis;
- hash do banco de referencia;
- exigencia de backup obrigatorio;
- bloqueio explicito de limpeza real nesta fase.

## Contexto

A Fase 6.9 simulou a limpeza com sucesso:

- 60/60 linhas elegiveis;
- 0 linhas bloqueadas;
- regra `America/Sao_Paulo` validada;
- nenhuma alteracao no banco.

## Guardrails

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao realizada.
- Nenhuma limpeza real autorizada.
- Backup obrigatorio definido para fase posterior.

## Criterio de aceite

A Fase 6.10 e considerada valida se:

- o script read-only for executado com sucesso;
- o relatorio de plano controlado for gerado;
- o manifesto JSON de IDs elegiveis for gerado;
- o SHA256 do banco for registrado;
- o relatorio declarar backup obrigatorio;
- o relatorio declarar que limpeza real nao esta aprovada;
- o teste automatizado passar.

## Decisao

A limpeza real permanece bloqueada.

A proxima fase, se aprovada explicitamente, devera criar backup fisico antes de qualquer comando destrutivo.

Marcador fim: FIM_AUDITORIA_FASE6_10_PLANO_EXECUCAO_CONTROLADA_BACKUP_20260713
