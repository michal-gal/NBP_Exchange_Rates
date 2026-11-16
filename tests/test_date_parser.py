from src.rate_parser import RateParser
from decimal import Decimal
from conftest import SAMPLE
import pytest

@pytest.fixture
def by_code_dict():
    parser = RateParser()
    data_utf8 = SAMPLE.encode("utf-8")
    currencies = parser.parse(data_utf8)
    by_code = {c.code: c for c in currencies}
    return by_code


def test_parse_adds_pln(by_code_dict):
    assert "PLN" in by_code_dict

def test_parse_checks_huf(by_code_dict):
    assert by_code_dict["HUF"].rate_per_unit() == Decimal("0.0115")

def test_parse_utf8(by_code_dict):
    assert by_code_dict["USD"].name == "dolar amerykański"

def test_parse_iso_8859_2():
    parser = RateParser()
    SAMPLE_ISO = SAMPLE.replace('encoding="utf-8"', 'encoding="ISO-8859-2"')
    data_iso = SAMPLE_ISO.encode("iso-8859-2")
    currencies_iso = parser.parse(data_iso)
    by_code = {c.code: c for c in currencies_iso}
    assert by_code["USD"].name == "dolar amerykański"            
