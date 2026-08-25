# Registro de encerramento da etapa 1

Gerado em: 2026-08-07T20:53:56

## Objetivo

Registrar o encerramento operacional da primeira etapa de contenção, estabilização e migração incremental do projeto.

Este documento consolida o estado até a Frente 76m, para permitir registro no Git sem incluir artefatos transitórios da pasta ATT.

## Escopo consolidado

A etapa consolidada cobre as frentes documentadas de 01 até 76m, incluindo:

- caminho canônico do banco em dados/app.db;
- schema mínimo e contratos de tabelas derivadas;
- contenção de db.reader e db.writer;
- transição controlada de aba para structure_id;
- contratos financeiros de legs, multiplier, premium, current_price e gregas;
- contrato RTD Option Quotes;
- parsers canônicos de número e data;
- envelope de pricing;
- redução incremental de SQL direto fora de repositories, db e infra;
- boundaries locais para services e UI;
- estabilização do Terminal VWAP Payoff Dark Panel;
- ponte de persistência de decisão via DecisionRepository;
- endpoint oficial insert_decision;
- guardrail da Frente 76m para manter patches e temporários em ATT e impedir rota tools para apply_frente_76.

## Validações finais informadas

Validação isolada da Frente 76m:

    pytest -q ATT/tests/test_frente_76m_development_route_att_only.py

Resultado:

    5 passed

Validação integrada da sequência 76b até 76m:

    pytest -q ATT/tests/test_frente_76b_terminal_vwap_payoff_dark_panel_operational_inventory.py ATT/tests/test_frente_76h_terminal_vwap_payoff_dark_panel_decision_registration_persistence_evidence.py ATT/tests/test_frente_76i_terminal_vwap_payoff_dark_panel_decision_repository_bridge.py ATT/tests/test_frente_76j_terminal_vwap_payoff_dark_panel_decision_persistence_order.py ATT/tests/test_frente_76k_terminal_vwap_payoff_dark_panel_decision_repository_write_contract.py ATT/tests/test_frente_76l_decision_repository_official_write_endpoint.py ATT/tests/test_frente_76m_development_route_att_only.py ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py

Resultado:

    61 passed

## Regras de Git para este encerramento

- Considerar arquivos deletados como deletados.
- Não incluir ATT nem subpastas de ATT no Git.
- Não incluir backups locais com sufixo bak.
- Não incluir documentos antigos de backup.
- Incluir documentos permanentes em docs.
- Incluir novos módulos permanentes criados fora de ATT, quando forem parte do código operacional, repositories, services, db, utils, infra, scripts ou UI.
- Preservar sistema local, sem Web, sem HTTP e sem API externa.
- Não alterar schema fora do que já foi validado pelas frentes.
- Não executar comandos de Git por patch automatizado.

## Normalizações aplicadas

- Renomeado docs/FRENTES_CORRIGIDAS_PARTE_2 .md para docs/FRENTES_CORRIGIDAS_PARTE_2.md

## Arquivos auxiliares permanentes gerados nesta etapa

- docs/REGISTRO_ENCERRAMENTO_ETAPA_1.md
- docs/MANIFESTO_GIT_ETAPA_1.md
- scripts/stage_etapa_1_git.sh

## Próxima etapa após o registro

Após o commit desta etapa, a próxima frente técnica pode seguir como 76n ou como novo precheck local, mantendo o mesmo padrão:

- uma frente pequena por vez;
- patch, teste e relatório em ATT;
- documentação permanente em docs;
- sem Web, HTTP ou API externa;
- sem alteração ampla de schema;
- sem git até fechamento da próxima etapa.
