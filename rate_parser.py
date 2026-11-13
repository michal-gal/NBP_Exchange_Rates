import xml.etree.ElementTree as ET
from decimal import Decimal
from currency import Currency

PLN = Currency("Polski złoty", "PLN", Decimal("1"), 1)

class RateParser:
    def parse(self, xml_data: bytes) -> list[Currency]:
        currencies = [PLN] 
        root = ET.fromstring(xml_data)
        for elem in root.findall('pozycja'):
            name = elem.find('nazwa_waluty').text
            multiplier = int(elem.find('przelicznik').text)
            code = elem.find('kod_waluty').text
            mid_rate = elem.find('kurs_sredni').text
            mid_rate = Decimal(mid_rate.replace(',','.'))

            currency = Currency(name, code, mid_rate, multiplier)
            currencies.append(currency)
        return currencies
        


if __name__ == "__main__":

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

    assert PLN in currencies

    assert by_code["USD"].name == "dolar amerykański"

    SAMPLE_ISO = SAMPLE.replace('encoding="utf-8"', 'encoding="ISO-8859-2"')
    data_iso = SAMPLE_ISO.encode("iso-8859-2")
    currencies_iso = parser.parse(data_iso)
    assert {c.code: c for c in currencies_iso}["USD"].name == "dolar amerykański"

    print("Wszystkie testy przeszły")
            
    


    

    

    
