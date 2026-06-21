# Fase 1 — Fechamento do mapa runtime do código atual

## Objetivo

Mapear, sem alterar código-fonte, os fluxos runtime relacionados a:

1. Atualizar Dados.
2. Cadastro manual de estruturas e erro de strike.
3. Cálculo e persistência de payoff.
4. Cálculo e persistência de decisões.
5. Leitura RTD, manual e rtd_option_quotes.

## Escopo

Esta fase foi exclusivamente diagnóstica.

Não houve alteração de código-fonte. Foram geradas apenas evidências em:

    docs/checkpoints/evidencias/

## Evidências geradas

### Mapas por termo

    fase-1-mapa-atualizar-dados-codigo-atual.txt
    fase-1-mapa-atualizar-dados-runtime-codigo-atual.txt
    fase-1-mapa-decisoes-codigo-atual.txt
    fase-1-mapa-decisoes-runtime-codigo-atual.txt
    fase-1-mapa-payoff-codigo-atual.txt
    fase-1-mapa-payoff-runtime-codigo-atual.txt
    fase-1-mapa-rtd-codigo-atual.txt
    fase-1-mapa-rtd-runtime-codigo-atual.txt
    fase-1-mapa-strike-codigo-atual.txt
    fase-1-mapa-strike-runtime-codigo-atual.txt

### Trechos cirúrgicos

    fase-1-trechos-atualizar-dados-runtime.txt
    fase-1-trechos-payoff-decisoes-runtime.txt
    fase-1-trechos-rtd-runtime.txt
    fase-1-trechos-strike-runtime.txt

### Índice consolidado

    fase-1-indice-trechos-runtime.txt

## 1. Fluxo de Atualizar Dados

Arquivos principais:

    UI/main_window.py
    UI/models/ui_data.py

Pontos encontrados:

    MainWindow.__init__() chama self.refresh_data()
    Menu Atualizar Dados chama self.refresh_data()
    F5 chama self.refresh_data()
    refresh_data() chama self.data_model.refresh()
    refresh_data() atualiza filtros, grid e detalhes

Fluxo runtime identificado:

    Inicialização / Menu Atualizar Dados / F5
        |
        v
    UI/main_window.py::refresh_data()
        |
        v
    UI/models/ui_data.py::refresh()
        |
        v
    FiltersPanel.update_structures(...)
        |
        v
    DecisionsGrid.update_data(...)
        |
        v
    DetailsPanel.update_decision(...)

Ponto candidato para investigação na Fase 2:

    Verificar se UIDataModel.refresh() lê o snapshot correto após recalcular
    e persistir payoff e decisões.

## 2. Cadastro manual e erro de strike

Arquivos principais:

    UI/components/structure_editor_dialog.py
    repositories/structures_repository.py
    validators/leg_validator.py
    validators/validators__init__.py

Pontos encontrados:

    structure_editor_dialog.py::_cmd_add_leg()
    structure_editor_dialog.py::_cmd_apply_leg()
    structure_editor_dialog.py::_build_legs_payload()
    structures_repository.py::_validate_leg()

Evidência principal:

    _cmd_add_leg() cria uma leg com strike vazio.
    _cmd_apply_leg() monta payload com strike vindo de self._lf_strike.get().
    structures_repository.py lê strike a partir de leg.get("strike").
    structures_repository.py tenta converter strike com float(strike).
    em caso de falha, levanta ValueError("strike must be numeric").

Fluxo provável do erro:

    Leg nova nasce com strike vazio.
        |
        v
    Usuário aplica ou salva sem preencher ou com formato não aceito.
        |
        v
    Payload leva strike como string vazia ou texto inválido.
        |
        v
    repositories/structures_repository.py::_validate_leg()
        |
        v
    float(strike)
        |
        v
    ValueError("strike must be numeric")

Observação sobre validators:

    validators verificam strike is None,
    mas a UI pode enviar strike como string vazia.

Candidato de correção para Fase 2:

    Normalizar e validar strike na borda da UI antes de persistir.
    Tratar string vazia como campo obrigatório ausente.
    Opcionalmente aceitar formato brasileiro com vírgula, se essa for a regra do produto.

## 3. Fluxo de payoff

Arquivos principais:

    services/calculation_orchestrator.py
    domain/payoff.py
    services/derived_service.py
    services/derived_payoff_persistence.py
    db/derived_repo.py
    UI/models/ui_data.py
    UI/components/payoff_chart.py

Funções principais:

    run_payoff()
    compute_payoff_from_canonical_input()
    compute_payoff_curve_from_canonical_legs()
    save_payoff_from_canonical_payload()
    DerivedRepo.write_payoff_snapshot_atomic()
    DerivedRepo.insert_payoff_points()
    DerivedRepo.write_complete_snapshot_atomic()

Fluxo identificado:

    CalculationRequest / canonical input
        |
        v
    services/calculation_orchestrator.py::run_payoff()
        |
        v
    domain/payoff.py::compute_payoff_from_canonical_input()
        |
        v
    services/derived_service.py / services/derived_payoff_persistence.py
        |
        v
    db/derived_repo.py
        |
        v
    payoff_curve_points
        |
        v
    UIDataModel / PayoffChart

Tabela principal:

    payoff_curve_points

Chaves e índices relevantes:

    UNIQUE(timestamp, aba, point_spot)
    INDEX(structure_id, timestamp)

Ponto candidato para investigação na Fase 2:

    Confirmar consistência entre timestamp, aba e structure_id usados na escrita
    e na leitura da UI.

## 4. Fluxo de decisões

Arquivos principais:

    services/calculation_orchestrator.py
    domain/decision.py
    services/derived_service.py
    services/derived_payoff_persistence.py
    db/derived_repo.py
    UI/models/ui_data.py
    UI/components/decisions_grid.py
    UI/components/details_panel.py

Funções principais:

    run_decision()
    compute_decision_from_contract()
    compute_decision_from_payoff()
    compute_decision_from_inputs()
    save_decision_from_canonical_payload()
    DerivedRepo.write_decision_snapshot_atomic()
    DerivedRepo.insert_structure_decision()
    DerivedRepo.write_complete_snapshot_atomic()

Fluxo identificado:

    Payoff / canonical input
        |
        v
    services/calculation_orchestrator.py::run_decision()
        |
        v
    domain/decision.py
        |
        v
    services/derived_service.py / services/derived_payoff_persistence.py
        |
        v
    db/derived_repo.py
        |
        v
    structure_decisions
        |
        v
    UIDataModel / DecisionsGrid / DetailsPanel

Tabela principal:

    structure_decisions

Chaves e índices relevantes:

    UNIQUE(timestamp, aba)
    INDEX(aba, timestamp)
    INDEX(timestamp)

Ponto candidato para investigação na Fase 2:

    Confirmar se a decisão exibida pela UI é a decisão recém-persistida
    ou snapshot anterior.

## 5. Fluxo RTD/manual/rtd_option_quotes

Arquivos principais:

    repositories/market_snapshot_repository.py
    services/market_snapshot_selector.py
    repositories/rtd_option_quotes_repository.py
    services/structure_leg_rtd_enrichment_service.py

Funções e classes principais:

    MarketSnapshotRepository.get_rtd_legs()
    MarketSnapshotRepository.get_rtd_option_quote_legs()
    MarketSnapshotRepository.get_manual_legs()
    MarketSnapshotRepository.get_rtd_summary()
    MarketSnapshotSelector.select()
    RtdOptionQuotesRepository.get_by_codigo()
    StructureLegRtdEnrichmentService.enrich()

Política identificada:

    manual > rtd_option_quotes > rtd

Observação importante:

    rtd_option_quotes é cache de cotação.
    rtd_option_quotes não define composição estrutural.
    A composição vem das legs RTD ou manuais.

Fluxo identificado:

    manual_analise_robo_legs / rtd_analise_robo_legs
        |
        v
    MarketSnapshotRepository
        |
        v
    opcional: enriquecimento por rtd_option_quotes
        |
        v
    MarketSnapshotSelector
        |
        v
    canonical/pricing pipeline

Ponto candidato para investigação na Fase 2:

    Confirmar que o snapshot escolhido para cálculo é o mesmo esperado
    pela tela e pela estrutura selecionada.

## 6. Hipóteses principais para Fase 2

### H1 — Erro de strike no cadastro manual

Causa provável:

    UI envia strike vazio ou string inválida.
    Repositório tenta float(strike).
    Erro exibido: "strike must be numeric".

Correção candidata:

    Validar e normalizar strike antes de chamar o repositório.
    Tratar string vazia como obrigatório ausente.
    Melhorar mensagem de erro na UI.

### H2 — Tela não reflete payoff/decisão atualizados

Causa possível:

    Cálculo e persistência usam uma combinação de aba, timestamp e structure_id.
    UIDataModel pode estar lendo por outra chave ou snapshot anterior.

Correção candidata:

    Auditar leitura da UIDataModel contra escrita em DerivedRepo.
    Garantir chave canônica consistente.

### H3 — Inconsistência entre RTD, manual e rtd_option_quotes

Causa possível:

    O cálculo pode usar snapshot enriquecido,
    enquanto a UI pode exibir dados de outra origem.

Correção candidata:

    Evidenciar e testar política manual > rtd_option_quotes > rtd no fluxo completo.

## 7. Arquivos candidatos para Fase 2

### Strike/cadastro

    UI/components/structure_editor_dialog.py
    repositories/structures_repository.py
    validators/leg_validator.py
    validators/validators__init__.py

### Atualização de tela

    UI/main_window.py
    UI/models/ui_data.py
    UI/components/decisions_grid.py
    UI/components/details_panel.py
    UI/components/payoff_chart.py

### Payoff/decisão/persistência

    services/calculation_orchestrator.py
    domain/payoff.py
    domain/decision.py
    services/derived_service.py
    services/derived_payoff_persistence.py
    db/derived_repo.py

### RTD/snapshot

    repositories/market_snapshot_repository.py
    services/market_snapshot_selector.py
    repositories/rtd_option_quotes_repository.py
    services/structure_leg_rtd_enrichment_service.py

## 8. Conclusão

A Fase 1 mapeou o runtime atual sem alteração de código-fonte.

Achados centrais:

1. O erro "strike must be numeric" provavelmente nasce do envio de strike vazio
   ou string inválida pela UI para o repositório.
2. Payoff e decisão convergem em db/derived_repo.py,
   usando payoff_curve_points e structure_decisions.
3. A UI atualiza via MainWindow.refresh_data() e UIDataModel.refresh().
4. O fluxo RTD usa política manual > rtd_option_quotes > rtd.
5. A Fase 2 deve focar em correções pequenas, com testes e guardrails
   antes e depois.
