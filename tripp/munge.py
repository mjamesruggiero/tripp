from bs4 import BeautifulSoup
from collections import Counter
from time import sleep
import matplotlib.pyplot as pyplot
import re
import requests


def is_video(td):
    """It's a video if it has exactly one price label
    and if the stripped text inside that label starts with 'Video'"""
    pricelabels = td('span', 'pricelabel')
    return (len(pricelabels) == 1 and
            pricelabels[0].text.strip().startswith("video"))


def book_info(td):
    """Given a BeautifulSoup <td> representing a book,
    extract the book's details and return a dict"""
    title = td.find("div", "thumbheader").a.text
    by_author = td.find("div", "AuthorName").text
    authors = [x.strip() for x in re.sub("^By ", "", by_author).split(",")]
    isbn_link = td.find("div", "thumbheader").a.get("href")
    isbn = re.match("/product/(.*)\.do", isbn_link).groups()[0]
    date = td.find("span", "directorydate").text.strip()

    return {
        "title": title,
        "authors": authors,
        "isbn": isbn,
        "date": date,
    }


def scrape(num_pages=1):
    base_url = "http://shop.oreilly.com/category/browse-subjects/" + \
        "data.do?sortby=publicationDate&page="

    books = []
    for page_num in range(1, num_pages + 1):
        print "scraping page", page_num
        url = base_url + str(page_num)
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')

        for td in soup('td', 'thumbtext'):
            if not is_video(td):
                books.append(book_info(td))
        sleep(30)

    return books


def get_year(book):
    """Format is 'November 1999' so
    split on space and take second element"""
    return int(book["date"].split()[-1])


def plot_years(books, asset="/tmp/oreilly-books.png"):
    year_counts = Counter(get_year(book) for book in books)

    years = sorted(year_counts)
    book_counts = [year_counts[year] for year in years]

    print "year_counts: {}".format(year_counts)
    print "book_counts: {}".format(book_counts)

    pyplot.bar([x - 0.5 for x in years], book_counts)
    pyplot.xlabel("years")
    pyplot.ylabel("# of data books")
    pyplot.title("Data grows up")
    pyplot.savefig(asset)

if __name__ == '__main__':
    books = scrape(6)
    for book in books:
        print "->{0}".format(book)

    plot_years(books)
