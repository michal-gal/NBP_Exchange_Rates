import xml.etree.ElementTree as ET
from decimal import Decimal
from src.currency import Currency

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
        





    

    

    
