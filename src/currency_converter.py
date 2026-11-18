from __future__ import annotations
from typing import NoReturn
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from src.fetch_data import RateSource
from src.rate_parser import RateParser, RateParseError
from src.rate_table import RateTable
from src.conversion import ConversionStrategy
from collections.abc import Iterator
from src.currency import Currency

class CurrencyConverter:
    def __init__(self, source: RateSource, parser: RateParser, table: RateTable, strategy: ConversionStrategy):
        self.source = source
        self.parser = parser
        self.table = table
        self.strategy = strategy
        self._state = NoDataState()

    def set_state(self, state) -> None:
        self._state = state

    def convert(self, amount: Decimal, src_code: str, dst_code: str) -> Decimal:
        return self._state.convert(self, amount, src_code, dst_code)

    def refresh(self) -> bool:
        return self._state.refresh(self)

    def currencies(self) -> Iterator[Currency]:
        return self._state.currencies(self)

    def attach(self, observer) -> None:
        self.table.attach(observer)

class ConverterNotReadyError(Exception):
    pass


class ConverterState(ABC):

    @abstractmethod
    def convert(self, context: CurrencyConverter, amount: Decimal, src_code: str, dst_code: str) -> Decimal:
        pass

    @abstractmethod
    def currencies(self, context: CurrencyConverter)-> Iterator[Currency]: 
        pass     

    def _raise_failed(self) -> NoReturn:
        raise ConverterNotReadyError("No Data. Downloading currency rates failed.")

    def _raise_no_data(self) -> NoReturn:
        raise ConverterNotReadyError("No Data. Download currency rates first...")
    

    def refresh(self, context: CurrencyConverter) -> bool:
        try:
            data = context.source.fetch()
            currencies = context.parser.parse(data)
        except (OSError, RateParseError):
            context.set_state(ErrorState())
            return False
        context.table.load(currencies)
        context.set_state(ReadyState())
        return True

class NoDataState(ConverterState):
    def convert(self, context: CurrencyConverter, amount: Decimal, src_code: str, dst_code: str) -> Decimal:
        self._raise_no_data()

    def currencies(self, context: CurrencyConverter) -> Iterator[Currency]: 
        self._raise_no_data()


class ErrorState(ConverterState):
    def convert(self, context: CurrencyConverter, amount: Decimal, src_code: str, dst_code: str) -> Decimal:
        self._raise_failed()

    def currencies(self, context: CurrencyConverter) -> Iterator[Currency]: 
        self._raise_failed()


class ReadyState(ConverterState):
    def convert(self, context: CurrencyConverter, amount: Decimal, src_code: str, dst_code: str) -> Decimal:
        if amount < 0:
            raise ValueError("Amount must not be negative")
        src = context.table.get(src_code)
        dst = context.table.get(dst_code)
        result = context.strategy.convert(amount,src,dst)
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def currencies(self, context: CurrencyConverter) -> Iterator[Currency]: 
        return iter(context.table)

        