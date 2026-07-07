# Checklist de smoke Payoff UI

Data de geracao:

    2026-07-06 22:18:40

Branch:

    audit/payoff-ui

Commit de referencia:

    29ea375

Status:

    CHECKLIST_SMOKE_DOCUMENTAL

## 1. Objetivo

Definir uma validacao manual minima e reproduzivel para a area Payoff UI antes de qualquer alteracao funcional.

Esta etapa nao executa patch em codigo de produto.

## 2. Escopo permitido nesta etapa

- Revisar abertura da tela ou painel Payoff.
- Observar renderizacao inicial da curva ou area grafica.
- Observar mensagens de erro visiveis na interface.
- Verificar se a tela permanece responsiva durante abertura e atualizacao.
- Registrar evidencias textuais no documento de smoke.

## 3. Fora do escopo nesta etapa

- Alterar controller.
- Alterar services.
- Alterar domain.
- Alterar banco ou migration.
- Alterar regra de calculo de payoff.
- Corrigir comportamento sem falha reproduzivel.

## 4. Arquivos de UI observados

- UI/components/payoff_chart.py
- UI/components/terminal_vwap_payoff_dark_panel.py
- UI/components/terminal_vwap_payoff_panel.py

## 5. Testes relacionados para referencia

- ATT/tests/test_payoff_canonical.py
- ATT/tests/test_payoff_chart.py
- ATT/tests/test_terminal_vwap_payoff_app_service.py
- ATT/tests/test_terminal_vwap_payoff_controller.py
- ATT/tests/test_terminal_vwap_payoff_panel.py
- ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py

## 6. Arquivos de suporte somente para leitura

- controllers/terminal_vwap_payoff_controller.py
- services/terminal_vwap_payoff_app_service.py
- services/terminal_vwap_payoff_viewmodel_service.py
- domain/payoff.py
- domain/payoff_features.py

## 7. Checklist manual proposto

### 7.1. Preparacao

- Confirmar branch audit/payoff-ui.
- Confirmar arvore limpa antes do smoke.
- Abrir a aplicacao pelo mesmo caminho usado nos registros anteriores do projeto.
- Nao aplicar alteracao manual em codigo durante o smoke.

### 7.2. Abertura da area Payoff

- Acessar a tela ou painel que exibe Payoff.
- Confirmar que a abertura nao encerra a aplicacao.
- Confirmar que nao aparece traceback no terminal.
- Confirmar que componentes principais ficam visiveis.

### 7.3. Renderizacao visual

- Confirmar que a area grafica ou componente de curva aparece.
- Confirmar que nao ha sobreposicao evidente que impeça leitura.
- Confirmar que textos basicos, valores ou labels visiveis nao ficam cortados de forma critica.
- Confirmar que o tema visual esperado nao quebra contraste basico.

### 7.4. Interacao minima

- Acionar controles disponiveis do painel Payoff, se existirem.
- Confirmar que a interface nao congela.
- Confirmar que mudancas visuais esperadas ocorrem ou que a ausencia delas e registrada.
- Confirmar que erros exibidos sejam anotados com texto exato.

### 7.5. Encerramento

- Fechar a tela ou aplicacao pelo fluxo normal.
- Confirmar que nao restaram processos ou erros visiveis no terminal.
- Registrar resultado como aprovado, reprovado ou inconclusivo.

## 8. Criterios de aprovacao

O smoke pode ser considerado aprovado se:

- A area Payoff abre sem derrubar a aplicacao.
- Nao ha traceback durante abertura e interacao minima.
- A area principal de Payoff e renderizada.
- A interface permanece responsiva.
- Nenhuma falha bloqueante e observada.

## 9. Criterios de reprovacao

O smoke deve ser considerado reprovado se:

- A aplicacao encerra durante abertura do Payoff.
- O terminal exibe traceback relacionado ao Payoff.
- O painel nao renderiza.
- A interface congela.
- Ha erro visual bloqueante que impede validar a tela.

## 10. Evidencia minima esperada

Para cada execucao, registrar:

- Data e horario.
- Branch.
- Commit.
- Caminho usado para abrir a aplicacao.
- Resultado observado.
- Erro textual, se houver.
- Decisao: aprovado, reprovado ou inconclusivo.

## 11. Decisao

A frente permanece documental.

O proximo passo recomendado e executar o smoke manual e preencher docs/REGISTRO_EXECUCAO_SMOKE_PAYOFF_UI.md.

Resultado desta etapa:

    CHECKLIST_SMOKE_PAYOFF_UI_GERADO_SEM_PATCH_FUNCIONAL

<!-- SMOKE_PAYOFF_UI_MODERNA_2026_07_07 -->

## Diretriz obrigatoria para execucao do smoke

O smoke Payoff UI desta frente deve ser executado na UI moderna.

Comando autorizado:

    python -m UI.modern

O comando run_ui.py nao deve ser usado como smoke principal desta frente, pois abre a UI antiga.

A UI antiga fica congelada para desenvolvimento evolutivo nesta frente. Ela pode ser consultada apenas como referencia visual ou historica, sem receber correcao como alvo principal.

Itens obrigatorios do smoke na UI moderna:

- abrir a UI moderna por python -m UI.modern;
- confirmar que a janela moderna abre sem erro fatal;
- localizar o acesso a Payoff ou Terminal VWAP Payoff na UI moderna;
- validar se a area de Payoff esta visivel;
- validar comportamento sem estrutura selecionada;
- validar carregamento de estrutura ou decisao quando disponivel;
- validar carregamento da curva de payoff quando disponivel;
- validar mensagens de status;
- registrar qualquer erro no terminal;
- registrar lacunas visiveis da UI moderna;
- nao declarar aprovado com base na UI antiga.

Resultado esperado:

Aprovacao, reprovacao ou aprovacao parcial devem refletir somente a UI moderna.
