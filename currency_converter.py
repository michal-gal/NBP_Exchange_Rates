from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from fetch_data import RateSource
from rate_parser import RateParser
from rate_table import RateTable
from conversion import ConversionStrategy

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
        self._state.refresh(self)

class ConverterNotReadyError(Exception):
    pass

class ConverterState(ABC):

    @abstractmethod
    def convert(self,context, amount, src_code, dst_code):
        pass

    def refresh(self, context):
        try:
            data = context.source.fetch()
            context.table.load(context.parser.parse(data))
        except OSError:
            context.set_state(ErrorState())
        else:
            context.set_state(ReadyState())

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




