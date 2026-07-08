# M12 - Testes de contrato e cobertura Terminal VWAP UI-only

## 1. Objetivo

Esta fase adiciona testes automatizados para confirmar se as alterações esperadas da frente Terminal VWAP estão realmente presentes no main.

A M12 foi criada para evitar falso encerramento documental.

Ela verifica, por teste executável, que:

- a infraestrutura consolidada da M9 existe;
- os testes de wiring do Terminal VWAP continuam presentes;
- os cenários de idempotência continuam protegidos;
- o painel Terminal VWAP continua defensivo contra ViewModels vazios ou malformados;
- M9 não é tratada como fechamento funcional completo;
- M10 e M11 permanecem corretamente classificadas como fases documentais;
- a validação assistida funcional permanece pendente para etapa posterior.

## 2. Escopo

Escopo permitido nesta fase:

- testes automatizados;
- contrato de cobertura;
- verificação de presença de helpers, fakes e testes essenciais;
- comportamento defensivo de helpers do painel Terminal VWAP;
- documentação da evidência.

Escopo proibido nesta fase:

- banco de dados;
- schema;
- pipeline;
- payoff;
- regras de negócio;
- services;
- repositories;
- controllers;
- alteração funcional ampla;
- reclassificação documental sem teste.

## 3. Arquivo de teste criado

Foi criado o arquivo:

- ATT/tests/test_terminal_vwap_m12_contract_coverage.py

## 4. Verificações implementadas

| Item | Verificação |
|---|---|
| Infraestrutura M9 | Confirma presença de FakeUIDataModel |
| Infraestrutura M9 | Confirma presença de patch_window_dependencies |
| Idempotência | Confirma presença do teste de decisão já selecionada |
| Idempotência | Confirma presença do teste de estrutura ausente preservando seleção válida |
| M9 | Confirma que M9 não é fechamento funcional completo |
| M10 | Confirma que a reconciliação mantém itens funcionais abertos |
| M11 | Confirma que M11 é roteiro documental, não execução funcional |
| Painel Terminal VWAP | Confirma tolerância a ViewModel malformado |
| Painel Terminal VWAP | Confirma defaults seguros para ViewModel vazio |
| Cobertura mínima | Confirma termos críticos no wiring |

Termos críticos verificados no wiring:

- missing_structure
- idempotent
- invalid
- zero
- selection
- load_structure

## 5. Execução realizada

### 5.1. Teste M12 isolado

Comando executado:

    python -m pytest ATT/tests/test_terminal_vwap_m12_contract_coverage.py -q

Resultado observado:

    6 passed in 0.12s

Conclusão:

    APROVADO

### 5.2. Pacote relacionado ao Terminal VWAP

Comando executado:

    python -m pytest \
      ATT/tests/test_terminal_vwap_m12_contract_coverage.py \
      ATT/tests/test_terminal_vwap_payoff_panel_helpers.py \
      ATT/tests/test_terminal_vwap_payoff_panel_rendering.py \
      ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py \
      -q

Resultado observado:

    44 passed in 0.47s

Conclusão:

    APROVADO

### 5.3. Suite ATT completa

Comando executado:

    python -m pytest ATT/tests -q

Resultado observado:

    730 passed, 2 skipped, 6 subtests passed in 38.00s

Conclusão:

    APROVADO

## 6. Conclusão da M12

A M12 foi concluída com sucesso.

Diferentemente de M10 e M11, esta fase produziu evidência automatizada executável.

A partir desta fase, fica comprovado por teste que:

- a infraestrutura esperada da M9 está presente;
- os testes de wiring Terminal VWAP continuam protegendo cenários críticos;
- o painel Terminal VWAP mantém comportamento defensivo em helpers;
- a documentação M10 e M11 não está declarando falso fechamento funcional;
- a validação funcional assistida ainda deve ser executada em fase posterior.

## 7. Decisão

Status da M12:

    CONCLUÍDA COM TESTES AUTOMATIZADOS APROVADOS

Próxima frente recomendada:

    M13 - execução assistida do roteiro M11-01 a M11-14 com registro de evidências

A M13 deverá observar a UI em execução e preencher a matriz de validação assistida.

