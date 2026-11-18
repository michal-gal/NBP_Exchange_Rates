from __future__ import annotations
from src.currency import Currency
from collections.abc import Iterable
from src.observer import Observer
from src.currency_converter import CurrencyConverter
from src.menu_command import MenuCommand
from decimal import Decimal, InvalidOperation
from src.rate_table import UnknownCurrencyError
from src.currency_converter import ConverterNotReadyError
from src.console_menu import ConsoleMenu

class ConsoleView(Observer):    

    def print_all(self,currencies: Iterable[Currency]) -> None:
        print('Currency name     Currency code     Average rate')
        for item in currencies:
            print(f'{item.name:<20}{item.code:<18}{item.rate_per_unit():.4f}')

    def update(self, currencies: tuple[Currency, ...]) -> None:
        print(f'Loaded {len(currencies)} currencies') 


class ShowCurrenciesCommand(MenuCommand):
    label = 'print all available currencies'

    def __init__(self, view: ConsoleView, converter: CurrencyConverter):
        self._view = view
        self._converter = converter

    def execute(self) -> None:
        try:
            currencies = self._converter.currencies()
        except ConverterNotReadyError as e:
            print(e)
        else:
            self._view.print_all(currencies)

class ConvertCommand(MenuCommand):
    label = 'find currency by code and calculate'

    def __init__(self,converter: CurrencyConverter):
        self._converter = converter

    def execute(self) -> None:
        text = input('Input amount: ').strip().replace(",", ".")
        try:
            amount = Decimal(text)
        except InvalidOperation:
            print('This is not a number')
            return
        src_code = input('Input source currency code: ').strip().upper()
        dst_code = input('Input destination currency code: ').strip().upper()
        try:
            result = self._converter.convert(amount, src_code, dst_code)
        except ValueError as e:
            print(e)
        except UnknownCurrencyError as e:
            print(f'Unknown currency code: {e}')
        except ConverterNotReadyError as e:
            print(e)
        else:
            print(f'{amount} {src_code} = {result} {dst_code}')

class RefreshCommand(MenuCommand):
    label = 'refresh data'

    def __init__(self, converter: CurrencyConverter):
        self._converter = converter

    def execute(self) -> None:
        if self._converter.refresh():
            print('Data refreshed')
        else:
            print('Data not refreshed')

class QuitCommand(MenuCommand):
    label = 'quit'

    def __init__(self, menu: ConsoleMenu):
        self._menu = menu

    def execute(self) -> None:
        print('Quitting...')
        self._menu.stop()
        





