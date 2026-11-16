from src.fetch_data import RateSource
from src.rate_parser import RateParser
from src.rate_table import RateTable, UnknownCurrencyError, Observer
from src.currency_converter import CurrencyConverter, ConverterNotReadyError
from src.fetch_data import FileRateSource
from src.conversion import ViaPlnStrategy, CommissionStrategy
from decimal import Decimal
import pytest
from conftest import USD, HUF, SAMPLE, SAMPLE_PATH

class FlakySource(RateSource):
    def __init__(self, data: bytes):
        self._data = data
        self._calls = 0

    def fetch(self) -> bytes:
        self._calls += 1
        if self._calls == 1:
            raise OSError("brak sieci")
        return self._data


@pytest.fixture
def fresh_converter():
    converter = CurrencyConverter(FileRateSource(SAMPLE_PATH), RateParser(), RateTable(), ViaPlnStrategy())
    return converter


@pytest.fixture
def ready_converter(fresh_converter):
    fresh_converter.refresh()
    return fresh_converter

def test_convert_before_refresh_raises(fresh_converter):
    with pytest.raises(ConverterNotReadyError):
        fresh_converter.convert(Decimal("10"), "USD", "PLN")

def test_convert_after_refresh(ready_converter):
    assert ready_converter.convert(Decimal("10"), "USD", "PLN") == Decimal("40.00")

def test_negative_amount_raises(ready_converter):
    with pytest.raises(ValueError):
        ready_converter.convert(Decimal("-1"), "USD", "PLN")

def test_unknown_currency_raises(ready_converter):
    with pytest.raises(UnknownCurrencyError):
        ready_converter.convert(Decimal("10"), "XYZ", "PLN")

def test_missing_file_goes_to_error_state():
    context = CurrencyConverter(FileRateSource("bad.xml"),RateParser(), RateTable(), ViaPlnStrategy())
    context.refresh()

    with pytest.raises(ConverterNotReadyError, match="nie udało"):
        context.convert(Decimal("10"), "USD", "PLN")

def test_fails_after_failed_refresh():
    data = FileRateSource(SAMPLE_PATH).fetch()
    flaky = CurrencyConverter(FlakySource(data), RateParser(), RateTable(), ViaPlnStrategy())

    flaky.refresh()
    with pytest.raises(ConverterNotReadyError, match="nie udało"):
        flaky.convert(Decimal("10"), "USD", "PLN")

def test_recovers_after_failed_refresh():
    data = FileRateSource(SAMPLE_PATH).fetch()
    flaky = CurrencyConverter(FlakySource(data), RateParser(), RateTable(), ViaPlnStrategy())
    flaky.refresh()
    with pytest.raises(ConverterNotReadyError, match="nie udało"):
        flaky.convert(Decimal("10"), "USD", "PLN")    
    flaky.refresh()                       
    assert flaky.convert(Decimal("10"), "USD", "PLN") == Decimal("40.00")

def test_commission_strategy_in_converter():
    commission = CurrencyConverter(FileRateSource(SAMPLE_PATH),RateParser(), RateTable(), CommissionStrategy(ViaPlnStrategy(), Decimal("0.05")) )
    commission.refresh()
    assert commission.convert(Decimal("10"), "USD", "PLN") == Decimal("38.00")
