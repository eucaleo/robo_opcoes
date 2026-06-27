from __future__ import annotations

from datetime import date, datetime
from typing import Any


def _first(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return default


def _number(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def _upper(value: Any) -> str:
    return _text(value).upper()


def _normalizar_tipo_opcao(value: Any) -> str | None:
    raw = _upper(value)

    if raw in {"CALL", "C", "COMPRA_CALL"}:
        return "CALL"

    if raw in {"PUT", "P", "VENDA_PUT"}:
        return "PUT"

    return None


def _normalizar_direcao(value: Any) -> str | None:
    raw = _upper(value)

    if raw in {"BUY", "B", "COMPRA", "COMPRADA", "LONG", "C"}:
        return "BUY"

    if raw in {"SELL", "S", "VENDA", "VENDIDA", "SHORT", "V"}:
        return "SELL"

    return None


def calcular_intrinseco(tipo: str, preco_ativo: float, strike: float) -> float:
    if tipo == "CALL":
        return max(preco_ativo - strike, 0.0)

    if tipo == "PUT":
        return max(strike - preco_ativo, 0.0)

    raise ValueError(f"Tipo de opcao invalido: {tipo}")


def calcular_extrinseco(preco_opcao: float | None, intrinseco: float) -> float | None:
    if preco_opcao is None:
        return None

    return preco_opcao - intrinseco


def calcular_pl_atual_perna(
    direcao: str,
    premio_entrada: float,
    preco_atual: float | None,
    quantidade: float,
) -> float | None:
    if preco_atual is None:
        return None

    if direcao == "BUY":
        return (preco_atual - premio_entrada) * quantidade

    if direcao == "SELL":
        return (premio_entrada - preco_atual) * quantidade

    raise ValueError(f"Direcao invalida: {direcao}")


def calcular_payoff_vencimento_perna(
    tipo: str,
    direcao: str,
    preco_simulado: float,
    strike: float,
    premio_entrada: float,
    quantidade: float,
) -> float:
    intrinseco = calcular_intrinseco(tipo, preco_simulado, strike)

    if direcao == "BUY":
        return (intrinseco - premio_entrada) * quantidade

    if direcao == "SELL":
        return (premio_entrada - intrinseco) * quantidade

    raise ValueError(f"Direcao invalida: {direcao}")


def _valor_atual_assinado(direcao: str, preco_atual: float | None, quantidade: float) -> float | None:
    if preco_atual is None:
        return None

    if direcao == "BUY":
        return preco_atual * quantidade

    if direcao == "SELL":
        return -preco_atual * quantidade

    return None


def _custo_inicial_assinado(direcao: str, premio_entrada: float, quantidade: float) -> float:
    if direcao == "BUY":
        return premio_entrada * quantidade

    if direcao == "SELL":
        return -premio_entrada * quantidade

    return 0.0


def _dias_ate_vencimento(vencimento: Any, hoje: date | None = None) -> int | None:
    if not vencimento:
        return None

    hoje = hoje or date.today()

    if isinstance(vencimento, datetime):
        data_vencimento = vencimento.date()
    elif isinstance(vencimento, date):
        data_vencimento = vencimento
    else:
        texto = str(vencimento)[:10]
        try:
            data_vencimento = datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            return None

    return (data_vencimento - hoje).days


def montar_linha_perna(
    leg: dict[str, Any],
    preco_ativo_atual: float,
) -> dict[str, Any]:
    ticker = _first(leg, "ticker", "codigo", "codigo_opcao", "option_ticker", default="")
    tipo = _normalizar_tipo_opcao(_first(leg, "type", "tipo", "call_put", "option_type"))
    direcao = _normalizar_direcao(_first(leg, "side", "direcao", "direction", "position_side"))

    strike = _number(_first(leg, "strike", "preco_exercicio"))
    quantidade = _number(_first(leg, "quantity", "quantidade", "qty"), 0.0)
    premio_entrada = _number(_first(leg, "entryPremium", "entry_premium", "premio_entrada", "preco_entrada"))
    preco_atual = _number(_first(leg, "currentPremium", "current_premium", "preco_atual", "ultimo_preco"))
    vencimento = _first(leg, "expirationDate", "expiration_date", "vencimento")

    erros: list[str] = []

    if not ticker:
        erros.append("ticker ausente")

    if tipo is None:
        erros.append("tipo da opcao ausente ou invalido")

    if direcao is None:
        erros.append("direcao ausente ou invalida")

    if strike is None:
        erros.append("strike ausente")

    if quantidade is None or quantidade <= 0:
        erros.append("quantidade ausente ou invalida")

    if premio_entrada is None:
        erros.append("premio de entrada ausente")

    if vencimento is None:
        erros.append("vencimento ausente")

    if erros:
        return {
            "ticker": ticker,
            "tipo": tipo,
            "direcao": direcao,
            "quantidade": quantidade,
            "strike": strike,
            "vencimento": vencimento,
            "premio_entrada": premio_entrada,
            "preco_atual": preco_atual,
            "status": "invalida",
            "erros": erros,
        }

    intrinseco_atual = calcular_intrinseco(tipo, preco_ativo_atual, strike)
    extrinseco_atual = calcular_extrinseco(preco_atual, intrinseco_atual)

    pl_atual = calcular_pl_atual_perna(
        direcao=direcao,
        premio_entrada=premio_entrada,
        preco_atual=preco_atual,
        quantidade=quantidade,
    )

    payoff_vencimento_ao_preco_atual = calcular_payoff_vencimento_perna(
        tipo=tipo,
        direcao=direcao,
        preco_simulado=preco_ativo_atual,
        strike=strike,
        premio_entrada=premio_entrada,
        quantidade=quantidade,
    )

    return {
        "ticker": ticker,
        "tipo": tipo,
        "direcao": direcao,
        "quantidade": quantidade,
        "strike": strike,
        "vencimento": vencimento,
        "premio_entrada": premio_entrada,
        "preco_atual": preco_atual,
        "intrinseco_atual": intrinseco_atual,
        "extrinseco_atual": extrinseco_atual,
        "pl_atual": pl_atual,
        "payoff_vencimento_ao_preco_atual": payoff_vencimento_ao_preco_atual,
        "valor_atual_assinado": _valor_atual_assinado(direcao, preco_atual, quantidade),
        "custo_inicial_assinado": _custo_inicial_assinado(direcao, premio_entrada, quantidade),
        "status": "ok",
        "erros": [],
    }


def montar_view_model_payoff_analitico(payload: dict[str, Any]) -> dict[str, Any]:
    structure_id = _first(payload, "structure_id", "structureId", "id")
    nome = _first(payload, "name", "nome", "structure_name", "structureName")
    ativo_base = _first(payload, "underlying", "underlying_asset", "ativo_base", "underlyingAsset")

    preco_implantacao = _number(
        _first(
            payload,
            "underlying_price_at_deployment",
            "underlyingPriceAtDeployment",
            "preco_base_implantacao",
        )
    )

    preco_atual = _number(
        _first(
            payload,
            "current_underlying_price",
            "currentUnderlyingPrice",
            "spot_price",
            "preco_base_atual",
        )
    )

    market_snapshot_source = _first(payload, "market_snapshot_source", "snapshot_source")
    is_static_fallback = bool(_first(payload, "is_static_fallback", "static_fallback", default=False))
    is_current_market = bool(_first(payload, "is_current_market", default=False))

    pernas = _first(payload, "legs", "pernas", "structure_legs", default=[])
    data_implantacao = _first(payload, "deployed_at", "deployedAt", "created_at", "data_implantacao")
    data_analise = _first(payload, "calculated_at", "calculatedAt", "data_analise")
    vencimento = _first(payload, "expiration_date", "expirationDate", "vencimento")

    erros: list[str] = []

    if structure_id is None:
        erros.append("structure_id ausente")

    if not ativo_base:
        erros.append("ativo-base ausente")

    if preco_implantacao is None:
        erros.append("preco de implantacao ausente")

    if preco_atual is None or preco_atual <= 0:
        erros.append("preco atual do ativo-base ausente ou invalido")

    if is_static_fallback:
        erros.append("fonte de mercado esta em fallback estatico")

    if not isinstance(pernas, list) or not pernas:
        erros.append("pernas da estrutura ausentes")

    linhas_pernas: list[dict[str, Any]] = []

    if preco_atual is not None and preco_atual > 0 and isinstance(pernas, list):
        for leg in pernas:
            if isinstance(leg, dict):
                linhas_pernas.append(montar_linha_perna(leg, preco_atual))

    for linha in linhas_pernas:
        if linha.get("status") != "ok":
            erros.append(f"perna invalida: {linha.get('ticker') or 'sem ticker'}")

    valores_atuais = [
        linha["valor_atual_assinado"]
        for linha in linhas_pernas
        if linha.get("valor_atual_assinado") is not None
    ]

    pls_atuais = [
        linha["pl_atual"]
        for linha in linhas_pernas
        if linha.get("pl_atual") is not None
    ]

    custos_iniciais = [
        linha["custo_inicial_assinado"]
        for linha in linhas_pernas
        if linha.get("custo_inicial_assinado") is not None
    ]

    payoffs_ao_preco_atual = [
        linha["payoff_vencimento_ao_preco_atual"]
        for linha in linhas_pernas
        if linha.get("payoff_vencimento_ao_preco_atual") is not None
    ]

    custo_inicial = sum(custos_iniciais)
    valor_atual_estrutura = sum(valores_atuais) if valores_atuais else None
    pl_atual = sum(pls_atuais) if pls_atuais else None

    if custo_inicial:
        pl_atual_percentual = None if pl_atual is None else pl_atual / abs(custo_inicial) * 100
    else:
        pl_atual_percentual = None

    payoff_vencimento_ao_preco_atual = (
        sum(payoffs_ao_preco_atual) if payoffs_ao_preco_atual else None
    )

    return {
        "identificacao_estrutura": {
            "structure_id": structure_id,
            "nome": nome,
            "ativo_base": ativo_base,
            "data_implantacao": data_implantacao,
            "data_analise": data_analise,
            "vencimento_principal": vencimento,
            "quantidade_pernas": len(pernas) if isinstance(pernas, list) else 0,
        },
        "snapshot_implantacao": {
            "preco_base_na_implantacao": preco_implantacao,
            "data_implantacao": data_implantacao,
            "vencimento": vencimento,
            "dias_ate_vencimento_na_implantacao": _first(
                payload,
                "days_to_expiration_at_deployment",
                "daysToExpirationAtDeployment",
            ),
            "custo_inicial_estrutura": custo_inicial,
        },
        "snapshot_atual": {
            "preco_base_atual": preco_atual,
            "fonte_preco_atual": market_snapshot_source,
            "is_static_fallback": is_static_fallback,
            "is_current_market": is_current_market,
            "data_analise": data_analise,
            "dias_restantes": _first(
                payload,
                "days_to_expiration",
                "daysToExpiration",
                default=_dias_ate_vencimento(vencimento),
            ),
            "valor_atual_estrutura": valor_atual_estrutura,
            "pl_atual_financeiro": pl_atual,
            "pl_atual_percentual": pl_atual_percentual,
        },
        "tabela_pernas": linhas_pernas,
        "payoff_vencimento": {
            "preco_usado_na_curva": preco_atual,
            "preco_simulado_no_vencimento": None,
            "payoff_no_vencimento_ao_preco_atual": payoff_vencimento_ao_preco_atual,
            "resultado_simulado_no_vencimento": None,
        },
        "separacao_visual_obrigatoria": {
            "exibir_pl_atual_separado": True,
            "exibir_payoff_vencimento_separado": True,
            "exibir_snapshot_implantacao": True,
            "exibir_snapshot_atual": True,
            "exibir_tabela_por_perna": True,
        },
        "validacao": {
            "status": "ok" if not erros else "erro",
            "erros": erros,
        },
    }
