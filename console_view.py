from rate_table import Observer, RateTable, UnknownCurrencyError

class ConsoleMenu:

    def __init__(self, view, table):
        self._view = view
        self._table = table
        

    def print_menu(self):
        print('Choose option:')
        print('1 - print all available currencies')
        print('2 - find currency by code and calculate')
        print('3 - quit')

    def run(self):
        while True:
            self.print_menu()
            choice = input()
            if choice == '1':
                self._view.print_all(self._table)
            elif choice == '2':
                code = input('Input currency code: ')
                self._view.find_and_calculate_by_code(self._table,code)
            elif choice == '3':
                break
            else:
                print('Unknown option, try again...')

class ConsoleView(Observer):    

    def print_all(self,table:RateTable):
        print('Currency name     Currency code     Average rate')
        for item in table:
            print(f'{item.name:<20}{item.code:<18}{item.rate_per_unit():.4f}')

    def find_and_calculate_by_code(self,table:RateTable, code:str):
            code = code.strip().upper()
            try:
                currency = table.get(code)
            except UnknownCurrencyError: 
                print('No such code in table')
                return
            print(f'Current rate for {currency.name} ({currency.code}) is {currency.rate_per_unit():.4f} PLN')

    def update(self, table):
        print(f'Loaded {len(table)} currencies') 