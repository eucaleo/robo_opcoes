# Rodada 43 - Sequencia full de desenvolvimento e correcao

## Centro de verdade mantido

UI
  -> PayoffRefreshCommandService
    -> PricingExecutionAppService
      -> PricingExecutionOrchestrationService
        -> PricingExecutionService
        -> PricingExecutionPersistenceService
          -> PricingExecutionsRepository
          -> SystemSnapshotsRepository
          -> DerivedPayoffPersistence
            -> payoff_curve_points
            -> structure_decisions

## Estado confirmado antes desta rodada

- Verificacao 38: aplicacao tecnica consistente.
- Verificacao 39: py_compile dos arquivos centrais passou.
- Verificacao 40: UI/main_window.py passou no py_compile.
- Correcao 41: erro de sintaxe em UI/main_window.py removido.
- Verificacao 42: execute_pricing sem UI aumentou as quatro contagens:
  - pricing_executions
  - structure_snapshots
  - payoff_curve_points
  - structure_decisions

## Regra operacional desta fase

- Nao executar git add.
- Nao executar git commit.
- Nao executar git push.
- Nao criar motor paralelo de payoff.
- Nao transformar script de manutencao em fluxo oficial.
- Nao corrigir UI antes de validar comando oficial.
- Nao permitir sucesso silencioso quando payoff_points_count for zero.

## Sequencia full recomendada

### 1. Verificar commits anteriores

Objetivo:
- entender a linha recente de desenvolvimento;
- evitar refazer patch ja aplicado;
- identificar arquivos alterados e nao rastreados.

Saidas esperadas:
- log recente;
- branch atual;
- status;
- diff sem stage.

### 2. Auditar arquivos ja gerados na frente

Pastas principais:
- FRENTE_RTD_EXCEL_BTG_ONLINE
- FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/GUARDRAILS_36
- FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/UI_CLEANUP_35

Objetivo:
- reaproveitar diagnosticos existentes;
- evitar duplicidade de auditoria;
- confirmar se os arquivos anteriores apontam pendencias ainda abertas.

### 3. Consolidar PayoffRefreshCommandService

Arquivo principal:
- services/payoff_refresh_command_service.py

Contrato esperado:
- valida structure_id;
- bloqueia estruturas nao active;
- captura timestamp antes;
- chama PricingExecutionAppService.execute_pricing;
- captura timestamp depois;
- conta pontos persistidos;
- valida decisao correspondente;
- retorna status ok, warning ou error;
- nunca retorna ok se payoff_points_count for zero.

### 4. Validar backend e wiring

Arquivos:
- services/pricing_execution_app_service.py
- services/pricing_execution_orchestration_service.py
- services/pricing_execution_persistence_service.py
- services/derived_payoff_persistence.py
- services/derived_service.py
- services/canonical_pricing_facade.py

Objetivo:
- confirmar que DerivedPayoffPersistence esta conectado ao fluxo oficial;
- confirmar que nao ha persistencia paralela desalinhada;
- classificar canonical_pricing_facade como fluxo oficial, fachada alternativa ou legado compativel.

### 5. Quarentenar script paralelo

Arquivo:
- scripts/recalculate_payoff_curve_points_once.py

Classificacao:
- manutencao;
- emergencia;
- legado operacional;
- nao fluxo oficial.

Regras:
- nao deve ser chamado pela UI;
- nao deve substituir PayoffRefreshCommandService;
- nao deve ser usado como motor produtivo.

### 6. Limpar UI somente depois do comando validado

Arquivo principal:
- UI/components/terminal_vwap_payoff_dark_panel.py

Pendencias esperadas:
- remover ou bloquear calculo local;
- remover fallback local;
- separar atualizar visual de recalcular payoff;
- UI deve apenas chamar comando oficial e reler snapshot persistido.

Metodos proibidos na UI:
- _calculate_payoff_from_legs
- _calculate_payoff_points_for_range
- _calculate_leg_payoff
- _collect_payoff_strikes
- _calculate_payoff_spot_range

### 7. Padronizar leitura do ultimo snapshot

Regra:
- buscar primeiro o ultimo timestamp por structure_id;
- carregar pontos somente daquele timestamp;
- buscar structure_decisions correspondente ao mesmo timestamp.

### 8. Criar ou reforcar guardrail automatico

O guardrail deve falhar se encontrar na UI:
- compute_payoff_from_canonical_input
- _calculate_payoff_from_legs
- _calculate_payoff_points_for_range
- _calculate_leg_payoff
- subprocess.run
- subprocess.Popen
- os.system
- INSERT INTO payoff_curve_points
- INSERT INTO structure_decisions

Tambem deve validar:
- PayoffRefreshCommandService existe;
- chama PricingExecutionAppService;
- chama execute_pricing;
- leitura usa ultimo timestamp;
- scripts legados nao sao chamados pela UI.

## Criterio de encerramento da fase

A fase so deve ser encerrada quando:

1. PayoffRefreshCommandService passar no contrato.
2. Backend continuar gerando as quatro persistencias.
3. Script paralelo estiver classificado como manutencao.
4. UI estiver sem calculo local ou com calculo local bloqueado por erro explicito.
5. Guardrail oficial passar.
6. py_compile dos arquivos centrais passar.
7. Git status estiver revisado conscientemente.
8. Somente entao decidir git add, commit e push controlados.
