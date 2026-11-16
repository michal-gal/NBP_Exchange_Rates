from src.rate_table import Observer, RateTable, UnknownCurrencyError
from src.currency_converter import CurrencyConverter, ConverterNotReadyError
from decimal import Decimal, InvalidOperation


class ConsoleMenu:

    def __init__(self, view, table, converter: CurrencyConverter):
        self._view = view
        self._table = table
        self._converter = converter

    def print_menu(self):
        print('Choose option:')
        print('1 - print all available currencies')
        print('2 - find currency by code and calculate')
        print('3 - refresh data')
        print('4 - quit')

    def _convert_dialog(self):
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

    def run(self):
        while True:
            self.print_menu()
            choice = input()
            if choice == '1':
                self._view.print_all(self._table)
            elif choice == '2':
                self._convert_dialog()
            elif choice == '3':
                if self._converter.refresh():
                    print('Data refreshed')
                else:
                    print('Data not refreshed')

            elif choice == '4':
                print('Quitting...')
                break
            else:
                print('Unknown option, try again...')

class ConsoleView(Observer):    

    def print_all(self,table:RateTable):
        print('Currency name     Currency code     Average rate')
        for item in table:
            print(f'{item.name:<20}{item.code:<18}{item.rate_per_unit():.4f}')

    def update(self, table):
        print(f'Loaded {len(table)} currencies') 