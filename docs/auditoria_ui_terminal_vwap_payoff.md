# Auditoria — UI Terminal VWAP Payoff

## 1. Objetivo da auditoria

Registrar a evolução do projeto UI Terminal VWAP Payoff, mantendo histórico de:

- decisões técnicas;
- buscas realizadas antes de alterações;
- testes executados;
- arquivos alterados;
- evidências de funcionamento;
- pendências;
- riscos identificados;
- critérios de aceite por fase;
- impacto ou ausência de impacto no sistema existente.

## 2. Regras de auditoria

- Toda fase encerrada deve atualizar este arquivo.
- Toda alteração concluída e testada deve ser commitada.
- Testes da fase atual devem incluir testes das fases anteriores.
- Nenhuma conclusão deve ser registrada sem teste correspondente.
- A auditoria deve indicar se houve ou não impacto no sistema existente.
- Antes de alterar arquivos, devem ser registradas as buscas realizadas.
- A UI não deve depender de CSVs derivados antigos.
- O banco de dados permanece como fonte da verdade.
- O Excel permanece apenas como ponte RTD.

## 3. Estado inicial conhecido

Branch de trabalho principal:

    feature/ui-terminal-vwap-payoff

Branch de experimentação visual:

    spike/ui-terminal-vwap-payoff

Branch main publicada no origin:

    Sim, conforme interação registrada.

Commits publicados na main antes deste projeto:

    5826883 fix(editor): normalize strike decimal in legs payload
    34bc73c docs(checkpoints): add fase 2a strike investigation evidence

Observação:

A branch feature/ui-terminal-vwap-payoff já existe localmente. Não deve ser criada novamente sem necessidade.

## 4. Fonte RTD validada documentalmente

Arquivo de referência:

    LISTA RTD FUNCOES.pdf

Arquivo Excel informado como ponte:

    LISTA_RTD.xlsm

Campo VWAP confirmado documentalmente:

    =RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")

Status:

    Confirmado documentalmente.
    Pendente teste prático de leitura pelo sistema.

## 5. Checklist permanente antes de alterações

Antes de qualquer alteração funcional, verificar:

    Branch atual
    Status do Git
    Histórico recente
    Arquivos relacionados a estrutura
    Arquivos relacionados a payoff
    Arquivos relacionados a snapshot
    Arquivos relacionados a RTD
    Arquivos relacionados a ViewModel
    Arquivos relacionados a UI
    Arquivos relacionados a CSV
    Testes existentes

Resultado da checagem inicial:

    Pendente execução local.

## 6. Fase 0 — Preparação, busca e proteção contra regressão

### Objetivo

Garantir que a base está íntegra antes de iniciar o terminal.

### Ações previstas

- verificar branch;
- verificar git status;
- verificar histórico recente;
- localizar serviços existentes de estrutura, payoff, snapshot e RTD;
- localizar ViewModels existentes;
- localizar dependências de CSV;
- executar testes atuais;
- registrar arquivos candidatos à alteração.

### Buscas executadas

    Pendente.

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Pendências

    Pendente.

### Decisão

    Pendente.

## 7. Fase 1 — Documentação base

### Objetivo

Criar documentação inicial do projeto e auditoria.

### Arquivos previstos

    docs/ui_terminal_vwap_payoff_plano.md
    docs/auditoria_ui_terminal_vwap_payoff.md

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 8. Fase 2 — Spike visual isolado

### Objetivo

Criar protótipos executáveis sem dados reais para escolha do layout.

### Regras da fase

- não acessar banco;
- não acessar RTD;
- não acessar CSV;
- não importar módulos reais do sistema;
- usar somente dados mockados;
- não criar regra financeira definitiva.

### Modelos previstos

    Modelo A — lateral operacional
    Modelo B — dashboard executivo
    Modelo C — modo foco com abas

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão visual

    Pendente.

## 9. Fase 3 — Escolha do layout base

### Objetivo

Registrar o layout escolhido antes da integração real.

### Recomendação inicial

    Base: Modelo A
    Evolução interna: Modelo C

### Critérios de avaliação

- clareza visual;
- conforto em tela cheia;
- capacidade de exibir tabela de pernas;
- capacidade de crescer com abas;
- separação entre preço, VWAP, PL e payoff;
- preservação da arquitetura atual.

### Resultado

    Pendente.

### Decisão

    Pendente.

## 10. Fase 4 — Contrato do ViewModel

### Objetivo

Definir contrato entre sistema e terminal.

### Campos previstos

    structure_id
    nome_estrutura
    ativo_base
    preco_atual
    vwap
    diferenca_preco_vwap_percentual
    variacao_percentual
    volume
    status_rtd
    fonte_rtd
    horario_cotacao
    payoff_curve_x
    payoff_curve_y
    preco_base_atual
    payoff_no_preco_atual
    pl_atual
    snapshot_implantacao
    snapshot_atual
    pernas
    mensagens

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 11. Fase 5 — Integração com estruturas reais

### Objetivo

Listar e carregar estruturas reais por structure_id.

### Validações obrigatórias

- estrutura real é listada;
- structure_id correto é carregado;
- pernas não se misturam;
- dados vêm do sistema;
- CSV antigo não é utilizado;
- UI não acessa banco diretamente.

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 12. Fase 6 — Prova isolada do RTD VWAP

### Objetivo

Ler QUOTE.VWAP via RTD.

### Campo confirmado

    =RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")

### Cuidados obrigatórios

- valor vazio;
- valor None;
- erro de RTD;
- Excel fechado;
- RTD inicializando;
- ativo sem VWAP;
- separador decimal brasileiro;
- separador decimal americano;
- atraso de atualização.

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 13. Fase 7 — Integração da VWAP no snapshot atual

### Objetivo

Incluir VWAP no snapshot de mercado sem substituir preço atual.

### Campos previstos

    structure_id
    ativo_base
    preco_atual
    bid
    ask
    vwap
    volume
    variacao_percentual
    status
    fonte_preco
    fonte_vwap
    capturado_em

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 14. Fase 8 — Payoff real no terminal

### Objetivo

Exibir payoff calculado pelo sistema.

### Validações obrigatórias

- payoff vem do ViewModel real;
- UI não recalcula payoff oficial;
- gráfico exibe curva recebida;
- preço atual e VWAP aparecem destacados;
- PL atual e payoff no vencimento aparecem separados;
- resultado bate com serviço atual.

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 15. Fase 9 — Tabela analítica por perna

### Objetivo

Exibir pernas reais com dados analíticos.

### Campos previstos

    numero_perna
    ticker
    tipo
    direcao
    quantidade
    strike
    vencimento
    premio_entrada
    preco_atual
    bid
    ask
    intrinseco
    extrinseco
    delta
    theta
    vega
    pl_atual
    payoff_no_vencimento_ao_preco_atual
    fonte
    status

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 16. Fase 10 — Refresh controlado

### Objetivo

Atualizar dados sem travar a interface.

### Validações obrigatórias

- refresh manual funcional;
- refresh automático opcional;
- sem loop bloqueante;
- sem concorrência de refresh;
- último horário de atualização exibido;
- falha de RTD não encerra aplicação.

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 17. Fase 11 — Validação integrada

### Objetivo

Validar todas as fases encerradas.

### Testes mínimos

    Testes antigos continuam passando
    Estruturas reais são listadas
    structure_id correto é carregado
    Pernas corretas são exibidas
    VWAP é lida quando disponível
    Ausência de VWAP é tratada
    Payoff vem do sistema
    UI não usa CSV antigo
    UI não cria estrutura
    UI não altera banco indevidamente
    Refresh não trava
    Auditoria documenta resultado

### Testes executados

    Pendente.

### Resultado

    Pendente.

### Arquivos alterados

    Pendente.

### Decisão

    Pendente.

## 18. Registro de commits do projeto

### Commit 1

    Pendente.

### Commit 2

    Pendente.

### Commit 3

    Pendente.

## 19. Pendências abertas

    Executar checagem local do Git.
    Executar busca de arquivos relevantes.
    Executar testes atuais.
    Criar documentação inicial.
    Commitar documentação inicial.
    Iniciar spike visual isolado.

## 20. Decisão atual

O projeto está aprovado como próxima evolução, desde que siga a regra central:

O terminal será uma camada visual local sobre o sistema existente.

Não haverá:

- migração web;
- regressão do sistema;
- cálculo financeiro paralelo na UI;
- dependência de CSV antigo;
- substituição do banco como fonte da verdade;
- substituição do Excel como ponte RTD.

## Registro de verificação local RTD

Verificação registrada para a branch feature/ui-terminal-vwap-payoff.

Estado observado:

    LISTA_RTD.xlsx aparece como deletado no Git, mas é arquivo legado.
    LISTA_RTD.xlsm aparece como arquivo operacional vigente da ponte RTD com macros.
    OPERACOES_E_OPCOES.xlsm aparece como deletado no Git e exige decisão separada.
    Os documentos do terminal VWAP Payoff foram criados em docs.
    Os documentos foram convertidos de txt para md.
    Os documentos não possuem blocos com crase.

Decisões registradas:

    Não restaurar LISTA_RTD.xlsx.
    Não tratar LISTA_RTD.xlsx como ponte RTD vigente.
    Preservar LISTA_RTD.xlsm como evolução consolidada.
    Não fazer restauração antes de verificações locais.
    Não usar buscas profundas no histórico para reintroduzir arquivos ou padrões legados.
    Não incluir alterações de Excel no mesmo commit de documentação.
    Não incluir reports, spikes ou scripts locais no commit de documentação.

Comandos proibidos nesta etapa:

    git restore LISTA_RTD.xlsx
    git reset --hard
    git clean -fd
    git add -A

Critério de segurança:

    Qualquer modificação em documentos ou arquivos deve ser feita por script Git Bash local, com verificações antes da escrita.

## Registro de andamento — Incremento 2 do Terminal VWAP Payoff

Marcador: AUDITORIA_INCREMENTO_2_TERMINAL_VWAP_PAYOFF_594057f

Data de registro:

    2026-06-29 09:47:54 -0300

Branch verificada:

    feature/ui-terminal-vwap-payoff

Commit funcional registrado:

    594057f feat(ui): adiciona app service do terminal vwap payoff

Histórico recente observado:

    594057f (HEAD -> feature/ui-terminal-vwap-payoff) feat(ui): adiciona app service do terminal vwap payoff
    37e915f feat(ui): adiciona viewmodel do terminal vwap payoff
    4610f38 docs: registra premissas rtd do terminal vwap payoff
    30dbc6c docs: adiciona plano e auditoria do terminal vwap payoff
    34bc73c (origin/main, spike/ui-terminal-vwap-payoff, main) docs(checkpoints): add fase 2a strike investigation evidence

Evidência do último commit:

    594057f feat(ui): adiciona app service do terminal vwap payoff
    ATT/tests/test_terminal_vwap_payoff_app_service.py
    services/terminal_vwap_payoff_app_service.py

Arquivos incluídos no Incremento 2:

    ATT/tests/test_terminal_vwap_payoff_app_service.py
    services/terminal_vwap_payoff_app_service.py

Testes executados:

    Comando: python -m pytest ATT/tests/test_terminal_vwap_payoff*.py
    Resultado: ============================== 7 passed in 0.17s ==============================

Resultado:

    Incremento 2 concluído, testado e commitado.
    App service do Terminal VWAP Payoff adicionado.
    Testes acumulados do terminal executados com sucesso.
    Arquivos sensíveis permaneceram fora do commit funcional.

Impacto no sistema existente:

    Sem alteração intencional em arquivos Excel.
    Sem inclusão de reports, spikes ou scripts locais.
    Sem uso de git add -A.
    Banco permanece como fonte da verdade.
    Excel permanece apenas como ponte RTD.
    UI permanece como camada consumidora de serviços/ViewModels.

Arquivos sensíveis observados fora do commit funcional:

    LISTA_RTD.xlsx
    LISTA_RTD.xlsm
    OPERACOES_E_OPCOES.xlsm

Decisão:

    Registrar o Incremento 2 como evolução válida da Fase 7.
    Prosseguir para os próximos incrementos mantendo commits pequenos, testados e auditados.

## Registro de correção de rota — remoção de risco REST/API indevido

Data de registro:

    2026-06-29 10:57:22 -0300

Branch verificada:

    feature/ui-terminal-vwap-payoff

Contexto:

    Foi identificada a necessidade de garantir que o Terminal VWAP Payoff permanecesse dentro do escopo local previsto no plano.
    O terminal não deve ser migrado para web, não deve expor endpoint REST/API próprio e não deve alterar a arquitetura do sistema atual.

Verificação realizada:

    api/terminal_vwap_payoff_controller.py ausente.
    main.py sem referência ao terminal.
    controllers/terminal_vwap_payoff_controller.py sem indício de FastAPI, APIRouter, HTTPException, TestClient, include_router ou rota REST.
    ATT/tests/test_terminal_vwap_payoff_controller.py sem indício de FastAPI, APIRouter, HTTPException, TestClient, include_router ou rota REST.

Resultado da auditoria final:

    Nenhum resíduo REST/API crítico detectado nos arquivos alvo.

Testes executados:

    Comando:
        python -m pytest ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py ATT/tests/test_terminal_vwap_payoff_app_service.py ATT/tests/test_terminal_vwap_payoff_controller.py

    Resultado:
        19 passed

Decisão:

    O desenvolvimento deve prosseguir no trilho local.
    O controller do terminal permanece permitido apenas como controller local de orquestração.
    Não deve ser criado endpoint REST/API para o Terminal VWAP Payoff nesta etapa.
    main.py não deve incluir router do terminal.
    A UI deve continuar consumindo ViewModels, controllers locais ou serviços do sistema.
    Banco permanece como fonte da verdade.
    Excel permanece apenas como ponte RTD.
    LISTA_RTD.xlsx permanece tratado como legado e não deve ser restaurado.

Arquivos sensíveis observados fora do escopo deste registro:

    LISTA_RTD.xlsx
    LISTA_RTD.xlsm
    OPERACOES_E_OPCOES.xlsm

Observação:

    Alterações de Excel, reports, spikes e scripts locais não fazem parte deste registro documental.

## Registro de auditoria — Integração UI principal, saneamento operacional e publicação remota

Marcador: REGISTRO_UI_PRINCIPAL_TERMINAL_VWAP_PAYOFF_434fd1e

Data de registro:

    2026-06-29 12:49:38 -0300

Branch verificada:

    feature/ui-terminal-vwap-payoff

Contexto:

    Foi concluída a integração do Terminal VWAP Payoff na UI principal.
    A alteração respeitou a arquitetura definida para o projeto, mantendo o terminal como camada visual local.
    Também foi realizado saneamento de arquivos operacionais e legados para evitar regressão e ruído permanente no Git.

Histórico recente observado:

    434fd1e chore: ignora arquivos operacionais locais
    4f2fe3f chore: remove planilhas legadas do sistema
    fb1b5d8 feat(ui): integra terminal VWAP payoff na UI principal

Commits registrados nesta etapa:

    fb1b5d8 feat(ui): integra terminal VWAP payoff na UI principal

        Arquivos:
            ATT/tests/test_terminal_vwap_payoff_panel.py
            UI/components/terminal_vwap_payoff_panel.py
            UI/main_window.py
            services/terminal_vwap_payoff_app_service.py

        Resultado:
            Painel local do terminal integrado à UI principal.
            Testes do painel adicionados.
            Integração preservou o consumo por serviços, controller local e ViewModel.

    4f2fe3f chore: remove planilhas legadas do sistema

        Arquivos removidos:
            LISTA_RTD.xlsx
            OPERACOES_E_OPCOES.xlsm

        Resultado:
            Remoção intencional dos arquivos que não pertencem mais ao sistema atualizado.
            LISTA_RTD.xlsx permanece classificado como legado e não deve ser restaurado.

    434fd1e chore: ignora arquivos operacionais locais

        Arquivo alterado:
            .gitignore

        Arquivos e pastas ignorados:
            LISTA_RTD.xlsm
            _local_scripts_fase7/
            reports/
            spikes/

        Resultado:
            LISTA_RTD.xlsm permanece como ponte RTD operacional local, sem versionamento.
            Artefatos locais, relatórios e spikes deixam de aparecer como pendências no Git.

Verificações executadas:

    Branch confirmada:
        feature/ui-terminal-vwap-payoff

    Status após saneamento:
        Working tree limpo.

    Push remoto:
        Branch publicada em origin/feature/ui-terminal-vwap-payoff.

Validação específica do terminal executada:

    Comando:
        python -m pytest ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py ATT/tests/test_terminal_vwap_payoff_app_service.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_panel.py

    Resultado:
        24 passed in 0.29s

Validação de compilação executada:

    Comando:
        python -m py_compile UI/components/terminal_vwap_payoff_panel.py UI/main_window.py services/terminal_vwap_payoff_app_service.py controllers/terminal_vwap_payoff_controller.py

    Resultado:
        Sem erro reportado.

Validação integrada geral executada:

    Comando:
        python -m pytest

    Resultado:
        651 passed, 2 skipped in 35.48s

Impacto no sistema existente:

    Testes gerais continuam passando.
    Não houve restauração de LISTA_RTD.xlsx.
    Não houve inclusão de arquivo Excel operacional no commit funcional.
    Não houve uso de git add -A.
    Não houve migração web.
    Não houve criação de endpoint REST/API específico para o terminal.
    Não houve dependência nova de CSV derivado antigo.
    Não houve acesso direto da UI ao banco.
    Não houve acesso direto da UI ao RTD bruto.
    Não houve cálculo financeiro oficial implementado dentro da UI.

Decisão sobre arquivos sensíveis:

    LISTA_RTD.xlsx:
        Arquivo legado removido intencionalmente.
        Não deve ser restaurado.

    LISTA_RTD.xlsm:
        Arquivo operacional vigente da ponte RTD.
        Deve permanecer local e ignorado pelo Git, pois sofre alterações constantes durante consultas RTD.

    OPERACOES_E_OPCOES.xlsm:
        Arquivo removido intencionalmente por não pertencer mais ao sistema atualizado.

Regras preservadas:

    Banco de dados permanece como fonte da verdade.
    Excel permanece apenas como ponte RTD.
    UI permanece como camada de apresentação.
    Terminal permanece local.
    Controller permanece local, sem API REST.
    Cálculos permanecem nos serviços do sistema.
    Structure_id permanece como referência central.
    Testes acumulados foram executados.
    Alterações concluídas foram commitadas.
    Branch foi publicada no remoto.

Posição atual revisada:

    A etapa de integração do Terminal VWAP Payoff na UI principal está concluída.
    A branch feature/ui-terminal-vwap-payoff está publicada no remoto.
    O repositório local estava limpo após os commits.
    A suíte completa foi executada com sucesso.
    O projeto está apto para pull request ou continuidade para a próxima etapa planejada.

Pendências atualizadas:

    Abrir pull request da branch feature/ui-terminal-vwap-payoff, se essa for a estratégia de integração.
    Revisar visualmente a tela em execução local.
    Definir próxima evolução após aprovação da integração principal.
    Manter LISTA_RTD.xlsm fora do versionamento.
    Não restaurar LISTA_RTD.xlsx.

