from src.console_menu import ConsoleMenu
from src.console_view import ConvertCommand, ShowCurrenciesCommand, QuitCommand, ConsoleView
from src.currency_converter import CurrencyConverter
from src.rate_table import RateTable
from src.conversion import ViaPlnStrategy
from src.rate_parser import RateParser
from src.fetch_data import FileRateSource

def test_show_currencies_without_data_prints_message(capsys):
    converter = CurrencyConverter(FileRateSource("bad.xml"), RateParser(), RateTable(), ViaPlnStrategy())
    ShowCurrenciesCommand(ConsoleView(), converter).execute()
    assert "Download currency rates first" in capsys.readouterr().out

def test_quit_stops_menu():
    menu = ConsoleMenu()
    menu._running = True
    QuitCommand(menu).execute()
    assert menu._running is False

def test_convert_command_prints_result(monkeypatch, capsys, ready_converter):
    answers = iter(["10", "usd", "pln"])
    monkeypatch.setattr("builtins.input", lambda _="": next(answers))
    ConvertCommand(ready_converter).execute()
    assert "10 USD = 40.00 PLN" in capsys.readouterr().out

def test_convert_command_not_a_number(monkeypatch, capsys, ready_converter):
    monkeypatch.setattr("builtins.input", lambda _="": "abc")
    ConvertCommand(ready_converter).execute()
    assert "not a number" in capsys.readouterr().out