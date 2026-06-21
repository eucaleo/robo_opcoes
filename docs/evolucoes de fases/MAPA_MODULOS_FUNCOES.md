# Mapa de Uso de SQL -- Tabela x Arquivo/Função (v2)

> Fonte: ATT/reports/sql_report_v3.json

## IF

- **bridge_ingest_csv.py**
    - linha 101: `conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({cols_sql})')`
    - linha 101: `conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({cols_sql})')`
- **create_payoff_summary_table.py**
    - linha 4: `CREATE TABLE IF NOT EXISTS payoff_curve_summary (`
    - linha 4: `CREATE TABLE IF NOT EXISTS payoff_curve_summary (`
- **db/derived_repo.py**
    - linha 19: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
    - linha 19: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
    - linha 42: `CREATE TABLE IF NOT EXISTS structure_decisions (`
    - linha 42: `CREATE TABLE IF NOT EXISTS structure_decisions (`
- **db/schema.py**
    - linha 7: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
    - linha 7: `CREATE TABLE IF NOT EXISTS payoff_curve_points (`
    - linha 25: `CREATE TABLE IF NOT EXISTS structure_decisions (`
    - linha 25: `CREATE TABLE IF NOT EXISTS structure_decisions (`
    - linha 51: `CREATE TABLE IF NOT EXISTS payoff_points (`
    - linha 51: `CREATE TABLE IF NOT EXISTS payoff_points (`
- **db/schema_excel.py**
    - linha 5: `CREATE TABLE IF NOT EXISTS robo_config (`
    - linha 5: `CREATE TABLE IF NOT EXISTS robo_config (`
    - linha 17: `CREATE TABLE IF NOT EXISTS robo_snapshot (`
    - linha 17: `CREATE TABLE IF NOT EXISTS robo_snapshot (`
    - linha 38: `CREATE TABLE IF NOT EXISTS robo_legs_snapshot (`
    - linha 38: `CREATE TABLE IF NOT EXISTS robo_legs_snapshot (`
    - linha 68: `CREATE TABLE IF NOT EXISTS robo_legs_history (`
    - linha 68: `CREATE TABLE IF NOT EXISTS robo_legs_history (`
    - linha 90: `CREATE TABLE IF NOT EXISTS encerramentos_manuais (`
    - linha 90: `CREATE TABLE IF NOT EXISTS encerramentos_manuais (`

---

## Lib

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3982: `# "class funclike" from Lib/test/test_inspect... on and on it goes.`
    - linha 3982: `# "class funclike" from Lib/test/test_inspect... on and on it goes.`

---

## None

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3512: `) from None`
    - linha 3512: `) from None`

---

## PEP

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1674: `# Add default and infer_variance parameters from PEP 696 and 695`
    - linha 1674: `# Add default and infer_variance parameters from PEP 696 and 695`

---

## Python

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 2456: `From Python 3.11, this can also be done using the `*` operator:`
    - linha 2456: `From Python 3.11, this can also be done using the `*` operator:`
    - linha 3464: `to the buffer protocol from Python code, and the`
    - linha 3464: `to the buffer protocol from Python code, and the`

---

## UI

- **scripts/fix_ui_debug.py**
    - linha 84: `t = ensure_import_once(t, "from UI.debug_utils import debug, info")`
    - linha 84: `t = ensure_import_once(t, "from UI.debug_utils import debug, info")`
    - linha 90: `t = ensure_import_once(t, "from UI.debug_utils import payoff_debug, payoff_info")`
    - linha 90: `t = ensure_import_once(t, "from UI.debug_utils import payoff_debug, payoff_info")`

---

## _UnionGenericAlias

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1566: `# 3.10: ForwardRefs of UnionType might be turned into _UnionGenericAlias`
    - linha 1566: `# 3.10: ForwardRefs of UnionType might be turned into _UnionGenericAlias`

---

## a

- **.venv/Lib/site-packages/six.py**
    - linha 983: `# Turn this module into a package.`
    - linha 983: `# Turn this module into a package.`
- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1444: `"""Strips Annotated, Required and NotRequired from a given type."""`
    - linha 1444: `"""Strips Annotated, Required and NotRequired from a given type."""`
    - linha 3314: `'can only inherit from a NamedTuple type and Generic')`
    - linha 3314: `'can only inherit from a NamedTuple type and Generic')`

---

## an

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3147: `# - Catch ValueError: maybe we're called from an unexpected module`
    - linha 3147: `# - Catch ValueError: maybe we're called from an unexpected module`

---

## both

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1096: `raise TypeError('cannot inherit from both a TypedDict type '`
    - linha 1096: `raise TypeError('cannot inherit from both a TypedDict type '`

---

## collections

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 37: `# ABCs (from collections.abc).`
    - linha 37: `# ABCs (from collections.abc).`

---

## cpython

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 230: `# Vendored from cpython typing._SpecialFrom`
    - linha 230: `# Vendored from cpython typing._SpecialFrom`

---

## e

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 858: `) from e`
    - linha 858: `) from e`
    - linha 3373: `raise RuntimeError(msg) from e`
    - linha 3373: `raise RuntimeError(msg) from e`

---

## from

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3344: `# update from user namespace without overriding special namedtuple attributes`
    - linha 3344: `# update from user namespace without overriding special namedtuple attributes`

---

## from_value

- **.venv/Lib/site-packages/six.py**
    - linha 753: `raise value from from_value`
    - linha 753: `raise value from from_value`

---

## further

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3698: `# Setting this attribute closes the TypeAliasType from further modification`
    - linha 3698: `# Setting this attribute closes the TypeAliasType from further modification`

---

## https

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3611: `# Copied and pasted from https://github.com/python/cpython/blob/986a4e1b6fcae7fe7a1d0a26aea446107dd5`
    - linha 3611: `# Copied and pasted from https://github.com/python/cpython/blob/986a4e1b6fcae7fe7a1d0a26aea446107dd5`

---

## list

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1831: `# Inherits from list as a workaround for Callable checks in Python < 3.9.2.`
    - linha 1831: `# Inherits from list as a workaround for Callable checks in Python < 3.9.2.`
    - linha 1935: `# Inherits from list as a workaround for Callable checks in Python < 3.9.2.`
    - linha 1935: `# Inherits from list as a workaround for Callable checks in Python < 3.9.2.`
    - linha 2025: `# This class inherits from list do not convert`
    - linha 2025: `# This class inherits from list do not convert`
    - linha 3733: `# Note in <= 3.9 _ConcatenateGenericAlias inherits from list`
    - linha 3733: `# Note in <= 3.9 _ConcatenateGenericAlias inherits from list`

---

## looking

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1955: `# Trick Generic into looking into this for __parameters__.`
    - linha 1955: `# Trick Generic into looking into this for __parameters__.`

---

## obj

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1489: `globals from obj (or the respective module's globals for classes),`
    - linha 1489: `globals from obj (or the respective module's globals for classes),`

---

## other

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 331: `Child classes of a disjoint base cannot inherit from other disjoint bases that are`
    - linha 331: `Child classes of a disjoint base cannot inherit from other disjoint bases that are`
    - linha 681: `f"Protocols can only inherit from other protocols, "`
    - linha 681: `f"Protocols can only inherit from other protocols, "`

---

## outside

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3152: `# If we somehow get invoked from outside typing.py,`
    - linha 3152: `# If we somehow get invoked from outside typing.py,`

---

## overlay

- **UI/components/payoff_chart.py**
    - linha 477: `# Extract xs, ys from overlay points list`
    - linha 477: `# Extract xs, ys from overlay points list`

---

## payoff_curve_points

- **UI/components/details_panel.py**
    - linha 376: `FROM payoff_curve_points`
    - linha 376: `FROM payoff_curve_points`
    - linha 463: `"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE aba = ?",`
    - linha 463: `"SELECT COUNT(*) AS n FROM payoff_curve_points WHERE aba = ?",`
- **UI/models/ui_data.py**
    - linha 519: `"FROM payoff_curve_points "`
    - linha 519: `"FROM payoff_curve_points "`
    - linha 543: `"SELECT timestamp FROM payoff_curve_points WHERE aba = ? ORDER BY timestamp DESC LIMIT 1",`
    - linha 543: `"SELECT timestamp FROM payoff_curve_points WHERE aba = ? ORDER BY timestamp DESC LIMIT 1",`
- **db/derived_repo.py**
    - linha 105: `INSERT OR REPLACE INTO payoff_curve_points`
    - linha 105: `INSERT OR REPLACE INTO payoff_curve_points`
    - linha 190: `FROM payoff_curve_points`
    - linha 190: `FROM payoff_curve_points`
    - linha 197: `FROM payoff_curve_points`
    - linha 197: `FROM payoff_curve_points`
    - linha 211: `DELETE FROM payoff_curve_points`
    - linha 211: `DELETE FROM payoff_curve_points`
- **db/reader.py**
    - linha 40: `FROM payoff_curve_points`
    - linha 40: `FROM payoff_curve_points`
    - linha 50: `FROM payoff_curve_points`
    - linha 50: `FROM payoff_curve_points`
    - linha 52: `SELECT MAX(timestamp) FROM payoff_curve_points WHERE aba = ?`
    - linha 52: `SELECT MAX(timestamp) FROM payoff_curve_points WHERE aba = ?`
    - linha 173: `cursor.execute("SELECT DISTINCT aba FROM payoff_curve_points ORDER BY aba")`
    - linha 173: `cursor.execute("SELECT DISTINCT aba FROM payoff_curve_points ORDER BY aba")`
    - linha 191: `FROM payoff_curve_points`
    - linha 191: `FROM payoff_curve_points`
- **db/writer.py**
    - linha 71: `INSERT INTO payoff_curve_points`
    - linha 71: `INSERT INTO payoff_curve_points`
    - linha 146: `FROM payoff_curve_points`
    - linha 146: `FROM payoff_curve_points`
- **scripts/build_payoff_summaries.py**
    - linha 19: `FROM payoff_curve_points`
    - linha 19: `FROM payoff_curve_points`
    - linha 32: `FROM payoff_curve_points`
    - linha 32: `FROM payoff_curve_points`
- **scripts/conferir_fechamento_v1.py**
    - linha 166: `FROM payoff_curve_points`
    - linha 166: `FROM payoff_curve_points`
- **scripts/derived_viewer.py**
    - linha 27: `FROM payoff_curve_points`
    - linha 27: `FROM payoff_curve_points`
- **services/derived_service.py**
    - linha 128: `FROM payoff_curve_points`
    - linha 128: `FROM payoff_curve_points`
    - linha 154: `FROM payoff_curve_points`
    - linha 154: `FROM payoff_curve_points`

---

## payoff_curve_summary

- **domain/payoff_features.py**
    - linha 175: `INSERT INTO payoff_curve_summary (`
    - linha 175: `INSERT INTO payoff_curve_summary (`

---

## payoff_points

- **UI/components/payoff_chart.py**
    - linha 414: `# Rebuild xs/ys from payoff_points (canonical: point_spot/point_pl)`
    - linha 414: `# Rebuild xs/ys from payoff_points (canonical: point_spot/point_pl)`

---

## plain

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 1108: `# typing.py generally doesn't let you inherit from plain Generic, unless`
    - linha 1108: `# typing.py generally doesn't let you inherit from plain Generic, unless`

---

## protocol

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 627: `# `__match_args__` attribute was removed from protocol members in 3.13,`
    - linha 627: `# `__match_args__` attribute was removed from protocol members in 3.13,`

---

## rtd_analise_robo

- **domain/decision.py**
    - linha 154: `cursor.execute("SELECT aba, pl_realista_total FROM rtd_analise_robo ORDER BY aba")`
    - linha 154: `cursor.execute("SELECT aba, pl_realista_total FROM rtd_analise_robo ORDER BY aba")`
- **domain/payoff.py**
    - linha 94: `SELECT * FROM rtd_analise_robo`
    - linha 94: `SELECT * FROM rtd_analise_robo`
    - linha 234: `cursor.execute("SELECT DISTINCT aba FROM rtd_analise_robo ORDER BY aba")`
    - linha 234: `cursor.execute("SELECT DISTINCT aba FROM rtd_analise_robo ORDER BY aba")`
- **scripts/run_derived_pipeline.py**
    - linha 38: `SELECT DISTINCT aba FROM rtd_analise_robo`
    - linha 38: `SELECT DISTINCT aba FROM rtd_analise_robo`

---

## rtd_analise_robo_legs

- **domain/payoff.py**
    - linha 60: `"SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",`
    - linha 60: `"SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",`
    - linha 72: `SELECT * FROM rtd_analise_robo_legs`
    - linha 72: `SELECT * FROM rtd_analise_robo_legs`

---

## rtd_consolidacoes

- **services/derived_service.py**
    - linha 214: `INSERT INTO rtd_consolidacoes (`
    - linha 214: `INSERT INTO rtd_consolidacoes (`

---

## six

- **.venv/Lib/site-packages/six.py**
    - linha 521: `"""Remove item from six.moves."""`
    - linha 521: `"""Remove item from six.moves."""`

---

## some

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 2440: `The type unpack operator takes the child types from some container type,`
    - linha 2440: `The type unpack operator takes the child types from some container type,`

---

## sqlite_master

- **UI/components/details_panel.py**
    - linha 53: `"SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (name,))`
    - linha 53: `"SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (name,))`
    - linha 98: `"SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",`
    - linha 98: `"SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",`
- **UI/models/ui_data.py**
    - linha 87: `cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")`
    - linha 87: `cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")`
- **scripts/conferir_fechamento_v1.py**
    - linha 34: `"SELECT name, type, sql FROM sqlite_master "`
    - linha 34: `"SELECT name, type, sql FROM sqlite_master "`
    - linha 44: `"SELECT 1 FROM sqlite_master WHERE name=? AND type=? LIMIT 1",`
    - linha 44: `"SELECT 1 FROM sqlite_master WHERE name=? AND type=? LIMIT 1",`
    - linha 48: `cur.execute("SELECT 1 FROM sqlite_master WHERE name=? LIMIT 1", (name,))`
    - linha 48: `cur.execute("SELECT 1 FROM sqlite_master WHERE name=? LIMIT 1", (name,))`
- **services/derived_service.py**
    - linha 105: `cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (name,))`
    - linha 105: `cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (name,))`

---

## structure_decisions

- **UI/components/details_panel.py**
    - linha 349: `FROM structure_decisions`
    - linha 349: `FROM structure_decisions`
    - linha 451: `FROM structure_decisions`
    - linha 451: `FROM structure_decisions`
- **db/derived_repo.py**
    - linha 163: `INSERT OR REPLACE INTO structure_decisions`
    - linha 163: `INSERT OR REPLACE INTO structure_decisions`
    - linha 223: `DELETE FROM structure_decisions`
    - linha 223: `DELETE FROM structure_decisions`
- **db/reader.py**
    - linha 87: `FROM structure_decisions`
    - linha 87: `FROM structure_decisions`
    - linha 177: `cursor.execute("SELECT DISTINCT aba FROM structure_decisions ORDER BY aba")`
    - linha 177: `cursor.execute("SELECT DISTINCT aba FROM structure_decisions ORDER BY aba")`
- **db/writer.py**
    - linha 113: `INSERT INTO structure_decisions`
    - linha 113: `INSERT INTO structure_decisions`
    - linha 129: `SELECT * FROM structure_decisions`
    - linha 129: `SELECT * FROM structure_decisions`
- **scripts/conferir_fechamento_v1.py**
    - linha 163: `FROM structure_decisions d`
    - linha 163: `FROM structure_decisions d`
- **scripts/derived_viewer.py**
    - linha 51: `FROM structure_decisions`
    - linha 51: `FROM structure_decisions`
- **services/derived_service.py**
    - linha 179: `FROM structure_decisions`
    - linha 179: `FROM structure_decisions`

---

## sys

- **.venv/Lib/site-packages/six.py**
    - linha 989: `# happen if six is removed from sys.modules and then reloaded. (Setuptools does`
    - linha 989: `# happen if six is removed from sys.modules and then reloaded. (Setuptools does`

---

## table

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 2312: `query("SELECT * FROM table")  # ok`
    - linha 2312: `query("SELECT * FROM table")  # ok`

---

## the

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 218: `Note that all the above statements are true from the point of view of`
    - linha 218: `Note that all the above statements are true from the point of view of`
    - linha 963: `"""Read data from the input stream and return it.`
    - linha 963: `"""Read data from the input stream and return it.`
    - linha 2275: `"""A special form representing the value that results from the evaluation`
    - linha 2275: `"""A special form representing the value that results from the evaluation`
    - linha 2450: `#  `TypeVar`s, which the `Unpack` is 'pulling out' directly into the`
    - linha 2450: `#  `TypeVar`s, which the `Unpack` is 'pulling out' directly into the`
    - linha 4027: `# "Inject" type parameters into the local namespace`
    - linha 4027: `# "Inject" type parameters into the local namespace`
    - linha 4091: `# "Inject" type parameters into the local namespace`
    - linha 4091: `# "Inject" type parameters into the local namespace`

---

## this

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 276: `# Note that inheriting from this class means that the object will be`
    - linha 276: `# Note that inheriting from this class means that the object will be`
    - linha 1040: `# Update this to something like >=3.13.0b1 if and when`
    - linha 1040: `# Update this to something like >=3.13.0b1 if and when`
    - linha 1955: `# Trick Generic into looking into this for __parameters__.`
    - linha 1955: `# Trick Generic into looking into this for __parameters__.`
    - linha 3469: `inherit from this ABC, either in a stub file or at runtime,`
    - linha 3469: `inherit from this ABC, either in a stub file or at runtime,`

---

## typing_extensions

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3807: `>>> from typing_extensions import Protocol, is_protocol`
    - linha 3807: `>>> from typing_extensions import Protocol, is_protocol`
    - linha 3828: `>>> from typing_extensions import Protocol, get_protocol_members`
    - linha 3828: `>>> from typing_extensions import Protocol, get_protocol_members`
    - linha 3861: `>>> from typing_extensions import Annotated, Doc`
    - linha 3861: `>>> from typing_extensions import Annotated, Doc`

---

## which

- **.venv/Lib/site-packages/typing_extensions.py**
    - linha 3765: `# as it is converted to a list from which no parameters are extracted.`
    - linha 3765: `# as it is converted to a list from which no parameters are extracted.`

---

