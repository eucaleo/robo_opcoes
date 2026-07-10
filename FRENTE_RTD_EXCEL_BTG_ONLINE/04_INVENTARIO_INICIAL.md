# Inventário inicial da frente RTD Excel BTG Online

## Situação após auditoria inicial

A frente foi aberta e commitada na branch `refactor/bd-unico-appdb`.

O banco `dados/app.db` está íntegro:

`PRAGMA integrity_check: ok`

## Conclusão inicial

O sistema já possui uma base importante relacionada a RTD, snapshot, enriquecimento de legs, estrutura operacional, terminal VWAP/payoff e banco único.

A nova frente não deve reescrever essas partes. A abordagem correta é:

1. Reaproveitar o snapshot já existente.
2. Reaproveitar os repositórios e serviços já testados.
3. Criar a ponte online Excel RTD como nova fonte alimentadora.
4. Evitar subprocessos para consulta individual.
5. Remover ou isolar código legado somente depois de teste equivalente.

## Itens encontrados

| Item | Situação | Ação sugerida |
|---|---|---|
| `LISTA_RTD.xlsm` | Existe na raiz | Usar como ponte viva RTD |
| `dados/RTD_LINKS.csv` | Existe | Manter como fonte legada/compatibilidade durante transição |
| `dados/RTD_LINKS_probe.csv` | Existe | Investigar se ainda é necessário |
| `dados/RTD_UNDERLYING_QUOTES.csv` | Existe | Manter como fonte legada/compatibilidade durante transição |
| `rtd_option_quotes` | Existe no `app.db` | Reaproveitar como snapshot de opções |
| `rtd_underlying_quotes` | Existe no `app.db` | Reaproveitar como snapshot de ativo base |
| `repositories/rtd_option_quotes_repository.py` | Existe | Reaproveitar |
| `repositories/market_snapshot_repository.py` | Existe | Reaproveitar |
| `services/market_snapshot_provider.py` | Existe | Reaproveitar |
| `services/market_snapshot_selector.py` | Existe | Reaproveitar |
| `services/structure_leg_rtd_enrichment_service.py` | Existe | Reaproveitar para preenchimento de legs |
| `infra/bootstrap_rtd_option_quotes_schema.py` | Existe | Revisar antes de qualquer migração |
| `scripts/import_rtd_option_quotes_wide_csv.py` | Existe | Manter como importador legado/controlado |
| `scripts/refresh_rtd_symbol_to_option_quotes.py` | Existe | Investigar se vira fallback ou se será substituído pelo coletor online |
| `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py` | Existe | Investigar como fallback |
| `scripts/list_abas_rtd.py` | Existe | Possível reaproveitamento para inspeção da planilha |
| `tools/audit_rtd_ui_flow.py` | Existe | Reaproveitar na auditoria do fluxo UI |
| `UI/components/terminal_vwap_payoff_panel.py` | Existe | Reaproveitar para UI operacional |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | Existe | Reaproveitar para UI operacional |
| `controllers/terminal_vwap_payoff_controller.py` | Existe | Reaproveitar |
| `services/terminal_vwap_payoff_app_service.py` | Existe | Reaproveitar |
| `services/terminal_vwap_payoff_viewmodel_service.py` | Existe | Reaproveitar |

## Tabelas atuais relevantes

| Tabela | Linhas | Papel provável |
|---|---:|---|
| `rtd_option_quotes` | 9 | Snapshot atual de opções |
| `rtd_underlying_quotes` | 2 | Snapshot atual de ativos base |
| `structure_legs` | 24 | Pernas das estruturas |
| `structure_snapshots` | 57 | Histórico/snapshots de estruturas |
| `structure_leg_snapshots` | 228 | Histórico de legs por snapshot |
| `payoff_curve_points` | 808 | Pontos de payoff |
| `structure_decisions` | 11 | Decisões operacionais |
| `pricing_executions` | 25 | Execuções de precificação |

## Classificação técnica inicial

### Manter

- Banco único `dados/app.db`.
- Tabelas `rtd_option_quotes` e `rtd_underlying_quotes`.
- Repositórios de snapshot e market snapshot.
- Serviços de enriquecimento de legs.
- Terminal VWAP/payoff.
- Testes existentes relacionados a RTD, snapshot, terminal e legs.

### Reaproveitar

- Scripts de importação CSV RTD como fallback.
- Scripts de refresh RTD como referência de mapeamento.
- Script `list_abas_rtd.py` para inspeção da planilha.
- Ferramenta `tools/audit_rtd_ui_flow.py`.

### Adaptar

- Fluxo de atualização RTD que hoje depende de CSV/refresh.
- Preenchimento de legs para priorizar snapshot vivo.
- UI para exibir status RTD/Excel/dados.

### Investigar

- Necessidade real de `RTD_LINKS_probe.csv`.
- Chamadas a subprocessos.
- Pontos de refresh sob demanda.
- Existência ou ausência de integração Excel COM já utilizável.
- Campos exatos da aba viva no `LISTA_RTD.xlsm`.

### Remover somente após prova

Nenhum arquivo deve ser removido nesta fase.

Remoção só pode ocorrer depois de:

1. Auditoria refinada.
2. Teste equivalente.
3. Substituição funcional validada.
4. Commit separado.
