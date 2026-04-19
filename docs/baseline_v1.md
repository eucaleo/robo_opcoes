1 - Colunas das abas que possuem os ativos e estruturas a serem calculados.
ATIVO
C/V
QUANT
VALOR_EXECUTADO
TOTAL_MERCADO
LUCRO_/_PREJUIZO
VALOR_INVESTIDO
CALL_/_PUT
SPOT
STRIKE
VENCIMENTO
DTE
ULTIMA_QUANTIDADE_NEGOCIADA
TOTAL_NEGOCIADO
TOTAL_EXECUTADO
ULTIMO_PRECO_MERCADO
BID
ASK
IV
DELTA
GAMMA
THETA
VEGA
MONEYNESS
2 - ABA Analise RAIOX

ABA
TIMESTAMP
ANALISE_RAIOX

3 - ABA Rolls detectados

	DATA
	ABA
	EVENTO
	CODIGO ROLADO
	QUANTIDADE
	PREÇO SAIDA
	CODIGO ENTRADA
	PREÇO ENTRADA
	PL REAL
	PL ESTIMADO
	DIF %
	OBS:



4 - ABA consolidações
	TIMESTAMP
	ABA
	PERNAS ABERTA
	TOTAL EXECUTADO ABERTO
TOTAL ATUAL ABERTO
	GANHO ATUAL ABERTO
	PL REALIZADO
	PL TOTAL
	OBS

5 - ABA hist._robo
	TIMSTAMP
	ABA
	ATIVO
	C/V
	QUANT
	VALOR EXECUTADO
	BID
	ASK
	DELTA
	THETA
VEGA
PL REALISTA


6 - ABA encerramentos manuais
	DATA
	ABA
	CODIGO
	TIPO
	QTD
	PRECO REAL
	MOTIVO
	OBSERVAÇÃO

7 - ABA analise robô
	ABA
	SPOT
	NUM_PERNAS
	DTE_MIN
	PL_REALISTA_TOTAL
	DELTA_LIQ
	GAMMA_LIQ
	THETA_LIQ
	VEGA_LIG
	SPREAD_MEDIO
	SPREAD_PCT_MEDIO
	ALERTAS_V2
8 - ABA robô_legs
	TIMESTAMP
	ABA
	ATIVO
	C/V
	CALL_/_PUT
	QUANT
	VALOR_EXECUTADO
	BID
	ASK
APREAD
	SPREAD_PCT
	IV
	DELTA
	GAMMA
	THETA
	VEGA
	STRIKE
	VENCIMENTO
	DTE
	PL_REALISTA

Mapa da solução (resumo do raciocínio + módulos e responsabilidades)
Objetivo
Transformar o Excel (com RTD) em fonte de dados, e o SQLite em sistema de verdade (histórico + consultas).
O app (Tkinter) só consulta o SQLite e exibe/gera alertas.
________________________________________
Arquitetura em camadas
1) DataSource (Excel/RTD)
Responsável por conectar no Excel via COM, identificar abas de ativos automaticamente, ler a tabela (header linha 1, dados linha 2, até 10 linhas), normalizar valores e produzir um “snapshot”.
Módulo: datasource/rtd_excel_bridge.py
Principais funções/classes:
•	ExcelRTDSnapshotter
•	__enter__() / __exit__()
Abre/fecha Excel invisível e o workbook.
•	calculate(full: bool=False)
Força recálculo (ajuda RTD atualizar).
•	read_table(sheet_name, required_columns, header_row=1, start_row=2, max_rows=10)
Lê linhas da aba; para quando ATIVO ficar vazio; devolve {ts, sheet, missing_columns, rows}.
•	normalize_cell(value)
Converte erro/vazio→None, número→float, texto→str, data→string ISO.
Módulo (detecção): datasource/sheet_discovery.py (ou dentro do bridge)
Funções:
•	sheet_headers(ws, header_row=1, scan_cols=80)
Lê cabeçalhos da linha 1.
•	is_assets_sheet(ws)
Decide se a aba é “de ativo” conferindo presença de colunas-chave (ex.: ATIVO, C/V, QUANT, etc.).
•	discover_assets_sheets(wb)
Percorre worksheets, ignora abas “sistema” conhecidas e valida pelo cabeçalho → retorna lista de abas de ativos.
________________________________________
2) Persistência (SQLite)
Responsável por criar schema, inserir snapshots e permitir consultas eficientes.
Módulo: db/schema.py
Função/constante:
•	SCHEMA_SQL
Script SQL com:
•	legs_snapshot (tabela base por perna/linha)
•	índices por (aba, ts) etc.
•	pragmas (WAL) para leitura/escrita concorrente.
Módulo: db/repo.py
Funções:
•	init_db(db_path)
Cria tabelas/índices se não existirem.
•	insert_legs_snapshot(db_path, ts, aba, rows)
Insere todas as linhas (pernas) de uma aba naquele timestamp.
•	(futuro) get_latest_snapshot(db_path, aba) / list_abas(db_path)
Para o Tkinter consumir.
•	(futuro) insert_analysis_*, insert_rolls_*, etc.
Para tabelas derivadas.
Tabela base definida:
•	legs_snapshot: 1 linha = 1 perna da estrutura no instante ts.
________________________________________
3) Serviço de atualização (Scheduler / Ciclo)
Responsável por rodar a coleta periodicamente:
1.	abrir Excel (ou manter aberto)
2.	recalcular
3.	descobrir abas de ativos
4.	ler até 10 linhas por aba
5.	salvar no SQLite
6.	dormir até próximo ciclo
Módulo: services/update_cycle.py
Funções:
•	run_once(xlsx_path, db_path, max_rows=10)
Executa um ciclo completo (descobre abas + coleta + grava).
•	run_loop(xlsx_path, db_path, interval_s=300)
Loop infinito chamando run_once.
•	(futuro, recomendado) run_loop_with_watchdog(...)
Se Excel travar/RTD falhar, reinicia a instância COM e segue.
Configuração do ciclo:
•	MVP: intervalo fixo (ex.: 300s)
•	Evolução: ler TimeFrame Snapshot (min) da aba CONFIGURACOES.
________________________________________
4) Cálculos / Regras de negócio (derivações)
Responsável por gerar:
•	ANALISE_ROBO (agregados por ABA)
•	ANALISE_ROBO_LEGS (cálculos por perna, PL realista, spreads etc.)
•	ANALISE_RAIOX (texto consolidado)
•	ROLLS_DETECTADOS (eventos de roll)
•	CONSOLIDACOES
Módulo: domain/calcs.py (planejado)
Funções (exemplos):
•	compute_robo_legs(snapshot_rows, slippage, ...) -> rows_com_PL
•	aggregate_analise_robo(rows_com_PL) -> resumo_por_aba
•	detect_rolls(prev_snapshot, curr_snapshot, regras_config) -> eventos_roll
•	build_raiox_text(resumo, top_delta, top_pl, ...) -> str
Observação importante:
Essas tabelas são derivadas. No novo desenho, elas podem ser:
•	gravadas no SQLite (recomendado)
•	e opcionalmente “exportadas” para o Excel se você quiser manter compatibilidade visual.
________________________________________
5) UI (Tkinter)
Responsável por consultar o SQLite e exibir:
•	último snapshot por aba
•	consolidações
•	alertas (Delta alto, Vega alto, spread, etc.)
•	histórico
Módulo: ui/app.py (planejado)
Componentes:
•	tela por ABA (estrutura atual + legs)
•	painel de alertas
•	histórico (chart simples ou tabela)
________________________________________
Fluxo ponta-a-ponta (o “pipeline”)
1.	services/update_cycle.run_loop()
2.	abre Excel → datasource/ExcelRTDSnapshotter
3.	discover_assets_sheets() identifica abas de ativos automaticamente
4.	read_table() lê até 10 linhas por aba
5.	db/repo.insert_legs_snapshot() grava no SQLite
6.	(fase 2) domain/calcs gera derivadas → grava em tabelas analíticas
7.	Tkinter lê do SQLite (nunca do Excel) e exibe
________________________________________
“Contrato” (assunções que fixamos)
•	Header sempre na linha 1; dados a partir da linha 2
•	Cada aba de ativo tem 1 estrutura; no máximo 10 linhas
•	Colunas padronizadas: nomes compostos com _, sem acento/caractere especial
•	Abas de ativos serão detectadas automaticamente por presença do cabeçalho esperado
________________________________________
Próximo passo após este mapa
Quando você aprovar esse desenho, eu gero:
1.	um projeto mínimo com esses módulos (bridge + discovery + repo + loop)
2.	com intervalo fixo (ex.: 300s) e logs
3.	e depois evoluímos para ler o timeframe de CONFIGURACOES e adicionar watchdog/reconexão.

PROGRAMAS (BIBLIOTECA PYTHON)

Aqui estão os programas (bibliotecas Python) que você deve instalar para esse projeto, com a função de cada um:
________________________________________
Principais bibliotecas
Biblioteca	Para quê serve?	Como instalar
pywin32	Conexão com o Excel via COM (Windows only)	pip install pywin32
sqlite3	Banco de dados SQLite embutido	Já vem do Python (nativo)
tkinter	Interface gráfica (UI simples, painel de controle)	Já vem do Python (nativo)
pandas (opcional)	Manipulação de dados tabulares (não essencial até agora, mas útil se quiser análises mais avançadas ou salvar CSV)	pip install pandas
colorama (opcional)	Deixar prints no terminal coloridos/fáceis de ler	pip install colorama
pytest (opcional)	Testes automatizados	pip install pytest
________________________________________
Comando do setup básico
Crie um ambiente (recomendado, mas opcional), depois instale:
shell
pip install pywin32# e, se quiser futuramente, pandas e colorama:pip install pandas colorama
Nota:
•	sqlite3 e tkinter já vêm com o Python do Windows, normalmente não precisa instalar.
•	Esse sistema roda em Windows, porque depende do Excel/COM (não funciona em Linux).
________________________________________
Checklist de instalação
1.	Python instalado:
•	Recomendado: Python 3.10 ou 3.11 (64 bits)
2.	Excel instalado:
•	Microsoft Office Excel 2016, 2019, ou 365 (não funciona com LibreOffice)
3.	pywin32 instalado:
•	pip install pywin32
4.	(opcional para ideias futuras) pandas, colorama
________________________________________
Teste rápido do pywin32
Após instalar, confirme que está ok rodando no terminal Python:
python
import win32com.clientexcel = win32com.client.Dispatch("Excel.Application")print(excel.Version)excel.Quit()
Se mostrar a versão do seu Excel sem erro: está tudo certo!
________________________________________
Se quiser atualizar tudo junto, pode usar:
shell
pip install pywin32 pandas colorama pytest
Mas para o MVP, só pywin32 é obrigatório.

0) Definições (glossário e premissas fixas)
0.1 Estrutura
•	1 ABA = 1 estrutura (conjunto de pernas).
•	Cada estrutura tem até 10 pernas (linhas).
0.2 Sinais e unidades
•	C/V: C = Compra (long), V = Venda (short).
•	QUANT: quantidade positiva (o sinal vem do C/V).
•	Opções são calculadas unitárias (sem multiplicador/lote).
“Lotes” servem apenas para compra/operacional; no cálculo de P&L da opção, tudo é unitário.
0.3 Prêmio de entrada e consistência
•	VALOR_EXECUTADO = prêmio de entrada (preço médio unitário) da perna.
•	TOTAL_EXECUTADO e VALOR_EXECUTADO são consistentes (informação confirmada).
0.4 Curva de ganho (escopo)
•	“Curva de ganho” = payoff no vencimento PLvenc(ST)PLvenc(ST).
•	Não é mark-to-market por tempo/IV (por enquanto).
________________________________________
1) Colunas (abas / tabelas lógicas) — confirmadas
1.1 Abas de ativos (pernas / snapshot)
(igual ao atual; já em snake_case no SQLite)
Campos relevantes para payoff/decisão:
•	ativo
•	c_v
•	quant
•	valor_executado
•	lucro_prejuizo
•	call_put
•	spot
•	strike
•	vencimento
•	dte
•	bid
•	ask
•	spread / spread_pct (em robo_legs)
•	Greeks / IV (existentes; não essenciais para payoff no vencimento)
1.2 Analíticas existentes
•	analise_raiox
•	rolls_detectados
•	consolidacoes
•	hist_robo
•	encerramentos_manuais
•	analise_robo
•	robo_legs
________________________________________
2) Novas capacidades adicionadas (a partir daqui)
2.1 Curva de ganho (payoff no vencimento)
Entrada
Lista de pernas (rows) de uma aba em um timestamp, com:
•	c_v, quant, valor_executado, call_put, strike
•	spot como referência de malha de preços STST
Saída
•	Lista de pontos: [(s_t, pl_venc), ...]
•	Métricas:
•	pl_max
•	pl_min
•	spot_ref (spot usado para construir a malha)
Fórmulas (unitárias)
Para cada perna com preço no vencimento STST:
•	Intrínseco:
•	Call: max⁡(ST−K,0)max(ST−K,0)
•	Put: max⁡(K−ST,0)max(K−ST,0)
•	P&L unitário:
•	Long: intrinsic−premiumintrinsic−premium
•	Short: premium−intrinsicpremium−intrinsic
•	P&L por perna:
PLperna(ST)=QUANT⋅PLunit(ST)PLperna(ST)=QUANT⋅PLunit(ST)
•	P&L da estrutura:
PLestrutura(ST)=∑PLperna(ST)PLestrutura(ST)=∑PLperna(ST)
Malha de preços (grid padrão)
•	Smin=0.5⋅SPOTSmin=0.5⋅SPOT
•	Smax=1.5⋅SPOTSmax=1.5⋅SPOT
•	step:
•	step=max⁡(0.01⋅SPOT,0.01)step=max(0.01⋅SPOT,0.01)
Observação: grid é suficiente para MVP. Melhorias futuras: grid adaptativo, segmentação linear, extrapolação, etc.
________________________________________
2.2 Encerramento / Decisão (múltiplos thresholds)
Métrica base
•	ratio=PLatualPLmaxratio=PLmaxPLatual, somente se PLmax>0PLmax>0.
Fonte de PLatualPLatual
•	PLatualPLatual = soma de lucro_prejuizo de todas as pernas da aba no snapshot.
Thresholds (default fixo)
•	Watch: ratio ≥ 0.30 → decisão principal ainda HOLD (mas com alerta)
•	Prepare: ratio ≥ 0.60 → PREPARE_ROLL
•	Close: ratio ≥ 0.80 → CLOSE_REOPEN
Gate de DTE (fixo)
•	Se dte_min ≤ 7 e ratio ≥ 0.60 → promover para CLOSE_REOPEN
Gate de spread (placeholder; pode ser ligado depois)
•	Se existir spread_pct_medio e estiver acima de um cap → evitar execução imediata (rebaixar para PREPARE_ROLL)
•	(Default pro cap, se usado): 1.50 (150%)
Saída (decisão)
Para cada aba/timestamp:
•	decision: HOLD | PREPARE_ROLL | CLOSE_REOPEN
•	level: 0-3
•	pl_atual, pl_max, pl_pct_of_max, dte_min
•	why_json: JSON com:
•	reasons (motivos numéricos e regras aplicadas)
•	alternatives (sugestões: “esperar close”, “fechar por DTE”, “aguardar spread”)
________________________________________
3) Onde isso entra na arquitetura (camada e pipeline)
3.1 Camada
•	Implementação em domain/:
•	domain/payoff.py (curva e métricas)
•	domain/decision.py (regras/decisão)
3.2 Pipeline ponta-a-ponta (atualizado)
1.	services/update_cycle.run_loop() / run_once()
2.	Excel RTD → snapshot por aba
3.	Descoberta de abas de ativos
4.	Leitura até 10 linhas por aba
5.	Persistência: db/repo.insert_legs_snapshot()
6.	Derivações:
•	domain/calcs (já existente/planejado): robo_legs, analise_robo, etc.
•	NOVO: domain/payoff gera curva
•	NOVO: domain/decision gera decisão
7.	Persistir derivadas no SQLite:
•	payoff_curve_points
•	structure_decisions
•	E inserir linha em consolidacoes quando decision == CLOSE_REOPEN
8.	Tkinter consome somente SQLite
________________________________________
4) Schema SQLite — novas tabelas (derivadas)
4.1 payoff_curve_points
•	Um conjunto de pontos por timestamp + aba.
Campos:
•	timestamp TEXT NOT NULL
•	aba TEXT NOT NULL
•	s_t REAL NOT NULL
•	pl_venc REAL NOT NULL
•	spot_ref REAL NULL
•	meta_json TEXT NULL
Chave/índices:
•	PK: (timestamp, aba, s_t)
•	Index: (aba, timestamp)
4.2 structure_decisions
•	Uma decisão por timestamp + aba.
Campos:
•	timestamp TEXT NOT NULL
•	aba TEXT NOT NULL
•	decision TEXT NOT NULL
•	level INTEGER NOT NULL
•	pl_atual REAL NULL
•	pl_max REAL NULL
•	pl_pct_of_max REAL NULL
•	dte_min INTEGER NULL
•	why_json TEXT NULL
•	created_at TEXT DEFAULT CURRENT_TIMESTAMP
Chave/índices:
•	PK: (timestamp, aba)
•	Index: (aba, timestamp)
________________________________________
5) Integração com “consolidações” (requisito confirmado)
Quando decision == CLOSE_REOPEN:
•	inserir uma linha em consolidacoes com:
•	timestamp, aba
•	obs = "CLOSE_REOPEN: PL_atual=..., PL_max=..., Ratio=..."
•	Demais campos podem ser NULL se o pipeline ainda não tiver agregado nesse momento.
•	(Melhoria futura) preencher também pl_total, ganho_atual_aberto, etc.
________________________________________
6) Contratos técnicos (para evitar ambiguidades)
•	Os nomes das colunas no SQLite estão em snake_case (confirmado).
•	A curva é calculada em unidades (sem multiplicador).
•	VALOR_EXECUTADO é o premium (preço médio de entrada) por perna.
•	O spot de referência do grid vem de spot da estrutura (aba).
•	PL_atual vem do somatório de lucro_prejuizo no snapshot.
________________________________________
7) Módulos / arquivos (estado do projeto)
Mantém os existentes e adiciona:
•	domain/payoff.py (novo)
•	domain/decision.py (novo)
•	Atualizar:
•	db/schema.py (adicionar tabelas)
•	db/repo.py (insert_* dessas tabelas + inserir linha em consolidações)
•	services/update_cycle.py (chamar payoff/decision após snapshot)
________________________________________
8) Parâmetros default (versão 1)
•	Grid:
•	low/high: 0.5x / 1.5x do spot
•	step: 1% do spot (mín. 0.01)
•	Thresholds:
•	0.30 / 0.60 / 0.80
•	Gate:
•	DTE ≤ 7 promove para close (se ratio ≥ 0.60)

FASES DE PRODUÇÃO

Fase 0 — Congelamento do baseline (1 commit)
0.1 Criar tag/branch de baseline
•	Branch: baseline_v1
•	Salvar este “Documento base atualizado” em docs/baseline_v1.md
Pronto quando:
•	existe o arquivo docs/baseline_v1.md
•	commit feito: chore: baseline v1 (docs)
________________________________________
Fase 1 — Schema SQLite (payoff + decisions) (1 commit)
1.1 Atualizar db/schema.py (SCHEMA_SQL)
•	Adicionar tabelas:
•	payoff_curve_points
•	structure_decisions
•	Garantir índices conforme baseline
1.2 Rodar init/migration simples
•	Executar db/repo.init_db() (ou script de init existente)
Pronto quando:
•	sqlite_master mostra as 2 tabelas novas
•	sem erro ao iniciar o app/coletor
Commit:
•	db: add payoff_curve_points and structure_decisions tables
________________________________________
Fase 2 — Repo (persistência das novas derivadas) (1 commit)
2.1 Atualizar db/repo.py Adicionar funções:
•	insert_payoff_points(conn, ts, aba, points, spot_ref, meta)
•	insert_structure_decision(conn, ts, aba, decision_dict)
•	insert_consolidacao_line_for_close(conn, ts, aba, obs) (inserção mínima)
Pronto quando:
•	você consegue chamar essas funções num script isolado e ver os inserts no SQLite
Teste rápido (script):
•	scripts/test_repo_inserts.py insere 2 pontos fake + 1 decisão fake
Commit:
•	db: repo inserts for payoff curve and decisions
________________________________________
Fase 3 — Domain: Payoff (curva) (1 commit)
3.1 Criar domain/payoff.py
•	compute_payoff_curve(rows, spot, grid_low_pct=0.5, grid_high_pct=1.5, step_pct=0.01)
•	Normalização usando snake_case (já confirmado)
3.2 Testes mínimos (sem pytest se não quiser)
•	scripts/test_payoff_curve.py com 1 call comprada e 1 call vendida (cenários simples)
Pronto quando:
•	curva retorna lista de pontos
•	pl_max e pl_min coerentes em exemplos simples
Commit:
•	domain: payoff curve (expiry) computation
________________________________________
Fase 4 — Domain: Decision (escada 30/60/80 + gate DTE) (1 commit)
4.1 Criar domain/decision.py
•	decide_structure(rows, spot, dte_min, pl_atual, spread_pct_medio=None, thresholds=...)
•	Defaults:
•	thresholds: 0.30/0.60/0.80
•	gate: dte_min <= 7 promove close se ratio >= 0.60
•	Gera why_json com reasons + alternatives
4.2 Testes mínimos
•	scripts/test_decision.py com:
•	caso ratio=0.35 → HOLD nível 1
•	caso ratio=0.65 → PREPARE_ROLL
•	caso ratio=0.85 → CLOSE_REOPEN
•	caso ratio=0.65 e dte_min=5 → CLOSE_REOPEN (gate)
Pronto quando:
•	decisões batem com o esperado
•	why_json sai bem formado
Commit:
•	domain: decision ladder 30/60/80 + DTE gate
________________________________________
Fase 5 — Integração no ciclo (run_once) (2 commits)
5A) Integração “somente grava no SQLite” (1 commit)
5.1 Em services/update_cycle.py (após insert_legs_snapshot)
•	Para cada aba coletada no ciclo:
•	calcular pl_atual = sum(lucro_prejuizo)
•	spot (pegar do snapshot; se tiver divergência, usar o primeiro não-nulo)
•	dte_min (min de dte na aba)
•	chamar decide_structure
•	gravar:
•	payoff_curve_points
•	structure_decisions
Pronto quando:
•	ao rodar 1 ciclo, aparecem registros nas 2 tabelas novas
•	sem travar Excel/COM
Commit:
•	services: compute+persist payoff curve and decisions per aba
5B) Integração com consolidações (linha OBS) (1 commit)
5.2 No mesmo loop:
•	se decisão == CLOSE_REOPEN:
•	inserir linha em consolidacoes com obs padronizado
Pronto quando:
•	consolidacoes recebe linhas quando close ocorrer
•	obs tem texto padrão e números
Commit:
•	services: write CLOSE_REOPEN note into consolidacoes
________________________________________
Fase 6 — Views/consultas para UI (opcional, mas recomendado) (1 commit)
6.1 Criar funções de consulta em db/repo.py
•	get_latest_decision(db_path, aba)
•	get_latest_curve(db_path, aba, max_points=200)
•	list_abas_with_latest_decisions(db_path)
Pronto quando:
•	Tkinter consegue mostrar “última decisão” por aba
Commit:
•	db: read APIs for decisions and payoff curves
________________________________________
Fase 7 — UI (Tkinter) incremental (2–3 commits)
7A) Tela “Decisões por ABA”
•	Lista abas + decisão (HOLD/PREPARE/CLOSE), ratio, dte_min
7B) Detalhe por ABA
•	Mostra reasons/alternatives (parsed do JSON)
7C) Curva simples (opcional)
•	Gráfico pode ser fase 2 (ou export CSV primeiro)
________________________________________
Fase 8 — Robustez (watchdog + tolerância a dados faltantes) (1–2 commits)
•	Se faltar spot, não calcula curva (grava decisão “HOLD / data_missing”)
•	Se pl_max <= 0, ratio=0 e não dispara close
•	Tratamento de None, strings e erros RTD
________________________________________
Ordem de execução recomendada (checklist rápido)
1.	Fase 0 (docs baseline)
2.	Fase 1 (schema)
3.	Fase 2 (repo inserts)
4.	Fase 3 (payoff)
5.	Fase 4 (decision)
6.	Fase 5A (integração grava no SQLite)
7.	Fase 5B (consolidações OBS)
8.	Fase 6 (queries UI) + Fase 7 (Tkinter)
________________________________________
Padrão de retomada (anti-timeout / anti-perda de contexto)
Sempre que você terminar uma fase, me mande:
•	o hash/descrição do último commit
•	e o resultado do teste (ex.: “rodou run_once e gravou 12 abas”)
Aí eu continuo exatamente do próximo passo, sem reinterpretação.
