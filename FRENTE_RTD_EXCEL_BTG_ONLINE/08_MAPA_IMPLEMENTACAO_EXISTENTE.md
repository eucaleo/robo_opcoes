# Mapa da implementação existente

## Objetivo

Mapear o que já existe antes de iniciar alterações funcionais da frente RTD Excel BTG Online.

## Camada de dados RTD atual

### Arquivos físicos

- `dados/RTD_LINKS.csv`
- `dados/RTD_LINKS_probe.csv`
- `dados/RTD_UNDERLYING_QUOTES.csv`

### Banco

- `rtd_option_quotes`
- `rtd_underlying_quotes`

As duas tabelas possuem campo `vwap`.

## Camada de repositórios

Arquivos relevantes:

- `repositories/rtd_option_quotes_repository.py`
- `repositories/market_snapshot_repository.py`
- `repositories/system_snapshots_repository.py`

Papel esperado:

- Ler e gravar snapshot.
- Servir dados para serviços superiores.
- Evitar acesso direto e duplicado ao banco.

## Camada de serviços

Arquivos relevantes:

- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`
- `services/structure_leg_rtd_enrichment_service.py`
- `services/structure_market_input_assembler.py`
- `services/terminal_vwap_payoff_app_service.py`
- `services/terminal_vwap_payoff_viewmodel_service.py`

Papel esperado:

- Selecionar melhor fonte de preço.
- Enriquecer legs com dados RTD.
- Alimentar terminal VWAP/payoff.
- Montar input operacional das estruturas.

## Camada de UI

Arquivos relevantes:

- `UI/components/terminal_vwap_payoff_panel.py`
- `UI/components/terminal_vwap_payoff_dark_panel.py`
- `controllers/terminal_vwap_payoff_controller.py`

Papel esperado:

- Exibir terminal operacional.
- Mostrar VWAP, payoff, estado e decisão.
- Futuramente exibir status de conexão RTD/Excel.

## Scripts legados ou auxiliares

Arquivos relevantes:

- `scripts/import_rtd_option_quotes_wide_csv.py`
- `scripts/refresh_rtd_symbol_to_option_quotes.py`
- `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py`
- `scripts/list_abas_rtd.py`
- `scripts/db_probe_manual_vs_rtd.py`

Papel esperado:

- Importação.
- Diagnóstico.
- Fallback.
- Auditoria.
- Nunca devem virar dependência principal da consulta online por símbolo.

## Testes já existentes úteis

Arquivos relevantes:

- `ATT/tests/test_bd_unico_rtd_tables_app_db.py`
- `ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py`
- `ATT/tests/test_market_snapshot_provider.py`
- `ATT/tests/test_market_snapshot_selector.py`
- `ATT/tests/test_structure_leg_rtd_enrichment_service.py`
- `ATT/tests/test_terminal_vwap_m12_contract_coverage.py`
- `ATT/tests/test_terminal_vwap_payoff_app_service.py`
- `ATT/tests/test_terminal_vwap_payoff_controller.py`
- `ATT/tests/test_terminal_vwap_payoff_panel.py`
- `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py`

Esses testes devem compor a base acumulativa da nova frente.

## Lacuna provável

Ainda precisa ser confirmado se existe integração viva com Excel aberto via COM.

A nova frente deve verificar:

- Detecção de Excel aberto.
- Detecção de `LISTA_RTD.xlsm`.
- Leitura em bloco da aba RTD.
- Validação de cabeçalhos obrigatórios.
- Atualização do snapshot sem subprocesso.
