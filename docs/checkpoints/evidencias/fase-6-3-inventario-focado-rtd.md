# Fase 6.3 — Inventário focado RTD

## 1. Arquivos produtivos que citam rtd_option_quotes

infra/bootstrap_rtd_option_quotes_schema.py
repositories/rtd_option_quotes_repository.py
scripts/audit_rtd_option_quotes.py
scripts/build_rtd_symbols.py
scripts/import_lista_rtd_excel_to_option_quotes.py
scripts/import_rtd_links_to_option_quotes.py
scripts/import_rtd_option_quotes_wide_csv.py
scripts/mapear_automacao_opcoes_rtd.py
scripts/run_lista_rtd_option_quotes_pipeline.py
scripts/run_rtd_option_quotes_pipeline.py
scripts/run_rtd_refresh_full.py
scripts/seed_current_rtd_option_quotes.py
services/canonical_pricing_facade.py

## 2. Arquivos produtivos que citam pipeline/auditoria RTD

scripts/audit_rtd_option_quotes.py
scripts/run_lista_rtd_option_quotes_pipeline.py
scripts/run_rtd_option_quotes_pipeline.py

## 3. Arquivos produtivos que citam integração canonical pricing / RTD


## 4. Testes diretamente relacionados


## 5. Snippets produtivos limitados

infra/bootstrap_rtd_option_quotes_schema.py:8:TABLE_NAME = "rtd_option_quotes"
infra/bootstrap_rtd_option_quotes_schema.py:35:CREATE TABLE IF NOT EXISTS rtd_option_quotes (
infra/bootstrap_rtd_option_quotes_schema.py:89:def ensure_rtd_option_quotes_schema(db_path: Path | str) -> None:
infra/bootstrap_rtd_option_quotes_schema.py:102:                "Tabela rtd_option_quotes existe, mas está sem colunas obrigatórias: "
infra/bootstrap_rtd_option_quotes_schema.py:108:        description="Cria/valida o schema vazio de rtd_option_quotes em banco SQLite."
infra/bootstrap_rtd_option_quotes_schema.py:120:    print("Bootstrap rtd_option_quotes")
infra/bootstrap_rtd_option_quotes_schema.py:145:    print("[OK] Schema rtd_option_quotes disponível.")
repositories/rtd_option_quotes_repository.py:1:# repositories/rtd_option_quotes_repository.py
repositories/rtd_option_quotes_repository.py:14:    Leitura da tabela rtd_option_quotes.
repositories/rtd_option_quotes_repository.py:50:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:82:            FROM rtd_option_quotes
repositories/rtd_option_quotes_repository.py:114:            FROM rtd_option_quotes
scripts/audit_rtd_option_quotes.py:3:Audita a tabela rtd_option_quotes em um banco SQLite.
scripts/audit_rtd_option_quotes.py:7:    python scripts/audit_rtd_option_quotes.py --db dados/app.db
scripts/audit_rtd_option_quotes.py:8:    python scripts/audit_rtd_option_quotes.py --db dados/app.db --json
scripts/audit_rtd_option_quotes.py:23:TABLE_NAME = "rtd_option_quotes"
scripts/audit_rtd_option_quotes.py:218:    print("Auditoria rtd_option_quotes")
scripts/audit_rtd_option_quotes.py:254:        description="Audita a tabela rtd_option_quotes em um banco SQLite."
scripts/build_rtd_symbols.py:81:def collect_from_rtd_option_quotes(cur):
scripts/build_rtd_symbols.py:82:    if not table_exists(cur, "rtd_option_quotes"):
scripts/build_rtd_symbols.py:87:        FROM rtd_option_quotes
scripts/build_rtd_symbols.py:129:            quote_symbols = collect_from_rtd_option_quotes(cur)
scripts/build_rtd_symbols.py:130:            sources.append(("rtd_option_quotes", quote_symbols))
scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
scripts/import_lista_rtd_excel_to_option_quotes.py:7:        -> tabela rtd_option_quotes
scripts/import_lista_rtd_excel_to_option_quotes.py:427:    columns = get_table_columns(conn, "rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:430:        raise RuntimeError("Tabela rtd_option_quotes não encontrada no banco.")
scripts/import_lista_rtd_excel_to_option_quotes.py:436:            "Tabela rtd_option_quotes está sem colunas obrigatórias: "
scripts/import_lista_rtd_excel_to_option_quotes.py:458:                "SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? LIMIT 1",
scripts/import_lista_rtd_excel_to_option_quotes.py:502:            UPDATE rtd_option_quotes
scripts/import_lista_rtd_excel_to_option_quotes.py:534:            INSERT INTO rtd_option_quotes (
scripts/import_lista_rtd_excel_to_option_quotes.py:588:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
scripts/import_lista_rtd_excel_to_option_quotes.py:694:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:704:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_rtd_links_to_option_quotes.py:3:Importa dados verticais de dados/RTD_LINKS.csv para rtd_option_quotes.
scripts/import_rtd_links_to_option_quotes.py:307:        FROM rtd_option_quotes
scripts/import_rtd_links_to_option_quotes.py:323:        "ativo_base = COALESCE(excluded.ativo_base, rtd_option_quotes.ativo_base)",
scripts/import_rtd_links_to_option_quotes.py:324:        "call_put = COALESCE(excluded.call_put, rtd_option_quotes.call_put)",
scripts/import_rtd_links_to_option_quotes.py:325:        "strike = COALESCE(excluded.strike, rtd_option_quotes.strike)",
scripts/import_rtd_links_to_option_quotes.py:326:        "vencimento = COALESCE(excluded.vencimento, rtd_option_quotes.vencimento)",
scripts/import_rtd_links_to_option_quotes.py:327:        "ultimo_preco = COALESCE(excluded.ultimo_preco, rtd_option_quotes.ultimo_preco)",
scripts/import_rtd_links_to_option_quotes.py:328:        "ultima_quantidade = COALESCE(excluded.ultima_quantidade, rtd_option_quotes.ultima_quantidade)",
scripts/import_rtd_links_to_option_quotes.py:329:        "bid = COALESCE(excluded.bid, rtd_option_quotes.bid)",
scripts/import_rtd_links_to_option_quotes.py:330:        "ask = COALESCE(excluded.ask, rtd_option_quotes.ask)",
scripts/import_rtd_links_to_option_quotes.py:331:        "volume = COALESCE(excluded.volume, rtd_option_quotes.volume)",
scripts/import_rtd_links_to_option_quotes.py:332:        "iv = COALESCE(excluded.iv, rtd_option_quotes.iv)",
scripts/import_rtd_links_to_option_quotes.py:333:        "delta = COALESCE(excluded.delta, rtd_option_quotes.delta)",
scripts/import_rtd_links_to_option_quotes.py:334:        "gamma = COALESCE(excluded.gamma, rtd_option_quotes.gamma)",
scripts/import_rtd_links_to_option_quotes.py:335:        "theta = COALESCE(excluded.theta, rtd_option_quotes.theta)",
scripts/import_rtd_links_to_option_quotes.py:336:        "vega = COALESCE(excluded.vega, rtd_option_quotes.vega)",
scripts/import_rtd_links_to_option_quotes.py:343:        INSERT INTO rtd_option_quotes ({columns_sql})
scripts/import_rtd_links_to_option_quotes.py:386:        description="Importa dados/RTD_LINKS.csv para rtd_option_quotes"
scripts/import_rtd_links_to_option_quotes.py:419:    print("Importação RTD_LINKS.csv -> rtd_option_quotes")
scripts/import_rtd_option_quotes_wide_csv.py:14:from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema
scripts/import_rtd_option_quotes_wide_csv.py:207:        CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo_opcao
scripts/import_rtd_option_quotes_wide_csv.py:208:        ON rtd_option_quotes(codigo_opcao)
scripts/import_rtd_option_quotes_wide_csv.py:226:    ensure_rtd_option_quotes_schema(db_path)
scripts/import_rtd_option_quotes_wide_csv.py:237:                "SELECT id, created_at FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
scripts/import_rtd_option_quotes_wide_csv.py:251:                    UPDATE rtd_option_quotes
scripts/import_rtd_option_quotes_wide_csv.py:299:                    INSERT INTO rtd_option_quotes (
scripts/mapear_automacao_opcoes_rtd.py:69:    "repositories/rtd_option_quotes_repository.py": "Prioritário para auditoria de persistência RTD.",
scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
scripts/run_lista_rtd_option_quotes_pipeline.py:7:    2. scripts/audit_rtd_option_quotes.py
scripts/run_lista_rtd_option_quotes_pipeline.py:10:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS
scripts/run_lista_rtd_option_quotes_pipeline.py:11:    python scripts/run_lista_rtd_option_quotes_pipeline.py --db dados/app.db --sheet RTD_PROBE_OPTIONS --json
scripts/run_lista_rtd_option_quotes_pipeline.py:12:    python scripts/run_lista_rtd_option_quotes_pipeline.py --dry-run --json
scripts/run_lista_rtd_option_quotes_pipeline.py:26:AUDIT_SCRIPT = Path("scripts/audit_rtd_option_quotes.py")
scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_rtd_option_quotes_pipeline.py:7:    dados/RTD_LINKS.csv -> rtd_option_quotes -> auditoria
scripts/run_rtd_option_quotes_pipeline.py:11:    python scripts/run_rtd_option_quotes_pipeline.py
scripts/run_rtd_option_quotes_pipeline.py:12:    python scripts/run_rtd_option_quotes_pipeline.py --csv dados/RTD_LINKS.csv --db dados/app.db
scripts/run_rtd_option_quotes_pipeline.py:13:    python scripts/run_rtd_option_quotes_pipeline.py --dry-run
scripts/run_rtd_option_quotes_pipeline.py:14:    python scripts/run_rtd_option_quotes_pipeline.py --fail-on-warn
scripts/run_rtd_option_quotes_pipeline.py:28:IMPORT_SCRIPT = SCRIPTS_DIR / "import_rtd_option_quotes_wide_csv.py"
scripts/run_rtd_option_quotes_pipeline.py:29:AUDIT_SCRIPT = SCRIPTS_DIR / "audit_rtd_option_quotes.py"
scripts/run_rtd_option_quotes_pipeline.py:142:        description="Executa importação e auditoria de rtd_option_quotes."
scripts/run_rtd_refresh_full.py:43:            FROM rtd_option_quotes
scripts/run_rtd_refresh_full.py:100:    import_script = Path("scripts/import_rtd_option_quotes_wide_csv.py")
scripts/run_rtd_refresh_full.py:101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
scripts/run_rtd_refresh_full.py:195:        print("- Cadastre uma estrutura pelo sistema ou rode sem --strict para usar fallback de rtd_option_quotes.")
scripts/seed_current_rtd_option_quotes.py:3:Limpa e popula rtd_option_quotes com dados manuais atuais das estruturas
scripts/seed_current_rtd_option_quotes.py:8:    python scripts/seed_current_rtd_option_quotes.py
scripts/seed_current_rtd_option_quotes.py:9:    python scripts/seed_current_rtd_option_quotes.py --db dados/app.db
scripts/seed_current_rtd_option_quotes.py:13:- O script limpa somente a tabela rtd_option_quotes.
scripts/seed_current_rtd_option_quotes.py:136:        if not table_exists(connection, "rtd_option_quotes"):
scripts/seed_current_rtd_option_quotes.py:137:            raise RuntimeError("Tabela rtd_option_quotes não encontrada.")
scripts/seed_current_rtd_option_quotes.py:140:            "SELECT COUNT(*) FROM rtd_option_quotes"
scripts/seed_current_rtd_option_quotes.py:143:        connection.execute("DELETE FROM rtd_option_quotes")
scripts/seed_current_rtd_option_quotes.py:146:            INSERT INTO rtd_option_quotes (
scripts/seed_current_rtd_option_quotes.py:224:            "SELECT COUNT(*) FROM rtd_option_quotes"
scripts/seed_current_rtd_option_quotes.py:229:    print("Seed rtd_option_quotes concluído.")
scripts/seed_current_rtd_option_quotes.py:240:        description="Limpa e popula rtd_option_quotes com dados atuais de SMAL e PRIO."
services/canonical_pricing_facade.py:34:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
services/canonical_pricing_facade.py:157:def _resolve_rtd_option_quotes_db_path(primary_db_path: Path) -> Path:
services/canonical_pricing_facade.py:159:    Resolve o banco correto para rtd_option_quotes.
services/canonical_pricing_facade.py:190:        if _sqlite_table_exists(candidate, "rtd_option_quotes"):
services/canonical_pricing_facade.py:320:    Escolhe o melhor preço disponível em rtd_option_quotes e informa
services/canonical_pricing_facade.py:355:    Escolhe o melhor preço disponível em rtd_option_quotes.
services/canonical_pricing_facade.py:457:    rtd_option_quotes_repository: RtdOptionQuotesRepository | None,
services/canonical_pricing_facade.py:465:      manual explícito > rtd_option_quotes > preço original do snapshot.
services/canonical_pricing_facade.py:484:    if rtd_option_quotes_repository is not None:
services/canonical_pricing_facade.py:486:            repository=rtd_option_quotes_repository,
services/canonical_pricing_facade.py:549:                "rtd_option_quotes",
services/canonical_pricing_facade.py:687:    rtd_option_quotes_repository: RtdOptionQuotesRepository | None = None,
services/canonical_pricing_facade.py:705:            rtd_option_quotes_repository=rtd_option_quotes_repository,
services/canonical_pricing_facade.py:810:        self._rtd_option_quotes_db_path = _resolve_rtd_option_quotes_db_path(self._db_path)
services/canonical_pricing_facade.py:811:        self._rtd_option_quotes_repository = RtdOptionQuotesRepository(
services/canonical_pricing_facade.py:812:            db_path=self._rtd_option_quotes_db_path,
services/canonical_pricing_facade.py:844:                rtd_option_quotes_repository=self._rtd_option_quotes_repository,
