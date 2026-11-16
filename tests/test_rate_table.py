from src.rate_table import UnknownCurrencyError, Observer, RateTable
from decimal import Decimal
import pytest
from sample_data import USD, HUF


class CountingObserver(Observer):
    def __init__(self):
        self.calls = 0

    def update(self, table):
        self.calls += 1

@pytest.fixture
def sample_table():
    table = RateTable()
    table.load([USD, HUF])   
    return table


def test_observer_notified_on_load():
    table = RateTable()
    obs = CountingObserver()
    table.attach(obs)
    table.load([USD, HUF])         
    assert obs.calls == 1

def test_detached_observer_not_notified():
    table = RateTable()
    obs = CountingObserver()
    table.attach(obs)
    table.detach(obs)
    table.load([USD, HUF])               
    assert obs.calls == 0      


def test_independent_iteration(sample_table):
    pairs = 0
    for i in sample_table:
        for j in sample_table:
            pairs +=1 
    assert pairs == len(sample_table) ** 2

def test_iteration_returns_all_currencies(sample_table):
    assert len(list(sample_table)) == 2

def test_get_returns_currency(sample_table):       
    assert sample_table.get("HUF").rate_per_unit() == Decimal("0.0115")

def test_get_unknown_currency_raises(sample_table):
    with pytest.raises(UnknownCurrencyError):
        sample_table.get("XYZ")