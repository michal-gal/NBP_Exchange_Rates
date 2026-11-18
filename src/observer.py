from abc import ABC, abstractmethod
from src.currency import Currency


class Observer(ABC):

    @abstractmethod
    def update(self, currencies: tuple[Currency, ...]) -> None:
        pass
