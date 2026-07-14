from domain.decision import compute_decision_from_payoff


def test_compute_decision_from_payoff_should_work_without_alias_legacy_aba():
    """
    Garante que compute_decision_from_payoff funciona com payoff canônico
    que não carrega alias_legacy_aba -- substitui o teste de contract com dict.
    """
    payoff = {
        "pl_atual": 120.0,
        "pl_max":   200.0,
        "pl_min":   -50.0,
        "points":   [],
        "spot":     198.35,
    }

    result = compute_decision_from_payoff(
        payoff=payoff,
        dte_min=12,
    )

    assert "decision" in result
    assert "why" in result
    assert result["decision"] in ("HOLD", "WATCH", "PREPARE", "PREPARE_ROLL", "CLOSE_REOPEN", "CLOSE")
    # dte_min é registrado no why quando DTE gate é ativado
    # com dte_min=12 > dte_gate=7 não há gate, decisão depende do ratio
    assert isinstance(result.get("why"), dict)
