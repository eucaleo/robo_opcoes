from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, Callable, Mapping

from rtd_excel_online import fase7_snapshot_adapter as adapter
from rtd_excel_online.fase7_alertas_decisao import (
    ParametrosAlerta,
    ResultadoAvaliacao,
    avaliar_snapshot,
)


class CotacaoRtdNaoEncontrada(LookupError):
    """Erro levantado quando a cotação local não é encontrada."""


def avaliar_codigo_opcao_local(
    codigo_opcao: str,
    parametros: ParametrosAlerta | None = None,
    *,
    quote_provider: Any | None = None,
    repository: Any | None = None,
    db_path: str | Path | None = None,
    preco_anterior: Any | None = None,
    vwap_anterior: Any | None = None,
    payoff_anterior: Any | None = None,
    payoff_atual: Any | None = None,
    estrutura_favoravel: bool | None = None,
) -> ResultadoAvaliacao:
    """
    Avalia uma opção usando exclusivamente uma fonte local de snapshot.

    A fonte pode ser injetada via quote_provider/repository para facilitar testes.
    Quando nenhuma fonte é informada, tenta localizar o repositório padrão do projeto.
    """
    codigo = _normalizar_codigo(codigo_opcao)

    provider = quote_provider or repository
    if provider is None:
        provider = _build_default_provider(db_path=db_path)

    quote = _buscar_quote_por_codigo(provider, codigo)

    if quote is None:
        raise CotacaoRtdNaoEncontrada(
            f"Cotação não encontrada para codigo_opcao: {codigo}"
        )

    return _avaliar_quote(
        quote,
        parametros,
        preco_anterior=preco_anterior,
        vwap_anterior=vwap_anterior,
        payoff_anterior=payoff_anterior,
        payoff_atual=payoff_atual,
        estrutura_favoravel=estrutura_favoravel,
    )


def snapshot_mercado_from_codigo_opcao_local(
    codigo_opcao: str,
    *,
    quote_provider: Any | None = None,
    repository: Any | None = None,
    db_path: str | Path | None = None,
    preco_anterior: Any | None = None,
    vwap_anterior: Any | None = None,
    payoff_anterior: Any | None = None,
    payoff_atual: Any | None = None,
    estrutura_favoravel: bool | None = None,
) -> Any:
    """
    Retorna apenas o SnapshotMercado correspondente ao código informado.
    """
    codigo = _normalizar_codigo(codigo_opcao)

    provider = quote_provider or repository
    if provider is None:
        provider = _build_default_provider(db_path=db_path)

    quote = _buscar_quote_por_codigo(provider, codigo)

    if quote is None:
        raise CotacaoRtdNaoEncontrada(
            f"Cotação não encontrada para codigo_opcao: {codigo}"
        )

    return _snapshot_from_quote(
        quote,
        preco_anterior=preco_anterior,
        vwap_anterior=vwap_anterior,
        payoff_anterior=payoff_anterior,
        payoff_atual=payoff_atual,
        estrutura_favoravel=estrutura_favoravel,
    )


def _normalizar_codigo(codigo_opcao: str) -> str:
    codigo = str(codigo_opcao or "").strip().upper()

    if not codigo:
        raise ValueError("codigo_opcao é obrigatório")

    return codigo


def _buscar_quote_por_codigo(provider: Any, codigo: str) -> Any | None:
    if isinstance(provider, Mapping):
        return provider.get(codigo) or provider.get(codigo.lower())

    if callable(provider):
        return provider(codigo)

    method_names = (
        "get_by_codigo_opcao",
        "get_by_codigo",
        "get_by_symbol",
        "buscar_por_codigo",
        "find_by_codigo",
        "obter_por_codigo",
    )

    for method_name in method_names:
        method = getattr(provider, method_name, None)
        if callable(method):
            return method(codigo)

    raise TypeError(
        "Fonte de cotações inválida. Informe um callable, Mapping ou repositório compatível."
    )


def _avaliar_quote(
    quote: Any,
    parametros: ParametrosAlerta | None,
    *,
    preco_anterior: Any | None = None,
    vwap_anterior: Any | None = None,
    payoff_anterior: Any | None = None,
    payoff_atual: Any | None = None,
    estrutura_favoravel: bool | None = None,
) -> ResultadoAvaliacao:
    fn = getattr(adapter, "avaliar_dado_rtd_quote", None)

    if callable(fn):
        return fn(
            quote,
            parametros,
            preco_anterior=preco_anterior,
            vwap_anterior=vwap_anterior,
            payoff_anterior=payoff_anterior,
            payoff_atual=payoff_atual,
            estrutura_favoravel=estrutura_favoravel,
        )

    fn = getattr(adapter, "avaliar_rtd_option_quote", None)

    if callable(fn):
        return fn(
            quote,
            parametros,
            preco_anterior=preco_anterior,
            vwap_anterior=vwap_anterior,
            payoff_anterior=payoff_anterior,
            payoff_atual=payoff_atual,
            estrutura_favoravel=estrutura_favoravel,
        )

    snapshot = _snapshot_from_quote(
        quote,
        preco_anterior=preco_anterior,
        vwap_anterior=vwap_anterior,
        payoff_anterior=payoff_anterior,
        payoff_atual=payoff_atual,
        estrutura_favoravel=estrutura_favoravel,
    )

    return avaliar_snapshot(
        snapshot,
        parametros,
        timestamp=_timestamp_from(quote),
    )


def _snapshot_from_quote(
    quote: Any,
    *,
    preco_anterior: Any | None = None,
    vwap_anterior: Any | None = None,
    payoff_anterior: Any | None = None,
    payoff_atual: Any | None = None,
    estrutura_favoravel: bool | None = None,
) -> Any:
    fn = getattr(adapter, "snapshot_mercado_from_rtd_option_quote", None)

    if callable(fn):
        return fn(
            quote,
            preco_anterior=preco_anterior,
            vwap_anterior=vwap_anterior,
            payoff_anterior=payoff_anterior,
            payoff_atual=payoff_atual,
            estrutura_favoravel=estrutura_favoravel,
        )

    fn = getattr(adapter, "adapt_snapshot_from_row", None)

    if callable(fn):
        return fn(
            quote,
            preco_anterior=preco_anterior,
            vwap_anterior=vwap_anterior,
            payoff_anterior=payoff_anterior,
            payoff_atual=payoff_atual,
            estrutura_favoravel=estrutura_favoravel,
        )

    raise RuntimeError("Adaptador de snapshot da Fase 7 não encontrado.")


def _timestamp_from(source: Any) -> str | None:
    for key in ("updated_at", "timestamp", "created_at", "captured_at"):
        if isinstance(source, Mapping):
            val = source.get(key)
        else:
            val = getattr(source, key, None)

        if val:
            return str(val)

    return None


def _build_default_provider(*, db_path: str | Path | None = None) -> Any:
    candidates = (
        (
            "rtd_excel_online.rtd_option_quotes_repository",
            "RtdOptionQuotesRepository",
        ),
        (
            "rtd_excel_online.rtd_option_quote_repository",
            "RtdOptionQuoteRepository",
        ),
        (
            "rtd_excel_online.repositories.rtd_option_quotes_repository",
            "RtdOptionQuotesRepository",
        ),
    )

    last_error: Exception | None = None

    for module_name, class_name in candidates:
        try:
            module = importlib.import_module(module_name)
            repo_class = getattr(module, class_name)

            if db_path is not None:
                try:
                    return repo_class(db_path)
                except TypeError:
                    return repo_class(str(db_path))

            return repo_class()
        except Exception as exc:
            last_error = exc

    raise RuntimeError(
        "Não foi possível inicializar o repositório local de cotações."
    ) from last_error
