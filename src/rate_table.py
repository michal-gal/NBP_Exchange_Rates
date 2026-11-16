from abc import ABC, abstractmethod
from src.currency import Currency
from decimal import Decimal

class Observer(ABC):

    @abstractmethod
    def update(self,table):
        pass

class UnknownCurrencyError(KeyError):
    pass

class RateTable:

    def __init__(self):
        self._currencies = {}
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)


    def detach(self,observer: Observer):
        self._observers.remove(observer)

    def load(self, currencies_list: list[Currency]):
        self._currencies = {c.code: c for c in currencies_list}
        for observer in self._observers:
            observer.update(self)

    def get(self, code: str) -> Currency:
        try:
            return self._currencies[code]
        except KeyError:
            raise UnknownCurrencyError(code)

    
    def __len__(self):
        return len(self._currencies)

    def __iter__(self):
        return CurrencyIterator(list(self._currencies.values()))

class CurrencyIterator:
    def __init__(self, currencies_list: list[Currency]):
        self._currencies = currencies_list
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._currencies):
            raise StopIteration
        currency = self._currencies[self._index]
        self._index += 1
        return currency



    




