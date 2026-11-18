from src.console_view import ConsoleView, ShowCurrenciesCommand, RefreshCommand, ConvertCommand, QuitCommand
from src.console_menu import ConsoleMenu
from src.rate_table import RateTable
from src.currency_converter import CurrencyConverter
from src.rate_parser import RateParser
from src.fetch_data import HttpRateSource
from src.conversion import ViaPlnStrategy

if __name__ == "__main__":

    view = ConsoleView()
    converter = CurrencyConverter(HttpRateSource(), RateParser(), RateTable(), ViaPlnStrategy())
    converter.attach(view)         
    if not converter.refresh():
        print('Could not download rates. Use option 3 to try again.')
    menu = ConsoleMenu()
    menu.register('1', ShowCurrenciesCommand(view, converter))
    menu.register('2', ConvertCommand(converter))
    menu.register('3', RefreshCommand(converter))
    menu.register('4', QuitCommand(menu))
    menu.run()