# tests/conftest.py
import pytest
from decimal import Decimal
from src.currency import Currency
from pathlib import Path

USD = Currency("dolar amerykański", "USD", Decimal("4.00"), 1)
PLN = Currency("złoty polski", "PLN", Decimal("1.00"), 1)
HUF = Currency("forint węgierski", "HUF",Decimal("1.1500"), 100)

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

SAMPLE_PATH = str(Path(__file__).parent / "sample.xml")


@pytest.fixture
def usd():
    return Currency("dolar amerykański", "USD", Decimal("4.00"), 1)

@pytest.fixture
def pln():
    return Currency("złoty polski", "PLN", Decimal("1.00"), 1)

@pytest.fixture
def huf():
    return Currency("forint węgierski", "HUF", Decimal("1.1500"), 100)


