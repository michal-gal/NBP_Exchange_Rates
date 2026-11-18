from abc import ABC, abstractmethod


class MenuCommand(ABC):
    label: str

    @abstractmethod
    def execute(self) -> None:
        pass



