from src.fetch_data import RateSource
from src.rate_parser import RateParser
from src.rate_table import RateTable, UnknownCurrencyError, Observer
from decimal import Decimal
from src.currency_converter import CurrencyConverter, ConverterNotReadyError
from src.fetch_data import FileRateSource
from src.rate_parser import RateParser
from src.conversion import ViaPlnStrategy, CommissionStrategy
from src.currency import Currency
from decimal import Decimal, ROUND_HALF_UP


#
# fetch_data
#
def test_feching_from_file():
    file_fetcher = FileRateSource("sample.xml")
    data1 = file_fetcher.fetch()
    parser = RateParser()
    currencies = parser.parse(data1)
    assert len(currencies) == 3

#
# currency
#

# 1. USD
def test_check_currency():
    usd = Currency("dolar amerykański", "USD", Decimal("4.00"), 1)
    assert usd.rate_per_unit() == Decimal("4.00")

    # 2. HUF
    mid_rate=Decimal("1.1500")
    multiplier=100
    huf = Currency("Forint węgierski", "HUF", mid_rate, multiplier)
    assert huf.rate_per_unit() == Decimal("0.0115")

    # 3. multiplier = 0
    try:
        Currency("Currency", "CUR", Decimal("1"), 0)
        assert False, "oczekiwano ValueError"
    except ValueError:
        pass

#
# Rate parser
#

def test_rate_parser():
    SAMPLE = """<?xml version="1.0" encoding="utf-8"?>
        <tabela_kursow typ="A">
        <numer_tabeli>001/A/NBP/2026</numer_tabeli>
        <data_publikacji>2026-01-02</data_publikacji>
        <pozycja>
            <nazwa_waluty>dolar amerykański</nazwa_waluty>
            <przelicznik>1</przelicznik>
            <kod_waluty>USD</kod_waluty>
            <kurs_sredni>4,0000</kurs_sredni>
        </pozycja>
        <pozycja>
            <nazwa_waluty>forint (Węgry)</nazwa_waluty>
            <przelicznik>100</przelicznik>
            <kod_waluty>HUF</kod_waluty>
            <kurs_sredni>1,1500</kurs_sredni>
        </pozycja>
        </tabela_kursow>"""

    parser = RateParser()

    data_utf8 = SAMPLE.encode("utf-8")
    currencies = parser.parse(data_utf8)

    assert len(currencies) == 3

    by_code = {c.code: c for c in currencies}
    assert by_code["HUF"].rate_per_unit() == Decimal("0.0115")


    assert by_code["USD"].name == "dolar amerykański"

    SAMPLE_ISO = SAMPLE.replace('encoding="utf-8"', 'encoding="ISO-8859-2"')
    data_iso = SAMPLE_ISO.encode("iso-8859-2")
    currencies_iso = parser.parse(data_iso)
    assert {c.code: c for c in currencies_iso}["USD"].name == "dolar amerykański"
            
#
# RateTable
#

class CountingObserver(Observer):
    def __init__(self):
        self.calls = 0

    def update(self, table):
        self.calls += 1


def test_rate_table():
    table = RateTable()
    obs = CountingObserver()
    table.attach(obs)
    table.load([
            Currency("dolar amerykański", "USD", Decimal("4.00"), 1), 
            Currency("Forint węgierski", "HUF",Decimal("1.1500"), 100)
        ])          # użyj PLN i HUF z poprzednich kroków
    assert obs.calls == 1

    table.detach(obs)
    table.load([
                Currency("dolar amerykański", "USD", Decimal("4.00"), 1), 
                Currency("Forint węgierski", "HUF",Decimal("1.1500"), 100)
            ])          # użyj PLN i HUF z poprzednich kroków
    assert obs.calls == 1      # po detach licznik się nie zmienia

    assert len(list(table)) == 2
    assert table.get("HUF").rate_per_unit() == Decimal("0.0115")

    try:
        table.get("XYZ")
        assert False, "oczekiwano UnknownCurrencyError"
    except UnknownCurrencyError:
        pass

#
# Strategy
# 

def test_strategy():
    USD = Currency("dolar amerykański", "USD", Decimal("4.00"), 1)
    PLN = Currency("złoty polski", "PLN", Decimal("1.00"), 1)
    HUF = Currency("forint węgierski", "HUF",Decimal("1.1500"), 100)
    strategy = ViaPlnStrategy()
    assert strategy.convert(Decimal("10"), USD, PLN)   == Decimal("40.00")
    assert strategy.convert(Decimal("40"), PLN, USD) == Decimal("10.00")
    result = strategy.convert(Decimal("100"), USD, HUF).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    assert result == Decimal("34782.61")    
    assert strategy.convert(Decimal("10"), USD, USD) == Decimal("10.00")
    assert strategy.convert(Decimal("10"), HUF, HUF) == Decimal("10.00")
    strategy = CommissionStrategy(ViaPlnStrategy(), Decimal("0.05"))    
    assert strategy.convert(Decimal("10"), USD, PLN) == Decimal("38.00")
    result = strategy.convert(Decimal("100"), USD, HUF).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) 
    assert result == Decimal("33043.48")

#
# converter
#
def test_converter():
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

def test_final():
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

