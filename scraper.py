from typing import List
from inspector import Inspector


class Scraper:
    link: str = ''
    results: List[Inspector] = []

    def getData(self) -> None:
        pass
