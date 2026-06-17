# AUDITORIA ROTA_MESTRE_2

Arquivo vivo de auditoria da ROTA_MESTRE_2.

Este documento deve ser atualizado ao final de cada fase, registrando comandos executados, testes, resultados, decisões, pendências e commit relacionado.

## Regras de auditoria

Para cada fase encerrada, registrar obrigatoriamente:

- fase
- objetivo
- arquivos auditados
- arquivos alterados
- comandos executados
- testes executados
- resultado
- pendências
- decisão tomada
- commit relacionado

Antes de qualquer alteração funcional, deve existir mapa de impacto contendo:

- arquivos que serão alterados
- arquivos apenas auditados
- risco esperado
- testes que validarão a mudança
- plano de reversão

---

## Fase 0 — Marco de Controle e Congelamento da Rota

### Status

Em preparação para encerramento.

### Data/hora

13/06/2026 18:38 BRT

### Objetivo

Formalizar a ROTA_MESTRE_2 como documento norteador do novo ciclo de desenvolvimento, preservando o encerramento da ROTA_MESTRE_1 e impedindo reabertura indevida de fases anteriores.

### Arquivos auditados

- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
- docs/AUDITORIA_ROTA_MESTRE_2.md

### Arquivos alterados

- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
- docs/AUDITORIA_ROTA_MESTRE_2.md

### Alterações funcionais

Nenhuma.

### Mapa de impacto

#### Arquivos que serão alterados

- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
- docs/AUDITORIA_ROTA_MESTRE_2.md

#### Arquivos apenas auditados

- docs/
- estado do Git

#### Risco esperado

Baixo. Alteração exclusivamente documental.

Não há impacto em:

- UI
- banco de dados
- repositórios
- serviços
- cálculo
- ingestão
- bridge
- scripts operacionais

#### Testes que validarão a mudança

- Conferência de existência dos arquivos documentais.
- Conferência do conteúdo mínimo da ROTA_MESTRE_2.
- Conferência do conteúdo mínimo da auditoria.
- Conferência de diff antes do commit.
- Conferência de status do Git.

#### Plano de reversão

Restaurar os arquivos documentais pelo Git ou remover o arquivo de auditoria caso ainda não esteja versionado.

### Comandos executados

```bash
git status
git branch --show-current
test -f docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
test -f docs/AUDITORIA_ROTA_MESTRE_2.md
grep -n "INICIO ROTA_MESTRE_2" docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
grep -n "Fase 0" docs/AUDITORIA_ROTA_MESTRE_2.md
git diff -- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md docs/AUDITORIA_ROTA_MESTRE_2.md

---

## Fase 1 — Mapeamento automatizado de RTD, Excel, Bridge, Serviços e UI

### Status

Iniciada.

### Objetivo

Executar mapeamento amplo de referências relacionadas a RTD, Excel, bridge, opções, persistência, serviços, cálculo e UI.

### Arquivos alterados

- `scripts/mapear_automacao_opcoes_rtd.py`
- `docs/mapeamento_automacao_opcoes_rtd.md`
- `docs/mapeamento_automacao_opcoes_rtd.json`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Alterações funcionais

Nenhuma.

### Testes executados

```bash
python -m py_compile scripts/mapear_automacao_opcoes_rtd.py
python scripts/mapear_automacao_opcoes_rtd.py
test -f docs/mapeamento_automacao_opcoes_rtd.md
test -f docs/mapeamento_automacao_opcoes_rtd.json
grep -n "Mapeamento automação opções RTD" docs/mapeamento_automacao_opcoes_rtd.md
git status --short

---

## Fase 1 — Encerramento com lista priorizada

### Status

Encerrada.

### Base utilizada

- `docs/mapeamento_automacao_opcoes_rtd.md`
- `docs/mapeamento_automacao_opcoes_rtd.json`
- `docs/lista_priorizada_automacao_opcoes_rtd.md`

### Resultado do mapeamento bruto

O mapeamento automatizado identificou alto volume de candidatos, incluindo documentação, testes e arquivos derivados.

Resumo do relatório bruto:

- Total de achados: 200
- Candidatos fortes: 152
- Candidatos médios: 33
- Candidatos baixos: 15

### Decisão de priorização

Foi criada lista priorizada separando arquivos operacionais de ruído documental/histórico.

Prioridade máxima para as próximas fases:

- `dados/RTD_LINKS.csv`
- `repositories/rtd_option_quotes_repository.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`
- `repositories/market_snapshot_repository.py`
- `services/structure_market_input_assembler.py`
- `services/canonical_input_service.py`

### Alterações funcionais

Nenhuma.

### Arquivos alterados nesta etapa

- `docs/lista_priorizada_automacao_opcoes_rtd.md`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Testes/conferências executados

```bash
sed -n '1,220p' docs/lista_priorizada_automacao_opcoes_rtd.md
git status --short
git diff --stat


---

## Fase 1 — Encerramento com lista priorizada

### Status

Encerrada.

### Base utilizada

- `docs/mapeamento_automacao_opcoes_rtd.md`
- `docs/mapeamento_automacao_opcoes_rtd.json`
- `docs/lista_priorizada_automacao_opcoes_rtd.md`

### Resultado do mapeamento bruto

O mapeamento automatizado identificou alto volume de candidatos, incluindo documentação, testes e arquivos derivados.

Resumo do relatório bruto:

- Total de achados: 200
- Candidatos fortes: 152
- Candidatos médios: 33
- Candidatos baixos: 15

### Decisão de priorização

Foi criada lista priorizada separando arquivos operacionais de ruído documental/histórico.

Prioridade máxima para as próximas fases:

- `dados/RTD_LINKS.csv`
- `repositories/rtd_option_quotes_repository.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`
- `repositories/market_snapshot_repository.py`
- `services/structure_market_input_assembler.py`
- `services/canonical_input_service.py`

### Alterações funcionais

Nenhuma.

### Arquivos alterados nesta etapa

- `docs/lista_priorizada_automacao_opcoes_rtd.md`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Testes/conferências executados

```bash
sed -n '1,220p' docs/lista_priorizada_automacao_opcoes_rtd.md
git status --short
git diff --stat


---

## Fase 2 — Auditoria do contrato RTD/Excel e arquivos de entrada

### Status

Iniciada.

### Objetivo

Auditar o contrato entre RTD, Excel e arquivos locais de entrada, sem alteração funcional.

### Base da fase anterior

- `docs/lista_priorizada_automacao_opcoes_rtd.md`

### Arquivos principais sob auditoria

- `dados/RTD_LINKS.csv`
- `bridge/analise_robo.csv`
- `bridge/analise_robo_legs.csv`
- `bridge/hist_robo.csv`
- `bridge/configuracoes.csv`
- `LISTA_RTD.xlsm`

### Arquivos gerados nesta etapa

- `docs/fase_2_auditoria_contrato_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.json`

### Alterações funcionais

Nenhuma.

### Testes/conferências executados

```bash
sed -n '1,220p' docs/fase_2_diagnostico_csvs_rtd_excel.md
git status --short
git diff --stat

---

## Fase 2 — Encerramento com mapa do contrato RTD/Excel

### Status

Encerrada.

### Base utilizada

- `docs/fase_2_auditoria_contrato_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.md`
- `docs/fase_2_diagnostico_csvs_rtd_excel.json`
- `docs/fase_2_mapa_contrato_rtd_excel.md`

### Achados principais

A Fase 2 identificou dois formatos principais de contrato:

1. Contrato atributo/valor:
   - `dados/RTD_LINKS.csv`

2. Contratos tabulares operacionais/exportados:
   - `bridge/analise_robo_legs.csv`
   - `bridge/analise_robo.csv`
   - `bridge/hist_robo.csv`
   - demais arquivos `bridge/*.csv`

### Arquivos classificados como prioritários

- `dados/RTD_LINKS.csv`
- `bridge/analise_robo_legs.csv`
- `bridge/analise_robo.csv`
- `bridge/hist_robo.csv`

### Achados de compatibilidade

Foram registrados:

- divergência de delimitador em `bridge/encerramentos_manuais.csv`
- sinais de encoding inconsistente em `bridge/configuracoes.csv`
- sinais de encoding inconsistente em `bridge/rolls_detectados.csv`
- diferença de nomes de colunas entre contratos RTD e bridge
- provável dependência indireta do Excel `.xlsm`

### Alterações funcionais

Nenhuma.

### Arquivos alterados nesta etapa

- `docs/fase_2_mapa_contrato_rtd_excel.md`
- `docs/AUDITORIA_ROTA_MESTRE_2.md`

### Testes/conferências executados

```bash
sed -n '1,260p' docs/fase_2_mapa_contrato_rtd_excel.md
git status --short
git diff --stat
```

### Decisão tomada

A Fase 2 está encerrada.

A próxima fase deve auditar a persistência de cotações RTD/opções, com foco em:

- `repositories/rtd_option_quotes_repository.py`
- `repositories/market_snapshot_repository.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`

Nenhuma alteração em UI, banco, schema, cálculo, ingestão, serviços operacionais, CSVs ou Excel operacional foi realizada.


---

## Checkpoint reconciliado — subciclo técnico SQL/timestamp clean

### Contexto

Durante a evolução da branch `ciclo-2-testes-evolucao`, foi executado um subciclo técnico identificado na interação assistida como:

- Fase 5;
- Fase 6A;
- Fase 6B;
- Fase 6C;
- Fase 6D;
- Fase 6E;
- Fase 6F.

Essas fases não foram gravadas com esses rótulos nos assuntos dos commits, mas estão reconciliadas oficialmente no checkpoint:

`docs/checkpoints/ciclo-2-sql-timestamp-clean.md`

### Mapeamento oficial

| Fase técnica | Commit | Descrição |
|---|---|---|
| Fase 5 | `233fe8b` | Ordena snapshots de mercado cronologicamente |
| Fase 6A | `46463fb` | Explicita colunas de execuções de pricing |
| Fase 6B | `3f01728` | Explicita colunas de eventos e snapshots |
| Fase 6C | `5a2fd34` | Normaliza consultas derived legadas com `StructureRef` |
| Fase 6D | `d7291ae` | Ordena leituras derived por timestamp em Python |
| Fase 6E | `0d75092` | Remove `SELECT *` real restante de `robo_legs_repository.py` |
| Fase 6F | `14483c2` | Remove literais SQL inseguros remanescentes em comentários |

### Tag de fechamento

`ciclo-2-sql-timestamp-clean`

### Commit documental posterior

`4283d67 docs: registra checkpoint sql timestamp clean`

### Decisão de rota

A partir deste registro, a continuidade da rota deve considerar como ponto de partida o estado posterior ao checkpoint `ciclo-2-sql-timestamp-clean`.

Não deve ser aberta uma nova frente baseada em fases antigas ou em numeração histórica sem reconciliar previamente com:

- histórico Git;
- checkpoint;
- auditoria da rota;
- testes executados;
- estado atual da branch.

### Status

Checkpoint técnico reconciliado documentalmente.

