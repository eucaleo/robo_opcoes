LOG de evolução (para ir “matando” o que resta)
1) Diagnóstico inicial (SQLite / schema)
•	Você inspecionou o schema do dados/derived.db:
•	payoff_curve_points tem as colunas:
•	timestamp (TEXT, NOT NULL)
•	aba (TEXT, NOT NULL)
•	spot_ref (REAL)
•	point_spot (REAL, NOT NULL)
•	point_pl (REAL, NOT NULL)
•	meta_json (TEXT)
•	created_at default datetime('now')
•	Também existe payoff_points, mas com esquema diferente e não é a tabela alvo do pipeline (ou é legado/auxiliar).
Decisão: alinhar o domínio para produzir pontos compatíveis com payoff_curve_points.
________________________________________
2) Causa provável do bug anterior
•	Seu pipeline (função tipo save_payoff_curve) esperava pontos como:
•	tuplas (point_spot, point_pl) ou
•	dicts com chaves point_spot/point_pl
•	Mas você tinha/teve pontos como dicts com chaves tipo s_t e pl_venc, gerando erro/KeyError no salvamento.
Ação: padronizar saída do domínio para (spot, pl).
________________________________________
3) Revisão do domain/payoff.py enviado por você
Status do arquivo original:
•	compute_payoff_curve() já estava retornando:
•	points.append((s_t, pl_total))
•	✅ formato correto para persistência (tupla spot, pl).
•	Porém havia pontos frágeis:
3.1) Problema de “snapshot” (mistura de timestamps)
•	read_structure_legs() quando timestamp=None fazia:
•	ORDER BY timestamp DESC ... LIMIT 10
•	Isso pode misturar legs de timestamps diferentes (dependendo do número de pernas / atualização).
Correção proposta:
•	Resolver MAX(timestamp) primeiro e buscar todas as legs daquele timestamp.
3.2) Normalização de cv (lado)
•	Assumir apenas cv == 'C' como comprado é frágil (pode vir V, BUY, SELL, etc.).
Correção proposta: normalizar para LONG/SHORT.
3.3) Normalização de call_put
•	Seu check if 'CALL' in call_put falha se vier C/P.
Correção proposta: aceitar CALL/C e PUT/P.
3.4) Bug no final do arquivo
•	Existia um ] sobrando no final do módulo, quebraria execução direta.
Correção proposta: remover.
________________________________________
4) Você confirmou os nomes das colunas
Você confirmou que em rtd_analise_robo_legs os campos são:
•	cv, call_put, quant, valor_executado, strike
✅ perfeito.
Depois você rodou o PRAGMA table_info(rtd_analise_robo_legs) e retornou o schema completo, confirmando:
•	existem timestamp, aba, ativo, cv, call_put, quant, valor_executado, strike, etc.
Decisão: manter o arquivo completo revisado sem renomear colunas.
________________________________________
Checklist de “restos” para matar (próximos passos práticos)
A) Validar que o domínio roda e gera pontos coerentes
Rode (exemplo):
bash
python -c "from domain.payoff import compute_payoff_for_aba; r=compute_payoff_for_aba('SUA_ABA'); print(r['aba'], r['timestamp_used'], len(r['points']), r['points'][:3])"
Esperado:
•	len(points) > 0
•	points[0] é tupla (float, float)
•	timestamp_used não é None
________________________________________
B) Validar o salvamento no derived.db (pipeline)
Depois de rodar a pipeline, conferir:
bash
python -c "import sqlite3; c=sqlite3.connect('dados/derived.db'); cur=c.cursor(); cur.execute('select aba, count(*) from payoff_curve_points group by aba order by count(*) desc'); print(cur.fetchall()[:10]); c.close()"
Esperado: contagens > 0 por aba.
________________________________________
C) Sanidade do snapshot (principal risco residual)
Se ainda der “curva estranha” (pulos, formato inconsistente), o primeiro suspeito é:
•	summary (spot) vindo de rtd_analise_robo com um timestamp
•	legs vindo de rtd_analise_robo_legs com outro timestamp
Se isso acontecer, o próximo ajuste é: fazer read_structure_summary() também por timestamp (pegar o mesmo timestamp_used das legs), ou armazenar e usar o timestamp comum entre as tabelas.


markdown
# LOG Técnico - executed_v1.md
## Pipeline de Derivados - Correção do Módulo `domain/payoff.py`
**Branch:** `executed_v1`  **Data:** 2026-04-20  **Responsável:** Carlos Rubio  
---
## 🔍 **PROBLEMA IDENTIFICADO**
### Sintomas- Pipeline falhava ao salvar curvas de payoff no `derived.db`- Possível KeyError/TypeError na persistência de pontos- Inconsistência entre formato esperado pela tabela `payoff_curve_points` e dados gerados
### Análise do Schema```sql-- Tabela alvo: payoff_curve_pointsCREATE TABLE payoff_curve_points (    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    spot_ref REAL,    point_spot REAL NOT NULL,    -- coordenada X    point_pl REAL NOT NULL,      -- coordenada Y      meta_json TEXT,    created_at TEXT DEFAULT (datetime('now')));
Diagnóstico
•	Pipeline esperava pontos como tuplas (point_spot, point_pl)
•	Possível mismatch de formato/chaves nos dados gerados pelo domínio
________________________________________
🎯 PROBLEMAS CRÍTICOS ENCONTRADOS
1) Snapshot Inconsistente (CRÍTICO)
Localização: read_structure_legs() linha ~65
python
# ANTES (PROBLEMÁTICO)cursor.execute("""    SELECT * FROM rtd_analise_robo_legs     WHERE aba = ?     ORDER BY timestamp DESC, strike     LIMIT 10""", (aba,))
Problema: Mistura legs de diferentes timestamps dependendo do número de pernas.
Impacto: Estruturas calculadas com dados de snapshots diferentes = curvas incorretas.
2) Normalização de cv Frágil
Localização: compute_payoff_curve() linha ~150
python
# ANTES (FRÁGIL)cv = str(leg.get('cv', '')).upper()if cv == 'C':  # longelse:          # short - ASSUME qualquer coisa != 'C'
Problema: Se cv vier como "BUY", "SELL", "B", "V" = comportamento incorreto.
3) Normalização de call_put Incompleta
python
# ANTES (INCOMPLETO)if 'CALL' in call_put:    intrinsic = max(s_t - strike, 0)else:    intrinsic = max(strike - s_t, 0)  # PUT
Problema: Se call_put="C", cai no else e vira PUT (incorreto).
4) Bug Sintático
Localização: Final do arquivo
python
        else:            print(f"❌ Não foi possível calcular payoff para '{test_aba}'")]  # <-- SOBRANDO, quebra execução direta
________________________________________
✅ SOLUÇÕES IMPLEMENTADAS
1) Snapshot Consistente
python
def read_structure_legs(aba: str, timestamp: Optional[str] = None) -> List[Dict]:    conn = get_app_db_connection()    cursor = conn.cursor()
    # Resolve timestamp mais recente se não informado    ts = timestamp    if ts is None:        cursor.execute(            "SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",            (aba,)        )        row = cursor.fetchone()        ts = row[0] if row else None
    if not ts:        conn.close()        return []
    # Carrega TODAS as legs do mesmo snapshot    cursor.execute(        """SELECT * FROM rtd_analise_robo_legs           WHERE aba = ? AND timestamp = ?           ORDER BY strike""",        (aba, ts)    )    # ... rest
2) Normalização Robusta de cv
python
def normalize_side(cv_raw: str) -> Optional[str]:    if cv_raw is None:        return None    s = str(cv_raw).strip().upper()    if s in ("C", "COMPRA", "COMPRADO", "BUY", "B", "LONG"):        return "LONG"    if s in ("V", "VENDA", "VENDIDO", "SELL", "S", "SHORT"):        return "SHORT"    return None
3) Normalização Robusta de call_put
python
cp = str(leg.get('call_put', '')).strip().upper()is_call = ("CALL" in cp) or (cp == "C")is_put  = ("PUT" in cp)  or (cp == "P")
if not (is_call or is_put):    continue
if is_call:    intrinsic = max(s_t - strike, 0)else:  # PUT    intrinsic = max(strike - s_t, 0)
4) Path Resolvido + Bug Fix
python
def get_app_db_connection():    """Conexão com app.db - resolve caminho para evitar erro de pasta"""    db_path = Path("dados/app.db").resolve()    return sqlite3.connect(str(db_path))
________________________________________
🧪 VALIDAÇÃO
Schema Source Confirmado
bash
$ python -c "import sqlite3; c=sqlite3.connect('dados/app.db'); cur=c.cursor(); cur.execute('PRAGMA table_info(rtd_analise_robo_legs)'); print(cur.fetchall()); c.close()"
Resultado: Campos cv, call_put, quant, valor_executado, strike confirmados.
Comandos de Teste
1) Teste Básico do Domínio
bash
python -c "from domain.payoff import compute_payoff_for_aba; r=compute_payoff_for_aba('SUA_ABA'); print(r['aba'], r['timestamp_used'], len(r['points']), r['points'][:3])"
Output Esperado:
ABA_TESTE 2026-04-20_17:44:39 101 [(50.0, -125.5), (50.5, -124.8), (51.0, -124.1)]
2) Verificar Persistência
bash
python -c "import sqlite3; c=sqlite3.connect('dados/derived.db'); cur=c.cursor(); cur.execute('select aba, count(*) from payoff_curve_points group by aba order by count(*) desc'); print(cur.fetchall()[:10]); c.close()"
Output Esperado:
[('ABA1', 101), ('ABA2', 101), ('ABA3', 101), ...]
3) Teste Direto do Módulo
bash
python domain/payoff.py
Output Esperado:
Testando payoff com dados reais...Abas disponíveis: ['ABA1', 'ABA2', 'ABA3']✅ Aba 'ABA1': 101 pontos, PL_max=250.75
________________________________________
📊 FORMATO FINAL DOS DADOS
Estrutura de Retorno
python
{    "points": [(point_spot, point_pl), ...],  # tuplas (X, Y)    "pl_max": float,    "pl_min": float,     "spot_ref": float,    "aba": str,    "timestamp_used": str,    "meta": {        "legs_count": int,        "grid_params": {...}    }}
Compatibilidade com payoff_curve_points
•	✅ points[i][0] → point_spot (REAL NOT NULL)
•	✅ points[i][1] → point_pl (REAL NOT NULL)
•	✅ spot_ref → spot_ref (REAL)
•	✅ timestamp_used → timestamp (TEXT NOT NULL)
________________________________________
🚦 STATUS
•	✅ CORRIGIDO: Snapshot consistency
•	✅ CORRIGIDO: Side normalization (cv)
•	✅ CORRIGIDO: Option type normalization (call_put)
•	✅ CORRIGIDO: Path resolution
•	✅ CORRIGIDO: Syntax bug
•	✅ TESTADO: Schema compatibility
Próximos Passos
1.	Executar pipeline completa
2.	Validar dados em derived.db
3.	Se houver "curva estranha", verificar sincronia timestamp entre rtd_analise_robo e rtd_analise_robo_legs
________________________________________
📝 ARQUIVOS ALTERADOS
•	domain/payoff.py - REESCRITO COMPLETO
Backup
Arquivo original salvo como domain/payoff_backup_20260420.py (recomendado).
________________________________________
22/04/2026
## P2 — Domain formal (payoff + decision) — Encerramento

### Objetivo
Consolidar o Domain Layer para:
- gerar curva de payoff no vencimento por aba (points compatíveis com derived.db)
- gerar decisão por aba (HOLD / PREPARE_ROLL / CLOSE_REOPEN) com thresholds 30/60/80 + gate DTE

### Ajuste crítico em domain/decision.py
**Bug:** compute_decision_for_aba() calculava `pl_atual` via `pl_realista_total` (rtd_analise_robo),
enquanto `pl_max` vinha da curva de payoff. Isso misturava fontes e gerava inconsistência.
Além disso, o ratio era zerado quando `pl_atual <= 0`, mascarando prejuízo.

**Fix:** `pl_atual` passou a ser calculado pela própria curva de payoff:
- calcula payoff via compute_payoff_for_aba(aba)
- interpola PL no spot_ref
- ratio = pl_atual / pl_max (quando pl_max > 0), permitindo ratio negativo

### Validação
Teste com `BOVA11`:
- spot_ref: 194.27
- pl_max: 381810
- pl_atual (decision): -11380
- ratio: -2.98%
- decision: HOLD (level 0)
- why_json inclui spread_pct_medio e dte_min

### Status
P2 concluído e consistente: payoff + decision usam a mesma fonte para PL e ratio.
Próximo: P3 (Hook pós-ingest) — acionar derivadores após ingest do bridge_ingest_csv.py.

## P2 — Domain formal (payoff + decision) — Encerramento

### Objetivo
Consolidar o Domain Layer para:
- gerar curva de payoff no vencimento por aba (points compatíveis com derived.db)
- gerar decisão por aba (HOLD / PREPARE_ROLL / CLOSE_REOPEN) com thresholds 30/60/80 + gate DTE

### Ajuste crítico em domain/decision.py
**Bug:** compute_decision_for_aba() calculava `pl_atual` via `pl_realista_total` (rtd_analise_robo),
enquanto `pl_max` vinha da curva de payoff. Isso misturava fontes e gerava inconsistência.
Além disso, o ratio era zerado quando `pl_atual <= 0`, mascarando prejuízo.

**Fix:** `pl_atual` passou a ser calculado pela própria curva de payoff:
- calcula payoff via compute_payoff_for_aba(aba)
- interpola PL no spot_ref
- ratio = pl_atual / pl_max (quando pl_max > 0), permitindo ratio negativo

### Validação
Teste com `BOVA11`:
- spot_ref: 194.27
- pl_max: 381810
- pl_atual (decision): -11380
- ratio: -2.98%
- decision: HOLD (level 0)
- why_json inclui spread_pct_medio e dte_min

### Status
P2 concluído e consistente: payoff + decision usam a mesma fonte para PL e ratio.
Próximo: P3 (Hook pós-ingest) — acionar derivadores após ingest do bridge_ingest_csv.py.

22/04/2026
## P3 - Pipeline de Dados Derivados (✅ CONCLUÍDO)

### Objetivo
Implementar processamento automático de dados derivados (payoffs e decisões de estruturas) com integração ao sistema de ingestão.

### Componentes Implementados

#### 1. **Schema de Dados Derivados** (`db/derived_repo.py`)
- **Tabela `payoff_curve_points`**: Pontos da curva de payoff por estrutura/timestamp
- **Tabela `structure_decisions`**: Decisões automatizadas (HOLD, ROLL, etc.) com métricas
- **Funções de inserção e consulta** com suporte a tuplas e dicts
- **Cleanup automático** de dados antigos (30+ dias)

```sql
-- Estrutura das tabelas criadas
payoff_curve_points: id, timestamp, aba, s_t, pl_venc, spot_ref, meta_json
structure_decisions: id, timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max, dte_min, why_json

## P4 — Hook de consolidação automática no fechamento de estrutura (CLOSE_REOPEN)

### Implementado
Quando a decisão computada para uma aba retorna `"CLOSE_REOPEN"`, o pipeline agora:
- insere automaticamente uma linha em `rtd_consolidacoes` (na dados/app.db)
- os campos essenciais (`timestamp`, `aba`, `obs`) são preenchidos, e os outros permanecem em branco
- o campo `obs` segue o padrão: `"CLOSE_REOPEN: PL_atual=X, PL_max=Y, Ratio=Z%"`
- o timestamp usado é sempre o do snapshot real (`timestamp_used`), garantindo total rastreabilidade e sincronismo nos dados derivados e raw.

### Código relacionado
- Função auxiliar: `insert_consolidacao_close_reopen(...)` em `services/derived_service.py`
- Chamada direta no pipeline, logo após a decisão e persistência da decisão em derived.

---

**Com isso, o pipeline está 100% aderente ao baseline.**
