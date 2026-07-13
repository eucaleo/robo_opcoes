from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ParametrosAlerta:
    max_spread_pct: float = 0.03
    min_volume: float = 0
    payoff_delta_relevante: float = 0.0


@dataclass(frozen=True)
class SnapshotMercado:
    simbolo: str
    ultimo_preco: float | None = None
    vwap: float | None = None
    preco_anterior: float | None = None
    vwap_anterior: float | None = None
    bid: float | None = None
    ask: float | None = None
    volume: float | None = None
    payoff_anterior: float | None = None
    payoff_atual: float | None = None
    estrutura_favoravel: bool = False


@dataclass(frozen=True)
class AlertaDecisao:
    regra: str
    simbolo: str
    mensagem: str
    severidade: str = "INFO"
    timestamp: str | None = None


@dataclass(frozen=True)
class Decisao:
    classificacao: str
    permite_execucao: bool = False
    motivo: str = ""


@dataclass(frozen=True)
class ResultadoAvaliacao:
    simbolo: str
    alertas: tuple[AlertaDecisao, ...] = field(default_factory=tuple)
    decisao: Decisao = field(
        default_factory=lambda: Decisao(
            classificacao="SEM_ALERTA",
            permite_execucao=False,
            motivo="Nenhum alerta relevante identificado.",
        )
    )
    timestamp: str | None = None


def _valor_presente(valor: float | None) -> bool:
    return valor is not None


def _adicionar_alerta(
    alertas: list[AlertaDecisao],
    regra: str,
    snapshot: SnapshotMercado,
    mensagem: str,
    severidade: str,
    timestamp: str | None,
) -> None:
    alertas.append(
        AlertaDecisao(
            regra=regra,
            simbolo=snapshot.simbolo,
            mensagem=mensagem,
            severidade=severidade,
            timestamp=timestamp,
        )
    )


def avaliar_snapshot(
    snapshot: SnapshotMercado,
    parametros: ParametrosAlerta | None = None,
    *,
    timestamp: str | None = None,
) -> ResultadoAvaliacao:
    if not snapshot.simbolo or not snapshot.simbolo.strip():
        raise ValueError("simbolo obrigatorio")

    parametros = parametros or ParametrosAlerta()
    alertas: list[AlertaDecisao] = []

    classificacao = "SEM_ALERTA"
    motivo = "Nenhum alerta relevante identificado."

    if (
        _valor_presente(snapshot.bid)
        and _valor_presente(snapshot.ask)
        and snapshot.bid > 0
        and snapshot.ask >= snapshot.bid
    ):
        spread_pct = (snapshot.ask - snapshot.bid) / snapshot.bid

        if spread_pct > parametros.max_spread_pct:
            _adicionar_alerta(
                alertas,
                "SPREAD_ANORMAL",
                snapshot,
                "Spread acima do limite configurado.",
                "BLOQUEIO",
                timestamp,
            )
            classificacao = "EVITAR_OPERACAO"
            motivo = "Spread anormal detectado."

    if (
        _valor_presente(snapshot.volume)
        and snapshot.volume < parametros.min_volume
    ):
        _adicionar_alerta(
            alertas,
            "LIQUIDEZ_BAIXA",
            snapshot,
            "Volume abaixo do minimo configurado.",
            "BLOQUEIO",
            timestamp,
        )
        classificacao = "EVITAR_OPERACAO"
        motivo = "Liquidez baixa detectada."

    cruzamento_alta = (
        _valor_presente(snapshot.preco_anterior)
        and _valor_presente(snapshot.vwap_anterior)
        and _valor_presente(snapshot.ultimo_preco)
        and _valor_presente(snapshot.vwap)
        and snapshot.preco_anterior <= snapshot.vwap_anterior
        and snapshot.ultimo_preco > snapshot.vwap
    )

    if cruzamento_alta:
        _adicionar_alerta(
            alertas,
            "CRUZAMENTO_ALTA_VWAP",
            snapshot,
            "Preco cruzou o VWAP para cima.",
            "SINAL",
            timestamp,
        )

        if classificacao != "EVITAR_OPERACAO":
            classificacao = "ACOMPANHAR_ALTA"
            motivo = "Cruzamento de alta do VWAP identificado."

    if (
        _valor_presente(snapshot.ultimo_preco)
        and _valor_presente(snapshot.vwap)
        and snapshot.ultimo_preco > snapshot.vwap
    ):
        _adicionar_alerta(
            alertas,
            "PRECO_ACIMA_VWAP",
            snapshot,
            "Preco atual acima do VWAP.",
            "SINAL",
            timestamp,
        )

        if classificacao == "SEM_ALERTA":
            classificacao = "ACIMA_DO_VWAP"
            motivo = "Preco acima do VWAP identificado."

    if (
        _valor_presente(snapshot.payoff_anterior)
        and _valor_presente(snapshot.payoff_atual)
        and abs(snapshot.payoff_atual - snapshot.payoff_anterior)
        >= parametros.payoff_delta_relevante
    ):
        _adicionar_alerta(
            alertas,
            "PAYOFF_ALTERADO",
            snapshot,
            "Payoff alterado de forma relevante.",
            "SINAL",
            timestamp,
        )

        if classificacao == "SEM_ALERTA":
            classificacao = "SOMENTE_LEITURA"
            motivo = "Payoff alterado."

    if snapshot.estrutura_favoravel:
        _adicionar_alerta(
            alertas,
            "ESTRUTURA_FAVORAVEL",
            snapshot,
            "Estrutura favoravel identificada.",
            "SINAL",
            timestamp,
        )

        if classificacao == "SEM_ALERTA":
            classificacao = "SOMENTE_LEITURA"
            motivo = "Estrutura favoravel identificada."

    return ResultadoAvaliacao(
        simbolo=snapshot.simbolo,
        alertas=tuple(alertas),
        decisao=Decisao(
            classificacao=classificacao,
            permite_execucao=False,
            motivo=motivo,
        ),
        timestamp=timestamp,
    )
