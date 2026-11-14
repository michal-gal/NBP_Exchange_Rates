from rate_table import RateTable
from decimal import Decimal
from currency_converter import CurrencyConverter, ConverterNotReadyError
from fetch_data import FileRateSource
from rate_parser import RateParser
from conversion import ViaPlnStrategy, CommissionStrategy
from fetch_data import RateSource


context = CurrencyConverter(FileRateSource("sample.xml"),RateParser(), RateTable(), ViaPlnStrategy())

try:
    context.convert(Decimal("10"), "USD", "PLN")
    assert False, "oczekiwano ConverterNotReadyError"
except ConverterNotReadyError:
        pass

context.refresh()

assert context.convert(Decimal("10"), "USD", "PLN") == Decimal("40.00")

try:
    context.convert(Decimal("-1"), "USD", "PLN")
    assert False, "oczekiwano ValueError"
except ValueError:
        pass

bad = CurrencyConverter(FileRateSource("bad.xml"),RateParser(), RateTable(), ViaPlnStrategy())
bad.refresh()
try:
    bad.convert(Decimal("10"), "USD", "PLN")
    assert False, "oczekiwano ConverterNotReadyError"
except ConverterNotReadyError as e:
    assert "nie udało" in str(e)

class FlakySource(RateSource):
    def __init__(self, data: bytes):
        self._data = data
        self._calls = 0

    def fetch(self) -> bytes:
        self._calls += 1
        if self._calls == 1:
            raise OSError("brak sieci")
        return self._data


data = FileRateSource("sample.xml").fetch()
flaky = CurrencyConverter(FlakySource(data), RateParser(), RateTable(), ViaPlnStrategy())

flaky.refresh()                       # 1. próba: OSError -> ErrorState
try:
    flaky.convert(Decimal("10"), "USD", "PLN")
    assert False, "oczekiwano ConverterNotReadyError"
except ConverterNotReadyError as e:
    assert "nie udało" in str(e)

flaky.refresh()                       # 2. próba: dane przychodzą -> ReadyState
assert flaky.convert(Decimal("10"), "USD", "PLN") == Decimal("40.00")

good = CurrencyConverter(FileRateSource("sample.xml"),RateParser(), RateTable(), ViaPlnStrategy())
good.refresh()
assert good.convert(Decimal("10"), "USD", "PLN") == Decimal("40.00")

commission = CurrencyConverter(FileRateSource("sample.xml"),RateParser(), RateTable(), CommissionStrategy(ViaPlnStrategy(), Decimal("0.05")) )
commission.refresh()
assert commission.convert(Decimal("10"), "USD", "PLN") == Decimal("38.00")

print("Wszytskie testy przeszły pomyślnie.")
