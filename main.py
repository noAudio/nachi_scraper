import csv
from scraper import Scraper


def main() -> None:
    scraper: Scraper = Scraper()
    scraper.getData()
    print(len(scraper.results), 'inspectors')
    for inspector in scraper.results:
        inspector.website = scraper.getWebsite(inspector.profileLink)
        if inspector.website != 'n/a':
            index: int = scraper.results.index(inspector) + 1
            print(
                f'[{index}/{len(scraper.results)}: {inspector.name}, {inspector.profileLink}, {inspector.website}]')
    with open(f'inspectors.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Name of Company', 'Phone Number', 'Website'])
        for inspector in scraper.results:
            writer.writerow([f"{inspector.name.replace('"', '')}", f"{inspector.company.replace(
                '"', '')}", inspector.phone, f"{inspector.website.replace('"', '')}"])
        f.close()


if __name__ == '__main__':
    main()
