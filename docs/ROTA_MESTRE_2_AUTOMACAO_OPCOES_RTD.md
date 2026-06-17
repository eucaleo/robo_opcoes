“ROTA MESTRE”

Índice ROTA_MESTRE_1 pgs 2-22
	- Importante
	- Objetivos e finalização
	- Rota de Desenvolvimento do projeto
	- Estratégia Central Re- fatorada
	- Nova Divisão de Fases Rota_Mestre_1
	- Fase 0 – Marco de Controle e Congelamento da Rota - (FINALIZADO E TESTADO)
	- Fase 1 – Higiene do Repositório e Estado Inicial	      - (FINALIZADO E TESTADO)
	- Fase 2 – Diagnóstico do Fluxo Atual		      - (FINALIZADO E TESTADO)
	- Fase 3 – Classificação da Fonte de Dados		      - (FINALIZADO E TESTADO)
	- Fase 4 – Auditoria de Dependência do Excel	      - (FINALIZADO E TESTADO)
	- Fase 5 – Definição do Contrato RTD		      - (FINALIZADO E TESTADO)
	- Fase 6 – Consolidação da Camada BRIDGE RTD	      - (FINALIZADO E TESTADO)
	- Fase 7 – Ingestão Bruta do RTD			      - (FINALIZADO E TESTADO)
	- Fase 8 – Banco como Fonte da Verdade		      - (FINALIZADO E TESTADO)
	- Fase 9 – Cadastro e Persistência de Estruturas      	      - (FINALIZADO E TESTADO)
	- Fase 10 – Motor de Cálculo Interno		      - (FINALIZADO E TESTADO)
	- Fase 11 – Snapshots e Histórico do Sistema 	      - (FINALIZADO E TESTADO)
	- Fase 12 – Encerramentos, Rolls e Eventos Operacionais - (FINALIZADO E TEST )
	- Fase 13 – Refatoração da UI			      - (FINALIZADO E TESTADO)
	- Fase 14 – Migração de Dados Legados		      - (FINALIZADO E TESTADO)
	- Fase 15 – Validação Integrada			      - (FINALIZADO E TESTADO)
	- Fase 16 – Limpeza, Versionamento e Release	      - (FINALIZADO E TESTADO)
	- Fase 17 – MAPA de Pastas e Arquivos		      - (FINALIZADO E TESTADO)
	- Estado geral do Projeto
	- Estrutura Principal do Projeto

Índice ROTA_MESTRE_2 pgs 23…

	- Regras de segurança do ciclo

	- Fase 1 — Mapeamento amplo de RTD, Excel, Bridge, Serviços e UI
- Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv
- Fase 3 — Auditoria da persistência de cotações
- Fase 4 — Auditoria do fluxo de snapshot de mercado
- Fase 5 — Definição do contrato canônico de cotação de opção
- Fase 6 — Importador somente-leitura do RTD_LINKS
- Fase 7 — Persistência controlada das cotações
- Fase 8 — Integração com snapshot/serviços
- Fase 9 — Integração controlada com cálculo
- Fase 10 — Exposição na UI
- Fase 11 — Testes integrados
- Fase 12 — Fechamento do ciclo
	
Importante:

A)	NÃO MIGRAR PARA WEB
B)	NÃO UTILIZAR EMOJIS
C)	MANTER-SE AO SCOPO DO PROJETO SEM DERIVAÇÕES
D)	EFETUAR BUSCAS DE DADOS E ARQUIVOS ANTES DE ALTERAÇÕES 
E)	TODA MUDANÇA DEVE SER TESTADA APOS CONCLUIDA
F)	APOS O ENCERRAMENTO DE FASE O TESTE DEVE COMPOR TODAS AS FASES ENCERRADAS, ASSIM NÃO FICARA PENDENCIAS
G)	EVITAR CODIGOS INTERMEDIARIOS EM EXPLICAÇÕES, IR DIRETO AO PONTO
H)	EM ALTERAÇÕES SEMPRE GERAR CODIGO INTEIRO DO ARQUIVO
I)	A CADA ALTERAÇÃO CONCLUIDA E TESTADA, COMMITAR.
J)	NÃO CODAR SEM RUMO, SE NECESSARIO BUSCAR A EVOLUÇÃO NO GIT
K)	CRIAR ARQUIVO DE AUDITORIA PRA SER ATUALIZADO COM OS TESTES, ASSIM VAMOS TESTANDO AS CONCLUSOES E CRIANDO O CAMINHO DE EVOLUÇÃO AO MESMO TEMPO AUDITANDO O QUE ESTA PRONTO
 

OBJETIVOS E FINALIZAÇÃO

O sistema tem como objetivo ser uma plataforma local de controle, análise e acompanhamento de operações com ações e opções, utilizando o Excel apenas como ponte de captura de dados RTD do BTG, e não como fonte da verdade operacional.
A fonte principal de dados deve ser o banco do próprio sistema, onde serão armazenadas as cotações, estruturas, pernas, eventos, configurações, cálculos, snapshots e históricos necessários para o funcionamento completo da aplicação.
O sistema deve integrar quatro blocos principais:
1.	Excel / RTD
•	Usado somente para capturar dados brutos de mercado via RTD.
•	Deve exportar essas informações para arquivos simples de ponte.
•	Não deve ser responsável por cálculos principais, controle de estruturas, histórico, PL, alertas ou decisões operacionais.
2.	Bridge / Ingestão
•	Responsável por transportar os dados brutos do Excel para o sistema.
•	Deve validar, normalizar e importar os dados para o banco.
•	Deve evitar duplicidades, dados vazios inválidos e sobrescrita indevida de informações úteis.
3.	Banco / Repositórios / Serviços
•	Deve ser a fonte da verdade do sistema.
•	Deve armazenar estruturas, pernas, cotações, configurações, eventos, snapshots e dados derivados.
•	Deve conter o motor interno de cálculo responsável por gerar métricas, riscos, PL, alertas e consolidações.
•	Deve substituir gradualmente qualquer dependência de abas calculadas do Excel.
4.	Interface Gráfica
•	Deve exibir informações consolidadas e atuais vindas do banco, repositórios e serviços.
•	Não deve acessar diretamente o Excel nem depender de CSVs derivados antigos.
•	Deve permitir visualizar estruturas, pernas, métricas, histórico, alertas e, futuramente, cadastrar ou alterar eventos operacionais.
Funções Principais Esperadas
O sistema deve ser capaz de:
•	capturar cotações brutas de ativos e opções via RTD;
•	importar snapshots de mercado para o banco;
•	cadastrar e manter estruturas de operações;
•	registrar pernas, posições e eventos operacionais;
•	armazenar configurações e parâmetros de cálculo;
•	calcular métricas por perna e por estrutura;
•	calcular PL realista, gregas líquidas, spreads, DTE, riscos e alertas;
•	gerar snapshots periódicos de pernas e estruturas;
•	manter histórico operacional independente do Excel;
•	registrar encerramentos, ajustes e rolls;
•	alimentar a UI com dados atuais e consistentes;
•	permitir rastreabilidade entre dado bruto, cálculo, snapshot e exibição;
•	reduzir o risco de dados antigos ou planilhas desatualizadas afetarem a operação.
Funcionamento Esperado ao Final
Ao final da implementação, o fluxo esperado será:
1.	O BTG envia dados de mercado ao Excel via RTD.
2.	O Excel apenas captura esses dados brutos e os exporta para a bridge.
3.	O sistema importa os dados RTD, valida e grava no banco.
4.	As estruturas e pernas são cadastradas e mantidas dentro do sistema.
5.	O motor de cálculo interno combina estruturas, posições, cotações e configurações.
6.	O sistema calcula PL, gregas, spreads, DTE, alertas, riscos e consolidações.
7.	Snapshots periódicos são gravados para formar histórico próprio.
8.	A interface gráfica exibe dados atuais diretamente do sistema.
9.	O Excel deixa de ser dependência operacional e passa a atuar somente como gateway RTD.
Com isso, o sistema passa a funcionar de forma autônoma, rastreável e segura, sem depender de abas antigas ou cálculos da planilha para atualizar posições, criar estruturas, calcular resultados ou alimentar a visualização.

Rota de Desenvolvimento do Projeto 
Sem WEB. Sem atalhos desnecessários. Sem misturar fases.
________________________________________

A melhor decisão agora é:
1.	Sintetizar a estratégia nova
2.	Reorganizar as fases
3.	Transformar isso na nova ROTA_MESTRE_1
4.	Commitar como marco documental
5.	Só depois voltar ao desenvolvimento técnico
Ou seja: antes de mexer no sistema, precisamos travar o plano.
________________________________________
Estratégia Central Refatorada
A nova direção do projeto deve ser:
O Excel deixa de ser fonte operacional e passa a ser apenas gateway RTD.
O sistema passa a ser a fonte da verdade, responsável por banco, estruturas, cálculos, snapshots, histórico e UI.
A partir disso, todo desenvolvimento deve seguir esta lógica:
1.	Identificar dependências antigas do Excel
2.	Separar dados brutos de dados calculados
3.	Formalizar contrato RTD
4.	Persistir dados brutos no banco
5.	Criar ou corrigir cadastro de estruturas
6.	Criar motor de cálculo interno
7.	Gerar snapshots pelo sistema
8.	Fazer UI consumir apenas dados do sistema
9.	Usar abas antigas apenas como legado, comparação ou migração
________________________________________
Nova Divisão de Fases da ROTA_MESTRE_1
Fase 0 — Marco de Controle e Congelamento da Rota
Objetivo
Travar a nova estratégia antes de continuar o desenvolvimento.
Escopo
Consolidar a ROTA_MESTRE_1 como documento norteador atualizado.
Decisões fixadas
•	Excel é apenas ponte RTD.
•	Banco de dados é a fonte da verdade.
•	UI não deve depender de CSVs derivados antigos.
•	Abas calculadas do Excel são legado.
•	Cálculos devem migrar para o sistema.
•	Novas estruturas devem nascer no sistema, não na planilha.
Entregável
Nova ROTA_MESTRE_1 refatorada e commitada.
Critério de saída
Documento revisado, aceito e versionado.
________________________________________
Fase 1 — Higiene do Repositório e Estado Inicial
Objetivo
Garantir que o projeto esteja em estado seguro antes de qualquer alteração técnica.
Escopo
Verificar:
•	branch atual;
•	alterações locais;
•	arquivos sensíveis;
•	stashes;
•	arquivos não rastreados;
•	risco de sobrescrever dados operacionais.
Atenção especial
Arquivos sensíveis:
•	LISTA_RTD.xlsm
•	arquivos da pasta bridge/
•	CSVs operacionais
•	arquivos gerados pelo Excel
Critério de saída
Working tree limpo ou com alterações conscientemente classificadas.
________________________________________
Fase 2 — Diagnóstico do Fluxo Atual
Objetivo
Entender como o sistema está funcionando hoje, antes de corrigir.
Perguntas principais
1.	De onde o sistema lê as estruturas?
2.	De onde ele lê as pernas das operações?
3.	De onde vêm bid, ask, last, gregas e volatilidade?
4.	Onde o sistema grava dados importados?
5.	A UI lê do banco, CSV ou Excel?
6.	Novas estruturas estão sendo persistidas?
7.	O sistema depende de ANALISE_ROBO, ANALISE_ROBO_LEGS ou HIST_ROBO?
Módulos analisados
•	Excel
•	bridge
•	ingestão
•	banco
•	repositories
•	scripts
•	UI models
•	UI components
Critério de saída
Mapa claro do fluxo atual.
________________________________________
Fase 3 — Classificação das Fontes de Dados
Objetivo
Separar o que é entrada legítima do que é dado derivado antigo.
Fonte bruta permitida
•	RTD vindo do BTG
•	LISTA RTD
•	CSV bruto exportado do Excel
•	cadastro manual de estruturas
•	configurações iniciais
Fonte derivada legada
•	ANALISE_ROBO
•	ANALISE_ROBO_LEGS
•	HIST_ROBO
•	analise_robo.csv
•	analise_robo_legs.csv
•	hist_robo.csv
•	consolidações calculadas pelo Excel
Regra
Fonte derivada não deve alimentar o sistema como verdade principal.
Critério de saída
Cada fonte de dado classificada como:
•	entrada bruta;
•	configuração;
•	legado;
•	derivado;
•	operacional;
•	temporário;
•	descartável.
________________________________________
Fase 4 — Auditoria de Dependência do Excel
Objetivo
Descobrir exatamente onde o sistema ainda depende das abas e CSVs antigos.
Alvos da auditoria
•	referências a abas do Excel;
•	referências a CSVs derivados;
•	leituras diretas da pasta bridge/;
•	dependências da UI em arquivos temporários;
•	dependência de cálculo pronto vindo da planilha.
Abas críticas
•	CONFIGURACOES
•	ANALISE_ROBO
•	ANALISE_ROBO_LEGS
•	HIST_ROBO
•	ENCERRAMENTOS_MANUAIS
Critério de saída
Lista objetiva de arquivos e funções que ainda dependem do Excel como fonte operacional.
________________________________________
Fase 5 — Definição do Contrato RTD
Objetivo
Padronizar o que o Excel entrega ao sistema.
Base
A LISTA RTD passa a ser o modelo de referência da conexão BTG.
Campos brutos esperados
Para ativos:
•	ticker;
•	bid;
•	ask;
•	último;
•	abertura;
•	fechamento;
•	máxima;
•	mínima;
•	volume;
•	VWAP;
•	volatilidade implícita;
•	horário da cotação;
•	origem.
Para opções:
•	ticker da opção;
•	ativo objeto;
•	tipo da opção;
•	strike;
•	vencimento;
•	bid;
•	ask;
•	último;
•	delta;
•	gamma;
•	theta;
•	vega;
•	volatilidade implícita;
•	horário da cotação;
•	origem.
Critério de saída
Contrato de campos definido entre Excel/RTD e sistema.
________________________________________
Fase 6 — Consolidação da Camada Bridge RTD
Objetivo
Transformar a bridge em transporte previsível de dados brutos.
Nova responsabilidade da bridge
Transportar dados RTD sem calcular regra de negócio.
A bridge pode conter
•	snapshot bruto RTD;
•	mapa de campos;
•	erros de importação;
•	arquivos temporários de integração.
A bridge não deve conter como fonte principal
•	análise consolidada;
•	PL calculado;
•	alertas;
•	histórico oficial;
•	estrutura operacional definitiva.
Critério de saída
Bridge organizada entre dados brutos, configuração, legado e arquivos descartáveis.
________________________________________
Fase 7 — Ingestão Bruta RTD
Objetivo
Importar dados brutos RTD para o banco.
Responsabilidade
A ingestão deve:
•	ler dados brutos;
•	validar estrutura;
•	normalizar campos;
•	impedir duplicidade;
•	evitar sobrescrever dados válidos com vazios;
•	gravar no banco;
•	retornar resumo claro.
Não deve fazer
•	cálculo de PL;
•	cálculo de risco;
•	alerta de roll;
•	consolidação de estrutura;
•	cálculo de gregas agregadas.
Critério de saída
RTD pode ser importado várias vezes sem duplicar nem corromper dados.
________________________________________
Fase 8 — Banco Como Fonte da Verdade
Objetivo
Consolidar o banco como centro operacional do sistema.
Dados que devem estar no banco
•	ativos;
•	instrumentos;
•	contratos de opções;
•	cotações de ativos;
•	cotações de opções;
•	snapshots RTD;
•	estruturas;
•	pernas;
•	eventos de posição;
•	encerramentos manuais;
•	parâmetros;
•	snapshots por perna;
•	snapshots por estrutura;
•	execuções de cálculo.
Critério de saída
O sistema consegue consultar dados essenciais sem depender das abas calculadas do Excel.
________________________________________
Fase 9 — Cadastro e Persistência de Estruturas
Objetivo
Corrigir o problema de novas estruturas não entrarem no sistema.
Fluxo desejado
1.	Usuário cadastra estrutura.
2.	Sistema grava estrutura.
3.	Sistema grava pernas.
4.	Sistema vincula pernas aos tickers RTD.
5.	Sistema busca cotações.
6.	Sistema calcula métricas.
7.	UI exibe estrutura ativa.
Pontos críticos
•	criação de estrutura;
•	vínculo de pernas;
•	status da operação;
•	quantidade;
•	preço de execução;
•	vencimento;
•	strike;
•	tipo da opção;
•	compra/venda;
•	ativo objeto.
Critério de saída
Nova estrutura criada no sistema aparece corretamente na UI sem edição manual no Excel.
________________________________________
Fase 10 — Motor de Cálculo Interno
Objetivo
Migrar para o sistema os cálculos que hoje parecem estar presos ao Excel.
Cálculos por perna
•	spread;
•	spread percentual;
•	DTE;
•	preço realista;
•	PL realista;
•	delta exposto;
•	gamma exposto;
•	theta exposto;
•	vega exposto.
Cálculos por estrutura
•	PL realista total;
•	delta líquido;
•	gamma líquido;
•	theta líquido;
•	vega líquido;
•	spread médio;
•	spread percentual médio;
•	DTE mínimo;
•	alertas;
•	risco;
•	gatilho de roll.
Critério de saída
O sistema gera dados equivalentes a ANALISE_ROBO e ANALISE_ROBO_LEGS sem ler essas abas.
________________________________________
Fase 11 — Snapshots e Histórico do Sistema
Objetivo
Substituir o histórico gerado pelo Excel por histórico gerado pelo sistema.
Responsabilidade
O sistema deve registrar snapshots periódicos de:
•	pernas;
•	estruturas;
•	cotações;
•	métricas calculadas;
•	alertas;
•	estado da operação.
Relação com HIST_ROBO
HIST_ROBO passa a ser:
•	legado;
•	fonte de migração histórica;
•	referência de comparação;
•	não fonte viva do sistema.
Critério de saída
Novos registros históricos são gerados pelo sistema sem depender do Excel.
________________________________________
Fase 12 — Encerramentos, Rolls e Eventos Operacionais
Objetivo
Trazer eventos operacionais para dentro do sistema.
Eventos mínimos
•	abertura;
•	ajuste;
•	roll;
•	encerramento parcial;
•	encerramento total;
•	encerramento manual;
•	observação operacional.
Relação com ENCERRAMENTOS_MANUAIS
A aba pode servir como referência temporária, mas o destino final deve ser o sistema.
Critério de saída
Eventos podem ser registrados, persistidos e refletidos nos cálculos da estrutura.
________________________________________
Fase 13 — Refatoração da UI
Objetivo
Fazer a UI consumir somente dados preparados pelo sistema.
A UI deve consumir
•	repositories;
•	services;
•	models;
•	snapshots calculados;
•	estruturas persistidas;
•	dados derivados do banco.
A UI não deve consumir
•	Excel diretamente;
•	CSV derivado antigo;
•	ANALISE_ROBO;
•	ANALISE_ROBO_LEGS;
•	HIST_ROBO;
•	arquivos temporários como fonte principal.
Critério de saída
A UI exibe dados atuais mesmo que as abas antigas estejam vazias ou desatualizadas.
________________________________________
Fase 14 — Migração de Dados Legados
Objetivo
Aproveitar dados históricos sem manter dependência do Excel.
Fontes de migração
•	HIST_ROBO;
•	ANALISE_ROBO;
•	ANALISE_ROBO_LEGS;
•	CONFIGURACOES;
•	ENCERRAMENTOS_MANUAIS;
•	CSVs antigos da bridge.
Regra
Migração é processo pontual, não fluxo permanente.
Critério de saída
Dados úteis preservados no banco e abas antigas desativadas como fonte viva.
________________________________________
Fase 15 — Validação Integrada
Objetivo
Testar o fluxo completo.
Validações mínimas
1.	RTD atualiza.
2.	Bridge recebe dados brutos.
3.	Ingestão grava no banco.
4.	Estrutura nova é criada.
5.	Pernas são vinculadas.
6.	Cotações são associadas às pernas.
7.	Motor calcula métricas.
8.	Snapshots são gerados.
9.	UI exibe dados atuais.
10.	Excel permanece apenas como ponte.
Critério de saída
Fluxo completo funcionando de ponta a ponta.
________________________________________
Fase 16 — Limpeza, Versionamento e Release
Objetivo
Consolidar a entrega com segurança.
Ações
•	revisar arquivos alterados;
•	separar código de dados operacionais;
•	não commitar CSV volátil sem intenção;
•	não commitar Excel sem intenção;
•	fazer commits pequenos;
•	atualizar documentação;
•	registrar pendências;
•	preparar próximo ciclo.
Critério de saída
Patch validado, commitado e pronto para continuidade.
________________________________________
Sequência Recomendada para Agora
A ordem prática que eu recomendo é esta:
Primeiro bloco: travar direção
1.	Refatorar ROTA_MESTRE_1
2.	Remover a ideia de “Fase 11” como início
3.	Reorganizar fases conforme acima
4.	Commitar documento norteador
Segundo bloco: diagnosticar
5.	Higiene do repositório
6.	Diagnóstico do fluxo atual
7.	Classificação das fontes
8.	Auditoria de dependência do Excel
Terceiro bloco: corrigir alimentação
9.	Contrato RTD
10.	Bridge RTD
11.	Ingestão bruta RTD
12.	Banco como fonte da verdade
Quarto bloco: recuperar operação
13.	Cadastro de estruturas
14.	Motor de cálculo
15.	Snapshots
16.	Eventos operacionais
Quinto bloco: exibição e fechamento
17.	UI consumindo banco
18.	Migração de legado
19.	Validação integrada
20.	Commit e release



Estado geral após limpeza:

Tamanho total local: 40MTotal de arquivos: 434Total de pastas: 37Branch: limpeza-inicial-repositorioStatus Git: limpoBranch em relação à main: 0 atrás / 5 à frente
Foram confirmados como ignorados pelo Git:
text
_cleanup_reports/_repo_audit/candidatos_limpeza_cache.txtreports/scripts/.smoke_context.json
Não foram encontrados novos arquivos óbvios de cache, build, temporários ou lixo na auditoria:
text
Possíveis arquivos/pastas de cache, build, temporários ou lixo: vazio
________________________________________
Estrutura principal do projeto
Raiz do projeto
Arquivos e scripts principais na raiz:
text
main.py
run_ui.py
validate_db.py
bridge_ingest_csv.py
cleanup_fase_b.py
create_payoff_summary_table.py
limpar_repositorio_seguro.sh
mapear_repositorio.sh
PATCHES.md
.gitignore

Diretórios principais
ATT/
Área de apoio técnico, patches, auditorias e testes.
Estrutura:
text
ATT/├── checks/├── patches/├── reports/└── tests/
Principais usos:
•	Guarda scripts de patches aplicados ao longo da evolução do sistema.
•	Contém testes automatizados.
•	Contém checks e smokes de validação.
•	Mantém histórico técnico auxiliar, como PATCHES.md e relatórios específicos.
Exemplos relevantes:
text
ATT/checks/run_all_checks.py
ATT/checks/run_real_smokes.py
ATT/patches/patch_66_import_legacy_structures.py
ATT/patches/patch_70_mainwindow_dialog_wiring.py
ATT/patches/patch_71_structures_list_archive.py
ATT/patches/patch_72_structure_audit_log.py
ATT/tests/test_structures_repository.py
ATT/tests/test_pricing_execution_controller.py
ATT/tests/test_structure_analysis_service.py
________________________________________
UI/
Camada de interface do sistema.
Estrutura:
text
UI/├── components/└── models/
Arquivos principais:
text
UI/main_window.py
UI/debug_utils.py
UI/models/ui_data.py
UI/components/details_panel.py
UI/components/payoff_chart.py
UI/components/structure_editor_dialog.py
UI/components/structures_list_panel.py
UI/components/decisions_grid.py
UI/components/filters_panel.py
Responsabilidade provável:
•	Janela principal da aplicação.
•	Painéis de detalhes.
•	Lista e edição de estruturas.
•	Gráficos de payoff.
•	Modelos de dados usados pela interface.
________________________________________
api/
Camada de entrada/controladores.
Arquivos:
text
api/pricing_execution_controller.pyapi/structures_controller.py
Responsabilidade:
•	Expor/controlar operações relacionadas a estruturas.
•	Controlar execuções de pricing.
________________________________________
bridge/
Área de integração com arquivos CSV externos/legados.
Arquivos encontrados:
text
bridge/analise_raiox.csv
bridge/analise_robo.csv
bridge/analise_robo_legs.csv
bridge/configuracoes.csv
bridge/consolidacoes.csv
bridge/encerramentos_manuais.csv
bridge/hist_robo.csv
bridge/last_export.txt
bridge/rolls_detectados.csv
Destaque de tamanho:
text
212K bridge/hist_robo.csv
Responsabilidade:
•	Armazenar/exportar dados intermediários de integração.
•	Servir como ponte entre rotinas legadas, planilhas ou processos externos.
________________________________________
dados/
Área local de dados e bancos SQLite.
Estrutura:
text
dados/├── backups/└── migrations/
Arquivos encontrados:
text
dados/app.db
dados/derived.db
dados/pricing_executions.json
dados/RTD_LINKS.csv
dados/audit_domain_coupling_patch24.json
dados/backups/app_20260529_111415.db
dados/migrations/004_pricing_executions_new_columns.sql
Observação importante:
text
dados/
não está versionado pelo Git conforme conferência com git ls-files. É tratado como área local de dados.
________________________________________
db/
Camada de banco de dados e infraestrutura SQLite.
Estrutura:
text
db/└── migrations/
Arquivos principais:
text
db/config.py
db/derived_repo.py
db/import_excel.py
db/init_db.py
db/init_excel_schema.py
db/reader.pydb/schema.py
db/schema_excel.py
db/sqlite.pydb/writer.py
db/migrations/run_patch_33.py
Responsabilidade:
•	Configuração de banco.
•	Inicialização de schema.
•	Leitura e escrita.
•	Repositório de dados derivados.
•	Importação de Excel.
•	Migrações auxiliares.
________________________________________
docs/
Documentação técnica do projeto.
Estrutura:
text
docs/└── decisions/
Arquivos relevantes:
text
docs/MAPA_MODULOS_FUNCOES.md
docs/DATABASE_LOCATOR.md
docs/DB_PATHS.md
docs/PREFLIGHT_CHECK.md
docs/SQL_SURFACE_MAP_v2.md
docs/baseline_v1.md
docs/baseline_v2.md
docs/changelog.md
docs/roteiro_v2.md
docs/executed_v1.md
docs/executed_v2.md
Responsabilidade:
•	Roteiros.
•	Baselines.
•	Mapeamento técnico.
•	Histórico de decisões.
•	Documentação de banco e SQL.
•	Relatórios de fechamento técnico.
________________________________________
domain/
Camada de domínio.
Arquivos:
text
domain/calculation_request.py
domain/canonical_validators.py
domain/contracts.pydomain/decision.py
domain/market_snapshot.pydomain/payoff.py
domain/payoff_features.py
domain/structure_metrics.py
Responsabilidade:
•	Entidades e objetos de domínio.
•	Validações canônicas.
•	Contratos.
•	Métricas de estruturas.
•	Payoff.
•	Snapshot de mercado.
•	Requisições de cálculo.
________________________________________
dto/
Objetos de transferência de dados.
Arquivos:
text
dto/robo_leg_dto.py
dto/robo_legs_status_dto.py
Responsabilidade:
•	Definir formatos de transporte para dados de pernas do robô e status.
________________________________________
infra/
Infraestrutura técnica.
Arquivos:
text
infra/bootstrap_structures_schema.py
infra/sqlite_conn.py
Responsabilidade:
•	Bootstrap de schema.
•	Conexão SQLite.
________________________________________
repositories/
Camada de acesso a dados.
Arquivos:
text
repositories/market_snapshot_repository.py
repositories/pricing_executions_repository.py
repositories/robo_legs_repository.py
repositories/robo_legs_status_repository.py
repositories/rtd_option_quotes_repository.py
repositories/structures_repository.py
repositories/_aba_resolver_mixin.py
Responsabilidade:
•	Persistência e consulta de estruturas.
•	Execuções de pricing.
•	Pernas do robô.
•	Status de pernas.
•	Cotações RTD de opções.
•	Snapshots de mercado.
________________________________________
services/
Camada de serviços de aplicação e orquestração.
Arquivos principais:
text
services/calculation_orchestrator.py
services/canonical_input_service.py
services/canonical_pricing_facade.py
services/derived_payoff_persistence.py
services/derived_service.py
services/legacy_robo_legs_fallback.py
services/market_snapshot_provider.py
services/market_snapshot_selector.py
services/payoff_persistence_port.py
services/pricing_engine_stub.py
services/pricing_execution_app_service.py
services/pricing_execution_orchestration_service.py
services/pricing_execution_persistence_service.py
services/pricing_execution_query_service.py
services/pricing_execution_service.py
services/pricing_input_service.py
services/pricing_payload_adapter.py
services/robo_leg_mapper.py
services/robo_legs_service.py
services/robo_legs_status_service.py
services/structure_analysis_service.py
services/structure_input_mapper.py
services/structure_market_input_assembler.py
Responsabilidade:
•	Orquestração de cálculo.
•	Montagem de input canônico.
•	Execução de pricing.
•	Persistência e consulta de execuções.
•	Integração com snapshots de mercado.
•	Serviços de estruturas.
•	Conversão/mapeamento de pernas do robô.
•	Fallback legado.
________________________________________
scripts/
Coleção de scripts operacionais, auditorias, smokes, migrações e validações.
Quantidade relevante:
text
scripts/ contém grande volume de scripts de smoke, auditoria e manutenção.
Exemplos:
text
scripts/run_smoke_quick.py
scripts/run_smoke_full.py
scripts/run_derived_pipeline.py
scripts/mapear_rtd_opcoes.py
scripts/git_mapear_fluxo_rtd.py
scripts/preflight_check_v2.py
scripts/db_locator.py
scripts/db_path_doctor.py
scripts/validate_derived_db.py
scripts/import_rtd_links_csv.py
scripts/patch_73_rtd_option_quotes.py
Observação pós-limpeza:
text
scripts/.smoke_context.json
foi removido do Git e passou a ser ignorado, pois representa contexto local de smoke tests.
________________________________________
src/
Estrutura complementar de código.
Arquivos encontrados:
text
src/domain/refs/structure_ref.py
Responsabilidade provável:
•	Referências de domínio relacionadas a estruturas.
________________________________________
utils/
Utilitários compartilhados.
Arquivo:
text
utils/leg_normalizers.py
Responsabilidade:
•	Normalização de pernas/operações.
________________________________________
validators/
Validações auxiliares.
Arquivos:
text
validators/leg_validator.py
validators/timestamp_validator.py
validators/validators__init__.py
Responsabilidade:
•	Validação de pernas.
•	Validação de timestamps.
________________________________________
reports/
Relatórios gerados por scripts de mapeamento.
Arquivos locais encontrados:
text
reports/mapeamento_rtd_opcoes.jsonreports/mapeamento_rtd_opcoes.mdreports/git_mapeamento_fluxo_rtd.jsonreports/git_mapeamento_fluxo_rtd.md
Observação pós-limpeza:
text
reports/
foi confirmado como ignorado pelo Git, pois os relatórios podem ser regenerados quando necessário.
________________________________________
_repo_audit/ e _cleanup_reports/
Pastas locais de auditoria e limpeza.
Confirmadas como ignoradas pelo Git:
text
_repo_audit/_cleanup_reports/
Responsabilidade:
•	Guardar saídas locais de auditoria.
•	Guardar relatórios locais de limpeza.
•	Não fazem parte do código versionado.


ENCERRADO AQUI AS FASES ANTERIORES (1-17)
_____________________________________________________________________________________

INICIO ROTA_MESTRE_2

Regras de segurança do ciclo

Durante esta rota, é proibido:
•	reabrir fases da ROTA_MESTRE_1 sem justificativa e consulta ao Git
•	alterar UI antes de fechar o contrato RTD
•	criar tabela nova antes de auditar rtd_option_quotes_repository.py
•	usar arquivos bridge legados como nova fonte de verdade sem decisão documentada
•	acoplar UI diretamente ao Excel
•	fazer alterações pontuais sem mapa de impacto

Ao encerrar cada fase, devem ser executados:

• testes específicos da fase atual
• testes de regressão das fases já encerradas da ROTA_MESTRE_2
• testes mínimos de não regressão da ROTA_MESTRE_1 quando houver impacto
• comando executado
• resultado
• data/hora
• commit

Antes de qualquer alteração funcional, deve existir mapa de impacto contendo:

• arquivos que serão alterados
• arquivos apenas auditados
• risco esperado
• testes que validarão a mudança
• plano de reversão

Nova Divisão de Fases da ROTA_MESTRE_2

Fase 0 — Marco de Controle e Congelamento da Rota
Objetivo
Travar a nova estratégia antes de continuar o desenvolvimento.
Escopo
Consolidar a ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md como documento norteador atualizado.
Decisões fixadas
•	Excel é apenas ponte RTD.
•	Banco de dados é a fonte da verdade.
•	UI não deve depender de CSVs derivados antigos.
•	Abas calculadas do Excel são legado.
•	Cálculos devem migrar para o sistema.
•	Novas estruturas devem nascer no sistema, não na planilha.
Entregável
Nova ROTA_MESTRE_2 refatorada e commitada.
Critério de saída
Documento revisado, aceito e versionado.

Obrigatório para esta etapa

Gerar auditoria em testes com reflexo em docs/AUDITORIA_ROTA_MESTRE_2.md atualizando a cada evolução mantendo a base concreta de desenvolvimento assim como:
• fase
• objetivo
• arquivos auditados
• comandos executados
• testes executados
• resultado
• pendências
• decisão tomada
• commit relacionado


Observação:
-Alguns scripts citados na documentação histórica da ROTA_MESTRE_1 podem não existir mais no estado atual do repositório. Para a ROTA_MESTRE_2, prevalece o mapeamento atual e, em caso de dúvida, o histórico deve ser conferido no Git.

- O arquivo dados/RTD_LINKS.csv é tratado como dado local operacional. O contrato versionado deve ser documentado em docs/, e não depender do versionamento direto do CSV real.
 
- RTD_LINKS.csv deve ser auditado inicialmente como catálogo/contrato de conexão RTD, não como fonte definitiva de snapshots de mercado, até que seu schema real confirme essa função.

Fase 1 — Mapeamento amplo de RTD, Excel, Bridge, Serviços e UI
Status inicial: iniciado.
Base:
•	mapeamento_automacao_opcoes_rtd.md
•	mapeamento_automacao_opcoes_rtd.json
Objetivo:
•	identificar todos os arquivos que mencionam RTD, Excel, bridge, opções, persistência, serviços e UI
•	classificar papéis prováveis
•	separar candidatos fortes de ruído
Entregáveis:
•	relatório Markdown
•	relatório JSON
•	lista priorizada de arquivos
Critério de aceite:
•	mapeamento executado sem alterar UI, banco, cálculo ou ingestão
________________________________________
Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv

Esta fase deve produzir somente diagnóstico, relatório e decisão. Não deve alterar schema, UI, cálculo, repositórios ou fluxo de ingestão.

Objetivo:
•	descobrir o contrato real do CSV
•	identificar colunas existentes
•	encoding do arquivo
•	separador usado
•	cabeçalhos reais
•	quantidade de linhas úteis
•	linhas vazias
•	duplicidade de tickers
•	presença de fórmulas RTD
•	presença de campos de mercado
•	presença de campos de identificação da opção
•	campos ausentes em relação ao contrato esperado
•	inferir campos de opção
•	validar presença de links ou fórmulas RTD
•	confirmar se o arquivo pode ser fonte fixa inicial
Entregáveis:
•	script de auditoria
•	relatório do contrato RTD
•	classificação do CSV como:
•	suficiente
•	insuficiente
•	ambíguo
Critério de aceite:
•	saber exatamente quais campos existem no RTD_LINKS.csv
•	saber quais campos faltam
•	nenhuma alteração funcional no Sistema

________________________________________
Fase 3 — Auditoria da persistência de cotações
Objetivo:
•	confirmar se rtd_option_quotes existe no banco
• identificar em qual banco a tabela reside: dados/app.db, dados/derived.db ou outro
• listar schema real via sqlite_master/PRAGMA
• confirmar se testes devem usar banco temporário
•	auditar repositories/rtd_option_quotes_repository.py
•	identificar métodos de insert/upsert/select
•	confirmar se há reuso possível
Entregáveis:
•	mapa de tabela/colunas
•	mapa de métodos do repositório
•	decisão: reutilizar, adaptar ou criar migração
Critério de aceite:
•	decisão documentada antes de qualquer alteração de schema
________________________________________
Fase 4 — Auditoria do fluxo de snapshot de mercado
Objetivo:
•	entender como market_snapshot_provider.py
•	market_snapshot_selector.py
•	market_snapshot_repository.py
•	structure_market_input_assembler.py
•	canonical_input_service.py
participam da montagem dos dados de mercado.
Entregáveis:
•	mapa do fluxo atual
•	pontos de entrada possíveis para cotações RTD
•	riscos de acoplamento
Critério de aceite:
•	identificar ponto de integração sem alterar cálculo
________________________________________
Fase 5 — Definição do contrato canônico de cotação de opção
Objetivo:
Definir estrutura mínima canônica para uma cotação de opção.
Campos mínimos propostos:
•	ticker
•	ativo objeto
•	tipo da opção
•	strike
•	vencimento
•	bid
•	ask
•	último
•	timestamp
•	origem
Campos opcionais:
•	delta
•	gamma
•	theta
•	vega
•	volatilidade implícita
Entregáveis:
•	documento de contrato
•	regras de normalização
•	regras para valores ausentes
Critério de aceite:
•	contrato aprovado antes do importador
________________________________________
Fase 6 — Importador somente-leitura do RTD_LINKS
Objetivo:
Criar importador inicial que leia dados/RTD_LINKS.csv, normalize campos e valide dados, sem ainda alterar UI ou cálculo.
Entregáveis:
•	script de importação
•	modo dry-run
•	relatório de linhas válidas/inválidas
Critério de aceite:
•	importador executa sem efeitos destrutivos
•	falhas são reportadas
•	nenhuma alteração visual no sistema
________________________________________
Fase 7 — Persistência controlada das cotações
Objetivo:
Persistir cotações normalizadas no repositório/tabela adequada.
Entregáveis:
•	integração com repositório existente ou migração mínima
•	testes de insert/upsert/select
•	relatório de auditoria
Critério de aceite:
•	dados persistidos podem ser consultados por ticker
•	histórico/último snapshot definidos claramente
________________________________________
Fase 8 — Integração com snapshot/serviços
Objetivo:
Fazer os serviços internos consumirem cotações persistidas, não diretamente Excel.
Entregáveis:
•	adaptação no provider/selector apropriado
•	testes unitários
•	teste de montagem do input de mercado
Critério de aceite:
•	estrutura consegue resolver dados de mercado por ticker/opção
•	sem dependência direta da UI com Excel
________________________________________
Fase 9 — Integração controlada com cálculo
Objetivo:
Permitir que cálculo use dados RTD persistidos como fonte de mercado.
Entregáveis:
•	teste de cálculo usando snapshot RTD
•	fallback documentado para dados ausentes
•	validação contra estrutura exemplo
Critério de aceite:
•	cálculo permanece estável
•	dados ausentes não quebram fluxo
________________________________________
Fase 10 — Exposição na UI
Objetivo:
Exibir dados básicos automatizados na UI somente após fonte, persistência e serviços estarem estabilizados.
Entregáveis:
•	ajuste mínimo em tela
•	indicadores de preço, bid, ask e timestamp
•	testes de UI existentes preservados
Critério de aceite:
•	UI consome serviço/camada canônica
•	UI não lê Excel diretamente
________________________________________
Fase 11 — Testes integrados
Objetivo:
Validar fluxo completo:
text
RTD_LINKS.csv→ importação→ persistência→ snapshot→ cálculo→ UI
Entregáveis:
•	teste integrado
•	relatório de validação
•	lista de riscos remanescentes
Critério de aceite:
•	fluxo executado em ambiente local
•	sem regressão nas fases da ROTA_MESTRE_1
________________________________________
Fase 12 — Fechamento do ciclo
Objetivo:
Encerrar oficialmente a ROTA_MESTRE_2.
Entregáveis:
•	relatório final
•	changelog
•	validação de testes
•	PR ou merge controlado
Critério de aceite:
•	todos os testes passam
•	documentação atualizada
•	sem fases pendentes abertas



