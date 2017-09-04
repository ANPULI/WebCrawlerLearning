import requests
from bs4 import BeautifulSoup
import codecs
import re
import sys

DOWNLOAD_URL = 'https://book.douban.com/top250'
rank = 1


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    book_list_soup = soup.find('div', attrs={'class': 'indent'})
    # book_title_list = []
    book_title_dict = {}
    global rank

    for book_table in book_list_soup.find_all('table'):
        detail = book_table.find('div', attrs={'class': 'pl2'})
        book_title = re.sub('\s', '', detail.find('a').getText())

        # book_title_list.append(book_title)
        rate_info = book_table.find('div', attrs={'class': 'star clearfix'})
        rating_num = rate_info.find('span', attrs={'class': 'rating_nums'}).getText()

        quote_info = book_table.find('p', attrs={'class': 'quote'})
        if quote_info is None:
            quote_content = None
        else:
            quote_content = quote_info.find('span', attrs={'class': 'inq'}).getText()

        book_title_dict[book_title] = [rank, rating_num, quote_content]

        print("Process: {}%".format(rank/2.5))
        rank += 1

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return book_title_dict, next_page['href']
    else:
        return book_title_dict, None


def main():
    url = DOWNLOAD_URL
    with codecs.open('books', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            books, url = parse_html(html)
            # fp.write(u'{books}\n'.format(books='\n'.join(books)))
            for book in books:
                fp.write(
                    u"No.{rank} {book} Rate: {rating_num}\n\t{quote_content}\n".format(rank=books[book][0], book=book,
                                                                                       rating_num=books[book][1],
                                                                                       quote_content=books[book][2]))


if __name__ == '__main__':
    main()
