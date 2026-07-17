# Rodada 32.1 — Auditoria Pós-Patch / Centro de Verdade

Gerado em: `2026-07-17T20:25:52`

## Arquivos auditados

| Arquivo | Status |
|---|---|
| `services/payoff_refresh_command_service.py` | OK |
| `services/derived_payoff_persistence.py` | OK |
| `services/pricing_execution_persistence_service.py` | OK |
| `services/pricing_execution_orchestration_service.py` | OK |
| `services/canonical_pricing_facade.py` | OK |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | OK |
| `scripts/recalculate_payoff_curve_points_once.py` | OK |

# 1. Contratos backend
## `services/payoff_refresh_command_service.py`

- `PricingExecutionAppService`: **OK** (4)
- `execute_pricing\s*\(`: **OK** (2)
- `payoff_curve_points`: **OK** (1)
- `structure_decisions`: **OK** (2)
- `MAX\s*\(\s*timestamp\s*\)|ORDER\s+BY\s+timestamp\s+DESC`: **OK** (1)
- `status`: **OK** (19)
- `warning`: **OK** (1)
- `error`: **OK** (13)

## `services/derived_payoff_persistence.py`

- `payoff_curve_points`: **NÃO ENCONTRADO** (0)
- `structure_decisions`: **NÃO ENCONTRADO** (0)
- `INSERT\s+INTO\s+payoff_curve_points`: **NÃO ENCONTRADO** (0)
- `INSERT\s+INTO\s+structure_decisions`: **NÃO ENCONTRADO** (0)
- `status\s*=\s*[\"']active[\"']|status.*active`: **OK** (2)

## `services/pricing_execution_persistence_service.py`

- `payoff_persistence_port`: **OK** (4)
- `DerivedPayoffPersistence|payoff_persistence`: **OK** (4)
- `pricing_executions`: **OK** (5)
- `structure_snapshots|system_snapshots`: **OK** (7)

## `services/pricing_execution_orchestration_service.py`

- `DerivedPayoffPersistence`: **OK** (2)
- `PricingExecutionPersistenceService`: **OK** (3)
- `payoff_persistence_port`: **OK** (1)


# 2. Padrões proibidos ou suspeitos na UI
## `UI/components/terminal_vwap_payoff_dark_panel.py`

Total de ocorrências proibidas ou suspeitas na UI: **10**

### Padrão proibido: `compute_payoff_from_canonical_input`
Ocorrências: **0**


### Padrão proibido: `_calculate_payoff_from_legs`
Ocorrências: **1**

#### Ocorrência 1
```text
   1247:             conn.close()
   1248: 
>> 1249:     def _calculate_payoff_from_legs(self, legs: List[Dict[str, Any]]) -> List[Dict[str, float]]:
   1250:         strikes = self._collect_payoff_strikes(legs)
   1251: 
```

### Padrão proibido: `_calculate_payoff_points_for_range`
Ocorrências: **2**

#### Ocorrência 1
```text
   1254: 
   1255:         x_min, x_max = self._calculate_payoff_spot_range(strikes)
>> 1256:         return self._calculate_payoff_points_for_range(legs, x_min, x_max)
   1257: 
   1258:     def _collect_payoff_strikes(self, legs: List[Dict[str, Any]]) -> List[float]:
```
#### Ocorrência 2
```text
   1268:         return x_min, x_max
   1269: 
>> 1270:     def _calculate_payoff_points_for_range(
   1271:         self,
   1272:         legs: List[Dict[str, Any]],
```

### Padrão proibido: `_calculate_leg_payoff`
Ocorrências: **2**

#### Ocorrência 1
```text
   1282: 
   1283:             for leg in legs:
>> 1284:                 total += self._calculate_leg_payoff(leg, spot)
   1285: 
   1286:             points.append({"spot": spot, "pl": total})
```
#### Ocorrência 2
```text
   1288:         return points
   1289: 
>> 1290:     def _calculate_leg_payoff(self, leg: Dict[str, Any], spot: float) -> float:
   1291:         strike = _to_float(leg.get("strike"))
   1292:         if strike is None:
```

### Padrão proibido: `_collect_payoff_strikes`
Ocorrências: **2**

#### Ocorrência 1
```text
   1248: 
   1249:     def _calculate_payoff_from_legs(self, legs: List[Dict[str, Any]]) -> List[Dict[str, float]]:
>> 1250:         strikes = self._collect_payoff_strikes(legs)
   1251: 
   1252:         if not strikes:
```
#### Ocorrência 2
```text
   1256:         return self._calculate_payoff_points_for_range(legs, x_min, x_max)
   1257: 
>> 1258:     def _collect_payoff_strikes(self, legs: List[Dict[str, Any]]) -> List[float]:
   1259:         strikes = [_to_float(leg.get("strike")) for leg in legs]
   1260:         return [s for s in strikes if s is not None]
```

### Padrão proibido: `_calculate_payoff_spot_range`
Ocorrências: **2**

#### Ocorrência 1
```text
   1253:             return []
   1254: 
>> 1255:         x_min, x_max = self._calculate_payoff_spot_range(strikes)
   1256:         return self._calculate_payoff_points_for_range(legs, x_min, x_max)
   1257: 
```
#### Ocorrência 2
```text
   1260:         return [s for s in strikes if s is not None]
   1261: 
>> 1262:     def _calculate_payoff_spot_range(self, strikes: List[float]) -> tuple[float, float]:
   1263:         low = min(strikes)
   1264:         high = max(strikes)
```

### Padrão proibido: `subprocess\.run`
Ocorrências: **0**


### Padrão proibido: `subprocess\.Popen`
Ocorrências: **0**


### Padrão proibido: `os\.system`
Ocorrências: **0**


### Padrão proibido: `INSERT\s+INTO\s+payoff_curve_points`
Ocorrências: **0**


### Padrão proibido: `INSERT\s+INTO\s+structure_decisions`
Ocorrências: **1**

#### Ocorrência 1
```text
   1935:             conn.execute(
   1936:                 """
>> 1937:                 INSERT INTO structure_decisions (
   1938:                     structure_id,
   1939:                     decision,
```


# 3. Leituras de último snapshot/timestamp
## `UI/models/ui_data.py`

- `MAX\s*\(\s*timestamp\s*\)`: **NÃO ENCONTRADO** (0)
- `ORDER\s+BY\s+timestamp\s+DESC`: **OK** (1)
- `latest.*timestamp`: **OK** (8)
- `_fetch_latest_canonical_payoff_timestamp`: **OK** (2)
- `_load_persisted_payoff_points`: **NÃO ENCONTRADO** (0)

## `UI/components/details_panel.py`

- `MAX\s*\(\s*timestamp\s*\)`: **NÃO ENCONTRADO** (0)
- `ORDER\s+BY\s+timestamp\s+DESC`: **NÃO ENCONTRADO** (0)
- `latest.*timestamp`: **OK** (8)
- `_fetch_latest_canonical_payoff_timestamp`: **NÃO ENCONTRADO** (0)
- `_load_persisted_payoff_points`: **NÃO ENCONTRADO** (0)

## `UI/components/terminal_vwap_payoff_dark_panel.py`

- `MAX\s*\(\s*timestamp\s*\)`: **OK** (2)
- `ORDER\s+BY\s+timestamp\s+DESC`: **NÃO ENCONTRADO** (0)
- `latest.*timestamp`: **OK** (2)
- `_fetch_latest_canonical_payoff_timestamp`: **NÃO ENCONTRADO** (0)
- `_load_persisted_payoff_points`: **OK** (6)


# 4. Script paralelo de recálculo
## `scripts/recalculate_payoff_curve_points_once.py`

- `structure_legs`: **NÃO ENCONTRADO** (0)
- `rtd_option_quotes`: **NÃO ENCONTRADO** (0)
- `rtd_underlying_quotes`: **NÃO ENCONTRADO** (0)
- `payoff_curve_points`: **OK** (2)
- `INSERT\s+INTO\s+payoff_curve_points`: **NÃO ENCONTRADO** (0)
- `calculate|calcular|payoff`: **OK** (18)
- `maintenance|legacy|emergência|emergencia`: **NÃO ENCONTRADO** (0)
- `não é fluxo oficial|nao e fluxo oficial`: **NÃO ENCONTRADO** (0)

# 5. Possível duplicação no painel terminal
## `UI/components/terminal_vwap_payoff_dark_panel.py`

### `payoff_points\s*=\s*payload\s*\[\s*[\"']payoff_points[\"']\s*\]`
Ocorrências: **2**

#### Ocorrência 1
```text
   702:         market = payload["market"]
>> 703:         payoff_points = payload["payoff_points"]
   704: 
```
#### Ocorrência 2
```text
   2495:         market = payload["market"]
>> 2496:         payoff_points = payload["payoff_points"]
   2497: 
```

### `self\._update_kpis\s*\(`
Ocorrências: **2**

#### Ocorrência 1
```text
   714: 
>> 715:         self._update_kpis(market, payoff_points)
   716:         self._render_legs(legs)
```
#### Ocorrência 2
```text
   2507: 
>> 2508:         self._update_kpis(market, payoff_points)
   2509:         self._render_legs(legs)
```

### `self\._render_charts\s*\(`
Ocorrências: **2**

#### Ocorrência 1
```text
   716:         self._render_legs(legs)
>> 717:         self._render_charts(market, payoff_points, asset, legs)
   718:         self._render_alerts(market, payoff_points, legs)
```
#### Ocorrência 2
```text
   2509:         self._render_legs(legs)
>> 2510:         self._render_charts(market, payoff_points, asset, legs)
   2511:         self._render_alerts(market, payoff_points, legs)
```

### `self\._render_alerts\s*\(`
Ocorrências: **2**

#### Ocorrência 1
```text
   717:         self._render_charts(market, payoff_points, asset, legs)
>> 718:         self._render_alerts(market, payoff_points, legs)
   719: 
```
#### Ocorrência 2
```text
   2510:         self._render_charts(market, payoff_points, asset, legs)
>> 2511:         self._render_alerts(market, payoff_points, legs)
   2512: 
```

### `def\s+_load_payoff_points\s*\(`
Ocorrências: **1**

#### Ocorrência 1
```text
   1131: 
>> 1132:     def _load_payoff_points(
   1133:         self,
```

### `def\s+_calculate_payoff_points_for_range\s*\(`
Ocorrências: **1**

#### Ocorrência 1
```text
   1269: 
>> 1270:     def _calculate_payoff_points_for_range(
   1271:         self,
```


# Conclusão operacional

- Se o backend não gerar `payoff_curve_points`, corrigir contrato de persistência antes da UI.
- Se o backend gerar payoff corretamente, bloquear/remover cálculo local da UI.
- O script `recalculate_payoff_curve_points_once.py` deve ser manutenção/legado, não fluxo oficial.
- Não criar outro serviço de comando se `PayoffRefreshCommandService` já existir.
