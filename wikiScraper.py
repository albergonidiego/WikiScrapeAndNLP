# inspired by https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/

import requests
import tools
from bs4 import BeautifulSoup

def scrape_Wiki(url):
    response = requests.get(
        url=url,
    )

    if response is not None:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the whole lot prettified
        # print(soup.prettify())

        # Get and print page title
        pagetitle = soup.find(id="firstHeading")
        title = pagetitle.text

        # Get and print the paragraph titles
        # allparagraphs = soup.find(id="bodyContent").find_all("h2")
        # for h2_tag in allparagraphs:
        #     str = h2_tag.text
        #     str = str.replace('[edit]', '')
        #     print(str)

        # Get and print the actual text
        alltext = soup.find(id="bodyContent").find_all("p")
        testo = ""
        for p_tag in alltext:
            if p_tag.text.startswith("Coordinates: "):
                print(p_tag.text)
            else:
                testo = testo + p_tag.text

        testo = tools.remove_things_in_sq_brackets(testo)
        testo = tools.remove_blank_lines((testo))
        fileSaved = tools.salva_txt(testo, title)
        # tools.remove_blank_lines(fileSaved)
        print(fileSaved + ' saved')

        return testo, title


if __name__ == "__main__":
    scrape_Wiki('https://en.wikipedia.org/wiki/Versace')