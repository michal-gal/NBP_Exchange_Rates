from decimal import Decimal
from dataclasses import dataclass

@dataclass(frozen=True)
class Currency:
    name: str
    code: str
    mid_rate: Decimal
    multiplier: int = 1

    def __post_init__(self):
        if self.multiplier <= 0:
            raise ValueError("multiplier must be greater than 0")

    def rate_per_unit(self) -> Decimal:
        return self.mid_rate / self.multiplier

if __name__ == "__main__":

    # 1. USD
    usd = Currency("dolar amerykański", "USD", Decimal("4.00"), 1)
    assert usd.rate_per_unit() == Decimal("4.00")

    # 2. HUF
    mid_rate=Decimal("1.1500")
    multiplier=100
    huf = Currency("Forint węgierski", "HUF", mid_rate, multiplier)
    assert huf.rate_per_unit() == Decimal("0.0115")

    # 3. multiplier = 0
    try:
        Currency("Currency", "CUR", Decimal("1"), 0)
        assert False, "oczekiwano ValueError"
    except ValueError:
        pass
    print("Wszystkie testy przeszły")