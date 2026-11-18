from __future__ import annotations
from src.menu_command import MenuCommand


class ConsoleMenu:
    def __init__(self) -> None:
        self._commands: dict[str, MenuCommand] = {}
        self._running = False

    def register(self, key: str, command: MenuCommand) -> None:
        self._commands[key] = command

    def stop(self) -> None:
        self._running = False

    def run(self) -> None:
        self._running = True
        while self._running:
            print('Choose option:')
            for key, cmd in self._commands.items():
                print(f'{key} - {cmd.label}')
            command = self._commands.get(input().strip())
            if command is None:
                print('Unknown option, try again...')
            else:
                command.execute()