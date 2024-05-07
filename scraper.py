from typing import List

import requests
from bs4 import BeautifulSoup as bs4

from inspector import Inspector


class Scraper:
    baseLink: str = 'https://www.nachi.org/certified-inspectors/browse/us?page='
    pages: int = 105
    results: List[Inspector] = []

    def getData(self) -> None:
        for pageNo in range(self.pages):
            pageNo = pageNo + 1

            page: str = f'{self.baseLink}{pageNo}'
            print(f'Scraping page {pageNo} ({page})')
            response: requests.Response = requests.get(page)
            soup: bs4 = bs4(response.content, 'html.parser')

            rows = soup.select('tbody>tr')
            for row in rows:
                linkElem = row.find('a', class_='group')
                profileLink: str = linkElem.get('href')

                nameElem = row.find('div', class_='font-bold')
                name: str = nameElem.text.strip()

                companyElem = row.find('div', class_='mt-0.5')
                company: str = 'n/a'
                if companyElem != None:
                    company = companyElem.text.strip()

                serviceAreaElem = row.select_one('td:nth-child(2)')
                serviceArea: str = serviceAreaElem.text.strip()

                phoneElem = row.find('td', class_='tabular-nums')
                phone: str = phoneElem.text.strip() if phoneElem != None else 'n/a'

                inspector = Inspector(
                    name=name,
                    phone=phone,
                    company=company,
                    serviceArea=serviceArea,
                    profileLink=profileLink,
                )
                self.results.append(inspector)

    def getWebsite(self, profileLink: str) -> str:
        website: str = 'n/a'
        response: requests.Response = requests.get(profileLink)
        soup: bs4 = bs4(response.content, 'html.parser')
        possibleWebsiteElements = soup.find_all("a", attrs={"data-lead": True})
        if len(possibleWebsiteElements) > 0:
            website = possibleWebsiteElements[0].get('href')
        return website
