# Diagnóstico da persistência RTD/opções — Fase 3

Documento automático de auditoria da Fase 3 da `ROTA_MESTRE_2`.

## Escopo

Esta etapa audita, sem alteração funcional, a persistência e leitura de cotações RTD/opções.

Arquivos inicialmente auditados:

- `repositories/rtd_option_quotes_repository.py`
- `repositories/market_snapshot_repository.py`
- `services/market_snapshot_provider.py`
- `services/market_snapshot_selector.py`

Tabelas-alvo:

- `rtd_option_quotes`
- `rtd_analise_robo_legs`
- `rtd_analise_robo`
- `manual_analise_robo_legs`

Nenhum arquivo operacional, banco, schema, CSV, Excel, UI ou cálculo foi alterado por este diagnóstico.

## Resumo dos arquivos auditados

### `repositories/rtd_option_quotes_repository.py`

- Existe: `True`
- Linhas: `119`
- Contém `INSERT INTO`: `False`
- Contém `UPDATE`: `False`
- Contém `DELETE FROM`: `False`
- Contém `CREATE TABLE`: `False`
- Menciona `rtd_option_quotes`: `True`
- Menciona `rtd_analise_robo_legs`: `False`
- Menciona `rtd_analise_robo`: `False`
- Menciona `manual_analise_robo_legs`: `False`

### `repositories/market_snapshot_repository.py`

- Existe: `True`
- Linhas: `254`
- Contém `INSERT INTO`: `False`
- Contém `UPDATE`: `False`
- Contém `DELETE FROM`: `False`
- Contém `CREATE TABLE`: `False`
- Menciona `rtd_option_quotes`: `False`
- Menciona `rtd_analise_robo_legs`: `True`
- Menciona `rtd_analise_robo`: `True`
- Menciona `manual_analise_robo_legs`: `True`

### `services/market_snapshot_provider.py`

- Existe: `True`
- Linhas: `70`
- Contém `INSERT INTO`: `False`
- Contém `UPDATE`: `False`
- Contém `DELETE FROM`: `False`
- Contém `CREATE TABLE`: `False`
- Menciona `rtd_option_quotes`: `False`
- Menciona `rtd_analise_robo_legs`: `False`
- Menciona `rtd_analise_robo`: `False`
- Menciona `manual_analise_robo_legs`: `False`

### `services/market_snapshot_selector.py`

- Existe: `True`
- Linhas: `107`
- Contém `INSERT INTO`: `False`
- Contém `UPDATE`: `False`
- Contém `DELETE FROM`: `False`
- Contém `CREATE TABLE`: `False`
- Menciona `rtd_option_quotes`: `False`
- Menciona `rtd_analise_robo_legs`: `False`
- Menciona `rtd_analise_robo`: `False`
- Menciona `manual_analise_robo_legs`: `False`

## Diagnóstico do banco

- Banco inspecionado: `dados\app.db`
- Banco existe: `True`

### Tabela `rtd_option_quotes`

- Existe: `True`
- Total de linhas: `1`

Colunas:

- `id` — tipo `INTEGER`, pk `1`, not null `0`
- `codigo_opcao` — tipo `TEXT`, pk `0`, not null `1`
- `ativo_base` — tipo `TEXT`, pk `0`, not null `0`
- `call_put` — tipo `TEXT`, pk `0`, not null `0`
- `strike` — tipo `REAL`, pk `0`, not null `0`
- `vencimento` — tipo `TEXT`, pk `0`, not null `0`
- `ultimo_preco` — tipo `REAL`, pk `0`, not null `0`
- `ultima_quantidade` — tipo `REAL`, pk `0`, not null `0`
- `bid` — tipo `REAL`, pk `0`, not null `0`
- `ask` — tipo `REAL`, pk `0`, not null `0`
- `volume` — tipo `REAL`, pk `0`, not null `0`
- `iv` — tipo `REAL`, pk `0`, not null `0`
- `delta` — tipo `REAL`, pk `0`, not null `0`
- `gamma` — tipo `REAL`, pk `0`, not null `0`
- `theta` — tipo `REAL`, pk `0`, not null `0`
- `vega` — tipo `REAL`, pk `0`, not null `0`
- `source` — tipo `TEXT`, pk `0`, not null `1`
- `raw_json` — tipo `TEXT`, pk `0`, not null `0`
- `updated_at` — tipo `TEXT`, pk `0`, not null `1`
- `created_at` — tipo `TEXT`, pk `0`, not null `1`

DDL registrado no SQLite:

```sql
CREATE TABLE rtd_option_quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo_opcao TEXT NOT NULL,
    ativo_base TEXT,

    call_put TEXT,
    strike REAL,
    vencimento TEXT,

    ultimo_preco REAL,
    ultima_quantidade REAL,

    bid REAL,
    ask REAL,
    volume REAL,

    iv REAL,
    delta REAL,
    gamma REAL,
    theta REAL,
    vega REAL,

    source TEXT NOT NULL DEFAULT 'rtd_links',
    raw_json TEXT,

    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(codigo_opcao)
)
```

Amostra de até 3 linhas:

```json
[
  {
    "id": 4,
    "codigo_opcao": "PETRA123",
    "ativo_base": "PETR4",
    "call_put": "CALL",
    "strike": 32.5,
    "vencimento": "2026-07-19",
    "ultimo_preco": 1.23,
    "ultima_quantidade": null,
    "bid": 1.2,
    "ask": 1.25,
    "volume": 10000.0,
    "iv": null,
    "delta": null,
    "gamma": null,
    "theta": null,
    "vega": null,
    "source": "rtd_links_csv",
    "raw_json": "[{\"codigo_opcao\": \"PETRA123\", \"ativo_base\": \"PETR4\", \"campo\": \"call_put\", \"valor\": \"CALL\", \"atualizado_em\": \"2026-06-06 17:50:00\"}, {\"codigo_opcao\": \"PETRA123\", \"ativo_base\": \"PETR4\", \"campo\": \"strike\", \"valor\": \"32.50\", \"atualizado_em\": \"2026-06-06 17:50:00\"}, {\"codigo_opcao\": \"PETRA123\", \"ativo_base\": \"PETR4\", \"campo\": \"vencimento\", \"valor\": \"2026-07-19\", \"atualizado_em\": \"2026-06-06 17:50:00\"}, {\"codigo_opcao\": \"PETRA123\", \"ativo_base\": \"PETR4\", \"campo\": \"ultimo_preco\", \"valor\": \"1.23\", \"atualizado_em\": \"2026-06-06 17:50:00\"}, {\"codigo_opcao\": \"PETRA123\", \"ativo_base\": \"PETR4\", \"campo\": \"bid\", \"valor\": \"1.20\", \"atualizado_em\": \"2026-06-06 17:50:00\"}, {\"codigo_opcao\": \"PETRA123\", \"ativo_base\": \"PETR4\", \"campo\": \"ask\", \"valor\": \"1.25\", \"atualizado_em\": \"2026-06-06 17:50:00\"}, {\"codigo_opcao\": \"PETRA123\", \"ativo_base\": \"PETR4\", \"campo\": \"volume\", \"valor\": \"10000\", \"atualizado_em\": \"2026-06-06 17:50:00\"}]",
    "updated_at": "2026-06-06 21:02:13",
    "created_at": "2026-06-06 21:02:13"
  }
]
```

### Tabela `rtd_analise_robo_legs`

- Existe: `True`
- Total de linhas: `20`

Colunas:

- `timestamp` — tipo `TEXT`, pk `0`, not null `0`
- `aba` — tipo `TEXT`, pk `0`, not null `0`
- `ativo` — tipo `TEXT`, pk `0`, not null `0`
- `cv` — tipo `TEXT`, pk `0`, not null `0`
- `call_put` — tipo `TEXT`, pk `0`, not null `0`
- `quant` — tipo `TEXT`, pk `0`, not null `0`
- `valor_executado` — tipo `TEXT`, pk `0`, not null `0`
- `bid` — tipo `TEXT`, pk `0`, not null `0`
- `ask` — tipo `TEXT`, pk `0`, not null `0`
- `spread` — tipo `TEXT`, pk `0`, not null `0`
- `spread_pct` — tipo `TEXT`, pk `0`, not null `0`
- `iv` — tipo `TEXT`, pk `0`, not null `0`
- `delta` — tipo `TEXT`, pk `0`, not null `0`
- `gamma` — tipo `TEXT`, pk `0`, not null `0`
- `theta` — tipo `TEXT`, pk `0`, not null `0`
- `vega` — tipo `TEXT`, pk `0`, not null `0`
- `strike` — tipo `TEXT`, pk `0`, not null `0`
- `vencimento` — tipo `TEXT`, pk `0`, not null `0`
- `dte` — tipo `TEXT`, pk `0`, not null `0`
- `pl_realista` — tipo `TEXT`, pk `0`, not null `0`
- `timestamp_aba_ativo_c_v_call_put_quant_valor_executado_bid_ask_spread_spread_pct_iv_delta_gamma_theta_vega_strike_vencimento_dte_pl_realista` — tipo `TEXT`, pk `0`, not null `0`

DDL registrado no SQLite:

```sql
CREATE TABLE "rtd_analise_robo_legs" ("timestamp" TEXT, "aba" TEXT, "ativo" TEXT, "cv" TEXT, "call_put" TEXT, "quant" TEXT, "valor_executado" TEXT, "bid" TEXT, "ask" TEXT, "spread" TEXT, "spread_pct" TEXT, "iv" TEXT, "delta" TEXT, "gamma" TEXT, "theta" TEXT, "vega" TEXT, "strike" TEXT, "vencimento" TEXT, "dte" TEXT, "pl_realista" TEXT, "timestamp_aba_ativo_c_v_call_put_quant_valor_executado_bid_ask_spread_spread_pct_iv_delta_gamma_theta_vega_strike_vencimento_dte_pl_realista" TEXT)
```

Amostra de até 3 linhas:

```json
[
  {
    "timestamp": "14/04/2026 17:55:51",
    "aba": "EMBJ3",
    "ativo": "EMBJE868",
    "cv": "C",
    "call_put": "CALL",
    "quant": "7000",
    "valor_executado": "1.38",
    "bid": "4.84",
    "ask": "4.93",
    "spread": "0.09",
    "spread_pct": "1.842374616",
    "iv": "37.78",
    "delta": "0.5909",
    "gamma": "0.039",
    "theta": "4.85",
    "vega": "10.2557",
    "strike": "86.81",
    "vencimento": "5/15/2026 3:00",
    "dte": "31",
    "pl_realista": "24220",
    "timestamp_aba_ativo_c_v_call_put_quant_valor_executado_bid_ask_spread_spread_pct_iv_delta_gamma_theta_vega_strike_vencimento_dte_pl_realista": null
  },
  {
    "timestamp": "14/04/2026 17:55:51",
    "aba": "EMBJ3",
    "ativo": "EMBJE704",
    "cv": "V",
    "call_put": "CALL",
    "quant": "4000",
    "valor_executado": "8.35",
    "bid": "0",
    "ask": "21.03",
    "spread": "21.03",
    "spread_pct": "200",
    "iv": "38.57",
    "delta": "0.982",
    "gamma": "0.0043",
    "theta": "18.55",
    "vega": "1.1667",
    "strike": "69.81",
    "vencimento": "5/15/2026 3:00",
    "dte": "31",
    "pl_realista": "-50720",
    "timestamp_aba_ativo_c_v_call_put_quant_valor_executado_bid_ask_spread_spread_pct_iv_delta_gamma_theta_vega_strike_vencimento_dte_pl_realista": null
  },
  {
    "timestamp": "14/04/2026 17:55:51",
    "aba": "EMBJ3",
    "ativo": "EMBJQ878",
    "cv": "V",
    "call_put": "PUT",
    "quant": "4000",
    "valor_executado": "4.85",
    "bid": "3.72",
    "ask": "3.82",
    "spread": "0.1",
    "spread_pct": "2.652519894",
    "iv": "48.58",
    "delta": "-0.4484",
    "gamma": "0.0308",
    "theta": "4.74",
    "vega": "10.442",
    "strike": "87.81",
    "vencimento": "5/15/2026 3:00",
    "dte": "31",
    "pl_realista": "4120",
    "timestamp_aba_ativo_c_v_call_put_quant_valor_executado_bid_ask_spread_spread_pct_iv_delta_gamma_theta_vega_strike_vencimento_dte_pl_realista": null
  }
]
```

### Tabela `rtd_analise_robo`

- Existe: `True`
- Total de linhas: `5`

Colunas:

- `aba` — tipo `TEXT`, pk `0`, not null `0`
- `spot` — tipo `TEXT`, pk `0`, not null `0`
- `num_pernas` — tipo `TEXT`, pk `0`, not null `0`
- `dte_min` — tipo `TEXT`, pk `0`, not null `0`
- `pl_realista_total` — tipo `TEXT`, pk `0`, not null `0`
- `delta_liq` — tipo `TEXT`, pk `0`, not null `0`
- `gamma_liq` — tipo `TEXT`, pk `0`, not null `0`
- `theta_liq` — tipo `TEXT`, pk `0`, not null `0`
- `vega_liq` — tipo `TEXT`, pk `0`, not null `0`
- `spread_medio` — tipo `TEXT`, pk `0`, not null `0`
- `spread_pct_medio` — tipo `TEXT`, pk `0`, not null `0`
- `alertas_v2` — tipo `TEXT`, pk `0`, not null `0`
- `aba_spot_num_pernas_dte_min_pl_realista_total_delta_liq_gamma_liq_theta_liq_vega_liq_spread_medio_spread_pct_medio_alertas_v2` — tipo `TEXT`, pk `0`, not null `0`

DDL registrado no SQLite:

```sql
CREATE TABLE "rtd_analise_robo" ("aba" TEXT, "spot" TEXT, "num_pernas" TEXT, "dte_min" TEXT, "pl_realista_total" TEXT, "delta_liq" TEXT, "gamma_liq" TEXT, "theta_liq" TEXT, "vega_liq" TEXT, "spread_medio" TEXT, "spread_pct_medio" TEXT, "alertas_v2" TEXT, "aba_spot_num_pernas_dte_min_pl_realista_total_delta_liq_gamma_liq_theta_liq_vega_liq_spread_medio_spread_pct_medio_alertas_v2" TEXT)
```

Amostra de até 3 linhas:

```json
[
  {
    "aba": "EMBJ3",
    "spot": "87.37",
    "num_pernas": "4",
    "dte_min": "31",
    "pl_realista_total": "-30500",
    "delta_liq": "1776.5",
    "gamma_liq": "166.2",
    "theta_liq": "-57810",
    "vega_liq": "38685.2",
    "spread_medio": "5.3125",
    "spread_pct_medio": "55.9624333",
    "alertas_v2": "Delta alto; Vega alto",
    "aba_spot_num_pernas_dte_min_pl_realista_total_delta_liq_gamma_liq_theta_liq_vega_liq_spread_medio_spread_pct_medio_alertas_v2": null
  },
  {
    "aba": "BOVA11",
    "spot": "194.27",
    "num_pernas": "4",
    "dte_min": "31",
    "pl_realista_total": "-3590",
    "delta_liq": "322.5",
    "gamma_liq": "75.6",
    "theta_liq": "-108220",
    "vega_liq": "59739.7",
    "spread_medio": "0.045",
    "spread_pct_medio": "1.68087761",
    "alertas_v2": "Vega alto",
    "aba_spot_num_pernas_dte_min_pl_realista_total_delta_liq_gamma_liq_theta_liq_vega_liq_spread_medio_spread_pct_medio_alertas_v2": null
  },
  {
    "aba": "PRIO3",
    "spot": "66.84",
    "num_pernas": "4",
    "dte_min": "3",
    "pl_realista_total": "-4014",
    "delta_liq": "-612.31",
    "gamma_liq": "9.34",
    "theta_liq": "-39257",
    "vega_liq": "-13363.59",
    "spread_medio": "0.085",
    "spread_pct_medio": "4.448687402",
    "alertas_v2": "Vega alto",
    "aba_spot_num_pernas_dte_min_pl_realista_total_delta_liq_gamma_liq_theta_liq_vega_liq_spread_medio_spread_pct_medio_alertas_v2": null
  }
]
```

### Tabela `manual_analise_robo_legs`

- Existe: `True`
- Total de linhas: `0`

Colunas:

- `timestamp` — tipo `TEXT`, pk `0`, not null `1`
- `aba` — tipo `TEXT`, pk `0`, not null `1`
- `ativo` — tipo `TEXT`, pk `0`, not null `0`
- `cv` — tipo `TEXT`, pk `0`, not null `0`
- `call_put` — tipo `TEXT`, pk `0`, not null `0`
- `quant` — tipo `TEXT`, pk `0`, not null `0`
- `valor_executado` — tipo `TEXT`, pk `0`, not null `0`
- `bid` — tipo `TEXT`, pk `0`, not null `0`
- `ask` — tipo `TEXT`, pk `0`, not null `0`
- `spread` — tipo `TEXT`, pk `0`, not null `0`
- `spread_pct` — tipo `TEXT`, pk `0`, not null `0`
- `iv` — tipo `TEXT`, pk `0`, not null `0`
- `delta` — tipo `TEXT`, pk `0`, not null `0`
- `gamma` — tipo `TEXT`, pk `0`, not null `0`
- `theta` — tipo `TEXT`, pk `0`, not null `0`
- `vega` — tipo `TEXT`, pk `0`, not null `0`
- `strike` — tipo `TEXT`, pk `0`, not null `0`
- `vencimento` — tipo `TEXT`, pk `0`, not null `0`
- `dte` — tipo `TEXT`, pk `0`, not null `0`
- `pl_realista` — tipo `TEXT`, pk `0`, not null `0`
- `source` — tipo `TEXT`, pk `0`, not null `0`
- `created_at` — tipo `TEXT`, pk `0`, not null `0`

DDL registrado no SQLite:

```sql
CREATE TABLE manual_analise_robo_legs (
  timestamp       TEXT NOT NULL,
  aba             TEXT NOT NULL,
  ativo           TEXT,
  cv              TEXT,
  call_put        TEXT,
  quant           TEXT,
  valor_executado TEXT,
  bid             TEXT,
  ask             TEXT,
  spread          TEXT,
  spread_pct      TEXT,
  iv              TEXT,
  delta           TEXT,
  gamma           TEXT,
  theta           TEXT,
  vega            TEXT,
  strike          TEXT,
  vencimento      TEXT,
  dte             TEXT,
  pl_realista     TEXT,
  source          TEXT DEFAULT 'manual',
  created_at      TEXT DEFAULT (datetime('now'))
)
```

## Referências encontradas no projeto

### Termo `rtd_option_quotes`

- `_repo_audit/rota_mestre_2_fase1/mapear_automacao_opcoes_rtd_backup_20260613_185438.py` — `7` ocorrência(s)
  - linha `107`: `"rtd_option_quotes",`
  - linha `145`: `"scripts/patch_73_rtd_option_quotes.py",`
  - linha `147`: `"repositories/rtd_option_quotes_repository.py",`
  - linha `346`: `if "repositories/rtd_option_quotes_repository.py" in existing_paths:`
  - linha `348`: `"Auditar repositories/rtd_option_quotes_repository.py como provável ponto de persistência das cotações de opções."`
  - linha `351`: `if "scripts/patch_73_rtd_option_quotes.py" in existing_paths:`
  - linha `353`: `"Auditar scripts/patch_73_rtd_option_quotes.py para entender schema/tabela de cotações RTD de opções."`
- `docs/AUDITORIA_ROTA_MESTRE_2.md` — `3` ocorrência(s)
  - linha `175`: `- `repositories/rtd_option_quotes_repository.py``
  - linha `231`: `- `repositories/rtd_option_quotes_repository.py``
  - linha `365`: `- `repositories/rtd_option_quotes_repository.py``
- `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `5` ocorrência(s)
  - linha `238`: `repositories/rtd_option_quotes_repository.py`
  - linha `244`: `rtd_option_quotes`
  - linha `306`: `rtd_option_quotes`
  - linha `317`: `repositories/rtd_option_quotes_repository.py`
  - linha `501`: `- fonte atual: app.db, rtd_option_quotes, rtd_analise_robo_legs e provider temporário`
- `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` — `1` ocorrência(s)
  - linha `280`: `| `rtd_option_quotes` | entrada bruta | tratar como cotação importada/normalizada |`
- `docs/FASE_6_CAMADA_CANONICA_LEITURA.md` — `5` ocorrência(s)
  - linha `84`: `- `repositories/rtd_option_quotes_repository.py``
  - linha `91`: `- `rtd_option_quotes``
  - linha `97`: `- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.`
  - linha `205`: `- `repositories/rtd_option_quotes_repository.py``
  - linha `255`: `- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.`
- `docs/fase_8_banco_fonte_verdade_auditoria.md` — `6` ocorrência(s)
  - linha `105`: `- rtd_option_quotes`
  - linha `123`: `- rtd_option_quotes: 1`
  - linha `138`: `- rtd_option_quotes`
  - linha `146`: `- rtd_option_quotes possui apenas um registro no estado analisado.`
  - linha `261`: `- rtd_option_quotes`
  - linha `281`: `- rtd_option_quotes`
- `docs/lista_priorizada_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `36`: `### `repositories/rtd_option_quotes_repository.py``
- `docs/mapeamento_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `324`: `### `repositories/rtd_option_quotes_repository.py``
- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `5` ocorrência(s)
  - linha `748`: `repositories/rtd_option_quotes_repository.py`
  - linha `813`: `scripts/patch_73_rtd_option_quotes.py`
  - linha `877`: `•	criar tabela nova antes de auditar rtd_option_quotes_repository.py`
  - linha `991`: `•	confirmar se rtd_option_quotes existe no banco`
  - linha `995`: `•	auditar repositories/rtd_option_quotes_repository.py`
- `repositories/rtd_option_quotes_repository.py` — `5` ocorrência(s)
  - linha `1`: `# repositories/rtd_option_quotes_repository.py`
  - linha `12`: `Leitura da tabela rtd_option_quotes.`
  - linha `48`: `FROM rtd_option_quotes`
  - linha `80`: `FROM rtd_option_quotes`
  - linha `112`: `FROM rtd_option_quotes`
- `scripts/mapear_automacao_opcoes_rtd.py` — `1` ocorrência(s)
  - linha `69`: `"repositories/rtd_option_quotes_repository.py": "Prioritário para auditoria de persistência RTD.",`

### Termo `rtd_analise_robo_legs`

- `ATT/tests/test_legacy_structure_legs_importer_integration.py` — `2` ocorrência(s)
  - linha `65`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `132`: `INSERT INTO rtd_analise_robo_legs (`
- `ATT/tests/test_legacy_structure_legs_reader.py` — `2` ocorrência(s)
  - linha `142`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `180`: `INSERT INTO rtd_analise_robo_legs`
- `ATT/tests/test_robo_legs_repository.py` — `5` ocorrência(s)
  - linha `25`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `54`: `INSERT INTO rtd_analise_robo_legs`
  - linha `79`: `INSERT INTO rtd_analise_robo_legs`
  - linha `133`: `INSERT INTO rtd_analise_robo_legs`
  - linha `158`: `INSERT INTO rtd_analise_robo_legs`
- `ATT/tests/test_robo_legs_status_repository.py` — `3` ocorrência(s)
  - linha `15`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `26`: `"INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `48`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
- `bridge_ingest_csv.py` — `1` ocorrência(s)
  - linha `36`: `CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),`
- `docs/baseline_v1a.md` — `3` ocorrência(s)
  - linha `51`: `ANALISE_ROBO_LEGS	rtd_analise_robo_legs	replace	[OK]`
  - linha `61`: `-- Exemplo de estrutura atual (criada dinamicamente)CREATE TABLE rtd_analise_robo_legs (    ativo TEXT,    cv TEXT,     quant TEXT,    valor_executado TEXT,    -- ... todas as colunas normalizadas como TEXT);`
  - linha `85`: `Input: ler rtd_analise_robo_legs (em vez de COM/Excel)`
- `docs/baseline_v2.md` — `2` ocorrência(s)
  - linha `8`: `| rtd_analise_robo_legs     |        [v]         |                         | Legs (pernas) de cada estrutura                        |`
  - linha `27`: `- `rtd_analise_robo_legs`, associando `aba`, `timestamp`, detalhes das pernas`
- `docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `1` ocorrência(s)
  - linha `160`: `- `rtd_analise_robo_legs``
- `docs/executed_v1.md` — `8` ocorrência(s)
  - linha `45`: `Você confirmou que em rtd_analise_robo_legs os campos são:`
  - linha `48`: `Depois você rodou o PRAGMA table_info(rtd_analise_robo_legs) e retornou o schema completo, confirmando:`
  - linha `71`: `*	legs vindo de rtd_analise_robo_legs com outro timestamp`
  - linha `91`: `# ANTES (PROBLEMÁTICO)cursor.execute("""    SELECT * FROM rtd_analise_robo_legs     WHERE aba = ?     ORDER BY timestamp DESC, strike     LIMIT 10""", (aba,))`
  - linha `112`: `# Resolve timestamp mais recente se não informado    ts = timestamp    if ts is None:        cursor.execute(            "SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",            (aba,)        )        row = cursor.fetchon`
  - linha `114`: `# Carrega TODAS as legs do mesmo snapshot    cursor.execute(        """SELECT * FROM rtd_analise_robo_legs           WHERE aba = ? AND timestamp = ?           ORDER BY strike""",        (aba, ts)    )    # ... rest`
  - linha `130`: `$ python -c "import sqlite3; c=sqlite3.connect('dados/app.db'); cur=c.cursor(); cur.execute('PRAGMA table_info(rtd_analise_robo_legs)'); print(cur.fetchall()); c.close()"`
  - linha `169`: `3.	Se houver "curva estranha", verificar sincronia timestamp entre rtd_analise_robo e rtd_analise_robo_legs`
- `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `6` ocorrência(s)
  - linha `179`: `rtd_analise_robo_legs`
  - linha `215`: `rtd_analise_robo_legs`
  - linha `308`: `rtd_analise_robo_legs`
  - linha `461`: `rtd_analise_robo_legs`
  - linha `498`: `- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs`
  - linha `501`: `- fonte atual: app.db, rtd_option_quotes, rtd_analise_robo_legs e provider temporário`
- `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` — `2` ocorrência(s)
  - linha `138`: `rtd_analise_robo_legs`
  - linha `277`: `| `rtd_analise_robo_legs` | legado | isolar e substituir progressivamente |`
- `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md` — `11` ocorrência(s)
  - linha `81`: `bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),`
  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `90`: `repositories/market_snapshot_repository.py:50:    FROM rtd_analise_robo_legs`
  - linha `93`: `repositories/robo_legs_repository.py:35:      manual_analise_robo_legs > rtd_analise_robo_legs`
  - linha `95`: `repositories/robo_legs_repository.py:72:            table="rtd_analise_robo_legs",`
  - linha `98`: `repositories/robo_legs_repository.py:111:                    SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?`
  - linha `100`: `repositories/robo_legs_repository.py:127:                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "`
  - linha `102`: `repositories/robo_legs_status_repository.py:57:                "SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",`
- `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md` — `1` ocorrência(s)
  - linha `134`: `rtd_analise_robo_legs`
- `docs/FASE_6_CAMADA_CANONICA_LEITURA.md` — `4` ocorrência(s)
  - linha `67`: `- `rtd_analise_robo_legs``
  - linha `89`: `- `rtd_analise_robo_legs``
  - linha `101`: `- `manual_analise_robo_legs > rtd_analise_robo_legs``
  - linha `256`: `- A regra `manual_analise_robo_legs > rtd_analise_robo_legs` deve ser preservada.`
- `docs/fase_8_banco_fonte_verdade_auditoria.md` — `21` ocorrência(s)
  - linha `100`: `- rtd_analise_robo_legs`
  - linha `118`: `- rtd_analise_robo_legs: 20`
  - linha `152`: `- rtd_analise_robo_legs`
  - linha `251`: `- A próxima ação técnica deve mapear como as estruturas existentes em structures se relacionam com rtd_analise_robo_legs e como esse vínculo pode ser migrado ou normalizado sem corromper dados.`
  - linha `259`: `- rtd_analise_robo_legs`
  - linha `279`: `- rtd_analise_robo_legs`
  - linha `344`: `## Resultado da inspeção de rtd_analise_robo_legs`
  - linha `346`: `A tabela `rtd_analise_robo_legs` possui 20 registros.`
- `docs/MAPA_MODULOS_FUNCOES.md` — `5` ocorrência(s)
  - linha `338`: `## rtd_analise_robo_legs`
  - linha `341`: `- linha 60: `"SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",``
  - linha `342`: `- linha 60: `"SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",``
  - linha `343`: `- linha 72: `SELECT * FROM rtd_analise_robo_legs``
  - linha `344`: `- linha 72: `SELECT * FROM rtd_analise_robo_legs``
- `docs/roteiro_v2.md` — `1` ocorrência(s)
  - linha `6`: `- Estruturas/abas populadas via `rtd_analise_robo`, legs em `rtd_analise_robo_legs``
- `docs/SQL_SURFACE_MAP_v2.md` — `1` ocorrência(s)
  - linha `6`: `| rtd_analise_robo_legs   | SELECT            | domain/payoff.py                                 |`
- `repositories/market_snapshot_repository.py` — `2` ocorrência(s)
  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `50`: `FROM rtd_analise_robo_legs`
- `repositories/robo_legs_repository.py` — `4` ocorrência(s)
  - linha `35`: `manual_analise_robo_legs > rtd_analise_robo_legs`
  - linha `72`: `table="rtd_analise_robo_legs",`
  - linha `111`: `SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?`
  - linha `127`: `"SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "`
- `repositories/robo_legs_status_repository.py` — `1` ocorrência(s)
  - linha `57`: `"SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",`

### Termo `rtd_analise_robo`

- `ATT/tests/test_legacy_structure_legs_importer_integration.py` — `2` ocorrência(s)
  - linha `65`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `132`: `INSERT INTO rtd_analise_robo_legs (`
- `ATT/tests/test_legacy_structure_legs_reader.py` — `2` ocorrência(s)
  - linha `142`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `180`: `INSERT INTO rtd_analise_robo_legs`
- `ATT/tests/test_robo_legs_repository.py` — `5` ocorrência(s)
  - linha `25`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `54`: `INSERT INTO rtd_analise_robo_legs`
  - linha `79`: `INSERT INTO rtd_analise_robo_legs`
  - linha `133`: `INSERT INTO rtd_analise_robo_legs`
  - linha `158`: `INSERT INTO rtd_analise_robo_legs`
- `ATT/tests/test_robo_legs_status_repository.py` — `3` ocorrência(s)
  - linha `15`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `26`: `"INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `48`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
- `bridge_ingest_csv.py` — `2` ocorrência(s)
  - linha `35`: `CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),`
  - linha `36`: `CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),`
- `docs/baseline_v1a.md` — `5` ocorrência(s)
  - linha `50`: `ANALISE_ROBO	rtd_analise_robo	replace	[OK]`
  - linha `51`: `ANALISE_ROBO_LEGS	rtd_analise_robo_legs	replace	[OK]`
  - linha `61`: `-- Exemplo de estrutura atual (criada dinamicamente)CREATE TABLE rtd_analise_robo_legs (    ativo TEXT,    cv TEXT,     quant TEXT,    valor_executado TEXT,    -- ... todas as colunas normalizadas como TEXT);`
  - linha `85`: `Input: ler rtd_analise_robo_legs (em vez de COM/Excel)`
  - linha `89`: `Input: usar dados de rtd_analise_robo + rtd_consolidacoes`
- `docs/baseline_v2.md` — `4` ocorrência(s)
  - linha `7`: `| rtd_analise_robo          |        [v]         |                         | Estrutura principal dos robôs                          |`
  - linha `8`: `| rtd_analise_robo_legs     |        [v]         |                         | Legs (pernas) de cada estrutura                        |`
  - linha `24`: `- `SELECT DISTINCT aba FROM rtd_analise_robo``
  - linha `27`: `- `rtd_analise_robo_legs`, associando `aba`, `timestamp`, detalhes das pernas`
- `docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `2` ocorrência(s)
  - linha `159`: `- `rtd_analise_robo``
  - linha `160`: `- `rtd_analise_robo_legs``
- `docs/executed_v1.md` — `11` ocorrência(s)
  - linha `45`: `Você confirmou que em rtd_analise_robo_legs os campos são:`
  - linha `48`: `Depois você rodou o PRAGMA table_info(rtd_analise_robo_legs) e retornou o schema completo, confirmando:`
  - linha `70`: `*	summary (spot) vindo de rtd_analise_robo com um timestamp`
  - linha `71`: `*	legs vindo de rtd_analise_robo_legs com outro timestamp`
  - linha `91`: `# ANTES (PROBLEMÁTICO)cursor.execute("""    SELECT * FROM rtd_analise_robo_legs     WHERE aba = ?     ORDER BY timestamp DESC, strike     LIMIT 10""", (aba,))`
  - linha `112`: `# Resolve timestamp mais recente se não informado    ts = timestamp    if ts is None:        cursor.execute(            "SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",            (aba,)        )        row = cursor.fetchon`
  - linha `114`: `# Carrega TODAS as legs do mesmo snapshot    cursor.execute(        """SELECT * FROM rtd_analise_robo_legs           WHERE aba = ? AND timestamp = ?           ORDER BY strike""",        (aba, ts)    )    # ... rest`
  - linha `130`: `$ python -c "import sqlite3; c=sqlite3.connect('dados/app.db'); cur=c.cursor(); cur.execute('PRAGMA table_info(rtd_analise_robo_legs)'); print(cur.fetchall()); c.close()"`
- `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `9` ocorrência(s)
  - linha `179`: `rtd_analise_robo_legs`
  - linha `215`: `rtd_analise_robo_legs`
  - linha `217`: `rtd_analise_robo`
  - linha `307`: `rtd_analise_robo`
  - linha `308`: `rtd_analise_robo_legs`
  - linha `460`: `rtd_analise_robo`
  - linha `461`: `rtd_analise_robo_legs`
  - linha `498`: `- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs`
- `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` — `4` ocorrência(s)
  - linha `138`: `rtd_analise_robo_legs`
  - linha `140`: `rtd_analise_robo`
  - linha `277`: `| `rtd_analise_robo_legs` | legado | isolar e substituir progressivamente |`
  - linha `279`: `| `rtd_analise_robo` | legado | isolar e substituir progressivamente |`
- `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md` — `19` ocorrência(s)
  - linha `80`: `bridge_ingest_csv.py:35:    CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),`
  - linha `81`: `bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),`
  - linha `88`: `domain/market_snapshot.py:58:    Agrega o cabeçalho da estrutura (rtd_analise_robo) e suas legs.`
  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `90`: `repositories/market_snapshot_repository.py:50:    FROM rtd_analise_robo_legs`
  - linha `92`: `repositories/market_snapshot_repository.py:98:    FROM rtd_analise_robo`
  - linha `93`: `repositories/robo_legs_repository.py:35:      manual_analise_robo_legs > rtd_analise_robo_legs`
  - linha `95`: `repositories/robo_legs_repository.py:72:            table="rtd_analise_robo_legs",`
- `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md` — `2` ocorrência(s)
  - linha `133`: `rtd_analise_robo`
  - linha `134`: `rtd_analise_robo_legs`
- `docs/FASE_6_CAMADA_CANONICA_LEITURA.md` — `8` ocorrência(s)
  - linha `66`: `- `rtd_analise_robo``
  - linha `67`: `- `rtd_analise_robo_legs``
  - linha `88`: `- `rtd_analise_robo``
  - linha `89`: `- `rtd_analise_robo_legs``
  - linha `101`: `- `manual_analise_robo_legs > rtd_analise_robo_legs``
  - linha `145`: `- `rtd_analise_robo``
  - linha `166`: `- `services/canonical_pricing_facade.py` possui exemplos/documentação citando `rtd_analise_robo`.`
  - linha `256`: `- A regra `manual_analise_robo_legs > rtd_analise_robo_legs` deve ser preservada.`
- `docs/FASE_7_ISOLAMENTO_NOMES_FISICOS_LEGADOS.md` — `1` ocorrência(s)
  - linha `39`: `- Removidas referências textuais/documentais diretas a `rtd_analise_robo`.`
- `docs/fase_8_banco_fonte_verdade_auditoria.md` — `25` ocorrência(s)
  - linha `99`: `- rtd_analise_robo`
  - linha `100`: `- rtd_analise_robo_legs`
  - linha `117`: `- rtd_analise_robo: 5`
  - linha `118`: `- rtd_analise_robo_legs: 20`
  - linha `151`: `- rtd_analise_robo`
  - linha `152`: `- rtd_analise_robo_legs`
  - linha `251`: `- A próxima ação técnica deve mapear como as estruturas existentes em structures se relacionam com rtd_analise_robo_legs e como esse vínculo pode ser migrado ou normalizado sem corromper dados.`
  - linha `259`: `- rtd_analise_robo_legs`
- `docs/MAPA_MODULOS_FUNCOES.md` — `14` ocorrência(s)
  - linha `322`: `## rtd_analise_robo`
  - linha `325`: `- linha 154: `cursor.execute("SELECT aba, pl_realista_total FROM rtd_analise_robo ORDER BY aba")``
  - linha `326`: `- linha 154: `cursor.execute("SELECT aba, pl_realista_total FROM rtd_analise_robo ORDER BY aba")``
  - linha `328`: `- linha 94: `SELECT * FROM rtd_analise_robo``
  - linha `329`: `- linha 94: `SELECT * FROM rtd_analise_robo``
  - linha `330`: `- linha 234: `cursor.execute("SELECT DISTINCT aba FROM rtd_analise_robo ORDER BY aba")``
  - linha `331`: `- linha 234: `cursor.execute("SELECT DISTINCT aba FROM rtd_analise_robo ORDER BY aba")``
  - linha `333`: `- linha 38: `SELECT DISTINCT aba FROM rtd_analise_robo``
- `docs/roteiro_v2.md` — `2` ocorrência(s)
  - linha `6`: `- Estruturas/abas populadas via `rtd_analise_robo`, legs em `rtd_analise_robo_legs``
  - linha `14`: `- `SELECT DISTINCT aba FROM rtd_analise_robo``
- `docs/SQL_SURFACE_MAP_v2.md` — `2` ocorrência(s)
  - linha `5`: `| rtd_analise_robo        | SELECT            | domain/decision.py, domain/payoff.py, scripts/run_derived_pipeline.py |`
  - linha `6`: `| rtd_analise_robo_legs   | SELECT            | domain/payoff.py                                 |`
- `repositories/market_snapshot_repository.py` — `3` ocorrência(s)
  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `50`: `FROM rtd_analise_robo_legs`
  - linha `98`: `FROM rtd_analise_robo`
- `repositories/robo_legs_repository.py` — `4` ocorrência(s)
  - linha `35`: `manual_analise_robo_legs > rtd_analise_robo_legs`
  - linha `72`: `table="rtd_analise_robo_legs",`
  - linha `111`: `SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?`
  - linha `127`: `"SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "`
- `repositories/robo_legs_status_repository.py` — `1` ocorrência(s)
  - linha `57`: `"SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",`

### Termo `manual_analise_robo_legs`

- `ATT/tests/test_legacy_structure_legs_importer_integration.py` — `2` ocorrência(s)
  - linha `50`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `151`: `INSERT INTO manual_analise_robo_legs (`
- `ATT/tests/test_legacy_structure_legs_reader.py` — `1` ocorrência(s)
  - linha `127`: `CREATE TABLE manual_analise_robo_legs (`
- `ATT/tests/test_robo_legs_repository.py` — `6` ocorrência(s)
  - linha `11`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `49`: `INSERT INTO manual_analise_robo_legs`
  - linha `103`: `INSERT INTO manual_analise_robo_legs`
  - linha `123`: `INSERT INTO manual_analise_robo_legs`
  - linha `128`: `INSERT INTO manual_analise_robo_legs`
  - linha `153`: `INSERT INTO manual_analise_robo_legs`
- `ATT/tests/test_robo_legs_status_repository.py` — `4` ocorrência(s)
  - linha `14`: `conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `18`: `"INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `22`: `"INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `47`: `conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")`
- `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `5` ocorrência(s)
  - linha `180`: `manual_analise_robo_legs`
  - linha `216`: `manual_analise_robo_legs`
  - linha `309`: `manual_analise_robo_legs`
  - linha `462`: `manual_analise_robo_legs`
  - linha `498`: `- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs`
- `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` — `2` ocorrência(s)
  - linha `139`: `manual_analise_robo_legs`
  - linha `278`: `| `manual_analise_robo_legs` | legado | isolar e substituir progressivamente |`
- `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md` — `10` ocorrência(s)
  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `91`: `repositories/market_snapshot_repository.py:79:    FROM manual_analise_robo_legs`
  - linha `93`: `repositories/robo_legs_repository.py:35:      manual_analise_robo_legs > rtd_analise_robo_legs`
  - linha `94`: `repositories/robo_legs_repository.py:63:            table="manual_analise_robo_legs",`
  - linha `96`: `repositories/robo_legs_repository.py:87:            FROM manual_analise_robo_legs`
  - linha `97`: `repositories/robo_legs_repository.py:109:                    SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?`
  - linha `99`: `repositories/robo_legs_repository.py:119:                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs "`
  - linha `101`: `repositories/robo_legs_status_repository.py:53:                "SELECT MAX(timestamp) AS ts FROM manual_analise_robo_legs WHERE aba = ?",`
- `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md` — `1` ocorrência(s)
  - linha `158`: `manual_analise_robo_legs`
- `docs/FASE_6_CAMADA_CANONICA_LEITURA.md` — `3` ocorrência(s)
  - linha `90`: `- `manual_analise_robo_legs``
  - linha `101`: `- `manual_analise_robo_legs > rtd_analise_robo_legs``
  - linha `256`: `- A regra `manual_analise_robo_legs > rtd_analise_robo_legs` deve ser preservada.`
- `docs/fase_8_banco_fonte_verdade_auditoria.md` — `5` ocorrência(s)
  - linha `96`: `- manual_analise_robo_legs`
  - linha `114`: `- manual_analise_robo_legs: 0`
  - linha `158`: `- manual_analise_robo_legs`
  - linha `260`: `- manual_analise_robo_legs`
  - linha `280`: `- manual_analise_robo_legs`
- `repositories/market_snapshot_repository.py` — `2` ocorrência(s)
  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `79`: `FROM manual_analise_robo_legs`
- `repositories/robo_legs_repository.py` — `5` ocorrência(s)
  - linha `35`: `manual_analise_robo_legs > rtd_analise_robo_legs`
  - linha `63`: `table="manual_analise_robo_legs",`
  - linha `87`: `FROM manual_analise_robo_legs`
  - linha `109`: `SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?`
  - linha `119`: `"SELECT DISTINCT timestamp FROM manual_analise_robo_legs "`
- `repositories/robo_legs_status_repository.py` — `1` ocorrência(s)
  - linha `53`: `"SELECT MAX(timestamp) AS ts FROM manual_analise_robo_legs WHERE aba = ?",`

### Termo `RTD_LINKS`

- `_repo_audit/rota_mestre_2_fase1/mapear_automacao_opcoes_rtd_backup_20260613_185438.py` — `5` ocorrência(s)
  - linha `55`: `"RTD_LINKS",`
  - linha `146`: `"dados/RTD_LINKS.csv",`
  - linha `327`: `if "dados/RTD_LINKS.csv" in existing_paths:`
  - linha `329`: `"Auditar dados/RTD_LINKS.csv como possível fonte fixa de links RTD antes de criar nova estrutura."`
  - linha `333`: `"Verificar se a lista fixa de links RTD precisa ser criada, pois dados/RTD_LINKS.csv não foi encontrado."`
- `docs/AUDITORIA_ROTA_MESTRE_2.md` — `5` ocorrência(s)
  - linha `174`: `- `dados/RTD_LINKS.csv``
  - linha `230`: `- `dados/RTD_LINKS.csv``
  - linha `273`: `- `dados/RTD_LINKS.csv``
  - linha `317`: `- `dados/RTD_LINKS.csv``
  - linha `327`: `- `dados/RTD_LINKS.csv``
- `docs/fase_2_auditoria_contrato_rtd_excel.md` — `2` ocorrência(s)
  - linha `15`: `- `dados/RTD_LINKS.csv``
  - linha `36`: `1. Qual é o papel de `dados/RTD_LINKS.csv`?`
- `docs/fase_2_diagnostico_csvs_rtd_excel.md` — `1` ocorrência(s)
  - linha `7`: `## `dados/RTD_LINKS.csv``
- `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `1` ocorrência(s)
  - linha `250`: `CSV exportado da aba RTD_LINKS`
- `docs/fase_2_mapa_contrato_rtd_excel.md` — `7` ocorrência(s)
  - linha `19`: `### `dados/RTD_LINKS.csv``
  - linha `151`: `- `dados/RTD_LINKS.csv``
  - linha `221`: `### 1. Qual é o papel de `dados/RTD_LINKS.csv`?`
  - linha `235`: `- `dados/RTD_LINKS.csv`, para atributos RTD/opções`
  - linha `252`: `- `ATIVO` em arquivos de pernas contra `codigo_opcao` em `RTD_LINKS.csv``
  - linha `267`: `- `dados/RTD_LINKS.csv``
  - linha `287`: `1. `dados/RTD_LINKS.csv``
- `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` — `2` ocorrência(s)
  - linha `53`: `CSV exportado da aba RTD_LINKS`
  - linha `333`: `Cotações RTD e exportações da aba RTD_LINKS são entrada bruta.`
- `docs/lista_priorizada_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `28`: `### `dados/RTD_LINKS.csv``
- `docs/mapeamento_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `700`: `### `dados/RTD_LINKS.csv``
- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `10` ocorrência(s)
  - linha `35`: `- Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv`
  - linha `39`: `- Fase 6 — Importador somente-leitura do RTD_LINKS`
  - linha `643`: `dados/RTD_LINKS.csv`
  - linha `936`: `- O arquivo dados/RTD_LINKS.csv é tratado como dado local operacional. O contrato versionado deve ser documentado em docs/, e não depender do versionamento direto do CSV real.`
  - linha `938`: `- RTD_LINKS.csv deve ser auditado inicialmente como catálogo/contrato de conexão RTD, não como fonte definitiva de snapshots de mercado, até que seu schema real confirme essa função.`
  - linha `956`: `Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv`
  - linha `984`: `•	saber exatamente quais campos existem no RTD_LINKS.csv`
  - linha `1047`: `Fase 6 — Importador somente-leitura do RTD_LINKS`
- `docs/validacoes/fase-17-mapa-pastas-arquivos.md` — `1` ocorrência(s)
  - linha `363`: `dados/RTD_LINKS.csv`
- `repositories/rtd_option_quotes_repository.py` — `1` ocorrência(s)
  - linha `14`: `Essa tabela é alimentada pelo CSV exportado da aba RTD_LINKS`
- `scripts/mapear_automacao_opcoes_rtd.py` — `1` ocorrência(s)
  - linha `75`: `"dados/RTD_LINKS.csv": "Prioritário para auditoria do contrato RTD/Excel.",`

### Termo `analise_robo_legs`

- `_repo_audit/rota_mestre_2_fase1/mapear_automacao_opcoes_rtd_backup_20260613_185438.py` — `1` ocorrência(s)
  - linha `72`: `"analise_robo_legs",`
- `ATT/checks/check_end_to_end.py` — `1` ocorrência(s)
  - linha `15`: `ROOT_DIR / "bridge" / "analise_robo_legs.csv",`
- `ATT/checks/check_legs.py` — `1` ocorrência(s)
  - linha `12`: `BRIDGE_DIR / "analise_robo_legs.csv",`
- `ATT/checks/check_structures.py` — `1` ocorrência(s)
  - linha `16`: `ROOT_DIR / "bridge" / "analise_robo_legs.csv",`
- `ATT/tests/test_legacy_structure_legs_importer_integration.py` — `4` ocorrência(s)
  - linha `50`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `65`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `132`: `INSERT INTO rtd_analise_robo_legs (`
  - linha `151`: `INSERT INTO manual_analise_robo_legs (`
- `ATT/tests/test_legacy_structure_legs_reader.py` — `3` ocorrência(s)
  - linha `127`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `142`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `180`: `INSERT INTO rtd_analise_robo_legs`
- `ATT/tests/test_robo_legs_repository.py` — `11` ocorrência(s)
  - linha `11`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `25`: `CREATE TABLE rtd_analise_robo_legs (`
  - linha `49`: `INSERT INTO manual_analise_robo_legs`
  - linha `54`: `INSERT INTO rtd_analise_robo_legs`
  - linha `79`: `INSERT INTO rtd_analise_robo_legs`
  - linha `103`: `INSERT INTO manual_analise_robo_legs`
  - linha `123`: `INSERT INTO manual_analise_robo_legs`
  - linha `128`: `INSERT INTO manual_analise_robo_legs`
- `ATT/tests/test_robo_legs_status_repository.py` — `7` ocorrência(s)
  - linha `14`: `conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `15`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `18`: `"INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `22`: `"INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `26`: `"INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `47`: `conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `48`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
- `bridge_ingest_csv.py` — `1` ocorrência(s)
  - linha `36`: `CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),`
- `docs/AUDITORIA_ROTA_MESTRE_2.md` — `3` ocorrência(s)
  - linha `275`: `- `bridge/analise_robo_legs.csv``
  - linha `320`: `- `bridge/analise_robo_legs.csv``
  - linha `328`: `- `bridge/analise_robo_legs.csv``
- `docs/baseline_v1a.md` — `3` ocorrência(s)
  - linha `51`: `ANALISE_ROBO_LEGS	rtd_analise_robo_legs	replace	[OK]`
  - linha `61`: `-- Exemplo de estrutura atual (criada dinamicamente)CREATE TABLE rtd_analise_robo_legs (    ativo TEXT,    cv TEXT,     quant TEXT,    valor_executado TEXT,    -- ... todas as colunas normalizadas como TEXT);`
  - linha `85`: `Input: ler rtd_analise_robo_legs (em vez de COM/Excel)`
- `docs/baseline_v2.md` — `2` ocorrência(s)
  - linha `8`: `| rtd_analise_robo_legs     |        [v]         |                         | Legs (pernas) de cada estrutura                        |`
  - linha `27`: `- `rtd_analise_robo_legs`, associando `aba`, `timestamp`, detalhes das pernas`
- `docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `1` ocorrência(s)
  - linha `160`: `- `rtd_analise_robo_legs``
- `docs/executed_v1.md` — `8` ocorrência(s)
  - linha `45`: `Você confirmou que em rtd_analise_robo_legs os campos são:`
  - linha `48`: `Depois você rodou o PRAGMA table_info(rtd_analise_robo_legs) e retornou o schema completo, confirmando:`
  - linha `71`: `*	legs vindo de rtd_analise_robo_legs com outro timestamp`
  - linha `91`: `# ANTES (PROBLEMÁTICO)cursor.execute("""    SELECT * FROM rtd_analise_robo_legs     WHERE aba = ?     ORDER BY timestamp DESC, strike     LIMIT 10""", (aba,))`
  - linha `112`: `# Resolve timestamp mais recente se não informado    ts = timestamp    if ts is None:        cursor.execute(            "SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",            (aba,)        )        row = cursor.fetchon`
  - linha `114`: `# Carrega TODAS as legs do mesmo snapshot    cursor.execute(        """SELECT * FROM rtd_analise_robo_legs           WHERE aba = ? AND timestamp = ?           ORDER BY strike""",        (aba, ts)    )    # ... rest`
  - linha `130`: `$ python -c "import sqlite3; c=sqlite3.connect('dados/app.db'); cur=c.cursor(); cur.execute('PRAGMA table_info(rtd_analise_robo_legs)'); print(cur.fetchall()); c.close()"`
  - linha `169`: `3.	Se houver "curva estranha", verificar sincronia timestamp entre rtd_analise_robo e rtd_analise_robo_legs`
- `docs/fase_2_auditoria_contrato_rtd_excel.md` — `1` ocorrência(s)
  - linha `17`: `- `bridge/analise_robo_legs.csv``
- `docs/fase_2_diagnostico_csvs_rtd_excel.md` — `1` ocorrência(s)
  - linha `55`: `## `bridge/analise_robo_legs.csv``
- `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `12` ocorrência(s)
  - linha `179`: `rtd_analise_robo_legs`
  - linha `180`: `manual_analise_robo_legs`
  - linha `215`: `rtd_analise_robo_legs`
  - linha `216`: `manual_analise_robo_legs`
  - linha `308`: `rtd_analise_robo_legs`
  - linha `309`: `manual_analise_robo_legs`
  - linha `461`: `rtd_analise_robo_legs`
  - linha `462`: `manual_analise_robo_legs`
- `docs/fase_2_mapa_contrato_rtd_excel.md` — `7` ocorrência(s)
  - linha `47`: `### `bridge/analise_robo_legs.csv``
  - linha `156`: `- `bridge/analise_robo_legs.csv``
  - linha `160`: `### 2. `bridge/analise_robo_legs.csv` é o contrato operacional mais rico`
  - linha `188`: `O arquivo possui volume maior e cabeçalho mais reduzido que `analise_robo_legs.csv`.`
  - linha `236`: `- `bridge/analise_robo_legs.csv`, para pernas operacionais`
  - linha `268`: `- `bridge/analise_robo_legs.csv``
  - linha `288`: `2. `bridge/analise_robo_legs.csv``
- `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` — `6` ocorrência(s)
  - linha `138`: `rtd_analise_robo_legs`
  - linha `139`: `manual_analise_robo_legs`
  - linha `142`: `bridge/analise_robo_legs.csv`
  - linha `277`: `| `rtd_analise_robo_legs` | legado | isolar e substituir progressivamente |`
  - linha `278`: `| `manual_analise_robo_legs` | legado | isolar e substituir progressivamente |`
  - linha `282`: `| `bridge/analise_robo_legs.csv` | legado | manter apenas enquanto houver consumidor |`
- `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md` — `25` ocorrência(s)
  - linha `69`: `ATT/checks/check_end_to_end.py:15:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",`
  - linha `72`: `ATT/checks/check_legs.py:12:    BRIDGE_DIR / "analise_robo_legs.csv",`
  - linha `76`: `ATT/checks/check_structures.py:16:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",`
  - linha `81`: `bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),`
  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `90`: `repositories/market_snapshot_repository.py:50:    FROM rtd_analise_robo_legs`
  - linha `91`: `repositories/market_snapshot_repository.py:79:    FROM manual_analise_robo_legs`
  - linha `93`: `repositories/robo_legs_repository.py:35:      manual_analise_robo_legs > rtd_analise_robo_legs`
- `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md` — `3` ocorrência(s)
  - linha `111`: `analise_robo_legs.csv`
  - linha `134`: `rtd_analise_robo_legs`
  - linha `158`: `manual_analise_robo_legs`
- `docs/FASE_6_CAMADA_CANONICA_LEITURA.md` — `5` ocorrência(s)
  - linha `67`: `- `rtd_analise_robo_legs``
  - linha `89`: `- `rtd_analise_robo_legs``
  - linha `90`: `- `manual_analise_robo_legs``
  - linha `101`: `- `manual_analise_robo_legs > rtd_analise_robo_legs``
  - linha `256`: `- A regra `manual_analise_robo_legs > rtd_analise_robo_legs` deve ser preservada.`
- `docs/fase_8_banco_fonte_verdade_auditoria.md` — `26` ocorrência(s)
  - linha `96`: `- manual_analise_robo_legs`
  - linha `100`: `- rtd_analise_robo_legs`
  - linha `114`: `- manual_analise_robo_legs: 0`
  - linha `118`: `- rtd_analise_robo_legs: 20`
  - linha `152`: `- rtd_analise_robo_legs`
  - linha `158`: `- manual_analise_robo_legs`
  - linha `251`: `- A próxima ação técnica deve mapear como as estruturas existentes em structures se relacionam com rtd_analise_robo_legs e como esse vínculo pode ser migrado ou normalizado sem corromper dados.`
  - linha `259`: `- rtd_analise_robo_legs`
- `docs/lista_priorizada_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `147`: `- `bridge/analise_robo_legs.csv` — `bridge` — score `11``
- `docs/MAPA_MODULOS_FUNCOES.md` — `5` ocorrência(s)
  - linha `338`: `## rtd_analise_robo_legs`
  - linha `341`: `- linha 60: `"SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",``
  - linha `342`: `- linha 60: `"SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",``
  - linha `343`: `- linha 72: `SELECT * FROM rtd_analise_robo_legs``
  - linha `344`: `- linha 72: `SELECT * FROM rtd_analise_robo_legs``
- `docs/mapeamento_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `1239`: `- `bridge/analise_robo_legs.csv` — `bridge` — score `11``
- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `2` ocorrência(s)
  - linha `214`: `•	analise_robo_legs.csv`
  - linha `619`: `bridge/analise_robo_legs.csv`
- `docs/roteiro_v2.md` — `1` ocorrência(s)
  - linha `6`: `- Estruturas/abas populadas via `rtd_analise_robo`, legs em `rtd_analise_robo_legs``
- `docs/SQL_SURFACE_MAP_v2.md` — `1` ocorrência(s)
  - linha `6`: `| rtd_analise_robo_legs   | SELECT            | domain/payoff.py                                 |`
- `docs/validacoes/fase-17-mapa-pastas-arquivos.md` — `1` ocorrência(s)
  - linha `159`: `| `bridge/analise_robo_legs.csv` | Sim | Versionado |`
- `repositories/market_snapshot_repository.py` — `3` ocorrência(s)
  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
  - linha `50`: `FROM rtd_analise_robo_legs`
  - linha `79`: `FROM manual_analise_robo_legs`
- `repositories/robo_legs_repository.py` — `8` ocorrência(s)
  - linha `35`: `manual_analise_robo_legs > rtd_analise_robo_legs`
  - linha `63`: `table="manual_analise_robo_legs",`
  - linha `72`: `table="rtd_analise_robo_legs",`
  - linha `87`: `FROM manual_analise_robo_legs`
  - linha `109`: `SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?`
  - linha `111`: `SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?`
  - linha `119`: `"SELECT DISTINCT timestamp FROM manual_analise_robo_legs "`
  - linha `127`: `"SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "`
- `repositories/robo_legs_status_repository.py` — `2` ocorrência(s)
  - linha `53`: `"SELECT MAX(timestamp) AS ts FROM manual_analise_robo_legs WHERE aba = ?",`
  - linha `57`: `"SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",`
- `services/legacy_structure_legs_reader.py` — `1` ocorrência(s)
  - linha `21`: `structures.alias_legacy_aba -> *_analise_robo_legs.aba`

### Termo `analise_robo.csv`

- `ATT/checks/check_end_to_end.py` — `1` ocorrência(s)
  - linha `16`: `ROOT_DIR / "bridge" / "analise_robo.csv",`
- `ATT/checks/check_legs.py` — `1` ocorrência(s)
  - linha `13`: `BRIDGE_DIR / "analise_robo.csv",`
- `ATT/checks/check_structures.py` — `1` ocorrência(s)
  - linha `15`: `ROOT_DIR / "bridge" / "analise_robo.csv",`
- `bridge_ingest_csv.py` — `1` ocorrência(s)
  - linha `35`: `CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),`
- `docs/AUDITORIA_ROTA_MESTRE_2.md` — `3` ocorrência(s)
  - linha `274`: `- `bridge/analise_robo.csv``
  - linha `321`: `- `bridge/analise_robo.csv``
  - linha `329`: `- `bridge/analise_robo.csv``
- `docs/fase_2_auditoria_contrato_rtd_excel.md` — `1` ocorrência(s)
  - linha `16`: `- `bridge/analise_robo.csv``
- `docs/fase_2_diagnostico_csvs_rtd_excel.md` — `1` ocorrência(s)
  - linha `31`: `## `bridge/analise_robo.csv``
- `docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` — `2` ocorrência(s)
  - linha `473`: `bridge/analise_robo.csv`
  - linha `513`: `- bridge/analise_robo.csv, bridge/analise_robo_legs.csv e bridge/analise_raiox.csv ainda aparecem em checks`
- `docs/fase_2_mapa_contrato_rtd_excel.md` — `6` ocorrência(s)
  - linha `33`: `### `bridge/analise_robo.csv``
  - linha `155`: `- `bridge/analise_robo.csv``
  - linha `180`: `### 3. `bridge/analise_robo.csv` é agregado por estrutura/aba`
  - linha `243`: `- `bridge/analise_robo.csv``
  - linha `269`: `- `bridge/analise_robo.csv``
  - linha `289`: `3. `bridge/analise_robo.csv``
- `docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` — `2` ocorrência(s)
  - linha `141`: `bridge/analise_robo.csv`
  - linha `281`: `| `bridge/analise_robo.csv` | legado | manter apenas enquanto houver consumidor |`
- `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md` — `7` ocorrência(s)
  - linha `70`: `ATT/checks/check_end_to_end.py:16:    ROOT_DIR / "bridge" / "analise_robo.csv",`
  - linha `73`: `ATT/checks/check_legs.py:13:    BRIDGE_DIR / "analise_robo.csv",`
  - linha `75`: `ATT/checks/check_structures.py:15:    ROOT_DIR / "bridge" / "analise_robo.csv",`
  - linha `80`: `bridge_ingest_csv.py:35:    CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),`
  - linha `114`: `ATT/checks/check_legs.py:13:    BRIDGE_DIR / "analise_robo.csv",`
  - linha `231`: `analise_robo.csv`
  - linha `371`: `analise_robo.csv`
- `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md` — `1` ocorrência(s)
  - linha `110`: `analise_robo.csv`
- `docs/lista_priorizada_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `149`: `- `bridge/analise_robo.csv` — `bridge` — score `9``
- `docs/mapeamento_automacao_opcoes_rtd.md` — `1` ocorrência(s)
  - linha `1245`: `- `bridge/analise_robo.csv` — `bridge` — score `9``
- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `2` ocorrência(s)
  - linha `213`: `•	analise_robo.csv`
  - linha `618`: `bridge/analise_robo.csv`
- `docs/validacoes/fase-17-mapa-pastas-arquivos.md` — `1` ocorrência(s)
  - linha `158`: `| `bridge/analise_robo.csv` | Sim | Versionado |`

### Termo `INSERT INTO`

- `ATT/tests/test_legacy_structure_legs_importer.py` — `2` ocorrência(s)
  - linha `56`: `INSERT INTO structures (`
  - linha `73`: `INSERT INTO structure_legs (`
- `ATT/tests/test_legacy_structure_legs_importer_integration.py` — `4` ocorrência(s)
  - linha `90`: `INSERT INTO structures (`
  - linha `110`: `INSERT INTO structure_legs (`
  - linha `132`: `INSERT INTO rtd_analise_robo_legs (`
  - linha `151`: `INSERT INTO manual_analise_robo_legs (`
- `ATT/tests/test_legacy_structure_legs_reader.py` — `3` ocorrência(s)
  - linha `174`: `INSERT INTO structures`
  - linha `180`: `INSERT INTO rtd_analise_robo_legs`
  - linha `237`: `INSERT INTO structures`
- `ATT/tests/test_robo_legs_repository.py` — `9` ocorrência(s)
  - linha `49`: `INSERT INTO manual_analise_robo_legs`
  - linha `54`: `INSERT INTO rtd_analise_robo_legs`
  - linha `79`: `INSERT INTO rtd_analise_robo_legs`
  - linha `103`: `INSERT INTO manual_analise_robo_legs`
  - linha `123`: `INSERT INTO manual_analise_robo_legs`
  - linha `128`: `INSERT INTO manual_analise_robo_legs`
  - linha `133`: `INSERT INTO rtd_analise_robo_legs`
  - linha `153`: `INSERT INTO manual_analise_robo_legs`
- `ATT/tests/test_robo_legs_status_repository.py` — `3` ocorrência(s)
  - linha `18`: `"INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `22`: `"INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
  - linha `26`: `"INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",`
- `ATT/tests/test_system_snapshots_repository.py` — `2` ocorrência(s)
  - linha `15`: `INSERT INTO structures (`
  - linha `49`: `INSERT INTO structure_legs (`
- `db/derived_repo.py` — `4` ocorrência(s)
  - linha `359`: `INSERT INTO payoff_curve_points`
  - linha `453`: `INSERT INTO payoff_curve_points`
  - linha `695`: `INSERT INTO payoff_curve_points`
  - linha `732`: `INSERT INTO structure_decisions`
- `db/writer.py` — `1` ocorrência(s)
  - linha `72`: `INSERT INTO payoff_curve_points`
- `docs/decisions/structure_ref_created_at.md` — `2` ocorrência(s)
  - linha `47`: `INSERT INTO structure_decisions`
  - linha `53`: `INSERT INTO structure_decisions`
- `docs/MAPA_MODULOS_FUNCOES.md` — `8` ocorrência(s)
  - linha `267`: `- linha 71: `INSERT INTO payoff_curve_points``
  - linha `268`: `- linha 71: `INSERT INTO payoff_curve_points``
  - linha `293`: `- linha 175: `INSERT INTO payoff_curve_summary (``
  - linha `294`: `- linha 175: `INSERT INTO payoff_curve_summary (``
  - linha `351`: `- linha 214: `INSERT INTO rtd_consolidacoes (``
  - linha `352`: `- linha 214: `INSERT INTO rtd_consolidacoes (``
  - linha `413`: `- linha 113: `INSERT INTO structure_decisions``
  - linha `414`: `- linha 113: `INSERT INTO structure_decisions``
- `domain/payoff_features.py` — `1` ocorrência(s)
  - linha `146`: `INSERT INTO payoff_curve_summary (`
- `repositories/pricing_executions_repository.py` — `1` ocorrência(s)
  - linha `58`: `INSERT INTO pricing_executions (`
- `repositories/structure_events_repository.py` — `1` ocorrência(s)
  - linha `322`: `INSERT INTO structure_events (`
- `repositories/structures_repository.py` — `6` ocorrência(s)
  - linha `281`: `INSERT INTO structure_audit_log`
  - linha `312`: `INSERT INTO structures (`
  - linha `366`: `INSERT INTO structures (`
  - linha `399`: `INSERT INTO structure_legs (`
  - linha `594`: `INSERT INTO structure_legs (`
  - linha `648`: `INSERT INTO structure_legs (`
- `repositories/system_snapshots_repository.py` — `2` ocorrência(s)
  - linha `113`: `INSERT INTO structure_snapshots (`
  - linha `171`: `INSERT INTO structure_leg_snapshots (`
- `scripts/apply_fase9_atomic_create.py` — `2` ocorrência(s)
  - linha `83`: `INSERT INTO structures (`
  - linha `116`: `INSERT INTO structure_legs (`

### Termo `UPDATE `

- `api/structures_controller.py` — `1` ocorrência(s)
  - linha `233`: `"UPDATE structures SET updated_at=? WHERE id=?",`
- `db/migrations/add_structure_id_to_payoff_curve_points.py` — `2` ocorrência(s)
  - linha `30`: `UPDATE payoff_curve_points`
  - linha `55`: `UPDATE payoff_curve_summary`
- `docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md` — `1` ocorrência(s)
  - linha `344`: `Mapear todos os SELECT/INSERT/UPDATE envolvendo rtd_*, manual_* e tabelas legadas do Excel.`
- `docs/SQL_SURFACE_MAP_v2.md` — `2` ocorrência(s)
  - linha `9`: `|                         | INSERT/UPDATE     | db/writer.py, db/derived_repo.py                 |`
  - linha `12`: `|                         | INSERT/UPDATE     | db/writer.py, db/derived_repo.py                 |`
- `domain/payoff_features.py` — `1` ocorrência(s)
  - linha `163`: `ON CONFLICT(structure_id, reference_date) DO UPDATE SET`
- `repositories/structure_events_repository.py` — `1` ocorrência(s)
  - linha `386`: `UPDATE structure_events`
- `repositories/structures_repository.py` — `4` ocorrência(s)
  - linha `516`: `UPDATE structures`
  - linha `560`: `"UPDATE structures SET status=?, updated_at=? WHERE id=?",`
  - linha `610`: `"UPDATE structures SET updated_at=? WHERE id=?",`
  - linha `663`: `"UPDATE structures SET updated_at=? WHERE id=?",`
- `scripts/repair_derived_db_consistency.py` — `1` ocorrência(s)
  - linha `199`: `UPDATE structure_decisions`

### Termo `DELETE FROM`

- `api/structures_controller.py` — `1` ocorrência(s)
  - linha `229`: `"DELETE FROM structure_legs WHERE id=?",`
- `bridge_ingest_csv.py` — `1` ocorrência(s)
  - linha `154`: `conn.execute(f'DELETE FROM "{table}"')`
- `db/derived_repo.py` — `10` ocorrência(s)
  - linha `298`: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
  - linha `354`: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
  - linha `448`: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
  - linha `474`: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
  - linha `611`: `f"DELETE FROM payoff_curve_points "`
  - linha `623`: `f"DELETE FROM structure_decisions "`
  - linha `691`: `"DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",`
  - linha `726`: `"DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",`
- `docs/MAPA_MODULOS_FUNCOES.md` — `4` ocorrência(s)
  - linha `253`: `- linha 211: `DELETE FROM payoff_curve_points``
  - linha `254`: `- linha 211: `DELETE FROM payoff_curve_points``
  - linha `405`: `- linha 223: `DELETE FROM structure_decisions``
  - linha `406`: `- linha 223: `DELETE FROM structure_decisions``
- `repositories/structures_repository.py` — `1` ocorrência(s)
  - linha `641`: `"DELETE FROM structure_legs WHERE structure_id=?",`
- `scripts/purge_derived_snapshots.py` — `2` ocorrência(s)
  - linha `108`: `cur = con.execute(f"DELETE FROM {table}")`
  - linha `118`: `f"DELETE FROM {table} WHERE timestamp < ?",`
- `scripts/repair_derived_db_consistency.py` — `2` ocorrência(s)
  - linha `244`: `f"DELETE FROM structure_decisions WHERE id IN ({placeholders})",`
  - linha `275`: `DELETE FROM payoff_curve_points`

### Termo `CREATE TABLE`

- `ATT/tests/test_legacy_structure_legs_importer.py` — `2` ocorrência(s)
  - linha `14`: `CREATE TABLE structures (`
  - linha `27`: `CREATE TABLE structure_legs (`
- `ATT/tests/test_legacy_structure_legs_importer_integration.py` — `4` ocorrência(s)
  - linha `17`: `CREATE TABLE structures (`
  - linha `30`: `CREATE TABLE structure_legs (`
  - linha `50`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `65`: `CREATE TABLE rtd_analise_robo_legs (`
- `ATT/tests/test_legacy_structure_legs_reader.py` — `3` ocorrência(s)
  - linha `117`: `CREATE TABLE structures (`
  - linha `127`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `142`: `CREATE TABLE rtd_analise_robo_legs (`
- `ATT/tests/test_pricing_executions_repository.py` — `1` ocorrência(s)
  - linha `14`: `CREATE TABLE pricing_executions (`
- `ATT/tests/test_robo_legs_repository.py` — `2` ocorrência(s)
  - linha `11`: `CREATE TABLE manual_analise_robo_legs (`
  - linha `25`: `CREATE TABLE rtd_analise_robo_legs (`
- `ATT/tests/test_robo_legs_status_repository.py` — `4` ocorrência(s)
  - linha `14`: `conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `15`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `47`: `conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")`
  - linha `48`: `conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")`
- `ATT/tests/test_structures_archive_wiring.py` — `4` ocorrência(s)
  - linha `536`: `"CREATE TABLE IF NOT EXISTS structures "`
  - linha `542`: `"CREATE TABLE IF NOT EXISTS structure_legs "`
  - linha `573`: `"CREATE TABLE IF NOT EXISTS structures "`
  - linha `579`: `"CREATE TABLE IF NOT EXISTS structure_legs "`
- `bridge_ingest_csv.py` — `2` ocorrência(s)
  - linha `145`: `conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({cols_sql})')`
  - linha `176`: `f'CREATE TABLE IF NOT EXISTS "{table}" '`
- `create_payoff_summary_table.py` — `1` ocorrência(s)
  - linha `4`: `CREATE TABLE IF NOT EXISTS payoff_curve_summary (`
- `db/derived_repo.py` — `2` ocorrência(s)
  - linha `77`: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
  - linha `101`: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- `db/schema.py` — `4` ocorrência(s)
  - linha `7`: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
  - linha `25`: `CREATE TABLE IF NOT EXISTS structure_decisions (`
  - linha `56`: `CREATE TABLE IF NOT EXISTS payoff_points (`
  - linha `71`: `CREATE TABLE IF NOT EXISTS structure_events (`
- `db/schema_excel.py` — `5` ocorrência(s)
  - linha `5`: `CREATE TABLE IF NOT EXISTS robo_config (`
  - linha `17`: `CREATE TABLE IF NOT EXISTS robo_snapshot (`
  - linha `38`: `CREATE TABLE IF NOT EXISTS robo_legs_snapshot (`
  - linha `68`: `CREATE TABLE IF NOT EXISTS robo_legs_history (`
  - linha `90`: `CREATE TABLE IF NOT EXISTS encerramentos_manuais (`
- `docs/baseline_v1a.md` — `3` ocorrência(s)
  - linha `61`: `-- Exemplo de estrutura atual (criada dinamicamente)CREATE TABLE rtd_analise_robo_legs (    ativo TEXT,    cv TEXT,     quant TEXT,    valor_executado TEXT,    -- ... todas as colunas normalizadas como TEXT);`
  - linha `64`: `-- Ajustado para compatibilidade com ingestor atualCREATE TABLE payoff_curve_points (    id INTEGER PRIMARY KEY AUTOINCREMENT,    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    s_t REAL NOT NULL,    pl_venc REAL NOT NULL,    spot_ref REA`
  - linha `65`: `CREATE TABLE structure_decisions (    id INTEGER PRIMARY KEY AUTOINCREMENT,    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    decision TEXT NOT NULL,    level INTEGER NOT NULL,    pl_atual REAL,    pl_max REAL,    pl_pct_of_max REAL,    `
- `docs/executed_v1.md` — `1` ocorrência(s)
  - linha `82`: `### Análise do Schema```sql-- Tabela alvo: payoff_curve_pointsCREATE TABLE payoff_curve_points (    timestamp TEXT NOT NULL,    aba TEXT NOT NULL,    spot_ref REAL,    point_spot REAL NOT NULL,    -- coordenada X    point_pl REAL NOT NULL, `
- `docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md` — `1` ocorrência(s)
  - linha `86`: `db/schema_excel.py:90:CREATE TABLE IF NOT EXISTS encerramentos_manuais (`
- `docs/MAPA_MODULOS_FUNCOES.md` — `24` ocorrência(s)
  - linha `8`: `- linha 101: `conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({cols_sql})')``
  - linha `9`: `- linha 101: `conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({cols_sql})')``
  - linha `11`: `- linha 4: `CREATE TABLE IF NOT EXISTS payoff_curve_summary (``
  - linha `12`: `- linha 4: `CREATE TABLE IF NOT EXISTS payoff_curve_summary (``
  - linha `14`: `- linha 19: `CREATE TABLE IF NOT EXISTS payoff_curve_points (``
  - linha `15`: `- linha 19: `CREATE TABLE IF NOT EXISTS payoff_curve_points (``
  - linha `16`: `- linha 42: `CREATE TABLE IF NOT EXISTS structure_decisions (``
  - linha `17`: `- linha 42: `CREATE TABLE IF NOT EXISTS structure_decisions (``
- `docs/SQL_SURFACE_MAP_v2.md` — `1` ocorrência(s)
  - linha `21`: `- Operações base: CREATE TABLE, SELECT, INSERT, UPDATE, DELETE.`
- `infra/bootstrap_structures_schema.py` — `7` ocorrência(s)
  - linha `33`: `CREATE TABLE IF NOT EXISTS structures (`
  - linha `51`: `CREATE TABLE IF NOT EXISTS structure_legs (`
  - linha `76`: `CREATE TABLE IF NOT EXISTS pricing_executions (`
  - linha `106`: `CREATE TABLE IF NOT EXISTS structure_audit_log (`
  - linha `127`: `CREATE TABLE IF NOT EXISTS structure_snapshots (`
  - linha `154`: `CREATE TABLE IF NOT EXISTS structure_leg_snapshots (`
  - linha `319`: `CREATE TABLE IF NOT EXISTS pricing_executions (`
- `repositories/structure_events_repository.py` — `1` ocorrência(s)
  - linha `199`: `CREATE TABLE IF NOT EXISTS structure_events (`
- `repositories/structures_repository.py` — `2` ocorrência(s)
  - linha `226`: `Idempotente (CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS).`
  - linha `232`: `CREATE TABLE IF NOT EXISTS structure_audit_log (`

### Termo `to_sql`

- `bridge_ingest_csv.py` — `1` ocorrência(s)
  - linha `156`: `df.to_sql(table, conn, if_exists="append", index=False)`
- `db/import_excel.py` — `1` ocorrência(s)
  - linha `83`: `df.to_sql(table, conn, if_exists="append", index=False)`

### Termo `executemany`

- `bridge_ingest_csv.py` — `1` ocorrência(s)
  - linha `190`: `conn.executemany(sql, df[cols].values.tolist())`
- `db/writer.py` — `1` ocorrência(s)
  - linha `71`: `cursor.executemany("""`

## Achados preliminares

1. `repositories/rtd_option_quotes_repository.py` é um repositório de leitura da tabela `rtd_option_quotes`.
2. `repositories/market_snapshot_repository.py` lê snapshots RTD e manuais a partir de tabelas normalizadas.
3. `services/market_snapshot_selector.py` aplica precedência `manual > rtd` por ativo.
4. `services/market_snapshot_provider.py` usa valores estáticos por ativo e não acessa RTD ou banco.
5. Os arquivos inicialmente auditados não demonstram, por si só, o ponto de persistência/importação das cotações RTD.

## Próxima pergunta da Fase 3

Identificar qual rotina cria, importa, atualiza ou sincroniza as tabelas RTD a partir de CSV/Excel/bridge.

Tabelas de interesse:

- `rtd_option_quotes`
- `rtd_analise_robo_legs`
- `rtd_analise_robo`
- `manual_analise_robo_legs`

Nenhuma alteração funcional foi autorizada por este documento.