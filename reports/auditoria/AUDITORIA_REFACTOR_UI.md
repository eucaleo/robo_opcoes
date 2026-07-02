# Auditoria da Refatoração de UI

## 1. Objetivo

Controlar a evolução da refatoração de UI do projeto, garantindo que nenhuma alteração visual ou estrutural seja feita sem inventário prévio, teste acumulado e commit rastreável.

## 2. Escopo da fase atual

Fase atual:

- UI-1: Inventário e Auditoria Inicial

Objetivo da fase:

- Mapear arquivos relacionados à UI
- Mapear entrada da aplicação
- Mapear classes visuais
- Mapear controllers, services e repositories
- Mapear usos de banco
- Registrar riscos antes de qualquer alteração de layout

## 3. Regras explícitas do projeto

A) Não migrar para web.

B) Não utilizar emojis.

C) Manter-se ao escopo do projeto sem derivações.

D) Efetuar buscas de dados e arquivos antes de alterações.

E) Toda mudança deve ser testada após concluída.

F) Após o encerramento de fase, o teste deve compor todas as fases encerradas, sem pendências.

G) Evitar códigos intermediários em explicações, ir direto ao ponto.

H) Em alterações, sempre gerar código automatizado via Git Bash indentado.

I) A cada alteração concluída e testada, commitar.

J) Não codar sem rumo; se necessário, buscar a evolução no git.

K) Criar arquivo de auditoria para ser atualizado com os testes, conclusões e caminho de evolução.

L) Não gerar código com crase; manter comandos e scripts organizados e indentados.

M) Não manter sync contínuo: derived.db -> app.db.

N) Não manter app.db -> derived.db.

O) Não permitir dívida técnica; para cotação viva isso é risco operacional.

P) Após testes, a melhor resposta como arquitetura final é um único banco canônico para mercado vivo: app.db.

## 4. Baseline de segurança

Branch base:

- patch-side-actions-structures

Tag de segurança:

- baseline-pre-refatoracao-ui-layout-20260701

Status:

- Tag criada localmente e enviada ao remoto.

## 5. Inventário executado

Diretório:

- reports/ui_inventory

Arquivos gerados:

- 01_python_files.txt
- 02_ui_related_files.txt
- 03_ui_entrypoints.txt
- 04_ui_classes.txt
- 05_ui_actions_widgets.txt
- 06_ui_layout_navigation.txt
- 07_theme_styles.txt
- 08_controllers.txt
- 09_services.txt
- 10_repositories.txt
- 11_api_endpoints.txt
- 12_database_usage.txt
- 13_tests_all.txt
- 14_tests_names_sorted.txt

Contagem recebida:

- 179 arquivos Python
- 71 arquivos relacionados à UI, view, window, dialog, panel, widget, controller, viewmodel, terminal, payoff ou structure
- 553 ocorrências relacionadas a entrypoints/UI
- 27 classes relacionadas à UI
- 0 ocorrências em ações/widgets no grep inicial
- 0 ocorrências em layout/navegação no grep inicial
- 202 ocorrências relacionadas a tema/estilo/cor
- 6 controllers
- 45 services
- 19 repositories
- 61 ocorrências de API/endpoints
- 630 ocorrências de uso de banco
- 58 testes

## 6. Leitura técnica inicial

Conclusão 1:

- A UI existe, mas o grep inicial não encontrou widgets ou layouts tradicionais.
- Isso indica possível abstração, criação dinâmica, framework diferente ou padrões ainda não mapeados.

Conclusão 2:

- Existe volume relevante de estilo/tema, com 202 ocorrências.
- Antes de implementar layout novo, é necessário classificar onde tema e estilos são definidos.

Conclusão 3:

- A presença de controllers, services e repositories indica separação razoável de camadas.
- A nova UI deve consumir camadas existentes, sem recriar regra de negócio.

Conclusão 4:

- O uso de banco é crítico.
- Não será criado sync contínuo entre derived.db e app.db.
- O destino arquitetural para mercado vivo é app.db como banco canônico.

## 7. Riscos identificados

Risco 1:

- Alterar UI antes de mapear ações pode remover função operacional.

Mitigação:

- Mapear ações reais por chamadas, métodos e conexões antes da alteração.

Risco 2:

- Reativar dark mode sem entender o ponto de aplicação pode afetar componentes ou legibilidade.

Mitigação:

- Inventariar estilos, temas, palettes, colors e arquivos de stylesheet antes de aplicar tema.

Risco 3:

- Misturar refatoração de layout com mudança de banco pode gerar dívida técnica.

Mitigação:

- Separar fase de UI da fase de arquitetura de dados.

Risco 4:

- Manter derived.db e app.db sincronizados continuamente criaria risco operacional.

Mitigação:

- Não implementar sync contínuo em nenhuma direção.

## 8. Decisões arquiteturais registradas

Decisão 1:

- A aplicação continuará desktop.

Decisão 2:

- A nova UI será implementada sem migração web.

Decisão 3:

- A nova UI deve preservar as funções existentes.

Decisão 4:

- A nova UI não deve modificar regra de negócio.

Decisão 5:

- A arquitetura final para mercado vivo deve convergir para app.db como banco canônico único.

Decisão 6:

- derived.db não será mantido em sincronismo contínuo com app.db.

Decisão 7:

- app.db não será mantido em sincronismo contínuo com derived.db.

## 9. Testes da fase

Status atual:

- Inventário gerado.
- Auditoria criada.
- Nenhuma alteração funcional executada nesta etapa.

Teste obrigatório antes de encerrar UI-1:

- pytest

Teste manual recomendado:

- python run_ui.py

## 10. Pendências da fase UI-1

Pendência 1:

- Ler conteúdo dos principais inventários para montar a tabela mestre da UI atual.

Arquivos prioritários:

- reports/ui_inventory/02_ui_related_files.txt
- reports/ui_inventory/03_ui_entrypoints.txt
- reports/ui_inventory/04_ui_classes.txt
- reports/ui_inventory/07_theme_styles.txt
- reports/ui_inventory/08_controllers.txt
- reports/ui_inventory/09_services.txt
- reports/ui_inventory/10_repositories.txt
- reports/ui_inventory/12_database_usage.txt

Pendência 2:

- Descobrir por que os inventários de ações/widgets e layout/navegação vieram vazios.

Pendência 3:

- Gerar busca ampliada para métodos, comandos, callbacks, slots e chamadas indiretas.

Pendência 4:

- Montar tabela mestre:

Área | Tela/Componente | Arquivo | Classe | Ações | Dados usados | Serviço chamado | Risco | Destino no novo layout

## 11. Critério de fechamento da fase UI-1

A fase UI-1 somente poderá ser encerrada quando:

- A tabela mestre da UI atual estiver criada.
- As ações reais da UI estiverem mapeadas.
- Os pontos de entrada da UI estiverem identificados.
- O uso de tema/estilo estiver classificado.
- pytest estiver aprovado.
- python run_ui.py tiver sido executado com sucesso.
- O commit da fase tiver sido criado.

## 12. Busca complementar UI-1

Executada busca ampliada para localizar ações, callbacks, layout, framework de UI, classes arquiteturais, conexões de banco e termos de negócio.

Arquivos gerados:

- reports/ui_inventory_deep/01_actions_callbacks_deep.txt
- reports/ui_inventory_deep/02_layout_navigation_deep.txt
- reports/ui_inventory_deep/03_ui_framework_detection.txt
- reports/ui_inventory_deep/04_architecture_classes.txt
- reports/ui_inventory_deep/05_database_connection_points.txt
- reports/ui_inventory_deep/06_business_terms_deep.txt

Contagem:

  2130 reports/ui_inventory_deep/01_actions_callbacks_deep.txt
  1495 reports/ui_inventory_deep/02_layout_navigation_deep.txt
   118 reports/ui_inventory_deep/03_ui_framework_detection.txt
    56 reports/ui_inventory_deep/04_architecture_classes.txt
   574 reports/ui_inventory_deep/05_database_connection_points.txt
  5841 reports/ui_inventory_deep/06_business_terms_deep.txt
 10214 total

## 13. Diretriz de novo layout baseada no anexo AppFinanceiraVwap.py

Foi analisado o arquivo de referência visual:

- AppFinanceiraVwap.py

Este arquivo não será adotado como implementação funcional do sistema. Ele será usado apenas como referência de layout e interação.

### 13.1. Elementos aproveitáveis do anexo

Serão considerados como referência para a nova UI:

- Aplicação desktop em CustomTkinter
- Aparência escura
- Barra lateral fixa
- Painel lateral retrátil para seleção de estruturas
- Área principal ampliada para análise
- Bloco visual de VWAP
- Bloco visual de Payoff
- Rodapé com componentes/pernas da estrutura
- Fluxo operacional de seleção de estrutura e foco na análise

### 13.2. Elementos descartados do anexo

Serão descartados integralmente:

- Banco fictício ESTRUTURAS_DB
- Dados simulados de estruturas
- Dados simulados de VWAP
- Dados simulados de payoff
- Uso de np.random para geração de mercado
- Cálculos de negócio implementados diretamente na UI
- Qualquer regra operacional embutida na camada visual

### 13.3. Diretriz arquitetural

A nova UI não definirá a regra do sistema.

Decisão registrada:

- A UI não molda o sistema.
- O sistema molda a UI.
- A nova interface será apenas uma camada visual conectada às funcionalidades já existentes.
- A regra de negócio continuará nos controllers, services, repositories e contratos canônicos atuais.
- A UI deve apenas orquestrar seleção, exibição, acionamento e atualização visual.

### 13.4. Destino da nova tela operacional

O novo layout deverá conter, no mínimo:

- Menu lateral fixo
- Painel lateral retrátil de estruturas
- Painel principal de análise
- Área de VWAP
- Área de Payoff
- Área de pernas/componentes da estrutura
- Espaço para status operacional
- Espaço para mensagens de validação/erro
- Integração com dados reais do sistema

### 13.5. Conexões funcionais obrigatórias

A nova UI deverá se conectar às camadas existentes, sem duplicar lógica:

- Estruturas
- Pernas da estrutura
- Eventos de estrutura
- Payoff
- Terminal VWAP Payoff
- Precificação
- Snapshots de mercado
- RTD/mercado vivo quando aplicável
- Serviços e controllers já testados

### 13.6. Restrições para implementação

Durante a substituição da UI atual:

- Não migrar para web.
- Não criar regra de negócio dentro da UI.
- Não usar dados simulados como fonte operacional.
- Não manter sync contínuo entre derived.db e app.db.
- Não criar dívida técnica.
- Não remover funcionalidade sem mapeamento prévio.
- Não alterar banco junto com layout sem fase específica.
- Não substituir a UI atual antes de mapear seus pontos de entrada e ações reais.
- Não implementar componentes visuais sem conexão prevista com serviço/controller existente.

### 13.7. Situação quanto à prontidão para alteração de UI

Status atual:

- Já existe inventário inicial.
- Já existe busca complementar.
- Testes automatizados passaram.
- A UI atual executou com sucesso via run_ui.py.
- O layout-alvo já possui referência visual.
- Ainda falta consolidar a tabela mestre da UI atual antes da eliminação da UI existente.

Conclusão:

- Há dados suficientes para desenhar o layout-alvo e planejar a substituição.
- Ainda não há segurança completa para eliminar a UI atual sem antes consolidar os pontos de entrada, componentes, ações e conexões reais.
- A próxima etapa deve ser a tabela mestre da UI atual e o plano de substituição por fases.

