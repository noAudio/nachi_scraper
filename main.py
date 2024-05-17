from bs4 import BeautifulSoup as bs4
import requests

import csv
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager

from typing import List, Tuple
from inspector import Inspector
from scraper import Scraper

completeList: List[Inspector] = []


def getWebsite(profileLink: str) -> str:
    website: str = 'n/a'
    response: requests.Response = requests.get(profileLink)
    soup: bs4 = bs4(response.content, 'html.parser')
    possibleWebsiteElements = soup.find_all("a", attrs={"data-lead": True})
    if len(possibleWebsiteElements) > 0:
        website = possibleWebsiteElements[0].get('href')
    return website


def main(start: int, end: int, scrapeList: List[Inspector], resultList: List[Inspector]) -> None:
    print(len(scrapeList), [start, end], len(scrapeList[start:end]))
    for inspector in scrapeList[start:end]:
        inspector.website = getWebsite(inspector.profileLink)
        resultList.append(inspector)
        if inspector.website != 'n/a':
            index: int = scrapeList.index(inspector) + 1
            print(
                f'[{index}/{len(scrapeList)}: {inspector.name}, {inspector.profileLink}, {inspector.website}]')


if __name__ == '__main__':
    args: List[Tuple[int, int]] = [(0, 868), (867, 1735), (1734, 2602), (2601, 3469), (3468, 4336), (
        4335, 5203), (5202, 6070), (6069, 6937), (6936, 7804), (7803, 8671), (8670, 9538), (9537, 10409)]

    scraper: Scraper = Scraper()
    scraper.getData()
    print(len(scraper.results), 'inspectors')

    with Manager() as manager:
        sharedList = manager.list()

        with ProcessPoolExecutor(max_workers=len(args)) as executor:
            results = list(executor.map(main, *zip(*args),
                                        [scraper.results] * len(args), [sharedList] * len(args)))
        completeList = list(sharedList)
    print(len(completeList))

    with open(f'inspectors.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Name of Company', 'Phone Number', 'Website'])
        for inspector in completeList:
            writer.writerow([f"{inspector.name.replace('"', '')}", f"{inspector.company.replace(
                '"', '')}", inspector.phone, f"{inspector.website.replace('"', '')}"])
        f.close()
