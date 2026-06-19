# repositories/rtd_option_quotes_repository.py

## Classes/funções/testes

- `RtdOptionQuotesRepository`
- `__init__`
- `_connect`
- `get_by_codigo`
- `list_by_ativo_base`
- `list_all`

## Linhas relevantes

1: # repositories/rtd_option_quotes_repository.py
14:     Leitura da tabela rtd_option_quotes.
16:     Essa tabela é alimentada pelo CSV exportado da aba RTD_LINKS
17:     e funciona como cache centralizado das cotações RTD de opções.
20:     def __init__(self, db_path: str | Path | None = None) -> None:
21:         self.db_path = Path(db_path).expanduser().resolve() if db_path is not None else get_app_db_path()
28:     def get_by_codigo(self, codigo_opcao: str) -> dict[str, Any] | None:
36:                 ultimo_preco,
50:             FROM rtd_option_quotes
58:         return dict(row) if row else None
68:                 ultimo_preco,
82:             FROM rtd_option_quotes
100:                 ultimo_preco,
114:             FROM rtd_option_quotes

---

# services/canonical_pricing_facade.py

## Classes/funções/testes

- `_get_structure_info`
- `_to_float`
- `_normalize_expiration_date`
- `_pick`
- `_quote_ident`
- `_sqlite_table_exists`
- `_resolve_rtd_option_quotes_db_path`
- `_is_manual_source`
- `_quote_value`
- `_parse_rtd_quote_updated_at`
- `_is_rtd_option_quote_stale`
- `_pick_rtd_option_price_with_trace`
- `_pick_rtd_option_price`
- `_normalize_asset_code`
- `_rtd_quote_traceability`
- `_lookup_rtd_option_quote`
- `_resolve_effective_leg_price`
- `_lookup_spot_price`
- `_snapshot_result_to_payload`
- `CanonicalPricingFacade`
- `__init__`
- `execute_pricing`

## Linhas relevantes

34: from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
61:     if row is None:
79:         if value is None or value == "":
100: def _normalize_expiration_date(value: Any) -> str | None:
102:         return None
125:         if value is not None:
127:     return None
130: def _quote_ident(name: str) -> str:
152:         return row is not None
157: def _resolve_rtd_option_quotes_db_path(primary_db_path: Path) -> Path:
159:     Resolve o banco correto para rtd_option_quotes.
165:     4. fallback seguro para o banco primário.
190:         if _sqlite_table_exists(candidate, "rtd_option_quotes"):
198:     if value is None:
205: def _quote_value(quote: Any, field: str) -> Any:
207:     if quote is None:
208:         return None
210:     if hasattr(quote, "get"):
212:             return quote.get(field)
217:         return quote[field]
222:         return getattr(quote, field)
224:         return None
227: RTD_OPTION_QUOTE_MAX_AGE_MINUTES = 30
230: def _parse_rtd_quote_updated_at(value: Any) -> datetime | None:
231:     """Converte updated_at da quote RTD para datetime local ingênuo."""
232:     if value is None:
233:         return None
240:             return None
248:             parsed = None
261:             if parsed is None:
262:                 return None
264:     if parsed.tzinfo is not None:
265:         return parsed.astimezone().replace(tzinfo=None)
270: def _is_rtd_option_quote_stale(
271:     quote: Any | None,
273:     max_age_minutes: int = RTD_OPTION_QUOTE_MAX_AGE_MINUTES,
274:     now: datetime | None = None,
275:     reference_date: Any | None = None,
278:     Retorna True quando a quote RTD está vencida.
283:     updated_at = _parse_rtd_quote_updated_at(_quote_value(quote, "updated_at"))
285:     if updated_at is None:
288:     if reference_date is not None:
289:         reference_dt = _parse_rtd_quote_updated_at(reference_date)
291:         if reference_dt is not None and updated_at.date() == reference_dt.date():
294:             if current_for_today.tzinfo is not None:
295:                 current_for_today = current_for_today.astimezone().replace(tzinfo=None)
297:             # Cenários históricos controlados usam quotes RTD do próprio
298:             # reference_date. Neles, a validade intradiária de 30 minutos
299:             # não deve invalidar o teste/backtest dias depois.
305:     if current.tzinfo is not None:
306:         current = current.astimezone().replace(tzinfo=None)
316: def _pick_rtd_option_price_with_trace(
317:     quote: Any | None,
318: ) -> tuple[float | None, str | None]:
320:     Escolhe o melhor preço disponível em rtd_option_quotes e informa
324:       1. ultimo_preco
325:       2. price / last_price, se existirem por compatibilidade
330:     if not quote:
331:         return None, None
333:     for field in ("ultimo_preco", "price", "last_price"):
334:         price = _to_float(_quote_value(quote, field), 0.0)
335:         if price > 0:
336:             return price, field
338:     bid = _to_float(_quote_value(quote, "bid"), 0.0)
339:     ask = _to_float(_quote_value(quote, "ask"), 0.0)
350:     return None, None
353: def _pick_rtd_option_price(quote: Any | None) -> float | None:
355:     Escolhe o melhor preço disponível em rtd_option_quotes.
358:     completa, usar _pick_rtd_option_price_with_trace.
360:     price, _field = _pick_rtd_option_price_with_trace(quote)
361:     return price
366:     if value is None:
372: def _rtd_quote_traceability(
373:     quote: Any | None,
375:     rtd_quote_found: bool,
376:     price_resolution_status: str,
377:     rtd_validation_status: str,
378:     rtd_validation_message: str | None,
379:     rtd_price_field: str | None = None,
381:     """Monta metadados de guardrail/diagnóstico RTD."""
383:         "price_resolution_status": price_resolution_status,
384:         "rtd_quote_found": rtd_quote_found,
385:         "rtd_validation_status": rtd_validation_status,
386:         "rtd_validation_message": rtd_validation_message,
389:     if rtd_price_field:
390:         traceability["rtd_price_field"] = rtd_price_field
392:     if quote is not None:
395:                 "rtd_quote_codigo_opcao": _quote_value(quote, "codigo_opcao"),
396:                 "rtd_quote_ativo_base": _quote_value(quote, "ativo_base"),
397:                 "rtd_price_source": _quote_value(quote, "source"),
398:                 "rtd_price_updated_at": _quote_value(quote, "updated_at"),
399:                 "rtd_price_created_at": _quote_value(quote, "created_at"),
406: def _lookup_rtd_option_quote(
409: ) -> Any | None:
411:     Busca cotação RTD da opção por código.
416:         return None
420:         return None
430:         "get_latest_by_codigo",
437:             method = getattr(repository, method_name, None)
438:             if method is None:
442:                 quote = method(codigo)
444:                 quote = None
446:             if quote:
447:                 return quote
449:     return None
452: def _resolve_effective_leg_price(
454:     raw_price: Any,
457:     rtd_option_quotes_repository: RtdOptionQuotesRepository | None,
458:     underlying_asset: Any | None = None,
459:     reference_date: Any | None = None,
465:       manual explícito > rtd_option_quotes > preço original do snapshot.
470:     original_price = _to_float(raw_price, 0.0)
472:     if _is_manual_source(leg_source) and original_price > 0:
474:             original_price,
477:                 "price_resolution_status": "ok",
478:                 "rtd_quote_found": None,
479:                 "rtd_validation_status": "not_applicable",
480:                 "rtd_validation_message": "Preço manual explícito preservado; RTD não consultado.",
484:     if rtd_option_quotes_repository is not None:
485:         quote = _lookup_rtd_option_quote(
486:             repository=rtd_option_quotes_repository,
490:         if not quote:
491:             fallback_source = "snapshot" if original_price > 0 else "missing"
493:                 original_price,
494:                 fallback_source,
495:                 _rtd_quote_traceability(
496:                     None,
497:                     rtd_quote_found=False,
498:                     price_resolution_status="missing_rtd_quote",
499:                     rtd_validation_status="error",
500:                     rtd_validation_message=(
501:                         f"Quote RTD não encontrada para a opção {raw_asset}."
506:         quote_ativo_base = _normalize_asset_code(_quote_value(quote, "ativo_base"))
509:         if quote_ativo_base and expected_ativo_base and quote_ativo_base != expected_ativo_base:
510:             fallback_source = "snapshot" if original_price > 0 else "missing"
512:                 original_price,
513:                 fallback_source,
514:                 _rtd_quote_traceability(
515:                     quote,
516:                     rtd_quote_found=True,
517:                     price_resolution_status="rtd_asset_mismatch",
518:                     rtd_validation_status="error",
519:                     rtd_validation_message=(
520:                         "Ativo base da quote RTD diverge do ativo base da estrutura: "
521:                         f"quote={quote_ativo_base}, estrutura={expected_ativo_base}."
526:         if _is_rtd_option_quote_stale(quote, reference_date=reference_date):
527:             fallback_source = "snapshot" if original_price > 0 else "missing"
529:                 original_price,
530:                 fallback_source,
531:                 _rtd_quote_traceability(
532:                     quote,
533:                     rtd_quote_found=True,
534:                     price_resolution_status="stale_rtd_quote",
535:                     rtd_validation_status="warn",
536:                     rtd_validation_message=(
537:                         "Quote RTD vencida pelo critério de validade de "
538:                         f"{RTD_OPTION_QUOTE_MAX_AGE_MINUTES} minutos; "
544:         rtd_price, rtd_price_field = _pick_rtd_option_price_with_trace(quote)
546:         if rtd_price is not None and rtd_price > 0:
548:                 rtd_price,
549:                 "rtd_option_quotes",
550:                 _rtd_quote_traceability(
551:                     quote,
552:                     rtd_quote_found=True,
553:                     price_resolution_status="ok",
554:                     rtd_validation_status="ok",
555:                     rtd_validation_message=None,
556:                     rtd_price_field=rtd_price_field,
560:         fallback_source = "snapshot" if original_price > 0 else "missing"
562:             original_price,
563:             fallback_source,
564:             _rtd_quote_traceability(
565:                 quote,
566:                 rtd_quote_found=True,
567:                 price_resolution_status="invalid_rtd_price",
568:                 rtd_validation_status="error",
569:                 rtd_validation_message=(
570:                     f"Quote RTD encontrada para {raw_asset}, mas sem preço utilizável."
575:     fallback_source = "snapshot" if original_price > 0 else "missing"
576:     fallback_status = "ok" if original_price > 0 else "missing_price"
579:         original_price,
580:         fallback_source,
582:             "price_resolution_status": fallback_status,
583:             "rtd_quote_found": None,
584:             "rtd_validation_status": "not_applicable",
585:             "rtd_validation_message": "Repository RTD não disponível para consulta.",
590: def _lookup_spot_price(db_path: Path, underlying_asset: str) -> float:
612:     price_candidates = {
614:         "spot_price",
615:         "underlying_price",
616:         "last_price",
617:         "price",
618:         "preco",
619:         "preco_atual",
635:                     f"PRAGMA table_info({_quote_ident(table_name)})"
647:                 price_cols = [
649:                     for name in price_candidates
653:                 if not symbol_cols or not price_cols:
657:                     for price_col in price_cols:
659:                             f"SELECT {_quote_ident(price_col)} "
660:                             f"FROM {_quote_ident(table_name)} "
661:                             f"WHERE UPPER(CAST({_quote_ident(symbol_col)} AS TEXT)) = UPPER(?) "
662:                             f"AND {_quote_ident(price_col)} IS NOT NULL "
672:                             price = _to_float(row[0], 0.0)
673:                             if price > 0:
674:                                 return price
685:     reference_date: str | None,
687:     rtd_option_quotes_repository: RtdOptionQuotesRepository | None = None,
696:         raw_price = _pick(d, "premium", "price", "valor_executado")
701:         effective_price, price_source, price_traceability = _resolve_effective_leg_price(
702:             raw_price=raw_price,
705:             rtd_option_quotes_repository=rtd_option_quotes_repository,
717:             "price":       effective_price,
728:             "price_source": price_source,
732:             "premium":         effective_price,
742:                 for key, value in price_traceability.items()
750:         getattr(selection_result, "spot_price", None)
751:         or getattr(selection_result, "spot", None)
752:         or getattr(selection_result, "underlying_price", None)
753:         or getattr(selection_result, "last_price", None)
756:     spot_price = _to_float(spot, 0.0)
758:     if spot_price <= 0:
759:         spot_price = _lookup_spot_price(
764:     if spot_price <= 0:
766:             f"spot_price inválido ou ausente para underlying_asset={underlying_asset}. "
767:             "Não persistir execução OK com spot_price <= 0."
774:         "spot_price":       spot_price,
781:             "manual_overrides": getattr(selection_result, "manual_overrides", None) or [],
803:         db_path: Path | str | None = None,
804:         pricing_execution_service: PricingExecutionService | None = None,
805:         persistence_service: PricingExecutionPersistenceService | None = None,
806:     ) -> None:
810:         self._rtd_option_quotes_db_path = _resolve_rtd_option_quotes_db_path(self._db_path)
811:         self._rtd_option_quotes_repository = RtdOptionQuotesRepository(
812:             db_path=self._rtd_option_quotes_db_path,
824:         reference_date: str | None = None,
834:             #  2. Seleciona snapshot (manual > rtd)
844:                 rtd_option_quotes_repository=self._rtd_option_quotes_repository,
862:                 error_message=None,
881:                     pricing_payload=None,
891:                 "canonical_input": None,
892:                 "pricing_payload": None,
893:                 "result":          None,
894:                 "persisted":       None,

---

# ATT/tests/test_rtd_option_quotes_repository_contract.py

## Classes/funções/testes

- `_create_schema`
- `test_get_by_codigo_returns_quote_dict_when_codigo_exists`
- `test_get_by_codigo_returns_none_when_codigo_does_not_exist`
- `test_get_by_codigo_uses_exact_codigo_match`
- `test_get_by_codigo_propagates_sqlite_error_when_table_is_missing`
- `test_list_by_ativo_base_returns_ordered_quotes_for_asset`
- `test_list_all_returns_quotes_as_dicts`

## Linhas relevantes

6: from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
9: def _create_schema(db_path: Path) -> None:
13:             CREATE TABLE rtd_option_quotes (
20:                 ultimo_preco REAL,
39: def test_get_by_codigo_returns_quote_dict_when_codigo_exists(tmp_path):
46:             INSERT INTO rtd_option_quotes (
52:                 ultimo_preco,
85:                 "rtd_option_quotes",
94:     quote = repository.get_by_codigo("PETRA123")
96:     assert quote is not None
97:     assert quote["codigo_opcao"] == "PETRA123"
98:     assert quote["ativo_base"] == "PETR4"
99:     assert quote["ultimo_preco"] == 1.23
100:     assert quote["bid"] == 1.20
101:     assert quote["ask"] == 1.26
102:     assert quote["source"] == "rtd_option_quotes"
103:     assert quote["updated_at"] == "2026-06-18 10:00:00"
112:     assert repository.get_by_codigo("INEXISTENTE") is None
122:             INSERT INTO rtd_option_quotes (
128:                 ultimo_preco,
142:                 "rtd_option_quotes",
150:     assert repository.get_by_codigo("petra123") is None
151:     assert repository.get_by_codigo("PETRA123") is not None
164: def test_list_by_ativo_base_returns_ordered_quotes_for_asset(tmp_path):
177:             INSERT INTO rtd_option_quotes (
183:                 ultimo_preco,
188:             VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
195:     quotes = repository.list_by_ativo_base("PETR4")
197:     assert [quote["codigo_opcao"] for quote in quotes] == ["PETRA123", "PETRB123"]
198:     assert all(quote["ativo_base"] == "PETR4" for quote in quotes)
201: def test_list_all_returns_quotes_as_dicts(tmp_path):
213:             INSERT INTO rtd_option_quotes (
219:                 ultimo_preco,
224:             VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
231:     quotes = repository.list_all()
233:     assert [quote["codigo_opcao"] for quote in quotes] == ["PETRA123", "VALEA123"]
234:     assert all(isinstance(quote, dict) for quote in quotes)

---

# ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py

## Classes/funções/testes

- `FakeRtdOptionQuotesRepository`
- `test_pick_rtd_option_price_prefers_ultimo_preco`
- `test_pick_rtd_option_price_falls_back_to_price_and_last_price`
- `test_pick_rtd_option_price_falls_back_to_bid_ask_mid`
- `test_pick_rtd_option_price_falls_back_to_bid_or_ask`
- `test_pick_rtd_option_price_returns_none_when_no_positive_price_exists`
- `test_lookup_rtd_option_quote_tries_original_and_uppercase_codigo`
- `test_lookup_rtd_option_quote_returns_none_when_repository_raises`
- `test_resolve_effective_leg_price_preserves_explicit_manual_price`
- `test_resolve_effective_leg_price_uses_rtd_when_source_is_not_manual`
- `test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_when_no_rtd_quote`
- `test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_on_repository_error`
- `test_snapshot_result_to_payload_uses_rtd_price_for_canonical_leg_fields`
- `test_resolve_effective_leg_price_exposes_rtd_quote_traceability_metadata`
- `test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_has_no_usable_price`
- `test_snapshot_result_to_payload_does_not_leak_rtd_traceability_for_manual_price`
- `test_resolve_effective_leg_price_diagnoses_missing_rtd_quote`
- `test_resolve_effective_leg_price_diagnoses_invalid_rtd_price`
- `test_resolve_effective_leg_price_diagnoses_rtd_asset_mismatch`
- `test_snapshot_result_to_payload_preserves_rtd_guardrails_for_valid_quote`
- `test_snapshot_result_to_payload_preserves_rtd_guardrails_when_falling_back_to_snapshot`
- `test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_is_stale`
- `__init__`
- `get_by_codigo`

## Linhas relevantes

4:     _lookup_rtd_option_quote,
5:     _pick_rtd_option_price,
6:     _resolve_effective_leg_price,
12:     def __init__(self, quotes=None, fail=False):
13:         self.quotes = quotes or {}
23:         return self.quotes.get(codigo_opcao)
26: def test_pick_rtd_option_price_prefers_ultimo_preco():
27:     quote = {
28:         "ultimo_preco": 10.5,
29:         "price": 11.5,
30:         "last_price": 12.5,
35:     assert _pick_rtd_option_price(quote) == 10.5
38: def test_pick_rtd_option_price_falls_back_to_price_and_last_price():
39:     assert _pick_rtd_option_price({"ultimo_preco": 0, "price": 11.5}) == 11.5
40:     assert _pick_rtd_option_price({"ultimo_preco": None, "price": 0, "last_price": "12,50"}) == 12.5
43: def test_pick_rtd_option_price_falls_back_to_bid_ask_mid():
44:     quote = {
45:         "ultimo_preco": None,
46:         "price": None,
47:         "last_price": None,
52:     assert _pick_rtd_option_price(quote) == 3.0
55: def test_pick_rtd_option_price_falls_back_to_bid_or_ask():
56:     assert _pick_rtd_option_price({"bid": 2.0, "ask": 0}) == 2.0
57:     assert _pick_rtd_option_price({"bid": 0, "ask": 4.0}) == 4.0
60: def test_pick_rtd_option_price_returns_none_when_no_positive_price_exists():
61:     assert _pick_rtd_option_price({}) is None
62:     assert _pick_rtd_option_price({"ultimo_preco": 0, "price": 0, "bid": 0, "ask": 0}) is None
65: def test_lookup_rtd_option_quote_tries_original_and_uppercase_codigo():
67:         quotes={
70:                 "ultimo_preco": 1.23,
75:     quote = _lookup_rtd_option_quote(repository, "abcd11")
77:     assert quote["codigo_opcao"] == "ABCD11"
81: def test_lookup_rtd_option_quote_returns_none_when_repository_raises():
84:     quote = _lookup_rtd_option_quote(repository, "ABCD11")
86:     assert quote is None
89: def test_resolve_effective_leg_price_preserves_explicit_manual_price():
91:         quotes={
94:                 "ultimo_preco": 9.99,
99:     price, price_source, traceability = _resolve_effective_leg_price(
100:         raw_price=5.55,
103:         rtd_option_quotes_repository=repository,
107:     assert price == 5.55
108:     assert price_source == "manual"
109:     assert traceability["price_resolution_status"] == "ok"
110:     assert traceability["rtd_quote_found"] is None
111:     assert traceability["rtd_validation_status"] == "not_applicable"
112:     assert "manual explícito" in traceability["rtd_validation_message"]
116: def test_resolve_effective_leg_price_uses_rtd_when_source_is_not_manual():
118:         quotes={
121:                 "ultimo_preco": 9.99,
126:     price, price_source, traceability = _resolve_effective_leg_price(
127:         raw_price=5.55,
129:         leg_source="rtd",
130:         rtd_option_quotes_repository=repository,
134:     assert price == 9.99
135:     assert price_source == "rtd_option_quotes"
139: def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_when_no_rtd_quote():
142:     price, price_source, traceability = _resolve_effective_leg_price(
143:         raw_price=5.55,
145:         leg_source="rtd",
146:         rtd_option_quotes_repository=repository,
150:     assert price == 5.55
151:     assert price_source == "snapshot"
152:     assert traceability["price_resolution_status"] == "missing_rtd_quote"
153:     assert traceability["rtd_quote_found"] is False
154:     assert traceability["rtd_validation_status"] == "error"
155:     assert "não encontrada" in traceability["rtd_validation_message"]
158: def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_on_repository_error():
161:     price, price_source, traceability = _resolve_effective_leg_price(
162:         raw_price=5.55,
164:         leg_source="rtd",
165:         rtd_option_quotes_repository=repository,
169:     assert price == 5.55
170:     assert price_source == "snapshot"
173: def test_snapshot_result_to_payload_uses_rtd_price_for_canonical_leg_fields(tmp_path):
175:         quotes={
178:                 "ultimo_preco": 9.99,
192:                 "source": "rtd",
196:         spot_price=100.0,
197:         source="rtd",
208:         rtd_option_quotes_repository=repository,
213:     assert leg["price"] == 9.99
215:     assert leg["price_source"] == "rtd_option_quotes"
218:     assert payload["spot_price"] == 100.0
220: def test_resolve_effective_leg_price_exposes_rtd_quote_traceability_metadata():
222:         quotes={
226:                 "ultimo_preco": 9.99,
227:                 "source": "rtd_option_quotes",
234:     price, price_source, traceability = _resolve_effective_leg_price(
235:         raw_price=5.55,
237:         leg_source="rtd",
238:         rtd_option_quotes_repository=repository,
242:     assert price == 9.99
243:     assert price_source == "rtd_option_quotes"
245:         "price_resolution_status": "ok",
246:         "rtd_quote_found": True,
247:         "rtd_validation_status": "ok",
248:         "rtd_validation_message": None,
249:         "rtd_price_field": "ultimo_preco",
250:         "rtd_quote_codigo_opcao": "ABCD11",
251:         "rtd_quote_ativo_base": "ABCD",
252:         "rtd_price_source": "rtd_option_quotes",
253:         "rtd_price_updated_at": "2026-06-15T10:01:00",
254:         "rtd_price_created_at": "2026-06-15T10:00:00",
258: def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_has_no_usable_price():
260:         quotes={
264:                 "ultimo_preco": 0,
265:                 "price": 0,
266:                 "last_price": 0,
269:                 "source": "rtd_option_quotes",
276:     price, price_source, traceability = _resolve_effective_leg_price(
277:         raw_price=5.55,
279:         leg_source="rtd",
280:         rtd_option_quotes_repository=repository,
284:     assert price == 5.55
285:     assert price_source == "snapshot"
286:     assert traceability["price_resolution_status"] == "invalid_rtd_price"
287:     assert traceability["rtd_quote_found"] is True
288:     assert traceability["rtd_validation_status"] == "error"
289:     assert "sem preço utilizável" in traceability["rtd_validation_message"]
290:     assert traceability["rtd_quote_codigo_opcao"] == "ABCD11"
291:     assert traceability["rtd_quote_ativo_base"] == "ABCD"
292:     assert traceability["rtd_price_source"] == "rtd_option_quotes"
293:     assert traceability["rtd_price_updated_at"] == "2026-06-15T10:01:00"
294:     assert traceability["rtd_price_created_at"] == "2026-06-15T10:00:00"
297: def test_snapshot_result_to_payload_does_not_leak_rtd_traceability_for_manual_price(tmp_path):
299:         quotes={
303:                 "ultimo_preco": 9.99,
304:                 "source": "rtd_option_quotes",
324:         spot_price=100.0,
336:         rtd_option_quotes_repository=repository,
341:     assert leg["price"] == 5.55
343:     assert leg["price_source"] == "manual"
344:     assert "rtd_price_field" not in leg
345:     assert "rtd_quote_codigo_opcao" not in leg
346:     assert "rtd_quote_ativo_base" not in leg
347:     assert "rtd_price_source" not in leg
348:     assert "rtd_price_updated_at" not in leg
349:     assert "rtd_price_created_at" not in leg
353: def test_resolve_effective_leg_price_diagnoses_missing_rtd_quote():
356:     price, price_source, traceability = _resolve_effective_leg_price(
357:         raw_price=5.55,
359:         leg_source="rtd",
360:         rtd_option_quotes_repository=repository,
365:     assert price == 5.55
366:     assert price_source == "snapshot"
367:     assert traceability["rtd_quote_found"] is False
368:     assert traceability["price_resolution_status"] == "missing_rtd_quote"
369:     assert traceability["rtd_validation_status"] == "error"
370:     assert "não encontrada" in traceability["rtd_validation_message"]
373: def test_resolve_effective_leg_price_diagnoses_invalid_rtd_price():
375:         quotes={
379:                 "ultimo_preco": 0,
380:                 "price": 0,
381:                 "last_price": 0,
384:                 "source": "rtd_option_quotes",
389:     price, price_source, traceability = _resolve_effective_leg_price(
390:         raw_price=5.55,
392:         leg_source="rtd",
393:         rtd_option_quotes_repository=repository,
398:     assert price == 5.55
399:     assert price_source == "snapshot"
400:     assert traceability["rtd_quote_found"] is True
401:     assert traceability["price_resolution_status"] == "invalid_rtd_price"
402:     assert traceability["rtd_validation_status"] == "error"
403:     assert traceability["rtd_quote_codigo_opcao"] == "ABCD11"
404:     assert traceability["rtd_quote_ativo_base"] == "ABCD"
407: def test_resolve_effective_leg_price_diagnoses_rtd_asset_mismatch():
409:         quotes={
413:                 "ultimo_preco": 9.99,
414:                 "source": "rtd_option_quotes",
419:     price, price_source, traceability = _resolve_effective_leg_price(
420:         raw_price=5.55,
422:         leg_source="rtd",
423:         rtd_option_quotes_repository=repository,
428:     assert price == 5.55
429:     assert price_source == "snapshot"
430:     assert traceability["rtd_quote_found"] is True
431:     assert traceability["price_resolution_status"] == "rtd_asset_mismatch"
432:     assert traceability["rtd_validation_status"] == "error"
433:     assert traceability["rtd_quote_ativo_base"] == "WXYZ"
434:     assert "diverge" in traceability["rtd_validation_message"]
437: def test_snapshot_result_to_payload_preserves_rtd_guardrails_for_valid_quote(tmp_path):
439:         quotes={
443:                 "ultimo_preco": 9.99,
444:                 "source": "rtd_option_quotes",
458:                 "source": "rtd",
462:         spot_price=100.0,
463:         source="rtd",
474:         rtd_option_quotes_repository=repository,
479:     assert leg["price_source"] == "rtd_option_quotes"
480:     assert leg["price_resolution_status"] == "ok"
481:     assert leg["rtd_quote_found"] is True
482:     assert leg["rtd_validation_status"] == "ok"
483:     assert leg["rtd_validation_message"] is None
484:     assert leg["rtd_price_field"] == "ultimo_preco"
485:     assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
486:     assert leg["rtd_quote_ativo_base"] == "ABCD"
489: def test_snapshot_result_to_payload_preserves_rtd_guardrails_when_falling_back_to_snapshot(tmp_path):
501:                 "source": "rtd",
505:         spot_price=100.0,
506:         source="rtd",
517:         rtd_option_quotes_repository=repository,
522:     assert leg["price"] == 5.55
524:     assert leg["price_source"] == "snapshot"
525:     assert leg["price_resolution_status"] == "missing_rtd_quote"
526:     assert leg["rtd_quote_found"] is False
527:     assert leg["rtd_validation_status"] == "error"
529: def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_is_stale():
531:         quotes={
534:                 "ultimo_preco": 9.99,
542:     price, price_source, traceability = _resolve_effective_leg_price(
543:         raw_price=5.55,
545:         leg_source="rtd",
546:         rtd_option_quotes_repository=repository,
550:     assert price == 5.55
551:     assert price_source == "snapshot"
552:     assert traceability["price_resolution_status"] == "stale_rtd_quote"
553:     assert traceability["rtd_quote_found"] is True
554:     assert traceability["rtd_validation_status"] == "warn"
555:     assert "vencida" in traceability["rtd_validation_message"]

---

# ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py

## Classes/funções/testes

- `FakePricingExecutionService`
- `FakePricingExecutionPersistenceService`
- `_create_controlled_app_db`
- `test_execute_pricing_uses_persisted_rtd_option_quote_price`
- `__init__`
- `execute_payload`
- `__init__`
- `persist_execution`

## Linhas relevantes

23:                     "spot_price": float(pricing_payload["spot_price"]),
41:         error_message=None,
86:             CREATE TABLE rtd_analise_robo_legs (
87:                 timestamp TEXT,
113:             INSERT INTO rtd_analise_robo_legs (
114:                 timestamp,
163:                 timestamp TEXT,
191:             CREATE TABLE rtd_analise_robo (
210:             INSERT INTO rtd_analise_robo (
243:             CREATE TABLE rtd_option_quotes (
249:                 ultimo_preco REAL,
269:             INSERT INTO rtd_option_quotes (
275:                 ultimo_preco,
307:                 "rtd_option_quotes",
317: def test_execute_pricing_uses_persisted_rtd_option_quote_price(tmp_path):
345:     assert pricing_payload["spot_price"] == 100.0
348:     # O preço efetivo deve vir de rtd_option_quotes.ultimo_preco = 9.99.
351:     assert leg["price"] == 9.99
353:     assert leg["price_source"] == "rtd_option_quotes"
354:     assert leg["rtd_price_field"] == "ultimo_preco"
355:     assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
356:     assert leg["rtd_quote_ativo_base"] == "ABCD"
357:     assert leg["rtd_price_source"] == "rtd_option_quotes"
358:     assert leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"
359:     assert leg["rtd_price_created_at"] == "2026-06-15T10:01:00"
364:     assert persisted_payload["legs"][0]["price"] == 9.99
366:     assert persisted_payload["legs"][0]["price_source"] == "rtd_option_quotes"
367:     assert persisted_payload["legs"][0]["rtd_price_field"] == "ultimo_preco"
368:     assert persisted_payload["legs"][0]["rtd_quote_codigo_opcao"] == "ABCD11"
369:     assert persisted_payload["legs"][0]["rtd_quote_ativo_base"] == "ABCD"
370:     assert persisted_payload["legs"][0]["rtd_price_source"] == "rtd_option_quotes"
371:     assert persisted_payload["legs"][0]["rtd_price_updated_at"] == "2026-06-15T10:01:00"
372:     assert persisted_payload["legs"][0]["rtd_price_created_at"] == "2026-06-15T10:01:00"

---

# ATT/tests/test_canonical_pricing_facade_rtd_db_path.py

## Classes/funções/testes

- `_create_sqlite_db`
- `_create_rtd_option_quotes_table`
- `test_sqlite_table_exists_returns_false_for_missing_database`
- `test_sqlite_table_exists_detects_existing_table`
- `test_resolve_rtd_option_quotes_db_path_prefers_app_db_when_primary_has_no_table`
- `test_resolve_rtd_option_quotes_db_path_prefers_primary_when_primary_has_table`
- `test_resolve_rtd_option_quotes_db_path_falls_back_to_primary_when_no_candidate_has_table`
- `test_canonical_pricing_facade_initializes_rtd_repository_with_resolved_app_db`

## Linhas relevantes

6:     _resolve_rtd_option_quotes_db_path,
11: def _create_sqlite_db(path: Path) -> None:
17: def _create_rtd_option_quotes_table(path: Path) -> None:
22:             CREATE TABLE IF NOT EXISTS rtd_option_quotes (
25:                 ultimo_preco REAL
35:     assert _sqlite_table_exists(db_path, "rtd_option_quotes") is False
40:     _create_rtd_option_quotes_table(db_path)
42:     assert _sqlite_table_exists(db_path, "rtd_option_quotes") is True
46: def test_resolve_rtd_option_quotes_db_path_prefers_app_db_when_primary_has_no_table(
57:     _create_rtd_option_quotes_table(app_db)
59:     resolved = _resolve_rtd_option_quotes_db_path(primary_db)
64: def test_resolve_rtd_option_quotes_db_path_prefers_primary_when_primary_has_table(
74:     _create_rtd_option_quotes_table(primary_db)
75:     _create_rtd_option_quotes_table(app_db)
77:     resolved = _resolve_rtd_option_quotes_db_path(primary_db)
82: def test_resolve_rtd_option_quotes_db_path_falls_back_to_primary_when_no_candidate_has_table(
95:     resolved = _resolve_rtd_option_quotes_db_path(primary_db)
100: def test_canonical_pricing_facade_initializes_rtd_repository_with_resolved_app_db(
111:     _create_rtd_option_quotes_table(app_db)
116:     assert facade._rtd_option_quotes_db_path == app_db
117:     assert facade._rtd_option_quotes_repository.db_path == app_db

---
