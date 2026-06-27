# Conferencia de seguimento - Payoff RTD

Gerado em: 2026-06-26 21:17:22

## Objetivo

Registrar evidencia de fechamento das tres primeiras pendencias da frente de payoff RTD e orientar o seguimento ate o fechamento final.

Esta conferencia nao altera codigo funcional. Apenas consulta banco, provider, grep e estado Git.

## Declaracao operacional

As tres primeiras pendencias foram informadas como fechadas pelo responsavel da frente.

Esta evidencia documenta as conferencias para reduzir retrabalho e manter rastreabilidade.

## Ambiente

Diretorio: C:\Users\eucal\projeto
MYHUBIA_DB_PATH: <vazio>
dados/app.db existe: True
dados/app.db tamanho bytes: 839680
dados/derived.db existe: True
dados/derived.db tamanho bytes: 3231744

## Conferencia 1 - Fonte RTD de ativos-base

Tabela rtd_underlying_quotes em dados/app.db: OK
Colunas encontradas:
- id
- ativo
- ultimo_preco
- bid
- ask
- close_price
- prev_close
- open_price
- high_price
- low_price
- volume
- change_percent
- source
- updated_at
- created_at

Ativo: BOVA11
Preco: 170.55
Source: btg_rtd_excel_underlying
Updated_at: 2026-06-26 20:54:49

Ativo: PRIO3
Preco: 53.2
Source: btg_rtd_excel_underlying
Updated_at: 2026-06-26 20:54:49

Resultado conferencia 1 banco RTD: OK

## Conferencia 2 - MarketSnapshotProvider

### Snapshot BOVA11

- interest_rate: 0.1175
- is_current_market: True
- is_static_fallback: False
- market_snapshot_rtd_source: btg_rtd_excel_underlying
- market_snapshot_source: rtd_underlying_quotes
- market_snapshot_updated_at: 2026-06-26 20:54:49
- reference_date: 2026-06-26
- snapshot_source: rtd_underlying_quotes
- snapshot_warning: None
- spot_price: 170.55
- underlying_asset: BOVA11
- volatility: 0.22

### Snapshot PRIO3

- interest_rate: 0.1175
- is_current_market: True
- is_static_fallback: False
- market_snapshot_rtd_source: btg_rtd_excel_underlying
- market_snapshot_source: rtd_underlying_quotes
- market_snapshot_updated_at: 2026-06-26 20:54:49
- reference_date: 2026-06-26
- snapshot_source: rtd_underlying_quotes
- snapshot_warning: None
- spot_price: 53.2
- underlying_asset: PRIO3
- volatility: 0.35

Resultado conferencia 2 provider RTD: OK

## Conferencia 3 - Qualidade RTD das opcoes

Tabela rtd_option_quotes em dados/app.db: OK
Colunas principais detectadas:
- codigo: codigo_opcao
- call_put: call_put
- ultimo_preco: ultimo_preco
- bid: bid
- ask: ask
- source: source
- updated_at: updated_at

Opcao: BOVAG34
  call_put: CALL
  ultimo_preco: 14.64
  bid: 9.75
  ask: 0.0
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19
Opcao: BOVAH186
  call_put: CALL
  ultimo_preco: 1.12
  bid: 0.5
  ask: 1.42
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19
Opcao: BOVAS61
  call_put: PUT
  ultimo_preco: 12.32
  bid: 11.9
  ask: 0.0
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19
Opcao: BOVAT158
  call_put: PUT
  ultimo_preco: 0.63
  bid: 0.59
  ask: 2.03
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19
Opcao: PRIOG800
  call_put: CALL
  ultimo_preco: 0.02
  bid: 0.0
  ask: 0.0
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19
Opcao: PRIOH505
  call_put: CALL
  ultimo_preco: 4.97
  bid: 0.0
  ask: 0.0
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19
Opcao: PRIOS525
  call_put: PUT
  ultimo_preco: 1.05
  bid: 0.05
  ask: 1.99
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19
Opcao: PRIOT700
  call_put: PUT
  ultimo_preco: 12.03
  bid: 0.0
  ask: 0.0
  source: BTG_RTD_EXCEL
  updated_at: 2026-06-26 21:10:19

Quantidade esperada de opcoes ativas: 8
Quantidade encontrada: 8
Escopo de opcoes ativo completo: OK
call_put normalizado: OK
Regra de preco para ultimo_preco zero conferida: OK

Resultado conferencia 3 qualidade opcoes: OK

## Conferencia 4 - Busca por referencias residuais

Busca executada em caminhos de codigo e scripts:
- services
- domain
- repositories
- scripts
- db
- api
- UI
- src
- core
- infra

Padrao:
66[,.]84|DEFAULT_MARKET_BY_ASSET|static_fallback|rtd_underlying_quotes|market_snapshot_source|is_static_fallback

Ocorrencias encontradas:
- domain/payoff.py:129:        market.get("market_snapshot_source")
- domain/payoff.py:131:        or meta.get("market_snapshot_source")
- domain/payoff.py:133:        or input_meta.get("market_snapshot_source")
- domain/payoff.py:141:            market.get("is_static_fallback"),
- domain/payoff.py:142:            market.get("market_is_static_fallback"),
- domain/payoff.py:143:            meta.get("is_static_fallback"),
- domain/payoff.py:144:            meta.get("market_is_static_fallback"),
- domain/payoff.py:145:            input_meta.get("is_static_fallback"),
- domain/payoff.py:146:            input_meta.get("market_is_static_fallback"),
- domain/payoff.py:150:    return explicit_static_flag or source == "static_fallback"
- domain/payoff.py:172:                    "market.spot_price veio de static_fallback; informe snapshot real/atual"
- domain/payoff.py:174:                "market_snapshot_source": (
- domain/payoff.py:175:                    market.get("market_snapshot_source")
- domain/payoff.py:178:                "is_static_fallback": True,
- scripts/conferir_seguimento_payoff_rtd.sh:192:        exists = table_exists(con, "rtd_underlying_quotes")
- scripts/conferir_seguimento_payoff_rtd.sh:193:        add(f"Tabela rtd_underlying_quotes em dados/app.db: {md_bool(exists)}")
- scripts/conferir_seguimento_payoff_rtd.sh:195:            cols = table_cols(con, "rtd_underlying_quotes")
- scripts/conferir_seguimento_payoff_rtd.sh:206:                    f"SELECT * FROM rtd_underlying_quotes WHERE {qident(ativo_col)} IN ('BOVA11', 'PRIO3') ORDER BY {qident(ativo_col)}"
- scripts/conferir_seguimento_payoff_rtd.sh:223:        add(f"ERRO ao consultar rtd_underlying_quotes: {exc}")
- scripts/conferir_seguimento_payoff_rtd.sh:259:        market_source = get_field(data, "market_snapshot_source")
- scripts/conferir_seguimento_payoff_rtd.sh:260:        static_fallback = get_field(data, "is_static_fallback")
- scripts/conferir_seguimento_payoff_rtd.sh:263:            source == "rtd_underlying_quotes"
- scripts/conferir_seguimento_payoff_rtd.sh:264:            or market_source == "rtd_underlying_quotes"
- scripts/conferir_seguimento_payoff_rtd.sh:266:        checks.append(static_fallback is False or str(static_fallback).lower() == "false")
- scripts/conferir_seguimento_payoff_rtd.sh:410:grep_pattern = "66[,.]84|DEFAULT_MARKET_BY_ASSET|static_fallback|rtd_underlying_quotes|market_snapshot_source|is_static_fallback"
- scripts/conferir_seguimento_payoff_rtd.sh:433:# Scan DB 66.84
- scripts/conferir_seguimento_payoff_rtd.sh:434:add("## Conferencia 5 - Busca de valor 66.84 nos bancos")
- scripts/conferir_seguimento_payoff_rtd.sh:438:db_findings.extend(scan_db_for_token(APP_DB, ["66.84", "66,84"]))
- scripts/conferir_seguimento_payoff_rtd.sh:439:db_findings.extend(scan_db_for_token(DERIVED_DB, ["66.84", "66,84"]))
- scripts/conferir_seguimento_payoff_rtd.sh:446:    add("Nenhuma ocorrencia de 66.84 ou 66,84 encontrada em dados/app.db ou dados/derived.db.")
- scripts/conferir_seguimento_payoff_rtd.sh:456:    ROOT / "docs" / "checklists" / "rtd_underlying_quotes.md",
- scripts/conferir_seguimento_payoff_rtd.sh:471:add(f"| MarketSnapshotProvider lendo rtd_underlying_quotes | {'Fechada conferida' if provider_ok else 'Requer atencao'} | Conferencias 1 e 2 |")
- scripts/conferir_seguimento_payoff_rtd.sh:472:add(f"| Payoff BOVA11 sem preco atual indevido 66.84 | {'Fechada conferida' if not db_findings else 'Requer atencao'} | Conferencia 5 e grep |")
- scripts/conferir_seguimento_payoff_rtd.sh:495:add("- Nenhum calculo de PL atual deve usar static_fallback como preco de mercado.")
- scripts/conferir_seguimento_payoff_rtd.sh:496:add("- O spot atual deve ter origem auditavel em rtd_underlying_quotes.")
- scripts/conferir_seguimento_payoff_rtd.sh:530:print("Conferencia 5 66.84 nos bancos:", "OK" if not db_findings else "ATENCAO")
- scripts/gerar_docs_rtd.sh:57:checklist_path = docs / "checklists" / "rtd_underlying_quotes.md"
- scripts/gerar_docs_rtd.sh:65:A validacao em runtime confirmou que o servico MarketSnapshotProvider consome corretamente os precos vindos da tabela rtd_underlying_quotes no banco dados/app.db.
- scripts/gerar_docs_rtd.sh:78:    scripts/import_rtd_underlying_quotes_csv.py
- scripts/gerar_docs_rtd.sh:84:    rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:103:    rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:105:A tabela rtd_underlying_quotes nao deve ser criada em dados/derived.db.
- scripts/gerar_docs_rtd.sh:117:Portanto, rtd_underlying_quotes pertence ao banco operacional dados/app.db.
- scripts/gerar_docs_rtd.sh:158:    snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:159:    market_snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:160:    is_static_fallback: False
- scripts/gerar_docs_rtd.sh:171:    snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:172:    market_snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:173:    is_static_fallback: False
- scripts/gerar_docs_rtd.sh:183:    snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:184:    market_snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:185:    is_static_fallback: False
- scripts/gerar_docs_rtd.sh:194:    is_static_fallback: True
- scripts/gerar_docs_rtd.sh:198:    is_static_fallback: False
- scripts/gerar_docs_rtd.sh:199:    snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:200:    market_snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:228:    dados/app.db:rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:249:    rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:257:    scripts/import_rtd_underlying_quotes_csv.py
- scripts/gerar_docs_rtd.sh:258:    scripts/refresh_rtd_underlying_quotes_excel.ps1
- scripts/gerar_docs_rtd.sh:304:        "SELECT ativo, ultimo_preco, source, updated_at FROM rtd_underlying_quotes ORDER BY ativo"
- scripts/gerar_docs_rtd.sh:335:    snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:336:    market_snapshot_source: rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:337:    is_static_fallback: False
- scripts/gerar_docs_rtd.sh:343:Se snapshot_source for rtd_underlying_quotes, o provider esta lendo corretamente de dados/app.db.
- scripts/gerar_docs_rtd.sh:345:Se is_static_fallback for False, o fluxo nao esta usando fallback estatico.
- scripts/gerar_docs_rtd.sh:351:Se o provider nao retornar rtd_underlying_quotes, verificar:
- scripts/gerar_docs_rtd.sh:355:    existencia da tabela rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:372:    rtd_underlying_quotes existe em dados/app.db
- scripts/gerar_docs_rtd.sh:375:    MarketSnapshotProvider.get_snapshot retorna snapshot_source igual a rtd_underlying_quotes
- scripts/gerar_docs_rtd.sh:376:    MarketSnapshotProvider.get_snapshot retorna is_static_fallback igual a False
- scripts/gerar_docs_rtd.sh:381:Nao criar rtd_underlying_quotes em dados/derived.db.
- scripts/gerar_docs_rtd.sh:401:- docs/checklists/rtd_underlying_quotes.md
- scripts/import_rtd_underlying_quotes_csv.py:99:        CREATE TABLE IF NOT EXISTS rtd_underlying_quotes (
- scripts/import_rtd_underlying_quotes_csv.py:121:        CREATE UNIQUE INDEX IF NOT EXISTS idx_rtd_underlying_quotes_ativo
- scripts/import_rtd_underlying_quotes_csv.py:122:        ON rtd_underlying_quotes(ativo)
- scripts/import_rtd_underlying_quotes_csv.py:193:          FROM rtd_underlying_quotes
- scripts/import_rtd_underlying_quotes_csv.py:225:            INSERT INTO rtd_underlying_quotes (
- scripts/import_rtd_underlying_quotes_csv.py:282:    cur.execute("SELECT COUNT(*) FROM rtd_underlying_quotes")
- scripts/import_rtd_underlying_quotes_csv.py:290:        description="Importa CSV RTD de ativos-base para rtd_underlying_quotes."
- scripts/run_rtd_underlying_refresh_full.py:30:               AND name = 'rtd_underlying_quotes'
- scripts/run_rtd_underlying_refresh_full.py:44:              FROM rtd_underlying_quotes
- scripts/run_rtd_underlying_refresh_full.py:146:            str(Path("scripts/refresh_rtd_underlying_quotes_excel.ps1").resolve()),
- scripts/run_rtd_underlying_refresh_full.py:164:        "scripts/import_rtd_underlying_quotes_csv.py",
- services/canonical_input_service.py:162:        market_snapshot_source = (
- services/canonical_input_service.py:163:            base_snapshot.get("market_snapshot_source")
- services/canonical_input_service.py:167:        market_is_static_fallback = bool(base_snapshot.get("is_static_fallback"))
- services/canonical_input_service.py:190:            "snapshot_source":          market_snapshot_source,
- services/canonical_input_service.py:191:            "market_snapshot_source":   market_snapshot_source,
- services/canonical_input_service.py:192:            "market_is_static_fallback": market_is_static_fallback,
- services/market_snapshot_provider.py:12:DEFAULT_MARKET_BY_ASSET: dict[str, dict[str, Any]] = {
- services/market_snapshot_provider.py:29:        "spot_price": 66.84,
- services/market_snapshot_provider.py:51:def _env_allows_static_fallback() -> bool:
- services/market_snapshot_provider.py:65:        allow_static_fallback: bool | None = None,
- services/market_snapshot_provider.py:72:        if allow_static_fallback is None:
- services/market_snapshot_provider.py:73:            allow_static_fallback = _env_allows_static_fallback()
- services/market_snapshot_provider.py:75:        self.allow_static_fallback = bool(allow_static_fallback)
- services/market_snapshot_provider.py:87:        db_snapshot = self._snapshot_from_rtd_underlying_quotes(asset, effective_reference_date)
- services/market_snapshot_provider.py:91:        if self.allow_static_fallback:
- services/market_snapshot_provider.py:92:            return self._snapshot_from_static_fallback(asset, effective_reference_date)
- services/market_snapshot_provider.py:116:    def _snapshot_from_rtd_underlying_quotes(
- services/market_snapshot_provider.py:134:                    FROM rtd_underlying_quotes
- services/market_snapshot_provider.py:142:            if self.allow_static_fallback:
- services/market_snapshot_provider.py:145:                f'erro ao consultar rtd_underlying_quotes para asset={asset}: {exc}'
- services/market_snapshot_provider.py:153:            if self.allow_static_fallback:
- services/market_snapshot_provider.py:156:                f'rtd_underlying_quotes sem ultimo_preco vÃ¡lido para asset={asset}'
- services/market_snapshot_provider.py:159:        defaults = DEFAULT_MARKET_BY_ASSET.get(asset, {})
- services/market_snapshot_provider.py:167:            "snapshot_source": "rtd_underlying_quotes",
- services/market_snapshot_provider.py:168:            "market_snapshot_source": "rtd_underlying_quotes",
- services/market_snapshot_provider.py:169:            "is_static_fallback": False,
- services/market_snapshot_provider.py:176:    def _snapshot_from_static_fallback(
- services/market_snapshot_provider.py:181:        market = DEFAULT_MARKET_BY_ASSET.get(asset)
- services/market_snapshot_provider.py:191:            "snapshot_source": "static_fallback",
- services/market_snapshot_provider.py:192:            "market_snapshot_source": "static_fallback",
- services/market_snapshot_provider.py:193:            "is_static_fallback": True,
- services/payoff_pricing_engine.py:34:                "pricing_payload.spot_price veio de static_fallback; "
- services/payoff_pricing_engine.py:102:            pricing_payload.get("market_snapshot_source")
- services/payoff_pricing_engine.py:104:            or meta.get("market_snapshot_source")
- services/payoff_pricing_engine.py:106:            or input_meta.get("market_snapshot_source")
- services/payoff_pricing_engine.py:114:                pricing_payload.get("is_static_fallback"),
- services/payoff_pricing_engine.py:115:                pricing_payload.get("market_is_static_fallback"),
- services/payoff_pricing_engine.py:116:                meta.get("is_static_fallback"),
- services/payoff_pricing_engine.py:117:                meta.get("market_is_static_fallback"),
- services/payoff_pricing_engine.py:118:                input_meta.get("is_static_fallback"),
- services/payoff_pricing_engine.py:119:                input_meta.get("market_is_static_fallback"),
- services/payoff_pricing_engine.py:123:        return explicit_static_flag or source == "static_fallback"
- services/pricing_payload_adapter.py:58:        "market_snapshot_source": (
- services/pricing_payload_adapter.py:59:            market.get("market_snapshot_source")
- services/pricing_payload_adapter.py:62:        "is_static_fallback": bool(market.get("is_static_fallback")),
- services/structure_market_input_assembler.py:31:            "market_snapshot_source": (
- services/structure_market_input_assembler.py:32:                market_snapshot.get("market_snapshot_source")
- services/structure_market_input_assembler.py:35:            "is_static_fallback": bool(market_snapshot.get("is_static_fallback")),

## Conferencia 5 - Busca de valor 66.84 nos bancos

Ocorrencias encontradas:
- {"db": "dados/app.db", "table": "pricing_executions", "column": "pricing_payload", "token": "66.84", "count": 18}
- {"db": "dados/app.db", "table": "pricing_executions", "column": "result", "token": "66.84", "count": 18}
- {"db": "dados/app.db", "table": "structure_snapshots", "column": "market_json", "token": "66.84", "count": 18}
- {"db": "dados/app.db", "table": "structure_snapshots", "column": "metrics_json", "token": "66.84", "count": 18}
- {"db": "dados/app.db", "table": "structure_snapshots", "column": "payoff_json", "token": "66.84", "count": 14}
- {"db": "dados/app.db", "table": "structure_snapshots", "column": "operation_state_json", "token": "66.84", "count": 18}
- {"db": "dados/derived.db", "table": "payoff_curve_points", "column": "point_spot", "token": "66.84", "count": 18}
- {"db": "dados/derived.db", "table": "structure_decisions", "column": "spot_ref", "token": "66.84", "count": 18}

## Conferencia 6 - Documentacao criada

docs/arquitetura/fonte_autoritativa_rtd_ativos_base.md: existe
docs/checklists/rtd_underlying_quotes.md: existe
docs/README.md: existe
docs/correcao_de_payoff.md: existe

## Resumo das tres primeiras pendencias

| Pendencia | Estado documentado | Evidencia |
| --- | --- | --- |
| MarketSnapshotProvider lendo rtd_underlying_quotes | Fechada conferida | Conferencias 1 e 2 |
| Payoff BOVA11 sem preco atual indevido 66.84 | Requer atencao | Conferencia 5 e grep |
| Qualidade RTD opcoes: call_put e ultimo_preco zero | Fechada conferida | Conferencia 3 |

## Seguimento em direcao ao fechamento final

Com as tres primeiras pendencias tratadas, a frente deve seguir para as pendencias finais de produto, motor e auditoria.

### Pendencias finais restantes

1. Separar explicitamente payoff no vencimento de marcacao atual e PL atual.
2. Separar preco base na implantacao, preco base atual, preco usado na curva e preco simulado no vencimento.
3. Remover ou renomear o rotulo generico Preco ref. na interface.
4. Exibir tabela por perna com ticker, tipo, direcao, quantidade, strike, vencimento, premio de entrada, preco atual, intrinseco, extrinseco, PL atual e payoff no vencimento ao preco atual.
5. Validar comparabilidade entre estruturas antes de comparar curvas.
6. Bloquear ou alertar estruturas com ativo-base divergente, vencimentos incompatíveis ou fonte de mercado estatica.
7. Criar testes automatizados cobrindo call comprada, call vendida, put comprada, put vendida, travas e multiplas pernas.
8. Revalidar visualmente e por dados a estrutura 3 de BOVA11.

### Criterio de aceite final

- Nenhum calculo de PL atual deve usar static_fallback como preco de mercado.
- O spot atual deve ter origem auditavel em rtd_underlying_quotes.
- O payoff no vencimento deve estar separado do PL atual.
- A UI deve deixar claro qual preco e de implantacao, qual e atual e qual e simulado.
- Cada perna deve ser auditavel individualmente.
- Estruturas incompativeis nao devem ser comparadas sem alerta.
- Testes automatizados devem cobrir os cenarios financeiros minimos.

## Estado Git no momento da conferencia

-  M LISTA_RTD.xlsm

