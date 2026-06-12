# repositories/structures_repository.py
"""
Repositório canônico de estruturas e suas pernas (legs).

alteracao_11: conexões SQLite fechadas explicitamente via try/finally.
alteracao_42: get_structure_by_alias e get_structure_id_by_alias adicionados.
alteracao_63: fix _validate_leg -- leg_order aceita >= 0 (era >= 1, bug).
alteracao_70: revertido leg_order para >= 1 (0 é inválido; alteracao_63 era equivocado).
alteracao_72: audit trail -- toda mutacao registrada em structure_audit_log.
          _log_action() interno; atomico na mesma transacao do metodo.
          get_audit_log() e get_full_audit_log() para consulta.
          ensure_audit_schema() cria tabela e indices idx_audit_log_structure_id
          e idx_audit_log_changed_at.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALID_POSITION_SIDES: frozenset[str] = frozenset({"LONG", "SHORT"})
VALID_OPTION_TYPES: frozenset[str] = frozenset({"CALL", "PUT"})
VALID_STRUCTURE_STATUS: frozenset[str] = frozenset({"active", "archived"})

# Acoes validas registradas no audit log -- alteracao_72
AUDIT_ACTIONS: frozenset[str] = frozenset(
    {"CREATE", "UPDATE", "ARCHIVE", "ADD_LEG", "REPLACE_LEGS"}
)


# ---------------------------------------------------------------------------
# Helpers de validação / normalização (funções puras, sem I/O)
# ---------------------------------------------------------------------------

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_expiration_date(value: str) -> str:
    if value is None or not str(value).strip():
        raise ValueError("expiration_date is required")

    value = str(value).strip()

    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            "expiration_date must be a valid date in YYYY-MM-DD format"
        ) from exc

    return parsed.strftime("%Y-%m-%d")


def _normalize_structure_payload(data: dict[str, Any]) -> dict[str, Any]:
    name = str(data.get("name", "")).strip()
    underlying_asset = str(data.get("underlying_asset", "")).strip().upper()
    alias_legacy_aba = data.get("alias_legacy_aba")
    status = str(data.get("status", "active")).strip().lower()
    notes = data.get("notes")

    if not name:
        raise ValueError("name is required")

    if not underlying_asset:
        raise ValueError("underlying_asset is required")

    if status not in VALID_STRUCTURE_STATUS:
        raise ValueError(f"invalid status: {status}")

    if alias_legacy_aba is not None:
        alias_legacy_aba = str(alias_legacy_aba).strip() or None

    if notes is not None:
        notes = str(notes).strip() or None

    return {
        "name": name,
        "underlying_asset": underlying_asset,
        "alias_legacy_aba": alias_legacy_aba,
        "status": status,
        "notes": notes,
    }


def _validate_leg(leg: dict[str, Any]) -> dict[str, Any]:
    position_side   = leg.get("position_side")
    option_type     = leg.get("option_type")
    strike          = leg.get("strike")
    expiration_date = _validate_expiration_date(leg.get("expiration_date"))
    quantity        = leg.get("quantity")
    multiplier      = leg.get("multiplier", 1)
    symbol          = leg.get("symbol")
    notes           = leg.get("notes")

    if position_side not in VALID_POSITION_SIDES:
        raise ValueError(f"invalid position_side: {position_side}")

    if option_type not in VALID_OPTION_TYPES:
        raise ValueError(f"invalid option_type: {option_type}")

    try:
        strike = float(strike)
    except Exception as exc:
        raise ValueError("strike must be numeric") from exc

    if strike <= 0:
        raise ValueError("strike must be > 0")

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

    try:
        leg_order = int(leg.get("leg_order", 0))
    except Exception as exc:
        raise ValueError("leg_order must be integer") from exc

    if leg_order < 1:
        raise ValueError("leg_order must be >= 1")

    premium = leg.get("premium")
    if premium is not None:
        try:
            premium = float(premium)
        except Exception as exc:
            raise ValueError("premium must be numeric when provided") from exc

    if symbol is not None:
        symbol = str(symbol).strip() or None

    if notes is not None:
        notes = str(notes).strip() or None

    return {
        "position_side":   position_side,
        "option_type":     option_type,
        "symbol":          symbol,
        "strike":          strike,
        "expiration_date": expiration_date,
        "quantity":        quantity,
        "premium":         premium,
        "multiplier":      multiplier,
        "leg_order":       leg_order,
        "notes":           notes,
    }


# ---------------------------------------------------------------------------
# Repositório
# ---------------------------------------------------------------------------

class StructuresRepository:
    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = str(db_path)

    # ------------------------------------------------------------------
    # Infraestrutura de conexão
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        db_path = Path(self.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        return dict(row)

    def _fetch_legs(
        self, conn: sqlite3.Connection, structure_id: int
    ) -> list[dict[str, Any]]:
        rows = conn.execute(
            """
            SELECT
                id, structure_id, position_side, option_type, symbol,
                strike, expiration_date, quantity, premium, multiplier,
                leg_order, notes, created_at, updated_at
            FROM structure_legs
            WHERE structure_id = ?
            ORDER BY leg_order ASC, id ASC
            """,
            (structure_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def _ensure_structure_exists(
        self, conn: sqlite3.Connection, structure_id: int
    ) -> None:
        row = conn.execute(
            "SELECT id FROM structures WHERE id = ?",
            (structure_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"structure not found: {structure_id}")

    # ------------------------------------------------------------------
    # alteracao_72 -- Schema do audit log
    # ------------------------------------------------------------------

    def ensure_audit_schema(self, conn: sqlite3.Connection) -> None:
        """
        Cria a tabela structure_audit_log e seus indices caso nao existam.
        Deve ser chamado dentro de uma conexao aberta, antes do primeiro uso.
        Idempotente (CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS).

        alteracao_72
        """
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structure_audit_log (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id INTEGER NOT NULL,
                action       TEXT    NOT NULL,
                changed_by   TEXT,
                changed_at   TEXT    NOT NULL,
                before_json  TEXT,
                after_json   TEXT,
                notes        TEXT,
                FOREIGN KEY (structure_id) REFERENCES structures(id)
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_audit_log_structure_id
                ON structure_audit_log (structure_id)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_audit_log_changed_at
                ON structure_audit_log (changed_at)
            """
        )

    # ------------------------------------------------------------------
    # alteracao_72 -- Audit log interno
    # ------------------------------------------------------------------

    @staticmethod
    def _log_action(
        conn: sqlite3.Connection,
        structure_id: int,
        action: str,
        before: dict[str, Any] | None = None,
        after: dict[str, Any] | None = None,
        notes: str | None = None,
        changed_by: str | None = None,
    ) -> None:
        """
        Insere uma linha em structure_audit_log dentro da conexao ativa.
        Deve ser chamado ANTES do conn.commit() do metodo pai para garantir
        atomicidade. Nao abre conexao propria -- usa a conexao passada.
        Falhas sao silenciadas para nao derrubar a operacao principal.
        """
        try:
            conn.execute(
                """
                INSERT INTO structure_audit_log
                    (structure_id, action, changed_by, changed_at,
                     before_json, after_json, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    structure_id,
                    action,
                    changed_by,
                    _utc_now_iso(),
                    json.dumps(before, ensure_ascii=False) if before is not None else None,
                    json.dumps(after,  ensure_ascii=False) if after  is not None else None,
                    notes,
                ),
            )
        except Exception:
            # Log nao pode derrubar operacao principal
            pass

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def create_structure(self, data: dict[str, Any]) -> int:
        payload = _normalize_structure_payload(data)
        now = _utc_now_iso()

        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                INSERT INTO structures (
                    name, underlying_asset, alias_legacy_aba,
                    status, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["name"], payload["underlying_asset"],
                    payload["alias_legacy_aba"], payload["status"],
                    payload["notes"], now, now,
                ),
            )
            new_id = int(cursor.lastrowid)

            # alteracao_72: registrar criacao no audit log
            self._log_action(
                conn,
                structure_id=new_id,
                action="CREATE",
                before=None,
                after={**payload, "id": new_id, "created_at": now, "updated_at": now},
            )

            conn.commit()
            return new_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


    def create_structure_with_legs(
        self,
        data: dict[str, Any],
        legs: list[dict[str, Any]],
    ) -> int:
        """
        Cria uma estrutura e suas legs em uma única transação.

        Garante que não exista estrutura persistida sem legs caso a gravação
        de alguma perna falhe.
        """
        payload = _normalize_structure_payload(data)
        validated_legs = [_validate_leg(leg) for leg in legs]

        if not validated_legs:
            raise ValueError("estrutura deve ter ao menos uma leg")

        now = _utc_now_iso()

        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                INSERT INTO structures (
                    name, underlying_asset, alias_legacy_aba,
                    status, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["name"],
                    payload["underlying_asset"],
                    payload["alias_legacy_aba"],
                    payload["status"],
                    payload["notes"],
                    now,
                    now,
                ),
            )
            new_id = int(cursor.lastrowid)

            self._log_action(
                conn,
                structure_id=new_id,
                action="CREATE",
                before=None,
                after={
                    **payload,
                    "id": new_id,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            for leg in validated_legs:
                conn.execute(
                    """
                    INSERT INTO structure_legs (
                        structure_id, position_side, option_type, symbol,
                        strike, expiration_date, quantity, premium,
                        multiplier, leg_order, notes, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        new_id,
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

            self._log_action(
                conn,
                structure_id=new_id,
                action="REPLACE_LEGS",
                before=None,
                after={
                    "legs_count": len(validated_legs),
                    "replaced_at": now,
                },
            )

            conn.commit()
            return new_id

        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    def list_structures(
        self, include_archived: bool = False
    ) -> list[dict[str, Any]]:
        query = """
            SELECT id, name, underlying_asset, alias_legacy_aba,
                   status, notes, created_at, updated_at
            FROM structures
        """
        params: tuple[Any, ...] = ()

        if not include_archived:
            query += " WHERE status = ?"
            params = ("active",)

        query += " ORDER BY id ASC"

        conn = self._connect()
        try:
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_structure(self, structure_id: int) -> dict[str, Any] | None:
        conn = self._connect()
        try:
            row = conn.execute(
                """
                SELECT id, name, underlying_asset, alias_legacy_aba,
                       status, notes, created_at, updated_at
                FROM structures WHERE id = ?
                """,
                (structure_id,),
            ).fetchone()

            structure = self._row_to_dict(row)
            if structure is None:
                return None

            structure["legs"] = self._fetch_legs(conn, structure_id)
            return structure
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update_structure(self, structure_id: int, data: dict[str, Any]) -> None:
        current = self.get_structure(structure_id)
        if current is None:
            raise ValueError(f"structure not found: {structure_id}")

        # snapshot antes da mudanca (sem legs para manter log enxuto)
        before_snap = {k: v for k, v in current.items() if k != "legs"}

        merged = {
            "name":             data.get("name",             current["name"]),
            "underlying_asset": data.get("underlying_asset", current["underlying_asset"]),
            "alias_legacy_aba": data.get("alias_legacy_aba", current["alias_legacy_aba"]),
            "status":           data.get("status",           current["status"]),
            "notes":            data.get("notes",            current["notes"]),
        }
        payload = _normalize_structure_payload(merged)
        now = _utc_now_iso()

        conn = self._connect()
        try:
            conn.execute(
                """
                UPDATE structures
                SET name=?, underlying_asset=?, alias_legacy_aba=?,
                    status=?, notes=?, updated_at=?
                WHERE id=?
                """,
                (
                    payload["name"], payload["underlying_asset"],
                    payload["alias_legacy_aba"], payload["status"],
                    payload["notes"], now, structure_id,
                ),
            )

            # alteracao_72: registrar atualizacao no audit log
            self._log_action(
                conn,
                structure_id=structure_id,
                action="UPDATE",
                before=before_snap,
                after={**payload, "id": structure_id, "updated_at": now},
            )

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # ARCHIVE (soft-delete)
    # ------------------------------------------------------------------

    def archive_structure(self, structure_id: int) -> None:
        current = self.get_structure(structure_id)
        if current is None:
            raise ValueError(f"structure not found: {structure_id}")

        before_snap = {k: v for k, v in current.items() if k != "legs"}
        now = _utc_now_iso()

        conn = self._connect()
        try:
            self._ensure_structure_exists(conn, structure_id)
            conn.execute(
                "UPDATE structures SET status=?, updated_at=? WHERE id=?",
                ("archived", now, structure_id),
            )

            # alteracao_72: registrar arquivamento no audit log
            self._log_action(
                conn,
                structure_id=structure_id,
                action="ARCHIVE",
                before=before_snap,
                after={**before_snap, "status": "archived", "updated_at": now},
            )

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # LEGS
    # ------------------------------------------------------------------

    def add_leg(self, structure_id: int, leg_data: dict[str, Any]) -> int:
        leg = _validate_leg(leg_data)
        now = _utc_now_iso()

        conn = self._connect()
        try:
            self._ensure_structure_exists(conn, structure_id)

            cursor = conn.execute(
                """
                INSERT INTO structure_legs (
                    structure_id, position_side, option_type, symbol,
                    strike, expiration_date, quantity, premium,
                    multiplier, leg_order, notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    structure_id, leg["position_side"], leg["option_type"],
                    leg["symbol"], leg["strike"], leg["expiration_date"],
                    leg["quantity"], leg["premium"], leg["multiplier"],
                    leg["leg_order"], leg["notes"], now, now,
                ),
            )
            leg_id = int(cursor.lastrowid)

            conn.execute(
                "UPDATE structures SET updated_at=? WHERE id=?",
                (now, structure_id),
            )

            # alteracao_72: registrar adicao de leg no audit log
            self._log_action(
                conn,
                structure_id=structure_id,
                action="ADD_LEG",
                after={**leg, "id": leg_id, "structure_id": structure_id},
            )

            conn.commit()
            return leg_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def replace_legs(
        self, structure_id: int, legs: list[dict[str, Any]]
    ) -> None:
        validated_legs = [_validate_leg(leg) for leg in legs]
        now = _utc_now_iso()

        conn = self._connect()
        try:
            self._ensure_structure_exists(conn, structure_id)

            conn.execute(
                "DELETE FROM structure_legs WHERE structure_id=?",
                (structure_id,),
            )

            for leg in validated_legs:
                conn.execute(
                    """
                    INSERT INTO structure_legs (
                        structure_id, position_side, option_type, symbol,
                        strike, expiration_date, quantity, premium,
                        multiplier, leg_order, notes, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        structure_id, leg["position_side"], leg["option_type"],
                        leg["symbol"], leg["strike"], leg["expiration_date"],
                        leg["quantity"], leg["premium"], leg["multiplier"],
                        leg["leg_order"], leg["notes"], now, now,
                    ),
                )

            conn.execute(
                "UPDATE structures SET updated_at=? WHERE id=?",
                (now, structure_id),
            )

            # alteracao_72: registrar substituicao de legs no audit log
            self._log_action(
                conn,
                structure_id=structure_id,
                action="REPLACE_LEGS",
                after={"legs_count": len(validated_legs), "replaced_at": now},
            )

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # UTILITÁRIOS
    # ------------------------------------------------------------------

    def count_legs(self, structure_id: int) -> int:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM structure_legs WHERE structure_id=?",
                (structure_id,),
            ).fetchone()
            return int(row["n"]) if row else 0
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # LOOKUP POR ALIAS LEGADO (alteracao_42)
    # ------------------------------------------------------------------

    def get_structure_by_alias(self, alias: str) -> dict[str, Any] | None:
        if not alias or not str(alias).strip():
            return None

        alias = str(alias).strip()

        conn = self._connect()
        try:
            row = conn.execute(
                """
                SELECT id, name, underlying_asset, alias_legacy_aba,
                       status, notes, created_at, updated_at
                FROM structures
                WHERE alias_legacy_aba = ? AND status = 'active'
                ORDER BY id DESC LIMIT 1
                """,
                (alias,),
            ).fetchone()

            structure = self._row_to_dict(row)
            if structure is None:
                return None

            structure["legs"] = self._fetch_legs(conn, structure["id"])
            return structure
        finally:
            conn.close()

    def get_structure_id_by_alias(self, alias: str) -> int | None:
        result = self.get_structure_by_alias(alias)
        if result is None:
            return None
        return int(result["id"])

    # ------------------------------------------------------------------
    # AUDIT LOG -- leitura (alteracao_72)
    # ------------------------------------------------------------------

    def get_audit_log(
        self,
        structure_id: int,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Retorna o historico de mutacoes de uma estrutura ordenado do mais
        recente para o mais antigo. Limite padrao: 50 registros.
        """
        conn = self._connect()
        try:
            rows = conn.execute(
                """
                SELECT id, structure_id, action, changed_by,
                       changed_at, before_json, after_json, notes
                FROM structure_audit_log
                WHERE structure_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (structure_id, limit),
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_full_audit_log(
        self,
        limit: int = 200,
        action: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retorna audit log global, opcionalmente filtrado por action.
        Util para scripts de governanca e relatorios de fase 8.
        """
        conn = self._connect()
        try:
            if action:
                rows = conn.execute(
                    """
                    SELECT id, structure_id, action, changed_by,
                           changed_at, before_json, after_json, notes
                    FROM structure_audit_log
                    WHERE action = ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (action, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT id, structure_id, action, changed_by,
                           changed_at, before_json, after_json, notes
                    FROM structure_audit_log
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
