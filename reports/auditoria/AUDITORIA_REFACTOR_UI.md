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


## 14. Auditoria visual da UI atual com base nos prints

Foram analisados prints da interface atual antes da substituição do layout.

Esta análise visual foi adicionada aos relatórios:

- reports/ui_visual_audit/01_prints_visual_controls.md
- reports/ui_visual_audit/02_code_concordance_visual_terms.txt
- reports/ui_visual_audit/03_menus.txt
- reports/ui_visual_audit/03_buttons.txt
- reports/ui_visual_audit/03_combos.txt
- reports/ui_visual_audit/03_tabs_notebooks.txt
- reports/ui_visual_audit/03_tables.txt
- reports/ui_visual_audit/03_bindings.txt
- reports/ui_visual_audit/03_matplotlib.txt
- reports/ui_visual_audit/03_services_controllers.txt

### 14.1. Controles visuais identificados

A UI atual contém os seguintes blocos funcionais:

- Menu superior:
  - Arquivo
  - Ferramentas
  - Ajuda

- Painel de filtros:
  - Período De/Até
  - Estrutura
  - Decisão
  - Level >=
  - DTE <=
  - Aplicar
  - Limpar
  - Indicador de filtros aplicados

- Tabela de decisões:
  - Data/Hora
  - Estrutura
  - Decisão
  - Nível
  - Ratio %
  - DTE
  - PL Atual
  - PL Máx

- Abas principais:
  - Detalhes da Decisão
  - Curva de Payoff
  - Estruturas
  - Terminal VWAP Payoff

- Ações de payoff:
  - Limpar Comparação
  - Fixar Curva A
  - Exportar PNG
  - Interações padrão da toolbar Matplotlib

- Ações de estruturas:
  - + Nova
  - Editar
  - Duplicar
  - Arquivar
  - Filtro por status
  - Busca

- Ações do Terminal VWAP Payoff:
  - Atualizar
  - Carregar
  - Subabas Resumo, Legs, Payoff e Avisos

- Ação operacional:
  - Recalcular esta estrutura

### 14.2. Diretriz de preservação funcional

A substituição visual não poderá remover implicitamente:

- filtros de decisões
- seleção de decisões
- detalhamento de decisão
- rationale/why JSON
- recalcular estrutura
- curva de payoff
- comparação por Curva A
- exportação PNG
- CRUD/arquivamento de estruturas
- terminal VWAP Payoff
- resumo de VWAP
- legs
- payoff
- avisos
- mensagens de status

Qualquer remoção deve ser decisão explícita, documentada e testada.

### 14.3. Relação com o novo layout

O layout de referência AppFinanceiraVwap.py continua sendo apenas referência visual.

Elementos aproveitáveis:

- barra lateral fixa
- painel retrátil de estruturas
- área principal de análise
- blocos para VWAP e Payoff
- rodapé/tabela de pernas
- foco operacional após seleção de estrutura

Elementos proibidos na implementação real:

- banco fictício
- simulação de mercado
- simulação de payoff
- cálculo de regra de negócio dentro da UI
- fonte operacional fora dos services/controllers existentes

### 14.4. Próxima etapa autorizada

Após conferência dos relatórios de auditoria visual, a próxima etapa poderá ser a preparação do novo shell visual em paralelo.

A UI atual ainda não deve ser eliminada diretamente.

Sequência recomendada:

1. Criar novo layout em paralelo.
2. Conectar painel de estruturas aos services/controllers existentes.
3. Conectar painel de payoff aos contratos existentes.
4. Conectar painel VWAP/Terminal aos services existentes.
5. Preservar filtros e tabela de decisões ou realocá-los no novo layout.
6. Validar manualmente.
7. Rodar testes.
8. Trocar entrypoint somente após equivalência funcional mínima.


## 15. Evolução executada após autorização do shell visual paralelo

Após a diretriz registrada na seção 14.4, foi iniciada a preparação do novo shell visual em paralelo, sem eliminar a UI atual.

A implementação seguiu a restrição principal da auditoria:

- a UI atual não foi removida;
- a regra de negócio não foi recriada na camada visual;
- os launchers antigos foram preservados;
- a evolução foi feita em checkpoints pequenos e rastreáveis;
- o novo layout moderno permanece paralelo até equivalência funcional mínima.

### 15.1. Checkpoints criados nesta frente

Foram criados os seguintes checkpoints locais:

- checkpoint-ui-audit-before-new-layout
- checkpoint-modern-ui-shell-opens
- checkpoint-modern-dark-ui-opens
- checkpoint-modern-unified-entrypoint
- checkpoint-modern-package-entrypoint
- checkpoint-modern-launcher-info

Commits associados na branch atual:

- bbd71f2 docs: registra auditoria e diretriz do novo layout desktop
- 05853ce docs: adiciona auditoria visual da UI atual
- ebcd5b3 feat(ui): adiciona shell paralelo para novo layout desktop
- 9402a43 feat(ui): adiciona launcher paralelo para layout dark
- 037fed2 feat(ui): adiciona entrypoint moderno unificado
- 8492f4b feat(ui): permite executar pacote moderno diretamente
- 38c2ff1 feat(ui): adiciona diagnostico ao launcher moderno

### 15.2. Estado atual da UI moderna

Foi criado um pacote moderno executável diretamente por módulo Python.

Comando canônico atual:

- python -m UI.modern

Modos disponíveis:

- python -m UI.modern --mode dark
- python -m UI.modern --mode shell

Diagnóstico disponível sem abrir janela:

- python -m UI.modern --info
- python -m UI.modern --mode shell --theme clean --info

O modo padrão atual é:

- dark

O módulo aberto por padrão é:

- UI.modern.dark_window

O modo shell permanece disponível como referência temporária:

- UI.modern.main_window

### 15.3. Decisão arquitetural sobre entrypoint moderno

Decisão registrada:

- UI.modern passa a ser o ponto de entrada canônico da UI moderna em paralelo.
- O modo dark é a base visual preferencial em evolução.
- O modo shell permanece como referência temporária para comparação e preservação de direção.
- Nenhum dos dois substitui a UI atual até validação funcional mínima.
- Novas features não devem ser adicionadas ao shell temporário sem decisão documentada.
- A evolução visual deve convergir para o modo dark ou para um sucessor documentado dele.

### 15.4. Regras de continuidade a partir deste ponto

Antes de novas alterações em layout, tema, navegação, painel lateral, payoff, VWAP, estruturas ou terminal:

- consultar este documento;
- verificar os checkpoints existentes;
- conferir se a alteração preserva a diretriz da seção 14.2;
- não remover função operacional sem decisão explícita;
- não duplicar regra de negócio na UI;
- não alterar banco junto com layout sem fase específica;
- atualizar esta auditoria após cada checkpoint relevante.

### 15.5. Validações executadas

Foram executadas validações de sintaxe e abertura dos entrypoints modernos.

Validação de compilação:

- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py

Validação do pacote moderno:

- python -m UI.modern

Resultado observado:

- abertura da UI moderna em modo dark;
- carregamento de estruturas reais;
- log indicando ModernDarkUI com estruturas carregadas.

Validação do modo shell:

- python -m UI.modern --mode shell

Resultado observado:

- abertura do shell moderno;
- uso do banco derived.db;
- uso do contrato canônico para payoff_curve_points.

Validação do diagnóstico:

- python -m UI.modern --info
- python -m UI.modern --mode shell --theme clean --info

Resultado observado:

- impressão de mode;
- impressão de theme;
- impressão de appearance_mode;
- impressão de module;
- impressão de project_root;
- impressão de python;
- impressão de python_version;
- impressão de platform.

### 15.6. Pendências abertas da frente moderna

Pendência 1:

- Consolidar a tabela mestre da UI atual prevista na seção 10.

Pendência 2:

- Mapear explicitamente quais funções da UI atual já aparecem no novo layout moderno e quais ainda faltam.

Pendência 3:

- Classificar os tokens visuais hardcoded do arquivo UI/modern/dark_window.py.

Pendência 4:

- Integrar gradualmente UI/modern/theme.py ao layout dark, sem alterar regra de negócio.

Pendência 5:

- Preservar ou realocar filtros, tabela de decisões, payoff, comparação Curva A, exportação PNG, CRUD de estruturas e Terminal VWAP Payoff.

Pendência 6:

- Definir critério objetivo para considerar o modo dark equivalente o suficiente para substituir o shell temporário.

### 15.7. Próxima etapa autorizada

A próxima etapa autorizada não é eliminar a UI atual.

A próxima etapa autorizada é documental e de mapeamento:

1. atualizar esta auditoria com o estado da UI moderna;
2. criar ou complementar a tabela mestre de equivalência funcional;
3. mapear funções preservadas, ausentes e realocadas;
4. somente depois iniciar a troca de tokens visuais hardcoded por tema centralizado.

A próxima alteração de código recomendada, após esta atualização documental, será pequena e restrita:

- inventariar cores e estilos hardcoded em UI/modern/dark_window.py;
- substituir apenas tokens visuais por chamadas ao tema central;
- não mudar layout funcional;
- não mudar banco;
- não mudar regra de negócio;
- validar com python -m UI.modern, python -m UI.modern --info e py_compile.

## 16. Mapa de equivalência funcional da UI moderna

Foi criada a primeira versão do mapa de equivalência funcional entre a UI atual auditada e a UI moderna em paralelo.

Relatório gerado:

- reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md

### 16.1. Objetivo do mapa

O mapa existe para impedir avanço visual sem controle funcional.

Ele compara as funções obrigatórias registradas na seção 14.2 com evidências textuais nos arquivos atuais de UI.modern.

### 16.2. Critério adotado

O relatório não declara equivalência funcional final.

Critério usado:

- ausência textual indica pendência;
- presença apenas no shell indica que a função ainda não está confirmada no caminho preferencial;
- presença no dark indica evidência parcial;
- equivalência final exige validação manual e, quando aplicável, teste.

### 16.3. Funções obrigatórias avaliadas

Foram avaliadas as seguintes funções:

- filtros de decisões;
- seleção de decisões;
- detalhamento de decisão;
- rationale/why JSON;
- recalcular estrutura;
- curva de payoff;
- comparação Curva A;
- exportação PNG;
- CRUD e arquivamento de estruturas;
- Terminal VWAP Payoff;
- legs/pernas da estrutura;
- mensagens de status;
- banco e contratos canônicos.

### 16.4. Decisão de continuidade

A UI atual ainda não será removida.

O modo dark continua sendo o caminho preferencial da UI moderna.

O shell continua como referência temporária.

A próxima alteração de código autorizada permanece pequena e restrita:

- inventariar tokens visuais hardcoded em UI/modern/dark_window.py;
- substituir tokens visuais por tema centralizado;
- não mudar layout funcional;
- não mudar regra de negócio;
- não mudar banco;
- validar abertura e diagnóstico do launcher moderno.

## 17. Inventário de tokens visuais da UI moderna

Foi criada a primeira etapa da rodada de tema da UI moderna.

Relatório gerado:

- reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md

### 17.1. Objetivo

Identificar cores, dimensões e parâmetros visuais hardcoded em:

- UI/modern/dark_window.py
- UI/modern/theme.py

### 17.2. Restrição desta etapa

Esta etapa não altera código.

Ela apenas prepara o patch de centralização visual.

### 17.3. Decisão de continuidade

A próxima alteração de código autorizada será restrita a:

- UI/modern/theme.py
- UI/modern/dark_window.py

Escopo permitido:

- centralizar tokens visuais;
- substituir cores hardcoded por constantes/funções de tema;
- manter o mesmo layout funcional;
- manter os mesmos callbacks;
- manter os mesmos textos operacionais;
- não alterar banco;
- não alterar regra de negócio.

Validações obrigatórias após o patch:

- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py UI/modern/dark_window.py
- python -m UI.modern --info
- python -m UI.modern

## 18. Centralização inicial dos tokens de tema CustomTkinter

Foi executada a primeira alteração de código da rodada de tema da UI moderna.

### 18.1. Arquivos alterados

Arquivos alterados:

- UI/modern/theme.py
- UI/modern/dark_window.py

### 18.2. Escopo da alteração

A alteração foi restrita a tokens visuais de inicialização do CustomTkinter.

Foram centralizados em UI/modern/theme.py:

- modo de aparência do CustomTkinter;
- tema base do CustomTkinter.

O modo dark passou a consumir estes tokens, em vez de literais diretos.

### 18.3. Restrições preservadas

A alteração não modificou:

- layout funcional;
- callbacks;
- consultas de banco;
- controllers;
- services;
- repositories;
- regra de negócio;
- textos operacionais;
- contratos canônicos.

### 18.4. Validações obrigatórias

Validações executadas nesta rodada:

- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py UI/modern/dark_window.py
- python -m UI.modern --info
- python -m UI.modern

Resultado observado:

- diagnóstico do launcher moderno funcionando;
- abertura da UI moderna em modo dark;
- manutenção do carregamento de estruturas reais;
- ausência de regressão visual ou funcional perceptível.

### 18.5. Decisão de continuidade

A próxima etapa não é trocar a UI atual.

A próxima etapa recomendada é validar manualmente a equivalência parcial do modo dark contra o mapa criado em:

- reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md

Prioridade da próxima rodada:

- confirmar visualmente o que já existe no modo dark;
- separar funções preservadas, ausentes e realocadas;
- só depois iniciar implementação funcional faltante por blocos pequenos.

## 19. Validação manual de equivalência funcional do modo dark

Foi criada a etapa de validação manual do modo dark contra o mapa de equivalência funcional.

Relatório gerado:

- reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md

### 19.1. Objetivo

Validar manualmente o caminho preferencial da UI moderna antes de qualquer troca de entrypoint.

A validação compara o modo dark com as funções obrigatórias registradas no mapa:

- reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md

### 19.2. Escopo

Esta etapa é documental e manual.

Ela não altera:

- código;
- layout;
- banco;
- callbacks;
- services;
- controllers;
- repositories;
- regra de negócio.

### 19.3. Decisão de continuidade

A UI atual permanece como caminho principal.

O modo dark continua como caminho moderno paralelo.

A próxima implementação funcional só deve ocorrer após classificação manual das funções como:

- validada;
- parcial;
- ausente;
- realocada;
- não testada.

### 19.4. Correção da tabela de validação manual

A tabela do relatório manual foi normalizada para manter o status na coluna correta.

Correção aplicada:

- status manual movido para a coluna Status manual;
- evidências resumidas na coluna Evidência/observação;
- próximas ações preenchidas sem alterar código;
- conclusões manuais marcadas conforme validação observada.

A correção não altera:

- código;
- layout;
- callbacks;
- banco;
- services;
- regra de negócio.

## 20. Inventário técnico da exportação PNG

Foi criada uma etapa documental para mapear a exportação PNG antes de qualquer implementação.

Relatório gerado:

- reports/ui_modern_equivalence/03_inventario_exportacao_png.md

### 20.1. Objetivo

Localizar pontos existentes relacionados a PNG, savefig, canvas, matplotlib, exportação e payoff.

### 20.2. Decisão de segurança

Nenhuma alteração funcional deve ser feita antes da leitura do inventário.

O modo dark permanece paralelo.

A UI atual permanece como caminho principal.

## 21. Inventário focado da exportação PNG

Foi criado um inventário focado para reduzir o ruído do levantamento amplo de exportação PNG.

Relatório gerado:

- reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md

### 21.1. Objetivo

Localizar apenas pontos relevantes da UI relacionados a gráfico, canvas, arquivo PNG e exportação.

### 21.2. Decisão de segurança

Esta etapa não altera código funcional.

O patch de exportação PNG só deve ser feito após identificar o arquivo alvo.

## 22. Exportação PNG no painel dark

Foi implementada exportação PNG do gráfico de Payoff no painel dark.

Relatório gerado:

- reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md

### 22.1. Arquivos verificados

- UI/components/terminal_vwap_payoff_dark_panel.py alterado nesta rodada
- ui/components/terminal_vwap_payoff_dark_panel.py já possuía implementação equivalente

### 22.2. Decisão de segurança

O patch é isolado na UI dark.

Não altera banco, contratos canônicos, decisões ou cálculo.

A UI atual permanece como caminho principal.

## 23. Validação da exportação PNG no painel dark

A exportação PNG do gráfico de Payoff no painel dark foi validada manualmente.

Relatório gerado:

- reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md

### 23.1. Resultado

A funcionalidade foi considerada 100 por cento funcional.

### 23.2. Evidência operacional

A execução de python -m UI.modern abriu a UI moderna em modo dark, carregou estruturas, carregou uma estrutura e registrou Payoff exportado em PNG.

### 23.3. Decisão

Checkpoint de validação manual recomendado: checkpoint-modern-export-png-dark-panel-validated.

## 24. Inventario das acoes laterais de estruturas no painel dark

Foi iniciado o inventario das acoes laterais de estruturas na UI moderna dark.

Relatorio gerado:

- reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md

### 24.1. Objetivo

Mapear botoes, callbacks e comandos relacionados a estruturas antes de aplicar novo patch funcional.

### 24.2. Decisao de seguranca

Nenhuma regra de negocio deve ser alterada nesta etapa.

### 24.3. Proximo passo

Classificar lacunas e escolher o menor patch seguro para equivalencia das acoes laterais de estruturas.

## 25. Classificacao das acoes laterais de estruturas no painel dark

As acoes laterais de estruturas da UI moderna dark foram classificadas quanto a presenca visual e callbacks.

Relatorio gerado:

- reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md

### 25.1. Resultado

O painel dark indica cobertura das principais acoes laterais de estruturas.

### 25.2. Acoes classificadas

- recarregar estruturas
- nova estrutura
- selecionar estrutura
- recalcular payoff
- editar pernas
- duplicar estrutura
- arquivar estrutura
- registrar decisoes HOLD, CLOSE e ADJUST
- abrir bloco de ajuste
- voltar para lista

### 25.3. Decisao de seguranca

Nenhuma alteracao funcional foi aplicada nesta etapa.

### 25.4. Proximo passo

Executar validacao manual dirigida das acoes laterais no modo dark.

## 26. Validacao manual das acoes laterais de estruturas no painel dark

Foi executada validacao manual dirigida das acoes laterais de estruturas na UI moderna dark.

Relatorio gerado:

- reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md

### 26.1. Resultado

A validacao encontrou acoes funcionais, acoes parciais e falhas a corrigir.

### 26.2. Acoes funcionais

- recarregar estruturas
- abrir lista de estruturas
- selecionar estrutura
- editar pernas
- voltar para lista
- abrir acoes da estrutura

### 26.3. Acoes parciais

- recalcular Payoff executa, mas precisa feedback operacional visivel
- encerrar estrutura registra decisao CLOSE no console, mas precisa feedback operacional visivel

### 26.4. Falhas

- duplicar estrutura falha por metodo _cmd_duplicate nao encontrado neste componente
- abrir ajuste nao funciona no fluxo manual
- arquivar estrutura nao funciona no fluxo manual

### 26.5. Decisao

A proxima etapa deve aplicar patch funcional minimo restrito ao painel dark.

## 27. Patch funcional das acoes laterais de estruturas no painel dark

Foi aplicado patch funcional minimo nas acoes laterais de estruturas da UI moderna dark.

Relatorio gerado:

- reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md

### 27.1. Correcoes

- duplicacao implementada localmente com StructuresRepository
- feedback visual adicionado para recalculo e decisoes
- bloco de ajuste tornou-se visualmente explicito
- arquivamento recebeu validacao e feedback adicional
- decisao CLOSE passou a arquivar a estrutura via StructuresRepository.archive_structure

### 27.2. Decisao de seguranca

O patch ficou restrito aos arquivos do painel dark e seu espelho ui.

### 27.3. Validacao

- py_compile executado nos caminhos UI e ui
- validacao manual executada na UI moderna dark
- estruturas encerradas deixaram de aparecer em list_structures padrao

### 27.4. Proximo passo

Registrar checkpoint git do patch validado.

## 28. Integracao do patch de acoes laterais na main

O patch funcional das acoes laterais de estruturas do painel dark foi integrado na branch principal.

### 28.1. Estado registrado

Branch de trabalho anterior:

- patch-side-actions-structures

Branch principal atual:

- main

Commit integrado:

- f454cb2 fix(ui): corrige acoes laterais de estruturas no dark

Tag principal da rodada:

- checkpoint-modern-side-actions-structures-fix

### 28.2. Resultado da integracao

A integracao foi realizada por fast-forward, sem conflito manual.

A branch main passou a conter:

- UI moderna dark em paralelo
- painel dark de Terminal VWAP Payoff
- exportacao PNG validada
- acoes laterais de estruturas corrigidas
- relatorios de inventario, classificacao, validacao e patch
- auditoria atualizada ate a frente de acoes laterais

### 28.3. Publicacao remota

Foi executado push da branch main para o remoto.

Tambem foi executado push das tags locais.

Resultado final observado:

- main enviada para origin/main
- tags enviadas ao remoto
- segunda execucao de push confirmou Everything up-to-date

### 28.4. Fechamento da secao 27

A secao 27 fica considerada encerrada.

O patch validado de acoes laterais esta agora:

- testado manualmente
- compilado com py_compile
- commitado
- tageado
- integrado na main
- publicado no remoto

### 28.5. Restricoes preservadas

A integracao nao altera a diretriz arquitetural registrada anteriormente:

- a UI atual ainda nao deve ser eliminada
- o modo dark permanece como UI moderna paralela
- regra de negocio nao deve ser recriada na UI
- banco nao deve ser alterado junto com layout
- derived.db e app.db nao devem ter sincronismo continuo
- app.db permanece o destino canonico para mercado vivo

### 28.6. Proxima frente recomendada

A proxima frente deve voltar ao mapa de equivalencia funcional.

Frente recomendada:

- inventario dirigido de filtros, tabela e detalhe de decisoes no modo dark

Objetivo da proxima frente:

- identificar o que ja existe no modo dark relacionado a decisoes
- comparar com a UI atual auditada
- mapear lacunas de filtros, tabela, selecao, detalhe e rationale/why JSON
- nao alterar codigo antes do inventario
- produzir relatorio em reports/ui_modern_equivalence

### 28.7. Comandos de verificacao recomendados

Antes da proxima alteracao, recomenda-se validar o estado da main com:

- git status --short
- git log --oneline -8 --decorate
- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py UI/modern/dark_window.py UI/components/terminal_vwap_payoff_dark_panel.py
- python -m UI.modern --info
- python -m UI.modern

### 28.8. Decisao

A proxima etapa autorizada e documental.

Nao iniciar novo patch funcional antes de concluir o inventario dirigido de decisoes no modo dark.

## 29. Inventario dirigido de decisoes, filtros e tabela no modo dark

Foi iniciado inventario dirigido das funcionalidades de decisoes no modo dark da UI moderna.

Relatorio gerado:

- reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md

### 29.1. Objetivo

Mapear, antes de qualquer patch funcional, a presenca ou ausencia de:

- filtros de decisoes
- tabela/listagem de decisoes
- selecao de decisao
- detalhe da decisao
- rationale/why JSON
- conexoes com controllers, services e repositories

### 29.2. Decisao de seguranca

Esta etapa e documental.

Nao altera:

- codigo funcional
- layout operacional
- callbacks
- banco
- regra de negocio
- contratos canonicos

### 29.3. Proximo passo

Ler o inventario gerado, classificar lacunas e definir o menor patch seguro para equivalencia parcial de decisoes no modo dark.

## 30. Classificacao das lacunas de decisoes no modo dark

Foi criada classificacao das lacunas de decisoes no modo dark a partir do inventario dirigido.

Relatorio gerado:

- reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md

### 30.1. Resultado

O modo dark ainda nao possui equivalencia funcional de decisoes.

Foram classificados como ausentes no modo dark:

- filtros de decisoes
- tabela/listagem de decisoes
- selecao de decisao
- detalhe da decisao
- rationale/why JSON no fluxo dark
- payoff acionado a partir de selecao de decisao

### 30.2. Componentes reaproveitaveis

A classificacao indica reaproveitamento provavel de componentes ja existentes:

- UI.components.filters_panel.FiltersPanel
- UI.components.decisions_grid.DecisionsGrid
- UI.components.details_panel.DetailsPanel
- fluxo de dados usado pelo shell moderno em UI/modern/main_window.py

### 30.3. Decisao de seguranca

A proxima etapa autorizada pode ser patch funcional minimo no modo dark para adicionar filtros, tabela e detalhe de decisoes.

Restricoes do patch futuro:

- nao criar regra de negocio na UI
- nao alterar banco
- nao alterar repositories, services ou controllers sem necessidade comprovada
- nao trocar entrypoint principal
- nao eliminar a UI atual
- manter o modo dark como UI moderna paralela

### 30.4. Proximo passo

Aplicar patch pequeno e restrito para equivalencia parcial de decisoes no modo dark, iniciando por:

- filtros
- tabela/listagem
- selecao
- detalhe

## 31. Historico de decisoes no painel dark

Foi implementado e validado o historico de decisoes operacionais por estrutura no painel dark da UI moderna.

Relatorio gerado:

- reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md

### 31.1. Objetivo

Registrar e exibir, no fluxo operacional da estrutura selecionada, as ultimas decisoes tomadas pelo usuario.

Decisoes cobertas:

- HOLD / Manter
- ADJUST / Ajustar
- CLOSE / Encerrar

### 31.2. Arquivo alterado

Arquivo alterado nesta rodada:

- UI/components/terminal_vwap_payoff_dark_panel.py

### 31.3. Persistencia criada

Foi criada, quando inexistente, a tabela:

- structure_decisions

Campos principais:

- id
- structure_id
- decision
- label
- note
- created_at

Tambem foi criado indice por structure_id para consulta do historico.

### 31.4. Resultado funcional

O painel dark passou a:

- registrar decisao operacional por estrutura;
- salvar label amigavel;
- salvar data e hora local;
- exibir bloco ULTIMAS DECISOES no painel lateral;
- manter o comportamento de CLOSE arquivando a estrutura;
- manter o modo dark como UI moderna paralela.

### 31.5. Validacao

Validacao manual executada:

- python -m UI.modern

Resultado observado:

- UI moderna abriu em modo dark;
- estruturas reais foram carregadas;
- estrutura ID 2 foi carregada;
- decisao HOLD foi registrada;
- historico apareceu na interface com data e hora;
- registro foi confirmado em dados/app.db na tabela structure_decisions.

Registro confirmado:

- structure_id: 2
- decision: HOLD
- label: Manter
- created_at: 2026-07-02 11:07:16

### 31.6. Commit funcional associado

Commit:

- 2830b8c Adiciona historico de decisoes no painel dark

### 31.7. Decisao de seguranca

A alteracao nao encerra a equivalencia funcional completa de decisoes registrada na secao 30.

Continuam pendentes:

- filtros globais de decisoes;
- tabela/listagem global de decisoes;
- selecao de decisao;
- detalhe da decisao;
- rationale/why JSON;
- payoff acionado a partir de decisao selecionada.

### 31.8. Proxima frente recomendada

A proxima frente deve continuar a secao 30.4, agora considerando que o historico operacional por estrutura ja existe.

Frente recomendada:

- equivalencia parcial de decisoes no modo dark

Escopo inicial:

- adicionar bloco/listagem global de decisoes no modo dark;
- reutilizar componentes existentes quando possivel;
- preservar filtros, tabela, selecao e detalhe;
- nao alterar banco sem necessidade;
- nao eliminar a UI atual;
- nao trocar entrypoint principal;
- nao recriar regra de negocio na UI.

---

## 32. Listagem global minima de decisoes no modo dark

### 32.1. Objetivo

Avancar a equivalencia parcial do fluxo de decisoes no modo dark, sem alterar a UI legada, sem trocar entrypoint principal e sem modificar banco de dados.

A frente foi orientada pelo inventario tecnico registrado em:

- reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md

### 32.2. Decisao tecnica

Foi adotada a opcao de adaptador minimo, em vez de reaproveitamento direto dos componentes existentes da UI clara.

Motivos:

- FiltersPanel, DecisionsGrid e DetailsPanel usam tkinter/ttk;
- o modo dark atual usa customtkinter;
- DetailsPanel possui acoplamentos maiores com recalc, derived.db, payoff e estado operacional;
- a primeira entrega funcional deveria reduzir risco e manter escopo pequeno.

### 32.3. Implementacao realizada

Foi criado o componente:

- UI/components/decisions_dark_panel.py

Responsabilidades do novo painel:

- carregar decisoes via UIDataModel.get_decisions();
- exibir listagem global simples em customtkinter;
- permitir selecao de decisao;
- exibir detalhe textual da decisao selecionada;
- preservar campos principais como timestamp, structure_id, decision, level, dte_min, pl_atual, pl_max, pl_pct_of_max e rationale/why quando disponivel;
- limitar exibicao inicial a 300 registros para evitar sobrecarga visual;
- nao alterar schema, tabelas ou regras de negocio.

O arquivo UI/modern/dark_window.py foi ajustado para:

- instanciar UIDataModel;
- criar CTkTabview;
- manter o Terminal VWAP na aba "Terminal VWAP";
- adicionar nova aba "Decisões";
- recarregar tambem a listagem de decisoes pelo menu Aplicacao > Atualizar.

### 32.4. Validacao manual

Comando executado:

- python -m py_compile UI/modern/dark_window.py UI/components/decisions_dark_panel.py
- python -m UI.modern

Resultado observado:

- aplicacao abriu no modo dark;
- painel Terminal VWAP continuou funcional;
- 4 estruturas foram carregadas;
- aba Decisões foi exibida;
- 8 decisoes foram carregadas no modo dark;
- selecao de decisoes alternou entre estruturas reais;
- detalhe textual foi atualizado conforme a decisao selecionada.

Logs observados:

- [ModernDarkUI] 4 estruturas carregadas
- [ModernDarkUI] 8 decisões carregadas no modo dark
- [ModernDarkUI] Decisão selecionada: estrutura=3, decisão=HOLD
- [ModernDarkUI] Decisão selecionada: estrutura=2, decisão=HOLD

### 32.5. Commit funcional associado

Commit:

- 004f0c0 feat(ui): adiciona listagem de decisoes no modo dark

Tag:

- checkpoint-modern-decisions-list-dark-minimal

### 32.6. Resultado funcional

A UI dark agora possui equivalencia parcial do fluxo de decisoes:

- listagem global de decisoes;
- selecao de decisao;
- detalhe textual simples;
- carregamento via UIDataModel existente;
- integracao ao shell dark por aba dedicada.

### 32.7. Pendencias conhecidas

Ainda nao foram migrados nesta frente:

- filtros avancados;
- grid completo equivalente ao DecisionsGrid;
- painel completo equivalente ao DetailsPanel;
- atualizacao do payoff a partir da decisao selecionada;
- acao direta para carregar a estrutura selecionada no Terminal VWAP;
- exportacao CSV da listagem dark;
- ordenacao/Busca textual no painel dark.

### 32.8. Proxima frente recomendada

A proxima frente deve conectar a decisao selecionada a uma acao operacional simples.

Opcoes recomendadas:

1. adicionar botao "Carregar estrutura no Terminal" na aba Decisões;
2. adicionar busca/filtro textual minimo por estrutura, decisao ou timestamp;
3. adicionar exportacao CSV da listagem de decisoes exibida.

Prioridade recomendada:

- carregar a estrutura da decisao selecionada no Terminal VWAP, se houver metodo seguro ja existente no TerminalVWAPPayoffDarkPanel.


---

## 33. Carregamento de estrutura a partir da decisao no modo dark

### 33.1. Objetivo

Conectar a listagem de decisoes do modo dark ao Terminal VWAP, permitindo que uma decisao selecionada carregue diretamente a estrutura associada.

A frente foi uma evolucao da entrega registrada na secao 32, que havia introduzido a listagem global minima de decisoes no modo dark.

### 33.2. Decisao tecnica

Foi adotada integracao por callback entre o painel de decisoes e a janela dark principal.

Motivos:

- manter DecisionsDarkPanel desacoplado do TerminalVWAPPayoffDarkPanel;
- evitar que o painel de decisoes conheca detalhes internos do terminal;
- preservar o Terminal VWAP como responsavel por carregar estrutura, pernas, mercado, payoff, KPIs, graficos e alertas;
- nao alterar banco de dados;
- nao modificar regra de negocio.

### 33.3. Inspecao previa

Foi confirmado que TerminalVWAPPayoffDarkPanel ja mantem as estruturas carregadas em:

- self.structures

Tambem foi confirmado metodo existente para carregamento operacional:

- select_structure(self, structure: Dict[str, Any]) -> None

Esse metodo ja executa o fluxo completo do Terminal VWAP:

- define selected_structure;
- carrega pernas;
- carrega mercado;
- carrega pontos de payoff;
- atualiza cabecalho;
- atualiza KPIs;
- renderiza pernas;
- renderiza graficos;
- renderiza alertas;
- renderiza painel de acoes da estrutura.

### 33.4. Implementacao realizada

O componente UI/components/decisions_dark_panel.py foi ajustado para receber callback opcional:

- on_load_structure

Foi adicionado o botao:

- Carregar estrutura no Terminal

Comportamento do botao:

- inicia desabilitado;
- habilita quando a decisao selecionada possui structure_id ou aba;
- ao clicar, chama o callback com o identificador da estrutura;
- exibe status quando nao ha decisao selecionada, quando a selecao e invalida ou quando nao ha callback disponivel.

O arquivo UI/modern/dark_window.py foi ajustado para:

- passar on_load_structure=self._load_structure_from_decision ao DecisionsDarkPanel;
- localizar a estrutura em self.panel.structures;
- recarregar estruturas se necessario;
- chamar self.panel.select_structure(selected);
- trocar a aba ativa para "Terminal VWAP";
- emitir status de sucesso ou erro.

### 33.5. Validacao manual

Comandos executados:

- python -m py_compile UI/modern/dark_window.py UI/components/decisions_dark_panel.py
- python -m UI.modern

Resultado observado:

- aplicacao abriu no modo dark;
- aba Decisões carregou as decisoes;
- botao "Carregar estrutura no Terminal" ficou ativo apos selecionar decisao com estrutura;
- clique no botao carregou a estrutura correspondente no Terminal VWAP;
- UI alternou para a aba Terminal VWAP;
- Terminal atualizou a analise ativa;
- fluxo funcionou para mais de uma estrutura.

Logs observados:

- [ModernDarkUI] Estrutura carregada: ID 3
- [ModernDarkUI] Estrutura 3 carregada a partir da decisão
- [ModernDarkUI] Estrutura carregada: ID 2
- [ModernDarkUI] Estrutura 2 carregada a partir da decisão

### 33.6. Commit funcional associado

Commit:

- 2b45b47 feat(ui): carrega estrutura da decisao no terminal dark

Tag:

- checkpoint-modern-decisions-load-structure-dark

### 33.7. Resultado funcional

A UI dark passa a oferecer fluxo operacional integrado:

- visualizar decisoes;
- selecionar uma decisao;
- carregar a estrutura associada diretamente no Terminal VWAP;
- continuar a analise pelo painel operacional ja existente.

### 33.8. Pendencias conhecidas

Ainda nao foram implementados nesta frente:

- filtro textual na listagem dark;
- filtros avancados equivalentes a FiltersPanel;
- grid completo equivalente ao DecisionsGrid;
- painel completo equivalente ao DetailsPanel;
- exportacao CSV;
- acao inversa Terminal VWAP -> Decisoes filtradas por estrutura;
- destaque visual persistente da decisao ja carregada.

### 33.9. Proxima frente recomendada

A proxima frente recomendada e adicionar busca/filtro textual minimo na aba Decisões.

Campos sugeridos para busca:

- structure_id;
- decision;
- timestamp;
- level;
- rationale/why.

Essa frente tem baixo risco, melhora bastante a usabilidade e nao exige alteracao de banco nem regra de negocio.

---

## 34. Busca por estrutura ativa na aba Decisoes dark

### 34.1. Objetivo

Adicionar busca textual na aba Decisoes do modo dark, mantendo o escopo operacional correto:

- buscar por ID da estrutura;
- buscar por nome da estrutura;
- exibir somente decisoes associadas a estruturas ativas;
- evitar busca em campos ruidosos como timestamp, rationale, why, level ou demais metadados internos.

A frente evoluiu diretamente a entrega da secao 33, que havia conectado a decisao selecionada ao carregamento da estrutura no Terminal VWAP.

### 34.2. Problema identificado

A primeira versao da busca textual foi ampla demais.

Ela permitia procurar em muitos campos da decisao, incluindo:

- timestamp;
- decision;
- level;
- rationale;
- why;
- why_json;
- demais chaves internas do registro.

Durante o teste manual, foi observado que isso gerava comportamento confuso:

- buscas por timestamp dependiam de sequencias numericas longas e pouco previsiveis;
- numeros soltos podiam coincidir com campos internos sem significado operacional;
- a busca deixava de refletir o uso real esperado na tela;
- o usuario precisava localizar decisoes a partir da estrutura, nao a partir dos metadados da decisao.

A diretriz operacional validada foi:

- a busca da aba Decisoes deve localizar decisoes por estrutura;
- estrutura significa ID ou nome;
- estruturas inativas nao devem participar da listagem principal.

### 34.3. Decisao tecnica

Foi mantido o componente DecisionsDarkPanel desacoplado do Terminal VWAP.

Para permitir que o painel de decisoes conheca as estruturas ativas sem acessar diretamente o terminal, foi criado callback opcional:

- get_structures

Responsabilidades:

- dark_window.py fornece as estruturas carregadas no Terminal VWAP;
- DecisionsDarkPanel monta indice local structure_id -> structure;
- DecisionsDarkPanel identifica estruturas ativas;
- DecisionsDarkPanel filtra decisoes com base nesse indice;
- DecisionsDarkPanel restringe a busca ao ID e nome/rotulo/descricao da estrutura.

Essa abordagem preserva:

- baixo acoplamento;
- ausencia de alteracao no banco;
- ausencia de alteracao em regras de negocio;
- compatibilidade com o fluxo ja existente do Terminal VWAP.

### 34.4. Implementacao realizada

Arquivo alterado:

- UI/components/decisions_dark_panel.py

Principais mudancas:

- adicionado atributo filtered_decisions;
- adicionado indice structure_index;
- adicionado conjunto active_structure_ids;
- adicionado campo de busca no cabecalho;
- adicionado botao Limpar;
- listagem passou a renderizar filtered_decisions;
- selecao passou a operar sobre filtered_decisions;
- carregamento da estrutura passou a usar a decisao filtrada selecionada;
- busca passou a ser aplicada em tempo real no evento KeyRelease;
- busca foi restringida a ID e nome/rotulo/descricao da estrutura;
- decisoes de estruturas inativas passaram a ser excluidas da listagem.

Campos considerados para nome/rotulo da estrutura:

- name;
- nome;
- label;
- title;
- titulo;
- título;
- description;
- descricao;
- descrição;
- structure_name;
- nome_estrutura;
- estrutura.

Campos considerados para status ativo/inativo de forma defensiva:

- active;
- is_active;
- ativo;
- enabled;
- status;
- state;
- situacao;
- situação.

Valores tratados como inativos incluem:

- inactive;
- inativo;
- inativa;
- closed;
- fechado;
- fechada;
- encerrado;
- encerrada;
- finalizado;
- finalizada;
- archived;
- arquivado;
- arquivada;
- deleted;
- removido;
- removida;
- cancelado;
- cancelada.

Arquivo alterado:

- UI/modern/dark_window.py

Principais mudancas:

- DecisionsDarkPanel passou a receber get_structures=self._get_structures_for_decisions;
- criado helper _get_structures_for_decisions;
- helper retorna self.panel.structures;
- se necessario, tenta recarregar estruturas via reload_structures.

### 34.5. Comportamento funcional validado

A aba Decisoes passou a apresentar busca ativa caractere a caractere.

Comportamento validado:

- buscar por ID da estrutura funciona;
- buscar por nome da estrutura funciona;
- busca por trechos do nome funciona;
- a listagem considera somente estruturas ativas;
- a selecao continua funcionando apos filtro;
- o botao "Carregar estrutura no Terminal" continua funcionando;
- ao carregar estrutura a partir da decisao, a UI alterna corretamente para o Terminal VWAP;
- a busca nao depende mais de timestamp nem campos internos ruidosos.

Exemplo validado:

- nome de estrutura no teste: SBSP+SMAL=BOVA;
- busca por ID funcionou;
- busca por nome/trecho funcionou;
- log indicou reducao da lista exibida para decisoes de estruturas ativas.

### 34.6. Validacao tecnica

Comandos executados:

- python -m py_compile UI/components/decisions_dark_panel.py UI/modern/dark_window.py
- python -m UI.modern

Resultado:

- compilacao sem erro;
- aplicacao abriu no modo dark;
- Terminal VWAP carregou estruturas;
- aba Decisoes carregou decisoes;
- filtro textual funcionou em tempo real;
- carregamento de estrutura a partir da decisao continuou funcional.

Logs observados:

- [ModernDarkUI] 4 estruturas carregadas
- [ModernDarkUI] 8 decisões carregadas no modo dark
- [ModernDarkUI] Decisão selecionada: estrutura=2, decisão=HOLD (3 de 8 exibidas)
- [ModernDarkUI] Estrutura carregada: ID 2
- [ModernDarkUI] Estrutura 2 carregada a partir da decisão

### 34.7. Commit funcional associado

Commit:

- bceedfa feat/ui): adiciona busca por estrutura ativa em decisoes dark

Observacao:

- a mensagem do commit foi publicada com pequeno desvio no padrao conventional commit: feat/ui) em vez de feat(ui);
- como o commit ja foi enviado ao repositorio remoto, nao foi reescrito historico apenas por esse detalhe.

Tag:

- checkpoint-modern-decisions-active-structure-search-dark

### 34.8. Resultado funcional

A UI dark passa a oferecer um fluxo operacional mais consistente para decisoes:

- listar decisoes relevantes;
- restringir a exibicao a estruturas ativas;
- buscar rapidamente por ID ou nome da estrutura;
- selecionar uma decisao;
- carregar a estrutura associada diretamente no Terminal VWAP.

A busca deixou de ser generica e passou a refletir o fluxo real de uso da tela.

### 34.9. Pendencias conhecidas

Ainda nao foram implementados nesta frente:

- exportacao CSV da listagem filtrada;
- filtros avancados equivalentes ao FiltersPanel legado;
- grid completo equivalente ao DecisionsGrid legado;
- painel completo equivalente ao DetailsPanel legado;
- destaque visual persistente da decisao ja carregada;
- acao inversa Terminal VWAP -> Decisoes filtradas pela estrutura selecionada;
- testes automatizados especificos para DecisionsDarkPanel.

### 34.10. Proxima frente recomendada

A proxima frente recomendada e uma das seguintes, em ordem sugerida:

1. exportar CSV da listagem filtrada de decisoes no modo dark;
2. enriquecer o detalhe da decisao com nome da estrutura e status ativo;
3. adicionar acao Terminal VWAP -> Decisoes filtradas pela estrutura selecionada;
4. iniciar equivalencia parcial com o DetailsPanel legado.

Prioridade recomendada:

- implementar exportacao CSV da listagem filtrada, pois reaproveita filtered_decisions, tem baixo risco e melhora a utilidade operacional da aba Decisoes sem alterar banco nem regra de negocio.

---

## 35. Exportacao CSV da listagem filtrada de decisoes no modo dark

### 35.1. Objetivo

Adicionar exportacao CSV na aba Decisoes do modo dark, usando como base exatamente a listagem exibida apos o filtro atual.

A frente evoluiu diretamente a secao 34, que havia introduzido:

- busca por ID da estrutura;
- busca por nome da estrutura;
- restricao da listagem a estruturas ativas;
- armazenamento da listagem exibida em filtered_decisions.

### 35.2. Escopo definido

A exportacao CSV foi limitada ao escopo operacional da aba Decisoes dark:

- exportar somente decisoes exibidas em filtered_decisions;
- respeitar busca textual atual;
- respeitar filtro de estruturas ativas;
- incluir nome da estrutura quando disponivel;
- incluir payload bruto da decisao para auditoria;
- nao alterar banco de dados;
- nao alterar regra de negocio;
- nao alterar geracao das decisoes;
- nao substituir componentes legados de DecisionsGrid ou FiltersPanel.

### 35.3. Inventario previo

Foi identificado que o projeto ja possuia padroes de exportacao em outras areas:

- UI/main_window.py;
- UI/modern/main_window.py;
- UI/models/ui_data.py;
- UI/components/payoff_chart.py;
- UI/components/terminal_vwap_payoff_dark_panel.py.

Padroes observados:

- uso de tkinter.filedialog.asksaveasfilename;
- uso de messagebox para sucesso ou erro;
- uso de csv.DictWriter em exportacao tabular;
- uso de status da UI para feedback operacional;
- exportacao especifica por contexto, sem alterar banco.

### 35.4. Implementacao realizada

Arquivo alterado:

- UI/components/decisions_dark_panel.py

Imports adicionados:

- csv;
- datetime;
- filedialog;
- messagebox.

Mudancas de layout:

- adicionado botao "Exportar CSV" no cabecalho da aba Decisoes;
- botao posicionado entre "Carregar estrutura no Terminal" e "Atualizar";
- header passou a usar uma coluna adicional;
- campo de busca foi ajustado para manter o layout responsivo;
- botao "Limpar" foi reposicionado para a nova coluna final.

Metodo principal adicionado:

- _export_filtered_csv

Responsabilidades do metodo:

- validar se existem decisoes exibidas para exportar;
- abrir dialogo de salvamento;
- sugerir nome de arquivo com timestamp;
- escrever CSV com encoding utf-8-sig;
- usar csv.DictWriter;
- exportar uma linha por decisao filtrada;
- emitir status de cancelamento, sucesso ou erro;
- exibir messagebox de sucesso ou erro.

Metodo auxiliar adicionado:

- _decision_export_row

Responsabilidades:

- montar linha padronizada para cada decisao;
- calcular structure_id a partir de structure_id ou aba;
- incluir nome da estrutura;
- indicar se a estrutura esta ativa;
- preservar campos principais da decisao;
- incluir payload bruto em raw_json.

Metodo auxiliar adicionado:

- _csv_value

Responsabilidades:

- normalizar valores para CSV;
- converter None para string vazia;
- serializar dict/list como JSON textual;
- converter demais valores para string.

Metodo auxiliar adicionado:

- _structure_name

Responsabilidades:

- resolver nome/rotulo/descricao da estrutura a partir de structure_index;
- reutilizar a mesma familia defensiva de campos usada na busca da secao 34.

### 35.5. Campos exportados

A exportacao CSV passou a gerar as seguintes colunas:

- export_index;
- timestamp;
- created_at;
- structure_id;
- structure_name;
- structure_active;
- decision;
- level;
- dte_min;
- pl_atual;
- pl_max;
- pl_pct_of_max;
- spot_reference;
- spot_ref;
- rationale;
- why;
- raw_json.

A coluna raw_json foi incluida para preservar rastreabilidade completa do registro original da decisao sem depender apenas dos campos tabulares principais.

### 35.6. Comportamento funcional validado

Comportamento esperado e validado:

- quando ha busca ativa, exporta somente as decisoes filtradas;
- quando nao ha busca ativa, exporta as decisoes exibidas de estruturas ativas;
- quando nao ha decisoes exibidas, informa que nao ha dados para exportar;
- cancelar o dialogo de salvamento nao gera erro;
- exportacao concluida exibe status de sucesso;
- arquivo CSV e salvo corretamente;
- arquivo CSV abre corretamente;
- selecao da decisao nao e alterada;
- estrutura carregada no Terminal nao e alterada;
- banco de dados nao e modificado.

### 35.7. Validacao tecnica

Comandos executados:

- python -m py_compile UI/components/decisions_dark_panel.py UI/modern/dark_window.py
- python -m UI.modern

Resultado:

- compilacao sem erro;
- aplicacao abriu no modo dark;
- aba Decisoes abriu corretamente;
- botao Exportar CSV ficou visivel;
- busca por ID funcionou;
- lista filtrada funcionou;
- exportacao funcionou;
- arquivo foi salvo;
- CSV foi aberto com sucesso.

### 35.8. Commit funcional associado

Commit:

- ad3c15f feat(ui): exporta csv de decisoes filtradas no modo dark

Tag:

- checkpoint-modern-decisions-filtered-csv-dark

### 35.9. Resultado funcional

A aba Decisoes do modo dark passa a oferecer ciclo operacional completo para a listagem filtrada:

- carregar decisoes;
- restringir a estruturas ativas;
- buscar por ID ou nome da estrutura;
- selecionar decisao;
- carregar estrutura associada no Terminal VWAP;
- exportar a listagem exibida em CSV.

A exportacao aproveita filtered_decisions e, portanto, respeita diretamente o estado visual atual da aba.

### 35.10. Pendencias conhecidas

Ainda nao foram implementados nesta frente:

- filtros avancados equivalentes ao FiltersPanel legado;
- grid completo equivalente ao DecisionsGrid legado;
- painel completo equivalente ao DetailsPanel legado;
- destaque visual persistente da decisao ja carregada;
- acao inversa Terminal VWAP -> Decisoes filtradas pela estrutura selecionada;
- testes automatizados especificos para exportacao CSV do DecisionsDarkPanel;
- configuracao customizada de colunas exportadas pelo usuario.

### 35.11. Proxima frente recomendada

A proxima frente recomendada e enriquecer o detalhe da decisao no modo dark.

Motivos:

- a aba ja lista, filtra, seleciona, carrega estrutura e exporta CSV;
- o proximo ganho natural esta na leitura detalhada da decisao;
- pode reaproveitar structure_index;
- pode exibir nome da estrutura, status ativo e dados principais de forma mais legivel;
- aproxima a aba dark da equivalencia parcial com o DetailsPanel legado;
- nao exige alteracao de banco nem de regra de negocio.

Prioridade sugerida:

- adicionar cabecalho estruturado no detalhe da decisao com estrutura, nome, status, decisao, nivel, timestamp e principais metricas;
- manter abaixo o bloco textual/raw atual para auditoria.

---

---

## Conteudo recuperado da copia da raiz AUDITORIA_REFACTOR_UI.md

Origem recuperada:

- arquivo: `AUDITORIA_REFACTOR_UI.md`
- motivo: a copia da raiz continha evolucoes posteriores nao presentes no arquivo canonico
- acao: conteudo preservado integralmente para evitar refazimento de auditoria/evolucao
- destino oficial apos esta mesclagem: `reports/auditoria/AUDITORIA_REFACTOR_UI.md`

## Frente 36 — Detalhe enriquecido da decisão no modo dark

Status: concluída
Data: 2026-07-02
Commit funcional: 7c66ead
Tag funcional: checkpoint-modern-decisions-detail-rich-dark
Relatório: reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md

### Resumo

Foi enriquecida a apresentação do detalhe da decisão no painel dark de decisões.

A alteração ficou restrita a:

- UI/components/decisions_dark_panel.py

### Resultado

O painel passou a apresentar:

- resumo operacional;
- identificação da estrutura;
- status da estrutura;
- decisão;
- nível;
- timestamps;
- métricas principais;
- rationale / why;
- campos adicionais brutos.

### Validação

Executado com sucesso:

    python -m py_compile UI/components/decisions_dark_panel.py UI/modern/dark_window.py
    python -m UI.modern --info
    python -m UI.modern

Validação manual aprovada na UI moderna dark.

## 35. Exportacao CSV de decisoes filtradas no modo dark

Foi implementada e registrada a exportacao CSV da listagem filtrada de decisoes no modo dark.

### 35.1. Objetivo

Permitir que a visao atual da aba Decisoes no modo dark seja exportada para CSV, respeitando a listagem filtrada exibida ao usuario.

### 35.2. Resultado funcional

A UI moderna dark passou a oferecer exportacao CSV associada ao fluxo de decisoes.

A funcionalidade preserva o escopo da camada visual:

- nao altera banco;
- nao altera regra de negocio;
- nao altera services, controllers ou repositories;
- nao substitui a UI atual;
- nao troca o entrypoint principal.

### 35.3. Commits e tags associados

Commits associados:

- ad3c15f feat(ui): exporta csv de decisoes filtradas no modo dark
- 82e13fe docs(ui): registra exportacao csv de decisoes filtradas dark

Tags associadas:

- checkpoint-modern-decisions-filtered-csv-dark
- checkpoint-modern-decisions-filtered-csv-dark-audit

## 36. Detalhe enriquecido de decisao no modo dark

Foi implementado e registrado o detalhe enriquecido de decisao na aba Decisoes do modo dark.

### 36.1. Objetivo

Melhorar a leitura operacional da decisao selecionada, exibindo mais campos relevantes sem recriar regra de negocio na UI.

### 36.2. Resultado funcional

O detalhe da decisao no modo dark passou a apresentar informacoes mais completas da decisao selecionada, mantendo o fluxo paralelo da UI moderna.

A alteracao preserva:

- banco de dados;
- contratos canonicos;
- regra de negocio;
- services;
- controllers;
- repositories;
- UI atual como caminho principal.

### 36.3. Commits e tags associados

Commits associados:

- 7c66ead feat(ui): enriquece detalhe de decisao no modo dark
- 9aaa8fa docs(ui): registra detalhe enriquecido de decisoes dark

Tags associadas:

- checkpoint-modern-decisions-detail-rich-dark
- checkpoint-modern-decisions-detail-rich-dark-docs

## 37. Copia do detalhe de decisao no modo dark

Foi implementada e registrada a copia do detalhe da decisao no modo dark.

Relatorio gerado:

- reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md

### 37.1. Objetivo

Permitir copiar o detalhe da decisao selecionada na aba Decisoes do modo dark, facilitando auditoria, suporte operacional e registro externo.

### 37.2. Resultado funcional

A aba Decisoes do modo dark passou a oferecer acao de copia do detalhe da decisao selecionada.

A entrega complementa as frentes anteriores de:

- listagem global de decisoes;
- busca por estrutura ativa;
- carregamento da estrutura no Terminal VWAP;
- exportacao CSV;
- detalhe enriquecido.

### 37.3. Restricoes preservadas

A alteracao nao modifica:

- banco;
- schema;
- regra de negocio;
- services;
- controllers;
- repositories;
- contratos canonicos;
- entrypoint principal;
- UI atual legada.

### 37.4. Commits e tags associados

Commits associados:

- fb857d3 feat(ui): copia detalhe de decisao no modo dark
- 4d61c43 docs(ui): registra copia de detalhe de decisao dark

Tags associadas:

- checkpoint-modern-decisions-copy-detail-dark
- checkpoint-modern-decisions-copy-detail-dark-docs

## 38. Inventario de filtros avancados de decisoes no modo dark

Foi aberta a proxima frente documental da equivalencia funcional de decisoes no modo dark.

Relatorio gerado:

- reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md

### 38.1. Objetivo

Inventariar os filtros avancados de decisoes antes de qualquer patch funcional.

A comparacao deve considerar os filtros da UI atual:

- Periodo De/Ate;
- Estrutura;
- Decisao;
- Level >=;
- DTE <=;
- Aplicar;
- Limpar;
- indicador de filtros aplicados.

### 38.2. Estado atual considerado

O modo dark ja possui evolucoes parciais importantes no fluxo de decisoes:

- listagem global;
- selecao;
- detalhe enriquecido;
- copia do detalhe;
- busca por estrutura ativa;
- exportacao CSV filtrada;
- carregamento da estrutura no Terminal VWAP.

Ainda falta classificar a equivalencia dos filtros avancados da UI atual.

### 38.3. Decisao de seguranca

Esta frente e documental.

Nao deve alterar:

- codigo funcional;
- layout operacional;
- callbacks;
- banco;
- regra de negocio;
- services;
- controllers;
- repositories;
- contratos canonicos;
- entrypoint principal;
- UI atual legada.

### 38.4. Proximo passo

Ler os arquivos candidatos, classificar campos disponiveis e definir o menor patch seguro para filtros avancados de decisoes no modo dark.

## 39. Classificacao tecnica dos filtros avancados de decisoes no modo dark

Foi criada a classificacao tecnica dos filtros avancados de decisoes no modo dark.

Relatorio gerado:

- reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md

### 39.1. Objetivo

Ler os arquivos candidatos da frente 38 e classificar o menor caminho seguro para filtros avancados na aba Decisoes do modo dark.

### 39.2. Arquivos considerados

Foram considerados os seguintes arquivos:

- UI/components/decisions_dark_panel.py
- UI/modern/dark_window.py
- UI/modern/main_window.py
- UI/components/filters_panel.py
- UI/components/decisions_grid.py
- UI/components/details_panel.py

### 39.3. Decisao tecnica preliminar

A proxima implementacao deve preferir filtragem em memoria sobre as decisoes ja carregadas por UIDataModel.get_decisions(), desde que os campos necessarios estejam disponiveis.

Filtros candidatos de menor risco:

- decisao;
- level minimo;
- DTE maximo;
- estrutura usando indice ja existente;
- limpar filtros;
- indicador textual de quantidade filtrada.

Filtro que exige cuidado adicional:

- periodo De/Ate, por depender da padronizacao do campo de data ou timestamp.

### 39.4. Restricoes preservadas

A classificacao nao altera:

- codigo funcional;
- layout operacional;
- callbacks;
- banco;
- schema;
- services;
- controllers;
- repositories;
- regra de negocio;
- contratos canonicos;
- entrypoint principal;
- UI atual legada.

### 39.5. Proximo passo

Revisar o relatorio tecnico e, se confirmado, abrir patch funcional minimo para filtros simples na aba Decisoes dark.

---

## 40. Filtros simples e estabilizacao da selecao de decisoes no modo dark

### 40.1. Objetivo

Avancar a equivalencia parcial da aba Decisoes no modo dark, adicionando filtros simples e corrigindo problemas operacionais de selecao, detalhe e mensagens de status.

Esta rodada continua a evolucao iniciada nas secoes anteriores sobre:

- listagem global de decisoes;
- selecao de decisao;
- detalhe textual;
- carregamento da estrutura da decisao no Terminal VWAP;
- busca por estrutura ativa.

### 40.2. Restricoes preservadas

As alteracoes desta rodada preservaram as restricoes arquiteturais do projeto:

- a UI atual nao foi eliminada;
- o modo dark permanece como UI moderna paralela;
- nao houve migracao para web;
- nao houve alteracao de banco;
- nao houve sincronismo continuo entre derived.db e app.db;
- nao houve recriacao de regra de negocio na UI;
- nao houve alteracao em repositories, services ou controllers;
- os contratos canonicos foram preservados.

### 40.3. Inventario e classificacao de filtros avancados

Antes da implementacao dos filtros simples, foram registradas etapas documentais de inventario e classificacao dos filtros avancados de decisoes no modo dark.

Commits associados:

- b5ec20c docs(ui): abre inventario de filtros avancados de decisoes dark
- d23f8ef docs(ui): classifica filtros avancados de decisoes dark

Tags associadas:

- checkpoint-modern-decisions-advanced-filters-dark-inventory
- checkpoint-modern-decisions-advanced-filters-dark-classification

Decisao registrada:

- filtros avancados completos nao deveriam ser implementados de uma vez;
- a proxima entrega funcional deveria ser pequena;
- o primeiro passo funcional seria adicionar filtros simples de baixo risco.

### 40.4. Implementacao de filtros simples

Foi implementada evolucao funcional no componente:

- UI/components/decisions_dark_panel.py

Funcionalidades adicionadas ou estabilizadas:

- filtro textual por estrutura ativa;
- filtro por decisao;
- filtro numerico minimo por level;
- filtro numerico maximo por DTE;
- limpeza dos filtros;
- preservacao da listagem filtrada;
- selecao operando sobre filtered_decisions;
- detalhe textual sincronizado com a decisao filtrada;
- botao de carregar estrutura preservado no fluxo filtrado.

Commit associado:

- a137c1e feat(ui): adiciona filtros simples em decisoes dark

Tag associada:

- checkpoint-modern-decisions-simple-filters-dark

### 40.5. Correcao de detalhe sem selecao

Foi corrigido comportamento no qual o painel de detalhe poderia ser acessado em situacao sem selecao valida.

A correcao tornou o fluxo mais defensivo em relacao a:

- selected_index ausente;
- selected_index fora da faixa;
- lista filtrada vazia;
- tentativa de copiar detalhe sem decisao valida.

Commit associado:

- 2ce94a6 fix(ui): corrige detalhe de decisao sem selecao

Tag associada:

- checkpoint-modern-decisions-simple-filters-dark-selection-fix

### 40.6. Dedupe de status de selecao

Foi corrigido excesso de mensagens repetidas de status quando a mesma decisao era selecionada repetidamente.

Problema observado:

- a UI registrava status repetido para a mesma selecao;
- isso gerava ruido no console operacional;
- a mensagem de selecao deveria ser emitida apenas quando o texto de status mudasse.

Correcao aplicada:

- criado controle interno para evitar emissao duplicada consecutiva do mesmo status de selecao.

Commit associado:

- 436b168 fix(ui): evita status duplicado em decisoes dark

Tag associada:

- checkpoint-modern-decisions-dark-dedupe-selection-status

### 40.7. Centralizacao do status de selecao

Foi aplicada refatoracao pequena para centralizar o controle de status de selecao em helper dedicado.

Arquivo alterado:

- UI/components/decisions_dark_panel.py

Helper criado:

- _status_selected_decision

Objetivo:

- reduzir duplicacao;
- concentrar a regra de dedupe;
- manter _select_decision mais legivel;
- facilitar manutencao futura.

Commit associado:

- 954585c refactor(ui): centraliza status de selecao em decisoes dark

Tag associada:

- checkpoint-modern-decisions-dark-selection-status-helper

### 40.8. Inicializacao explicita do estado de status

Foi inicializado explicitamente no construtor o estado interno usado para deduplicar status de selecao.

Estado adicionado:

- self._last_decision_status_text: Optional[str] = None

Motivo:

- evitar atributo implicito criado apenas durante o fluxo;
- tornar o estado do painel mais previsivel;
- reduzir risco de manutencao futura.

Commit associado:

- d4ab1be refactor(ui): inicializa status de selecao em decisoes dark

Tag associada:

- checkpoint-modern-decisions-dark-selection-status-state

### 40.9. Validacoes executadas

Validacoes executadas ao longo da rodada:

- python -m py_compile UI/components/decisions_dark_panel.py
- git diff --check
- git diff --cached --check
- python -m UI.modern

Resultados observados:

- UI moderna abriu em modo dark;
- estruturas reais foram carregadas;
- decisoes foram carregadas no modo dark;
- filtros simples permaneceram funcionais;
- selecao de decisoes funcionou;
- detalhe da decisao foi atualizado;
- copia do detalhe funcionou;
- carregamento de estrutura a partir da decisao funcionou;
- Terminal VWAP recebeu a estrutura carregada;
- mensagens duplicadas consecutivas de mesma selecao foram evitadas.

### 40.10. Estado atual apos a rodada

Checkpoint atual da main:

- d4ab1be refactor(ui): inicializa status de selecao em decisoes dark

Tag atual:

- checkpoint-modern-decisions-dark-selection-status-state

A aba Decisoes do modo dark possui agora equivalencia parcial mais robusta:

- listagem global;
- filtros simples;
- selecao;
- detalhe;
- copia de detalhe;
- carregamento da estrutura no Terminal VWAP;
- controle de status sem repeticao consecutiva.

### 40.11. Pendencia tecnica identificada

Foi identificada uma pendencia pequena de robustez:

- quando a selecao e limpa com selected_index = None, o cache _last_decision_status_text permanece com o ultimo texto.

Risco:

- baixo;
- nao quebra o fluxo atual;
- mas deixa estado antigo preservado apos limpeza da selecao.

Proxima correcao recomendada:

- centralizar a limpeza de selecao em helper;
- ao limpar selected_index, tambem limpar _last_decision_status_text;
- aplicar apenas em UI/components/decisions_dark_panel.py;
- validar com py_compile e python -m UI.modern.

## 41. Rota alinhada para a proxima frente

### 41.1. Proxima frente recomendada

Frente recomendada:

- resetar estado de status quando a selecao de decisao for limpa.

Escopo permitido:

- UI/components/decisions_dark_panel.py

Objetivo:

- substituir pontos diretos de selected_index = None por helper local;
- garantir que _last_decision_status_text tambem seja limpo;
- preservar comportamento visual e funcional atual.

### 41.2. Restricoes da proxima frente

A proxima frente nao deve:

- alterar banco;
- alterar repositories;
- alterar services;
- alterar controllers;
- alterar contratos canonicos;
- recriar regra de negocio na UI;
- alterar layout funcional;
- trocar entrypoint;
- eliminar UI atual.

### 41.3. Validacoes obrigatorias da proxima frente

Validacoes obrigatorias:

- python -m py_compile UI/components/decisions_dark_panel.py
- git diff --check
- python -m UI.modern

Validacao manual minima:

- abrir aba Decisoes;
- selecionar decisao;
- aplicar filtro sem resultado;
- limpar filtro;
- selecionar decisao novamente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

Resultado esperado:

- nenhuma regressao;
- selecao limpa corretamente;
- status continua sem duplicacao consecutiva;
- carregamento de estrutura permanece funcional.

---

## 42. Reset do estado de status ao limpar selecao de decisoes dark

### 42.1. Objetivo

Corrigir pendencia tecnica registrada na secao 40.11, garantindo que o estado interno de status da selecao seja limpo sempre que a selecao de decisao for resetada.

### 42.2. Arquivo alterado

Arquivo alterado nesta rodada:

- UI/components/decisions_dark_panel.py

### 42.3. Implementacao realizada

Foi criado helper local para centralizar a limpeza de selecao:

- _clear_selection

Responsabilidades do helper:

- limpar selected_index;
- limpar _last_decision_status_text;
- evitar que o cache de status preserve texto antigo apos a selecao ser resetada.

Os pontos diretos de limpeza de selecao foram substituidos por chamada centralizada ao helper.

### 42.4. Restricoes preservadas

A alteracao nao modifica:

- layout funcional;
- banco de dados;
- repositories;
- services;
- controllers;
- contratos canonicos;
- regra de negocio;
- entrypoint principal;
- UI atual.

O modo dark permanece como UI moderna paralela.

### 42.5. Validacoes obrigatorias

Validacoes previstas para esta rodada:

- python -m py_compile UI/components/decisions_dark_panel.py
- git diff --check
- python -m UI.modern

Validacao manual minima:

- abrir aba Decisoes;
- selecionar decisao;
- aplicar filtro sem resultado;
- limpar filtro;
- selecionar decisao novamente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 42.6. Resultado esperado

Resultado esperado:

- selecao limpa corretamente;
- cache de status tambem e limpo;
- status continua sem duplicacao consecutiva;
- detalhe permanece funcional;
- copia de detalhe permanece funcional;
- carregamento de estrutura no Terminal VWAP permanece funcional.

---

## 43. Mapa de equivalencia atual da aba Decisoes dark

### 43.1. Objetivo

Registrar o estado atual da equivalencia parcial da aba Decisoes no modo dark apos as rodadas de filtros, detalhe, copia, exportacao, carregamento de estrutura e estabilizacao de selecao/status.

### 43.2. Recursos ja cobertos no modo dark

Recursos atualmente cobertos na UI moderna dark:

- listagem global de decisoes;
- carregamento de decisoes a partir do data model existente;
- filtros simples de baixo risco;
- selecao de decisao na tabela/listagem;
- painel de detalhe enriquecido da decisao selecionada;
- protecao contra detalhe sem selecao valida;
- copia do detalhe da decisao para a area de transferencia;
- exportacao CSV respeitando a listagem filtrada;
- carregamento da estrutura associada no Terminal VWAP;
- deduplicacao de mensagens consecutivas de status de selecao;
- limpeza consistente de selecao e cache interno de status.

### 43.3. Restricoes preservadas

As rodadas recentes preservaram:

- UI atual como caminho principal;
- modo dark como UI moderna paralela;
- entrypoint principal existente;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- regra de negocio.

### 43.4. Equivalencia parcial consolidada

A aba Decisoes no modo dark atingiu equivalencia parcial operacional para consulta, filtro simples, leitura, copia, exportacao e acionamento da estrutura associada.

Esta equivalencia ainda nao significa substituicao da UI atual.

### 43.5. Pendencias candidatas para proximas frentes

Pendencias candidatas, a serem tratadas apenas em frentes pequenas e isoladas:

- revisar filtros avancados ainda nao implementados;
- avaliar ordenacao visual da listagem;
- revisar estados vazios e mensagens auxiliares;
- avaliar indicadores de contagem filtrada versus total;
- revisar ergonomia dos botoes de acao;
- confirmar se ha diferencas relevantes em relacao a UI atual.

### 43.6. Proxima direcao recomendada

A proxima frente funcional recomendada deve ser pequena e de baixo risco.

Candidata preferencial:

- adicionar indicador textual de contagem filtrada versus total na aba Decisoes dark.

Objetivo da candidata:

- melhorar feedback operacional dos filtros;
- nao alterar regra de negocio;
- nao alterar repositories, services ou controllers;
- manter escopo restrito a UI/components/decisions_dark_panel.py.

---

## 44. Robustez de acoes sem selecao na aba Decisoes dark

### 44.1. Objetivo

Reforcar a robustez das acoes dependentes de selecao na aba Decisoes do modo dark, evitando comparacoes invalidas quando o indice selecionado estiver ausente ou inconsistente.

### 44.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 44.3. Implementacao realizada

Foi criado um helper interno para validar o indice atualmente selecionado:

- retorna o indice quando ele e inteiro e esta dentro dos limites da lista filtrada;
- retorna vazio quando nao ha selecao valida.

O helper passou a ser usado em:

- atualizacao do estado do botao de copia de detalhe;
- acao de copiar detalhe da decisao selecionada.

### 44.4. Ganho operacional

A aba Decisoes dark passa a tolerar melhor estados transitorios de UI, como:

- selecao limpa;
- filtro aplicado apos uma selecao anterior;
- lista filtrada vazia;
- acionamento defensivo de comando sem selecao valida.

### 44.5. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 44.6. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtros com e sem resultado;
- tentar copiar detalhe com selecao valida;
- confirmar que copia sem selecao valida nao quebra a UI.

### 44.7. Resultado esperado

Resultado esperado:

- copia de detalhe permanece funcional com selecao valida;
- estado sem selecao passa a ser tratado de forma defensiva;
- filtros e detalhe permanecem operacionais;
- nenhum contrato externo e alterado.

---

## 45. Consolidacao do feedback de filtros na aba Decisoes dark

### 45.1. Objetivo

Reduzir ruido operacional no status da UI moderna dark ao aplicar filtros na aba Decisoes, evitando repeticao consecutiva da mesma mensagem de filtro.

### 45.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 45.3. Implementacao realizada

Foi adicionado um estado interno especifico para mensagens de filtro:

- `_last_filter_status_text`

Tambem foi criado um helper dedicado:

- `_status_filter_result`

Esse helper centraliza o envio de mensagens relacionadas a filtro e evita repetir consecutivamente o mesmo texto.

### 45.4. Separacao preservada entre selecao e filtro

A frente manteve separados os fluxos de status:

- `_status_selected_decision` continua dedicado a mensagens de selecao de decisao;
- `_status_filter_result` passa a tratar mensagens de filtro, erro de filtro e ausencia de resultados.

Essa separacao evita misturar dedupe de selecao com dedupe de filtros.

### 45.5. Casos cobertos

Passaram a usar o helper de feedback de filtro:

- filtro invalido por campo numerico incorreto;
- filtro sem resultados em decisoes de estruturas ativas;
- ausencia de decisao de estrutura ativa;
- resumo de decisoes exibidas apos reload com filtro aplicado;
- filtro sem resultados apos reload.

### 45.6. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 45.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro sem resultado mais de uma vez;
- confirmar que mensagens repetidas nao poluem o status;
- aplicar filtro invalido;
- limpar filtros;
- selecionar decisao;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 45.8. Resultado esperado

Resultado esperado:

- mensagens consecutivas identicas de filtro deixam de ser repetidas;
- mensagens de selecao continuam funcionando;
- resumo visual de filtros permanece preservado;
- filtros, detalhe, copia, exportacao e carregamento de estrutura continuam operacionais.

---

## 46. Separacao entre selecao automatica e selecao manual na aba Decisoes dark

### 46.1. Objetivo

Reduzir ruido de status na aba Decisoes da UI moderna dark ao diferenciar selecoes automaticas feitas pela propria tela de selecoes manuais feitas pelo usuario.

### 46.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 46.3. Implementacao realizada

A rotina de selecao de decisao passou a aceitar um parametro opcional:

- `notify_status`

Quando esse parametro esta desabilitado, a decisao continua sendo selecionada internamente, com atualizacao de detalhe e botoes, mas sem emitir mensagem de status de selecao.

### 46.4. Selecoes automaticas ajustadas

Passaram a usar selecao silenciosa:

- selecao da primeira decisao apos reload;
- selecao da primeira decisao apos aplicacao de filtro com resultado.

Isso evita repeticoes como mensagens consecutivas de decisao selecionada quando a propria UI apenas esta mantendo uma selecao valida.

### 46.5. Selecao manual preservada

A selecao acionada pelo usuario na lista continua usando o comportamento padrao:

- atualiza detalhe;
- habilita acoes relacionadas;
- emite status de decisao selecionada.

### 46.6. Feedback de filtro com resultado

Foi adicionado um helper para identificar filtros ativos:

- `_has_active_filters`

Com isso, filtros com resultado passam a emitir status de filtro, sem depender de uma mensagem indireta de selecao automatica.

### 46.7. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 46.8. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- recarregar dados;
- aplicar filtro com resultado;
- aplicar filtro sem resultado;
- limpar filtros;
- selecionar manualmente uma decisao;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 46.9. Resultado esperado

Resultado esperado:

- reload e filtros deixam de repetir status de decisao selecionada por selecao automatica;
- selecao manual continua informando a decisao selecionada;
- filtros com resultado informam quantidade exibida;
- detalhe, copia, exportacao e carregamento de estrutura continuam operacionais.

---

## 47. Silenciamento de filtro limpo em estado neutro na aba Decisoes dark

### 47.1. Objetivo

Evitar ruido de status na aba Decisoes da UI moderna dark quando a tela esta apenas renderizando em estado neutro, sem filtros ativos.

### 47.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 47.3. Implementacao realizada

A rotina de aplicacao de filtro passou a aceitar um parametro opcional:

- `announce_clear`

Esse parametro controla se a mensagem de filtros limpos deve ser emitida quando nao existem filtros ativos.

### 47.4. Comportamento ajustado

A mensagem:

- `Filtros limpos: X decisões de estruturas ativas`

passa a ser emitida apenas em acoes explicitas de limpeza, como:

- limpar busca;
- limpar filtros avancados.

### 47.5. Estado neutro preservado

Quando a tela apenas carrega, recarrega ou re-renderiza sem filtros ativos, a UI deixa de emitir a mensagem de filtros limpos.

Isso reduz ruido operacional apos reload e evita status redundante logo depois da mensagem de decisoes carregadas.

### 47.6. Comportamentos preservados

Foram preservados:

- filtro aplicado com resultado;
- filtro sem resultado;
- filtro invalido;
- selecao automatica silenciosa;
- selecao manual com status;
- detalhe da decisao;
- copia de detalhe;
- carregamento de estrutura no Terminal VWAP.

### 47.7. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 47.8. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- confirmar que o carregamento inicial nao mostra filtros limpos;
- aplicar filtro com resultado;
- limpar filtros pelo botao;
- confirmar que a limpeza explicita informa filtros limpos;
- aplicar filtro sem resultado;
- aplicar filtro invalido;
- selecionar manualmente decisao;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 47.9. Resultado esperado

Resultado esperado:

- estado neutro sem filtros nao polui o status;
- limpeza explicita continua comunicada;
- feedback de filtros permanece rastreavel;
- operacoes da aba Decisoes dark continuam funcionais.

---

## 48. Correcao do anuncio explicito de limpeza de filtros na aba Decisoes dark

### 48.1. Objetivo

Corrigir a separacao entre mudanca normal de filtro e acao explicita de limpeza na aba Decisoes da UI moderna dark.

### 48.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 48.3. Ajuste realizado

A rotina de alteracao textual da busca voltou a aplicar filtro sem anunciar limpeza:

- `_on_search_changed`

A rotina de limpeza explicita dos filtros avancados passou a anunciar limpeza:

- `_clear_advanced_filters`

### 48.4. Comportamento esperado

Com o ajuste:

- digitar ou alterar busca apenas aplica filtro;
- limpar busca pelo botao comunica filtros limpos;
- limpar filtros avancados pelo botao comunica filtros limpos;
- carregamento neutro permanece silencioso quanto a filtros limpos.

### 48.5. Motivo da correcao

A frente anterior introduziu corretamente o parametro `announce_clear`, mas o uso precisava ficar restrito a acoes explicitas de limpeza.

Isso evita que uma simples alteracao de texto na busca seja interpretada como limpeza completa de filtros.

### 48.6. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 48.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- confirmar carregamento neutro sem mensagem de filtros limpos;
- digitar busca com resultado;
- limpar busca pelo botao;
- limpar filtros avancados pelo botao;
- aplicar filtro invalido;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 48.8. Resultado esperado

Resultado esperado:

- anuncio de filtros limpos fica restrito a limpeza explicita;
- busca textual continua responsiva;
- filtros avancados comunicam limpeza corretamente;
- status da aba Decisoes dark fica mais previsivel e menos ruidoso.

---

## 49. Clarificacao de filtro ativo sem reducao de resultados na aba Decisoes dark

### 49.1. Objetivo

Melhorar a clareza operacional do status de filtros na aba Decisoes da UI moderna dark quando existe filtro ativo, mas ele nao reduz a quantidade de decisoes exibidas.

### 49.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 49.3. Ajuste realizado

O feedback de filtro aplicado passou a diferenciar dois cenarios:

- filtro ativo que reduz a lista;
- filtro ativo que mantem todas as decisoes de estruturas ativas visiveis.

### 49.4. Comportamento anterior

Antes do ajuste, um filtro ativo que retornava todos os itens emitia mensagem no mesmo formato de um filtro realmente restritivo:

- `Filtro aplicado: 8 de 8 decisões de estruturas ativas`

Embora correta, a mensagem nao deixava claro que o filtro nao reduziu a lista.

### 49.5. Comportamento novo

Quando o filtro ativo nao reduz os resultados, a mensagem passa a ser:

- `Filtro aplicado sem reduzir resultados: X decisões de estruturas ativas`

Quando o filtro reduz resultados, permanece:

- `Filtro aplicado: X de Y decisões de estruturas ativas`

### 49.6. Comportamentos preservados

Foram preservados:

- filtro com reducao de resultados;
- filtro sem resultados;
- filtro invalido;
- limpeza explicita de filtros;
- estado neutro silencioso quanto a filtros limpos;
- selecao automatica silenciosa;
- selecao manual com status;
- copia de detalhe;
- carregamento de estrutura no Terminal VWAP.

### 49.7. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 49.8. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro que reduza resultados;
- aplicar filtro ativo que mantenha todos os resultados;
- aplicar filtro sem resultado;
- limpar filtros explicitamente;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 49.9. Resultado esperado

Resultado esperado:

- filtros restritivos continuam indicando X de Y decisoes;
- filtros nao restritivos passam a indicar que nao houve reducao;
- status da aba Decisoes dark fica mais informativo;
- operacoes da aba permanecem funcionais.

---

## 50. Centralizacao do status de resultado de filtros na aba Decisoes dark

### 50.1. Objetivo

Melhorar a organizacao interna da aba Decisoes da UI moderna dark centralizando a montagem do status de resultado de filtros em um metodo dedicado.

### 50.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 50.3. Ajuste realizado

Foi criado o metodo:

- `_status_filter_summary`

Esse metodo concentra a decisao de qual mensagem emitir apos aplicacao de filtros com resultado.

### 50.4. Comportamentos preservados

Foram preservadas as mensagens para:

- filtro aplicado com reducao de resultados;
- filtro aplicado sem reducao de resultados;
- limpeza explicita de filtros;
- estado neutro silencioso quanto a filtros limpos.

### 50.5. Reducao de complexidade local

A rotina `_apply_filter` deixou de conter diretamente o bloco aninhado de decisao de status para filtros com resultado.

Com isso, `_apply_filter` permanece focada em:

- ler filtros;
- validar filtros numericos;
- montar lista filtrada;
- renderizar linhas;
- selecionar automaticamente quando aplicavel;
- delegar o feedback consolidado.

### 50.6. Escopo preservado

A frente nao altera:

- regra de negocio;
- repositories;
- services;
- controllers;
- banco de dados;
- contratos canonicos;
- entrypoint principal;
- UI atual como caminho principal.

### 50.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro que reduza resultados;
- aplicar filtro que nao reduza resultados;
- aplicar filtro sem resultado;
- limpar filtros explicitamente;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 50.8. Resultado esperado

Resultado esperado:

- comportamento visual inalterado;
- status de filtros preservado;
- codigo mais legivel;
- decisao de status concentrada em metodo dedicado.

---

## 51. Centralizacao do rotulo de decisoes ativas na aba Decisoes dark

### 51.1. Objetivo

Melhorar a manutencao dos textos de status da aba Decisoes da UI moderna dark centralizando o rotulo de contagem de decisoes de estruturas ativas.

### 51.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 51.3. Ajuste realizado

Foi criado o metodo:

- `_active_decisions_label`

Esse metodo retorna o texto padronizado usado nas mensagens de status relacionadas a filtros:

- `X decisões de estruturas ativas`

### 51.4. Comportamento preservado

Foram preservadas as mensagens funcionais para:

- filtro aplicado com reducao;
- filtro aplicado sem reducao;
- limpeza explicita de filtros.

### 51.5. Motivo da mudanca

Antes do ajuste, o trecho `decisões de estruturas ativas` aparecia repetido dentro da montagem do status de filtros.

A centralizacao reduz duplicidade e facilita ajustes futuros de texto sem alterar a regra de filtragem.

### 51.6. Escopo preservado

A frente nao altera:

- regra de negocio;
- filtros;
- selecao automatica;
- selecao manual;
- repositories;
- services;
- controllers;
- banco de dados;
- contratos canonicos;
- entrypoint principal;
- UI atual como caminho principal.

### 51.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro que reduza resultados;
- aplicar filtro que nao reduza resultados;
- limpar filtros explicitamente;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 51.8. Resultado esperado

Resultado esperado:

- comportamento visual inalterado;
- mensagens de status preservadas;
- texto de contagem de decisoes ativas centralizado;
- codigo mais facil de manter.

## Frente 53 — refactor agressivo interno da aba Decisões dark

Bloco maior aplicado na branch refactor/decisions-dark-panel-large-block.

Escopo:

- criação de estado explícito para filtros da aba Decisões dark;
- decomposição do pipeline de filtragem em helpers dedicados;
- redução da responsabilidade direta de _apply_filter;
- separação entre coleta de filtros, validação, filtragem e exibição de resultado vazio;
- preservação do comportamento visual e dos contratos externos da aba.

Arquivos impactados:

- UI/components/decisions_dark_panel.py
- AUDITORIA_REFACTOR_UI.md

Validação esperada:

    python -m py_compile UI/components/decisions_dark_panel.py
    git diff --check
    python -m UI.modern

Critério de aceite:

- aba Decisões dark carrega normalmente;
- filtros continuam funcionando;
- filtros numéricos inválidos exibem mensagem de erro;
- limpar filtros restaura a listagem esperada;
- seleção de decisão atualiza o detalhe;
- copiar detalhe continua funcionando;
- carregar estrutura continua funcionando;
- exportação CSV continua funcionando.

- DecisionsDarkPanel: busca unificada por decisão, ID e nome; limpeza consolidada em um único botão.

- DecisionsDarkPanel: _build_layout dividido em helpers privados de grade, cabeçalho, ações, busca, filtros, listagem e detalhe.

- DecisionsDarkPanel: seção de filtros dividida em helpers privados para controles de level, DTE, botões e resumo.

- DecisionsDarkPanel: _render_rows dividido em helpers privados para limpeza, estado vazio, renderização de linhas e aviso de limite.

- DecisionsDarkPanel: consolidação dos métodos grandes restantes (reload, índice de estruturas, heurística de estrutura ativa, busca, exportação CSV e detalhe textual) em helpers privados menores, preservando comportamento funcional.

- DecisionsDarkPanel: finalização dos métodos médios restantes (_build_detail_section, _update_filter_summary, _apply_filter, _select_decision e _format_detail_header), extraindo helpers privados menores e preservando comportamento funcional.

- DetailsPanel: quebra inicial dos métodos grandes (_get_latest_snapshot_timestamp_for_structure, _setup_widgets, update_decision, update_operational_state e _on_recalculate_click), extraindo helpers privados menores e preservando regras de fallback de DB, estado operacional e recálculo.

- TerminalVWAPPayoffDarkPanel: quebra de _setup_layout em helpers privados de grade, rail, side panel, main panel, header, KPIs, charts, painel inferior, tabela de pernas e avisos, preservando layout e comportamento funcional.

- TerminalVWAPPayoffDarkPanel: quebra dos renderizadores laterais de estruturas, ações, ajuste e histórico de decisões em helpers privados menores, preservando callbacks, textos, status e comportamento visual.

- TerminalVWAPPayoffDarkPanel: quebra de _build_rail_panel em helpers privados menores, preservando composição visual do rail, comandos existentes e comportamento operacional.

- TerminalVWAPPayoffDarkPanel: normalização semântica dos helpers do rail, removendo helpers genéricos part_* e preservando composição visual, comandos e comportamento operacional.

- TerminalVWAPPayoffDarkPanel: quebra de _render_vwap_chart em helpers privados menores, preservando assinatura original, renderização visual do gráfico VWAP, dados carregados e comportamento operacional.

- TerminalVWAPPayoffDarkPanel: quebra de _load_legs em helpers privados semânticos, preservando seleção da tabela de pernas, resolução de colunas, SQL, retornos vazios e fechamento da conexão.

- TerminalVWAPPayoffDarkPanel: quebra de _calculate_payoff_from_legs em helpers privados para coleta de strikes, range de spot, pontos da curva e payoff por perna, preservando fórmula, sinais, prêmios, quantidades, multiplicadores e fallback sem strikes.

- TerminalVWAPPayoffDarkPanel: quebra de duplicate_selected_structure em helpers privados para disponibilidade do repositório, carregamento da estrutura origem, criação da cópia, duplicação das pernas e atualização visual, preservando mensagens, status, seleção, cópia de payload e tratamento de erro.

- Nota técnica: durante validação manual foi observada divergência existente entre dados/app.db e dados/derived.db; estruturas/decisões gravadas pelo fluxo moderno podem não aparecer em consultas realizadas contra o banco volátil legado derived.db. Correção arquitetural deve ser tratada em etapa própria de consolidação do banco canônico.

- TerminalVWAPPayoffDarkPanel: quebra de archive_selected_structure em helpers privados para carregamento da estrutura, resolução do nome, detecção de arquivamento prévio, confirmação, cancelamento, arquivamento via repositório, atualização visual e mensagem de sucesso, preservando fluxo, mensagens, status, renderização e tratamento de erro.

---

## 35. Refatoracao tecnica de metodos longos da UI

Foi executada uma rodada de refatoracao tecnica focada em reduzir metodos longos da camada UI, sem alterar comportamento funcional, layout, banco de dados, regra de negocio ou contratos publicos.

### 35.1. Objetivo

Reduzir blocos grandes de codigo em arquivos ja envolvidos na frente moderna/dark, melhorando:

- legibilidade;
- manutencao;
- isolamento de responsabilidades;
- testabilidade;
- controle de risco em proximas alteracoes.

A rodada seguiu a diretriz de nao criar divida tecnica, especialmente em areas relacionadas a payoff, decisoes e mercado vivo.

### 35.2. Arquivos alterados

Arquivos alterados nesta rodada:

- UI/components/payoff_chart.py
- UI/models/ui_data.py

### 35.3. Refatoracao do fluxo de renderizacao do grafico de payoff

Foi refatorado o fluxo de renderizacao do grafico de payoff.

Commit associado:

- e68842a refactor(ui): split payoff chart rendering flow

Arquivo alterado:

- UI/components/payoff_chart.py

Escopo:

- dividir o metodo grande de desenho do grafico em helpers menores;
- preservar o comportamento visual;
- preservar comparacao de curvas;
- preservar spot_ref;
- preservar breakevens;
- preservar anotacoes e titulo;
- preservar exportacao e integracao com Matplotlib.

Resultado:

- fluxo principal ficou mais legivel;
- responsabilidades de desenho foram separadas;
- o arquivo deixou de aparecer no ranking de funcoes/metodos com 50+ linhas.

### 35.4. Refatoracao do fluxo de consulta de decisoes

Foi refatorado o metodo UIDataModel.get_decisions.

Commit associado:

- bb88c11 refactor(ui): split decisions query flow

Arquivo alterado:

- UI/models/ui_data.py

Escopo:

- separar montagem da expressao pl_pct_of_max;
- separar montagem dos campos do SELECT;
- preservar derivacao compativel entre structure_id e aba;
- separar montagem da subquery;
- separar filtros de data;
- separar filtro de estrutura;
- separar filtros simples;
- separar construcao final do SQL;
- separar execucao da consulta;
- separar normalizacao das linhas retornadas.

Resultado:

- UIDataModel.get_decisions deixou de concentrar todo o fluxo em um unico metodo longo;
- o contrato de retorno foi preservado;
- a conexao local por chamada continuou sendo fechada corretamente;
- o metodo deixou de aparecer no ranking de funcoes/metodos com 50+ linhas.

### 35.5. Validacoes executadas

Validacoes executadas apos a refatoracao de UI/models/ui_data.py:

- python -m py_compile UI/models/ui_data.py
- git diff --check
- git diff --stat
- git diff -- UI/models/ui_data.py

Resultado observado:

- compilacao Python aprovada;
- git diff --check sem apontar erro;
- alteracao revisada antes do commit;
- backup temporario removido apos commit.

### 35.6. Commit da rodada

Commit registrado:

- bb88c11 refactor(ui): split decisions query flow

Alteracao registrada pelo Git:

- 1 arquivo alterado
- 188 insercoes
- 121 delecoes

### 35.7. Estado atual do ranking de metodos longos

Apos as refatoracoes, get_decisions nao aparece mais no ranking de funcoes/metodos com 50+ linhas.

Ranking atual observado:

- 123 linhas | UI\models\ui_data.py | UIDataModel.get_payoff_curve_info | 543-665
- 81 linhas | UI\main_window.py | MainWindow.recalculate_structure | 355-435
- 80 linhas | UI\components\filters_panel.py | FiltersPanel._setup_widgets | 15-94
- 79 linhas | UI\components\structure_editor_dialog.py | StructureEditorDialog._cmd_fill_leg_from_rtd | 499-577
- 77 linhas | UI\components\structure_editor_dialog.py | StructureEditorDialog._build_ui | 117-193
- 74 linhas | UI\main_window.py | MainWindow._start_payoff_load | 199-272
- 74 linhas | UI\models\ui_data.py | UIDataModel.get_payoff_curve | 468-541
- 73 linhas | UI\modern\main_window.py | ModernMainWindow._start_payoff_load | 356-428
- 67 linhas | UI\modern\main_window.py | ModernMainWindow.recalculate_structure | 625-691
- 65 linhas | UI\main_window.py | MainWindow.refresh_data | 274-338
- 62 linhas | UI\components\structure_editor_dialog.py | StructureEditorDialog._refresh_rtd_symbol_on_demand | 411-472
- 62 linhas | UI\components\terminal_vwap_payoff_panel.py | TerminalVWAPPayoffPanel._build_summary_tab | 276-337
- 61 linhas | UI\main_window.py | MainWindow._setup_layout | 64-124
- 61 linhas | UI\components\structure_editor_dialog.py | StructureEditorDialog._build_leg_form | 195-255
- 61 linhas | UI\modern\main_window.py | ModernMainWindow.refresh_data | 491-551
- 57 linhas | UI\components\terminal_vwap_payoff_panel.py | TerminalVWAPPayoffPanel._build_left_panel | 199-255
- 57 linhas | UI\modern\main_window.py | ModernMainWindow.worker | 370-426
- 53 linhas | UI\main_window.py | MainWindow.run_pipeline | 437-489
- 53 linhas | UI\main_window.py | MainWindow._setup_terminal_vwap_payoff_tab | 698-750

### 35.8. Decisao de seguranca

Esta rodada foi tecnica e nao funcional.

Nao foram alterados:

- banco de dados;
- schema;
- regra de negocio;
- layout operacional;
- entrypoint principal;
- contratos canonicos;
- comportamento esperado da UI;
- modo dark como UI moderna paralela;
- diretriz de manter a UI atual ate equivalencia funcional minima.

### 35.9. Proxima frente recomendada

A proxima frente tecnica recomendada e continuar em UI/models/ui_data.py, pois ainda existem dois metodos longos no mesmo arquivo.

Prioridade recomendada:

1. UIDataModel.get_payoff_curve_info
2. UIDataModel.get_payoff_curve

Motivo:

- get_payoff_curve_info possui 123 linhas;
- get_payoff_curve possui 74 linhas;
- ambos estao relacionados ao fluxo de payoff;
- refatorar esses metodos melhora a base usada pela UI atual, shell moderno e modo dark.

Escopo recomendado para get_payoff_curve_info:

- separar inicializacao de cache e metadados;
- separar consulta canonica em payoff_curve_points;
- separar fallback para timestamp mais recente;
- separar consulta alternativa quando aplicavel;
- separar montagem dos pontos;
- separar atualizacao do objeto info;
- separar persistencia em cache.

Restricoes preservadas para a proxima frente:

- nao alterar banco;
- nao alterar regra de negocio;
- nao alterar layout;
- nao trocar entrypoint;
- nao eliminar UI atual;
- manter commits pequenos e rastreaveis;
- validar com py_compile, git diff --check e ranking de metodos longos.

## Checkpoint - UIDataModel payoff colmap

- Arquivo auditado: `UI/models/ui_data.py`.
- Refactor aplicado em `UIDataModel._build_payoff_colmap`.
- O metodo original de 44 linhas foi quebrado em helpers menores:
  - `_payoff_colmap_missing_table`;
  - `_payoff_column_aliases`;
  - `_build_colmap_from_aliases`;
  - `_ensure_required_payoff_colmap`;
  - `_warn_missing_payoff_structure_id`.
- A responsabilidade principal passou a ser orquestrada por helpers:
  - tratar tabela de payoff ausente;
  - selecionar aliases canonicos ou flexiveis;
  - montar o colmap;
  - validar colunas obrigatorias;
  - avisar ausencia de `structure_id`.
- A alteracao nao modifica banco, schema, repositories, services, controllers ou regra de negocio.
- Validacoes executadas:
  - `python -m py_compile UI/models/ui_data.py`;
  - `git diff --check`;
  - ranking AST de metodos por tamanho.
- Resultado do ranking apos o refactor:
  - `UIDataModel.get_payoff_curve_info`: 38 linhas.
- Observacao operacional:
  - uma tentativa anterior de patch corrompeu quebras de linha em `UI/models/ui_data.py`;
  - ela foi revertida com `git reset --hard HEAD~1` antes da reaplicacao correta.

---

## Frente 54 - Inventario do proximo refactor interno da UI

Status: inventario concluido
Data: 2026-07-03
Branch: refactor/decisions-dark-panel-large-block
Baseline: 9cd8632
Relatorio: reports/ui_refactor/54_next_internal_refactor_inventory.txt

### 54.1. Objetivo

Identificar o proximo alvo seguro de refatoracao interna da UI apos a consolidacao do arquivo canonico de auditoria e apos o checkpoint de split do builder de colunas de payoff.

### 54.2. Restricoes preservadas

- nao alterar banco de dados
- nao alterar contratos canonicos
- nao alterar services, controllers ou repositories
- nao trocar entrypoint principal
- nao recriar regra de negocio na UI
- nao editar copia de auditoria fora de reports/auditoria/AUDITORIA_REFACTOR_UI.md

### 54.3. Inventario executado

Foi gerado inventario AST dos metodos e funcoes sob UI/, priorizando candidatos longos e arquivos ja trabalhados na frente atual.

Arquivo gerado:

- reports/ui_refactor/54_next_internal_refactor_inventory.txt

### 54.4. Top inicial de candidatos

| linhas | arquivo | simbolo | inicio | fim |
|---:|---|---|---:|---:|
| 81 | UI/main_window.py | MainWindow.recalculate_structure | 355 | 435 |
| 80 | UI/components/filters_panel.py | FiltersPanel._setup_widgets | 15 | 94 |
| 79 | UI/components/structure_editor_dialog.py | StructureEditorDialog._cmd_fill_leg_from_rtd | 499 | 577 |
| 77 | UI/components/structure_editor_dialog.py | StructureEditorDialog._build_ui | 117 | 193 |
| 74 | UI/main_window.py | MainWindow._start_payoff_load | 199 | 272 |
| 73 | UI/modern/main_window.py | ModernMainWindow._start_payoff_load | 356 | 428 |
| 67 | UI/modern/main_window.py | ModernMainWindow.recalculate_structure | 625 | 691 |
| 65 | UI/main_window.py | MainWindow.refresh_data | 274 | 338 |
| 62 | UI/components/structure_editor_dialog.py | StructureEditorDialog._refresh_rtd_symbol_on_demand | 411 | 472 |
| 62 | UI/components/terminal_vwap_payoff_panel.py | TerminalVWAPPayoffPanel._build_summary_tab | 276 | 337 |
| 61 | UI/components/structure_editor_dialog.py | StructureEditorDialog._build_leg_form | 195 | 255 |
| 61 | UI/main_window.py | MainWindow._setup_layout | 64 | 124 |
| 61 | UI/modern/main_window.py | ModernMainWindow.refresh_data | 491 | 551 |
| 57 | UI/components/terminal_vwap_payoff_panel.py | TerminalVWAPPayoffPanel._build_left_panel | 199 | 255 |
| 57 | UI/modern/main_window.py | worker | 370 | 426 |

### 54.5. Decisao de seguranca

Nenhum codigo funcional foi alterado nesta etapa.

A proxima alteracao deve ser escolhida a partir do ranking gerado, preferindo extracao de helpers privados pequenos, sem mudanca de assinatura publica e sem alteracao de comportamento.

### 54.6. Validacoes executadas

Comandos obrigatorios apos o inventario:

- git status --short
- git diff --check

### 54.7. Proximo passo

Selecionar o metodo mais seguro do ranking atual e executar refactor interno minimo, com validacao por py_compile e novo registro neste documento canonico.
# Triagem formal da fatia Decisoes dark panel

## Decisao

A frente UI completa permanece aberta.

A fatia `Decisoes no modo dark` pode ser considerada em estado de **equivalencia parcial operacional**, desde que as validacoes tecnicas finais continuem aprovadas.

Esta decisao nao autoriza:

- eliminar a UI atual;
- trocar o entrypoint principal;
- alterar banco de dados;
- alterar regra de negocio;
- declarar equivalencia funcional completa da UI moderna dark.

## Escopo encerravel nesta fatia

A equivalencia parcial operacional da aba Decisoes no modo dark cobre:

- consulta/listagem de decisoes;
- filtro simples/busca textual;
- selecao de decisao;
- leitura de detalhe textual enriquecido;
- copia do detalhe;
- exportacao CSV da listagem filtrada;
- carregamento/acionamento da estrutura associada no Terminal VWAP;
- robustez basica das acoes dependentes de selecao/status.

## Reclassificacoes formais

### 1. Criterio de encerramento global

Itens que afirmam que a UI atual ainda nao deve ser eliminada permanecem verdadeiros, mas sao classificados como criterio global de substituicao da UI, nao como bloqueio para encerrar a fatia parcial de Decisoes.

Classificacao:

`CRITERIO_GLOBAL_UI`

### 2. Filtros avancados de decisoes

Itens sobre filtros avancados, ordenacao visual, estados vazios, contagem filtrada versus total e ergonomia dos botoes sao reclassificados como proximas frentes pequenas.

Classificacao:

`BACKLOG_MELHORIA_UI_DECISOES`

### 3. Rationale/why JSON

Itens sobre `rationale/why JSON` ficam reclassificados como melhoria de detalhamento/equivalencia futura, salvo se for definido como requisito obrigatorio de equivalencia completa.

Classificacao:

`BACKLOG_MELHORIA_UI_DECISOES`

### 4. Divergencia dados/app.db versus dados/derived.db

A divergencia observada entre banco canonico moderno e banco volatil legado deve ser tratada em frente propria de banco/dados/pipeline.

Classificacao:

`BANCO_DADOS_PIPELINE`

### 5. Terminal VWAP, payoff e UIDataModel

Itens sobre Terminal VWAP, payoff curve, `UI/models/ui_data.py` e refatoracoes tecnicas de payoff ficam fora do escopo desta branch de Decisoes dark panel.

Classificacao:

`FORA_ESCOPO_BRANCH_DECISOES_DARK`

### 6. Relatorios historicos superados

Relatorios anteriores que indicavam ausencia total de filtros, tabela, selecao e detalhe em Decisoes dark foram parcialmente superados por implementacoes posteriores registradas na auditoria.

Classificacao:

`HISTORICO_SUPERADO_PARCIALMENTE`

## Pendencias que ainda podem bloquear esta fatia

Antes de considerar a fatia pronta para commit/merge, validar:

- py_compile dos arquivos alterados;
- git diff --check;
- smoke manual da aba Decisoes;
- selecao vazia/invalida nao quebra botoes dependentes;
- copia/exportacao/status funcionam;
- carregamento de estrutura associada funciona;
- nao houve alteracao em banco, regra de negocio, services, repositories ou entrypoint principal.

## Conclusao

A branch atual nao deve tentar resolver toda a frente UI.

O caminho recomendado e encerrar documentalmente apenas a fatia `Decisoes dark panel - equivalencia parcial operacional`, deixando os demais itens como backlog, banco/pipeline, criterio global ou fora de escopo.

---

## Checkpoint final - Decisoes dark panel equivalencia parcial operacional

### Resultado tecnico

Validacoes executadas:

    python -m py_compile UI/components/decisions_dark_panel.py UI/modern/dark_window.py UI/components/terminal_vwap_payoff_dark_panel.py UI/models/ui_data.py
    git diff --check

Resultado:

- py_compile: aprovado sem erros.
- git diff --check: aprovado; houve apenas aviso de conversao LF/CRLF no documento de auditoria.

### Verificacao estrutural dos callbacks

Foi verificada a presenca dos fluxos relevantes:

- selecao de decisao;
- validacao de indice selecionado;
- copia de detalhe;
- carregamento da estrutura associada;
- duplicacao de estrutura;
- arquivamento de estrutura;
- recalculo de payoff;
- registro das decisoes ADJUST e CLOSE;
- mensagens operacionais via _safe_status.

### Decisao de encerramento da fatia

A fatia Decisoes dark panel fica classificada como:

    EQUIVALENCIA_PARCIAL_OPERACIONAL

Esta classificacao nao encerra a frente UI completa e nao autoriza substituir a UI atual.

### Itens reclassificados fora do bloqueio desta fatia

- filtros avancados de decisoes: BACKLOG_MELHORIA_UI_DECISOES;
- rationale/why JSON: BACKLOG_MELHORIA_UI_DECISOES;
- divergencia dados/app.db versus dados/derived.db: BANCO_DADOS_PIPELINE;
- Terminal VWAP/payoff/UIDataModel: FORA_ESCOPO_BRANCH_DECISOES_DARK;
- relatorios historicos antigos de ausencia total: HISTORICO_SUPERADO_PARCIALMENTE.

### Conclusao operacional

A branch atual deve ser encerrada como entrega parcial e restrita de Decisoes no modo dark, mantendo a UI atual como caminho principal e preservando banco de dados, regra de negocio, entrypoint, services, repositories e contratos canonicos.

---

## Checkpoint roadmap UI remanescente - Decisoes dark panel encerrado parcialmente

Data: 2026-07-03 15:55:24 -0300

Branch: refactor/decisions-dark-panel-large-block

### Estado atual registrado

A fatia Decisoes dark panel foi encerrada como:

    EQUIVALENCIA_PARCIAL_OPERACIONAL

Esta classificacao encerra apenas a entrega parcial e restrita da aba/painel de Decisoes no modo dark.

Nao encerra a frente UI completa.

A UI atual/canonica permanece como caminho principal ate que exista criterio global de equivalencia, regressao e substituicao controlada.

### O que foi considerado encerrado nesta fatia

- equivalencia operacional parcial da area de Decisoes no modo dark;
- callbacks essenciais presentes e documentados;
- selecao de decisao com validacao de indice;
- copia de detalhe;
- carregamento da estrutura associada;
- duplicacao de estrutura;
- arquivamento de estrutura;
- recalculo de payoff;
- registro de decisoes ADJUST e CLOSE;
- mensagens operacionais via _safe_status;
- preservacao de banco de dados, regra de negocio, services, repositories, entrypoint e contratos canonicos.

### Pendencias remanescentes da frente UI

As pendencias abaixo ficam fora do bloqueio desta branch e devem ser tratadas em frentes proprias.

#### 1. Backlog de melhorias da UI de Decisoes

Classificacao:

    BACKLOG_MELHORIA_UI_DECISOES

Itens:

- filtros avancados de decisoes;
- exibicao estruturada de rationale/why JSON;
- refinamentos visuais e ergonomicos;
- validacao manual ampliada de selecao vazia, selecao invalida e botoes dependentes;
- criterios adicionais de navegacao, ordenacao e leitura da tabela;
- revisao futura para eventual equivalencia completa com a UI atual.

#### 2. Criterio global de equivalencia da UI

Classificacao:

    CRITERIO_GLOBAL_UI

Itens:

- montar matriz de equivalencia entre UI atual/canonica e UI moderna/dark;
- definir quais telas podem ser consideradas equivalentes, parciais ou apenas experimentais;
- criar checklist minimo por aba;
- registrar criterios de substituicao segura;
- impedir troca do caminho principal sem validacao funcional e operacional.

#### 3. Terminal VWAP, payoff e UIDataModel

Classificacao:

    FORA_ESCOPO_BRANCH_DECISOES_DARK

Itens:

- Terminal VWAP;
- payoff curve;
- UI/models/ui_data.py;
- refatoracoes tecnicas de payoff;
- validacoes especificas de fluxo do terminal;
- consistencia de dados consumidos pela UI moderna.

Esta frente deve ser auditada separadamente, sem ser misturada com a entrega de Decisoes dark panel.

#### 4. Banco, dados e pipeline

Classificacao:

    BANCO_DADOS_PIPELINE

Itens:

- divergencia entre banco canonico moderno e banco volatil legado;
- verificacao de dados/app.db versus dados/derived.db;
- rastreio de origem dos dados exibidos;
- confirmacao dos contratos de leitura usados pela UI;
- saneamento de pipeline antes de qualquer conclusao global de UI.

Esta frente nao deve ser corrigida dentro de branch visual de Decisoes.

#### 5. Regressao e smoke manual da UI

Classificacao:

    REGRESSAO_UI

Itens:

- roteiro manual por aba;
- validacao de abertura da aplicacao pelo entrypoint principal;
- validacao de navegacao entre abas;
- validacao de acoes sem selecao;
- validacao de dados ausentes;
- validacao de mensagens de status;
- validacao visual em dark mode;
- registro de evidencias minimas antes de merge amplo.

#### 6. Estrategia de encerramento da frente UI

Classificacao:

    PLANO_ENCERRAMENTO_UI

Ordem sugerida:

1. manter a UI atual/canonica como caminho principal;
2. concluir documentacao das pendencias por classificacao;
3. abrir frentes pequenas e separadas por area;
4. evitar misturar banco, regra de negocio, services e UI visual na mesma branch;
5. validar cada fatia com py_compile, git diff --check e smoke manual;
6. somente discutir substituicao da UI atual apos matriz global de equivalencia.

### Decisao operacional

A branch atual pode seguir como encerrada para a fatia Decisoes dark panel, mas a frente UI permanece aberta.

Proximo trabalho recomendado:

    documentar matriz global de equivalencia UI
    separar backlog de Decisoes
    abrir auditoria propria para Terminal VWAP/payoff/UIDataModel
    abrir frente propria para banco/dados/pipeline

### Regra de preservacao

Enquanto a frente UI nao estiver encerrada globalmente, devem permanecer preservados:

- banco de dados;
- regras de negocio;
- services;
- repositories;
- entrypoint principal;
- contratos canonicos;
- UI atual como caminho principal.
