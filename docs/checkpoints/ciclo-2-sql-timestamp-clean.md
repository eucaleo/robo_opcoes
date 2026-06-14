# Checkpoint: ciclo-2-sql-timestamp-clean

## Objetivo

Encerrar a limpeza de consultas SQL sensíveis a timestamp textual no SQLite e remover padrões SQL genéricos/inseguros em repositórios críticos.

## Validações

- Suite completa ATT:
  - 564 passed
  - 10 skipped

- Grep de padrões eliminados:
  - SELECT estrela
  - ordenação SQL direta por timestamp textual
  - agregação SQL direta sobre timestamp textual

## Tag

ciclo-2-sql-timestamp-clean

## Branch

ciclo-2-testes-evolucao

## HEAD

14483c2 chore: remove literais sql inseguros de comentarios

---

## Reconciliação das fases técnicas do subciclo SQL/timestamp clean

Esta seção reconcilia a nomenclatura usada durante a execução assistida com os commits reais do Git.

Embora os rótulos `Fase 6A`, `Fase 6B`, `Fase 6C`, `Fase 6D`, `Fase 6E` e `Fase 6F` não apareçam nos assuntos dos commits, eles correspondem aos commits técnicos abaixo.

| Fase técnica | Commit | Descrição | Status |
|---|---|---|---|
| Fase 5 | `233fe8b` | Ordena snapshots de mercado cronologicamente | Concluída |
| Fase 6A | `46463fb` | Explicita colunas de execuções de pricing | Concluída |
| Fase 6B | `3f01728` | Explicita colunas de eventos e snapshots | Concluída |
| Fase 6C | `5a2fd34` | Normaliza consultas derived legadas com `StructureRef` | Concluída |
| Fase 6D | `d7291ae` | Ordena leituras derived por timestamp em Python | Concluída |
| Fase 6E | `0d75092` | Remove `SELECT *` real restante de `robo_legs_repository.py` | Concluída |
| Fase 6F | `14483c2` | Remove literais SQL inseguros remanescentes em comentários | Concluída |

## Marco final do subciclo

O subciclo técnico SQL/timestamp clean foi encerrado funcionalmente no commit:

`14483c2 chore: remove literais sql inseguros de comentarios`

Esse commit recebeu a tag:

`ciclo-2-sql-timestamp-clean`

O checkpoint documental posterior foi registrado em:

`4283d67 docs: registra checkpoint sql timestamp clean`

## Validações registradas

Durante o fechamento das fases técnicas foram registradas as seguintes validações:

- `compileall` OK;
- `bridge_ingest_csv.py --run-now` OK;
- pipeline derivado OK;
- snapshots consistentes OK;
- greps focados sem ocorrências reais problemáticas;
- grep geral final sem saída para literais SQL inseguros;
- testes específicos de robo legs OK: `10 passed`;
- suíte completa OK: `564 passed, 10 skipped`;
- working tree limpo.

## Resultado técnico consolidado

Após o fechamento do subciclo:

- não há `SELECT *` real problemático;
- não há `ORDER BY timestamp` real problemático;
- não há `MAX(timestamp)` real problemático;
- não há literais SQL inseguros remanescentes nem em comentários;
- a ordenação temporal sensível foi migrada para comparação controlada em Python quando aplicável;
- o repositório está apto a avançar para a próxima frente após o checkpoint `ciclo-2-sql-timestamp-clean`.

## Regra de continuidade

Para evitar retrabalho, qualquer próxima frente deve partir do estado posterior ao checkpoint `ciclo-2-sql-timestamp-clean`.

Não reabrir fases anteriores, como Fase 4 da rota antiga, sem justificativa documental explícita.
