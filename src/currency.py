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


