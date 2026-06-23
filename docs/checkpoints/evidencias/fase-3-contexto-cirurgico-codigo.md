# Fase 3 - Contexto cirurgico para alteracao de codigo

Data: Tue Jun 23 19:54:53     2026
Branch: reinicio-normalizacao-idioma-ptbr
HEAD: 545f4e6

## Status git
?? docs/checkpoints/evidencias/fase-3-4-alvos-provaveis-correcao.txt
?? docs/checkpoints/evidencias/fase-3-contexto-cirurgico-codigo.md
?? docs/checkpoints/evidencias/fase-3-correcao-codigo-inventario.txt
?? docs/checkpoints/evidencias/fase-4-correcao-codigo-inventario.txt
?? tools/

## Objetivo tecnico da Fase 3
Encerrar a Fase 3 com alteracao real de codigo:
- cadastro/manual/assistido deve funcionar sem exigir alias_legacy_aba;
- alias_legacy_aba pode existir como compatibilidade, mas nao pode ser chave obrigatoria do fluxo canonical/manual;
- pricing payload nao deve expor alias_legacy_aba como contrato canonical;
- structure_id deve ser preservado do cadastro ate pricing/persistencia;
- fallback manual precisa ser caminho normal para estruturas sem aba legada.

## Ocorrencias criticas em codigo produtivo - alias/aba
UI/components/structure_editor_dialog.py:9:        structure_id: int | None,   # None -> nova estrutura
UI/components/structure_editor_dialog.py:23:    _structure_id   int | None
UI/components/structure_editor_dialog.py:26:    _load_existing()       sem argumento -- usa self._structure_id
UI/components/structure_editor_dialog.py:65:        structure_id: Optional[int] = None,
UI/components/structure_editor_dialog.py:72:        self._structure_id = structure_id
UI/components/structure_editor_dialog.py:75:        self.saved_structure_id = None
UI/components/structure_editor_dialog.py:95:        if structure_id is not None:
UI/components/structure_editor_dialog.py:109:        title = "Nova Estrutura" if self._structure_id is None else "Editar Estrutura"
UI/components/structure_editor_dialog.py:244:        Usa self._structure_id (nao recebe argumento -- compativel com testes
UI/components/structure_editor_dialog.py:247:        data = self._repo.get_structure(self._structure_id)
UI/components/structure_editor_dialog.py:251:                f"Estrutura {self._structure_id} nao encontrada.",
UI/components/structure_editor_dialog.py:259:        self._f_alias.set(data.get("alias_legacy_aba") or "")
UI/components/structure_editor_dialog.py:492:            "alias_legacy_aba": self._f_alias.get().strip() or None,
UI/components/structure_editor_dialog.py:500:            if self._structure_id is None:
UI/components/structure_editor_dialog.py:508:                sid = self._structure_id
UI/components/structure_editor_dialog.py:513:                if getattr(self, "_structure_id", None) is not None:
UI/components/structure_editor_dialog.py:514:                    self.saved_structure_id = int(self._structure_id)
UI/components/structure_editor_dialog.py:516:                    _candidate_saved_structure_id = (
UI/components/structure_editor_dialog.py:517:                        locals().get("created_structure_id")
UI/components/structure_editor_dialog.py:518:                        or locals().get("new_structure_id")
UI/components/structure_editor_dialog.py:519:                        or locals().get("structure_id")
UI/components/structure_editor_dialog.py:524:                    self.saved_structure_id = (
UI/components/structure_editor_dialog.py:525:                        int(_candidate_saved_structure_id)
UI/components/structure_editor_dialog.py:526:                        if _candidate_saved_structure_id is not None
UI/components/structure_editor_dialog.py:530:                self.saved_structure_id = getattr(self, "_structure_id", None)
UI/components/structures_list_panel.py:182:                or term in (r.get("alias_legacy_aba") or "").lower()
UI/components/structures_list_panel.py:197:                    row.get("alias_legacy_aba") or "--",
UI/components/structures_list_panel.py:221:    def _get_full_structure(self, structure_id: int) -> Optional[dict]:
UI/components/structures_list_panel.py:224:            return self._repo.get_structure(structure_id)
UI/components/structures_list_panel.py:287:                "alias_legacy_aba": src.get("alias_legacy_aba"),
UI/components/structures_list_panel.py:293:                 if k not in ("id", "structure_id", "created_at", "updated_at")}
domain/calculation_request.py:139:    structure_id      : PK canônica (INTEGER do DB)
domain/calculation_request.py:143:    alias_legacy_aba  : compatibilidade -- NÃO é chave de cálculo
domain/calculation_request.py:145:    structure_id:     int
domain/calculation_request.py:150:    alias_legacy_aba: Optional[str] = None
domain/calculation_request.py:153:        if not isinstance(self.structure_id, int) or self.structure_id <= 0:
domain/calculation_request.py:155:                f"structure_id deve ser inteiro positivo, recebeu: {self.structure_id!r}"
repositories/structures_repository.py:6:alteracao_42: get_structure_by_alias e get_structure_id_by_alias adicionados.
repositories/structures_repository.py:12:          ensure_audit_schema() cria tabela e indices idx_audit_log_structure_id
repositories/structures_repository.py:63:    alias_legacy_aba = data.get("alias_legacy_aba")
repositories/structures_repository.py:76:    if alias_legacy_aba is not None:
repositories/structures_repository.py:77:        alias_legacy_aba = str(alias_legacy_aba).strip() or None
repositories/structures_repository.py:85:        "alias_legacy_aba": alias_legacy_aba,
repositories/structures_repository.py:194:        self, conn: sqlite3.Connection, structure_id: int
repositories/structures_repository.py:199:                id, structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:203:            WHERE structure_id = ?
repositories/structures_repository.py:206:            (structure_id,),
repositories/structures_repository.py:211:        self, conn: sqlite3.Connection, structure_id: int
repositories/structures_repository.py:215:            (structure_id,),
repositories/structures_repository.py:218:            raise ValueError(f"structure not found: {structure_id}")
repositories/structures_repository.py:236:                structure_id INTEGER NOT NULL,
repositories/structures_repository.py:243:                FOREIGN KEY (structure_id) REFERENCES structures(id)
repositories/structures_repository.py:249:            CREATE INDEX IF NOT EXISTS idx_audit_log_structure_id
repositories/structures_repository.py:250:                ON structure_audit_log (structure_id)
repositories/structures_repository.py:267:        structure_id: int,
repositories/structures_repository.py:284:                    (structure_id, action, changed_by, changed_at,
repositories/structures_repository.py:289:                    structure_id,
repositories/structures_repository.py:315:                    name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:321:                    payload["alias_legacy_aba"], payload["status"],
repositories/structures_repository.py:330:                structure_id=new_id,
repositories/structures_repository.py:369:                    name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:376:                    payload["alias_legacy_aba"],
repositories/structures_repository.py:387:                structure_id=new_id,
repositories/structures_repository.py:402:                        structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:426:                structure_id=new_id,
repositories/structures_repository.py:452:            SELECT id, name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:471:    def get_structure(self, structure_id: int) -> dict[str, Any] | None:
repositories/structures_repository.py:476:                SELECT id, name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:480:                (structure_id,),
repositories/structures_repository.py:487:            structure["legs"] = self._fetch_legs(conn, structure_id)
repositories/structures_repository.py:496:    def update_structure(self, structure_id: int, data: dict[str, Any]) -> None:
repositories/structures_repository.py:497:        current = self.get_structure(structure_id)
repositories/structures_repository.py:499:            raise ValueError(f"structure not found: {structure_id}")
repositories/structures_repository.py:507:            "alias_legacy_aba": data.get("alias_legacy_aba", current["alias_legacy_aba"]),
repositories/structures_repository.py:519:                SET name=?, underlying_asset=?, alias_legacy_aba=?,
repositories/structures_repository.py:525:                    payload["alias_legacy_aba"], payload["status"],
repositories/structures_repository.py:526:                    payload["notes"], now, structure_id,
repositories/structures_repository.py:533:                structure_id=structure_id,
repositories/structures_repository.py:536:                after={**payload, "id": structure_id, "updated_at": now},
repositories/structures_repository.py:550:    def archive_structure(self, structure_id: int) -> None:
repositories/structures_repository.py:551:        current = self.get_structure(structure_id)
repositories/structures_repository.py:553:            raise ValueError(f"structure not found: {structure_id}")
repositories/structures_repository.py:560:            self._ensure_structure_exists(conn, structure_id)
repositories/structures_repository.py:563:                ("archived", now, structure_id),
repositories/structures_repository.py:569:                structure_id=structure_id,
repositories/structures_repository.py:586:    def add_leg(self, structure_id: int, leg_data: dict[str, Any]) -> int:
repositories/structures_repository.py:592:            self._ensure_structure_exists(conn, structure_id)
repositories/structures_repository.py:597:                    structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:603:                    structure_id, leg["position_side"], leg["option_type"],
repositories/structures_repository.py:613:                (now, structure_id),
repositories/structures_repository.py:619:                structure_id=structure_id,
repositories/structures_repository.py:621:                after={**leg, "id": leg_id, "structure_id": structure_id},
repositories/structures_repository.py:633:        self, structure_id: int, legs: list[dict[str, Any]]
repositories/structures_repository.py:640:            self._ensure_structure_exists(conn, structure_id)
repositories/structures_repository.py:643:                "DELETE FROM structure_legs WHERE structure_id=?",
repositories/structures_repository.py:644:                (structure_id,),
repositories/structures_repository.py:651:                        structure_id, position_side, option_type, symbol,
repositories/structures_repository.py:657:                        structure_id, leg["position_side"], leg["option_type"],
repositories/structures_repository.py:666:                (now, structure_id),
repositories/structures_repository.py:672:                structure_id=structure_id,
repositories/structures_repository.py:688:    def count_legs(self, structure_id: int) -> int:
repositories/structures_repository.py:692:                "SELECT COUNT(*) AS n FROM structure_legs WHERE structure_id=?",
repositories/structures_repository.py:693:                (structure_id,),
repositories/structures_repository.py:713:                SELECT id, name, underlying_asset, alias_legacy_aba,
repositories/structures_repository.py:716:                WHERE alias_legacy_aba = ? AND status = 'active'
repositories/structures_repository.py:731:    def get_structure_id_by_alias(self, alias: str) -> int | None:
repositories/structures_repository.py:743:        structure_id: int,
repositories/structures_repository.py:754:                SELECT id, structure_id, action, changed_by,
repositories/structures_repository.py:757:                WHERE structure_id = ?
repositories/structures_repository.py:761:                (structure_id, limit),
repositories/structures_repository.py:781:                    SELECT id, structure_id, action, changed_by,
repositories/structures_repository.py:793:                    SELECT id, structure_id, action, changed_by,
services/calculation_orchestrator.py:86:        structure_id=int(structure_row["id"]),
services/calculation_orchestrator.py:90:        alias_legacy_aba=structure_row.get("alias_legacy_aba"),
services/calculation_orchestrator.py:115:    """alteracao_47: multiplier usa leg.multiplier com fallback 1.0."""
services/calculation_orchestrator.py:133:            "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:218:        "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:279:            structure_id=int(structure_dict["structure_id"]),
services/calculation_orchestrator.py:282:            alias_legacy_aba=structure_dict.get("alias_legacy_aba"),
services/calculation_orchestrator.py:322:                "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:400:            "structure_id":     request.structure.structure_id,
services/calculation_orchestrator.py:410:        structure_id: int,
services/calculation_orchestrator.py:433:        structure = self._structures_repo.get_structure(structure_id)
services/calculation_orchestrator.py:436:                f"Estrutura nao encontrada: structure_id={structure_id}"
services/calculation_orchestrator.py:441:                f"structure_id={structure_id}"
services/calculation_orchestrator.py:447:                f"Estrutura sem legs: structure_id={structure_id}"
services/calculation_orchestrator.py:464:            "structure_id":    structure["id"],
services/calculation_orchestrator.py:467:            "alias_legacy_aba": structure.get("alias_legacy_aba"),
services/calculation_orchestrator.py:500:        structure_id: int,
services/calculation_orchestrator.py:506:        Retorna dict com chaves: structure_id, payoff, decision.
services/calculation_orchestrator.py:509:            structure_id=structure_id,
services/calculation_orchestrator.py:515:            "structure_id": structure_id,
services/canonical_input_service.py:29:from services.legacy_robo_legs_fallback import LegacyRoboLegsFallback
services/canonical_input_service.py:45:        enable_legacy_legs_fallback: bool = True,
services/canonical_input_service.py:46:        allow_legacy_name_fallback: bool = False,
services/canonical_input_service.py:53:        self.enable_legacy_legs_fallback = enable_legacy_legs_fallback
services/canonical_input_service.py:54:        self.allow_legacy_name_fallback  = allow_legacy_name_fallback
services/canonical_input_service.py:68:        # LegacyRoboLegsFallback sempre inicializado, independente da origem do robo_legs_service
services/canonical_input_service.py:69:        self.legacy_robo_legs_fallback = LegacyRoboLegsFallback(
services/canonical_input_service.py:71:            allow_name_fallback=self.allow_legacy_name_fallback,
services/canonical_input_service.py:91:        structure_id: int,
services/canonical_input_service.py:94:        structure = self.repository.get_structure(structure_id)
services/canonical_input_service.py:96:            raise ValueError(f"structure not found: {structure_id}")
services/canonical_input_service.py:102:            "alias_legacy_aba":  self._clean_text(structure.get("alias_legacy_aba")),
services/canonical_input_service.py:150:        Se o selector estiver injetado E alias_legacy_aba existir, substitui as
services/canonical_input_service.py:154:        aba              = structure.get("alias_legacy_aba")
services/canonical_input_service.py:261:    # Enriquecimento de legs canônicas / fallback (inalterado do alteracao_13)
services/canonical_input_service.py:268:        legacy_aba: str | None = None,
services/canonical_input_service.py:270:        fallback_reason: str | None = None,
services/canonical_input_service.py:274:        if legacy_aba        is not None: meta["legacy_aba"]        = legacy_aba
services/canonical_input_service.py:276:        if fallback_reason   is not None: meta["fallback_reason"]   = fallback_reason
services/canonical_input_service.py:284:        fallback_reason: str | None = None,
services/canonical_input_service.py:288:            self._build_meta(legs_source=legs_source, fallback_reason=fallback_reason),
services/canonical_input_service.py:305:        if not self.enable_legacy_legs_fallback:
services/canonical_input_service.py:310:                fallback_reason="legacy_fallback_disabled",
services/canonical_input_service.py:313:        fallback_legs, fallback_meta = self.legacy_robo_legs_fallback.load(
services/canonical_input_service.py:318:        if fallback_legs:
services/canonical_input_service.py:320:                {**structure, "legs": fallback_legs},
services/canonical_input_service.py:322:                    "legs_source":       fallback_meta.get("legs_source", "legacy_fallback"),
services/canonical_input_service.py:323:                    "legacy_timestamp":  fallback_meta.get("legacy_timestamp"),
services/canonical_input_service.py:324:                    "legacy_aba":        fallback_meta.get("legacy_aba"),
services/canonical_input_service.py:325:                    "legacy_key_source": fallback_meta.get("legacy_key_source"),
services/canonical_input_service.py:326:                    "fallback_reason":   fallback_meta.get("fallback_reason"),
services/canonical_input_service.py:335:                fallback_reason="canonical_legs_retained_after_empty_fallback",
services/canonical_input_service.py:342:            fallback_reason=(
services/canonical_input_service.py:343:                fallback_meta.get("fallback_reason") if fallback_meta else "no_legs_available"
services/canonical_pricing_facade.py:9:  C6: _get_alias_legacy_aba() substituído por _get_structure_info() --
services/canonical_pricing_facade.py:10:      busca alias_legacy_aba E underlying_asset em uma única query.
services/canonical_pricing_facade.py:18:  C2: alias_legacy_aba buscado via query antes de chamar o selector
services/canonical_pricing_facade.py:43:#  C6: substitui _get_alias_legacy_aba -- busca aba + underlying em 1 query 
services/canonical_pricing_facade.py:45:def _get_structure_info(structure_id: int, db_path: Path) -> tuple[str, str]:
services/canonical_pricing_facade.py:47:    Retorna (alias_legacy_aba, underlying_asset) para a estrutura.
services/canonical_pricing_facade.py:51:      - alias_legacy_aba for nulo (sem aba legada mapeada)
services/canonical_pricing_facade.py:56:            "SELECT alias_legacy_aba, underlying_asset FROM structures WHERE id = ?",
services/canonical_pricing_facade.py:57:            (structure_id,),
services/canonical_pricing_facade.py:61:        raise ValueError(f"structure not found: {structure_id}")
services/canonical_pricing_facade.py:63:    aba = row["alias_legacy_aba"]
services/canonical_pricing_facade.py:65:        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")
services/canonical_pricing_facade.py:237:    structure_id: int,
services/canonical_pricing_facade.py:305:        "structure_id":     structure_id,
services/canonical_pricing_facade.py:325:        structure_id
services/canonical_pricing_facade.py:326:             alias_legacy_aba + underlying_asset  (query em structures)
services/canonical_pricing_facade.py:353:        structure_id: int,
services/canonical_pricing_facade.py:362:            #   structures.alias_legacy_aba preenchido -> MarketSnapshotSelector.
services/canonical_pricing_facade.py:365:            #   structures.alias_legacy_aba NULL -> PricingInputService.build_pricing_payload().
services/canonical_pricing_facade.py:370:                    structure_id,
services/canonical_pricing_facade.py:378:                    structure_id=structure_id,
services/canonical_pricing_facade.py:387:                if "alias_legacy_aba is null" not in message:
services/canonical_pricing_facade.py:396:                    pricing_payload = pricing_input_service.build_pricing_payload(
services/canonical_pricing_facade.py:397:                        structure_id=structure_id,
services/canonical_pricing_facade.py:401:                    pricing_payload = pricing_input_service.build_pricing_payload(
services/canonical_pricing_facade.py:402:                        structure_id=structure_id,
services/canonical_pricing_facade.py:407:                        "PricingInputService.build_pricing_payload() retornou payload inválido"
services/canonical_pricing_facade.py:410:                pricing_payload.setdefault("structure_id", structure_id)
services/canonical_pricing_facade.py:421:                meta.setdefault("alias_legacy_aba", None)
services/canonical_pricing_facade.py:422:                meta.setdefault("fallback_reason", message.strip())
services/pricing_input_service.py:14:    def build_pricing_payload(
services/pricing_input_service.py:16:        structure_id: int,
services/pricing_input_service.py:20:            structure_id=structure_id,
services/pricing_input_service.py:24:        return self.build_pricing_payload_from_canonical_input(canonical_input)
services/pricing_input_service.py:26:    def build_pricing_payload_from_canonical_input(
services/pricing_payload_adapter.py:53:        "structure_id": structure["structure_id"],
services/structure_input_mapper.py:92:        "structure_id": structure["id"],

## Ocorrencias criticas em testes Fase 3
ATT/tests/test_canonical_input_service.py:3:from services.canonical_input_service import CanonicalInputService
ATT/tests/test_canonical_input_service.py:67:class CanonicalInputServiceTests(unittest.TestCase):
ATT/tests/test_canonical_input_service.py:68:    def test_should_always_prefer_canonical_legs_when_structure_already_has_legs(self):
ATT/tests/test_canonical_input_service.py:73:            "alias_legacy_aba": "BOVA11",
ATT/tests/test_canonical_input_service.py:88:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:95:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:104:        self.assertEqual(result["meta"]["legs_source"], "canonical")
ATT/tests/test_canonical_input_service.py:108:        self.assertNotIn("alias_legacy_aba", result["structure"])
ATT/tests/test_canonical_input_service.py:110:    def test_should_use_legacy_robo_only_when_no_canonical_legs_exist(self):
ATT/tests/test_canonical_input_service.py:115:            "alias_legacy_aba": "BOVA11",
ATT/tests/test_canonical_input_service.py:119:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:148:        self.assertEqual(result["meta"]["legacy_key_source"], "alias_legacy_aba")
ATT/tests/test_canonical_input_service.py:151:        self.assertNotIn("alias_legacy_aba", result["structure"])
ATT/tests/test_canonical_input_service.py:153:    def test_should_return_empty_when_no_canonical_legs_and_fallback_disabled(self):
ATT/tests/test_canonical_input_service.py:158:            "alias_legacy_aba": "BOVA11",
ATT/tests/test_canonical_input_service.py:162:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:180:        self.assertNotIn("alias_legacy_aba", result["structure"])
ATT/tests/test_canonical_input_service.py:188:            "alias_legacy_aba": "BOVA11",
ATT/tests/test_canonical_input_service.py:192:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:195:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:218:            "alias_legacy_aba": "BOVA11",
ATT/tests/test_canonical_input_service.py:255:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:259:            prefer_canonical_legs=True,
ATT/tests/test_canonical_input_service.py:288:            "alias_legacy_aba": "BOVA11",
ATT/tests/test_canonical_input_service.py:292:        service = CanonicalInputService(
ATT/tests/test_canonical_input_service.py:296:            prefer_canonical_legs=True,
ATT/tests/test_canonical_pricing_facade.py:6:from services.canonical_pricing_facade import _snapshot_result_to_payload
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:1:import services.canonical_pricing_facade as facade_module
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:8:    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:61:def test_facade_falls_back_to_pricing_input_service_when_alias_legacy_aba_is_null(monkeypatch, tmp_path):
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:63:        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:82:    facade = facade_module.CanonicalPricingFacade(
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:96:    assert response["pricing_payload"]["meta"]["snapshot_source"] == "canonical_manual_without_alias"
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:97:    assert response["pricing_payload"]["meta"]["alias_legacy_aba"] is None
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py:98:    assert "alias_legacy_aba is null" in response["pricing_payload"]["meta"]["fallback_reason"]
ATT/tests/test_pricing_input_service.py:6:class FakeCanonicalInputService:
ATT/tests/test_pricing_input_service.py:7:    def __init__(self, canonical_input=None, error=None):
ATT/tests/test_pricing_input_service.py:8:        self.canonical_input = canonical_input
ATT/tests/test_pricing_input_service.py:23:        return self.canonical_input
ATT/tests/test_pricing_input_service.py:26:def test_build_pricing_payload_calls_canonical_input_service(monkeypatch):
ATT/tests/test_pricing_input_service.py:27:    canonical_input = {
ATT/tests/test_pricing_input_service.py:43:    fake_canonical_service = FakeCanonicalInputService(canonical_input)
ATT/tests/test_pricing_input_service.py:57:    service = PricingInputService(canonical_input_service=fake_canonical_service)
ATT/tests/test_pricing_input_service.py:59:    result = service.build_pricing_payload(
ATT/tests/test_pricing_input_service.py:64:    assert fake_canonical_service.calls == [
ATT/tests/test_pricing_input_service.py:77:def test_build_pricing_payload_from_canonical_input_delegates_to_adapter(monkeypatch):
ATT/tests/test_pricing_input_service.py:78:    canonical_input = {
ATT/tests/test_pricing_input_service.py:94:    service = PricingInputService(canonical_input_service=None)
ATT/tests/test_pricing_input_service.py:96:    result = service.build_pricing_payload_from_canonical_input(canonical_input)
ATT/tests/test_pricing_input_service.py:98:    assert calls == [canonical_input]
ATT/tests/test_pricing_input_service.py:102:def test_build_pricing_payload_passes_none_reference_date(monkeypatch):
ATT/tests/test_pricing_input_service.py:103:    canonical_input = {
ATT/tests/test_pricing_input_service.py:108:    fake_canonical_service = FakeCanonicalInputService(canonical_input)
ATT/tests/test_pricing_input_service.py:121:    service = PricingInputService(canonical_input_service=fake_canonical_service)
ATT/tests/test_pricing_input_service.py:123:    result = service.build_pricing_payload(structure_id=321)
ATT/tests/test_pricing_input_service.py:125:    assert fake_canonical_service.calls == [
ATT/tests/test_pricing_input_service.py:137:def test_build_pricing_payload_propagates_canonical_input_service_error(monkeypatch):
ATT/tests/test_pricing_input_service.py:138:    fake_canonical_service = FakeCanonicalInputService(
ATT/tests/test_pricing_input_service.py:153:    service = PricingInputService(canonical_input_service=fake_canonical_service)
ATT/tests/test_pricing_input_service.py:156:        service.build_pricing_payload(structure_id=404)
ATT/tests/test_pricing_input_service.py:158:    assert fake_canonical_service.calls == [
ATT/tests/test_pricing_input_service.py:167:def test_build_pricing_payload_from_canonical_input_propagates_adapter_error(monkeypatch):
ATT/tests/test_pricing_input_service.py:168:    canonical_input = {
ATT/tests/test_pricing_input_service.py:174:        raise ValueError("invalid canonical input")
ATT/tests/test_pricing_input_service.py:181:    service = PricingInputService(canonical_input_service=None)
ATT/tests/test_pricing_input_service.py:183:    with pytest.raises(ValueError, match="invalid canonical input"):
ATT/tests/test_pricing_input_service.py:184:        service.build_pricing_payload_from_canonical_input(canonical_input)
ATT/tests/test_pricing_payload_adapter.py:7:    def test_should_not_include_alias_legacy_aba_in_pricing_payload(self):
ATT/tests/test_pricing_payload_adapter.py:8:        canonical_input = {
ATT/tests/test_pricing_payload_adapter.py:13:                "alias_legacy_aba": "BOVA11",
ATT/tests/test_pricing_payload_adapter.py:35:        payload = to_pricing_payload(canonical_input)
ATT/tests/test_pricing_payload_adapter.py:39:        self.assertNotIn("alias_legacy_aba", payload)
ATT/tests/test_pricing_payload_adapter.py:42:        canonical_input = {
ATT/tests/test_pricing_payload_adapter.py:68:        payload = to_pricing_payload(canonical_input)
ATT/tests/test_pricing_payload_adapter.py:89:                canonical_input = {
ATT/tests/test_pricing_payload_adapter.py:115:                payload = to_pricing_payload(canonical_input)
ATT/tests/test_structure_editor_dialog.py:154:            "alias_legacy_aba": "BOVA11", "status": "active",
ATT/tests/test_structure_editor_dialog.py:172:            "alias_legacy_aba": None, "status": "active", "notes": None,
ATT/tests/test_structure_editor_dialog.py:239:        self.assertEqual(structure_arg["alias_legacy_aba"], "PRIO3")
ATT/tests/test_structure_editor_dialog.py:323:            "alias_legacy_aba": None, "status": "active", "notes": None,
ATT/tests/test_structure_input_mapper.py:4:def test_to_structure_input_should_not_expose_alias_legacy_aba():
ATT/tests/test_structure_input_mapper.py:9:        "alias_legacy_aba": "BOVA11",
ATT/tests/test_structure_input_mapper.py:29:    assert "alias_legacy_aba" not in result
ATT/tests/test_structure_market_input_assembler.py:12:            "alias_legacy_aba": "BOVA11",

## Arquivos completos com numeracao - Fase 3

## FILE: services/canonical_pricing_facade.py
```python
     1	# services/canonical_pricing_facade.py
     2	"""
     3	alteracao_17 -- Fachada canônica corrigida.
     4	alteracao_21 -- Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado
     5	           no PricingExecutionPersistenceService.
     6	alteracao_41 -- Corrige underlying_asset no pricing_payload.
     7	
     8	Correções alteracao_41:
     9	  C6: _get_alias_legacy_aba() substituído por _get_structure_info() --
    10	      busca alias_legacy_aba E underlying_asset em uma única query.
    11	  C7: _snapshot_result_to_payload() recebe underlying_asset explícito --
    12	      elimina uso de selection_result.aba como underlying_asset
    13	      (aba legada  ativo subjacente real).
    14	  C8: execute_pricing() passa underlying_asset para o payload builder.
    15	
    16	Correções anteriores mantidas:
    17	  C1: sel.select(aba=...) -- parâmetro correto
    18	  C2: alias_legacy_aba buscado via query antes de chamar o selector
    19	  C3: orquestração direta repo  selector  execute_payload()
    20	  C4: engine_result extraído do wrapper antes de passar ao persister
    21	  C5: DerivedPayoffPersistence injetado como payoff_persistence_port
    22	"""
    23	from __future__ import annotations
    24	
    25	
    26	import sqlite3
    27	import time
    28	from datetime import datetime
    29	from pathlib import Path
    30	from typing import Any
    31	
    32	from repositories.market_snapshot_repository import MarketSnapshotRepository
    33	from repositories.system_snapshots_repository import SystemSnapshotsRepository
    34	from services.derived_payoff_persistence import DerivedPayoffPersistence
    35	from services.market_snapshot_selector import MarketSnapshotSelector
    36	from services.pricing_execution_persistence_service import PricingExecutionPersistenceService
    37	from services.pricing_execution_service import PricingExecutionService
    38	from services.pricing_input_service import PricingInputService
    39	
    40	_DEFAULT_DB = Path("dados/app.db")
    41	
    42	
    43	#  C6: substitui _get_alias_legacy_aba -- busca aba + underlying em 1 query 
    44	
    45	def _get_structure_info(structure_id: int, db_path: Path) -> tuple[str, str]:
    46	    """
    47	    Retorna (alias_legacy_aba, underlying_asset) para a estrutura.
    48	
    49	    Raises ValueError se:
    50	      - estrutura não existir
    51	      - alias_legacy_aba for nulo (sem aba legada mapeada)
    52	    """
    53	    with sqlite3.connect(str(db_path)) as conn:
    54	        conn.row_factory = sqlite3.Row
    55	        row = conn.execute(
    56	            "SELECT alias_legacy_aba, underlying_asset FROM structures WHERE id = ?",
    57	            (structure_id,),
    58	        ).fetchone()
    59	
    60	    if row is None:
    61	        raise ValueError(f"structure not found: {structure_id}")
    62	
    63	    aba = row["alias_legacy_aba"]
    64	    if not aba:
    65	        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")
    66	
    67	    underlying_asset = row["underlying_asset"]  # NOT NULL -- sempre presente
    68	
    69	    return aba, underlying_asset
    70	
    71	
    72	#  C7: recebe underlying_asset explícito -- não usa selection_result.aba 
    73	
    74	
    75	
    76	def _to_float(value: Any, default: float = 0.0) -> float:
    77	    try:
    78	        if value is None or value == "":
    79	            return default
    80	
    81	        if isinstance(value, str):
    82	            text = value.strip()
    83	            if not text:
    84	                return default
    85	
    86	            text = text.replace("R$", "").replace("$", "").strip()
    87	
    88	            # Remove espaços internos comuns em valores monetários.
    89	            text = text.replace(" ", "")
    90	
    91	            # Formatos comuns vindos de RTD/planilha:
    92	            #   BR: "1.234,56" -> "1234.56"
    93	            #   US: "1,234.56" -> "1234.56"
    94	            #   BR simples: "124,66" -> "124.66"
    95	            if "," in text and "." in text:
    96	                if text.rfind(",") > text.rfind("."):
    97	                    text = text.replace(".", "").replace(",", ".")
    98	                else:
    99	                    text = text.replace(",", "")
   100	            elif "," in text:
   101	                text = text.replace(",", ".")
   102	
   103	            return float(text)
   104	
   105	        return float(value)
   106	    except Exception:
   107	        return default
   108	
   109	
   110	def _normalize_expiration_date(value: Any) -> str | None:
   111	    if not value:
   112	        return None
   113	
   114	    text = str(value).strip()
   115	
   116	    formats = [
   117	        "%m/%d/%Y %H:%M",
   118	        "%m/%d/%Y %H:%M:%S",
   119	        "%Y-%m-%d",
   120	        "%Y-%m-%dT%H:%M:%S",
   121	    ]
   122	
   123	    for fmt in formats:
   124	        try:
   125	            return datetime.strptime(text, fmt).date().isoformat()
   126	        except ValueError:
   127	            pass
   128	
   129	    return text
   130	
   131	
   132	def _pick(data: dict[str, Any], *names: str) -> Any:
   133	    for name in names:
   134	        value = data.get(name)
   135	        if value is not None:
   136	            return value
   137	    return None
   138	
   139	
   140	def _quote_ident(name: str) -> str:
   141	    return '"' + name.replace('"', '""') + '"'
   142	
   143	
   144	def _lookup_spot_price(db_path: Path, underlying_asset: str) -> float:
   145	    """
   146	    Procura spot positivo no app.db.
   147	
   148	    Caso confirmado:
   149	      estrutura SMAL11 possui spot positivo disponível na base canônica/staging.
   150	      spot observado = 124.66
   151	    """
   152	    if not underlying_asset:
   153	        return 0.0
   154	
   155	    symbol_candidates = {
   156	        "aba",
   157	        "ativo",
   158	        "asset",
   159	        "symbol",
   160	        "ticker",
   161	        "underlying_asset",
   162	        "codigo",
   163	        "papel",
   164	    }
   165	
   166	    price_candidates = {
   167	        "spot",
   168	        "spot_price",
   169	        "underlying_price",
   170	        "last_price",
   171	        "price",
   172	        "preco",
   173	        "preco_atual",
   174	        "valor",
   175	        "cotacao",
   176	        "ultimo",
   177	        "fechamento",
   178	        "close",
   179	    }
   180	
   181	    try:
   182	        with sqlite3.connect(str(db_path)) as conn:
   183	            tables = conn.execute(
   184	                "SELECT name FROM sqlite_master WHERE type = 'table'"
   185	            ).fetchall()
   186	
   187	            for (table_name,) in tables:
   188	                columns_info = conn.execute(
   189	                    f"PRAGMA table_info({_quote_ident(table_name)})"
   190	                ).fetchall()
   191	
   192	                columns = [row[1] for row in columns_info]
   193	                lower_to_real = {col.lower(): col for col in columns}
   194	
   195	                symbol_cols = [
   196	                    lower_to_real[name]
   197	                    for name in symbol_candidates
   198	                    if name in lower_to_real
   199	                ]
   200	
   201	                price_cols = [
   202	                    lower_to_real[name]
   203	                    for name in price_candidates
   204	                    if name in lower_to_real
   205	                ]
   206	
   207	                if not symbol_cols or not price_cols:
   208	                    continue
   209	
   210	                for symbol_col in symbol_cols:
   211	                    for price_col in price_cols:
   212	                        query = (
   213	                            f"SELECT {_quote_ident(price_col)} "
   214	                            f"FROM {_quote_ident(table_name)} "
   215	                            f"WHERE UPPER(CAST({_quote_ident(symbol_col)} AS TEXT)) = UPPER(?) "
   216	                            f"AND {_quote_ident(price_col)} IS NOT NULL "
   217	                            f"LIMIT 20"
   218	                        )
   219	
   220	                        try:
   221	                            rows = conn.execute(query, (underlying_asset,)).fetchall()
   222	                        except Exception:
   223	                            continue
   224	
   225	                        for row in rows:
   226	                            price = _to_float(row[0], 0.0)
   227	                            if price > 0:
   228	                                return price
   229	    except Exception:
   230	        return 0.0
   231	
   232	    return 0.0
   233	
   234	
   235	def _snapshot_result_to_payload(
   236	    selection_result: Any,
   237	    structure_id: int,
   238	    underlying_asset: str,
   239	    reference_date: str | None,
   240	    db_path: Path,
   241	) -> dict[str, Any]:
   242	    legs_data = []
   243	
   244	    for leg in selection_result.legs:
   245	        d = leg if isinstance(leg, dict) else vars(leg)
   246	
   247	        quantity = _to_float(_pick(d, "quantity", "quant"), 0.0)
   248	
   249	        raw_price = _pick(d, "premium", "price", "valor_executado")
   250	        raw_asset = _pick(d, "symbol", "asset", "ativo")
   251	        raw_expiry = _pick(d, "expiration_date", "expiry", "vencimento")
   252	
   253	        side = _pick(d, "side", "position_side")
   254	        if not side:
   255	            side = "SHORT" if quantity < 0 else "LONG"
   256	
   257	        canonical_leg = {
   258	            # campos originais/compatíveis
   259	            "quantity":    quantity,
   260	            "price":       _to_float(raw_price, 0.0),
   261	            "asset":       raw_asset,
   262	            "option_type": _pick(d, "option_type", "call_put"),
   263	            "strike":      _to_float(_pick(d, "strike"), 0.0),
   264	            "expiry":      raw_expiry,
   265	            "iv":          _pick(d, "iv"),
   266	            "delta":       _pick(d, "delta"),
   267	            "gamma":       _pick(d, "gamma"),
   268	            "theta":       _pick(d, "theta"),
   269	            "vega":        _pick(d, "vega"),
   270	            "source":      str(_pick(d, "source")),
   271	
   272	            # campos canônicos esperados pelo fluxo pricing/payoff
   273	            "symbol":          raw_asset,
   274	            "premium":         _to_float(raw_price, 0.0),
   275	            "expiration_date": _normalize_expiration_date(raw_expiry),
   276	            "multiplier":      1.0,
   277	            "side":            str(side).upper(),
   278	            "position_side":   str(side).upper(),
   279	        }
   280	
   281	        legs_data.append(canonical_leg)
   282	
   283	    spot = (
   284	        getattr(selection_result, "spot_price", None)
   285	        or getattr(selection_result, "spot", None)
   286	        or getattr(selection_result, "underlying_price", None)
   287	        or getattr(selection_result, "last_price", None)
   288	    )
   289	
   290	    spot_price = _to_float(spot, 0.0)
   291	
   292	    if spot_price <= 0:
   293	        spot_price = _lookup_spot_price(
   294	            db_path=db_path,
   295	            underlying_asset=underlying_asset,
   296	        )
   297	
   298	    if spot_price <= 0:
   299	        raise ValueError(
   300	            f"spot_price inválido ou ausente para underlying_asset={underlying_asset}. "
   301	            "Não persistir execução OK com spot_price <= 0."
   302	        )
   303	
   304	    return {
   305	        "structure_id":     structure_id,
   306	        "underlying_asset": underlying_asset,
   307	        "reference_date":   reference_date,
   308	        "spot_price":       spot_price,
   309	        "interest_rate":    0.0,
   310	        "volatility":       0.0,
   311	        "legs":             legs_data,
   312	        "meta": {
   313	            "snapshot_source":  str(selection_result.source),
   314	            "snapshot_aba":     selection_result.aba,
   315	            "manual_overrides": getattr(selection_result, "manual_overrides", None) or [],
   316	            "legs_count":       len(legs_data),
   317	        },
   318	    }
   319	
   320	
   321	class CanonicalPricingFacade:
   322	    """
   323	    Orquestra o pipeline canônico ponta a ponta:
   324	
   325	        structure_id
   326	             alias_legacy_aba + underlying_asset  (query em structures)
   327	                     MarketSnapshotSelector.select(aba=...)
   328	                             pricing_payload  (underlying_asset = ativo real)
   329	                                     PricingExecutionService.execute_payload()
   330	                                             PricingExecutionPersistenceService.persist()
   331	                                                     DerivedPayoffPersistence.persist()
   332	                                                             derived.db
   333	    """
   334	
   335	    def __init__(
   336	        self,
   337	        db_path: Path | str = _DEFAULT_DB,
   338	        pricing_execution_service: PricingExecutionService | None = None,
   339	        persistence_service: PricingExecutionPersistenceService | None = None,
   340	    ) -> None:
   341	        self._db_path  = Path(db_path)
   342	        self._repo     = MarketSnapshotRepository(db_path=self._db_path)
   343	        self._selector = MarketSnapshotSelector(repository=self._repo)
   344	        self._engine   = pricing_execution_service or PricingExecutionService()
   345	
   346	        self._persister = persistence_service or PricingExecutionPersistenceService(
   347	            payoff_persistence_port=DerivedPayoffPersistence(),
   348	            system_snapshots_repository=SystemSnapshotsRepository(db_path=self._db_path),
   349	        )
   350	
   351	    def execute_pricing(
   352	        self,
   353	        structure_id: int,
   354	        reference_date: str | None = None,
   355	    ) -> dict[str, Any]:
   356	        started_at = time.perf_counter()
   357	
   358	        try:
   359	            # 1. Monta pricing_payload.
   360	            #
   361	            # Caminho A - legado/captura:
   362	            #   structures.alias_legacy_aba preenchido -> MarketSnapshotSelector.
   363	            #
   364	            # Caminho B - manual canônico:
   365	            #   structures.alias_legacy_aba NULL -> PricingInputService.build_pricing_payload().
   366	            #
   367	            # O caminho B corrige estruturas cadastradas manualmente pela UI.
   368	            try:
   369	                aba, underlying_asset = _get_structure_info(
   370	                    structure_id,
   371	                    self._db_path,
   372	                )
   373	
   374	                selection = self._selector.select(aba=aba)
   375	
   376	                pricing_payload = _snapshot_result_to_payload(
   377	                    selection_result=selection,
   378	                    structure_id=structure_id,
   379	                    underlying_asset=underlying_asset,
   380	                    reference_date=reference_date,
   381	                    db_path=self._db_path,
   382	                )
   383	
   384	            except ValueError as exc:
   385	                message = str(exc)
   386	
   387	                if "alias_legacy_aba is null" not in message:
   388	                    raise
   389	
   390	                try:
   391	                    pricing_input_service = PricingInputService(db_path=self._db_path)
   392	                except TypeError:
   393	                    pricing_input_service = PricingInputService()
   394	
   395	                try:
   396	                    pricing_payload = pricing_input_service.build_pricing_payload(
   397	                        structure_id=structure_id,
   398	                        reference_date=reference_date,
   399	                    )
   400	                except TypeError:
   401	                    pricing_payload = pricing_input_service.build_pricing_payload(
   402	                        structure_id=structure_id,
   403	                    )
   404	
   405	                if not isinstance(pricing_payload, dict):
   406	                    raise ValueError(
   407	                        "PricingInputService.build_pricing_payload() retornou payload inválido"
   408	                    )
   409	
   410	                pricing_payload.setdefault("structure_id", structure_id)
   411	
   412	                if reference_date is not None:
   413	                    pricing_payload.setdefault("reference_date", reference_date)
   414	
   415	                meta = pricing_payload.get("meta")
   416	                if not isinstance(meta, dict):
   417	                    meta = {}
   418	                    pricing_payload["meta"] = meta
   419	
   420	                meta.setdefault("snapshot_source", "canonical_manual_without_alias")
   421	                meta.setdefault("alias_legacy_aba", None)
   422	                meta.setdefault("fallback_reason", message.strip())
   423	
   424	            # 2. Executa engine
   425	            execution_result = self._engine.execute_payload(
   426	                pricing_payload=pricing_payload,
   427	            )
   428	
   429	            # C4: extrai dict interno do wrapper
   430	            engine_result = execution_result.get("result", execution_result)
   431	
   432	            duration_ms = int((time.perf_counter() - started_at) * 1000)
   433	
   434	            # 3. Persiste app.db + derived.db via port
   435	            persisted = self._persister.persist_execution(
   436	                pricing_payload=pricing_payload,
   437	                result=engine_result,
   438	                duration_ms=duration_ms,
   439	                error_message=None,
   440	            )
   441	
   442	            return {
   443	                "status":          "ok",
   444	                "canonical_input": pricing_payload,
   445	                "pricing_payload": pricing_payload,
   446	                "result":          execution_result,
   447	                "persisted":       persisted,
   448	                "meta":            pricing_payload.get("meta", {}),
   449	                "duration_ms":     duration_ms,
   450	            }
   451	
   452	        except Exception as exc:
   453	            duration_ms   = int((time.perf_counter() - started_at) * 1000)
   454	            error_message = str(exc)
   455	
   456	            try:
   457	                self._persister.persist_execution(
   458	                    pricing_payload=None,
   459	                    result={"engine": "payoff_pricing_engine", "status": "error", "error_message": error_message},
   460	                    duration_ms=duration_ms,
   461	                    error_message=error_message,
   462	                )
   463	            except Exception:
   464	                pass
   465	
   466	            return {
   467	                "status":          "error",
   468	                "canonical_input": None,
   469	                "pricing_payload": None,
   470	                "result":          None,
   471	                "persisted":       None,
   472	                "meta":            {},
   473	                "duration_ms":     duration_ms,
   474	                "error_message":   error_message,
   475	            }
```

## FILE: services/canonical_input_service.py
```python
     1	from __future__ import annotations
     2	from domain.structure_metrics import compute_structure_metrics_from_canonical_input
     3	
     4	# services/canonical_input_service.py
     5	"""
     6	alteracao_25 — Separa responsabilidades de resolução de snapshot:
     7	  - _resolve_spot_and_rates  → MarketSnapshotProvider (spot, taxa, vol)
     8	  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
     9	  - _resolve_snapshot        → merge das duas fontes em contrato completo para o assembler
    10	
    11	Contrato exigido pelo assemble_structure_market_input:
    12	  {
    13	    "reference_date":     str | None,
    14	    "underlying_asset":   str,
    15	    "spot_price":         float | None,
    16	    "interest_rate":      float | None,
    17	    "volatility":         float | None,
    18	    "legs":               list[dict],   # campo extra, assembler ignora mas outros consomem
    19	    "aba":                str | None,
    20	  }
    21	"""
    22	
    23	from src.domain.refs.structure_ref import StructureRef
    24	
    25	from typing import Any
    26	
    27	from repositories.structures_repository import StructuresRepository
    28	from repositories.structure_events_repository import StructureEventsRepository
    29	from services.legacy_robo_legs_fallback import LegacyRoboLegsFallback
    30	from services.market_snapshot_provider import MarketSnapshotProvider
    31	from services.market_snapshot_selector import MarketSnapshotSelector
    32	from services.structure_events_service import StructureEventsService
    33	from services.structure_market_input_assembler import assemble_structure_market_input
    34	
    35	
    36	class CanonicalInputService:
    37	    def __init__(
    38	        self,
    39	        repository: StructuresRepository | None = None,
    40	        market_snapshot_provider: MarketSnapshotProvider | None = None,
    41	        market_snapshot_selector: MarketSnapshotSelector | None = None,
    42	        robo_legs_service: Any | None = None,  # injeção explícita
    43	        structure_events_service: StructureEventsService | None = None,
    44	        prefer_canonical_legs: bool = True,
    45	        enable_legacy_legs_fallback: bool = True,
    46	        allow_legacy_name_fallback: bool = False,
    47	        enable_structure_events: bool = True,
    48	    ):
    49	        self.repository                  = repository or StructuresRepository()
    50	        self.market_snapshot_provider    = market_snapshot_provider or MarketSnapshotProvider()
    51	        self.market_snapshot_selector    = market_snapshot_selector  # None = desabilitado
    52	        self.prefer_canonical_legs       = prefer_canonical_legs
    53	        self.enable_legacy_legs_fallback = enable_legacy_legs_fallback
    54	        self.allow_legacy_name_fallback  = allow_legacy_name_fallback
    55	
    56	        if robo_legs_service is not None:
    57	            # Injecao explicita — path canonico preferencial
    58	            self.robo_legs_service = robo_legs_service
    59	        else:
    60	            # BRIDGE LEGADO: import dinamico de robo_legs_service para compatibilidade
    61	            # com pipeline legado. Remover quando legado for desligado.
    62	            try:
    63	                from services.robo_legs_service import RoboLegsService  # noqa: PLC0415
    64	                self.robo_legs_service = RoboLegsService()
    65	            except ImportError:
    66	                self.robo_legs_service = None
    67	
    68	        # LegacyRoboLegsFallback sempre inicializado, independente da origem do robo_legs_service
    69	        self.legacy_robo_legs_fallback = LegacyRoboLegsFallback(
    70	            robo_legs_service=self.robo_legs_service,
    71	            allow_name_fallback=self.allow_legacy_name_fallback,
    72	        )
    73	
    74	        if structure_events_service is not None:
    75	            self.structure_events_service = structure_events_service
    76	        elif enable_structure_events and getattr(self.repository, "db_path", None):
    77	            self.structure_events_service = StructureEventsService(
    78	                structure_events_repository=StructureEventsRepository(
    79	                    db_path=self.repository.db_path,
    80	                )
    81	            )
    82	        else:
    83	            self.structure_events_service = None
    84	
    85	    # ──────────────────────────────────────────────────────────────────────────
    86	    # API pública
    87	    # ──────────────────────────────────────────────────────────────────────────
    88	
    89	    def build_structure_market_input(
    90	        self,
    91	        structure_id: int,
    92	        reference_date: str | None = None,
    93	    ) -> dict[str, Any]:
    94	        structure = self.repository.get_structure(structure_id)
    95	        if structure is None:
    96	            raise ValueError(f"structure not found: {structure_id}")
    97	
    98	        structure = {
    99	            **structure,
   100	            "name":              self._clean_text(structure.get("name")),
   101	            "underlying_asset":  self._clean_text(structure.get("underlying_asset")),
   102	            "alias_legacy_aba":  self._clean_text(structure.get("alias_legacy_aba")),
   103	        }
   104	
   105	        snapshot, snapshot_meta = self._resolve_snapshot(
   106	            structure=structure,
   107	            reference_date=reference_date,
   108	        )
   109	
   110	        effective_reference_date = reference_date or snapshot.get("reference_date")
   111	
   112	        enriched_structure, enrichment_meta = self._enrich_structure_with_legs(
   113	            structure=structure,
   114	            reference_date=effective_reference_date,
   115	        )
   116	
   117	        enriched_structure, events_meta = self._apply_structure_events(
   118	            structure=enriched_structure,
   119	        )
   120	
   121	        assembled       = assemble_structure_market_input(enriched_structure, snapshot)
   122	        assembled       = self._enrich_assembled_with_structure_metrics(assembled)
   123	        assembled_meta  = assembled.get("meta") or {}
   124	
   125	        return {
   126	            **assembled,
   127	            "meta": {
   128	                **assembled_meta,
   129	                "reference_date": effective_reference_date,
   130	                **enrichment_meta,
   131	                **events_meta,
   132	                **snapshot_meta,
   133	            },
   134	        }
   135	
   136	
   137	    # ──────────────────────────────────────────────────────────────────────────
   138	    # Resolução de snapshot — alteracao_25: duas responsabilidades separadas
   139	    # ──────────────────────────────────────────────────────────────────────────
   140	
   141	    def _resolve_snapshot(
   142	        self,
   143	        structure: dict[str, Any],
   144	        reference_date: str | None,
   145	    ) -> tuple[dict[str, Any], dict[str, Any]]:
   146	        """
   147	        Monta o snapshot dict completo exigido pelo assembler.
   148	
   149	        Sempre busca spot/taxa/vol no MarketSnapshotProvider (fonte autoritativa).
   150	        Se o selector estiver injetado E alias_legacy_aba existir, substitui as
   151	        legs pelo resultado do selector (manual > rtd).
   152	        """
   153	        underlying_asset = structure["underlying_asset"]
   154	        aba              = structure.get("alias_legacy_aba")
   155	
   156	        # 1. Spot, taxa, vol — sempre via provider
   157	        base_snapshot = self.market_snapshot_provider.get_snapshot(
   158	            underlying_asset,
   159	            reference_date=reference_date,
   160	        )
   161	
   162	        # 2. Legs — via selector se disponível, senão mantém o que o provider trouxe
   163	        if self.market_snapshot_selector is not None and aba:
   164	            ref = StructureRef.from_aba(aba)
   165	            legs_list, legs_meta = self._resolve_legs_via_selector(ref)
   166	            snapshot_source = legs_meta["snapshot_source"]
   167	        else:
   168	            legs_list  = base_snapshot.get("legs", [])
   169	            legs_meta  = {}
   170	            snapshot_source = "provider_legacy"
   171	
   172	        # 3. Monta contrato completo para o assembler
   173	        snapshot = {
   174	            **base_snapshot,            # reference_date, underlying_asset, spot_price,
   175	                                        # interest_rate, volatility (e qualquer extra)
   176	            "aba":  aba,
   177	            "legs": legs_list,
   178	        }
   179	
   180	        meta = {
   181	            "snapshot_source":  snapshot_source,
   182	            **legs_meta,
   183	        }
   184	
   185	        return snapshot, meta
   186	
   187	    # ──────────────────────────────────────────────────────────────────────────
   188	    # Legs via selector (manual > rtd)
   189	    # ──────────────────────────────────────────────────────────────────────────
   190	
   191	    def _resolve_legs_via_selector(
   192	        self,
   193	        ref: StructureRef,
   194	    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
   195	        """
   196	        Delega ao MarketSnapshotSelector e serializa legs completas.
   197	
   198	        Serialização cobre todos os campos de LegMarketSnapshot para que
   199	        consumidores downstream (pricing, greeks, payoff) tenham os dados.
   200	        """
   201	        aba_str = ref.aba
   202	        result = self.market_snapshot_selector.select(aba_str)
   203	
   204	        legs_as_dict = [
   205	            {
   206	                # ── identificação ──────────────────────────────────────────
   207	                "aba":              leg.aba,
   208	                "ativo":            leg.ativo,
   209	                "source":           leg.source.value if hasattr(leg.source, "value") else str(leg.source),
   210	                # ── posição ────────────────────────────────────────────────
   211	                "cv":               leg.cv,
   212	                "call_put":         leg.call_put,
   213	                "quant":            leg.quant,
   214	                "valor_executado":  leg.valor_executado,
   215	                # ── preços ─────────────────────────────────────────────────
   216	                "bid":              leg.bid,
   217	                "ask":              leg.ask,
   218	                "mid":              leg.mid,
   219	                "spread":           leg.spread,
   220	                "spread_pct":       leg.spread_pct,
   221	                # ── greeks ─────────────────────────────────────────────────
   222	                "iv":               leg.iv,
   223	                "delta":            leg.delta,
   224	                "gamma":            leg.gamma,
   225	                "theta":            leg.theta,
   226	                "vega":             leg.vega,
   227	                # ── contrato ───────────────────────────────────────────────
   228	                "strike":           leg.strike,
   229	                "vencimento":       leg.vencimento,
   230	                "dte":              leg.dte,
   231	                "pl_realista":      leg.pl_realista,
   232	                # ── auditoria ──────────────────────────────────────────────
   233	                "timestamp":        leg.timestamp,
   234	            }
   235	            for leg in result.legs
   236	        ]
   237	
   238	        # reference_date derivada do timestamp da leg mais recente
   239	        reference_date = self._reference_date_from_legs(result.legs)
   240	
   241	        meta = {
   242	            "snapshot_source":  result.source.value if hasattr(result.source, "value") else str(result.source),
   243	            "snapshot_aba":     aba_str,
   244	            "manual_overrides": result.manual_overrides,
   245	            "is_manual_first":  result.is_manual_first,
   246	            "legs_reference_date": reference_date,
   247	        }
   248	
   249	        return legs_as_dict, meta
   250	
   251	    @staticmethod
   252	    def _reference_date_from_legs(legs) -> str | None:
   253	        """Extrai a data (YYYY-MM-DD) do timestamp mais recente entre as legs."""
   254	        timestamps = [leg.timestamp for leg in legs if leg.timestamp]
   255	        if not timestamps:
   256	            return None
   257	        latest = max(timestamps)          # ISO string → max() funciona diretamente
   258	        return latest[:10]               # "YYYY-MM-DD HH:MM:SS" → "YYYY-MM-DD"
   259	
   260	    # ──────────────────────────────────────────────────────────────────────────
   261	    # Enriquecimento de legs canônicas / fallback (inalterado do alteracao_13)
   262	    # ──────────────────────────────────────────────────────────────────────────
   263	
   264	    def _build_meta(
   265	        self,
   266	        legs_source: str,
   267	        legacy_timestamp: str | None = None,
   268	        legacy_aba: str | None = None,
   269	        legacy_key_source: str | None = None,
   270	        fallback_reason: str | None = None,
   271	    ) -> dict[str, Any]:
   272	        meta: dict[str, Any] = {"legs_source": legs_source}
   273	        if legacy_timestamp  is not None: meta["legacy_timestamp"]  = legacy_timestamp
   274	        if legacy_aba        is not None: meta["legacy_aba"]        = legacy_aba
   275	        if legacy_key_source is not None: meta["legacy_key_source"] = legacy_key_source
   276	        if fallback_reason   is not None: meta["fallback_reason"]   = fallback_reason
   277	        return meta
   278	
   279	    def _base_legs_response(
   280	        self,
   281	        structure: dict[str, Any],
   282	        existing_legs: list[dict[str, Any]],
   283	        legs_source: str,
   284	        fallback_reason: str | None = None,
   285	    ) -> tuple[dict[str, Any], dict[str, Any]]:
   286	        return (
   287	            {**structure, "legs": existing_legs},
   288	            self._build_meta(legs_source=legs_source, fallback_reason=fallback_reason),
   289	        )
   290	
   291	    def _enrich_structure_with_legs(
   292	        self,
   293	        structure: dict[str, Any],
   294	        reference_date: str | None,
   295	    ) -> tuple[dict[str, Any], dict[str, Any]]:
   296	        existing_legs = structure.get("legs", []) or []
   297	
   298	        if self.prefer_canonical_legs and existing_legs:
   299	            return self._base_legs_response(
   300	                structure=structure,
   301	                existing_legs=existing_legs,
   302	                legs_source="canonical",
   303	            )
   304	
   305	        if not self.enable_legacy_legs_fallback:
   306	            return self._base_legs_response(
   307	                structure=structure,
   308	                existing_legs=existing_legs,
   309	                legs_source="empty",
   310	                fallback_reason="legacy_fallback_disabled",
   311	            )
   312	
   313	        fallback_legs, fallback_meta = self.legacy_robo_legs_fallback.load(
   314	            structure=structure,
   315	            reference_date=reference_date,
   316	        )
   317	
   318	        if fallback_legs:
   319	            return (
   320	                {**structure, "legs": fallback_legs},
   321	                {
   322	                    "legs_source":       fallback_meta.get("legs_source", "legacy_fallback"),
   323	                    "legacy_timestamp":  fallback_meta.get("legacy_timestamp"),
   324	                    "legacy_aba":        fallback_meta.get("legacy_aba"),
   325	                    "legacy_key_source": fallback_meta.get("legacy_key_source"),
   326	                    "fallback_reason":   fallback_meta.get("fallback_reason"),
   327	                },
   328	            )
   329	
   330	        if existing_legs:
   331	            return self._base_legs_response(
   332	                structure=structure,
   333	                existing_legs=existing_legs,
   334	                legs_source="canonical",
   335	                fallback_reason="canonical_legs_retained_after_empty_fallback",
   336	            )
   337	
   338	        return self._base_legs_response(
   339	            structure=structure,
   340	            existing_legs=existing_legs,
   341	            legs_source="empty",
   342	            fallback_reason=(
   343	                fallback_meta.get("fallback_reason") if fallback_meta else "no_legs_available"
   344	            ),
   345	        )
   346	
   347	
   348	    # ──────────────────────────────────────────────────────────────────────────
   349	    # Eventos operacionais
   350	    # ──────────────────────────────────────────────────────────────────────────
   351	
   352	    def _apply_structure_events(
   353	        self,
   354	        structure: dict[str, Any],
   355	    ) -> tuple[dict[str, Any], dict[str, Any]]:
   356	        if self.structure_events_service is None:
   357	            return structure, {
   358	                "structure_events_enabled": False,
   359	                "structure_events_applied": 0,
   360	            }
   361	
   362	        effective_structure = self.structure_events_service.apply_events_to_structure(
   363	            structure=structure,
   364	        )
   365	
   366	        operational_state = effective_structure.get("operational_state") or {}
   367	
   368	        return effective_structure, {
   369	            "structure_events_enabled": True,
   370	            "structure_events_applied": operational_state.get("events_applied", 0),
   371	            "structure_events_ignored_cancelled": operational_state.get(
   372	                "events_ignored_cancelled",
   373	                0,
   374	            ),
   375	            "structure_operational_closed": operational_state.get("is_closed", False),
   376	        }
   377	
   378	    # ──────────────────────────────────────────────────────────────────────────
   379	    # Métricas internas da estrutura
   380	    # ──────────────────────────────────────────────────────────────────────────
   381	
   382	    def _enrich_assembled_with_structure_metrics(
   383	        self,
   384	        assembled: dict[str, Any],
   385	    ) -> dict[str, Any]:
   386	        """
   387	        Calcula métricas internas a partir do input canônico montado e injeta
   388	        os campos agregados no bloco market.
   389	
   390	        Mantém o contrato existente e apenas acrescenta campos opcionais já
   391	        previstos no domínio de MarketSnapshot.
   392	        """
   393	        structure_metrics = compute_structure_metrics_from_canonical_input(assembled)
   394	
   395	        market = assembled.get("market") or {}
   396	        meta = assembled.get("meta") or {}
   397	
   398	        return {
   399	            **assembled,
   400	            "market": {
   401	                **market,
   402	                "dte_min": structure_metrics.get("dte_min"),
   403	                "pl_realista_total": structure_metrics.get("pl_realista_total"),
   404	                "delta_liq": structure_metrics.get("delta_liq"),
   405	                "gamma_liq": structure_metrics.get("gamma_liq"),
   406	                "theta_liq": structure_metrics.get("theta_liq"),
   407	                "vega_liq": structure_metrics.get("vega_liq"),
   408	                "spread_medio": structure_metrics.get("spread_medio"),
   409	                "spread_pct_medio": structure_metrics.get("spread_pct_medio"),
   410	            },
   411	            "meta": {
   412	                **meta,
   413	                "structure_metrics_source": "internal_engine",
   414	            },
   415	        }
   416	
   417	
   418	    # ──────────────────────────────────────────────────────────────────────────
   419	    # Utilitários
   420	    # ──────────────────────────────────────────────────────────────────────────
   421	
   422	    def _clean_text(self, value: Any) -> Any:
   423	        if isinstance(value, str):
   424	            return value.strip()
   425	        return value
```

## FILE: services/pricing_input_service.py
```python
     1	from typing import Any
     2	
     3	from services.canonical_input_service import CanonicalInputService
     4	from services.pricing_payload_adapter import to_pricing_payload
     5	
     6	
     7	class PricingInputService:
     8	    def __init__(
     9	        self,
    10	        canonical_input_service: CanonicalInputService | None = None,
    11	    ):
    12	        self.canonical_input_service = canonical_input_service or CanonicalInputService()
    13	
    14	    def build_pricing_payload(
    15	        self,
    16	        structure_id: int,
    17	        reference_date: str | None = None,
    18	    ) -> dict[str, Any]:
    19	        canonical_input = self.canonical_input_service.build_structure_market_input(
    20	            structure_id=structure_id,
    21	            reference_date=reference_date,
    22	        )
    23	
    24	        return self.build_pricing_payload_from_canonical_input(canonical_input)
    25	
    26	    def build_pricing_payload_from_canonical_input(
    27	        self,
    28	        canonical_input: dict[str, Any],
    29	    ) -> dict[str, Any]:
    30	        return to_pricing_payload(canonical_input)
```

## FILE: services/pricing_payload_adapter.py
```python
     1	from typing import Any
     2	
     3	from domain.position_side import to_pricing_engine_side
     4	
     5	
     6	def _clean_text(value: Any) -> str | None:
     7	    if value is None:
     8	        return None
     9	    text = str(value).strip()
    10	    return text or None
    11	
    12	
    13	def _clean_upper_text(value: Any) -> str | None:
    14	    text = _clean_text(value)
    15	    return text.upper() if text is not None else None
    16	
    17	
    18	def to_pricing_payload(canonical_input: dict[str, Any]) -> dict[str, Any]:
    19	    if not canonical_input:
    20	        raise ValueError("canonical_input is required")
    21	
    22	    structure = canonical_input.get("structure")
    23	    market = canonical_input.get("market")
    24	
    25	    if not structure:
    26	        raise ValueError("canonical_input.structure is required")
    27	
    28	    if not market:
    29	        raise ValueError("canonical_input.market is required")
    30	
    31	    legs = structure.get("legs", [])
    32	    pricing_legs = []
    33	
    34	    for index, leg in enumerate(legs):
    35	        if not leg:
    36	            raise ValueError(f"canonical_input.structure.legs[{index}] is required")
    37	
    38	        pricing_legs.append(
    39	            {
    40	                "side": to_pricing_engine_side(leg["position_side"]),
    41	                "instrument_type": "OPTION",
    42	                "option_type": _clean_upper_text(leg["option_type"]),
    43	                "symbol": _clean_upper_text(leg.get("symbol")),
    44	                "strike": float(leg["strike"]),
    45	                "expiration_date": _clean_text(leg["expiration_date"]),
    46	                "quantity": int(leg["quantity"]),
    47	                "premium": float(leg["premium"]) if leg.get("premium") is not None else None,
    48	                "multiplier": float(leg["multiplier"]),
    49	            }
    50	        )
    51	
    52	    return {
    53	        "structure_id": structure["structure_id"],
    54	        "structure_name": _clean_text(structure["name"]),
    55	        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
    56	        "reference_date": _clean_text(market["reference_date"]),
    57	        "spot_price": float(market["spot_price"]),
    58	        "interest_rate": float(market["interest_rate"]),
    59	        "volatility": float(market["volatility"]),
    60	        "legs": pricing_legs,
    61	    }
```

## FILE: services/structure_input_mapper.py
```python
     1	from typing import Any
     2	
     3	from domain.position_side import normalize_position_side
     4	
     5	
     6	def _clean_text(value: Any) -> str | None:
     7	    if value is None:
     8	        return None
     9	    text = str(value).strip()
    10	    return text or None
    11	
    12	
    13	def _clean_upper_text(value: Any) -> str | None:
    14	    text = _clean_text(value)
    15	    return text.upper() if text is not None else None
    16	
    17	
    18	def _to_float_or_none(value: Any) -> float | None:
    19	    if value is None:
    20	        return None
    21	
    22	    try:
    23	        return float(value)
    24	    except (TypeError, ValueError):
    25	        return None
    26	
    27	
    28	def _enrich_bid_ask_derived_fields(mapped_leg: dict[str, Any]) -> None:
    29	    bid = _to_float_or_none(mapped_leg.get("bid"))
    30	    ask = _to_float_or_none(mapped_leg.get("ask"))
    31	
    32	    if bid is None or ask is None:
    33	        return
    34	
    35	    spread = ask - bid
    36	    mid = (bid + ask) / 2
    37	
    38	    if "spread" not in mapped_leg or mapped_leg.get("spread") is None:
    39	        mapped_leg["spread"] = spread
    40	
    41	    if "mid" not in mapped_leg or mapped_leg.get("mid") is None:
    42	        mapped_leg["mid"] = mid
    43	
    44	    if (
    45	        ("spread_pct" not in mapped_leg or mapped_leg.get("spread_pct") is None)
    46	        and mid
    47	    ):
    48	        mapped_leg["spread_pct"] = spread / mid
    49	
    50	
    51	def _map_leg_to_structure_input(leg: dict[str, Any]) -> dict[str, Any]:
    52	    mapped_leg = {
    53	        "position_side": normalize_position_side(leg["position_side"]),
    54	        "option_type": _clean_upper_text(leg["option_type"]),
    55	        "symbol": _clean_upper_text(leg.get("symbol")),
    56	        "strike": leg["strike"],
    57	        "expiration_date": _clean_text(leg["expiration_date"]),
    58	        "quantity": leg["quantity"],
    59	        "premium": leg.get("premium"),
    60	        "multiplier": leg.get("multiplier", 1.0),
    61	    }
    62	
    63	    optional_market_fields = (
    64	        "bid",
    65	        "ask",
    66	        "mid",
    67	        "spread",
    68	        "spread_pct",
    69	        "iv",
    70	        "delta",
    71	        "gamma",
    72	        "theta",
    73	        "vega",
    74	    )
    75	
    76	    for field in optional_market_fields:
    77	        if field in leg:
    78	            mapped_leg[field] = leg[field]
    79	
    80	    _enrich_bid_ask_derived_fields(mapped_leg)
    81	
    82	    return mapped_leg
    83	
    84	
    85	def to_structure_input(structure: dict[str, Any]) -> dict[str, Any]:
    86	    if not structure:
    87	        raise ValueError("structure is required")
    88	
    89	    legs = structure.get("legs", [])
    90	
    91	    return {
    92	        "structure_id": structure["id"],
    93	        "name": _clean_text(structure["name"]),
    94	        "underlying_asset": _clean_upper_text(structure["underlying_asset"]),
    95	        "legs": [
    96	            _map_leg_to_structure_input(leg)
    97	            for leg in legs
    98	        ],
    99	    }
```

## FILE: services/structure_market_input_assembler.py
```python
     1	from typing import Any
     2	
     3	from services.structure_input_mapper import to_structure_input
     4	
     5	
     6	def assemble_structure_market_input(
     7	    structure: dict[str, Any],
     8	    market_snapshot: dict[str, Any],
     9	) -> dict[str, Any]:
    10	    if not structure:
    11	        raise ValueError("structure is required")
    12	
    13	    if not market_snapshot:
    14	        raise ValueError("market_snapshot is required")
    15	
    16	    structure_input = to_structure_input(structure)
    17	    structure_asset = structure_input["underlying_asset"]
    18	    market_asset = market_snapshot.get("underlying_asset")
    19	
    20	    if structure_asset != market_asset:
    21	        raise ValueError(
    22	            f"underlying_asset mismatch: structure={structure_asset} market={market_asset}"
    23	        )
    24	
    25	    return {
    26	        "structure": structure_input,
    27	        "market": {
    28	            "reference_date": market_snapshot["reference_date"],
    29	            "underlying_asset": market_snapshot["underlying_asset"],
    30	            "spot_price": market_snapshot["spot_price"],
    31	            "interest_rate": market_snapshot["interest_rate"],
    32	            "volatility": market_snapshot["volatility"],
    33	        },
    34	        "meta": {
    35	            "input_source": "structure_market_input_assembler",
    36	        },
    37	    }
```

## FILE: services/calculation_orchestrator.py
```python
     1	# services/calculation_orchestrator.py
     2	# alteracao_45: CalculationRequest contract + build_calculation_request
     3	# alteracao_46: _request_to_payoff_dict, run_payoff, run_decision
     4	# alteracao_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
     5	# alteracao_48: CalculationOrchestrator class, build_calculation_request_from_db,
     6	#           run_full_pipeline_from_db
     7	
     8	from __future__ import annotations
     9	
    10	import logging
    11	from types import SimpleNamespace
    12	from typing import Optional, Dict, Any, List
    13	
    14	from domain.calculation_request import (
    15	    CalculationRequest,
    16	    MarketSnapshotInput,
    17	    StructureInput,
    18	    StructureLegInput,
    19	)
    20	from domain.payoff import compute_payoff_from_canonical_input
    21	from domain.decision import compute_decision_from_contract
    22	from domain.position_side import to_pricing_engine_side
    23	
    24	logger = logging.getLogger(__name__)
    25	
    26	# ---------------------------------------------------------------------------
    27	# Mapeamento legado -> contrato tecnico de calculo
    28	# ---------------------------------------------------------------------------
    29	_CP_NORM = {"CALL": "CALL", "PUT": "PUT", "C": "CALL", "P": "PUT"}
    30	
    31	
    32	def _normalize_position_side(raw: str) -> str:
    33	    try:
    34	        return to_pricing_engine_side(raw)
    35	    except ValueError as exc:
    36	        raise ValueError(f"position_side desconhecido: {raw!r}") from exc
    37	
    38	
    39	def _normalize_option_type(raw: str) -> str:
    40	    v = str(raw).strip().upper()
    41	    if v not in _CP_NORM:
    42	        raise ValueError(f"option_type desconhecido: {raw!r}")
    43	    return _CP_NORM[v]
    44	
    45	
    46	# ---------------------------------------------------------------------------
    47	# Funcao legada build_calculation_request (alteracao_45 -- mantida para
    48	# retrocompatibilidade com testes anteriores)
    49	# ---------------------------------------------------------------------------
    50	def build_calculation_request(
    51	    structure_row: dict,
    52	    legs_rows: list,
    53	    snapshot_row: dict,
    54	) -> CalculationRequest:
    55	    """
    56	    Monta um CalculationRequest a partir de dicts vindos do repositorio.
    57	    Mantida para retrocompatibilidade (alteracao_45).
    58	    """
    59	    if not isinstance(legs_rows, list) or len(legs_rows) == 0:
    60	        raise ValueError("legs_rows nao pode ser vazio")
    61	
    62	    legs = []
    63	    for i, row in enumerate(legs_rows):
    64	        try:
    65	            leg = StructureLegInput(
    66	                position_side=_normalize_position_side(
    67	                    row.get("position_side") or row.get("cv", "")
    68	                ),
    69	                option_type=_normalize_option_type(
    70	                    row.get("option_type") or row.get("call_put", "")
    71	                ),
    72	                strike=float(row["strike"]),
    73	                expiration_date=str(row["expiration_date"]),
    74	                quantity=int(row["quantity"]),
    75	                symbol=row.get("symbol"),
    76	                premium=float(row["premium"]) if row.get("premium") is not None else None,
    77	                multiplier=float(row.get("multiplier") or 1.0),
    78	                leg_order=int(row.get("leg_order") or i),
    79	                notes=row.get("notes"),
    80	            )
    81	        except (KeyError, TypeError, ValueError) as exc:
    82	            raise ValueError(f"Erro ao montar leg[{i}]: {exc}") from exc
    83	        legs.append(leg)
    84	
    85	    structure = StructureInput(
    86	        structure_id=int(structure_row["id"]),
    87	        underlying_asset=str(structure_row["underlying_asset"]),
    88	        legs=legs,
    89	        name=structure_row.get("name"),
    90	        alias_legacy_aba=structure_row.get("alias_legacy_aba"),
    91	    )
    92	
    93	    snapshot = MarketSnapshotInput(
    94	        snapshot_timestamp=str(snapshot_row["snapshot_timestamp"]),
    95	        underlying_asset=str(snapshot_row["underlying_asset"]),
    96	        spot_price=float(snapshot_row["spot_price"]),
    97	        source=str(snapshot_row.get("source", "rtd")),
    98	        snapshot_id=snapshot_row.get("snapshot_id") or snapshot_row.get("id"),
    99	        option_quotes=snapshot_row.get("option_quotes"),
   100	        greeks=snapshot_row.get("greeks"),
   101	        volatility_context=snapshot_row.get("volatility_context"),
   102	    )
   103	
   104	    return CalculationRequest(structure=structure, market_snapshot=snapshot)
   105	
   106	
   107	# ---------------------------------------------------------------------------
   108	# Funcoes legadas de pipeline (alteracao_46/47 -- mantidas para
   109	# retrocompatibilidade com testes anteriores)
   110	# ---------------------------------------------------------------------------
   111	def _request_to_payoff_dict(
   112	    request: CalculationRequest,
   113	    extra_meta: Optional[dict] = None,
   114	) -> dict:
   115	    """alteracao_47: multiplier usa leg.multiplier com fallback 1.0."""
   116	    legs = []
   117	    for leg in request.structure.legs:
   118	        legs.append({
   119	            "position_side":   leg.position_side,
   120	            "option_type":     leg.option_type,
   121	            "strike":          leg.strike,
   122	            "expiration_date": leg.expiration_date,
   123	            "quantity":        leg.quantity,
   124	            "symbol":          getattr(leg, "symbol",      None),
   125	            "premium":         getattr(leg, "premium",     None),
   126	            "multiplier":      getattr(leg, "multiplier",  1.0),
   127	            "leg_order":       getattr(leg, "leg_order",   0),
   128	            "notes":           getattr(leg, "notes",       None),
   129	        })
   130	
   131	    return {
   132	        "structure": {
   133	            "structure_id":     request.structure.structure_id,
   134	            "underlying_asset": request.structure.underlying_asset,
   135	            "name":             getattr(request.structure, "name", None),
   136	            "legs":             legs,
   137	        },
   138	        "market": {
   139	            "spot_price":       request.market_snapshot.spot_price,
   140	            "underlying_asset": request.market_snapshot.underlying_asset,
   141	            "reference_date":   getattr(request.market_snapshot, "snapshot_timestamp", None),
   142	            "option_quotes":    getattr(request.market_snapshot, "option_quotes",      {}),
   143	            "greeks":           getattr(request.market_snapshot, "greeks",             {}),
   144	        },
   145	        "meta": extra_meta or {},
   146	    }
   147	
   148	
   149	def run_payoff(
   150	    request: CalculationRequest,
   151	    low_pct: float = 0.5,
   152	    high_pct: float = 1.5,
   153	    step_pct: float = 0.01,
   154	    extra_meta: Optional[dict] = None,
   155	) -> dict:
   156	    """Executa calculo de payoff a partir de um CalculationRequest."""
   157	    canonical = _request_to_payoff_dict(request, extra_meta=extra_meta)
   158	    return compute_payoff_from_canonical_input(
   159	        canonical,
   160	        low_pct=low_pct,
   161	        high_pct=high_pct,
   162	        step_pct=step_pct,
   163	    )
   164	
   165	
   166	def run_decision(
   167	    request: CalculationRequest,
   168	    payoff: Optional[dict] = None,
   169	    pl_atual: Optional[float] = None,
   170	    pl_max: Optional[float] = None,
   171	    dte_min: Optional[int] = None,
   172	) -> dict:
   173	    """alteracao_47: extrai pl_max/pl_atual/dte_min automaticamente."""
   174	    _pl_max = pl_max
   175	    if _pl_max is None and payoff:
   176	        _pl_max = float(payoff.get("pl_max") or 0.0)
   177	    if _pl_max is None:
   178	        _pl_max = 0.0
   179	
   180	    _pl_atual = pl_atual
   181	    if _pl_atual is None and payoff:
   182	        _pl_atual = float(payoff.get("pl_atual") or payoff.get("pl_now") or 0.0)
   183	    if _pl_atual is None:
   184	        _pl_atual = 0.0
   185	
   186	    _dte_min = dte_min
   187	    if _dte_min is None:
   188	        _dte_min = getattr(request.market_snapshot, "dte_min", None)
   189	
   190	    contract = SimpleNamespace(
   191	        pl_max=_pl_max,
   192	        pl_atual=_pl_atual,
   193	        dte_min=_dte_min,
   194	    )
   195	    return compute_decision_from_contract(contract, payoff=payoff)
   196	
   197	
   198	def run_full_pipeline(
   199	    request: CalculationRequest,
   200	    low_pct: float = 0.5,
   201	    high_pct: float = 1.5,
   202	    step_pct: float = 0.01,
   203	    extra_meta: Optional[dict] = None,
   204	) -> dict:
   205	    """alteracao_47: pipeline completo payoff + decision."""
   206	    payoff_result = run_payoff(
   207	        request,
   208	        low_pct=low_pct,
   209	        high_pct=high_pct,
   210	        step_pct=step_pct,
   211	        extra_meta=extra_meta,
   212	    )
   213	    decision_result = run_decision(request, payoff=payoff_result)
   214	
   215	    return {
   216	        "payoff":           payoff_result,
   217	        "decision":         decision_result,
   218	        "structure_id":     request.structure.structure_id,
   219	        "underlying_asset": request.structure.underlying_asset,
   220	    }
   221	
   222	
   223	# ===========================================================================
   224	# alteracao_48 -- CalculationOrchestrator (classe canonica)
   225	# ===========================================================================
   226	
   227	class CalculationOrchestrator:
   228	    """
   229	    Orquestrador canonico de calculo.
   230	
   231	    Responsabilidades:
   232	    - Montar CalculationRequest a partir de dicts ja normalizados
   233	    - Executar payoff e decisao sem acessar raw DB diretamente
   234	    - Montar CalculationRequest a partir dos repositorios canonicos (alteracao_48)
   235	
   236	    via repositórios injetados.
   237	    """
   238	
   239	    def __init__(
   240	        self,
   241	        structures_repository=None,
   242	        market_snapshot_repository=None,
   243	    ):
   244	        self._structures_repo = structures_repository
   245	        self._snapshot_repo   = market_snapshot_repository
   246	
   247	    # ------------------------------------------------------------------
   248	    # Construcao manual do CalculationRequest
   249	    # ------------------------------------------------------------------
   250	
   251	    def build_calculation_request(
   252	        self,
   253	        structure_dict: Dict[str, Any],
   254	        market_snapshot_dict: Dict[str, Any],
   255	    ) -> CalculationRequest:
   256	        """Monta CalculationRequest a partir de dicts ja normalizados."""
   257	        legs = []
   258	        for i, leg in enumerate(structure_dict.get("legs", [])):
   259	            legs.append(
   260	                StructureLegInput(
   261	                    position_side=_normalize_position_side(
   262	                        leg.get("position_side") or leg.get("cv", "")
   263	                    ),
   264	                    option_type=_normalize_option_type(
   265	                        leg.get("option_type") or leg.get("call_put", "CALL")
   266	                    ),
   267	                    strike=float(leg["strike"]),
   268	                    expiration_date=str(leg["expiration_date"]),
   269	                    quantity=int(leg["quantity"]),
   270	                    symbol=leg.get("symbol"),
   271	                    premium=float(leg["premium"]) if leg.get("premium") is not None else None,
   272	                    multiplier=float(leg.get("multiplier") or 1.0),
   273	                    leg_order=int(leg.get("leg_order") or i),
   274	                    notes=leg.get("notes"),
   275	                )
   276	            )
   277	
   278	        structure = StructureInput(
   279	            structure_id=int(structure_dict["structure_id"]),
   280	            name=structure_dict.get("name", ""),
   281	            underlying_asset=str(structure_dict.get("underlying_asset", "")),
   282	            alias_legacy_aba=structure_dict.get("alias_legacy_aba"),
   283	            legs=legs,
   284	        )
   285	
   286	        snapshot = MarketSnapshotInput(
   287	            snapshot_id=market_snapshot_dict.get("snapshot_id"),
   288	            snapshot_timestamp=str(market_snapshot_dict.get("snapshot_timestamp", "")),
   289	            underlying_asset=str(market_snapshot_dict.get("underlying_asset", "")),
   290	            spot_price=float(market_snapshot_dict.get("spot_price", 0.0)),
   291	            source=str(market_snapshot_dict.get("source", "rtd")),
   292	            option_quotes=market_snapshot_dict.get("option_quotes"),
   293	            greeks=market_snapshot_dict.get("greeks"),
   294	            volatility_context=market_snapshot_dict.get("volatility_context"),
   295	        )
   296	
   297	        return CalculationRequest(structure=structure, market_snapshot=snapshot)
   298	
   299	    # ------------------------------------------------------------------
   300	    # Adaptacao interna
   301	    # ------------------------------------------------------------------
   302	
   303	    def _request_to_payoff_dict(self, request: CalculationRequest) -> Dict[str, Any]:
   304	        """Converte CalculationRequest para o dict de payoff."""
   305	        legs = []
   306	        for leg in request.structure.legs:
   307	            legs.append({
   308	                "position_side":   leg.position_side,
   309	                "option_type":     leg.option_type,
   310	                "strike":          leg.strike,
   311	                "expiration_date": leg.expiration_date,
   312	                "quantity":        leg.quantity,
   313	                "symbol":          getattr(leg, "symbol",     None),
   314	                "premium":         getattr(leg, "premium",    None),
   315	                "multiplier":      getattr(leg, "multiplier", 1.0),
   316	                "leg_order":       getattr(leg, "leg_order",  0),
   317	                "notes":           getattr(leg, "notes",      None),
   318	            })
   319	
   320	        return {
   321	            "structure": {
   322	                "structure_id":     request.structure.structure_id,
   323	                "underlying_asset": request.structure.underlying_asset,
   324	                "name":             getattr(request.structure, "name", None),
   325	                "legs":             legs,
   326	            },
   327	            "market": {
   328	                "spot_price":       request.market_snapshot.spot_price,
   329	                "underlying_asset": request.market_snapshot.underlying_asset,
   330	                "reference_date":   getattr(request.market_snapshot, "snapshot_timestamp", None),
   331	                "option_quotes":    getattr(request.market_snapshot, "option_quotes", {}),
   332	                "greeks":           getattr(request.market_snapshot, "greeks",        {}),
   333	            },
   334	            "meta": {},
   335	        }
   336	
   337	    # ------------------------------------------------------------------
   338	    # run_payoff / run_decision / run_full_pipeline
   339	    # ------------------------------------------------------------------
   340	
   341	    def run_payoff(
   342	        self,
   343	        request: CalculationRequest,
   344	        low_pct: float = 0.5,
   345	        high_pct: float = 1.5,
   346	        step_pct: float = 0.01,
   347	    ) -> Dict[str, Any]:
   348	        canonical = self._request_to_payoff_dict(request)
   349	        return compute_payoff_from_canonical_input(
   350	            canonical,
   351	            low_pct=low_pct,
   352	            high_pct=high_pct,
   353	            step_pct=step_pct,
   354	        )
   355	
   356	    def run_decision(
   357	        self,
   358	        request: CalculationRequest,
   359	        payoff_result: Optional[Dict[str, Any]] = None,
   360	    ) -> Dict[str, Any]:
   361	        if payoff_result is None:
   362	            payoff_result = self.run_payoff(request)
   363	
   364	        _pl_max = float(
   365	            payoff_result.get("pl_max") or payoff_result.get("max_profit") or 0.0
   366	        )
   367	        _pl_atual = float(
   368	            payoff_result.get("pl_atual")
   369	            or payoff_result.get("current_pl")
   370	            or payoff_result.get("pl_now")
   371	            or 0.0
   372	        )
   373	        _dte_min = (
   374	            payoff_result.get("dte_min")
   375	            or getattr(request.market_snapshot, "dte_min", None)
   376	            or 0
   377	        )
   378	
   379	        contract = SimpleNamespace(
   380	            pl_max=_pl_max,
   381	            pl_atual=_pl_atual,
   382	            dte_min=_dte_min,
   383	        )
   384	        return compute_decision_from_contract(contract, payoff=payoff_result)
   385	
   386	    def run_full_pipeline(
   387	        self,
   388	        request: CalculationRequest,
   389	        low_pct: float = 0.5,
   390	        high_pct: float = 1.5,
   391	        step_pct: float = 0.01,
   392	    ) -> Dict[str, Any]:
   393	        """Executa run_payoff -> run_decision em sequencia."""
   394	        payoff_result   = self.run_payoff(request, low_pct=low_pct, high_pct=high_pct, step_pct=step_pct)
   395	        decision_result = self.run_decision(request, payoff_result=payoff_result)
   396	
   397	        return {
   398	            "payoff":           payoff_result,
   399	            "decision":         decision_result,
   400	            "structure_id":     request.structure.structure_id,
   401	            "underlying_asset": request.structure.underlying_asset,
   402	        }
   403	
   404	    # ------------------------------------------------------------------
   405	    # alteracao_48 -- resolucao via repositorios canonicos
   406	    # ------------------------------------------------------------------
   407	
   408	    def build_calculation_request_from_db(
   409	        self,
   410	        structure_id: int,
   411	        snapshot_timestamp: Optional[str] = None,
   412	    ) -> CalculationRequest:
   413	        """
   414	        Monta CalculationRequest buscando dados dos repositorios canonicos.
   415	
   416	        Raises:
   417	            RuntimeError: se repositorios nao foram injetados
   418	            ValueError  : se estrutura nao encontrada, arquivada ou sem legs
   419	            ValueError  : se snapshot nao encontrado
   420	        """
   421	        if self._structures_repo is None:
   422	            raise RuntimeError(
   423	                "StructuresRepository nao foi injetado no orquestrador. "
   424	                "Passe structures_repository= no construtor."
   425	            )
   426	        if self._snapshot_repo is None:
   427	            raise RuntimeError(
   428	                "MarketSnapshotRepository nao foi injetado no orquestrador. "
   429	                "Passe market_snapshot_repository= no construtor."
   430	            )
   431	
   432	        # 1. Busca estrutura
   433	        structure = self._structures_repo.get_structure(structure_id)
   434	        if structure is None:
   435	            raise ValueError(
   436	                f"Estrutura nao encontrada: structure_id={structure_id}"
   437	            )
   438	        if structure.get("status") == "archived":
   439	            raise ValueError(
   440	                f"Estrutura arquivada nao pode ser recalculada: "
   441	                f"structure_id={structure_id}"
   442	            )
   443	
   444	        legs_raw = structure.get("legs", [])
   445	        if not legs_raw:
   446	            raise ValueError(
   447	                f"Estrutura sem legs: structure_id={structure_id}"
   448	            )
   449	
   450	        # 2. Busca snapshot
   451	        underlying = structure.get("underlying_asset", "")
   452	        snapshot = self._snapshot_repo.get_snapshot(
   453	            underlying_asset=underlying,
   454	            timestamp=snapshot_timestamp,
   455	        )
   456	        if snapshot is None:
   457	            raise ValueError(
   458	                f"Snapshot nao encontrado para underlying_asset='{underlying}' "
   459	                f"timestamp={snapshot_timestamp!r}"
   460	            )
   461	
   462	        # 3. Monta dicts e delega para build_calculation_request
   463	        structure_dict = {
   464	            "structure_id":    structure["id"],
   465	            "name":            structure.get("name", ""),
   466	            "underlying_asset": underlying,
   467	            "alias_legacy_aba": structure.get("alias_legacy_aba"),
   468	            "legs": [
   469	                {
   470	                    "position_side":   leg["position_side"],
   471	                    "option_type":     leg["option_type"],
   472	                    "strike":          leg["strike"],
   473	                    "expiration_date": leg["expiration_date"],
   474	                    "quantity":        leg["quantity"],
   475	                    "symbol":          leg.get("symbol"),
   476	                    "premium":         leg.get("premium"),
   477	                    "multiplier":      leg.get("multiplier", 1.0),
   478	                    "leg_order":       leg.get("leg_order", 0),
   479	                    "notes":           leg.get("notes"),
   480	                }
   481	                for leg in legs_raw
   482	            ],
   483	        }
   484	
   485	        market_snapshot_dict = {
   486	            "snapshot_id":        snapshot.get("id"),
   487	            "snapshot_timestamp": snapshot.get("snapshot_timestamp", ""),
   488	            "underlying_asset":   snapshot.get("underlying_asset", underlying),
   489	            "spot_price":         snapshot.get("spot_price", 0.0),
   490	            "source":             snapshot.get("source", "rtd"),
   491	            "option_quotes":      snapshot.get("option_quotes"),
   492	            "greeks":             snapshot.get("greeks"),
   493	            "volatility_context": snapshot.get("volatility_context"),
   494	        }
   495	
   496	        return self.build_calculation_request(structure_dict, market_snapshot_dict)
   497	
   498	    def run_full_pipeline_from_db(
   499	        self,
   500	        structure_id: int,
   501	        snapshot_timestamp: Optional[str] = None,
   502	    ) -> Dict[str, Any]:
   503	        """
   504	        Pipeline completo resolvendo estrutura e snapshot pelos repositorios.
   505	
   506	        Retorna dict com chaves: structure_id, payoff, decision.
   507	        """
   508	        request        = self.build_calculation_request_from_db(
   509	            structure_id=structure_id,
   510	            snapshot_timestamp=snapshot_timestamp,
   511	        )
   512	        pipeline_result = self.run_full_pipeline(request)
   513	
   514	        return {
   515	            "structure_id": structure_id,
   516	            "payoff":       pipeline_result["payoff"],
   517	            "decision":     pipeline_result["decision"],
   518	        }
```

## FILE: domain/calculation_request.py
```python
     1	"""
     2	alteracao_45 -- Contrato canônico de entrada para cálculo.
     3	
     4	Define os DTOs imutáveis que o domínio recebe:
     5	  CalculationRequest
     6	     structure: StructureInput
     7	          legs: List[StructureLegInput]
     8	     market_snapshot: MarketSnapshotInput
     9	
    10	O domínio NÃO acessa banco diretamente -- recebe estes objetos
    11	já normalizados pelo orquestrador.
    12	"""
    13	from __future__ import annotations
    14	
    15	import re
    16	from dataclasses import dataclass, field
    17	from datetime import date, datetime
    18	from typing import List, Optional
    19	
    20	from domain.position_side import to_pricing_engine_side
    21	
    22	
    23	# ---------------------------------------------------------------------------
    24	# Constantes de domínio
    25	# ---------------------------------------------------------------------------
    26	VALID_POSITION_SIDES = {"LONG", "SHORT"}
    27	VALID_OPTION_TYPES   = {"CALL", "PUT"}
    28	VALID_SOURCES        = {"rtd", "manual", "ui"}
    29	_DATE_RE             = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    30	
    31	
    32	# ---------------------------------------------------------------------------
    33	# Helpers de validação
    34	# ---------------------------------------------------------------------------
    35	def _require_nonempty(value: str, field_name: str) -> str:
    36	    if not isinstance(value, str) or not value.strip():
    37	        raise ValueError(f"{field_name} não pode ser vazio")
    38	    return value.strip()
    39	
    40	
    41	def _require_positive(value: float | int, field_name: str) -> float:
    42	    try:
    43	        v = float(value)
    44	    except (TypeError, ValueError):
    45	        raise ValueError(f"{field_name} deve ser numérico, recebeu: {value!r}")
    46	    if v <= 0:
    47	        raise ValueError(f"{field_name} deve ser positivo, recebeu: {v}")
    48	    return v
    49	
    50	
    51	def _require_date_str(value: str, field_name: str) -> str:
    52	    """Aceita string 'YYYY-MM-DD' e valida."""
    53	    if not isinstance(value, str) or not _DATE_RE.match(value):
    54	        raise ValueError(
    55	            f"{field_name} deve estar no formato YYYY-MM-DD, recebeu: {value!r}"
    56	        )
    57	    # Valida calendário
    58	    try:
    59	        date.fromisoformat(value)
    60	    except ValueError:
    61	        raise ValueError(f"{field_name} é uma data inválida: {value!r}")
    62	    return value
    63	
    64	
    65	# ---------------------------------------------------------------------------
    66	# StructureLegInput
    67	# ---------------------------------------------------------------------------
    68	@dataclass(frozen=True)
    69	class StructureLegInput:
    70	    """
    71	    Representa uma perna (leg) da estrutura, já normalizada.
    72	
    73	    position_side : LONG | SHORT tecnico; aceita aliases COMPRADO/VENDIDO e C/V
    74	    option_type   : CALL | PUT
    75	    strike        : decimal positivo
    76	    expiration_date: YYYY-MM-DD
    77	    quantity      : inteiro positivo (direção fica em position_side)
    78	    symbol        : código da opção (ex.: BOVAE195) -- opcional
    79	    premium       : preço de entrada -- opcional
    80	    multiplier    : padrão 1.0
    81	    leg_order     : ordem para exibição
    82	    """
    83	    position_side:   str
    84	    option_type:     str
    85	    strike:          float
    86	    expiration_date: str
    87	    quantity:        int
    88	
    89	    symbol:      Optional[str]   = None
    90	    premium:     Optional[float] = None
    91	    multiplier:  float           = 1.0
    92	    leg_order:   int             = 0
    93	    notes:       Optional[str]   = None
    94	
    95	    def __post_init__(self):
    96	        try:
    97	            position_side = to_pricing_engine_side(self.position_side)
    98	        except ValueError as exc:
    99	            raise ValueError(
   100	                f"position_side inválido: {self.position_side!r}. "
   101	                f"Use: {VALID_POSITION_SIDES} ou COMPRADO/VENDIDO"
   102	            ) from exc
   103	
   104	        object.__setattr__(self, "position_side", position_side)
   105	
   106	        if position_side not in VALID_POSITION_SIDES:
   107	            raise ValueError(
   108	                f"position_side inválido: {position_side!r}. "
   109	                f"Use: {VALID_POSITION_SIDES}"
   110	            )
   111	        if self.option_type not in VALID_OPTION_TYPES:
   112	            raise ValueError(
   113	                f"option_type inválido: {self.option_type!r}. "
   114	                f"Use: {VALID_OPTION_TYPES}"
   115	            )
   116	        # strike deve ser positivo
   117	        object.__setattr__(self, "strike", _require_positive(self.strike, "strike"))
   118	        # quantity deve ser inteiro positivo
   119	        if not isinstance(self.quantity, int) or self.quantity <= 0:
   120	            raise ValueError(f"quantity deve ser inteiro positivo, recebeu: {self.quantity!r}")
   121	        # expiration_date: formato canônico
   122	        object.__setattr__(
   123	            self, "expiration_date",
   124	            _require_date_str(self.expiration_date, "expiration_date")
   125	        )
   126	        # multiplier
   127	        if self.multiplier <= 0:
   128	            raise ValueError(f"multiplier deve ser positivo, recebeu: {self.multiplier}")
   129	
   130	
   131	# ---------------------------------------------------------------------------
   132	# StructureInput
   133	# ---------------------------------------------------------------------------
   134	@dataclass(frozen=True)
   135	class StructureInput:
   136	    """
   137	    Representa a estrutura completa pronta para cálculo.
   138	
   139	    structure_id      : PK canônica (INTEGER do DB)
   140	    underlying_asset  : ativo base (ex.: BOVA11)
   141	    legs              : pernas já normalizadas
   142	    name              : label amigável
   143	    alias_legacy_aba  : compatibilidade -- NÃO é chave de cálculo
   144	    """
   145	    structure_id:     int
   146	    underlying_asset: str
   147	    legs:             List[StructureLegInput]
   148	
   149	    name:             Optional[str] = None
   150	    alias_legacy_aba: Optional[str] = None
   151	
   152	    def __post_init__(self):
   153	        if not isinstance(self.structure_id, int) or self.structure_id <= 0:
   154	            raise ValueError(
   155	                f"structure_id deve ser inteiro positivo, recebeu: {self.structure_id!r}"
   156	            )
   157	        _require_nonempty(self.underlying_asset, "underlying_asset")
   158	        if not isinstance(self.legs, list) or len(self.legs) == 0:
   159	            raise ValueError("legs não pode ser lista vazia")
   160	        for i, leg in enumerate(self.legs):
   161	            if not isinstance(leg, StructureLegInput):
   162	                raise TypeError(
   163	                    f"legs[{i}] deve ser StructureLegInput, recebeu: {type(leg)}"
   164	                )
   165	
   166	
   167	# ---------------------------------------------------------------------------
   168	# MarketSnapshotInput
   169	# ---------------------------------------------------------------------------
   170	@dataclass(frozen=True)
   171	class MarketSnapshotInput:
   172	    """
   173	    Representa o estado de mercado no momento do cálculo.
   174	
   175	    snapshot_timestamp : ISO-8601 string (ex.: '2026-06-02T20:49:43')
   176	    underlying_asset   : deve coincidir com StructureInput.underlying_asset
   177	    spot_price         : preço spot positivo
   178	    source             : 'rtd' | 'manual' | 'ui'
   179	    snapshot_id        : referência interna opcional
   180	    """
   181	    snapshot_timestamp: str
   182	    underlying_asset:   str
   183	    spot_price:         float
   184	    source:             str
   185	
   186	    snapshot_id:         Optional[int]   = None
   187	    option_quotes:       Optional[dict]  = None   # bid/ask por símbolo
   188	    greeks:              Optional[dict]  = None
   189	    volatility_context:  Optional[dict]  = None
   190	
   191	    def __post_init__(self):
   192	        _require_nonempty(self.snapshot_timestamp, "snapshot_timestamp")
   193	        _require_nonempty(self.underlying_asset,   "underlying_asset")
   194	        object.__setattr__(
   195	            self, "spot_price",
   196	            _require_positive(self.spot_price, "spot_price")
   197	        )
   198	        if self.source not in VALID_SOURCES:
   199	            raise ValueError(
   200	                f"source inválido: {self.source!r}. Use: {VALID_SOURCES}"
   201	            )
   202	        # Tenta parsear timestamp para garantir que é válido
   203	        try:
   204	            datetime.fromisoformat(self.snapshot_timestamp)
   205	        except ValueError:
   206	            raise ValueError(
   207	                f"snapshot_timestamp não é ISO-8601 válido: {self.snapshot_timestamp!r}"
   208	            )
   209	
   210	
   211	# ---------------------------------------------------------------------------
   212	# CalculationRequest -- envelope completo
   213	# ---------------------------------------------------------------------------
   214	@dataclass(frozen=True)
   215	class CalculationRequest:
   216	    """
   217	    Contrato canônico de entrada para qualquer cálculo de payoff/decisão.
   218	
   219	    O orquestrador monta este objeto a partir do DB e do bridge/RTD,
   220	    e o domínio (payoff, decision) recebe SOMENTE este objeto -- sem
   221	    acessar banco diretamente.
   222	    """
   223	    structure:       StructureInput
   224	    market_snapshot: MarketSnapshotInput
   225	
   226	    def __post_init__(self):
   227	        if self.structure.underlying_asset != self.market_snapshot.underlying_asset:
   228	            raise ValueError(
   229	                f"underlying_asset diverge entre structure "
   230	                f"({self.structure.underlying_asset!r}) "
   231	                f"e market_snapshot ({self.market_snapshot.underlying_asset!r})"
   232	            )
```

## FILE: ATT/tests/test_canonical_pricing_facade_manual_without_alias.py
```python
     1	import services.canonical_pricing_facade as facade_module
     2	
     3	
     4	class FakePricingInputService:
     5	    def __init__(self, *args, **kwargs):
     6	        pass
     7	
     8	    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
     9	        return {
    10	            "structure_id": structure_id,
    11	            "underlying_asset": "BOVA11",
    12	            "reference_date": reference_date,
    13	            "spot_price": 124.66,
    14	            "interest_rate": 0.0,
    15	            "volatility": 0.0,
    16	            "legs": [],
    17	            "meta": {
    18	                "source": "fake_pricing_input_service",
    19	            },
    20	        }
    21	
    22	
    23	class FakePricingExecutionService:
    24	    def execute_payload(self, pricing_payload):
    25	        return {
    26	            "result": {
    27	                "engine": "fake",
    28	                "status": "ok",
    29	                "valuation": {
    30	                    "theoretical_value": 0,
    31	                },
    32	            }
    33	        }
    34	
    35	
    36	class FakePersistenceService:
    37	    def __init__(self):
    38	        self.calls = []
    39	
    40	    def persist_execution(
    41	        self,
    42	        pricing_payload,
    43	        result,
    44	        duration_ms=None,
    45	        error_message=None,
    46	    ):
    47	        self.calls.append(
    48	            {
    49	                "pricing_payload": pricing_payload,
    50	                "result": result,
    51	                "duration_ms": duration_ms,
    52	                "error_message": error_message,
    53	            }
    54	        )
    55	        return {
    56	            "ok": True,
    57	            "structure_id": pricing_payload["structure_id"] if pricing_payload else None,
    58	        }
    59	
    60	
    61	def test_facade_falls_back_to_pricing_input_service_when_alias_legacy_aba_is_null(monkeypatch, tmp_path):
    62	    def fake_get_structure_info(structure_id, db_path):
    63	        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")
    64	
    65	    monkeypatch.setattr(
    66	        facade_module,
    67	        "_get_structure_info",
    68	        fake_get_structure_info,
    69	    )
    70	
    71	    monkeypatch.setattr(
    72	        facade_module,
    73	        "PricingInputService",
    74	        FakePricingInputService,
    75	    )
    76	
    77	    persister = FakePersistenceService()
    78	
    79	    db_path = tmp_path / "app.db"
    80	    db_path.touch()
    81	
    82	    facade = facade_module.CanonicalPricingFacade(
    83	        db_path=db_path,
    84	        pricing_execution_service=FakePricingExecutionService(),
    85	        persistence_service=persister,
    86	    )
    87	
    88	    response = facade.execute_pricing(
    89	        structure_id=2,
    90	        reference_date="2026-06-21",
    91	    )
    92	
    93	    assert response["status"] == "ok"
    94	    assert response["pricing_payload"]["structure_id"] == 2
    95	    assert response["pricing_payload"]["reference_date"] == "2026-06-21"
    96	    assert response["pricing_payload"]["meta"]["snapshot_source"] == "canonical_manual_without_alias"
    97	    assert response["pricing_payload"]["meta"]["alias_legacy_aba"] is None
    98	    assert "alias_legacy_aba is null" in response["pricing_payload"]["meta"]["fallback_reason"]
    99	
   100	    assert len(persister.calls) == 1
   101	    assert persister.calls[0]["pricing_payload"]["structure_id"] == 2
   102	    assert persister.calls[0]["result"]["status"] == "ok"
```

## FILE: ATT/tests/test_canonical_pricing_facade.py
```python
     1	import sqlite3
     2	from types import SimpleNamespace
     3	
     4	import pytest
     5	
     6	from services.canonical_pricing_facade import _snapshot_result_to_payload
     7	
     8	
     9	def _selection(**overrides):
    10	    defaults = {
    11	        "legs": [],
    12	        "spot_price": 124.66,
    13	        "source": "rtd",
    14	        "aba": "ABA_LEGADA_NAO_E_UNDERLYING",
    15	        "manual_overrides": [],
    16	    }
    17	    defaults.update(overrides)
    18	    return SimpleNamespace(**defaults)
    19	
    20	
    21	@pytest.mark.parametrize(
    22	    "raw_numeric, expected",
    23	    [
    24	        ("R$ 1.234,56", 1234.56),
    25	        ("1.234,56", 1234.56),
    26	        ("1,234.56", 1234.56),
    27	        ("R$ 124,66", 124.66),
    28	    ],
    29	)
    30	def test_snapshot_result_to_payload_normalizes_common_rtd_number_formats(
    31	    tmp_path,
    32	    raw_numeric,
    33	    expected,
    34	):
    35	    payload = _snapshot_result_to_payload(
    36	        selection_result=_selection(
    37	            spot_price=raw_numeric,
    38	            legs=[
    39	                {
    40	                    "quantity": "100",
    41	                    "price": raw_numeric,
    42	                    "asset": "ABCD100",
    43	                    "strike": raw_numeric,
    44	                }
    45	            ],
    46	        ),
    47	        structure_id=15,
    48	        underlying_asset="ABCD11",
    49	        reference_date="2026-06-19",
    50	        db_path=tmp_path / "app.db",
    51	    )
    52	
    53	    assert payload["spot_price"] == pytest.approx(expected)
    54	
    55	    leg = payload["legs"][0]
    56	    assert leg["price"] == pytest.approx(expected)
    57	    assert leg["premium"] == pytest.approx(expected)
    58	    assert leg["strike"] == pytest.approx(expected)
    59	
    60	
    61	def test_snapshot_result_to_payload_uses_explicit_underlying_asset_not_legacy_aba(tmp_path):
    62	    selection = _selection(
    63	        aba="SMAL11_ABA_LEGADA",
    64	        legs=[
    65	            {
    66	                "quantity": "-100",
    67	                "price": "R$ 1,25",
    68	                "asset": "SMALF100",
    69	                "option_type": "CALL",
    70	                "strike": "100,00",
    71	                "expiry": "2026-07-17T12:00:00",
    72	                "source": "rtd_option_quotes",
    73	            }
    74	        ],
    75	        spot_price="124,66",
    76	        manual_overrides=["price"],
    77	    )
    78	
    79	    payload = _snapshot_result_to_payload(
    80	        selection_result=selection,
    81	        structure_id=10,
    82	        underlying_asset="SMAL11",
    83	        reference_date="2026-06-19",
    84	        db_path=tmp_path / "app.db",
    85	    )
    86	
    87	    assert payload["structure_id"] == 10
    88	    assert payload["underlying_asset"] == "SMAL11"
    89	    assert payload["reference_date"] == "2026-06-19"
    90	    assert payload["spot_price"] == 124.66
    91	
    92	    assert payload["meta"] == {
    93	        "snapshot_source": "rtd",
    94	        "snapshot_aba": "SMAL11_ABA_LEGADA",
    95	        "manual_overrides": ["price"],
    96	        "legs_count": 1,
    97	    }
    98	
    99	    leg = payload["legs"][0]
   100	    assert leg["asset"] == "SMALF100"
   101	    assert leg["symbol"] == "SMALF100"
   102	    assert leg["price"] == 1.25
   103	    assert leg["premium"] == 1.25
   104	    assert leg["strike"] == 100.0
   105	    assert leg["expiry"] == "2026-07-17T12:00:00"
   106	    assert leg["expiration_date"] == "2026-07-17"
   107	    assert leg["side"] == "SHORT"
   108	    assert leg["position_side"] == "SHORT"
   109	    assert leg["source"] == "rtd_option_quotes"
   110	
   111	
   112	@pytest.mark.parametrize(
   113	    "leg_input, expected_side",
   114	    [
   115	        ({"quantity": "100", "price": 2.5, "asset": "ABCD100"}, "LONG"),
   116	        ({"quantity": "-100", "price": 2.5, "asset": "ABCD100"}, "SHORT"),
   117	        ({"quantity": "100", "price": 2.5, "asset": "ABCD100", "side": "short"}, "SHORT"),
   118	        ({"quantity": "-100", "price": 2.5, "asset": "ABCD100", "position_side": "long"}, "LONG"),
   119	    ],
   120	)
   121	def test_snapshot_result_to_payload_side_matrix(tmp_path, leg_input, expected_side):
   122	    payload = _snapshot_result_to_payload(
   123	        selection_result=_selection(legs=[leg_input]),
   124	        structure_id=20,
   125	        underlying_asset="ABCD11",
   126	        reference_date=None,
   127	        db_path=tmp_path / "app.db",
   128	    )
   129	
   130	    leg = payload["legs"][0]
   131	    assert leg["side"] == expected_side
   132	    assert leg["position_side"] == expected_side
   133	
   134	
   135	def test_snapshot_result_to_payload_uses_spot_fallback_from_database(tmp_path):
   136	    db_path = tmp_path / "app.db"
   137	
   138	    with sqlite3.connect(str(db_path)) as conn:
   139	        conn.execute("CREATE TABLE market_prices (underlying_asset TEXT, spot REAL)")
   140	        conn.execute(
   141	            "INSERT INTO market_prices (underlying_asset, spot) VALUES (?, ?)",
   142	            ("SMAL11", 124.66),
   143	        )
   144	        conn.commit()
   145	
   146	    payload = _snapshot_result_to_payload(
   147	        selection_result=_selection(spot_price=0, legs=[]),
   148	        structure_id=30,
   149	        underlying_asset="SMAL11",
   150	        reference_date="2026-06-19",
   151	        db_path=db_path,
   152	    )
   153	
   154	    assert payload["spot_price"] == 124.66
   155	    assert payload["legs"] == []
   156	    assert payload["meta"]["legs_count"] == 0
   157	
   158	
   159	def test_snapshot_result_to_payload_rejects_missing_or_invalid_spot(tmp_path):
   160	    with pytest.raises(ValueError) as exc:
   161	        _snapshot_result_to_payload(
   162	            selection_result=_selection(spot_price=0, legs=[]),
   163	            structure_id=40,
   164	            underlying_asset="SMAL11",
   165	            reference_date="2026-06-19",
   166	            db_path=tmp_path / "app.db",
   167	        )
   168	
   169	    assert "spot_price inválido ou ausente para underlying_asset=SMAL11" in str(exc.value)
   170	    assert "Não persistir execução OK com spot_price <= 0" in str(exc.value)
```

## FILE: ATT/tests/test_canonical_input_service.py
```python
     1	import unittest
     2	
     3	from services.canonical_input_service import CanonicalInputService
     4	
     5	
     6	class FakeRepository:
     7	    def __init__(self, structure):
     8	        self.structure = structure
     9	
    10	    def get_structure(self, structure_id):
    11	        if self.structure and self.structure.get("id") == structure_id:
    12	            return self.structure
    13	        return None
    14	
    15	
    16	class FakeMarketSnapshotProvider:
    17	    def get_snapshot(self, underlying_asset, reference_date=None):
    18	        return {
    19	            "reference_date": reference_date or "2026-05-18",
    20	            "underlying_asset": underlying_asset,
    21	            "spot_price": 198.35,
    22	            "interest_rate": 0.1175,
    23	            "volatility": 0.22,
    24	        }
    25	
    26	
    27	class FakeStatus:
    28	    def __init__(self, chosen_ts):
    29	        self.chosen_ts = chosen_ts
    30	
    31	
    32	class FakeRoboRepo:
    33	    def __init__(self, timestamps):
    34	        self._timestamps = timestamps
    35	
    36	    def list_timestamps(self, aba):
    37	        return self._timestamps
    38	
    39	
    40	class FakeRoboLegsService:
    41	    def __init__(self, timestamps=None, legs=None):
    42	        self.repo = FakeRoboRepo(timestamps or [])
    43	        self._timestamps = timestamps or []
    44	        self._legs = legs or []
    45	
    46	    def status(self, aba, requested_timestamp):
    47	        if self._timestamps:
    48	            return FakeStatus(self._timestamps[0])
    49	        return FakeStatus(None)
    50	
    51	    def get_legs(self, aba, timestamp, validate=False):
    52	        if timestamp is None:
    53	            return []
    54	        return self._legs
    55	
    56	
    57	
    58	class FakeLegacyFallback:
    59	    def __init__(self, legs, meta):
    60	        self._legs = legs
    61	        self._meta = meta
    62	
    63	    def load(self, structure, reference_date):
    64	        return self._legs, self._meta
    65	
    66	
    67	class CanonicalInputServiceTests(unittest.TestCase):
    68	    def test_should_always_prefer_canonical_legs_when_structure_already_has_legs(self):
    69	        structure = {
    70	            "id": 7,
    71	            "name": "BOVA11 Condor Maio/2026",
    72	            "underlying_asset": "BOVA11",
    73	            "alias_legacy_aba": "BOVA11",
    74	            "legs": [
    75	                {
    76	                    "position_side": "LONG",
    77	                    "option_type": "CALL",
    78	                    "symbol": "BOVAE195",
    79	                    "strike": 195.0,
    80	                    "expiration_date": "2026-05-15",
    81	                    "quantity": 5000,
    82	                    "premium": None,
    83	                    "multiplier": 1.0,
    84	                }
    85	            ],
    86	        }
    87	
    88	        service = CanonicalInputService(
    89	            repository=FakeRepository(structure),
    90	            market_snapshot_provider=FakeMarketSnapshotProvider(),
    91	            robo_legs_service=FakeRoboLegsService(
    92	                timestamps=["2026-05-18 10:00:00"],
    93	                legs=[{"any": "value"}],
    94	            ),
    95	            prefer_canonical_legs=True,
    96	            enable_legacy_legs_fallback=True,
    97	        )
    98	
    99	        result = service.build_structure_market_input(
   100	            structure_id=7,
   101	            reference_date="2026-05-18",
   102	        )
   103	
   104	        self.assertEqual(result["meta"]["legs_source"], "canonical")
   105	        self.assertNotIn("legacy_timestamp", result["meta"])
   106	        self.assertEqual(len(result["structure"]["legs"]), 1)
   107	        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
   108	        self.assertNotIn("alias_legacy_aba", result["structure"])
   109	
   110	    def test_should_use_legacy_robo_only_when_no_canonical_legs_exist(self):
   111	        structure = {
   112	            "id": 7,
   113	            "name": "BOVA11 Condor Maio/2026",
   114	            "underlying_asset": "BOVA11",
   115	            "alias_legacy_aba": "BOVA11",
   116	            "legs": [],
   117	        }
   118	
   119	        service = CanonicalInputService(
   120	            repository=FakeRepository(structure),
   121	            market_snapshot_provider=FakeMarketSnapshotProvider(),
   122	            robo_legs_service=FakeRoboLegsService(
   123	                timestamps=["2026-05-18 10:00:00"],
   124	                legs=[
   125	                    {
   126	                        "position_side": "LONG",
   127	                        "option_type": "CALL",
   128	                        "symbol": "BOVAE195",
   129	                        "strike": 195.0,
   130	                        "expiration_date": "2026-05-15",
   131	                        "quantity": 5000,
   132	                        "premium": None,
   133	                        "multiplier": 1.0,
   134	                    }
   135	                ],
   136	            ),
   137	            enable_legacy_legs_fallback=True,
   138	        )
   139	
   140	        result = service.build_structure_market_input(
   141	            structure_id=7,
   142	            reference_date="2026-05-18",
   143	        )
   144	
   145	        self.assertEqual(result["meta"]["legs_source"], "legacy_fallback")
   146	        self.assertEqual(result["meta"]["legacy_timestamp"], "2026-05-18 10:00:00")
   147	        self.assertEqual(result["meta"]["legacy_aba"], "BOVA11")
   148	        self.assertEqual(result["meta"]["legacy_key_source"], "alias_legacy_aba")
   149	        self.assertEqual(len(result["structure"]["legs"]), 1)
   150	        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
   151	        self.assertNotIn("alias_legacy_aba", result["structure"])
   152	
   153	    def test_should_return_empty_when_no_canonical_legs_and_fallback_disabled(self):
   154	        structure = {
   155	            "id": 7,
   156	            "name": "BOVA11 Condor Maio/2026",
   157	            "underlying_asset": "BOVA11",
   158	            "alias_legacy_aba": "BOVA11",
   159	            "legs": [],
   160	        }
   161	
   162	        service = CanonicalInputService(
   163	            repository=FakeRepository(structure),
   164	            market_snapshot_provider=FakeMarketSnapshotProvider(),
   165	            robo_legs_service=FakeRoboLegsService(
   166	                timestamps=["2026-05-18 10:00:00"],
   167	                legs=[],
   168	            ),
   169	            enable_legacy_legs_fallback=False,
   170	        )
   171	
   172	        result = service.build_structure_market_input(
   173	            structure_id=7,
   174	            reference_date="2026-05-18",
   175	        )
   176	
   177	        self.assertEqual(result["meta"]["legs_source"], "empty")
   178	        self.assertNotIn("legacy_timestamp", result["meta"])
   179	        self.assertEqual(result["structure"]["legs"], [])
   180	        self.assertNotIn("alias_legacy_aba", result["structure"])
   181	
   182	
   183	    def test_should_return_empty_when_legacy_fallback_returns_no_legs(self):
   184	        structure = {
   185	            "id": 7,
   186	            "name": "BOVA11 Condor Maio/2026",
   187	            "underlying_asset": "BOVA11",
   188	            "alias_legacy_aba": "BOVA11",
   189	            "legs": [],
   190	        }
   191	
   192	        service = CanonicalInputService(
   193	            repository=FakeRepository(structure),
   194	            market_snapshot_provider=FakeMarketSnapshotProvider(),
   195	            prefer_canonical_legs=True,
   196	            enable_legacy_legs_fallback=True,
   197	        )
   198	
   199	        service.legacy_robo_legs_fallback = FakeLegacyFallback(
   200	            legs=[],
   201	            meta={"fallback_reason": "no_legacy_legs_found"},
   202	        )
   203	
   204	        enriched, meta = service._enrich_structure_with_legs(
   205	            structure=structure,
   206	            reference_date="2026-05-18",
   207	        )
   208	
   209	        self.assertEqual(enriched["legs"], [])
   210	        self.assertEqual(meta["legs_source"], "empty")
   211	        self.assertEqual(meta["fallback_reason"], "no_legacy_legs_found")
   212	
   213	    def test_should_enrich_market_with_internal_structure_metrics(self):
   214	        structure = {
   215	            "id": 7,
   216	            "name": "BOVA11 Condor Maio/2026",
   217	            "underlying_asset": "BOVA11",
   218	            "alias_legacy_aba": "BOVA11",
   219	            "legs": [
   220	                {
   221	                    "position_side": "LONG",
   222	                    "option_type": "PUT",
   223	                    "symbol": "BOVAM190",
   224	                    "strike": 190.0,
   225	                    "expiration_date": "2026-05-20",
   226	                    "quantity": 10,
   227	                    "premium": 1.00,
   228	                    "bid": 1.20,
   229	                    "ask": 1.40,
   230	                    "delta": 0.40,
   231	                    "gamma": 0.01,
   232	                    "theta": -0.02,
   233	                    "vega": 0.03,
   234	                    "multiplier": 1.0,
   235	                },
   236	                {
   237	                    "position_side": "SHORT",
   238	                    "option_type": "PUT",
   239	                    "symbol": "BOVAM185",
   240	                    "strike": 185.0,
   241	                    "expiration_date": "2026-05-17",
   242	                    "quantity": 10,
   243	                    "premium": 0.85,
   244	                    "bid": 0.70,
   245	                    "ask": 0.80,
   246	                    "delta": 0.40,
   247	                    "gamma": 0.01,
   248	                    "theta": -0.02,
   249	                    "vega": 0.03,
   250	                    "multiplier": 1.0,
   251	                },
   252	            ],
   253	        }
   254	
   255	        service = CanonicalInputService(
   256	            repository=FakeRepository(structure),
   257	            market_snapshot_provider=FakeMarketSnapshotProvider(),
   258	            robo_legs_service=FakeRoboLegsService(),
   259	            prefer_canonical_legs=True,
   260	            enable_legacy_legs_fallback=True,
   261	        )
   262	
   263	        result = service.build_structure_market_input(
   264	            structure_id=7,
   265	            reference_date="2026-05-15",
   266	        )
   267	
   268	        expected_spread_pct_medio = ((0.20 / 1.30) + (0.10 / 0.75)) / 2
   269	
   270	        self.assertEqual(result["market"]["dte_min"], 2)
   271	        self.assertAlmostEqual(result["market"]["pl_realista_total"], 4.0)
   272	        self.assertAlmostEqual(result["market"]["delta_liq"], 0.0)
   273	        self.assertAlmostEqual(result["market"]["gamma_liq"], 0.0)
   274	        self.assertAlmostEqual(result["market"]["theta_liq"], 0.0)
   275	        self.assertAlmostEqual(result["market"]["vega_liq"], 0.0)
   276	        self.assertAlmostEqual(result["market"]["spread_medio"], 0.15)
   277	        self.assertAlmostEqual(
   278	            result["market"]["spread_pct_medio"],
   279	            expected_spread_pct_medio,
   280	        )
   281	        self.assertEqual(result["meta"]["structure_metrics_source"], "internal_engine")
   282	
   283	    def test_should_keep_internal_metric_fields_as_none_when_no_legs(self):
   284	        structure = {
   285	            "id": 7,
   286	            "name": "BOVA11 Condor Maio/2026",
   287	            "underlying_asset": "BOVA11",
   288	            "alias_legacy_aba": "BOVA11",
   289	            "legs": [],
   290	        }
   291	
   292	        service = CanonicalInputService(
   293	            repository=FakeRepository(structure),
   294	            market_snapshot_provider=FakeMarketSnapshotProvider(),
   295	            robo_legs_service=FakeRoboLegsService(),
   296	            prefer_canonical_legs=True,
   297	            enable_legacy_legs_fallback=False,
   298	        )
   299	
   300	        result = service.build_structure_market_input(
   301	            structure_id=7,
   302	            reference_date="2026-05-15",
   303	        )
   304	
   305	        self.assertIsNone(result["market"]["dte_min"])
   306	        self.assertIsNone(result["market"]["pl_realista_total"])
   307	        self.assertIsNone(result["market"]["delta_liq"])
   308	        self.assertIsNone(result["market"]["gamma_liq"])
   309	        self.assertIsNone(result["market"]["theta_liq"])
   310	        self.assertIsNone(result["market"]["vega_liq"])
   311	        self.assertIsNone(result["market"]["spread_medio"])
   312	        self.assertIsNone(result["market"]["spread_pct_medio"])
   313	        self.assertEqual(result["meta"]["structure_metrics_source"], "internal_engine")
   314	
   315	
   316	
   317	if __name__ == "__main__":
   318	    unittest.main()
```

## FILE: ATT/tests/test_pricing_input_service.py
```python
     1	import pytest
     2	
     3	from services.pricing_input_service import PricingInputService
     4	
     5	
     6	class FakeCanonicalInputService:
     7	    def __init__(self, canonical_input=None, error=None):
     8	        self.canonical_input = canonical_input
     9	        self.error = error
    10	        self.calls = []
    11	
    12	    def build_structure_market_input(self, structure_id: int, reference_date: str | None = None):
    13	        self.calls.append(
    14	            {
    15	                "structure_id": structure_id,
    16	                "reference_date": reference_date,
    17	            }
    18	        )
    19	
    20	        if self.error is not None:
    21	            raise self.error
    22	
    23	        return self.canonical_input
    24	
    25	
    26	def test_build_pricing_payload_calls_canonical_input_service(monkeypatch):
    27	    canonical_input = {
    28	        "structure": {
    29	            "structure_id": 123,
    30	            "name": "Fence BOVA11",
    31	            "underlying_asset": "BOVA11",
    32	            "legs": [],
    33	        },
    34	        "market": {
    35	            "reference_date": "2026-05-16",
    36	            "underlying_asset": "BOVA11",
    37	            "spot_price": 198.35,
    38	            "interest_rate": 0.1175,
    39	            "volatility": 0.22,
    40	        },
    41	    }
    42	
    43	    fake_canonical_service = FakeCanonicalInputService(canonical_input)
    44	
    45	    def fake_to_pricing_payload(value):
    46	        return {
    47	            "structure_id": value["structure"]["structure_id"],
    48	            "reference_date": value["market"]["reference_date"],
    49	            "payload_source": "fake_adapter",
    50	        }
    51	
    52	    monkeypatch.setattr(
    53	        "services.pricing_input_service.to_pricing_payload",
    54	        fake_to_pricing_payload,
    55	    )
    56	
    57	    service = PricingInputService(canonical_input_service=fake_canonical_service)
    58	
    59	    result = service.build_pricing_payload(
    60	        structure_id=123,
    61	        reference_date="2026-05-16",
    62	    )
    63	
    64	    assert fake_canonical_service.calls == [
    65	        {
    66	            "structure_id": 123,
    67	            "reference_date": "2026-05-16",
    68	        }
    69	    ]
    70	    assert result == {
    71	        "structure_id": 123,
    72	        "reference_date": "2026-05-16",
    73	        "payload_source": "fake_adapter",
    74	    }
    75	
    76	
    77	def test_build_pricing_payload_from_canonical_input_delegates_to_adapter(monkeypatch):
    78	    canonical_input = {
    79	        "structure": {"structure_id": 999},
    80	        "market": {"reference_date": "2026-05-17"},
    81	    }
    82	
    83	    calls = []
    84	
    85	    def fake_to_pricing_payload(value):
    86	        calls.append(value)
    87	        return {"ok": True, "structure_id": 999}
    88	
    89	    monkeypatch.setattr(
    90	        "services.pricing_input_service.to_pricing_payload",
    91	        fake_to_pricing_payload,
    92	    )
    93	
    94	    service = PricingInputService(canonical_input_service=None)
    95	
    96	    result = service.build_pricing_payload_from_canonical_input(canonical_input)
    97	
    98	    assert calls == [canonical_input]
    99	    assert result == {"ok": True, "structure_id": 999}
   100	
   101	
   102	def test_build_pricing_payload_passes_none_reference_date(monkeypatch):
   103	    canonical_input = {
   104	        "structure": {"structure_id": 321},
   105	        "market": {"reference_date": "2026-05-18"},
   106	    }
   107	
   108	    fake_canonical_service = FakeCanonicalInputService(canonical_input)
   109	
   110	    def fake_to_pricing_payload(value):
   111	        return {
   112	            "structure_id": value["structure"]["structure_id"],
   113	            "reference_date": value["market"]["reference_date"],
   114	        }
   115	
   116	    monkeypatch.setattr(
   117	        "services.pricing_input_service.to_pricing_payload",
   118	        fake_to_pricing_payload,
   119	    )
   120	
   121	    service = PricingInputService(canonical_input_service=fake_canonical_service)
   122	
   123	    result = service.build_pricing_payload(structure_id=321)
   124	
   125	    assert fake_canonical_service.calls == [
   126	        {
   127	            "structure_id": 321,
   128	            "reference_date": None,
   129	        }
   130	    ]
   131	    assert result == {
   132	        "structure_id": 321,
   133	        "reference_date": "2026-05-18",
   134	    }
   135	
   136	
   137	def test_build_pricing_payload_propagates_canonical_input_service_error(monkeypatch):
   138	    fake_canonical_service = FakeCanonicalInputService(
   139	        error=ValueError("structure not found: 404")
   140	    )
   141	
   142	    adapter_calls = []
   143	
   144	    def fake_to_pricing_payload(value):
   145	        adapter_calls.append(value)
   146	        return {"should_not_happen": True}
   147	
   148	    monkeypatch.setattr(
   149	        "services.pricing_input_service.to_pricing_payload",
   150	        fake_to_pricing_payload,
   151	    )
   152	
   153	    service = PricingInputService(canonical_input_service=fake_canonical_service)
   154	
   155	    with pytest.raises(ValueError, match="structure not found: 404"):
   156	        service.build_pricing_payload(structure_id=404)
   157	
   158	    assert fake_canonical_service.calls == [
   159	        {
   160	            "structure_id": 404,
   161	            "reference_date": None,
   162	        }
   163	    ]
   164	    assert adapter_calls == []
   165	
   166	
   167	def test_build_pricing_payload_from_canonical_input_propagates_adapter_error(monkeypatch):
   168	    canonical_input = {
   169	        "structure": {"structure_id": 888},
   170	        "market": {"reference_date": "2026-05-19"},
   171	    }
   172	
   173	    def fake_to_pricing_payload(value):
   174	        raise ValueError("invalid canonical input")
   175	
   176	    monkeypatch.setattr(
   177	        "services.pricing_input_service.to_pricing_payload",
   178	        fake_to_pricing_payload,
   179	    )
   180	
   181	    service = PricingInputService(canonical_input_service=None)
   182	
   183	    with pytest.raises(ValueError, match="invalid canonical input"):
   184	        service.build_pricing_payload_from_canonical_input(canonical_input)
```

## FILE: ATT/tests/test_pricing_payload_adapter.py
```python
     1	import unittest
     2	
     3	from services.pricing_payload_adapter import to_pricing_payload
     4	
     5	
     6	class PricingPayloadAdapterTests(unittest.TestCase):
     7	    def test_should_not_include_alias_legacy_aba_in_pricing_payload(self):
     8	        canonical_input = {
     9	            "structure": {
    10	                "structure_id": 7,
    11	                "name": "BOVA11 Condor Maio/2026",
    12	                "underlying_asset": "BOVA11",
    13	                "alias_legacy_aba": "BOVA11",
    14	                "legs": [
    15	                    {
    16	                        "position_side": "LONG",
    17	                        "option_type": "CALL",
    18	                        "symbol": "BOVAE195",
    19	                        "strike": 195.0,
    20	                        "expiration_date": "2026-05-15",
    21	                        "quantity": 5000,
    22	                        "premium": None,
    23	                        "multiplier": 1.0,
    24	                    }
    25	                ],
    26	            },
    27	            "market": {
    28	                "reference_date": "2026-05-18",
    29	                "spot_price": 198.35,
    30	                "interest_rate": 0.1175,
    31	                "volatility": 0.22,
    32	            },
    33	        }
    34	
    35	        payload = to_pricing_payload(canonical_input)
    36	
    37	        self.assertEqual(payload["structure_id"], 7)
    38	        self.assertEqual(payload["underlying_asset"], "BOVA11")
    39	        self.assertNotIn("alias_legacy_aba", payload)
    40	
    41	    def test_should_map_legs_to_pricing_shape(self):
    42	        canonical_input = {
    43	            "structure": {
    44	                "structure_id": 7,
    45	                "name": "BOVA11 Condor Maio/2026",
    46	                "underlying_asset": "BOVA11",
    47	                "legs": [
    48	                    {
    49	                        "position_side": "short",
    50	                        "option_type": "put",
    51	                        "symbol": "bovaq195",
    52	                        "strike": 195,
    53	                        "expiration_date": "2026-05-15",
    54	                        "quantity": 4000,
    55	                        "premium": 1.25,
    56	                        "multiplier": 1,
    57	                    }
    58	                ],
    59	            },
    60	            "market": {
    61	                "reference_date": "2026-05-18",
    62	                "spot_price": 198.35,
    63	                "interest_rate": 0.1175,
    64	                "volatility": 0.22,
    65	            },
    66	        }
    67	
    68	        payload = to_pricing_payload(canonical_input)
    69	
    70	        self.assertEqual(len(payload["legs"]), 1)
    71	        self.assertEqual(payload["legs"][0]["side"], "SHORT")
    72	        self.assertEqual(payload["legs"][0]["option_type"], "PUT")
    73	        self.assertEqual(payload["legs"][0]["symbol"], "BOVAQ195")
    74	        self.assertEqual(payload["legs"][0]["instrument_type"], "OPTION")
    75	
    76	
    77	    def test_should_convert_position_side_to_pricing_technical_side(self):
    78	        cases = [
    79	            ("COMPRADO", "LONG"),
    80	            ("VENDIDO", "SHORT"),
    81	            ("C", "LONG"),
    82	            ("V", "SHORT"),
    83	            ("long", "LONG"),
    84	            ("short", "SHORT"),
    85	        ]
    86	
    87	        for raw_side, expected_side in cases:
    88	            with self.subTest(raw_side=raw_side):
    89	                canonical_input = {
    90	                    "structure": {
    91	                        "structure_id": 7,
    92	                        "name": "BOVA11 Condor Maio/2026",
    93	                        "underlying_asset": "BOVA11",
    94	                        "legs": [
    95	                            {
    96	                                "position_side": raw_side,
    97	                                "option_type": "CALL",
    98	                                "symbol": "BOVAE195",
    99	                                "strike": 195.0,
   100	                                "expiration_date": "2026-05-15",
   101	                                "quantity": 5000,
   102	                                "premium": None,
   103	                                "multiplier": 1.0,
   104	                            }
   105	                        ],
   106	                    },
   107	                    "market": {
   108	                        "reference_date": "2026-05-18",
   109	                        "spot_price": 198.35,
   110	                        "interest_rate": 0.1175,
   111	                        "volatility": 0.22,
   112	                    },
   113	                }
   114	
   115	                payload = to_pricing_payload(canonical_input)
   116	
   117	                self.assertEqual(payload["legs"][0]["side"], expected_side)
   118	
   119	
   120	if __name__ == "__main__":
   121	    unittest.main()
```

## FILE: ATT/tests/test_structure_input_mapper.py
```python
     1	from services.structure_input_mapper import to_structure_input
     2	
     3	
     4	def test_to_structure_input_should_not_expose_alias_legacy_aba():
     5	    structure = {
     6	        "id": 7,
     7	        "name": "  BOVA11 Condor Maio/2026  ",
     8	        "underlying_asset": " bova11 ",
     9	        "alias_legacy_aba": "BOVA11",
    10	        "legs": [
    11	            {
    12	                "position_side": "long",
    13	                "option_type": "call",
    14	                "symbol": " bovae195 ",
    15	                "strike": 195.0,
    16	                "expiration_date": " 2026-05-15 ",
    17	                "quantity": 5000,
    18	                "premium": None,
    19	                "multiplier": 1.0,
    20	            }
    21	        ],
    22	    }
    23	
    24	    result = to_structure_input(structure)
    25	
    26	    assert result["structure_id"] == 7
    27	    assert result["name"] == "BOVA11 Condor Maio/2026"
    28	    assert result["underlying_asset"] == "BOVA11"
    29	    assert "alias_legacy_aba" not in result
    30	    assert len(result["legs"]) == 1
    31	    assert result["legs"][0]["position_side"] == "COMPRADO"
    32	    assert result["legs"][0]["option_type"] == "CALL"
    33	    assert result["legs"][0]["symbol"] == "BOVAE195"
```

## FILE: ATT/tests/test_structure_market_input_assembler.py
```python
     1	import unittest
     2	
     3	from services.structure_market_input_assembler import assemble_structure_market_input
     4	
     5	
     6	class StructureMarketInputAssemblerTests(unittest.TestCase):
     7	    def test_should_assemble_structure_and_market_input(self):
     8	        structure = {
     9	            "id": 7,
    10	            "name": "BOVA11 Condor Maio/2026",
    11	            "underlying_asset": "BOVA11",
    12	            "alias_legacy_aba": "BOVA11",
    13	            "legs": [
    14	                {
    15	                    "position_side": "LONG",
    16	                    "option_type": "CALL",
    17	                    "symbol": "BOVAE195",
    18	                    "strike": 195.0,
    19	                    "expiration_date": "2026-05-15",
    20	                    "quantity": 5000,
    21	                    "premium": None,
    22	                    "multiplier": 1.0,
    23	                }
    24	            ],
    25	        }
    26	
    27	        market_snapshot = {
    28	            "reference_date": "2026-05-18",
    29	            "underlying_asset": "BOVA11",
    30	            "spot_price": 198.35,
    31	            "interest_rate": 0.1175,
    32	            "volatility": 0.22,
    33	        }
    34	
    35	        result = assemble_structure_market_input(structure, market_snapshot)
    36	
    37	        self.assertIn("structure", result)
    38	        self.assertIn("market", result)
    39	        self.assertIn("meta", result)
    40	
    41	        self.assertEqual(result["structure"]["underlying_asset"], "BOVA11")
    42	        self.assertEqual(result["market"]["underlying_asset"], "BOVA11")
    43	        self.assertEqual(result["market"]["reference_date"], "2026-05-18")
    44	        self.assertEqual(result["meta"]["input_source"], "structure_market_input_assembler")
    45	
    46	    def test_should_raise_when_underlying_asset_mismatches(self):
    47	        structure = {
    48	            "id": 7,
    49	            "name": "BOVA11 Condor Maio/2026",
    50	            "underlying_asset": "BOVA11",
    51	            "legs": [],
    52	        }
    53	
    54	        market_snapshot = {
    55	            "reference_date": "2026-05-18",
    56	            "underlying_asset": "PETR4",
    57	            "spot_price": 198.35,
    58	            "interest_rate": 0.1175,
    59	            "volatility": 0.22,
    60	        }
    61	
    62	        with self.assertRaises(ValueError) as ctx:
    63	            assemble_structure_market_input(structure, market_snapshot)
    64	
    65	        self.assertIn("underlying_asset mismatch", str(ctx.exception))
    66	
    67	    def test_should_raise_when_structure_is_missing(self):
    68	        market_snapshot = {
    69	            "reference_date": "2026-05-18",
    70	            "underlying_asset": "BOVA11",
    71	            "spot_price": 198.35,
    72	            "interest_rate": 0.1175,
    73	            "volatility": 0.22,
    74	        }
    75	
    76	        with self.assertRaises(ValueError) as ctx:
    77	            assemble_structure_market_input({}, market_snapshot)
    78	
    79	        self.assertIn("structure is required", str(ctx.exception))
    80	
    81	    def test_should_raise_when_market_snapshot_is_missing(self):
    82	        structure = {
    83	            "id": 7,
    84	            "name": "BOVA11 Condor Maio/2026",
    85	            "underlying_asset": "BOVA11",
    86	            "legs": [],
    87	        }
    88	
    89	        with self.assertRaises(ValueError) as ctx:
    90	            assemble_structure_market_input(structure, {})
    91	
    92	        self.assertIn("market_snapshot is required", str(ctx.exception))
    93	
    94	
    95	if __name__ == "__main__":
    96	    unittest.main()
```

## Coleta dos testes Fase 3
ATT/tests/test_canonical_pricing_facade_manual_without_alias.py::test_facade_falls_back_to_pricing_input_service_when_alias_legacy_aba_is_null
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_normalizes_common_rtd_number_formats[R$ 1.234,56-1234.56]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_normalizes_common_rtd_number_formats[1.234,56-1234.56]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_normalizes_common_rtd_number_formats[1,234.56-1234.56]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_normalizes_common_rtd_number_formats[R$ 124,66-124.66]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_uses_explicit_underlying_asset_not_legacy_aba
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_side_matrix[leg_input0-LONG]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_side_matrix[leg_input1-SHORT]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_side_matrix[leg_input2-SHORT]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_side_matrix[leg_input3-LONG]
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_uses_spot_fallback_from_database
ATT/tests/test_canonical_pricing_facade.py::test_snapshot_result_to_payload_rejects_missing_or_invalid_spot
ATT/tests/test_canonical_input_service.py::CanonicalInputServiceTests::test_should_always_prefer_canonical_legs_when_structure_already_has_legs
ATT/tests/test_canonical_input_service.py::CanonicalInputServiceTests::test_should_enrich_market_with_internal_structure_metrics
ATT/tests/test_canonical_input_service.py::CanonicalInputServiceTests::test_should_keep_internal_metric_fields_as_none_when_no_legs
ATT/tests/test_canonical_input_service.py::CanonicalInputServiceTests::test_should_return_empty_when_legacy_fallback_returns_no_legs
ATT/tests/test_canonical_input_service.py::CanonicalInputServiceTests::test_should_return_empty_when_no_canonical_legs_and_fallback_disabled
ATT/tests/test_canonical_input_service.py::CanonicalInputServiceTests::test_should_use_legacy_robo_only_when_no_canonical_legs_exist
ATT/tests/test_pricing_input_service.py::test_build_pricing_payload_calls_canonical_input_service
ATT/tests/test_pricing_input_service.py::test_build_pricing_payload_from_canonical_input_delegates_to_adapter
ATT/tests/test_pricing_input_service.py::test_build_pricing_payload_passes_none_reference_date
ATT/tests/test_pricing_input_service.py::test_build_pricing_payload_propagates_canonical_input_service_error
ATT/tests/test_pricing_input_service.py::test_build_pricing_payload_from_canonical_input_propagates_adapter_error
ATT/tests/test_pricing_payload_adapter.py::PricingPayloadAdapterTests::test_should_convert_position_side_to_pricing_technical_side
ATT/tests/test_pricing_payload_adapter.py::PricingPayloadAdapterTests::test_should_map_legs_to_pricing_shape
ATT/tests/test_pricing_payload_adapter.py::PricingPayloadAdapterTests::test_should_not_include_alias_legacy_aba_in_pricing_payload
ATT/tests/test_structure_input_mapper.py::test_to_structure_input_should_not_expose_alias_legacy_aba
ATT/tests/test_structure_market_input_assembler.py::StructureMarketInputAssemblerTests::test_should_assemble_structure_and_market_input
ATT/tests/test_structure_market_input_assembler.py::StructureMarketInputAssemblerTests::test_should_raise_when_market_snapshot_is_missing
ATT/tests/test_structure_market_input_assembler.py::StructureMarketInputAssemblerTests::test_should_raise_when_structure_is_missing
ATT/tests/test_structure_market_input_assembler.py::StructureMarketInputAssemblerTests::test_should_raise_when_underlying_asset_mismatches

31 tests collected in 0.40s

## Execucao dos testes Fase 3
...............................                                    [100%]
31 passed, 6 subtests passed in 1.47s
