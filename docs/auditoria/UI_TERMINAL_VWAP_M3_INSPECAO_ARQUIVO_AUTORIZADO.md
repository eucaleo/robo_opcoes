# M3 - Inspecao cirurgica do arquivo autorizado Terminal VWAP

Data: 2026-07-07 16:07:04

Branch: `audit/ui-modern-terminal-vwap`

HEAD: `6e7fa2c`

## 1. Arquivo autorizado

- `UI/components/terminal_vwap_payoff_panel.py`

## 2. Estado Git

Status:

```text
LIMPO
```

Ultimos commits:

```text
6e7fa2c docs: correct terminal vwap m3 ui-only whitelist
c6eb642 docs: classify terminal vwap m3 ui-only scope
104bf43 docs: inventory terminal vwap ui audit scope
f4faca0 docs: track macro ui audit strategy
bd08ff7 test: cover partial ui modern cli env precedence
3341dee test: document ui modern cli help options
a356a9b test: add ui modern cli invalid env fallback smoke
34a6e8d feat: honor ui modern launcher environment options
50fbf49 test: add ui modern cli help smoke
3ef66a5 test: add ui modern cli subprocess smoke
fedd676 test: add ui modern package entrypoint smoke
cf4e39c test: add ui modern launcher routing smoke
```

## 3. Imports

- `__future__`
- `tkinter`
- `typing`

## 4. Classes

- `TerminalVWAPPayoffPanel`

## 5. Funcoes top-level

- `_to_float` linhas 25-44
- `_safe_text` linhas 47-52
- `_format_number_br` linhas 55-61
- `_format_currency_br` linhas 64-69
- `_format_percent_br` linhas 72-77
- `_extract_leg_table_rows` linhas 80-97
- `_extract_payoff_table_rows` linhas 100-120
- `_summarize_viewmodel` linhas 123-148

## 6. Metodos por classe

### `TerminalVWAPPayoffPanel` linhas 151-537

- `__init__` linhas 154-172
- `_build_ui` linhas 178-197
- `_build_left_panel` linhas 199-255
- `_build_right_panel` linhas 257-274
- `_build_summary_tab` linhas 276-337
- `_build_legs_tab` linhas 339-373
- `_build_payoff_tab` linhas 375-399
- `_build_warnings_tab` linhas 401-404
- `reload_structures` linhas 410-423
- `load_selected_structure` linhas 425-440
- `load_structure` linhas 442-455
- `_render_structures` linhas 461-477
- `render_viewmodel` linhas 479-488
- `_render_legs` linhas 490-495
- `_render_payoff` linhas 497-516
- `_render_warnings` linhas 518-527
- `_set_status` linhas 529-537

## 7. Snippets das funcoes auxiliares

### `_to_float`

```python
0025: def _to_float(value: Any) -> float | None:
0026:     if value is None:
0027:         return None
0028: 
0029:     if isinstance(value, bool):
0030:         return None
0031: 
0032:     if isinstance(value, (int, float)):
0033:         return float(value)
0034: 
0035:     text = str(value).strip()
0036:     if not text:
0037:         return None
0038: 
0039:     try:
0040:         if "," in text:
0041:             text = text.replace(".", "").replace(",", ".")
0042:         return float(text)
0043:     except Exception:
0044:         return None
```

### `_safe_text`

```python
0047: def _safe_text(value: Any, default: str = "N/A") -> str:
0048:     if value is None:
0049:         return default
0050: 
0051:     text = str(value).strip()
0052:     return text if text else default
```

### `_format_number_br`

```python
0055: def _format_number_br(value: Any, decimals: int = 2) -> str:
0056:     number = _to_float(value)
0057:     if number is None:
0058:         return "N/A"
0059: 
0060:     rendered = f"{number:,.{decimals}f}"
0061:     return rendered.replace(",", "X").replace(".", ",").replace("X", ".")
```

### `_format_currency_br`

```python
0064: def _format_currency_br(value: Any, decimals: int = 2) -> str:
0065:     number = _to_float(value)
0066:     if number is None:
0067:         return "N/A"
0068: 
0069:     return f"R$ {_format_number_br(number, decimals)}"
```

### `_format_percent_br`

```python
0072: def _format_percent_br(value: Any, decimals: int = 2) -> str:
0073:     number = _to_float(value)
0074:     if number is None:
0075:         return "N/A"
0076: 
0077:     return f"{_format_number_br(number, decimals)}%"
```

### `_extract_leg_table_rows`

```python
0080: def _extract_leg_table_rows(viewmodel: dict[str, Any]) -> list[tuple[str, ...]]:
0081:     rows: list[tuple[str, ...]] = []
0082: 
0083:     for leg in viewmodel.get("legs") or []:
0084:         rows.append(
0085:             (
0086:                 _safe_text(leg.get("leg_order")),
0087:                 _safe_text(leg.get("symbol")),
0088:                 _safe_text(leg.get("position_side")),
0089:                 _safe_text(leg.get("option_type")),
0090:                 _format_number_br(leg.get("strike"), 2),
0091:                 _safe_text(leg.get("expiration_date")),
0092:                 _format_number_br(leg.get("quantity"), 0),
0093:                 _format_currency_br(leg.get("premium"), 2),
0094:             )
0095:         )
0096: 
0097:     return rows
```

### `_extract_payoff_table_rows`

```python
0100: def _extract_payoff_table_rows(
0101:     viewmodel: dict[str, Any],
0102:     *,
0103:     limit: int | None = None,
0104: ) -> list[tuple[str, str]]:
0105:     payoff = viewmodel.get("payoff") or {}
0106:     points = payoff.get("points") or []
0107: 
0108:     if limit is not None:
0109:         points = points[:limit]
0110: 
0111:     rows: list[tuple[str, str]] = []
0112:     for point in points:
0113:         rows.append(
0114:             (
0115:                 _format_number_br(point.get("underlying_price"), 2),
0116:                 _format_currency_br(point.get("result"), 2),
0117:             )
0118:         )
0119: 
0120:     return rows
```

### `_summarize_viewmodel`

```python
0123: def _summarize_viewmodel(viewmodel: dict[str, Any]) -> dict[str, str]:
0124:     structure = viewmodel.get("structure") or {}
0125:     market = viewmodel.get("market") or {}
0126:     payoff = viewmodel.get("payoff") or {}
0127: 
0128:     return {
0129:         "structure_id": _safe_text(structure.get("structure_id")),
0130:         "name": _safe_text(structure.get("name")),
0131:         "underlying_asset": _safe_text(structure.get("underlying_asset")),
0132:         "status": _safe_text(structure.get("status")),
0133:         "current_price": _format_number_br(market.get("current_price"), 2),
0134:         "vwap": _format_number_br(market.get("vwap"), 2),
0135:         "price_vs_vwap_percent": _format_percent_br(
0136:             market.get("price_vs_vwap_percent"),
0137:             2,
0138:         ),
0139:         "market_source": _safe_text(market.get("source")),
0140:         "market_timestamp": _safe_text(market.get("timestamp")),
0141:         "points_count": _safe_text(payoff.get("points_count")),
0142:         "min_result": _format_currency_br(payoff.get("min_result"), 2),
0143:         "max_result": _format_currency_br(payoff.get("max_result"), 2),
0144:         "break_even_points": ", ".join(
0145:             _format_number_br(item, 2)
0146:             for item in payoff.get("break_even_points") or []
0147:         ) or "N/A",
0148:     }
```

## 8. Snippets dos metodos criticos de renderizacao

### `TerminalVWAPPayoffPanel.__init__`

```python
0154:     def __init__(
0155:         self,
0156:         parent: tk.Widget,
0157:         controller: Any,
0158:         *,
0159:         on_status: Callable[[str], None] | None = None,
0160:     ) -> None:
0161:         super().__init__(parent, padding=6)
0162: 
0163:         if controller is None:
0164:             raise ValueError("controller é obrigatório")
0165: 
0166:         self._controller = controller
0167:         self._on_status = on_status
0168:         self._structures: list[dict[str, Any]] = []
0169:         self._current_viewmodel: dict[str, Any] | None = None
0170: 
0171:         self._build_ui()
0172:         self.reload_structures()
```

### `TerminalVWAPPayoffPanel._build_ui`

```python
0178:     def _build_ui(self) -> None:
0179:         outer = ttk.PanedWindow(self, orient="horizontal")
0180:         outer.pack(fill="both", expand=True)
0181: 
0182:         left = ttk.Frame(outer)
0183:         right = ttk.Frame(outer)
0184: 
0185:         outer.add(left, weight=1)
0186:         outer.add(right, weight=3)
0187: 
0188:         self._build_left_panel(left)
0189:         self._build_right_panel(right)
0190: 
0191:         self._status_var = tk.StringVar(value="Terminal VWAP Payoff pronto")
0192:         ttk.Label(
0193:             self,
0194:             textvariable=self._status_var,
0195:             relief=tk.SUNKEN,
0196:             anchor="w",
0197:         ).pack(side="bottom", fill="x", pady=(6, 0))
```

### `TerminalVWAPPayoffPanel._build_left_panel`

```python
0199:     def _build_left_panel(self, parent: tk.Widget) -> None:
0200:         box = ttk.LabelFrame(parent, text="Estruturas", padding=6)
0201:         box.pack(fill="both", expand=True)
0202: 
0203:         toolbar = ttk.Frame(box)
0204:         toolbar.pack(fill="x", pady=(0, 6))
0205: 
0206:         ttk.Button(
0207:             toolbar,
0208:             text="Atualizar",
0209:             command=self.reload_structures,
0210:         ).pack(side="left")
0211: 
0212:         ttk.Button(
0213:             toolbar,
0214:             text="Carregar",
0215:             command=self.load_selected_structure,
0216:         ).pack(side="left", padx=(6, 0))
0217: 
0218:         columns = ("structure_id", "name", "underlying_asset", "status", "legs")
0219:         self._structures_tree = ttk.Treeview(
0220:             box,
0221:             columns=columns,
0222:             show="headings",
0223:             selectmode="browse",
0224:             height=12,
0225:         )
0226: 
0227:         headers = {
0228:             "structure_id": ("ID", 55, "center"),
0229:             "name": ("Nome", 190, "w"),
0230:             "underlying_asset": ("Ativo", 75, "center"),
0231:             "status": ("Status", 75, "center"),
0232:             "legs": ("Legs", 55, "center"),
0233:         }
0234: 
0235:         for column in columns:
0236:             text, width, anchor = headers[column]
0237:             self._structures_tree.heading(column, text=text)
0238:             self._structures_tree.column(
0239:                 column,
0240:                 width=width,
0241:                 anchor=anchor,
0242:                 stretch=(column == "name"),
0243:             )
0244: 
0245:         vsb = ttk.Scrollbar(
0246:             box,
0247:             orient="vertical",
0248:             command=self._structures_tree.yview,
0249:         )
0250:         self._structures_tree.configure(yscrollcommand=vsb.set)
0251: 
0252:         vsb.pack(side="right", fill="y")
0253:         self._structures_tree.pack(fill="both", expand=True)
0254: 
0255:         self._structures_tree.bind("<Double-1>", lambda _e: self.load_selected_structure())
```

### `TerminalVWAPPayoffPanel._build_right_panel`

```python
0257:     def _build_right_panel(self, parent: tk.Widget) -> None:
0258:         notebook = ttk.Notebook(parent)
0259:         notebook.pack(fill="both", expand=True)
0260: 
0261:         summary_tab = ttk.Frame(notebook, padding=6)
0262:         legs_tab = ttk.Frame(notebook, padding=6)
0263:         payoff_tab = ttk.Frame(notebook, padding=6)
0264:         warnings_tab = ttk.Frame(notebook, padding=6)
0265: 
0266:         notebook.add(summary_tab, text="Resumo")
0267:         notebook.add(legs_tab, text="Legs")
0268:         notebook.add(payoff_tab, text="Payoff")
0269:         notebook.add(warnings_tab, text="Avisos")
0270: 
0271:         self._build_summary_tab(summary_tab)
0272:         self._build_legs_tab(legs_tab)
0273:         self._build_payoff_tab(payoff_tab)
0274:         self._build_warnings_tab(warnings_tab)
```

### `TerminalVWAPPayoffPanel._build_summary_tab`

```python
0276:     def _build_summary_tab(self, parent: tk.Widget) -> None:
0277:         self._summary_vars: dict[str, tk.StringVar] = {}
0278: 
0279:         groups = [
0280:             (
0281:                 "Estrutura",
0282:                 [
0283:                     ("structure_id", "ID"),
0284:                     ("name", "Nome"),
0285:                     ("underlying_asset", "Ativo"),
0286:                     ("status", "Status"),
0287:                 ],
0288:             ),
0289:             (
0290:                 "Mercado e VWAP",
0291:                 [
0292:                     ("current_price", "Preço atual"),
0293:                     ("vwap", "VWAP"),
0294:                     ("price_vs_vwap_percent", "Preço vs VWAP"),
0295:                     ("market_source", "Fonte"),
0296:                     ("market_timestamp", "Atualizado em"),
0297:                 ],
0298:             ),
0299:             (
0300:                 "Payoff",
0301:                 [
0302:                     ("points_count", "Pontos"),
0303:                     ("min_result", "Resultado mín."),
0304:                     ("max_result", "Resultado máx."),
0305:                     ("break_even_points", "Break-even"),
0306:                 ],
0307:             ),
0308:         ]
0309: 
0310:         for group_title, fields in groups:
0311:             group = ttk.LabelFrame(parent, text=group_title, padding=8)
0312:             group.pack(fill="x", pady=(0, 8))
0313: 
0314:             for row, (key, label) in enumerate(fields):
0315:                 ttk.Label(group, text=f"{label}:", width=18, anchor="e").grid(
0316:                     row=row,
0317:                     column=0,
0318:                     sticky="e",
0319:                     padx=(0, 8),
0320:                     pady=2,
0321:                 )
0322: 
0323:                 var = tk.StringVar(value="N/A")
0324:                 self._summary_vars[key] = var
0325: 
0326:                 ttk.Label(
0327:                     group,
0328:                     textvariable=var,
0329:                     anchor="w",
0330:                 ).grid(
0331:                     row=row,
0332:                     column=1,
0333:                     sticky="ew",
0334:                     pady=2,
0335:                 )
0336: 
0337:             group.columnconfigure(1, weight=1)
```

### `TerminalVWAPPayoffPanel._build_legs_tab`

```python
0339:     def _build_legs_tab(self, parent: tk.Widget) -> None:
0340:         columns = (
0341:             "order",
0342:             "symbol",
0343:             "side",
0344:             "type",
0345:             "strike",
0346:             "expiry",
0347:             "quantity",
0348:             "premium",
0349:         )
0350: 
0351:         self._legs_tree = ttk.Treeview(parent, columns=columns, show="headings")
0352: 
0353:         headers = {
0354:             "order": ("#", 45, "center"),
0355:             "symbol": ("Símbolo", 110, "center"),
0356:             "side": ("Lado", 90, "center"),
0357:             "type": ("Tipo", 70, "center"),
0358:             "strike": ("Strike", 90, "e"),
0359:             "expiry": ("Vencimento", 105, "center"),
0360:             "quantity": ("Qtde", 85, "e"),
0361:             "premium": ("Prêmio", 95, "e"),
0362:         }
0363: 
0364:         for column in columns:
0365:             text, width, anchor = headers[column]
0366:             self._legs_tree.heading(column, text=text)
0367:             self._legs_tree.column(column, width=width, anchor=anchor)
0368: 
0369:         vsb = ttk.Scrollbar(parent, orient="vertical", command=self._legs_tree.yview)
0370:         self._legs_tree.configure(yscrollcommand=vsb.set)
0371: 
0372:         vsb.pack(side="right", fill="y")
0373:         self._legs_tree.pack(fill="both", expand=True)
```

### `TerminalVWAPPayoffPanel._build_payoff_tab`

```python
0375:     def _build_payoff_tab(self, parent: tk.Widget) -> None:
0376:         top = ttk.Frame(parent)
0377:         top.pack(fill="x", pady=(0, 6))
0378: 
0379:         self._payoff_summary_var = tk.StringVar(value="Payoff ainda não carregado")
0380:         ttk.Label(
0381:             top,
0382:             textvariable=self._payoff_summary_var,
0383:             anchor="w",
0384:         ).pack(side="left", fill="x", expand=True)
0385: 
0386:         columns = ("underlying_price", "result")
0387:         self._payoff_tree = ttk.Treeview(parent, columns=columns, show="headings")
0388: 
0389:         self._payoff_tree.heading("underlying_price", text="Spot")
0390:         self._payoff_tree.heading("result", text="Resultado")
0391: 
0392:         self._payoff_tree.column("underlying_price", width=120, anchor="e")
0393:         self._payoff_tree.column("result", width=140, anchor="e")
0394: 
0395:         vsb = ttk.Scrollbar(parent, orient="vertical", command=self._payoff_tree.yview)
0396:         self._payoff_tree.configure(yscrollcommand=vsb.set)
0397: 
0398:         vsb.pack(side="right", fill="y")
0399:         self._payoff_tree.pack(fill="both", expand=True)
```

### `TerminalVWAPPayoffPanel._build_warnings_tab`

```python
0401:     def _build_warnings_tab(self, parent: tk.Widget) -> None:
0402:         self._warnings_text = tk.Text(parent, height=8, wrap="word")
0403:         self._warnings_text.pack(fill="both", expand=True)
0404:         self._warnings_text.configure(state="disabled")
```

### `TerminalVWAPPayoffPanel.reload_structures`

```python
0410:     def reload_structures(self) -> None:
0411:         try:
0412:             structures = self._controller.list_structures()
0413:         except Exception as exc:
0414:             self._set_status(f"Erro ao listar estruturas: {exc}")
0415:             messagebox.showerror(
0416:                 "Terminal VWAP Payoff",
0417:                 f"Erro ao listar estruturas:\n{exc}",
0418:             )
0419:             return
0420: 
0421:         self._structures = list(structures or [])
0422:         self._render_structures()
0423:         self._set_status(f"{len(self._structures)} estruturas disponíveis no terminal")
```

### `TerminalVWAPPayoffPanel.load_selected_structure`

```python
0425:     def load_selected_structure(self) -> None:
0426:         selected = self._structures_tree.selection()
0427:         if not selected:
0428:             self._set_status("Selecione uma estrutura para carregar")
0429:             return
0430: 
0431:         item_id = selected[0]
0432:         try:
0433:             index = int(item_id)
0434:             structure = self._structures[index]
0435:         except Exception:
0436:             self._set_status("Seleção inválida")
0437:             return
0438: 
0439:         structure_id = structure.get("structure_id")
0440:         self.load_structure(structure_id)
```

### `TerminalVWAPPayoffPanel.load_structure`

```python
0442:     def load_structure(self, structure_id: Any) -> None:
0443:         try:
0444:             self._set_status(f"Carregando estrutura {structure_id}...")
0445:             viewmodel = self._controller.load_structure(structure_id)
0446:         except Exception as exc:
0447:             self._set_status(f"Erro ao carregar estrutura {structure_id}: {exc}")
0448:             messagebox.showerror(
0449:                 "Terminal VWAP Payoff",
0450:                 f"Erro ao carregar estrutura {structure_id}:\n{exc}",
0451:             )
0452:             return
0453: 
0454:         self.render_viewmodel(viewmodel)
0455:         self._set_status(f"Estrutura {structure_id} carregada no Terminal VWAP Payoff")
```

### `TerminalVWAPPayoffPanel._render_structures`

```python
0461:     def _render_structures(self) -> None:
0462:         for item in self._structures_tree.get_children():
0463:             self._structures_tree.delete(item)
0464: 
0465:         for index, structure in enumerate(self._structures):
0466:             self._structures_tree.insert(
0467:                 "",
0468:                 "end",
0469:                 iid=str(index),
0470:                 values=(
0471:                     _safe_text(structure.get("structure_id")),
0472:                     _safe_text(structure.get("name")),
0473:                     _safe_text(structure.get("underlying_asset")),
0474:                     _safe_text(structure.get("status")),
0475:                     _safe_text(structure.get("legs_count")),
0476:                 ),
0477:             )
```

### `TerminalVWAPPayoffPanel.render_viewmodel`

```python
0479:     def render_viewmodel(self, viewmodel: dict[str, Any]) -> None:
0480:         self._current_viewmodel = dict(viewmodel or {})
0481: 
0482:         summary = _summarize_viewmodel(self._current_viewmodel)
0483:         for key, var in self._summary_vars.items():
0484:             var.set(summary.get(key, "N/A"))
0485: 
0486:         self._render_legs(self._current_viewmodel)
0487:         self._render_payoff(self._current_viewmodel)
0488:         self._render_warnings(self._current_viewmodel)
```

### `TerminalVWAPPayoffPanel._render_legs`

```python
0490:     def _render_legs(self, viewmodel: dict[str, Any]) -> None:
0491:         for item in self._legs_tree.get_children():
0492:             self._legs_tree.delete(item)
0493: 
0494:         for index, row in enumerate(_extract_leg_table_rows(viewmodel)):
0495:             self._legs_tree.insert("", "end", iid=str(index), values=row)
```

### `TerminalVWAPPayoffPanel._render_payoff`

```python
0497:     def _render_payoff(self, viewmodel: dict[str, Any]) -> None:
0498:         for item in self._payoff_tree.get_children():
0499:             self._payoff_tree.delete(item)
0500: 
0501:         rows = _extract_payoff_table_rows(viewmodel)
0502:         for index, row in enumerate(rows):
0503:             self._payoff_tree.insert("", "end", iid=str(index), values=row)
0504: 
0505:         payoff = viewmodel.get("payoff") or {}
0506:         self._payoff_summary_var.set(
0507:             "Pontos: {points} | Mín: {min_result} | Máx: {max_result} | BE: {be}".format(
0508:                 points=_safe_text(payoff.get("points_count")),
0509:                 min_result=_format_currency_br(payoff.get("min_result"), 2),
0510:                 max_result=_format_currency_br(payoff.get("max_result"), 2),
0511:                 be=", ".join(
0512:                     _format_number_br(item, 2)
0513:                     for item in payoff.get("break_even_points") or []
0514:                 ) or "N/A",
0515:             )
0516:         )
```

### `TerminalVWAPPayoffPanel._render_warnings`

```python
0518:     def _render_warnings(self, viewmodel: dict[str, Any]) -> None:
0519:         meta = viewmodel.get("meta") or {}
0520:         warnings = meta.get("warnings") or []
0521: 
0522:         text = "\n".join(f"- {item}" for item in warnings) if warnings else "Sem avisos."
0523: 
0524:         self._warnings_text.configure(state="normal")
0525:         self._warnings_text.delete("1.0", tk.END)
0526:         self._warnings_text.insert("1.0", text)
0527:         self._warnings_text.configure(state="disabled")
```

### `TerminalVWAPPayoffPanel._set_status`

```python
0529:     def _set_status(self, message: str) -> None:
0530:         if hasattr(self, "_status_var"):
0531:             self._status_var.set(message)
0532: 
0533:         if self._on_status is not None:
0534:             try:
0535:                 self._on_status(message)
0536:             except Exception:
0537:                 pass
```

## 9. Decisao

Este documento serve como base para o M3 restrito.

O patch do M3 deve alterar somente:

- `UI/components/terminal_vwap_payoff_panel.py`
- `ATT/tests/`
- `docs/auditoria/`

Classificacao:

M3_INSPECAO_ARQUIVO_AUTORIZADO

UI_ONLY_RESTRITO
