import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation
from src.currency import Currency

PLN = Currency("Polski złoty", "PLN", Decimal("1"), 1)


class RateParseError(Exception):
    pass


def _text(elem: ET.Element, tag: str) -> str:
    child = elem.find(tag)
    if child is None or child.text is None:
        raise RateParseError(f"Missing field: {tag}")
    return child.text


class RateParser:

    def parse(self, xml_data: bytes) -> list[Currency]:
        currencies = [PLN] 
        try:
            root = ET.fromstring(xml_data)
            for elem in root.findall('pozycja'):
                name = _text(elem, 'nazwa_waluty')
                multiplier = int(_text(elem,'przelicznik'))
                code = _text(elem, 'kod_waluty')
                mid_rate = Decimal(_text(elem, 'kurs_sredni').replace(',', '.'))
                currencies.append(Currency(name, code, mid_rate, multiplier))
        except (ET.ParseError, ValueError, InvalidOperation) as e:
            raise RateParseError("Invalid rates data.") from e
        return currencies
        





    

    

    
