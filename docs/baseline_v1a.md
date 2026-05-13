Baseline v1a — Atualização com Bridge CSV (19/12/2024)
Evolução do baseline_v1 original para refletir a implementação real usando bridge CSV + Python ingestor
Mudanças principais do baseline_v1 → baseline_v1a
✅ Arquitetura confirmada operacional
•	Excel: permanece como RTD bridge + exportador CSV (não mais COM direto)
•	Python ingestor: bridge_ingest_csv.py como substituto do services/update_cycle.py original
•	SQLite: mantém a estrutura app.db (raw) + derived.db (payoff/decisões)
✅ Pipeline validado (funcionando)
Excel RTD → CSV export → Python ingest → app.db (raw) → derivadores → derived.db
________________________________________
0) Definições (atualizadas para v1a)
0.1 Estrutura (mantido)
•	1 ABA = 1 estrutura (conjunto de pernas)
•	Cada estrutura tem até 10 pernas (linhas)
0.2 Fonte de dados (atualizado)
•	Excel/RTD: ativo, mas apenas como bridge/exportador
•	CSVs: formato de transporte (UTF-8, separador ;)
•	SQLite: sistema de verdade (persistência e consultas)
0.3 Tabelas e normalização (confirmado)
•	Colunas em snake_case (já implementado no ingestor)
•	Tabelas rtd_* para dados raw vindos do Excel
•	Tabelas derivadas (payoff_curve_points, structure_decisions) para análises
________________________________________
1) Arquitetura atualizada (v1a)
1.1 Excel/RTD Layer (bridge only)
Responsabilidade: captura RTD + exportação CSV
•	Módulo: VBA BridgeExport (já implementado)
•	Output: pasta bridge/ com CSVs + last_export.txt
•	Frequência: configurável (default: 10s)
1.2 Ingest Layer (substituiu services/update_cycle.py)
Responsabilidade: importação CSV → app.db
•	Módulo: bridge_ingest_csv.py (já implementado)
•	Tabelas: rtd_* (snapshot + histórico conforme modo replace/append)
•	Validação: encoding, normalização, tolerância a dados faltantes
1.3 Domain Layer (próximas fases)
Responsabilidade: payoff + decisões a partir do raw
•	Módulos planejados:
•	domain/payoff.py
•	domain/decision.py
•	Input: tabelas rtd_* do app.db
•	Output: tabelas derivadas no derived.db
1.4 UI Layer (futuro)
Responsabilidade: consulta + visualização
•	Fonte: somente SQLite (nunca Excel direto)
________________________________________
2) Mapeamento de abas → tabelas (confirmado funcionando)
Aba Excel	Tabela SQLite	Modo	Status
ANALISE_RAIOX	rtd_analise_raiox	replace	✅
CONSOLIDACOES	rtd_consolidacoes	replace	✅
ANALISE_ROBO	rtd_analise_robo	replace	✅
ANALISE_ROBO_LEGS	rtd_analise_robo_legs	replace	✅
CONFIGURACOES	rtd_configuracoes	replace	✅
ROLLS_DETECTADOS	rtd_rolls_detectados	append	✅
HIST_ROBO	rtd_hist_robo	append	✅
ENCERRAMENTOS_MANUAIS	rtd_encerramentos_manuais	append	✅
Status confirmado: última validação mostrou 2459 linhas processadas com sucesso.
________________________________________
3) Schema SQLite (ajustado para v1a)
3.1 Raw tables (app.db) — ✅ IMPLEMENTADO
sql
-- Exemplo de estrutura atual (criada dinamicamente)CREATE TABLE rtd_analise_robo_legs (    ativo TEXT,    cv TEXT,     quant TEXT,    valor_executado TEXT,    -- ... todas as colunas normalizadas como TEXT);
3.2 Derived tables (derived.db) — 🔄 PRÓXIMA FASE
sql
-- Ajustado para compatibilidade com ingestor atualCREATE TABLE payoff_curve_points (    id INTEGER PRIMARY KEY AUTOINCREMENT,    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    s_t REAL NOT NULL,    pl_venc REAL NOT NULL,    spot_ref REAL,    meta_json TEXT,    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE structure_decisions (    id INTEGER PRIMARY KEY AUTOINCREMENT,    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    decision TEXT NOT NULL,    level INTEGER NOT NULL,    pl_atual REAL,    pl_max REAL,    pl_pct_of_max REAL,    dte_min INTEGER,    why_json TEXT,    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
________________________________________
4) Fases atualizadas (v1a)
✅ Fase 0 — Baseline fixado (CONCLUÍDO)
•	Branch baseline_v1 + docs/baseline_v1.md
•	Commit: chore: baseline v1 (docs)
✅ Fase 1 — Schema básico (CONCLUÍDO)
•	db/schema.py com tabelas derivadas
•	Commit: feat(db): add sqlite schema for derived tables
✅ Fase Extra — Bridge operacional (CONCLUÍDO)
•	VBA exportador + bridge_ingest_csv.py
•	Validação: 2459 linhas importadas, 8 tabelas rtd_* funcionais
🔄 Fase 2 — Repo derivadas (PRÓXIMO PASSO)
Objetivo: funções para gravar payoff/decisões
•	Atualizar db/repo.py ou criar db/derived_repo.py
•	Funções:
python
insert_payoff_points(conn, timestamp, aba, points, spot_ref)insert_structure_decision(conn, timestamp, aba, decision_dict)
•	Teste: scripts/test_derived_inserts.py
🔄 Fase 3 — Domain: Payoff (FUTURO)
Input: ler rtd_analise_robo_legs (em vez de COM/Excel)
•	domain/payoff.py com compute_payoff_curve()
•	Teste com estrutura real vinda do app.db
🔄 Fase 4 — Domain: Decision (FUTURO)
Input: usar dados de rtd_analise_robo + rtd_consolidacoes
•	domain/decision.py com thresholds 30/60/80
•	Gate DTE ≤ 7
🔄 Fase 5 — Integração payoff/decision (FUTURO)
Trigger: executar após cada ingest bem-sucedido
•	Adicionar hook em bridge_ingest_csv.py ou criar derived_processor.py
•	Gerar curvas + decisões para todas as abas ativas
________________________________________
5) Contratos técnicos (mantidos + atualizações)
5.1 Dados raw (confirmado)
•	Todas as colunas como TEXT no app.db (tolerância a variações do Excel)
•	Normalização de nomes já implementada (snake_case, sem acentos)
•	Timestamps em formato ISO where possível
5.2 Dados derivados (especificação)
•	Payoff: calculado em unidades (sem multiplicador/lote)
•	PL_atual: soma de lucro_prejuizo da aba
•	Grid default: 50%–150% do spot, step 1%
•	Thresholds: 0.30/0.60/0.80 conforme baseline original
5.3 Integração com consolidações (próximo)
•	Quando decision == "CLOSE_REOPEN": inserir em rtd_consolidacoes
•	Formato: obs = "CLOSE_REOPEN: PL_atual=X, PL_max=Y, Ratio=Z"
________________________________________
6) Status atual e próximo commit
✅ Pipeline operacional confirmado
Excel → bridge/*.csv → app.db (8 tabelas rtd_*) → derived.db (próximo)
🎯 Próximo passo (Fase 2)
Implementar repo para dados derivados
Arquivos a criar/editar:
1.	db/derived_repo.py (ou expandir db/repo.py)
2.	scripts/test_derived_inserts.py
3.	Validação com dados reais do rtd_*
Commit esperado: "feat(db): derived repo inserts for payoff + decisions"
________________________________________
7) Versionamento
•	baseline_v1: documento original (COM-based)
•	baseline_v1a: este documento (bridge CSV-based)
•	Próximas tags: v1a.2, v1a.3 conforme implementação das fases
Data desta atualização: 19/12/2024
Arquivo: docs/baseline_v1a.md
