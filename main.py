from console_view import ConsoleView, ConsoleMenu
from rate_table import RateTable
from currency_converter import CurrencyConverter
from rate_parser import RateParser
from fetch_data import HttpRateSource
from conversion import ViaPlnStrategy

table = RateTable()
view = ConsoleView()
table.attach(view)          # po udanym refresh zobaczysz "Loaded N currencies"
converter = CurrencyConverter(HttpRateSource(), RateParser(), table, ViaPlnStrategy())
if not converter.refresh():
    print('Could not download rates. Use option 3 to try again.')
ConsoleMenu(view, table, converter).run()