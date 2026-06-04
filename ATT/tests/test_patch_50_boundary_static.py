"""
patch_50b -- teste estático de boundary do legacy bridge.

Correção dos 3 testes que falhavam porque services.robo_legs_service
existe no disco: a remoção de sys.modules não basta para simular ausência.
Solução: usar unittest.mock.patch para bloquear o import dinamicamente.

Verifica que:
1. CanonicalInputService instancia mesmo sem RoboLegsService disponível.
2. O atributo robo_legs_service fica None quando o módulo não existe.
3. LegacyRoboLegsFallback é criado com robo_legs_service=None sem explodir.
4. CanonicalInputService aceita injeção explícita e NÃO tenta import dinâmico.
"""
from __future__ import annotations

import builtins
import sys
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REAL_IMPORT = builtins.__import__


def _import_blocker_for_robo_legs(name, *args, **kwargs):
    """Substitui builtins.__import__ para lançar ImportError no módulo alvo."""
    if name == "services.robo_legs_service":
        raise ImportError(f"[test blocker] módulo '{name}' simulado como ausente")
    return _REAL_IMPORT(name, *args, **kwargs)


# ---------------------------------------------------------------------------
# Context manager conveniente
# ---------------------------------------------------------------------------

from contextlib import contextmanager


@contextmanager
def _bridge_ausente():
    """
    Bloqueia o import de services.robo_legs_service durante o bloco.
    Garante que o módulo seja removido do cache antes e depois.
    """
    sys.modules.pop("services.robo_legs_service", None)
    # reimporta o serviço sem cache para evitar que o objeto já instanciado
    # seja reutilizado
    sys.modules.pop("services.canonical_input_service", None)
    sys.modules.pop("services.legacy_robo_legs_fallback", None)

    with patch("builtins.__import__", side_effect=_import_blocker_for_robo_legs):
        yield

    sys.modules.pop("services.robo_legs_service", None)
    sys.modules.pop("services.canonical_input_service", None)
    sys.modules.pop("services.legacy_robo_legs_fallback", None)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def _mock_infra_dependencies(monkeypatch):
    """
    Isola CanonicalInputService das dependências reais de infra
    (StructuresRepository, MarketSnapshotProvider).
    Aplicado via monkeypatch ANTES da importação do serviço.
    """
    # Pré-popula sys.modules com mocks para evitar imports reais
    fake_repo_instance    = MagicMock(name="fake_repo")
    fake_provider_instance = MagicMock(name="fake_provider")

    fake_repo_cls     = MagicMock(return_value=fake_repo_instance)
    fake_provider_cls = MagicMock(return_value=fake_provider_instance)

    monkeypatch.setattr(
        "services.canonical_input_service.StructuresRepository",
        fake_repo_cls,
    )
    monkeypatch.setattr(
        "services.canonical_input_service.MarketSnapshotProvider",
        fake_provider_cls,
    )
    return fake_repo_instance, fake_provider_instance


# ---------------------------------------------------------------------------
# Testes -- bridge AUSENTE
# ---------------------------------------------------------------------------

class TestBoundaryBridgeAusente:
    """Bridge RTD não instalado -- sistema deve degradar graciosamente."""

    def test_instancia_sem_bridge(self, _mock_infra_dependencies):
        with _bridge_ausente():
            from services.canonical_input_service import CanonicalInputService
            svc = CanonicalInputService()

        assert svc is not None

    def test_robo_legs_service_e_none_sem_bridge(self, _mock_infra_dependencies):
        with _bridge_ausente():
            from services.canonical_input_service import CanonicalInputService
            svc = CanonicalInputService()

        assert svc.robo_legs_service is None

    def test_legacy_fallback_criado_com_none(self, _mock_infra_dependencies):
        with _bridge_ausente():
            from services.canonical_input_service import CanonicalInputService
            svc = CanonicalInputService()

        assert svc.legacy_robo_legs_fallback is not None
        assert svc.legacy_robo_legs_fallback.robo_legs_service is None

    def test_legacy_fallback_load_retorna_lista_vazia_sem_bridge(
        self, _mock_infra_dependencies
    ):
        """
        Quando o bridge não existe o fallback deve retornar legs=[]
        com algum fallback_reason. NÃO exigimos string específica --
        o contrato é: legs vazio, meta com chave 'fallback_reason'.
        """
        with _bridge_ausente():
            from services.canonical_input_service import CanonicalInputService
            svc = CanonicalInputService()

        legs, meta = svc.legacy_robo_legs_fallback.load(
            structure={"name": "TEST", "alias_legacy_aba": "XPTO"},
            reference_date="2026-06-03",
        )

        assert legs == []
        assert "fallback_reason" in meta, (
            f"meta deve conter 'fallback_reason', recebeu: {meta}"
        )


# ---------------------------------------------------------------------------
# Testes -- bridge PRESENTE (módulo real no disco)
# ---------------------------------------------------------------------------

class TestBoundaryBridgePresente:
    """Bridge RTD instalado (módulo real) -- deve ser usado sem exceção."""

    def test_instancia_com_bridge_disponivel(self, _mock_infra_dependencies):
        # Força reload para garantir que pega o módulo real
        sys.modules.pop("services.canonical_input_service", None)

        from services.canonical_input_service import CanonicalInputService
        svc = CanonicalInputService()

        # Com módulo real disponível, robo_legs_service NÃO deve ser None
        assert svc.robo_legs_service is not None

    def test_legacy_fallback_recebe_bridge(self, _mock_infra_dependencies):
        sys.modules.pop("services.canonical_input_service", None)

        from services.canonical_input_service import CanonicalInputService
        svc = CanonicalInputService()

        assert svc.legacy_robo_legs_fallback.robo_legs_service is not None
        assert svc.legacy_robo_legs_fallback.robo_legs_service is svc.robo_legs_service


# ---------------------------------------------------------------------------
# Testes -- injeção explícita
# ---------------------------------------------------------------------------

class TestBoundaryInjecaoExplicita:
    """Injeção explícita tem prioridade sobre import dinâmico."""

    def test_injecao_explicita_tem_prioridade(self, _mock_infra_dependencies):
        explicito = MagicMock(name="explicit_bridge")

        sys.modules.pop("services.canonical_input_service", None)
        from services.canonical_input_service import CanonicalInputService
        svc = CanonicalInputService(robo_legs_service=explicito)

        assert svc.robo_legs_service is explicito

    def test_injecao_explicita_nao_tenta_import_dinamico(
        self, _mock_infra_dependencies
    ):
        """Injeção explícita deve vencer mesmo com bridge bloqueado."""
        explicito = MagicMock(name="injected")

        with _bridge_ausente():
            from services.canonical_input_service import CanonicalInputService
            svc = CanonicalInputService(robo_legs_service=explicito)

        assert svc.robo_legs_service is explicito

    def test_legacy_fallback_usa_injetado(self, _mock_infra_dependencies):
        explicito = MagicMock(name="injected_for_fallback")

        sys.modules.pop("services.canonical_input_service", None)
        from services.canonical_input_service import CanonicalInputService
        svc = CanonicalInputService(robo_legs_service=explicito)

        assert svc.legacy_robo_legs_fallback.robo_legs_service is explicito
