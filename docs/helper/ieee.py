from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import pyperclip
import os

REQ_AUTHOR = "Author: "

AUTHOR_EXIT = "none"

def get_authors() -> str:
    authors = ""
    author = input(REQ_AUTHOR)

    while author != AUTHOR_EXIT:
        authors += author        
        author = input(REQ_AUTHOR)
        if author != AUTHOR_EXIT:
            authors += ", "

    if authors != "":
        authors += ". "

    return authors

REQ_URL = "URL: "

def get_url() -> tuple[str, str]:
    url = input(REQ_URL)
    try:
        soup = BeautifulSoup(urlopen(url), features="html.parser")
        website_title = soup.title.get_text()
        return url, website_title
    except Exception:
        print("could not read page")
        website_title = input("Website Title: ")
        return url, website_title

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

ieee_citation = "{authors}\"{page_title}\" {website_title}. Accessed: {month}. {day}, {year}. [Online.] Available: {url}"

def get_citation():
    authors = get_authors()
    page_title = input("Title: ")
    url, website_title = get_url()
    now = datetime.now()

    citation = ieee_citation.format(
        authors=authors,
        page_title=page_title,
        website_title=website_title,
        month = months[now.month],
        day = now.day,
        year = now.year,
        url = url
    )

    return citation

if __name__ == "__main__":
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("IEEE Citation\ninput ^C to quit")
            citation = get_citation()
            print(citation)
            pyperclip.copy(citation)
            input("press Enter to continue ...")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e) 