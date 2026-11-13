from abc import ABC, abstractmethod
from currency import Currency
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
        

if  __name__ == "__main__":
    USD = Currency("dolar amerykański", "USD", Decimal("4.00"), 1)
    PLN = Currency("złoty polski", "PLN", Decimal("1.00"), 1)
    HUF = Currency("forint węgierski", "HUF",Decimal("1.1500"), 100)
    strategy = ViaPlnStrategy()
    assert strategy.convert(Decimal("10"), USD, PLN)   == Decimal("40.00")
    assert strategy.convert(Decimal("40"), PLN, USD) == Decimal("10.00")
    result = strategy.convert(Decimal("100"), USD, HUF).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    assert result == Decimal("34782.61")    
    assert strategy.convert(Decimal("10"), USD, USD) == Decimal("10.00")
    assert strategy.convert(Decimal("10"), HUF, HUF) == Decimal("10.00")
    strategy = CommissionStrategy(ViaPlnStrategy(), Decimal("0.05"))    
    assert strategy.convert(Decimal("10"), USD, PLN) == Decimal("38.00")
    result = strategy.convert(Decimal("100"), USD, HUF).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) 
    assert result == Decimal("33043.48")



