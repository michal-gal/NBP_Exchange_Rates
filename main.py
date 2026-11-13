from console_view import ConsoleView, ConsoleMenu
from rate_table import RateTable
from currency import Currency
from decimal import Decimal

table = RateTable()
view = ConsoleView() 
table.attach(ConsoleView())
table.load([
                Currency("dolar amerykański", "USD", Decimal("4.00"), 1), 
                Currency("Forint węgierski", "HUF",Decimal("1.1500"), 100)
            ])  
ConsoleMenu(view, table).run()