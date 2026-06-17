# Fase 2 - Diagnóstico do Fluxo Atual

## Objetivo

Registrar o diagnóstico do fluxo atual do sistema antes de qualquer correção técnica, conforme definido na ROTA MESTRE.

Esta fase não altera regra de negócio. O objetivo é mapear as fontes atuais de leitura, escrita, cálculo e exibição.

## Estado inicial

Branch analisada:

```text
limpeza-tests-scripts-checks
```

Commit anterior de referência:

```text
0fc0495 Remove duplicidade de testes de carga do editor de estruturas
```

## Testes executados

### Suite completa

Comando:

```bash
python -m pytest ATT/tests -q
```

Resultado:

```text
445 passed, 2 skipped
```

### Checks completos

Comando:

```bash
python ATT/checks/run_all_checks.py
```

Resultado:

```text
Todos os checks passaram
```

### Validação de diff

Comando:

```bash
git diff --check
```

Resultado:

```text
sem erros
```

### Testes focados

Comando:

```bash
python -m pytest \
  ATT/tests/test_structures_repository.py \
  ATT/tests/test_structure_editor_dialog.py \
  ATT/tests/test_structure_editor_integration.py \
  ATT/tests/test_structures_archive_wiring.py \
  ATT/tests/test_structure_analysis_service.py \
  ATT/tests/test_pricing_execution_controller.py \
  -q
```

Resultado:

```text
141 passed, 2 skipped
```

## 1. Leitura de estruturas

O cadastro operacional de estruturas utiliza o banco:

```text
dados/app.db
```

Módulo principal:

```text
repositories/structures_repository.py
```

Consumidores identificados:

```text
UI/components/structures_list_panel.py
UI/components/structure_editor_dialog.py
api/structures_controller.py
services/canonical_input_service.py
services/canonical_pricing_facade.py
```

Funções relevantes:

```text
create_structure
list_structures
get_structure
update_structure
archive_structure
add_leg
replace_legs
get_structure_by_alias
get_structure_id_by_alias
```

Conclusão:

```text
As estruturas novas e persistidas já têm caminho principal no banco app.db via StructuresRepository.
```

## 2. Leitura e escrita de pernas

Há dois fluxos distintos.

### Pernas cadastradas na estrutura

Fonte:

```text
dados/app.db
```

Módulo:

```text
repositories/structures_repository.py
```

Funções:

```text
_fetch_legs
add_leg
replace_legs
count_legs
```

Consumidores:

```text
UI/components/structure_editor_dialog.py
UI/components/structures_list_panel.py
api/structures_controller.py
services/canonical_input_service.py
```

### Pernas de mercado, robô ou RTD legado

Fonte:

```text
dados/app.db
```

Tabelas ou conceitos encontrados:

```text
rtd_analise_robo_legs
manual_analise_robo_legs
```

Módulos:

```text
repositories/market_snapshot_repository.py
repositories/robo_legs_repository.py
repositories/robo_legs_status_repository.py
services/market_snapshot_selector.py
services/robo_legs_service.py
services/legacy_robo_legs_fallback.py
```

Conclusão:

```text
As pernas operacionais novas estão no banco, mas ainda existe dependência de tabelas com semântica legada ANALISE_ROBO_LEGS.
```

## 3. Origem de bid, ask, last, gregas e volatilidade

Foram identificados três caminhos.

### Snapshots de mercado no app.db

Módulo:

```text
repositories/market_snapshot_repository.py
```

Tabelas:

```text
rtd_analise_robo_legs
manual_analise_robo_legs
rtd_analise_robo
```

Campos encontrados:

```text
bid
ask
iv
delta
gamma
theta
vega
spot
```

### Cotações RTD de opções

Módulo:

```text
repositories/rtd_option_quotes_repository.py
```

Tabela:

```text
rtd_option_quotes
```

Origem declarada no código:

```text
CSV exportado da aba RTD_LINKS
```

Campos:

```text
ativo_base
ticker
bid
ask
last
iv
delta
gamma
theta
vega
```

### Provider temporário de mercado

Módulo:

```text
services/market_snapshot_provider.py
```

Campos internos:

```text
spot
interest_rate
volatility
```

Conclusão:

```text
O sistema possui repositórios de mercado, mas ainda mistura fonte RTD, tabelas legadas e provider interno temporário.
```

## 4. Escrita de dados importados e derivados

### Banco operacional

Banco:

```text
dados/app.db
```

Usado para:

```text
estruturas
pernas
pricing executions
rtd_option_quotes
rtd_analise_robo
rtd_analise_robo_legs
manual_analise_robo_legs
```

Módulos principais:

```text
repositories/structures_repository.py
repositories/pricing_executions_repository.py
repositories/rtd_option_quotes_repository.py
repositories/market_snapshot_repository.py
repositories/robo_legs_repository.py
```

### Banco derivado

Banco:

```text
dados/derived.db
```

Usado para:

```text
payoff
decisões
snapshots derivados
curvas calculadas
```

Módulos principais:

```text
db/derived_repo.py
services/derived_service.py
services/derived_payoff_persistence.py
UI/models/ui_data.py
UI/components/details_panel.py
```

Conclusão:

```text
O sistema separa parcialmente dados operacionais em app.db e dados derivados em derived.db.
```

## 5. Consumo da UI

A UI consome principalmente bancos SQLite.

### Estruturas

Fonte:

```text
StructuresRepository -> dados/app.db
```

Arquivos:

```text
UI/components/structures_list_panel.py
UI/components/structure_editor_dialog.py
```

### Payoff, decisões e detalhes

Fonte:

```text
dados/derived.db
```

Arquivos:

```text
UI/models/ui_data.py
UI/components/details_panel.py
```

### Excel direto na UI

Não foi identificada importação direta de Excel na camada de UI, como:

```text
win32com
openpyxl
OPERACOES_E_OPCOES
```

Conclusão:

```text
A UI não parece acessar Excel diretamente, mas ainda consome dados derivados que podem ter origem indireta no fluxo legado.
```

## 6. Persistência de novas estruturas

Evidências:

```text
141 passed, 2 skipped nos testes focados
```

Módulos envolvidos:

```text
UI/components/structure_editor_dialog.py
UI/components/structures_list_panel.py
repositories/structures_repository.py
api/structures_controller.py
```

Funções confirmadas:

```text
create_structure
replace_legs
update_structure
archive_structure
get_structure
list_structures
```

Conclusão:

```text
O fluxo de cadastro e persistência de novas estruturas está funcional no banco app.db.
```

## 7. Dependência de ANALISE_ROBO, ANALISE_ROBO_LEGS e HIST_ROBO

Ainda existem dependências.

### Dependências em código ou schema

Arquivos:

```text
repositories/market_snapshot_repository.py
repositories/robo_legs_repository.py
repositories/robo_legs_status_repository.py
domain/market_snapshot.py
services/canonical_pricing_facade.py
db/schema_excel.py
db/import_excel.py
```

Tabelas e conceitos encontrados:

```text
rtd_analise_robo
rtd_analise_robo_legs
manual_analise_robo_legs
robo_snapshot
robo_legs_snapshot
robo_legs_history
```

### Dependências em checks

Arquivos validados pelos checks:

```text
bridge/analise_robo.csv
bridge/analise_robo_legs.csv
bridge/analise_raiox.csv
LISTA_RTD.xlsm
```

Conclusão:

```text
A dependência operacional legada ainda existe e deve ser classificada na Fase 3 e auditada formalmente na Fase 4.
```

## Mapa resumido do fluxo atual

```text
Estruturas:
- leitura: repositories/structures_repository.py
- escrita: repositories/structures_repository.py
- persistência: dados/app.db
- UI: structures_list_panel e structure_editor_dialog

Pernas:
- leitura: structures_repository, market_snapshot_repository, robo_legs_repository
- escrita: structures_repository para pernas cadastradas
- vínculo com estrutura: app.db
- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs

Cotações:
- fonte atual: app.db, rtd_option_quotes, rtd_analise_robo_legs e provider temporário
- banco usado: app.db
- fallback legado: legacy_robo_legs_fallback e tabelas com semântica ANALISE_ROBO

UI:
- fontes consumidas: app.db e derived.db
- dependência direta de CSV: não evidenciada como fonte principal de UI
- dependência direta de Excel: não evidenciada na UI
- risco: dados derivados exibidos podem ter origem indireta no fluxo legado

Excel/bridge:
- Excel ainda aparece em checks locais
- bridge/analise_robo.csv, bridge/analise_robo_legs.csv e bridge/analise_raiox.csv ainda aparecem em checks
- estes artefatos devem ser classificados na Fase 3
```

## Critério de saída da Fase 2

Critério da ROTA:

```text
Mapa claro do fluxo atual.
```

Status:

```text
Atendido para avanço à Fase 3, após commit deste documento.
```

## Próxima fase

A próxima fase da ROTA é:

```text
Fase 3 - Classificação das Fontes de Dados
```

Objetivo da próxima fase:

```text
Separar entrada bruta, configuração, legado, derivado, operacional, temporário e descartável.
```
