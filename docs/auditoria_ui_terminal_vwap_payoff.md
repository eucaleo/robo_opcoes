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
