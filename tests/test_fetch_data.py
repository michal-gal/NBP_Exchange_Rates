from src.rate_parser import RateParser
from src.fetch_data import FileRateSource
from conftest import SAMPLE_PATH

def test_fetching_from_file():
    file_fetcher = FileRateSource(SAMPLE_PATH)
    data1 = file_fetcher.fetch()
    parser = RateParser()
    currencies = parser.parse(data1)
    assert len(currencies) == 3
