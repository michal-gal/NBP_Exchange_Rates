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


if  __name__ == "__main__":
    from rate_parser import RateParser

    file_fetcher = FileRateSource("sample.xml")
    data1 = file_fetcher.fetch()
    parser = RateParser()
    currencies = parser.parse(data1)
    print(currencies)
    assert len(currencies) == 3

    http_fetcher = HttpRateSource()
    data2 = http_fetcher.fetch()
    currencies = parser.parse(data2)
    print(len(currencies))
    print(currencies[1].name)    

