# VERIFICAÇÃO FASE 5 — CONTRATO MÍNIMO DO RESUMO DO PIPELINE

## Status

Verificação gerada automaticamente.

## Arquivos analisados

- scripts/run_derived_pipeline.py: existe
- scripts/run_rtd_option_quotes_pipeline.py: existe
- scripts/run_rtd_refresh_full.py: existe
- UI/components/structure_editor_dialog.py: existe

## Conceitos verificados

| Conceito | Encontrado |
|---|---|
| Estruturas lidas | Sim |
| Estruturas processadas | Não |
| Estruturas ignoradas | Não |
| Pontos de payoff | Sim |
| Decisões | Sim |
| Cotações RTD | Sim |
| Avisos | Sim |
| Erros | Sim |
| Sucesso sem dados novos | Não |

## Ocorrências

### Estruturas lidas

205:            "structures": _first_count(
207:                "structure_snapshots",
208:                "structures",
209:                "derived_structures",
215:                "structure_decisions",
321:    print(f"  Estruturas: {_display_summary_value(summary.get('structures'))}")
86:    parser.add_argument("--strict", action="store_true", help="Usa somente structure_legs como fonte de símbolos.")
194:        print("- Em modo --strict, isso é esperado se não houver registros em structure_legs.")
195:        print("- Cadastre uma estrutura pelo sistema ou rode sem --strict para usar fallback de rtd_option_quotes.")
1:# UI/components/structure_editor_dialog.py
4:Dialog modal para criar / editar uma estrutura com suas legs.
9:        structure_id: int | None,   # None -> nova estrutura
23:    _structure_id   int | None
26:    _load_existing()       sem argumento -- usa self._structure_id
37:from repositories.structures_repository import StructuresRepository
39:from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
62:    """Dialog modal de criacao / edicao de estrutura."""
67:        structure_id: Optional[int] = None,
75:        self._structure_id = structure_id
78:        self.saved_structure_id = None
100:        if structure_id is not None:
114:        title = "Nova Estrutura" if self._structure_id is None else "Editar Estrutura"
254:    # Carregar estrutura existente
259:        Carrega campos e legs de uma estrutura existente via repositorio.
260:        Usa self._structure_id (nao recebe argumento -- compativel com testes
263:        data = self._repo.get_structure(self._structure_id)
267:                f"Estrutura {self._structure_id} nao encontrada.",
521:        """Preenche/valida o ativo objeto da estrutura a partir da opção."""
530:                f"estrutura={current}, detectado={underlying}, "
750:        structure_data = {
759:            if self._structure_id is None:
761:                sid = self._repo.create_structure_with_legs(
762:                    structure_data,
767:                sid = self._structure_id
768:                self._repo.update_structure(sid, structure_data)
772:                if getattr(self, "_structure_id", None) is not None:
773:                    self.saved_structure_id = int(self._structure_id)
775:                    _candidate_saved_structure_id = (
776:                        locals().get("created_structure_id")
777:                        or locals().get("new_structure_id")
778:                        or locals().get("structure_id")
783:                    self.saved_structure_id = (
784:                        int(_candidate_saved_structure_id)
785:                        if _candidate_saved_structure_id is not None
789:                self.saved_structure_id = getattr(self, "_structure_id", None)

### Estruturas processadas

- Nenhuma ocorrência encontrada.

### Estruturas ignoradas

- Nenhuma ocorrência encontrada.

### Pontos de payoff

149:    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
218:            "payoff_points": _first_count(
220:                "payoff_curve_points",
221:                "payoff_points",
222:                "derived_payoff_points",
323:    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")

### Decisões

211:            "decisions": _first_count(
214:                "decisions",
215:                "structure_decisions",
216:                "derived_decisions",
322:    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")

### Cotações RTD

24:_RTD_METRIC_RE = re.compile(r"^\s*(input_rows|inserted|updated|skipped):\s*(-?\d+)\s*$")
39:def _parse_rtd_pipeline_metrics(output: str) -> dict:
40:    """Extrai métricas textuais emitidas pelo pipeline RTD restaurado."""
49:        match = _RTD_METRIC_RE.match(line)
59:def _rtd_quotes_updated_count(rtd_result: dict | None) -> int:
60:    """Retorna o total de cotações efetivamente inseridas/atualizadas."""
61:    if not rtd_result:
64:    return int(rtd_result.get("inserted") or 0) + int(rtd_result.get("updated") or 0)
67:def _run_rtd_option_quotes_import(
69:    csv_path: str = "dados/RTD_LINKS.csv",
73:    Executa a cadeia operacional RTD já restaurada contra o derived.db.
76:    - Usa somente CSV local dados/RTD_LINKS.csv.
77:    - Não aciona Excel, PowerShell, COM ou refresh RTD ao vivo.
78:    - Delega importação + auditoria para scripts/run_rtd_option_quotes_pipeline.py.
81:    pipeline_script = repo_root / "scripts" / "run_rtd_option_quotes_pipeline.py"
90:            "message": f"Script RTD não encontrado: {pipeline_script}",
102:            "message": f"CSV RTD não encontrado: {resolved_csv}",
134:    metrics = _parse_rtd_pipeline_metrics(stdout)
184:def _collect_pipeline_summary(rtd_result: dict | None = None) -> dict:
189:    - Inclui a quantidade de cotações RTD inseridas/atualizadas.
191:    - Apenas lê contagens do banco depois que o pipeline RTD CSV já rodou.
235:            "rtd_quotes_updated": _rtd_quotes_updated_count(rtd_result),
236:            "rtd_import": rtd_result,
237:            "warnings": int((rtd_result or {}).get("warnings") or 0),
238:            "errors": int((rtd_result or {}).get("errors") or 0),
258:        "--skip-rtd",
260:        help="Não importar dados/RTD_LINKS.csv para rtd_option_quotes no derived.db",
263:        "--rtd-csv",
264:        default="dados/RTD_LINKS.csv",
265:        help="Caminho do CSV RTD usado pelo pipeline derivado",
280:    rtd_result = None
281:    if args.skip_rtd:
282:        print("\n[PIPELINE] Importação RTD pulada por --skip-rtd.")
283:        rtd_result = {
294:        print("\n[PIPELINE] Importando cotações RTD para derived.db...")
295:        rtd_result = _run_rtd_option_quotes_import(
297:            csv_path=args.rtd_csv,
301:        if int(rtd_result.get("returncode") or 0) != 0:
302:            print("[ERROR] PIPELINE FALHOU: importação/auditoria RTD falhou")
303:            if rtd_result.get("message"):
304:                print(f"[ERROR] {rtd_result.get('message')}")
305:            summary = _collect_pipeline_summary(rtd_result)
307:            return int(rtd_result.get("returncode") or 1)
313:        summary = _collect_pipeline_summary(rtd_result)
318:    summary = _collect_pipeline_summary(rtd_result)
326:    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
3:Executa o pipeline operacional de cotações RTD de opções.
7:    dados/RTD_LINKS.csv -> rtd_option_quotes -> auditoria
11:    python scripts/run_rtd_option_quotes_pipeline.py
12:    python scripts/run_rtd_option_quotes_pipeline.py --csv dados/RTD_LINKS.csv --db dados/app.db
13:    python scripts/run_rtd_option_quotes_pipeline.py --dry-run
14:    python scripts/run_rtd_option_quotes_pipeline.py --fail-on-warn
28:IMPORT_SCRIPT = SCRIPTS_DIR / "import_rtd_option_quotes_wide_csv.py"
29:AUDIT_SCRIPT = SCRIPTS_DIR / "audit_rtd_option_quotes.py"
89:    csv_path: str = "dados/RTD_LINKS.csv",
96:    print("Pipeline RTD option quotes")
142:        description="Executa importação e auditoria de rtd_option_quotes."
146:        default="dados/RTD_LINKS.csv",
147:        help="Caminho do CSV RTD_LINKS.csv. Padrão: dados/RTD_LINKS.csv",
34:def count_quotes(db_path):
43:            FROM rtd_option_quotes
76:        description="Pipeline completo: gerar símbolos RTD, atualizar Excel/CSV e importar cotações no SQLite."
80:    parser.add_argument("--symbols", default="dados/rtd_symbols.txt")
81:    parser.add_argument("--csv", default="dados/RTD_LINKS.csv")
82:    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
99:    build_script = Path("scripts/build_rtd_symbols.py")
100:    import_script = Path("scripts/import_rtd_option_quotes_wide_csv.py")
101:    ps1_script = Path("scripts/refresh_rtd_option_quotes_excel.ps1")
103:    print("=== RTD Refresh Full ===")
126:    before = count_quotes(db_path)
141:        build_cmd += ["--no-existing-quotes", "--no-snapshots"]
195:        print("- Cadastre uma estrutura pelo sistema ou rode sem --strict para usar fallback de rtd_option_quotes.")
205:        print("Pipeline interrompido: nenhum símbolo para consultar no RTD.")
241:            print("Pipeline interrompido no refresh Excel/RTD.")
245:        print("Refresh Excel/RTD pulado por --skip-excel.")
264:    after = count_quotes(db_path)
271:    print("OK: pipeline RTD finalizado.")
38:from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
39:from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
400:        """Compatibilidade: permite leg manual completa mesmo sem cotacao RTD."""
419:            preserva compatibilidade e nao acessa RTD.
434:                self._refresh_rtd_quote_for_symbol(symbol)
446:    def _refresh_rtd_quote_for_symbol(self, symbol: str) -> None:
447:        """Atualiza uma opção avulsa no RTD/Excel e importa para o cache local."""
459:        script = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
460:        workbook_path = project_root / "LISTA_RTD.xlsm"
474:            raise ValueError(f"Script de refresh RTD não encontrado: {script}")
477:            raise ValueError(f"Workbook RTD não encontrado: {workbook_path}")
515:                "Não foi possível atualizar a cotação RTD para "

### Avisos

89:            "warnings": 0,
101:            "warnings": 0,
140:        "warnings": 0,
237:            "warnings": int((rtd_result or {}).get("warnings") or 0),
286:            "warnings": 1,
327:    print(f"  Avisos: {_display_summary_value(summary.get('warnings'))}")
364:            messagebox.showwarning("Remover Leg", "Selecione uma leg primeiro.", parent=self)
570:            messagebox.showwarning(
594:            messagebox.showwarning(
719:            messagebox.showwarning("Salvar", "O campo 'Nome' e obrigatorio.", parent=self)
738:                messagebox.showwarning(
747:            messagebox.showwarning("Salvar", "O campo 'Ativo' e obrigatorio.", parent=self)

### Erros

88:            "errors": 1,
100:            "errors": 1,
139:        "errors": 0 if completed.returncode == 0 else 1,
238:            "errors": int((rtd_result or {}).get("errors") or 0),
285:            "errors": 0,
314:        summary["errors"] = int(summary.get("errors") or 0) + 1
328:    print(f"  Erros: {_display_summary_value(summary.get('errors'))}")
20:            errors="replace",
67:        for line in p.read_text(encoding="utf-8", errors="replace").splitlines()
499:            errors="replace",

### Sucesso sem dados novos

- Nenhuma ocorrência encontrada.

## Leitura esperada

A Fase 5 deve garantir que o botão Atualizar Dados tenha retorno claro para:

- estruturas lidas;
- estruturas processadas;
- estruturas ignoradas;
- pontos de payoff gerados;
- decisões geradas;
- cotações RTD atualizadas;
- avisos;
- erros;
- execução sem dados novos.
