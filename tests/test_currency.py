
from src.currency import Currency
from decimal import Decimal
import pytest
from conftest import USD, HUF


def test_rate_per_unit_usd():
    assert USD.rate_per_unit() == Decimal("4.00")

def test_rate_per_unit_huf():
    assert HUF.rate_per_unit() == Decimal("0.0115")

def test_multiplier_zero_raises():
    with pytest.raises(ValueError):
        Currency("Currency", "CUR", Decimal("1"), 0)