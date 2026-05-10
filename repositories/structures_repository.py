import sqlite3
from datetime import datetime
from pathlib import Path


VALID_STATUS = {"active", "archived"}
VALID_POSITION_SIDES = {"LONG", "SHORT"}
VALID_OPTION_TYPES = {"CALL", "PUT"}


def _utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat()


def _validate_non_empty(value: str, field_name: str) -> str:
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} is required")
    return str(value).strip()


def _validate_status(status: str) -> str:
    if status not in VALID_STATUS:
        raise ValueError(f"invalid status: {status}")
    return status


def _validate_leg(leg: dict) -> dict:
    position_side = leg.get("position_side")
    option_type = leg.get("option_type")
    strike = leg.get("strike")
    expiration_date = leg.get("expiration_date")
    quantity = leg.get("quantity")
    multiplier = leg.get("multiplier", 1)

    if position_side not in VALID_POSITION_SIDES:
        raise ValueError(f"invalid position_side: {position_side}")

    if option_type not in VALID_OPTION_TYPES:
        raise ValueError(f"invalid option_type: {option_type}")

    try:
        strike = float(strike)
    except Exception as exc:
        raise ValueError("strike must be numeric") from exc

    if not str(expiration_date).strip():
        raise ValueError("expiration_date is required")

    try:
        quantity = int(quantity)
    except Exception as exc:
        raise ValueError("quantity must be integer") from exc

    if quantity <= 0:
        raise ValueError("quantity must be > 0")

    try:
        multiplier = float(multiplier)
    except Exception as exc:
        raise ValueError("multiplier must be numeric") from exc

    if multiplier <= 0:
        raise ValueError("multiplier must be > 0")

    premium = leg.get("premium")
    if premium is not None:
        premium = float(premium)

    return {
        "position_side": position_side,
        "option_type": option_type,
        "symbol": leg.get("symbol"),
        "strike": strike,
        "expiration_date": str(expiration_date).strip(),
        "quantity": quantity,
        "premium": premium,
        "multiplier": multiplier,
        "leg_order": int(leg.get("leg_order", 0)),
        "notes": leg.get("notes"),
    }


class StructuresRepository:
    def __init__(self, db_path: str | Path = "dados/app.db"):
        self.db_path = str(db_path)

    def _connect(self):
        db_path = Path(self.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def create_structure(self, data: dict) -> int:
        name = _validate_non_empty(data.get("name"), "name")
        underlying_asset = _validate_non_empty(data.get("underlying_asset"), "underlying_asset")
        status = _validate_status(data.get("status", "active"))
        alias_legacy_aba = data.get("alias_legacy_aba")
        notes = data.get("notes")
        now = _utc_now_iso()

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO structures (
                    name, underlying_asset, alias_legacy_aba, status, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, underlying_asset, alias_legacy_aba, status, notes, now, now),
            )
            conn.commit()
            return cursor.lastrowid

    def add_leg(self, structure_id: int, leg_data: dict) -> int:
        leg = _validate_leg(leg_data)
        now = _utc_now_iso()

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO structure_legs (
                    structure_id, position_side, option_type, symbol, strike,
                    expiration_date, quantity, premium, multiplier, leg_order,
                    notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    structure_id,
                    leg["position_side"],
                    leg["option_type"],
                    leg["symbol"],
                    leg["strike"],
                    leg["expiration_date"],
                    leg["quantity"],
                    leg["premium"],
                    leg["multiplier"],
                    leg["leg_order"],
                    leg["notes"],
                    now,
                    now,
                ),
            )

            conn.execute(
                "UPDATE structures SET updated_at = ? WHERE id = ?",
                (now, structure_id),
            )

            conn.commit()
            return cursor.lastrowid

    def get_structure(self, structure_id: int) -> dict | None:
        with self._connect() as conn:
            structure = conn.execute(
                "SELECT * FROM structures WHERE id = ?",
                (structure_id,),
            ).fetchone()

            if not structure:
                return None

            legs = conn.execute(
                """
                SELECT * FROM structure_legs
                WHERE structure_id = ?
                ORDER BY leg_order ASC, id ASC
                """,
                (structure_id,),
            ).fetchall()

            return {
                **dict(structure),
                "legs": [dict(row) for row in legs],
            }

    def list_structures(self, include_archived: bool = False) -> list[dict]:
        query = "SELECT * FROM structures"
        params = ()

        if not include_archived:
            query += " WHERE status = ?"
            params = ("active",)

        query += " ORDER BY id DESC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def update_structure(self, structure_id: int, updates: dict) -> None:
        allowed_fields = {
            "name",
            "underlying_asset",
            "alias_legacy_aba",
            "status",
            "notes",
        }

        set_clauses = []
        values = []

        for field, value in updates.items():
            if field not in allowed_fields:
                continue

            if field == "name":
                value = _validate_non_empty(value, "name")
            elif field == "underlying_asset":
                value = _validate_non_empty(value, "underlying_asset")
            elif field == "status":
                value = _validate_status(value)

            set_clauses.append(f"{field} = ?")
            values.append(value)

        if not set_clauses:
            return

        values.append(_utc_now_iso())
        values.append(structure_id)

        with self._connect() as conn:
            conn.execute(
                f"""
                UPDATE structures
                SET {", ".join(set_clauses)}, updated_at = ?
                WHERE id = ?
                """,
                values,
            )
            conn.commit()

    def replace_legs(self, structure_id: int, legs: list[dict]) -> None:
        normalized_legs = []

        for index, leg in enumerate(legs, start=1):
            leg = dict(leg)
            leg.setdefault("leg_order", index)
            normalized_legs.append(_validate_leg(leg))

        now = _utc_now_iso()

        with self._connect() as conn:
            conn.execute("DELETE FROM structure_legs WHERE structure_id = ?", (structure_id,))

            for leg in normalized_legs:
                conn.execute(
                    """
                    INSERT INTO structure_legs (
                        structure_id, position_side, option_type, symbol, strike,
                        expiration_date, quantity, premium, multiplier, leg_order,
                        notes, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        structure_id,
                        leg["position_side"],
                        leg["option_type"],
                        leg["symbol"],
                        leg["strike"],
                        leg["expiration_date"],
                        leg["quantity"],
                        leg["premium"],
                        leg["multiplier"],
                        leg["leg_order"],
                        leg["notes"],
                        now,
                        now,
                    ),
                )

            conn.execute(
                "UPDATE structures SET updated_at = ? WHERE id = ?",
                (now, structure_id),
            )

            conn.commit()

    def archive_structure(self, structure_id: int) -> None:
        self.update_structure(structure_id, {"status": "archived"})
