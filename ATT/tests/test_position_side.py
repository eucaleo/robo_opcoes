import pytest

from domain.position_side import normalize_position_side, to_pricing_engine_side


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("C", "COMPRADO"),
        ("COMPRA", "COMPRADO"),
        ("COMPRADO", "COMPRADO"),
        ("LONG", "COMPRADO"),
        (" c ", "COMPRADO"),
        (" compra ", "COMPRADO"),
        (" comprado ", "COMPRADO"),
        (" long ", "COMPRADO"),
        ("V", "VENDIDO"),
        ("VENDA", "VENDIDO"),
        ("VENDIDO", "VENDIDO"),
        ("SHORT", "VENDIDO"),
        (" v ", "VENDIDO"),
        (" venda ", "VENDIDO"),
        (" vendido ", "VENDIDO"),
        (" short ", "VENDIDO"),
    ],
)
def test_normalize_position_side_accepts_aliases(raw, expected):
    assert normalize_position_side(raw) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("COMPRADO", "LONG"),
        ("C", "LONG"),
        ("LONG", "LONG"),
        ("VENDIDO", "SHORT"),
        ("V", "SHORT"),
        ("SHORT", "SHORT"),
    ],
)
def test_to_pricing_engine_side_converts_to_long_short_only_at_technical_boundary(raw, expected):
    assert to_pricing_engine_side(raw) == expected


@pytest.mark.parametrize("raw", [None, "", " ", "BUY", "SELL", "INVALIDO"])
def test_normalize_position_side_rejects_invalid_values(raw):
    with pytest.raises(ValueError):
        normalize_position_side(raw)
