from src.conversion import ViaPlnStrategy, CommissionStrategy
from decimal import Decimal, ROUND_HALF_UP
import pytest
from sample_data import USD, HUF, PLN

@pytest.mark.parametrize("amount, src, dst, expected", [
    (Decimal("10"), USD, PLN, Decimal("40.00")),
    (Decimal("40"), PLN, USD, Decimal("10.00")),
    (Decimal("100"), USD, HUF, Decimal("34782.61")),
    (Decimal("10"), USD, USD, Decimal("10.00")),
    (Decimal("10"), HUF, HUF, Decimal("10.00")),])
def test_via_pln_strategy(amount, src, dst, expected):
    result = ViaPlnStrategy().convert(amount, src, dst)
    assert result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == expected

@pytest.mark.parametrize("commission, amount, src, dst, expected", [
    (Decimal("0.05"), Decimal("10"), USD, PLN, Decimal("38.00")),
    (Decimal("0.05"), Decimal("100"), USD, HUF, Decimal("33043.48")),])
def test_via_commission_strategy(commission ,amount, src, dst, expected):
    result = CommissionStrategy(ViaPlnStrategy(), commission).convert(amount, src, dst)
    assert result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == expected

@pytest.mark.parametrize("commission", [Decimal("1"), Decimal("-0.1")])
def test_via_commission_strategy_incorrect_commission(commission):
    with pytest.raises(ValueError):
        CommissionStrategy(ViaPlnStrategy(), commission)