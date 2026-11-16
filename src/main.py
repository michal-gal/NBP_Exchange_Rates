from src.console_view import ConsoleView, ConsoleMenu
from src.rate_table import RateTable
from src.currency_converter import CurrencyConverter
from src.rate_parser import RateParser
from src.fetch_data import HttpRateSource
from src.conversion import ViaPlnStrategy

table = RateTable()
view = ConsoleView()
table.attach(view)          # po udanym refresh zobaczysz "Loaded N currencies"
converter = CurrencyConverter(HttpRateSource(), RateParser(), table, ViaPlnStrategy())
if not converter.refresh():
    print('Could not download rates. Use option 3 to try again.')
ConsoleMenu(view, table, converter).run()