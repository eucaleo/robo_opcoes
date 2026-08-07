# repositories/market_snapshot_repository.py
"""
Repositorio canonico de snapshots de mercado.

Le legs RTD (rtd_analise_robo_legs), cotações RTD de opções
(rtd_option_quotes) e manuais (manual_analise_robo_legs), normaliza os campos
e retorna objetos LegMarketSnapshot prontos para uso.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from domain.refs.structure_ref import StructureRef

from domain.market_snapshot import (
    LegMarketSnapshot,
    SnapshotSource,
    StructureMarketSnapshot,
)

# --- Caminhos ----------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_DB = _PROJECT_ROOT / "dados" / "app.db"

RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"

# --- SQL ---------------------------------------------------------------------

_SQL_RTD_LEGS = """
    SELECT
        timestamp,
        aba,
        ativo,
        cv,
        call_put,
        quant,
        valor_executado,
        bid,
        ask,
        spread,
        spread_pct,
        iv,
        delta,
        gamma,
        theta,
        vega,
        strike,
        vencimento,
        dte,
        pl_realista
    FROM rtd_analise_robo_legs
    WHERE aba = ?
    ORDER BY timestamp DESC
"""

_SQL_MANUAL_LEGS = """
    SELECT
        timestamp,
        aba,
        ativo,
        cv,
        call_put,
        quant,
        valor_executado,
        bid,
        ask,
        spread,
        spread_pct,
        iv,
        delta,
        gamma,
        theta,
        vega,
        strike,
        vencimento,
        dte,
        pl_realista,
        source,
        created_at
    FROM manual_analise_robo_legs
    WHERE aba = ?
    ORDER BY timestamp DESC
"""

_SQL_RTD_SUMMARY = """
    SELECT
        aba,
        spot,
        num_pernas,
        dte_min,
        pl_realista_total,
        delta_liq,
        gamma_liq,
        theta_liq,
        vega_liq,
        spread_medio,
        spread_pct_medio,
        alertas_v2
    FROM rtd_analise_robo
    WHERE aba = ?
    ORDER BY rowid DESC
    LIMIT 1
"""

# --- Helpers -----------------------------------------------------------------


def _ref_to_aba(ref: StructureRef | str) -> str:
    """Aceita StructureRef ou str e devolve a string da aba."""
    if isinstance(ref, StructureRef):
        if ref.aba:
            return str(ref.aba)
        raise ValueError("StructureRef precisa ter aba preenchida para consulta de market snapshot.")
    return str(ref)


def _parse_br_float(value) -> Optional[float]:
    # Converte string pt-BR ('1,38' ou '1,38E-02') para float.
    if value is None:
        return None
    try:
        normalized = str(value).strip().replace(",", ".")
        return float(normalized)
    except (ValueError, TypeError):
        return None


def _first_float(*values) -> Optional[float]:
    for value in values:
        parsed = _parse_br_float(value)
        if parsed is not None:
            return parsed
    return None


def _first_text(*values) -> str | None:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def _mid_price(bid: Optional[float], ask: Optional[float]) -> Optional[float]:
    # Calcula mid price. Nao usa coluna 'last' - nao existe no schema.
    if bid is not None and ask is not None:
        return round((bid + ask) / 2.0, 6)
    if bid is not None:
        return bid
    if ask is not None:
        return ask
    return None


def _row_to_leg(row: sqlite3.Row, source: SnapshotSource) -> LegMarketSnapshot:
    bid = _parse_br_float(row["bid"])
    ask = _parse_br_float(row["ask"])
    mid = _mid_price(bid, ask)

    return LegMarketSnapshot(
        aba=row["aba"],
        ativo=row["ativo"],
        cv=row["cv"],
        call_put=row["call_put"],
        quant=_parse_br_float(row["quant"]),
        valor_executado=_parse_br_float(row["valor_executado"]),
        bid=bid,
        ask=ask,
        mid=mid,
        spread=_parse_br_float(row["spread"]),
        spread_pct=_parse_br_float(row["spread_pct"]),
        iv=_parse_br_float(row["iv"]),
        delta=_parse_br_float(row["delta"]),
        gamma=_parse_br_float(row["gamma"]),
        theta=_parse_br_float(row["theta"]),
        vega=_parse_br_float(row["vega"]),
        strike=_parse_br_float(row["strike"]),
        vencimento=row["vencimento"],
        dte=_parse_br_float(row["dte"]),
        pl_realista=_parse_br_float(row["pl_realista"]),
        timestamp=row["timestamp"],
        source=source,
    )


def _row_to_rtd_option_quote_leg(
    base_leg: LegMarketSnapshot,
    quote_row: sqlite3.Row,
) -> LegMarketSnapshot:
    """
    Converte uma cotação de rtd_option_quotes em LegMarketSnapshot mantendo
    os campos posicionais da leg RTD original.

    A tabela rtd_option_quotes é cache de cotação. Ela não define composição
    da estrutura. Por isso, quant/cv/dte/pl continuam vindo da leg estrutural
    em rtd_analise_robo_legs.
    """
    bid = _first_float(quote_row["bid"], base_leg.bid)
    ask = _first_float(quote_row["ask"], base_leg.ask)
    mid = _mid_price(bid, ask)
    ultimo_preco = _parse_br_float(quote_row["ultimo_preco"])

    valor_executado = _first_float(
        mid,
        ultimo_preco,
        base_leg.valor_executado,
    )

    ativo = _first_text(quote_row["codigo_opcao"], base_leg.ativo)

    return LegMarketSnapshot(
        aba=base_leg.aba,
        ativo=ativo,
        cv=base_leg.cv,
        call_put=_first_text(quote_row["call_put"], base_leg.call_put),
        quant=base_leg.quant,
        valor_executado=valor_executado,
        bid=bid,
        ask=ask,
        mid=mid,
        spread=base_leg.spread,
        spread_pct=base_leg.spread_pct,
        iv=_first_float(quote_row["iv"], base_leg.iv),
        delta=_first_float(quote_row["delta"], base_leg.delta),
        gamma=_first_float(quote_row["gamma"], base_leg.gamma),
        theta=_first_float(quote_row["theta"], base_leg.theta),
        vega=_first_float(quote_row["vega"], base_leg.vega),
        strike=_first_float(quote_row["strike"], base_leg.strike),
        vencimento=_first_text(quote_row["vencimento"], base_leg.vencimento),
        dte=base_leg.dte,
        pl_realista=base_leg.pl_realista,
        timestamp=_first_text(
            quote_row["updated_at"],
            quote_row["created_at"],
            base_leg.timestamp,
        ),
        source=RTD_OPTION_QUOTES_SOURCE,
    )


# --- Repositorio -------------------------------------------------------------


class MarketSnapshotRepository:
    """
    Acesso de leitura aos snapshots de mercado.

    Metodos:
      get_rtd_legs(aba)                -> lista de LegMarketSnapshot source=RTD
      get_rtd_option_quote_legs(aba)   -> lista enriquecida source=rtd_option_quotes
      get_manual_legs(aba)             -> lista de LegMarketSnapshot source=MANUAL
      get_rtd_summary(aba)             -> dict com cabecalho RTD ou None
      get_structure(aba)               -> StructureMarketSnapshot completo
    """

    def __init__(self, db_path: Path | str = _DEFAULT_DB) -> None:
        self._db_path = Path(db_path)
        if not self._db_path.exists():
            raise FileNotFoundError(f"Banco nao encontrado: {self._db_path}")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        return conn

    # -- Ponte canônica structure_id -> aba -----------------------------------

    def _resolve_aba_from_structure_id(self, structure_id: int) -> str:
        """
        Resolve a identidade canônica structure_id para o alias legado de aba.

        O MarketSnapshotRepository ainda lê tabelas RTD/manuais legadas que são
        indexadas por aba. Portanto, structure_id é a entrada canônica, mas a
        consulta física permanece por alias_legacy_aba enquanto essas tabelas
        existirem.
        """
        try:
            sid = int(structure_id)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"structure_id inválido para market snapshot: {structure_id!r}") from exc

        if sid <= 0:
            raise ValueError(f"structure_id deve ser positivo: {structure_id!r}")

        try:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    SELECT alias_legacy_aba
                      FROM structures
                     WHERE id = ?
                     LIMIT 1
                    """,
                    (sid,),
                ).fetchone()
        except sqlite3.OperationalError as exc:
            raise ValueError(
                "Tabela structures/coluna alias_legacy_aba indisponível para "
                f"resolver structure_id={sid}"
            ) from exc

        if row is None:
            raise ValueError(f"structure_id={sid} não encontrado em structures")

        aba = row["alias_legacy_aba"]
        if aba is None or not str(aba).strip():
            raise ValueError(f"structure_id={sid} sem alias_legacy_aba em structures")

        return str(aba).strip()

    def resolve_aba(
        self,
        ref: StructureRef | str | int | None = None,
        *,
        structure_id: int | None = None,
    ) -> str:
        """
        Normaliza entradas aceitas pelo repositório para aba legada.

        Preferência:
          1. structure_id explícito;
          2. StructureRef.aba, se disponível;
          3. StructureRef.structure_id resolvido via structures.alias_legacy_aba;
          4. int como structure_id;
          5. str como aba legada, para compatibilidade.
        """
        if structure_id is not None:
            return self._resolve_aba_from_structure_id(structure_id)

        if isinstance(ref, StructureRef):
            if ref.aba:
                return str(ref.aba).strip()
            if ref.structure_id is not None:
                return self._resolve_aba_from_structure_id(ref.structure_id)
            raise ValueError("StructureRef sem aba e sem structure_id para market snapshot.")

        if isinstance(ref, int) and not isinstance(ref, bool):
            return self._resolve_aba_from_structure_id(ref)

        if ref is None:
            raise ValueError("Informe ref, aba ou structure_id para market snapshot.")

        return str(ref).strip()

    # -- RTD ------------------------------------------------------------------

    def get_rtd_legs(
        self,
        ref: StructureRef | str | int | None = None,
        *,
        structure_id: int | None = None,
    ) -> list[LegMarketSnapshot]:
        aba = self.resolve_aba(ref, structure_id=structure_id)
        with self._connect() as conn:
            rows = conn.execute(_SQL_RTD_LEGS, (aba,)).fetchall()
        return [_row_to_leg(r, SnapshotSource.RTD) for r in rows]

    def get_rtd_option_quote_legs(
        self,
        ref: StructureRef | str | int | None = None,
        *,
        structure_id: int | None = None,
    ) -> list[LegMarketSnapshot]:
        """
        Retorna legs RTD enriquecidas com rtd_option_quotes.

        A composição da estrutura vem de rtd_analise_robo_legs. Para cada ativo
        dessa composição, se houver cotação em rtd_option_quotes.codigo_opcao,
        preço/greeks/strike/vencimento passam a vir da cotação centralizada.
        """
        base_legs = self.get_rtd_legs(ref, structure_id=structure_id)
        if not base_legs:
            return []

        ativos = sorted({
            str(leg.ativo).strip().upper()
            for leg in base_legs
            if leg.ativo and str(leg.ativo).strip()
        })
        if not ativos:
            return []

        placeholders = ", ".join("?" for _ in ativos)
        sql = f"""
            SELECT
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            FROM rtd_option_quotes
            WHERE UPPER(codigo_opcao) IN ({placeholders})
            ORDER BY updated_at DESC, created_at DESC
        """

        try:
            with self._connect() as conn:
                rows = conn.execute(sql, ativos).fetchall()
        except sqlite3.OperationalError:
            # Banco sem tabela rtd_option_quotes: mantém compatibilidade com
            # instalações/testes que ainda não possuem o cache centralizado.
            return []

        quote_by_codigo: dict[str, sqlite3.Row] = {}
        for row in rows:
            codigo = str(row["codigo_opcao"]).strip().upper()
            if codigo and codigo not in quote_by_codigo:
                quote_by_codigo[codigo] = row

        enriched: list[LegMarketSnapshot] = []
        for base_leg in base_legs:
            codigo = str(base_leg.ativo).strip().upper() if base_leg.ativo else ""
            quote_row = quote_by_codigo.get(codigo)
            if quote_row is not None:
                enriched.append(_row_to_rtd_option_quote_leg(base_leg, quote_row))

        return enriched

    def get_rtd_summary(
        self,
        ref: StructureRef | str | int | None = None,
        *,
        structure_id: int | None = None,
    ) -> Optional[dict]:
        aba = self.resolve_aba(ref, structure_id=structure_id)
        with self._connect() as conn:
            row = conn.execute(_SQL_RTD_SUMMARY, (aba,)).fetchone()
        if row is None:
            return None
        return dict(row)

    # -- Manual ---------------------------------------------------------------

    def get_manual_legs(
        self,
        ref: StructureRef | str | int | None = None,
        *,
        structure_id: int | None = None,
    ) -> list[LegMarketSnapshot]:
        aba = self.resolve_aba(ref, structure_id=structure_id)
        with self._connect() as conn:
            rows = conn.execute(_SQL_MANUAL_LEGS, (aba,)).fetchall()
        return [_row_to_leg(r, SnapshotSource.MANUAL) for r in rows]

    # -- Estrutura completa ---------------------------------------------------

    def get_structure(
        self,
        ref: StructureRef | str | int | None = None,
        source: SnapshotSource = SnapshotSource.RTD,
        *,
        structure_id: int | None = None,
    ) -> StructureMarketSnapshot:
        aba = self.resolve_aba(ref, structure_id=structure_id)

        if source == SnapshotSource.RTD:
            legs = self.get_rtd_legs(ref, structure_id=structure_id)
            summary = self.get_rtd_summary(ref, structure_id=structure_id)
        else:
            legs = self.get_manual_legs(ref, structure_id=structure_id)
            summary = None

        def _f(key: str) -> Optional[float]:
            return (
                _parse_br_float(summary[key])
                if summary and summary.get(key) is not None
                else None
            )

        return StructureMarketSnapshot(
            aba=aba,
            legs=legs,
            source=source,
            spot=_f("spot"),
            num_pernas=int(_f("num_pernas")) if _f("num_pernas") is not None else None,
            dte_min=int(_f("dte_min")) if _f("dte_min") is not None else None,
            pl_realista_total=_f("pl_realista_total"),
            delta_liq=_f("delta_liq"),
            gamma_liq=_f("gamma_liq"),
            theta_liq=_f("theta_liq"),
            vega_liq=_f("vega_liq"),
            spread_medio=_f("spread_medio"),
            spread_pct_medio=_f("spread_pct_medio"),
            alertas_v2=summary.get("alertas_v2") if summary else None,
        )
