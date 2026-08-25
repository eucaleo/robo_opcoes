"""Boundary SQL isolado para services.derived_service.

Este modulo concentra dependencias SQLite e literais SQL removidos
de services/derived_service.py pela Frente 74b.
"""

from __future__ import annotations

import sqlite3 as SQLITE3

DERIVED_SERVICE_SQL_BOUNDARY_001 = '\n            SELECT timestamp, aba, point_spot, point_pl, meta_json\n            FROM payoff_curve_points\n            ORDER BY timestamp DESC, point_spot\n        '

DERIVED_SERVICE_SQL_BOUNDARY_002 = "\n                SELECT id, alias_legacy_aba\n                FROM structures\n                WHERE alias_legacy_aba IS NOT NULL\n                  AND alias_legacy_aba != ''\n            "

DERIVED_SERVICE_SQL_BOUNDARY_003 = '\n            SELECT timestamp, point_spot, point_pl, meta_json\n              FROM payoff_curve_points\n             WHERE '

DERIVED_SERVICE_SQL_BOUNDARY_004 = '\n            SELECT '

DERIVED_SERVICE_SQL_BOUNDARY_005 = 'PRAGMA table_info(structure_decisions)'
