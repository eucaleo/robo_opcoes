# Fase 6.10 - Plano de execucao controlada com backup

Marcador inicio: INICIO_FASE6_10_PLANO_EXECUCAO_CONTROLADA_BACKUP_20260713

Data de geracao: 2026-07-13T16:33:51+00:00

## Natureza

Plano operacional nao destrutivo, somente leitura, sem remocao de registros.

## Banco de referencia

- Caminho: `dados/app.db`
- Tamanho em bytes: 1548288
- SHA256: `2ee46208d4e61574f93c5548c2e081c4f5d6ce052e98b40cfab8f8d046b2f026`

## Regra canonica consolidada

```text
Timezone local operacional: America/Sao_Paulo
captured_at com timezone -> converter para America/Sao_Paulo
captured_at sem timezone -> assumir America/Sao_Paulo
bucket_start -> horario local operacional
elegibilidade -> mesmo simbolo e mesmo bucket local
```

## Volumetria planejada

- Linhas no historico bruto: 60
- Linhas em candles: 110
- Intervalo primario avaliado: 1 minutos
- IDs elegiveis no plano: 60/60
- IDs bloqueados no plano: 0
- Percentual elegivel: 100.0000

## Distribuicao por motivo

| Motivo | Quantidade |
|---|---:|
| `ELEGIVEL_BACKUP_OBRIGATORIO` | 60 |

## Manifesto

- Arquivo: `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_manifesto_ids_elegiveis_20260713.json`
- IDs elegiveis: `11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70`
- IDs bloqueados: ``

## Plano obrigatorio antes de qualquer limpeza real

1. Confirmar branch correta.
2. Confirmar working tree limpo.
3. Parar qualquer processo que escreva no banco.
4. Criar backup fisico do arquivo `dados/app.db`.
5. Calcular SHA256 do backup.
6. Comparar SHA256 do banco original com o registrado neste plano.
7. Executar validacao read-only imediatamente antes da limpeza.
8. Executar limpeza real somente em fase posterior explicitamente aprovada.
9. Validar contagens apos a limpeza.
10. Manter backup ate fechamento da auditoria.

## Resultado

- Status: PLANO_CONTROLADO_GERADO_COM_BACKUP_OBRIGATORIO
- IDs elegiveis no plano: 60/60
- IDs bloqueados no plano: 0
- Backup obrigatorio antes da limpeza real: sim
- Aprovado para limpeza real: nao
- Registros removidos: 0
- Banco alterado: nao

## Decisao

Esta fase nao executa limpeza real.

A limpeza real permanece bloqueada ate uma fase posterior com confirmacao explicita.

Marcador fim: FIM_FASE6_10_PLANO_EXECUCAO_CONTROLADA_BACKUP_20260713
