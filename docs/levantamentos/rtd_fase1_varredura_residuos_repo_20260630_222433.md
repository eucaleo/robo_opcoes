# Fase 1 RTD - varredura de resíduos no repositório

Atualizado em: 20260630_222433

## Objetivo

Mapear referências remanescentes a subprocesso, refresh RTD sob demanda e chamadas diretas a scripts RTD/Excel fora do fluxo operacional esperado.

## Critérios

    Resíduo crítico:
    UI chamando subprocesso.
    UI chamando scripts RTD/Excel.
    UI executando refresh por símbolo.
    Services de domínio chamando subprocesso para RTD/Excel.

    Resíduo aceitável:
    Scripts operacionais em scripts/.
    Documentação em docs/.
    Testes que validam guardrails ou comportamento legado controlado.

## Referências ao método removido _refresh_rtd_symbol_on_demand

    docs/AUDITORIA_RTD_EXCEL_VIVO.md:401:    O método _refresh_rtd_symbol_on_demand foi removido.
    docs/AUDITORIA_RTD_EXCEL_VIVO.md:407:        -> _refresh_rtd_symbol_on_demand
    docs/AUDITORIA_RTD_EXCEL_VIVO.md:424:        _refresh_rtd_symbol_on_demand
    docs/levantamentos/rtd_fase1_alvos_iniciais_20260630_220530.md:52:    def _refresh_rtd_symbol_on_demand(self, codigo_opcao: str) -> tuple[bool, str]:
    docs/levantamentos/rtd_fase1_remocao_subprocess_structure_editor_20260630_221911.md:17:    O método _refresh_rtd_symbol_on_demand foi removido da UI.

## Referências ao script refresh_rtd_symbol_to_option_quotes_fallback

    ATT/patches/pre_correct_rtd_derived_db_20260630_status.txt:17:?? scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
    ATT/tests/test_rtd_live_db_guardrail.py:16:    "scripts/refresh_rtd_symbol_to_option_quotes_fallback.py",
    docs/AUDITORIA_RTD_EXCEL_VIVO.md:409:                -> scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
    docs/AUDITORIA_RTD_EXCEL_VIVO.md:425:        refresh_rtd_symbol_to_option_quotes_fallback
    docs/levantamentos/auditoria_bd_rtd_appdb_20260630_185425.md:455:| `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py` | 4 | `subprocess` | `import subprocess` |
    docs/levantamentos/auditoria_bd_rtd_appdb_20260630_185425.md:456:| `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py` | 60 | `subprocess` | `cp = subprocess.run(` |
    docs/levantamentos/auditoria_bd_rtd_appdb_20260630_185425.md:63356:| `docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt` | 52231 | `subprocess` | `./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:4:import subprocess` |
    docs/levantamentos/auditoria_bd_rtd_appdb_20260630_185425.md:63357:| `docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt` | 52232 | `subprocess` | `./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:60:    cp = subprocess.run(` |
    docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt:683:./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes_fallback.cpython-313.pyc
    docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt:699:./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
    docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt:52231:./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:4:import subprocess
    docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt:52232:./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:60:    cp = subprocess.run(
    docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt:52555:./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes_fallback.cpython-313.pyc
    docs/levantamentos/consulta_projeto_rtd_20260630_160457.txt:52565:./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
    docs/levantamentos/mapa_alvos_rtd_fase0_20260630_160919.md:48:- `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py`: existe; 163 linhas
    docs/levantamentos/mapa_alvos_rtd_fase0_20260630_160919.md:490:- `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py`
    docs/levantamentos/mapa_alvos_rtd_fase0_20260630_160919.md:805:### `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py`
    docs/levantamentos/rtd_fase0_arquivos_candidatos_20260630_215918.txt:118:./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes_fallback.cpython-313.pyc
    docs/levantamentos/rtd_fase0_arquivos_candidatos_20260630_215918.txt:129:./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
    docs/levantamentos/rtd_fase0_conclusao_20260630_220155.md:294:      2 scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
    docs/levantamentos/rtd_fase0_conclusao_20260630_220155.md:793:./scripts/__pycache__/refresh_rtd_symbol_to_option_quotes_fallback.cpython-313.pyc
    docs/levantamentos/rtd_fase0_conclusao_20260630_220155.md:804:./scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
    docs/levantamentos/rtd_fase0_mapa_excel_subprocess_20260630_215903.txt:612:scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:4:import subprocess
    docs/levantamentos/rtd_fase0_mapa_excel_subprocess_20260630_215903.txt:613:scripts/refresh_rtd_symbol_to_option_quotes_fallback.py:60:    cp = subprocess.run(
    docs/levantamentos/rtd_fase1_alvos_iniciais_20260630_220530.md:60:        script_path = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
    docs/levantamentos/rtd_fase1_alvos_iniciais_20260630_220530.md:706:    "scripts/refresh_rtd_symbol_to_option_quotes_fallback.py",
    scripts/rtd_mapa_alvos_fase0.py:20:    "scripts/refresh_rtd_symbol_to_option_quotes_fallback.py",

## Referências a subprocess em UI

    Nenhuma referência encontrada em UI.

## Referências a subprocess em services, repositories, core e app

    Nenhuma referência encontrada nos alvos consultados.

## Referências gerais a RTD/Excel em UI

    UI/components/details_panel.py:694:            self._refresh_operational_state_for_structure(structure_id)
    UI/components/details_panel.py:854:    def _refresh_operational_state_for_structure(self, structure_id):
    UI/components/details_panel.py:1023:    def _refresh_current_from_derived(self, structure_id):
    UI/components/structure_editor_dialog.py:40:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
    UI/components/structure_editor_dialog.py:41:from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
    UI/components/structure_editor_dialog.py:73:        _rtd_leg_enrichment_service=None,    # <-- injecao opcional para testes/UI
    UI/components/structure_editor_dialog.py:88:        self._rtd_leg_enrichment_service = _rtd_leg_enrichment_service
    UI/components/structure_editor_dialog.py:244:            text="[RTD] Preencher por Simbolo",
    UI/components/structure_editor_dialog.py:245:            command=self._cmd_fill_leg_from_rtd,
    UI/components/structure_editor_dialog.py:281:        self._refresh_leg_tree()
    UI/components/structure_editor_dialog.py:287:    def _refresh_leg_tree(self):
    UI/components/structure_editor_dialog.py:345:        self._refresh_leg_tree()
    UI/components/structure_editor_dialog.py:368:        self._refresh_leg_tree()
    UI/components/structure_editor_dialog.py:381:        self._refresh_leg_tree()
    UI/components/structure_editor_dialog.py:405:        self._refresh_leg_tree()
    UI/components/structure_editor_dialog.py:408:    def _get_rtd_leg_enrichment_service(self):
    UI/components/structure_editor_dialog.py:409:        """Cria/lazily retorna o service de preenchimento de leg via RTD."""
    UI/components/structure_editor_dialog.py:410:        if self._rtd_leg_enrichment_service is None:
    UI/components/structure_editor_dialog.py:412:            rtd_db_path = project_root / "dados" / "app.db"
    UI/components/structure_editor_dialog.py:413:            rtd_repo = RtdOptionQuotesRepository(rtd_db_path)
    UI/components/structure_editor_dialog.py:414:            self._rtd_leg_enrichment_service = StructureLegRtdEnrichmentService(
    UI/components/structure_editor_dialog.py:415:                rtd_repo
    UI/components/structure_editor_dialog.py:417:        return self._rtd_leg_enrichment_service
    UI/components/structure_editor_dialog.py:433:    def _cmd_fill_leg_from_rtd(self):
    UI/components/structure_editor_dialog.py:434:        """Preenche a leg selecionada usando rtd_option_quotes.codigo_opcao."""
    UI/components/structure_editor_dialog.py:438:                "Preencher via RTD",
    UI/components/structure_editor_dialog.py:447:                "Preencher via RTD",
    UI/components/structure_editor_dialog.py:448:                "Informe o campo 'Simbolo' antes de consultar o RTD.",
    UI/components/structure_editor_dialog.py:463:            enriched = self._get_rtd_leg_enrichment_service().enrich(leg_data)
    UI/components/structure_editor_dialog.py:466:                "Preencher via RTD",
    UI/components/structure_editor_dialog.py:467:                f"Nao foi possivel preencher a leg pelo RTD:\n{exc}",
    UI/components/structure_editor_dialog.py:500:        self._refresh_leg_tree()
    UI/components/terminal_vwap_payoff_dark_panel.py:676:            table = "rtd_underlying_quotes"
    UI/components/terminal_vwap_payoff_dark_panel.py:989:            alerts.append("VWAP do ativo-base ausente em rtd_underlying_quotes")
    UI/components/terminal_vwap_payoff_panel.py:608:                "Nenhum cálculo, RTD, banco ou serviço foi alterado nesta camada."
    UI/models/ui_data.py:202:    def refresh(self):
    UI/models/ui_data.py:254:            self.refresh()
    UI/models/ui_data.py:488:            self.refresh()
    UI/models/ui_data.py:623:        self.refresh()

## Imports json/sys/subprocess no arquivo corrigido

    Nenhum import residual encontrado em UI/components/structure_editor_dialog.py.

## Conclusão preliminar

    Revisar as seções acima.
    Se houver ocorrência crítica em UI ou services, abrir alteração corretiva específica.
    Se as ocorrências estiverem restritas a docs, tests ou scripts operacionais, não há bloqueio arquitetural imediato.
