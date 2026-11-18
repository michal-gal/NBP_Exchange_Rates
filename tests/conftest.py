import pytest
from src.currency_converter import CurrencyConverter
from src.fetch_data import FileRateSource
from src.rate_parser import RateParser
from src.rate_table import RateTable
from src.conversion import ViaPlnStrategy
from sample_data import SAMPLE_PATH


@pytest.fixture
def fresh_converter():
    return CurrencyConverter(FileRateSource(SAMPLE_PATH), RateParser(), RateTable(), ViaPlnStrategy())


@pytest.fixture
def ready_converter(fresh_converter):
    fresh_converter.refresh()
    return fresh_converter