from abc import ABC, abstractmethod
import urllib.request


class RateSource(ABC):
    @abstractmethod
    def fetch(self) -> bytes:
        pass


class FileRateSource(RateSource): 
    def __init__(self, path: str):
        self.path = path

    def fetch(self) -> bytes:
        with open(self.path,'rb') as file:
            data = file.read()
            return data



class HttpRateSource(RateSource):
    URL = "https://static.nbp.pl/dane/kursy/xml/LastA.xml"

    def fetch(self) -> bytes:
        with urllib.request.urlopen(self.URL, timeout=10) as response:
            data = response.read()
        return data


