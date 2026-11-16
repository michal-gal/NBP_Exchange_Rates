from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from src.fetch_data import RateSource
from src.rate_parser import RateParser
from src.rate_table import RateTable
from src.conversion import ConversionStrategy
import xml.etree.ElementTree as ET

class CurrencyConverter:
    def __init__(self, source:RateSource, parser: RateParser, table: RateTable, strategy: ConversionStrategy):
        self.source = source
        self.parser = parser
        self.table = table
        self.strategy = strategy
        self._state = NoDataState()

    def set_state(self, state):
        self._state = state

    def convert(self, amount, src_code, dst_code):
        return self._state.convert(self, amount, src_code, dst_code)

    def refresh(self):
        return self._state.refresh(self)

class ConverterNotReadyError(Exception):
    pass

class ConverterState(ABC):

    @abstractmethod
    def convert(self,context, amount, src_code, dst_code):
        pass

    def refresh(self, context) -> bool:
        try:
            data = context.source.fetch()
            context.table.load(context.parser.parse(data))
        except (OSError, ET.ParseError, AttributeError):
            context.set_state(ErrorState())
            return False
        else:
            context.set_state(ReadyState())
            return True

class NoDataState(ConverterState):
    def convert(self, context, amount, src_code, dst_code):
        raise ConverterNotReadyError("Brak danych. Najpierw pobierz kursy.")

class ErrorState(ConverterState):
    def convert(self, context, amount, src_code, dst_code):
                raise ConverterNotReadyError("pobranie się nie udało")

class ReadyState(ConverterState):
    def convert(self, context, amount, src_code, dst_code):
        if amount < 0:
            raise ValueError("Amount must not be negative")
        src = context.table.get(src_code)
        dst = context.table.get(dst_code)
        result = context.strategy.convert(amount,src,dst)
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
