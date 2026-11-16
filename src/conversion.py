from abc import ABC, abstractmethod
from src.currency import Currency
from decimal import Decimal, ROUND_HALF_UP


class ConversionStrategy(ABC):

    @abstractmethod
    def convert(self, amount:Decimal, src: Currency, dst: Currency) -> Decimal:
        pass

class ViaPlnStrategy(ConversionStrategy):

    def convert(self, amount: Decimal, src: Currency, dst:Currency) -> Decimal:
        return (amount * src.rate_per_unit() / dst.rate_per_unit())

class CommissionStrategy(ConversionStrategy):

    def __init__(self, base: ConversionStrategy, commission: Decimal):
        if  not (Decimal("0") <=  commission < Decimal("1")):
            raise ValueError("Commission must be in range 0 - 1")
        self._commission = commission
        self._base = base



    def convert(self, amount:Decimal, src: Currency, dst:Currency) -> Decimal:
        return self._base.convert(amount, src, dst) * (1 - self._commission)